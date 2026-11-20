"""Independent synthetic mechanism experiment. No real identities or vendor implementation."""
from pathlib import Path
import json,hashlib,time
import numpy as np
import pandas as pd
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error,mean_squared_error,median_absolute_error

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'results';OUT.mkdir(exist_ok=True)
SCENARIOS=['individual_signal','group_sufficient','source_shift']
SEEDS=[731,732,733];RATES=[0,.01,.05,.10,.20]

def generate(n,seed,scenario,k,test=False):
    r=np.random.default_rng(seed);group=r.integers(0,8,n);onehot=np.eye(8)[group]
    gv=np.array([-1,-.7,-.4,-.1,.1,.4,.7,1])[group];z=r.normal(size=n)
    gc,ic=(1.2,.12) if scenario=='group_sufficient' else (.35,1.)
    logvalue=1.1+gc*gv+ic*z+.35*r.normal(size=n)
    payer=r.random(n)<1/(1+np.exp(-(-.2+.4*gv+.5*ic*z)))
    y=np.exp(logvalue)*payer
    # Historical observations stand in for events on 8 apps and 2 simulated devices.
    hist=z[:,None,None]+.25*gv[:,None,None]+r.normal(0,1.8/np.sqrt(k),size=(n,2,8))
    if scenario=='source_shift' and test:
        hist[:,1,:]=-.6*z[:,None]+.25*gv[:,None]+r.normal(0,1.8/np.sqrt(k),size=(n,8))
    a=np.column_stack([onehot,hist[:,0,0]])
    b=np.column_stack([a,hist[:,0,1:].mean(axis=1)])
    peer=hist[:,1,:].mean(axis=1)
    c=np.column_stack([b,peer])
    # t0 0/30/60 by role recorded in run manifest, all history before it and y after.
    return dict(y=y,group=group,A=a,B=b,C=c,peer=peer)

def fit(x,y):
    m=make_pipeline(StandardScaler(),Ridge(alpha=10))
    m.fit(x,np.log1p(y));return m
def pred(m,x):return np.maximum(0,np.expm1(m.predict(x)))
def score(y,p):
    n=len(y);k=max(1,int(np.ceil(.1*n)));truth=np.argsort(-y,kind='stable')[:k];top=np.argsort(-p,kind='stable')[:k]
    return dict(mae=float(mean_absolute_error(y,p)),rmse=float(np.sqrt(mean_squared_error(y,p))),median_ae=float(median_absolute_error(y,p)),recall_at_10=float(len(np.intersect1d(truth,top))/k),top10_amount_capture=float(y[top].sum()/y.sum()),total_bias=float(p.sum()/y.sum()-1))
def bootstrap_delta(y,p,base,r):
    ix=r.integers(0,len(y),size=(200,len(y)))
    delta=(np.abs(y-p)-np.abs(y-base))[ix].mean(axis=1)
    lo,hi=np.quantile(delta,[.025,.975]);return float(lo),float(hi)

