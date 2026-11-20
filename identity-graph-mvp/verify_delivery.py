"""Offline provenance and delivery checks; never contacts a service or changes research."""
from pathlib import Path
from urllib.parse import unquote,urlsplit
import ast,csv,hashlib,json,re,sqlite3
from datetime import datetime,timezone
from generate_synthetic_data import generate
R=Path(__file__).resolve().parent;P=R.parent
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
checks=[]
def check(label,ok):checks.append(dict(check=label,passed=bool(ok)))
baseline=load(R/'RESEARCH_BASELINE.json')
for p,h in baseline.items():check('preserved:'+p,(P/p).is_file() and sha(P/p)==h)
check('2124 research files preserved',len(baseline)==2124)
for name in ['ACCEPTANCE_TEST_DESIGN.csv','REFERENCE_CONTRACTS.json','RELATIONSHIP_RULES.csv']:
    check('contract exact copy:'+name,(R/'contracts'/name).read_bytes()==(P/'server-identity-reference'/name).read_bytes())
run=R/(R/'LATEST_RUN.txt').read_text().strip();s=load(run/'SUMMARY.json');m=load(run/'RUN_MANIFEST.json')
check('real latest test run PASS',s['status']=='PASS' and s['failures']==s['errors']==0)
check('20 acceptance +20 regression actual execution',s['tests_run']==40 and s['acceptance_passed']==s['acceptance_total']==s['regression_total']==20)
check('131 actual assertions',s['assertions']==131)
for rel,h in m['code_hashes'].items():check('tested source unchanged:'+rel,sha(R/rel)==h)
check('acceptance input hash',sha(R/'contracts/ACCEPTANCE_TEST_DESIGN.csv')==m['source_acceptance_sha256'])
check('seed and network policy',s['seed']==760078 and s['network_connections_allowed'] is False)
original=list(csv.DictReader((R/'contracts/ACCEPTANCE_TEST_DESIGN.csv').open(encoding='utf-8-sig',newline='')))
mapped=list(csv.DictReader((run/'ACCEPTANCE_MAPPING_RESULTS.csv').open(encoding='utf-8-sig',newline='')))
check('all20 exact requirements retained',len(mapped)==len(original)==20)
for old,new in zip(original,mapped):
    tid=old['test_id'];check('original wording:'+tid,new['test_id']==tid and new['original_test']==old['test'] and new['original_expected']==old['expected'] and new['original_rules']==old['rules'])
    check('acceptance passed:'+tid,new['implementation_status']=='PASS')
for case in sorted((run/'cases').iterdir()):
    if not case.is_dir():continue
    outcome=load(case/'RESULT.json');inputs=load(case/'INPUT.json');comp=load(case/'EXPECTATIONS_AND_ACTUALS.json')
    check('case actual PASS:'+case.name,outcome['status']=='PASS' and outcome['assertions']==len(comp)>0)
    check('case inputs:'+case.name,inputs['test_id']==case.name and inputs['seed']==760078 and inputs['environment']=='LOCAL_SYNTHETIC_ONLY' and 'fixture' in inputs and 'operations' in inputs)
    check('case expected/actual captured:'+case.name,all(set(['expected','actual','passed'])<=set(x) and x['passed'] for x in comp))
    for db in ['state.sqlite','privacy.sqlite']:
        connection=sqlite3.connect('file:'+(case/'database'/db).as_posix()+'?mode=ro',uri=True)
        check('sqlite integrity:'+case.name+':'+db,connection.execute('PRAGMA integrity_check').fetchone()[0]=='ok')
        check('sqlite foreign keys:'+case.name+':'+db,connection.execute('PRAGMA foreign_key_check').fetchall()==[])
        connection.close()
check('reported outputs are exact run copies',(R/'SUMMARY.json').read_bytes()==(run/'SUMMARY.json').read_bytes() and (R/'ACCEPTANCE_MAPPING_RESULTS.csv').read_bytes()==(run/'ACCEPTANCE_MAPPING_RESULTS.csv').read_bytes())
check('unittest log confirms actual execution','Ran 40 tests' in (run/'UNITTEST.log').read_text(encoding='utf-8') and '\nOK\n' in (run/'UNITTEST.log').read_text(encoding='utf-8'))
check('generator same-seed deterministic',generate(760078)==generate(760078))
check('generator different seed differs',generate(760078)!=generate(760079))
check('CLI demo executed',load(R/'demo/run-001/SUMMARY.json')['status']=='PASS')
check('demo input is synthetic',load(R/'demo/run-001/INPUT.json')['environment']=='LOCAL_SYNTHETIC_ONLY')
schema=load(R/'DATABASE_SCHEMA.json')
check('actual SQL schema exported',any(x['database']=='privacy.sqlite' and x['table']=='erased_entities' for x in schema) and any(x['table']=='edge_revisions' for x in schema))
for rel in ['README.md','ARCHITECTURE.md','DATABASE_CONTRACTS.md','TEST_REPORT.md','FAILURES_AND_RISKS.md','LTV_FEATURE_ADMISSION.md']:
    text=(R/rel).read_text(encoding='utf-8');check('document and scope:'+rel,len(text)>700 and 'UNKNOWN' in text and 'STOP' in text)
    for link in re.findall(r'\]\(([^)]+)\)',text):
        target=unquote(link.split('#')[0])
        if target and not urlsplit(target).scheme:
            path=(R/rel).parent/target
            check('document link:'+rel+':'+link,path.resolve()==(R/'DELIVERY_VERIFICATION.json').resolve() or path.exists())
tree=ast.parse((R/'identity_mvp/system.py').read_text(encoding='utf-8'))
imports={n.names[0].name.split('.')[0] for n in ast.walk(tree) if isinstance(n,ast.Import)}
check('core no networking library',not imports&{'socket','requests','urllib','http','httpx','aiohttp'})
check('core no model training dependencies',not imports&{'torch','tensorflow','sklearn','xgboost'})
check('all vendor conclusions unchanged',s['C_graph_Axon']==s['C_graph_Vector']==s['D']=='UNKNOWN' and s['production_forensics']=='STOP')
out=dict(checked_utc=datetime.now(timezone.utc).isoformat(),status='PASS' if all(x['passed'] for x in checks) else 'FAIL',
    check_count=len(checks),passed=sum(x['passed'] for x in checks),failed=[x for x in checks if not x['passed']],
    official_run=run.relative_to(R).as_posix(),scope='Static delivery/provenance checks; engineering behavior proven only by linked local synthetic unittest run',checks=checks)
(R/'DELIVERY_VERIFICATION.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:out[k] for k in ['status','check_count','passed','failed','official_run']},ensure_ascii=False))
raise SystemExit(0 if out['status']=='PASS' else 1)
