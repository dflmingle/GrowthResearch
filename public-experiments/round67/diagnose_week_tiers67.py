"""Rebuild identical fixed predictors only to produce missing week x tier summaries.
No hyperparameter changes, model selection or expanded hypotheses; preserve first run.
"""
from pathlib import Path
import ast,json,hashlib
import pandas as pd
import numpy as np
ROOT=Path(r'D:\GrowthResearch');OUT=ROOT/'public-experiments/round67'
source=OUT/'run67.py';tree=ast.parse(source.read_text(encoding='utf-8'))
prefix=[]
for stmt in tree.body:
 if isinstance(stmt,ast.Expr) and isinstance(stmt.value,ast.Call) and isinstance(stmt.value.func,ast.Name) and stmt.value.func.id=='print':break
 # Only redirect the audit outputs of this exact fixed training reconstruction.
 if isinstance(stmt,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='OUT' for t in stmt.targets):
  stmt.value=ast.Call(func=ast.Name(id='Path',ctx=ast.Load()),args=[ast.Constant(str(OUT/'diagnostic-reconstruction'))],keywords=[])
 prefix.append(stmt)
ns={'__file__':str(source),'__name__':'round67_fixed_diagnostic'}
exec(compile(ast.fix_missing_locations(ast.Module(body=prefix,type_ignores=[])),str(source),'exec'),ns)
test=ns['test'];y=test.y28.to_numpy(float);pred=ns['preds']['test'];metrics=ns['env']['metrics'];old=pd.read_csv(OUT/'MODEL_RESULTS.csv');old=old.loc[old.split=='test'].set_index('model')
for name,p in pred.items():
 m=metrics(y,p)
 for metric,value in m.items():assert np.isclose(value,old.loc[name,metric],rtol=1e-10,atol=1e-9),(name,metric)
positive=y[y>0];q50,q90,q99=np.quantile(positive,[.5,.9,.99]);tiers=np.full(len(y),'no_positive_record',dtype=object)
for lo,hi,label in [(0,q50,'positive_0_50'),(q50,q90,'positive_50_90'),(q90,q99,'positive_90_99'),(q99,np.inf,'positive_top1')]:tiers[(y>lo)&(y<=hi)]=label
rows=[]
for week in sorted(test.landmark.unique()):
 for tier in np.unique(tiers):
  mask=(test.landmark.to_numpy()==week)&(tiers==tier)
  if not mask.any():continue
  for name,p in pred.items():
   err=np.abs(y[mask]-p[mask]);denom=y[mask].sum()
   rows.append(dict(week=week,observed_tier=tier,model=name,n=int(mask.sum()),customers=int(test.loc[mask,'key'].nunique()),observed_mean=float(y[mask].mean()),predicted_mean=float(p[mask].mean()),mae=float(err.mean()),rmse=float(np.sqrt(np.mean((y[mask]-p[mask])**2))),total_prediction_ratio=float(p[mask].sum()/denom) if denom>0 else None,scope='descriptive; test-global tier boundaries, no week-specific tuning or gain significance'))
pd.DataFrame(rows).to_csv(OUT/'WEEK_BY_TIER_DIAGNOSTIC.csv',index=False,encoding='utf-8',lineterminator='\n')
log={'purpose':'Required week x consumption tier descriptive check; original run lacks saved individual forecasts','identical_fixed_refit':True,'all_9_predictors_match_original_67_test_metrics':True,'original_run_not_overwritten':True,'test_tuning_or_selection':False,'new_confirmatory_tests':0,'new_synthetic_value_labels':False,'no_individual_keys_or_predictions_saved':True,'rows':len(rows)}
(OUT/'WEEK_TIER_DIAGNOSTIC_MANIFEST.json').write_text(json.dumps(log,indent=2)+'\n',encoding='utf-8')
print(json.dumps(log,indent=2),flush=True)
