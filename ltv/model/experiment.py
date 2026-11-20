"""Synthetic, offline feature-ablation laboratory. NOT Axon/Vector implementation.

All history features exist before the simulated bid. Future install/D28 revenue are labels only.
No device identifiers, accounts, networking or production SDKs are used.
"""
from pathlib import Path
import sys,json,hashlib,math,platform
from dataclasses import asdict
import numpy as np
from sklearn.ensemble import HistGradientBoostingClassifier,HistGradientBoostingRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score,mean_squared_error
from scipy.stats import spearmanr
from threadpoolctl import threadpool_limits

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'auction/model'))
from auction_model import Auction,Offer,Profile,D

R=Path(__file__).resolve().parent;OUT=R/'output'
CONTEXT=['device_capacity','supply_app_category','creative_match','placement','hour_sin']
BEHAVIOR=['past_ad_engagement','past_session_proxy']
IDENTITY=['linked_past_value_proxy','linked_category_affinity']
FEATURES=CONTEXT+BEHAVIOR+IDENTITY+['behavior_available','identity_available']
ARMS={
 'install_only':CONTEXT,
 'context_ltv':CONTEXT,
 'context_behavior':CONTEXT+BEHAVIOR+['behavior_available'],
 'context_identity':CONTEXT+IDENTITY+['identity_available'],
 'context_behavior_identity':FEATURES,
}
SHAPES=['diffuse','heavy_tail','identity_null']
SEEDS=[4101,4102,4103]

def sigmoid(x):return 1/(1+np.exp(-np.clip(x,-25,25)))

def generate(n,seed,shape):
 rng=np.random.default_rng(seed)
 ctx=rng.normal(size=(n,5));ctx[:,1]=rng.integers(0,4,n);ctx[:,3]=rng.integers(0,2,n)
 engagement=rng.normal(size=n);affinity=rng.normal(size=n)
 # Pre-bid synthetic summaries from OTHER prior experiences, never future target-app events.
 behavior=np.column_stack([engagement+rng.normal(0,.65,n),.6*engagement+.25*affinity+rng.normal(0,.7,n)])
 identity=np.column_stack([affinity+rng.normal(0,.4,n),.6*affinity+.4*engagement+rng.normal(0,.55,n)])
 if shape=='identity_null':
  # A randomized synthetic identity with no extra predictive history; model is not guaranteed uplift.
  identity=rng.normal(size=(n,2))
 behavior_available=rng.random(n)<.85
 identity_available=rng.random(n)<.65 # hypothetical consent AND availability; not a real coverage estimate.
 behavior[~behavior_available]=np.nan;identity[~identity_available]=np.nan
 X=np.column_stack([ctx,behavior,identity,behavior_available.astype(float),identity_available.astype(float)])
 # Generate future outcomes AFTER feature construction. No label or future action is passed to X.
 p=sigmoid(-1.45+.45*ctx[:,0]+.55*ctx[:,2]+.45*engagement)
 log_mean=-.3+.25*ctx[:,0]+.16*(ctx[:,1]==2)+.65*engagement
 if shape!='identity_null':log_mean+=.65*affinity
 if shape=='heavy_tail':
  log_mean+=1.6*(affinity>1.25)
  sigma=.95
 else:sigma=.55
 conditional_mean=np.exp(np.clip(log_mean,-4,4))
 value=conditional_mean*np.exp(rng.normal(-sigma*sigma/2,sigma,n))
 install=rng.random(n)<p
 # Common inventory, competitors, timeline, price and realizations for every arm.
 floor=np.full(n,4.)
 rival=rng.lognormal(mean=4.05,sigma=.65,size=n)
 rival_latency=rng.choice([70,180,350],size=n,p=[.5,.4,.1])
 render_draw=rng.random(n)
 return dict(X=X,p=p,value=value,conditional_mean=conditional_mean,install=install,
             floor=floor,rival=rival,rival_latency=rival_latency,render_draw=render_draw,
             shape=shape,seed=seed)

def column_indices(names):return [FEATURES.index(x) for x in names]

def fit_model(train,cal,names,install_only=False):
 cols=column_indices(names)
 config=dict(max_iter=90,max_leaf_nodes=15,learning_rate=.08,l2_regularization=10,random_state=0)
 classifier=HistGradientBoostingClassifier(**config).fit(train['X'][:,cols],train['install'])
 cp=np.clip(classifier.predict_proba(cal['X'][:,cols])[:,1],1e-6,1-1e-6)
 # Separate calibration partition, never fit or select hyperparameters on held-out outcomes.
 platt=LogisticRegression(C=1e3).fit(np.log(cp/(1-cp)).reshape(-1,1),cal['install'])
 if install_only:
  reg=None;constant=float(np.mean(train['value'][train['install']]))
  raw=np.full(np.sum(cal['install']),constant)
 else:
  reg=HistGradientBoostingRegressor(loss='poisson',**config).fit(train['X'][train['install']][:,cols],train['value'][train['install']])
  constant=None;raw=np.maximum(reg.predict(cal['X'][cal['install']][:,cols]),1e-5)
 scale=float(np.sum(cal['value'][cal['install']])/np.sum(raw))
 return dict(classifier=classifier,platt=platt,reg=reg,cols=cols,constant=constant,scale=scale)

