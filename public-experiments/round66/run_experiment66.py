"""Real UCI retail invoice forecasting; fixed temporal/customer splits, no network."""
import os
os.environ['OMP_NUM_THREADS']='2'
os.environ['OPENBLAS_NUM_THREADS']='2'
from pathlib import Path
from datetime import datetime,timezone
import json,csv,hashlib,zipfile,time,math,sys
import numpy as np
import pandas as pd
import sklearn
from sklearn.ensemble import HistGradientBoostingRegressor
from threadpoolctl import threadpool_limits

ROOT=Path(r'D:\GrowthResearch');OUT=ROOT/'public-experiments/round66';OUT.mkdir(parents=True,exist_ok=True)
def save(name,obj):
 (OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
def hashfile(p):return hashlib.sha256(p.read_bytes()).hexdigest()
PROTOCOL=OUT/'PREREGISTERED_PROTOCOL.md'
SAVE=dict(started_utc=datetime.now(timezone.utc).isoformat(),protocol_sha256=hashfile(PROTOCOL),script_sha256=hashfile(Path(__file__)),
          numpy=np.__version__,pandas=pd.__version__,sklearn=sklearn.__version__,models={},no_network=True,customer_ids_not_model_features=True)
save('RUN_START.json',SAVE)
raw=ROOT/'public-experiments/audit/retail352.download'
assets=json.loads((ROOT/'public-experiments/audit/ASSET_VERIFICATION.json').read_text(encoding='utf-8'))
expected=next(x['sha256'] for x in assets if x['id']=='retail352')
assert hashfile(raw)==expected
with zipfile.ZipFile(raw) as z: df=pd.read_excel(z.open('Online Retail.xlsx'),engine='openpyxl')
df['InvoiceDate']=pd.to_datetime(df.InvoiceDate)
duplicate=df.duplicated(keep='first')
dedup=df.loc[~duplicate].copy()

def bucket(customer):
 key=format(float(customer),'.0f')
 b=int.from_bytes(hashlib.sha256(('round66-customer-split:'+key).encode()).digest()[:8],'big')%10
 return 'train' if b<=5 else ('validation' if b<=7 else 'test')

quality={'original_sha256':expected,'original_rows':len(df),'exact_duplicate_rows_removed':int(duplicate.sum()),'deduplicated_rows':len(dedup),
 'original_missing_customer_rows':int(df.CustomerID.isna().sum()),'dedup_missing_customer_rows':int(dedup.CustomerID.isna().sum()),
 'event_time_min':str(df.InvoiceDate.min()),'event_time_max':str(df.InvoiceDate.max()),'original_unchanged':True,
 'available_at':'ABSENT; event-time offline assumption, no production real-time availability claim',
 'missing_customer_country_audit':dedup.assign(missing_customer=dedup.CustomerID.isna()).groupby('Country').agg(rows=('InvoiceNo','size'),missing=('missing_customer','sum')).reset_index().to_dict('records')}

def rowaudit(d):
 cancel=d.InvoiceNo.astype(str).str.upper().str.startswith('C');amount=d.Quantity*d.UnitPrice
 return {'rows':len(d),'missing_customer_rows':int(d.CustomerID.isna().sum()),'cancel_prefix_rows':int(cancel.sum()),
  'negative_quantity_rows':int((d.Quantity<0).sum()),'negative_unit_price_rows':int((d.UnitPrice<0).sum()),
  'nonpositive_unit_price_rows':int((d.UnitPrice<=0).sum()),'negative_amount_rows':int((amount<0).sum()),
  'cancel_and_nonnegative_amount_rows':int((cancel & (amount>=0)).sum()),'negative_amount_without_cancel_prefix_rows':int(((amount<0)&~cancel).sum()),
  'cancel_signed_amount_gbp':float(amount[cancel].sum()),'negative_amount_sum_gbp':float(amount[amount<0].sum()),
  'nonpositive_unit_price_signed_amount_gbp':float(amount[d.UnitPrice<=0].sum())}
quality['original_row_audit']=rowaudit(df);quality['dedup_row_audit']=rowaudit(dedup)
save('DATA_QUALITY.json',quality)

dates={'train':list(pd.date_range('2011-01-03','2011-04-25',freq='W-MON')),
       'validation':list(pd.date_range('2011-06-06','2011-06-27',freq='W-MON')),
       'test':list(pd.date_range('2011-08-01','2011-08-29',freq='W-MON'))}
assert max(dates['train'])+pd.Timedelta(days=28)<min(dates['validation'])
assert max(dates['validation'])+pd.Timedelta(days=28)<min(dates['test'])
assert max(dates['test'])+pd.Timedelta(days=28)<df.InvoiceDate.max()

def dataframes(keep_duplicates=False,signed=False):
 d=(df if keep_duplicates else dedup).copy()
 d=d.loc[d.CustomerID.notna() & d.InvoiceDate.notna() & (d.UnitPrice>0)].copy()
 d['key']=d.CustomerID.map(lambda x:format(float(x),'.0f'))
 d['amount']=d.Quantity.astype(float)*d.UnitPrice.astype(float)
 cancel=d.InvoiceNo.astype(str).str.upper().str.startswith('C')
 positive=d.loc[(d.Quantity>0)&~cancel].copy()
 ledger=d if signed else positive
 return positive,ledger

def snapshots(positive,ledger):
 result=[]
 for split,landmarks in dates.items():
  for t in landmarks:
   h=positive.loc[positive.InvoiceDate<t]
   cust=h.groupby('key').agg(hist_amount=('amount','sum'),hist_orders=('InvoiceNo','nunique'),
       hist_units=('Quantity','sum'),first_purchase=('InvoiceDate','min'),last_purchase=('InvoiceDate','max'),country=('Country','last'))
   cust['split']=cust.index.map(lambda x:bucket(float(x)))
   cust=cust.loc[cust.split==split].copy()
   orders=h.groupby(['key','InvoiceNo']).InvoiceDate.min().reset_index().sort_values(['key','InvoiceDate'])
   orders['gap_days']=orders.groupby('key').InvoiceDate.diff().dt.total_seconds()/86400
   gaps=orders.groupby('key').gap_days.agg(['mean','std']).fillna(0)
   cust['gap_mean']=gaps['mean'].reindex(cust.index).fillna(0)
   cust['gap_std']=gaps['std'].reindex(cust.index).fillna(0)
   cust['recency_days']=(t-cust.last_purchase).dt.total_seconds()/86400
   cust['history_days']=np.maximum((t-cust.first_purchase).dt.total_seconds()/86400,1)
   for days in [7,28,90]:
    w=h.loc[h.InvoiceDate>=t-pd.Timedelta(days=days)].groupby('key').agg(amount=('amount','sum'),orders=('InvoiceNo','nunique'),units=('Quantity','sum'))
    for source in ['amount','orders','units']:cust[f'{source}_{days}']=w[source].reindex(cust.index).fillna(0)
   cust['amount_trend_7_vs_previous21']=cust.amount_7/7-(cust.amount_28-cust.amount_7)/21
   cust['amount_trend_28_vs_previous62']=cust.amount_28/28-(cust.amount_90-cust.amount_28)/62
   cust['orders_trend_7_vs_previous21']=cust.orders_7/7-(cust.orders_28-cust.orders_7)/21
   hist_ledger=ledger.loc[ledger.InvoiceDate<t].groupby('key').amount.sum()
   cust['hist_ledger_amount']=hist_ledger.reindex(cust.index).fillna(0)
   for days in [7,28]:
    future=ledger.loc[(ledger.InvoiceDate>=t)&(ledger.InvoiceDate<t+pd.Timedelta(days=days))].groupby('key').amount.sum()
    cust[f'y{days}']=future.reindex(cust.index).fillna(0)
   cust['landmark']=str(t.date());cust['key']=cust.index
   result.append(cust.reset_index(drop=True).drop(columns=['first_purchase','last_purchase']))
 frame=pd.concat(result,ignore_index=True)
 for a,b in [('train','validation'),('train','test'),('validation','test')]:assert set(frame.loc[frame.split==a,'key']).isdisjoint(frame.loc[frame.split==b,'key'])
 return frame

features={'M0':['hist_amount','hist_orders']}
features['M1']=features['M0']+[f'{k}_{d}' for d in [7,28,90] for k in ['amount','orders']]
features['M2']=features['M1']+['gap_mean','gap_std','recency_days','hist_units','units_7','units_28','units_90','amount_trend_7_vs_previous21','amount_trend_28_vs_previous62','orders_trend_7_vs_previous21']
assert all(not any(s in n.lower() for s in ['customer','key','y7','y28','split','landmark']) for names in features.values() for n in names)
save('FEATURE_SCHEMA.json',features)

def topweights(values,k,positive_only=False):
 eligible=values>0 if positive_only else np.ones(len(values),dtype=bool)
 k=min(k,int(eligible.sum()));weights=np.zeros(len(values),dtype=float)
 if not k:return weights
 cutoff=np.sort(values[eligible])[-k]
 above=eligible & (values>cutoff);ties=eligible & (values==cutoff)
 weights[above]=1.;weights[ties]=(k-int(above.sum()))/int(ties.sum())
 return weights

def metrics(y,p):
 err=np.abs(y-p);k=max(1,int(math.ceil(len(y)*.1)))
 actual=topweights(y,k,positive_only=True);pred=topweights(p,k)
 denom=float(np.maximum(y,0).sum())
 return dict(mae=float(err.mean()),rmse=float(np.sqrt(np.mean((y-p)**2))),median_ae=float(np.median(err)),
  top10_recall=float(np.sum(actual*pred)/actual.sum()) if actual.sum() else 0,top10_value_capture=float(np.sum(np.maximum(y,0)*pred)/denom) if denom else 0,
  total_prediction_ratio=float(p.sum()/y.sum()) if y.sum()!=0 else 0)

def boot(y,pred,keys,horizon,arm,split):
 # Paired customer cluster bootstrap; all repeated landmarks follow customer.
 unique=np.unique(keys);indices=[np.flatnonzero(keys==c) for c in unique]
 rng=np.random.default_rng(660100+horizon)
 records={name:[] for name in pred}
 for rep in range(500):
  ix=np.concatenate([indices[j] for j in rng.integers(0,len(indices),len(indices))])
  vals={name:metrics(y[ix],p[ix]) for name,p in pred.items()}
  for name,m in vals.items():
   m['mae_gain_vs_history_pct']=100*(1-m['mae']/vals['B1_HISTORY_RATE']['mae'])
   m['rmse_gain_vs_history_pct']=100*(1-m['rmse']/vals['B1_HISTORY_RATE']['rmse'])
   m['mae_gain_vs_global_pct']=100*(1-m['mae']/vals['B0_GLOBAL']['mae'])
   m['recall_gain_vs_history']=m['top10_recall']-vals['B1_HISTORY_RATE']['top10_recall']
   records[name].append(m)
 out={}
 for name,items in records.items():
  out[name]={}
  for met in items[0]:
   values=[item[met] for item in items]
   lo,hi=np.quantile(values,[.025,.975]);out[name][met]=[float(lo),float(hi)]
   if met=='mae_gain_vs_history_pct':
    lo,hi=np.quantile(values,[.05/(2*6),1-.05/(2*6)])
    out[name]['mae_gain_vs_history_familywise99_1667']=[float(lo),float(hi)]
 return out

allrows=[];strata=[];summaries=[];integrity=[]
arms=[('dedup_positive_sales',False,False),('dedup_signed_invoice_net',False,True),('duplicates_retained_positive_sensitivity',True,False)]
for arm,keepdup,signed in arms:
 pos,ledger=dataframes(keepdup,signed);frame=snapshots(pos,ledger)
 integrity.append(dict(arm=arm,splits={s:{'rows':int((frame.split==s).sum()),'unique_customers':int(frame.loc[frame.split==s,'key'].nunique()),'landmarks':sorted(frame.loc[frame.split==s,'landmark'].unique().tolist())} for s in dates},
   all_pairwise_customer_overlap=0,last_feature_time_condition='InvoiceDate < landmark',label_time_condition='landmark <= InvoiceDate < landmark + H',no_future_customer_selection=True))
 train=frame.loc[frame.split=='train'];val=frame.loc[frame.split=='validation'];test=frame.loc[frame.split=='test']
 for H in [7,28]:
  start=time.perf_counter();ytrain=train[f'y{H}'].to_numpy(float)
  predictions={};fit_times={}
  for split,d in [('validation',val),('test',test)]:
   predictions[split]={'B0_GLOBAL':np.full(len(d),ytrain.mean()),'B1_HISTORY_RATE':(d.hist_ledger_amount/d.history_days*H).to_numpy(float),'B2_ZERO_EXPLORATORY':np.zeros(len(d))}
  for name,cols in features.items():
   t0=time.perf_counter()
   model=HistGradientBoostingRegressor(loss='squared_error' if signed else 'poisson',learning_rate=.05,max_iter=160,max_leaf_nodes=7,max_depth=3,min_samples_leaf=40,l2_regularization=10,max_bins=64,early_stopping=False,random_state=6601)
   with threadpool_limits(limits=2):
    model.fit(train[cols].to_numpy(float),ytrain)
    for split,d in [('validation',val),('test',test)]:predictions[split][name]=model.predict(d[cols].to_numpy(float))
   fit_times[name]=time.perf_counter()-t0
  for split,d in [('validation',val),('test',test)]:
   y=d[f'y{H}'].to_numpy(float);keys=d.key.to_numpy();pred=predictions[split]
   point={name:metrics(y,p) for name,p in pred.items()}
   intervals=boot(y,pred,keys,H,arm,split) if split=='test' else {}
   positive=y[y>0];sortedpos=np.sort(np.maximum(y,0))[::-1];n1=max(1,math.ceil(len(y)*.01))
   summaries.append(dict(arm=arm,horizon_days=H,split=split,n=len(d),customers=int(d.key.nunique()),zero_recorded_amount_fraction=float(np.mean(y==0)),negative_recorded_amount_fraction=float(np.mean(y<0)),
    observed_amount_mean_gbp=float(y.mean()),observed_amount_median_gbp=float(np.median(y)),positive_amount_p50_p90_p99_gbp=[float(x) for x in np.quantile(positive,[.5,.9,.99])] if len(positive) else [],
    positive_amount_top1_share=float(sortedpos[:n1].sum()/sortedpos.sum()) if sortedpos.sum() else 0))
   for name,m in point.items():
    row=dict(arm=arm,target='signed_recorded_invoice_net_GBP' if signed else 'positive_recorded_sales_GBP',horizon_days=H,split=split,model=name,n=len(d),unique_customers=int(d.key.nunique()),features=len(features.get(name,[])),fit_seconds=fit_times.get(name,0),**m)
    row['mae_gain_vs_history_pct']=100*(1-m['mae']/point['B1_HISTORY_RATE']['mae'])
    row['rmse_gain_vs_history_pct']=100*(1-m['rmse']/point['B1_HISTORY_RATE']['rmse'])
    row['mae_gain_vs_global_pct']=100*(1-m['mae']/point['B0_GLOBAL']['mae'])
    row['recall_gain_vs_history']=m['top10_recall']-point['B1_HISTORY_RATE']['top10_recall']
    for met in ['mae','rmse','median_ae','top10_recall','top10_value_capture','total_prediction_ratio','mae_gain_vs_history_pct','rmse_gain_vs_history_pct','mae_gain_vs_global_pct','recall_gain_vs_history','mae_gain_vs_history_familywise99_1667']:
     ci=intervals.get(name,{}).get(met,[None,None]);row[met+'_ci_low']=ci[0];row[met+'_ci_high']=ci[1]
    row['bootstrap']='500 paired customer clusters; fixed fitted model/date; exploratory except prespecified MAE vs B1 family' if split=='test' else 'none; validation not used for tuning'
    allrows.append(row)
   if split=='test':
    bins=np.full(len(y),'zero_recorded',dtype=object);bins[y<0]='negative_net'
    if len(positive):
     q50,q90,q99=np.quantile(positive,[.5,.9,.99])
     for lo,hi,label in [(0,q50,'positive_0_50'),(q50,q90,'positive_50_90'),(q90,q99,'positive_90_99'),(q99,np.inf,'positive_top1')]:bins[(y>lo)&(y<=hi)]=label
    groups=[('value_tier',str(k),bins==k) for k in np.unique(bins)]
    groups += [('landmark',str(k),d.landmark.to_numpy()==k) for k in sorted(d.landmark.unique())]
    groups += [('country',str(k),d.country.to_numpy()==k) for k in d.country.unique() if int((d.country==k).sum())>=50]
    for dimension,group,mask in groups:
     for name,p in pred.items():
      a=np.abs(y[mask]-p[mask]);strata.append(dict(arm=arm,horizon_days=H,dimension=dimension,group=group,model=name,n=int(mask.sum()),mae=float(a.mean()),rmse=float(np.sqrt(np.mean((y[mask]-p[mask])**2))),median_ae=float(np.median(a)),observed_mean=float(y[mask].mean()),predicted_mean=float(p[mask].mean())))
  print(json.dumps({'arm':arm,'H':H,'seconds':round(time.perf_counter()-start,2),'test_n':len(test),'M2_test':point.get('M2')},ensure_ascii=True),flush=True)

def csvout(path,rows):
 with path.open('w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
csvout(OUT/'MODEL_RESULTS.csv',allrows);csvout(OUT/'STRATIFIED_ERRORS.csv',strata)
prior=pd.read_csv(OUT/'initial-run/MODEL_RESULTS.csv')
current=pd.DataFrame(allrows)
joined=prior.merge(current,on=['arm','horizon_days','split','model'],suffixes=('_before','_after'))
for metric in ['mae','rmse','median_ae']:
 assert np.allclose(joined[metric+'_before'],joined[metric+'_after'],rtol=1e-12,atol=1e-10)
save('EVALUATION_FIX_CHECK.json',{'initial_core_metric_rows_checked':len(joined),'mae_rmse_median_unchanged':True,'split_features_hyperparameters_unchanged':True,'top10_ties_expected_weights':True,'added_zero_baseline_exploratory_only':True})
save('LABEL_DISTRIBUTIONS.json',summaries);save('SPLIT_AND_LEAKAGE_CHECKS.json',integrity)
SAVE.update(finished_utc=datetime.now(timezone.utc).isoformat(),raw_unchanged=(hashfile(raw)==expected),arms=[x[0] for x in arms],horizons=[7,28],trained_models=18,hyperparameter_searches=0,
 result_rows=len(allrows),no_customer_keys_or_individual_predictions_saved=True,feature_names=features,
 checks={'customer_overlap':0,'label_maturity':True,'temporal_embargo':True,'feature_and_target_times_separated':True,'source_hash_matches':True},
 limitations=['event_time only, no available_at','conditional on observed retailer buyers, future non-observation is not true zero global consumption','customer cluster CI fixed-date/fixed-model only','no gaming or bidding inference'])
save('RUN_MANIFEST.json',SAVE)
assert SAVE['raw_unchanged']
print('COMPLETE: no model selection or retuning; all prespecified arms/results retained',flush=True)
