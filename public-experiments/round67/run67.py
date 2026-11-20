"""Independent-time UCI invoice forecasts. No network; no platform/gaming inference."""
import os
os.environ['OMP_NUM_THREADS']='2'
os.environ['OPENBLAS_NUM_THREADS']='2'
from pathlib import Path
from datetime import datetime,timezone
import ast,json,csv,hashlib,zipfile,time,math,shutil,re
import numpy as np
import pandas as pd
import sklearn
from sklearn.ensemble import HistGradientBoostingRegressor,HistGradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from threadpoolctl import threadpool_limits

ROOT=Path(r'D:\GrowthResearch');OUT=ROOT/'public-experiments/round67'
OUT.mkdir(parents=True,exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,obj):
 (OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
def csvsave(name,rows):
 keys=[]
 for row in rows:
  for k in row:
   if k not in keys:keys.append(k)
 with (OUT/name).open('w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=keys,lineterminator='\n');w.writeheader();w.writerows(rows)

protocol=next(ROOT.glob('67_*协议.md'));raw=ROOT/'public-experiments/audit/retail352.download';source66=ROOT/'public-experiments/round66/run_experiment66.py'
if (OUT/'RUN_MANIFEST.json').exists():raise RuntimeError('Final run exists. Preserve it and use a separately named amended run, do not overwrite.')
history={}
for p in ROOT.glob('*'):
 if p.is_file() and re.match(r'\d\d_',p.name) and int(p.name[:2])<=66:history[p.relative_to(ROOT).as_posix()]=sha(p)
for p in (ROOT/'public-experiments/round66').rglob('*'):
 if p.is_file():history[p.relative_to(ROOT).as_posix()]=sha(p)
for rel in ['EVIDENCE_INDEX.md','prediction-system/EVIDENCE_GRAPH.json','public-experiments/audit/retail352.download']:
 history[rel]=sha(ROOT/rel)
save('HISTORY_BEFORE67.json',history)
shutil.copyfile(ROOT/'EVIDENCE_INDEX.md',OUT/'EVIDENCE_INDEX.before67.md')
shutil.copyfile(ROOT/'prediction-system/EVIDENCE_GRAPH.json',OUT/'EVIDENCE_GRAPH.before67.json')
run={'started_utc':datetime.now(timezone.utc).isoformat(),'protocol_path':protocol.relative_to(ROOT).as_posix(),'protocol_sha256':sha(protocol),
 'script_sha256':sha(Path(__file__)),'raw_sha256':sha(raw),'source66_sha256':sha(source66),'numpy':np.__version__,'pandas':pd.__version__,'sklearn':sklearn.__version__,
 'network_requests':0,'hyperparameter_searches':0,'test_used_for_tuning':False,'game_research_resumed':False,'raw_customer_keys_exported':False}
save('RUN_START.json',run)
assert run['raw_sha256']=='f5385cbb54bbebf7196389109c6b0621faab0c304e3702548165e71c84aede8b'
with zipfile.ZipFile(raw) as z:df=pd.read_excel(z.open('Online Retail.xlsx'),engine='openpyxl')
df['InvoiceDate']=pd.to_datetime(df.InvoiceDate);dedup=df.loc[~df.duplicated(keep='first')].copy()
tree=ast.parse(source66.read_text(encoding='utf-8'))
fnames=['bucket','dataframes','snapshots','topweights','metrics','rowaudit']
fnodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in fnames]
env=dict(np=np,pd=pd,math=math,hashlib=hashlib,df=df,dedup=dedup)
exec(compile(ast.Module(body=fnodes,type_ignores=[]),'reused_round66_visible_functions','exec'),env)
pos,ledger=env['dataframes'](False,False)
features=json.loads((ROOT/'public-experiments/round66/FEATURE_SCHEMA.json').read_text(encoding='utf-8'))
assert [len(features[n]) for n in ['M0','M1','M2']]==[2,8,18]
assert not set(['key','CustomerID','y28','y7','landmark','split']).intersection(set(sum(features.values(),[])))
old_dates={'train':list(pd.date_range('2011-01-03','2011-04-25',freq='W-MON')),
 'validation':list(pd.date_range('2011-06-06','2011-06-27',freq='W-MON')),'test':list(pd.date_range('2011-08-01','2011-08-29',freq='W-MON'))}
new_dates={'train':list(pd.date_range('2011-01-03','2011-07-25',freq='W-MON')),
 'validation':[pd.Timestamp('2011-08-29'),pd.Timestamp('2011-09-05')],
 'test':list(pd.date_range('2011-10-10','2011-11-07',freq='W-MON'))}
assert min(new_dates['test'])>max(old_dates['test'])+pd.Timedelta(days=28)
assert max(new_dates['train'])+pd.Timedelta(days=28)<min(new_dates['validation'])
assert max(new_dates['validation'])+pd.Timedelta(days=28)<min(new_dates['test'])
assert max(new_dates['test'])+pd.Timedelta(days=28)<df.InvoiceDate.max()
quality={'original_rows':len(df),'exact_duplicates_removed':len(df)-len(dedup),'dedup_rows':len(dedup),
 'dedup_missing_customer_rows':int(dedup.CustomerID.isna().sum()),'positive_eligible_rows':len(pos),'eligible_unique_customers':int(pos.key.nunique()),
 'event_min':str(df.InvoiceDate.min()),'event_max':str(df.InvoiceDate.max()),'final_test_label_end_exclusive':'2011-12-05',
 'dedup_audit':env['rowaudit'](dedup),'amount_unit':'recorded positive invoice sales GBP, not cash/net income',
 'available_at':'absent; event-time offline assumption only','zero_semantics':'No recorded positive invoice in horizon, not true zero consumption or permanent churn'}
save('DATA_QUALITY_AND_MATURITY.json',quality)
env['dates']=old_dates;frame66=env['snapshots'](pos,ledger)
env['dates']=new_dates;frame=env['snapshots'](pos,ledger)
train=frame.loc[frame.split=='train'].copy();val=frame.loc[frame.split=='validation'].copy();test=frame.loc[frame.split=='test'].copy()
for a,b in [(train,val),(train,test),(val,test)]:assert set(a.key).isdisjoint(set(b.key))
oldtestkeys=set(frame66.loc[frame66.split=='test','key']);newtestkeys=set(test.key)-oldtestkeys
splitcheck={'splits':{s:{'rows':int((frame.split==s).sum()),'unique_customers':int(frame.loc[frame.split==s,'key'].nunique()),'landmarks':sorted(frame.loc[frame.split==s,'landmark'].unique().tolist())} for s in new_dates},
 'pairwise_customer_overlap':0,'new_test_customers_not_in_round66_test':len(newtestkeys),'test_customer_overlap_with_round66':len(set(test.key)&oldtestkeys),
 'test_new_customer_rows':int(test.key.isin(newtestkeys).sum()),'feature_time':'InvoiceDate < t','label_time':'t <= InvoiceDate < t+28d','all_labels_mature':True,
 'train_label_end':'2011-08-22','validation_label_end':'2011-10-03','first_test':'2011-10-10','last_test_label_end':'2011-12-05','separate_time_not_separate_retailer':True}
save('SPLIT_AND_LEAKAGE_CHECKS.json',splitcheck)
save('FEATURE_SCHEMA.json',features)
params=dict(learning_rate=.05,max_iter=160,max_leaf_nodes=7,max_depth=3,min_samples_leaf=40,l2_regularization=10,max_bins=64,early_stopping=False,random_state=6601)
def reg():return HistGradientBoostingRegressor(loss='poisson',**params)
fitlogs={};preds={s:{} for s in ['validation','test']};probs={s:{} for s in preds}
ytrain=train.y28.to_numpy(float)
for s,d in [('validation',val),('test',test)]:
 preds[s]['B0_GLOBAL']=np.full(len(d),float(ytrain.mean()));probs[s]['B0_GLOBAL']=np.full(len(d),float(np.mean(ytrain>0)))
 preds[s]['B1_HISTORY_RATE']=(d.hist_ledger_amount/d.history_days*28).to_numpy(float)
 preds[s]['B2_ZERO']=np.zeros(len(d));probs[s]['B2_ZERO']=np.zeros(len(d))

with threadpool_limits(limits=2):
 t0=time.perf_counter();frozen=reg();oldtrain=frame66.loc[frame66.split=='train'];oldtest=frame66.loc[frame66.split=='test']
 frozen.fit(oldtrain[features['M2']].to_numpy(float),oldtrain.y28.to_numpy(float))
 oldprediction=frozen.predict(oldtest[features['M2']].to_numpy(float))
 reference=pd.read_csv(ROOT/'public-experiments/round66/MODEL_RESULTS.csv')
 reference=reference[(reference.arm=='dedup_positive_sales')&(reference.split=='test')&(reference.horizon_days==28)&(reference.model=='M2')].iloc[0]
 reconstructed=env['metrics'](oldtest.y28.to_numpy(float),oldprediction)
 for name in ['mae','rmse','median_ae','top10_recall','top10_value_capture','total_prediction_ratio']:
  assert np.isclose(reconstructed[name],reference[name],rtol=1e-10,atol=1e-9),(name,reconstructed[name],reference[name])
 save('FROZEN66_RECONSTRUCTION.json',dict(status='PASS',metrics_reconstructed=reconstructed,training_rows=len(oldtrain),old_test_rows=len(oldtest),same_features_and_hyperparameters=True,no_old_outputs_overwritten=True))
 fitlogs['FROZEN66_M2']={'seconds':time.perf_counter()-t0,'training_rows':len(oldtrain),'components':1}
 for s,d in [('validation',val),('test',test)]:preds[s]['FROZEN66_M2']=frozen.predict(d[features['M2']].to_numpy(float))
 for name in ['M0','M1','M2']:
  t0=time.perf_counter();model=reg();model.fit(train[features[name]].to_numpy(float),ytrain)
  for s,d in [('validation',val),('test',test)]:preds[s][name]=model.predict(d[features[name]].to_numpy(float))
  fitlogs[name]={'seconds':time.perf_counter()-t0,'training_rows':len(train),'components':1}
 t0=time.perf_counter();classifier=HistGradientBoostingClassifier(**params)
 classifier.fit(train[features['M2']].to_numpy(float),(ytrain>0).astype(int))
 conditional=reg();mask=ytrain>0;conditional.fit(train.loc[mask,features['M2']].to_numpy(float),ytrain[mask])
 conditional_predictions={}
 for s,d in [('validation',val),('test',test)]:
  probs[s]['M3']=classifier.predict_proba(d[features['M2']].to_numpy(float))[:,1]
  conditional_predictions[s]=conditional.predict(d[features['M2']].to_numpy(float))
  preds[s]['M3']=probs[s]['M3']*conditional_predictions[s]
 fitlogs['M3']={'seconds':time.perf_counter()-t0,'training_classifier_rows':len(train),'training_positive_amount_rows':int(mask.sum()),'components':2}
 t0=time.perf_counter();pval=np.clip(probs['validation']['M3'],1e-8,1-1e-8)
 logits=np.log(pval/(1-pval)).reshape(-1,1);vbinary=(val.y28.to_numpy()>0).astype(int)
 assert len(np.unique(vbinary))==2
 calibrator=LogisticRegression(C=1000,max_iter=1000,random_state=6701).fit(logits,vbinary)
 positive_val=vbinary==1;scale=float(val.y28.to_numpy()[positive_val].sum()/conditional_predictions['validation'][positive_val].sum())
 for s in preds:
  ps=np.clip(probs[s]['M3'],1e-8,1-1e-8)
  probs[s]['M4']=calibrator.predict_proba(np.log(ps/(1-ps)).reshape(-1,1))[:,1]
  preds[s]['M4']=probs[s]['M4']*scale*conditional_predictions[s]
 fitlogs['M4']={'seconds':time.perf_counter()-t0,'base':'M3 reused, not independently refit','calibration_rows':len(val),'positive_calibration_rows':int(positive_val.sum()),'components':'Platt and positive-amount scalar'}
 calibration_fit={'logistic_intercept':float(calibrator.intercept_[0]),'logistic_slope':float(calibrator.coef_[0,0]),'positive_amount_scale':scale,
  'fit_only_on_validation':True,'calibration_labels_end':'2011-10-03','first_test_prediction':'2011-10-10','test_aggregate_not_used':True}
save('CALIBRATION_FIT.json',calibration_fit)
print('All fixed models fit; frozen66 reconstruction PASS; no test tuning. Starting paired customer bootstrap.',flush=True)

def probmetrics(binary,p):
 p=np.asarray(p);clipped=np.clip(p,1e-8,1-1e-8);binid=np.minimum((p*10).astype(int),9)
 ece=0.
 for j in range(10):
  mask=binid==j
  if mask.any():ece+=float(mask.mean()*abs(binary[mask].mean()-p[mask].mean()))
 return dict(brier=float(np.mean((p-binary)**2)),logloss=float(-np.mean(binary*np.log(clipped)+(1-binary)*np.log(1-clipped))),ece10=float(ece),mean_probability=float(p.mean()))

def met(y,p,prob=None):
 m=env['metrics'](y,p);m['total_bias_gbp']=float(p.sum()-y.sum());m['total_bias_pct']=100*(m['total_prediction_ratio']-1)
 m['abs_ratio_bias']=abs(m['total_prediction_ratio']-1)
 if prob is not None:m.update(probmetrics((y>0).astype(int),prob))
 return m

comparisons=[('replicate_frozen66','FROZEN66_M2','B1_HISTORY_RATE',True),('replicate_refit67','M2','B1_HISTORY_RATE',True),
 ('two_stage_vs_direct','M3','M2',True),('calibrated_vs_direct','M4','M2',True),
 ('calibration_vs_twostage','M4','M3',False),('twostage_vs_zero','M3','B2_ZERO',False),('calibrated_vs_zero','M4','B2_ZERO',False),
 ('frozen66_vs_zero','FROZEN66_M2','B2_ZERO',False),('refit_vs_zero','M2','B2_ZERO',False)]
def compmetrics(values,a,b):
 ma,mb=values[a],values[b]
 d={k+'_gain_pct':100*(1-ma[k]/mb[k]) for k in ['mae','rmse']}
 d.update(recall_gain=ma['top10_recall']-mb['top10_recall'],capture_gain=ma['top10_value_capture']-mb['top10_value_capture'],abs_ratio_bias_reduction=mb['abs_ratio_bias']-ma['abs_ratio_bias'])
 for k in ['brier','logloss','ece10']:
  if k in ma and k in mb:d[k+'_reduction']=mb[k]-ma[k]
 return d

y=test.y28.to_numpy(float);keys=test.key.to_numpy();binary=(y>0).astype(int)
point={name:met(y,p,probs['test'].get(name)) for name,p in preds['test'].items()}
boot_values={name:{metric:[] for metric in m} for name,m in point.items()};boot_comps={label:{} for label,_,_,_ in comparisons}
unique=np.unique(keys);groups=[np.flatnonzero(keys==k) for k in unique];rng=np.random.default_rng(6701)
for rep in range(2000):
 ix=np.concatenate([groups[j] for j in rng.integers(0,len(groups),len(groups))])
 vals={name:met(y[ix],p[ix],probs['test'][name][ix] if name in probs['test'] else None) for name,p in preds['test'].items()}
 for name,m in vals.items():
  for metric,v in m.items():boot_values[name][metric].append(v)
 for label,a,b,_ in comparisons:
  for metric,v in compmetrics(vals,a,b).items():boot_comps[label].setdefault(metric,[]).append(v)

resultrows=[]
for split,d in [('validation',val),('test',test)]:
 ys=d.y28.to_numpy(float)
 for name,p in preds[split].items():
  m=met(ys,p,probs[split].get(name));row=dict(split=split,model=name,horizon_days=28,n=len(d),customers=int(d.key.nunique()),amount_unit='positive_recorded_invoice_GBP',features=len(features.get(name,features['M2'] if name in ['M3','M4','FROZEN66_M2'] else [])),**m)
  row['calibration_score_is_in_sample']=bool(split=='validation' and name=='M4')
  for metric in ['mae','rmse','median_ae','top10_recall','top10_value_capture','total_prediction_ratio','total_bias_gbp','total_bias_pct','abs_ratio_bias','brier','logloss','ece10','mean_probability']:
   if split=='test' and metric in boot_values[name]:lo,hi=np.quantile(boot_values[name][metric],[.025,.975])
   else:lo,hi=None,None
   row[metric+'_ci_low']=None if lo is None else float(lo);row[metric+'_ci_high']=None if hi is None else float(hi)
  row['probability_status']='explicit model or constant probability' if name in probs[split] else 'N/A direct amount prediction has no specified purchase probability'
  resultrows.append(row)
csvsave('MODEL_RESULTS.csv',resultrows)
comparisonrows=[]
for label,a,b,primary in comparisons:
 for metric,value in compmetrics(point,a,b).items():
  distribution=boot_comps[label][metric];lo,hi=np.quantile(distribution,[.025,.975]);simlo,simhi=(None,None)
  if primary and metric in ['mae_gain_pct','rmse_gain_pct']:simlo,simhi=np.quantile(distribution,[.05/(2*8),1-.05/(2*8)])
  comparisonrows.append(dict(comparison=label,model=a,reference=b,metric=metric,estimate=value,ci95_low=float(lo),ci95_high=float(hi),
   simultaneous_primary_8=bool(primary and metric in ['mae_gain_pct','rmse_gain_pct']),ci99_375_low=None if simlo is None else float(simlo),ci99_375_high=None if simhi is None else float(simhi),
   bootstrap='2000 paired customer clusters; fixed trained models, calibrator and calendar'))
csvsave('PAIRED_COMPARISONS.csv',comparisonrows)

calibrationrows=[];stratarows=[]
amountedges=np.array([0,25,50,100,250,500,1000,2500,5000,np.inf],float)
for name,p in preds['test'].items():
 for j,(lo,hi) in enumerate(zip(amountedges[:-1],amountedges[1:])):
  mask=(p>=lo)&(p<hi)
  calibrationrows.append(dict(model=name,dimension='predicted_amount_bin',group=f'[{lo:g},{hi:g})',n=int(mask.sum()),
   predicted_mean=float(p[mask].mean()) if mask.any() else None,observed_mean=float(y[mask].mean()) if mask.any() else None,
   predicted_total=float(p[mask].sum()),observed_total=float(y[mask].sum()),observed_purchase_rate=float(binary[mask].mean()) if mask.any() else None,
   predicted_probability=None,prediction_to_observed_ratio=float(p[mask].sum()/y[mask].sum()) if y[mask].sum()>0 else None))
 if name in probs['test']:
  prob=probs['test'][name];bi=np.minimum((prob*10).astype(int),9)
  for j in range(10):
   mask=bi==j
   calibrationrows.append(dict(model=name,dimension='predicted_purchase_probability_bin',group=f'[{j/10:.1f},{(j+1)/10:.1f}'+(']' if j==9 else ')'),n=int(mask.sum()),
    predicted_mean=None,observed_mean=None,predicted_total=None,observed_total=None,observed_purchase_rate=float(binary[mask].mean()) if mask.any() else None,
    predicted_probability=float(prob[mask].mean()) if mask.any() else None,prediction_to_observed_ratio=None))

positive=y[y>0];q50,q90,q99=np.quantile(positive,[.5,.9,.99]);tiers=np.full(len(y),'no_positive_record',dtype=object)
for lo,hi,lab in [(0,q50,'positive_0_50'),(q50,q90,'positive_50_90'),(q90,q99,'positive_90_99'),(q99,np.inf,'positive_top1')]:tiers[(y>lo)&(y<=hi)]=lab
groupdefs=[('observed_amount_tier',str(t),tiers==t) for t in np.unique(tiers)]
groupdefs += [('test_week',str(t),test.landmark.to_numpy()==t) for t in sorted(test.landmark.unique())]
groupdefs += [('country',str(t),test.country.to_numpy()==t) for t in test.country.unique() if int((test.country==t).sum())>=50]
groupdefs += [('round66_test_membership','not_in_round66_test',test.key.isin(newtestkeys).to_numpy()),('round66_test_membership','also_in_round66_test',~test.key.isin(newtestkeys).to_numpy())]
for dim,group,mask in groupdefs:
 if not mask.any():continue
 for name,p in preds['test'].items():
  m=met(y[mask],p[mask],probs['test'][name][mask] if name in probs['test'] else None)
  stratarows.append(dict(model=name,dimension=dim,group=group,n=int(mask.sum()),customers=int(test.loc[mask,'key'].nunique()),
   observed_mean=float(y[mask].mean()),predicted_mean=float(p[mask].mean()),observed_purchase_rate=float(binary[mask].mean()),**m))
csvsave('CALIBRATION_ANALYSIS.csv',calibrationrows);csvsave('STRATIFIED_ERRORS.csv',stratarows)
summary={}
for split,d in [('train',train),('validation',val),('test',test)]:
 ys=d.y28.to_numpy(float);yp=ys[ys>0];n1=math.ceil(.01*len(ys))
 summary[split]=dict(n=len(d),customers=int(d.key.nunique()),no_positive_record_fraction=float(np.mean(ys==0)),
  observed_mean=float(ys.mean()),observed_median=float(np.median(ys)),positive_quantiles={str(q):float(np.quantile(yp,q)) for q in [.5,.9,.99,.999]},
  max_observed_amount=float(ys.max()),top1_row_positive_amount_share=float(np.sort(ys)[-n1:].sum()/ys.sum()))
save('LABEL_DISTRIBUTIONS.json',summary)
for rel,expected in history.items():assert sha(ROOT/rel)==expected,rel
assert sha(protocol)==run['protocol_sha256']
assert sha(raw)==run['raw_sha256']
run.update(finished_utc=datetime.now(timezone.utc).isoformat(),models=dict(fitlogs),calibration=calibration_fit,
  primary_comparison_count=8,bootstrap_replicates=2000,source66_function_reuse='AST-selected functions only; historical module never executed',
  old_m2_reconstruction_verified=True,customer_overlap=0,all_label_windows_mature=True,old_files_unchanged=True,
  per_customer_output_saved=False,probability_not_invented_for_direct_models=True,
  caveats=['same retailer and potentially same past test customers; only future period independent','missing available_at and true data completeness/zero-consumption state','fixed-calendar conditional bootstrap, no refitting uncertainty','no game value/ROAS/platform inference'])
save('RUN_MANIFEST.json',run)
print(json.dumps({'status':'COMPLETE','test_rows':len(test),'test_customers':int(test.key.nunique()),'frozen66_reconstruction':'PASS','calibration':calibration_fit,'test_results':point},ensure_ascii=True,indent=2),flush=True)