def main():
    assert (ROOT/'PREREGISTRATION.md').is_file()
    config=dict(data_type='SYNTHETIC_ONLY',seeds=SEEDS,scenarios=SCENARIOS,history_counts=[1,8],target_train_sizes=[2000,150],source_train_size=6000,validation_size=500,test_size=3000,rates=RATES,estimator='StandardScaler + Ridge(alpha=10), log1p target',test_users_disjoint=True,real_data_used=False,training_rates='correct peer at train;perturbed peer only at test',history_before_prediction=True,label_after_prediction=True,t0_roles=dict(train=0,validation=30,test=60),notes=['E_shared has extra source training rows;not an equal-data-budget proof','Group-only priors use mature synthetic source-training labels only','No user/device/app ID used directly as feature','Metrics are generated units,not monetary ROAS'])
    cf=OUT/'D_CONFIG.json';assert not cf.exists(),'Do not overwrite previous run'
    cf.write_text(json.dumps(config,indent=2),encoding='utf-8')
    rows=[];checks=[];start=time.time()
    for si,scenario in enumerate(SCENARIOS):
      for k in [1,8]:
       for nt in [2000,150]:
        for seed in SEEDS:
            base_seed=seed+si*10000+k*100+nt
            tr=generate(nt,base_seed,scenario,k)
            # Validation reserved under protocol;no tuning/calibration uses it in this fixed baseline.
            va=generate(500,base_seed+200000,scenario,k)
            te=generate(3000,base_seed+400000,scenario,k,test=True)
            so=generate(6000,base_seed+600000,scenario,k)
            models={key:fit(tr[key],tr['y']) for key in ['A','B','C']}
            predictions={key:pred(m,te[key]) for key,m in models.items()}
            means=np.array([so['y'][so['group']==g].mean() for g in range(8)])
            predictions['E_group']=means[te['group']]
            shared=fit(np.vstack([so['A'],tr['A']]),np.r_[so['y'],tr['y']])
            predictions['E_shared']=pred(shared,te['A'])
            random=np.random.default_rng(base_seed+800000)
            for rate in RATES:
                nwrong=int(round(rate*len(te['y'])));ix=random.permutation(len(te['y']))[:nwrong]
                donor=np.arange(len(te['y']))
                if nwrong>=2:donor[ix]=np.roll(ix,1)
                x=np.column_stack([te['B'],te['peer'][donor]])
                p=pred(models['C'],x);predictions[f'D_{int(rate*100):02}']=p
                checks.append(dict(scenario=scenario,k=k,nt=nt,seed=seed,rate=rate,actual_wrong=int(np.sum(donor!=np.arange(len(donor)))),expected_wrong=nwrong,zero_equals_oracle=bool(np.array_equal(p,predictions['C'])) if rate==0 else None))
            for name,p in predictions.items():
                met=score(te['y'],p);lo,hi=bootstrap_delta(te['y'],p,predictions['A'],np.random.default_rng(base_seed+900000))
                rows.append(dict(experiment='D',data_type='SYNTHETIC_ONLY',scenario=scenario,history_per_app_device=k,target_train_n=nt,source_train_n=6000 if name.startswith('E_') else 0,test_n=len(te['y']),seed=seed,model=name,nominal_false_link_rate=float(name[2:])/100 if name.startswith('D_') else None,zero_fraction=float(np.mean(te['y']==0)),**met,mae_delta_vs_A=met['mae']-score(te['y'],predictions['A'])['mae'],mae_delta_vs_C=met['mae']-score(te['y'],predictions['C'])['mae'],mae_delta_vs_A_ci_low=lo,mae_delta_vs_A_ci_high=hi))
    df=pd.DataFrame(rows);df.to_csv(OUT/'D_RESULTS.csv',index=False,encoding='utf-8-sig')
    agg=df.groupby(['scenario','history_per_app_device','target_train_n','model'],dropna=False).agg(mae_mean=('mae','mean'),mae_sd=('mae','std'),rmse_mean=('rmse','mean'),recall_at_10_mean=('recall_at_10','mean'),top10_amount_capture_mean=('top10_amount_capture','mean'),mae_delta_vs_A_mean=('mae_delta_vs_A','mean'),mae_delta_vs_C_mean=('mae_delta_vs_C','mean')).reset_index()
    agg.to_csv(OUT/'D_AGGREGATE.csv',index=False,encoding='utf-8-sig')
    assert all(x['actual_wrong']==x['expected_wrong'] for x in checks)
    assert all(x['zero_equals_oracle'] is True for x in checks if x['rate']==0)
    (OUT/'D_CHECKS.json').write_text(json.dumps(dict(status='PASS',checks=checks,elapsed_seconds=time.time()-start,rows=len(rows),config_sha256=hashlib.sha256(cf.read_bytes()).hexdigest(),protocol_sha256=hashlib.sha256((ROOT/'PREREGISTRATION.md').read_bytes()).hexdigest()),indent=2),encoding='utf-8')
    print(json.dumps(dict(rows=len(rows),seconds=time.time()-start,checks='PASS')))
if __name__=='__main__':main()