def predict(model,data):
 x=data['X'][:,model['cols']]
 p=np.clip(model['classifier'].predict_proba(x)[:,1],1e-6,1-1e-6)
 p=model['platt'].predict_proba(np.log(p/(1-p)).reshape(-1,1))[:,1]
 l=np.full(len(x),model['constant']) if model['reg'] is None else np.maximum(model['reg'].predict(x),1e-5)
 return p,l*model['scale']

def top_recall(y,pred):
 k=max(1,math.ceil(.1*len(y)))
 true=set(np.argsort(-y,kind='stable')[:k]);chosen=np.argsort(-pred,kind='stable')[:k]
 return len(true.intersection(chosen))/k,float(np.sum(y[chosen])/np.sum(y))

def metrics(data,p,l):
 installed=data['install'];y=data['value'][installed];pred=l[installed]
 bins=np.array_split(np.argsort(pred,kind='stable'),10)
 reliability=[dict(n=len(b),predicted_mean=float(np.mean(pred[b])),actual_mean=float(np.mean(y[b]))) for b in bins]
 ece=sum(abs(np.sum(pred[b])-np.sum(y[b])) for b in bins)/np.sum(y)
 recall,capture=top_recall(y,pred)
 decision_recall,decision_capture=top_recall(y,p[installed]*pred)
 return dict(install_auc=float(roc_auc_score(installed,p)),install_brier=float(np.mean((installed-p)**2)),
             ltv_predicted_to_actual=float(np.sum(pred)/np.sum(y)),ltv_decile_calibration_error=float(ece),
             conditional_ltv_rmse=float(np.sqrt(mean_squared_error(y,pred))),
             top10_value_recall=float(recall),top10_revenue_capture=capture,
             decision_score_top10_recall=float(decision_recall),decision_score_top10_revenue_capture=float(decision_capture),
             conditional_ltv_spearman=None if np.std(pred)<1e-10 else float(spearmanr(y,pred).statistic),
             calibration_bins=reliability,eligible_installs=int(np.sum(installed)),
             expected_revenue_mae=float(np.mean(np.abs(p*l-data['p']*data['conditional_mean']))))

def bid_curve(data,p,l,target_roas=1.0):
 # Teaching economic policy, unchanged across all feature/model arms, not vendor bidding logic.
 return np.clip(1000*p*l/target_roas*.8,0,400)

def tune_pacing(cal,p,l,budget=75.):
 base=bid_curve(cal,p,l)
 eligible_rival=np.where(cal['rival_latency']<=250,cal['rival'],0)
 # Only calibration inventory and shared render draws; no test outcomes enter pacing.
 def spend(k):
  b=base*k
  won=(b>cal['floor'])&(b>eligible_rival)&(cal['render_draw']>.05)
  return float(np.sum(b[won]/1000))
 lo=0.;hi=5.
 for _ in range(35):
  mid=(lo+hi)/2
  if spend(mid)>budget:hi=mid
  else:lo=mid
 return lo

def auction_evaluate(data,p,l,pacing,budget=225.):
 # Reuse the existing first-price engine; one common neutral profile for every arm.
 engine=Auction(Profile('offline_common',250,True))
 budgets={'advertiser':D(str(budget)),'competitor':D('1000000')}
 bids=bid_curve(data,p,l)*pacing
 spend=0.;wins=0;installs=0;revenue=0.;expected=0.;selected=[]
 for i,b in enumerate(bids):
  req='synthetic-ltv-'+str(i)
  offers=[Offer('advertiser',D(str(round(float(b),6))),request_id=req,render=data['render_draw'][i]>.05),
          Offer('competitor',D(str(round(float(data['rival'][i]),6))),latency_ms=int(data['rival_latency'][i]),request_id=req)]
  result=engine.run(offers,floor=D(str(data['floor'][i])),request_id=req,budgets=budgets)
  if result.selected=='advertiser' and result.rendered:
   spend+=float(result.billed_usd);wins+=1;selected.append(i)
   expected+=float(data['p'][i]*data['conditional_mean'][i])
   if data['install'][i]:installs+=1;revenue+=float(data['value'][i])
 # Sequence indices are local synthetic row numbers, never platform IDs.
 return dict(spend_usd=spend,budget_usd=budget,budget_utilization=spend/budget,rendered_wins=wins,
             acquired_installs=installs,realized_D28_revenue_usd=revenue,realized_D28_ROAS=revenue/spend if spend else None,
             synthetic_oracle_expected_revenue=expected,expected_D28_ROAS=expected/spend if spend else None,
             CPI=spend/installs if installs else None,pacing=pacing,
             selection_digest=hashlib.sha256(np.asarray(selected,dtype=np.int64).tobytes()).hexdigest())

