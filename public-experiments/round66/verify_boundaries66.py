"""Independent boundary fixtures only; synthetic fixtures never count as model evidence."""
from pathlib import Path
import ast,json,math,hashlib
import numpy as np
import pandas as pd
ROOT=Path(r'D:\GrowthResearch');OUT=ROOT/'public-experiments/round66'
tree=ast.parse((OUT/'run_experiment66.py').read_text(encoding='utf-8'))
functions=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ['bucket','snapshots','topweights','metrics']]
env=dict(np=np,pd=pd,math=math,hashlib=hashlib,dates={'train':[pd.Timestamp('2011-04-01')],'validation':[pd.Timestamp('2011-06-01')],'test':[pd.Timestamp('2011-08-01')]})
exec(compile(ast.Module(body=functions,type_ignores=[]),'isolated_visible_functions','exec'),env)
keys={s:next(str(i) for i in range(1,100) if env['bucket'](i)==s) for s in env['dates']}
events=[]
for split,ds in env['dates'].items():
 t=ds[0];k=keys[split]
 for days,amount,invoice in [(-30,10,'history_a'),(-2,20,'history_b'),(0,7,'at_boundary'),(7,28,'day7'),(28,300,'day28_excluded')]:
  events.append(dict(key=k,InvoiceDate=t+pd.Timedelta(days=days),amount=amount,InvoiceNo=invoice,Quantity=1,Country='fixture'))
f=pd.DataFrame(events);a=env['snapshots'](f,f)
assert np.allclose(a.hist_amount,30)
assert np.allclose(a.y7,7)
assert np.allclose(a.y28,35)
# Poison only future event values; feature construction must be invariant.
poison=f.copy()
for split,ts in env['dates'].items():
 mask=(poison.key==keys[split])&(poison.InvoiceDate>=ts[0])
 poison.loc[mask,'amount']=999999
b=env['snapshots'](poison,poison)
cols=[c for c in a if c not in ['y7','y28']]
pd.testing.assert_frame_equal(a[cols],b[cols])
assert np.allclose(b.y7,999999) and np.allclose(b.y28,1999998)
# Constant predictors must not gain from row ordering, and zeros cannot become high spend targets.
y=np.zeros(100);y[0]=10;y[1]=100
m=env['metrics'](y,np.zeros(100))
assert abs(m['top10_recall']-.1)<1e-12
assert abs(m['top10_value_capture']-.1)<1e-12
perm=np.random.default_rng(66).permutation(100)
m2=env['metrics'](y[perm],np.zeros(100))
assert m==m2
summary=dict(status='PASS',synthetic_fixtures_only=True,does_not_validate_model_gain=True,
 checks=['history excludes events at landmark','7-day label excludes t+7','28-day label excludes t+28','future-amount poisoning leaves every feature invariant','customer partition keys separate','constant-score ties do not yield fake ranking','zero amount excluded from high-spend target'],
 real_customer_identifiers_exported=False)
(OUT/'BOUNDARY_TESTS.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8');print(json.dumps(summary,indent=2))
