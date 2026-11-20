"""Run meaningful checks and freeze this phase's evidence inventory."""
from pathlib import Path
import json, hashlib, subprocess, sys, datetime, re, importlib.metadata, unittest, io
from jsonschema import Draft202012Validator
from .validation import SCHEMA

R=Path(__file__).resolve().parents[2];W=R/'prediction-validation';OUT=W/'results'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n','utf-8')
checks=[]
def check(name,ok,detail=None):checks.append(dict(name=name,passed=bool(ok),detail=detail))
baseline=json.loads((OUT/'prior_artifacts.before56.json').read_text('utf-8'))
check('All previous protected report/graph/experiment hashes unchanged',all((R/x['path']).exists() and sha(R/x['path'])==x['sha256'] for x in baseline),len(baseline))
Draft202012Validator.check_schema(SCHEMA)
check('Draft2020-12 contract schema validates',True)
suite=unittest.defaultTestLoader.discover(str(W/'tests'))
buffer=io.StringIO();result=unittest.TextTestRunner(stream=buffer,verbosity=2).run(suite)
(OUT/'TEST_RESULTS.txt').write_text(buffer.getvalue(),'utf-8')
save(OUT/'TEST_RESULTS.json',dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    tests=result.testsRun,failures=len(result.failures),errors=len(result.errors),passed=result.wasSuccessful(),
    scope='Only synthetic contract/accounting/time/privacy tests; no fitted model',
    python=sys.version,jsonschema_version=importlib.metadata.version('jsonschema')))
check('Synthetic contract and accounting tests',result.wasSuccessful(),result.testsRun)
smoke=OUT/'round56_smoke_v2'
if not smoke.exists():
    p=subprocess.run([sys.executable,'-X','utf8','-m','src.run','--synthetic-smoke','--run-id','round56_smoke_v2'],cwd=W,capture_output=True,text=True,encoding='utf-8')
    check('Fresh immutable smoke run',p.returncode==0,p.stdout.strip() if p.returncode==0 else p.stderr[-1500:])
else:check('Existing immutable v2 result retained',True)
data=json.loads((smoke/'smoke_result.json').read_text('utf-8'))
check('Synthetic only and model metrics absent',data['provenance']=='synthetic' and data['prediction_metrics'] is None and data['auction_roas'] is None and not data['model_training_performed'])
check('Smoke data quality passed',data['quality']['passed'])
check('Real training stays closed',not data['quality']['real_training_allowed'])
check('No 57-60 real reports created',not any(list(R.glob(f'{n}_*.md')) for n in range(57,61)))

docs=[next(R.glob('56_*.md'))]+list(W.rglob('*.md'))
for p in docs:
    t=p.read_text('utf-8')
    check(p.name+' encoding', '\ufffd' not in t)
    for m in re.finditer(r'\]\(([^)#]+)(?:#[^)]*)?\)',t):
        link=m.group(1)
        if link.startswith(('http:','https:')):continue
        target=(p.parent/link).resolve()
        check(p.name+' link '+link,target.exists() or target==OUT/'DELIVERABLE_VALIDATION.json')
# This code is intentionally local. Imports of network clients or production SDKs are forbidden.
import ast
for p in (W/'src').glob('*.py'):
    tree=ast.parse(p.read_text('utf-8'))
    imports=[n.module for n in ast.walk(tree) if isinstance(n,ast.ImportFrom)]+[a.name for n in ast.walk(tree) if isinstance(n,ast.Import) for a in n.names]
    check(p.name+' no network or production SDK imports',not any((x or '').split('.')[0] in {'requests','urllib','httpx','socket','firebase_admin','adjust','applovin'} for x in imports))
all_files=[p for p in W.rglob('*') if p.is_file() and '__pycache__' not in str(p) and p.name not in {'DELIVERABLE_VALIDATION.json','ARTIFACT_MANIFEST.json'}]
evidence=[dict(path=p.relative_to(R).as_posix(),sha256=sha(p),bytes=p.stat().st_size) for p in all_files]
save(OUT/'ARTIFACT_MANIFEST.json',dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    provenance='Code/contracts/research metadata and explicitly synthetic fixture only',files=evidence))
check('Previous artifacts remain unchanged at finish',all(sha(R/x['path'])==x['sha256'] for x in baseline))
validation=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),passed=all(c['passed'] for c in checks),
    scope='First-round audit, contract and synthetic smoke; no real-data or vendor prediction evidence',checks=checks,
    real_datasets_verified=0,model_training_performed=False,real_roas_measured=False,
    preserved_prior_artifacts=len(baseline),test_count=result.testsRun)
save(OUT/'DELIVERABLE_VALIDATION.json',validation)
mp=R/'EVIDENCE_MANIFEST.json';manifest=json.loads(mp.read_text('utf-8'))
paths=[next(R.glob('56_*.md')),OUT/'asset_audit.json',OUT/'ARTIFACT_MANIFEST.json',OUT/'DELIVERABLE_VALIDATION.json',W/'data_contracts/bundle.schema.json']
entry=dict(id='PV56',title='56号第一轮数据资产与契约',claim='No verified real cohort; synthetic checks only; no model training',
    utc=validation['utc'],sources=[dict(path=p.relative_to(R).as_posix(),sha256=sha(p),bytes=p.stat().st_size) for p in paths])
pos=next((i for i,x in enumerate(manifest['entries']) if x['id']=='PV56'),None)
if pos is None:manifest['entries'].append(entry)
else:manifest['entries'][pos]=entry
mp.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n','utf-8')
print(json.dumps({k:v for k,v in validation.items() if k!='checks'},ensure_ascii=False))
for c in checks:
    if not c['passed']:print('FAIL',c)
raise SystemExit(0 if validation['passed'] else 1)