def alter_features(data,mode,seed):
 d={**data,'X':data['X'].copy()};x=d['X'];rng=np.random.default_rng(seed)
 if mode=='identity_removed':
  x[:,7:9]=np.nan;x[:,10]=0
 elif mode=='wrong_links_30pct':
  idx=np.flatnonzero(x[:,10]==1);bad=idx[rng.random(len(idx))<.3]
  # Permute authorized-looking history, never use future labels to select mismatches.
  if len(bad):x[bad,7:9]=x[rng.choice(idx,len(bad),replace=True),7:9]
 elif mode=='privacy_limited':
  dropb=rng.random(len(x))>.3;dropi=rng.random(len(x))>.2
  x[dropb,5:7]=np.nan;x[dropb,9]=0;x[dropi,7:9]=np.nan;x[dropi,10]=0
 elif mode=='behavior_removed':
  x[:,5:7]=np.nan;x[:,9]=0
 else:raise ValueError(mode)
 return d

def inventory_digest(data):
 h=hashlib.sha256()
 for key in ['p','value','install','floor','rival','rival_latency','render_draw']:
  h.update(np.ascontiguousarray(data[key]).tobytes())
 return h.hexdigest()

def main():
 OUT.mkdir(exist_ok=True);rows=[];audit=[]
 with threadpool_limits(limits=2):
  for shape_no,shape in enumerate(SHAPES):
   for seed in SEEDS:
    s=seed+shape_no*10000
    train=generate(20000,s,shape);cal=generate(4000,s+100,shape);test=generate(12000,s+200,shape)
    digest=inventory_digest(test)
    audit.append(dict(shape=shape,seed=seed,train_n=20000,calibration_n=4000,test_n=12000,inventory_digest=digest,
     prebid_features=FEATURES,feature_time='synthetic historical days -30 to -1; available before bid',
     label_time='future install and mature D28 revenue',no_personal_identifiers=True,
     realized_value_mean=float(np.mean(test['value'])),realized_value_p99=float(np.quantile(test['value'],.99)),
     nominal_behavior_coverage=float(np.mean(test['X'][:,9])),nominal_identity_coverage=float(np.mean(test['X'][:,10]))))
    fitted={}
    for arm,names in ARMS.items():
     model=fit_model(train,cal,names,arm=='install_only');fitted[arm]=model
     cp,cl=predict(model,cal);p,l=predict(model,test);pace=tune_pacing(cal,cp,cl)
     row=dict(shape=shape,seed=seed,arm=arm,kind='trained_ablation',inventory_digest=digest,
              **metrics(test,p,l),**auction_evaluate(test,p,l,pace))
     rows.append(row)
     print(shape,seed,arm,'recall',round(row['top10_value_recall'],3),'ROAS',round(row['realized_D28_ROAS'],3),flush=True)
    # Deployed-model stress tests: same fitted full model, same inventory/outcomes; only observed features change.
    full=fitted['context_behavior_identity'];cp,cl=predict(full,cal);pace=tune_pacing(cal,cp,cl)
    for mode in ['identity_removed','wrong_links_30pct','privacy_limited','behavior_removed']:
     alt=alter_features(test,mode,s+300);assert inventory_digest(alt)==digest
     p,l=predict(full,alt)
     rows.append(dict(shape=shape,seed=seed,arm=mode,kind='inference_stress',inventory_digest=digest,
                      **metrics(alt,p,l),**auction_evaluate(alt,p,l,pace)))
    (OUT/'progress.json').write_text(json.dumps(dict(completed=len(rows),last_shape=shape,last_seed=seed)))
 result=dict(synthetic_only=True,not_vendor_comparison=True,seeds=SEEDS,shapes=SHAPES,
             fixed_common_auction=dict(tmax_ms=250,strict_floor=True,first_price=True,test_budget_usd=225),
             model='HistGradientBoosting classifier + conditional Poisson regressor; Platt/global scale calibration; NOT Axon or Vector',
             metrics_population='ranking and calibration on all synthetic held-out installed rows, NOT only auction winners; oracle expectations unavailable in production',
             rows=rows,audit=audit)
 (OUT/'results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
 print('COMPLETE',len(rows),'arms',flush=True)

if __name__=='__main__':main()
