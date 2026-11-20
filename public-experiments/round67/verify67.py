"""Boundary fixtures, historical hashes and actual run provenance. No training."""
from pathlib import Path
import ast,json,hashlib,math
import numpy as np
import pandas as pd
ROOT=Path(r'D:\GrowthResearch');OUT=ROOT/'public-experiments/round67'
source=ROOT/'public-experiments/round66/run_experiment66.py'
tree=ast.parse(source.read_text(encoding='utf-8'));names=['bucket','snapshots','topweights','metrics']
functions=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names]
env=dict(np=np,pd=pd,math=math,hashlib=hashlib,dates={'train':[pd.Timestamp('2011-07-25')],'validation':[pd.Timestamp('2011-09-05')],'test':[pd.Timestamp('2011-10-10')]})
exec(compile(ast.Module(body=functions,type_ignores=[]),'reused_boundaries67','exec'),env)
keys={s:next(str(i) for i in range(1,1000) if env['bucket'](i)==s) for s in env['dates']}
rows=[]
for split,ts in env['dates'].items():
 t=ts[0]
 for day,amount,inv in [(-30,10,'a'),(-1,20,'b'),(0,7,'c'),(7,28,'d'),(28,1000,'e')]:
  rows.append(dict(key=keys[split],InvoiceDate=t+pd.Timedelta(days=day),amount=amount,InvoiceNo=inv,Quantity=1,Country='fixture'))
f=pd.DataFrame(rows);before=env['snapshots'](f,f)
assert np.allclose(before.hist_amount,30) and np.allclose(before.y28,35) and np.allclose(before.y7,7)
poison=f.copy()
for split,ts in env['dates'].items():poison.loc[(poison.key==keys[split])&(poison.InvoiceDate>=ts[0]),'amount']=1000000
after=env['snapshots'](poison,poison)
cols=[c for c in before if c not in ['y7','y28']];pd.testing.assert_frame_equal(before[cols],after[cols])
assert np.allclose(after.y28,2000000)
y=np.zeros(100);y[0]=10;y[1]=100;m=env['metrics'](y,np.zeros(100))
assert np.isclose(m['top10_recall'],.1) and np.isclose(m['top10_value_capture'],.1)
newtree=ast.parse((OUT/'run67.py').read_text(encoding='utf-8'))
newfn=[n for n in newtree.body if isinstance(n,ast.FunctionDef) and n.name=='probmetrics'];penv=dict(np=np)
exec(compile(ast.Module(body=newfn,type_ignores=[]),'probability_metrics67','exec'),penv)
p=penv['probmetrics'](np.array([0,1]),np.array([0.,0.]));assert p['brier']==.5 and p['ece10']==.5 and np.isfinite(p['logloss'])
history=json.loads((OUT/'HISTORY_BEFORE67.json').read_text(encoding='utf-8'))
assert all(hashlib.sha256((ROOT/k).read_bytes()).hexdigest()==v for k,v in history.items())
run=json.loads((OUT/'RUN_MANIFEST.json').read_text(encoding='utf-8'))
assert hashlib.sha256((ROOT/run['protocol_path']).read_bytes()).hexdigest()==run['protocol_sha256']
assert hashlib.sha256((OUT/'run67.py').read_bytes()).hexdigest()==run['script_sha256']
assert json.loads((OUT/'FROZEN66_RECONSTRUCTION.json').read_text(encoding='utf-8'))['status']=='PASS'
assert run['customer_overlap']==0 and run['all_label_windows_mature']
result=dict(status='PASS',checked_utc=__import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat(),
 checks=['future amount poisoning leaves all features unchanged','t excluded from past','t+28 excluded from label','fixed customer buckets disjoint','constant ties expectation correct','zero probability Brier/ECE and finite diagnostic logloss','all historical files byte hashes preserved','protocol/script match pre-fit run hashes','frozen66 old metrics reconstructed','actual run maturity/customer checks passed'],
 synthetic_fixtures_validate_code_only=True,actual_model_gain_comes_only_from_public_retail_results=True,game_or_platform_effect_proven=False)
(OUT/'BOUNDARY_AND_PROVENANCE_TESTS.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps(result,indent=2))
