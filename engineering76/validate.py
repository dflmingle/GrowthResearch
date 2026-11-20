"""Integrity and evidence freshness verification;does not rerun or enlarge tests."""
from pathlib import Path
import ast,csv,datetime,hashlib,json,re,sys

R=Path(__file__).resolve().parent.parent;D=R/'engineering76';O=D/'results/acceptance-v3';V=D/'VALIDATION.json'
sys.path.insert(0,str(D))
from mock76.io import verify
from mock76.auditor import audit

checks=[]
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def check(name,ok,detail=''):
    checks.append(dict(name=name,pass_check=bool(ok),detail=detail))
    if not ok:raise AssertionError(name+': '+str(detail))

def main():
    save(V,dict(status='RUNNING',started_utc=datetime.datetime.now(datetime.timezone.utc).isoformat()))
    baseline=read(D/'HISTORY_BEFORE.json');old=read(D/'EVIDENCE_GRAPH.before.json');g=read(R/'prediction-system/EVIDENCE_GRAPH.json')
    for rel,digest in baseline.items():
        if rel not in ['EVIDENCE_INDEX.md','prediction-system/EVIDENCE_GRAPH.json']:
            check('Historical bytes: '+rel,sha(R/rel)==digest)
    check('142 old numbered files unchanged',len(baseline)-2==142)
    check('Frozen graph baseline',sha(D/'EVIDENCE_GRAPH.before.json')==baseline['prediction-system/EVIDENCE_GRAPH.json'])
    check('Frozen index baseline',sha(D/'EVIDENCE_INDEX.before.md')==baseline['EVIDENCE_INDEX.md'])
    check('Index append only',(R/'EVIDENCE_INDEX.md').read_bytes().startswith((D/'EVIDENCE_INDEX.before.md').read_bytes()))
    for k,v in old.items():check('Old graph section: '+k,g[k][:len(v)]==v if k in ['nodes','edges','sources'] else g[k]==v)
    for x in read(R/'blackbox75/ARTIFACT_MANIFEST.json'):
        if x['path'] not in ['EVIDENCE_INDEX.md','prediction-system/EVIDENCE_GRAPH.json']:
            check('Prior75 artifact: '+x['path'],sha(R/x['path'])==x['sha256'])
    for k in ['nodes','edges','sources']:check('Unique graph IDs: '+k,len(g[k])==len({x['id'] for x in g[k]}))
    nn=g['nodes'][len(old['nodes']):];ne=g['edges'][len(old['edges']):];ns=g['sources'][len(old['sources']):]
    check('Only expected new objects',(len(nn),len(ne),len(ns))==(11,12,12))
    ni={x['id'] for x in g['nodes']};si={x['id'] for x in g['sources']}
    check('New graph references valid',all(e['source'] in ni and e['target'] in ni and set(e['source_ids'])<=si for e in ne))
    check('No production E5/E6 upgrade',all(not set(x['evidence_stages'])&{'E5','E6'} and x['production_match_proven'] is False and x['prediction_model_consumption_proven'] is False and x['independent_real_identity_lift_proven'] is False for x in ns+ne))
    for x in ns+read(D/'REUSED_EVIDENCE.json'):check('Source SHA: '+x['id'],sha(R/x['path'])==x['sha256'])
    summary=read(O/'SUMMARY.json');units=read(O/'UNITTEST.json');reg=read(O/'REGRESSION_RESULTS.json')
    check('Final acceptance current PASS',summary['status']=='PASS' and summary['seed']==760031 and summary['matrix_cases']==summary['matrix_passed']==56 and summary['regressions_passed']==summary['process_regressions']==13 and summary['unit_tests']==40 and summary['unit_passed'])
    check('No unit skips/failures/errors',units['tests_run']==40 and units['passed'] and not units['failures'] and not units['errors'] and units['skipped']==0)
    check('All process regressions PASS',len(reg)==13 and all(x['passed'] for x in reg))
    for rel,digest in read(O/'CODE_AT_RUN.json').items():check('Code matches actual final run: '+rel,sha(D/rel)==digest)
    tests=ast.parse((D/'tests/test_engine.py').read_text('utf-8'))
    check('40 current test methods',len([x for x in ast.walk(tests) if isinstance(x,ast.FunctionDef) and x.name.startswith('test_')])==40)
    check('40 preserved unit-case service logs',len(list((O/'unit_cases').iterdir()))==40 and all((p/'audit/ledger.jsonl').exists() and (p/'private/service_state.json').exists() for p in (O/'unit_cases').iterdir()))
    manifest=read(O/'MANIFEST.json')
    check('Complete final-run file manifest',len(manifest)==len([p for p in O.rglob('*') if p.is_file() and p.name!='MANIFEST.json']))
    check('All final-run artifacts match hashes',all(sha(R/x['path'])==x['sha256'] and (R/x['path']).stat().st_size==x['bytes'] for x in manifest))
    # All full process results must still reproduce verdicts from only the recorded packet.
    packets=list((O/'process_runs').glob('*/audit/packet.json'))
    check('Ten finite process fixtures,not Monte Carlo',len(packets)==10)
    for p in packets:
        packet=read(p);verdict=read(p.with_name('verdict.json'))
        check('Public packet reproducible independent verdict: '+p.parents[1].name,audit(packet)==verdict)
        check('Process log chain: '+p.parents[1].name,verify(packet['records']))
        transcript=[json.loads(s) for s in (p.parents[1]/'process_transcript.jsonl').read_text('utf-8').splitlines()]
        check('Subprocess transcript chain: '+p.parents[1].name,verify(transcript) and all(x['data']['returncode']==0 for x in transcript))
        modules={x['data']['module'] for x in transcript}
        check('Source target service auditor actually launched: '+p.parents[1].name,{'mock76.app_source','mock76.app_target','mock76.service','mock76.auditor'}<=modules)
        check('Response only remains unknown: '+p.parents[1].name,read(p.with_name('external_verdict.json'))['status']=='UNIDENTIFIABLE')
    main={route:read(O/f'process_runs/{route}/audit/verdict.json') for route in ['D0','D1','LEAK']}
    check('D1 response equals LEAK response but routes differ',main['D1']['requests'][0]['response']==main['LEAK']['requests'][0]['response'] and main['D1']['routes']==['SAME_DEVICE_HISTORY_READ'] and main['LEAK']['routes']==['CONTEXT_LEAKAGE'])
    check('Seeded complete audit replay identical',read(O/'process_runs/D1/audit/packet.json')==read(O/'process_runs/replay_D1/audit/packet.json'))
    check('Auditor isolated from private files',sorted(p.name for p in (O/'auditor_isolated').iterdir())==['packet.json','verdict.json'] and read(O/'auditor_isolated/verdict.json')==main['D1'])
    with (R/'75_黑盒可识别性矩阵.csv').open(encoding='utf-8-sig',newline='') as f:original=list(csv.DictReader(f))
    cases=read(O/'CASES.json');compiled=read(D/'acceptance/CASES.json')
    check('Original56 exact row preservation',[x['original_row'] for x in cases['cases']]==original and len(original)==cases['row_count']==56 and cases==compiled)
    check('Original matrix SHA retained',sha(R/cases['source_path'])==cases['source_sha256'])
    with (O/'MATRIX_RESULTS.csv').open(encoding='utf-8-sig',newline='') as f:matrix=list(csv.DictReader(f))
    check('Every original ID has one passing result',[x['case_id'] for x in matrix]==[x['row_id'] for x in original] and all(x['passed']=='True' for x in matrix))
    for c in cases['cases']:
        x=read(O/f"matrix_cases/{c['case_id']}.json")
        check('Row-specific contract: '+c['case_id'],x['case']==c and x['verdict']['status']==c['expected_status'] and x['hypothesis_observed']==c['hypothesis_outcome'] and x['passed'])
        claims=set(x['verdict']['claims'])
        check('Required/forbidden claims: '+c['case_id'],set(c['required_claims'])<=claims and not claims&set(c['forbidden_claims']))
        if c['observation_level'] in ['feature','score','audience','match']:
            check('Evidence ablation unknown: '+c['case_id'],x['weakened_verdict']['status']=='UNIDENTIFIABLE' and not x['weakened_verdict']['claims'])
        if c['observation_level']=='match':
            check('Derived not existing match: '+c['case_id'],'provider_maintained_status' not in x['derived_variant_verdict']['claims'])
    # Actual module dependency audit:engine/auditor are standard library and local package only.
    imports={}
    for p in (D/'mock76').glob('*.py'):
        tree=ast.parse(p.read_text('utf-8'));names=[]
        for x in ast.walk(tree):
            if isinstance(x,ast.Import):names.extend(z.name for z in x.names)
            elif isinstance(x,ast.ImportFrom) and not x.level:names.append(x.module or '')
        imports[p.name]=names
        check('No external network or SDK import: '+p.name,all(n.split('.')[0] in ['argparse','random','pathlib','hashlib','json','os','sys'] for n in names))
    auditor=(D/'mock76/auditor.py').read_text('utf-8')
    check('Auditor no service/private dependency','from .service' not in auditor and 'private/' not in auditor and 'service_state' not in auditor)
    check('No new statistics or real platform claims',summary['scope'].startswith('offline engineering') and summary['real_platform_claims'] is False and summary['no_external_calls'])
    # New documentation only;frozen historical index has links relative to its original root.
    docs=[next(R.glob('76_*.md')),D/'README.md',D/'TEST_REPORT.md']
    for p in docs:
        txt=p.read_text('utf-8');check('No replacement decoding: '+p.name,'\ufffd' not in txt)
        for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',txt):
            target=target.strip('<>').split('#')[0]
            if not target or re.match(r'https?://|mailto:',target):continue
            check('New local link: '+p.name+' -> '+target,(p.parent/target).exists())
    paths=docs+[R/'EVIDENCE_INDEX.md',R/'prediction-system/EVIDENCE_GRAPH.json']+[p for p in D.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p not in [V,D/'ARTIFACT_MANIFEST.json']]
    artifact=[dict(path=p.relative_to(R).as_posix(),bytes=p.stat().st_size,sha256=sha(p)) for p in sorted(set(paths))]
    save(D/'ARTIFACT_MANIFEST.json',artifact)
    result=dict(status='PASS',completed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),checks_passed=len(checks),checks=checks,
      historical_numbered_files_unchanged=len(baseline)-2,matrix_passed=56,process_regressions_passed=13,unit_tests_passed=40,
      graph_counts={k:len(g[k]) for k in ['nodes','edges','sources']},code_freshness='Final v3 run code hashes match current engine/tests',
      actual_apps='Two Python CLI mock processes;not mobile APKs',actual_external_requests=0,real_identity_query=False,real_platform_evidence=False,
      C_graph='UNKNOWN',D_real_value_gain='UNKNOWN',artifact_manifest_sha256=sha(D/'ARTIFACT_MANIFEST.json'),
      limitations=['Hash/link checks are integrity,not independent production authentication','Language-level network guard,not OS sandbox','H2/person/household not implemented;matrix confirms bounded/unknown behavior','No new statistical efficacy experiment or real value labels'])
    save(V,result)
    print(json.dumps({k:result[k] for k in ['status','checks_passed','historical_numbered_files_unchanged','matrix_passed','process_regressions_passed','unit_tests_passed','graph_counts']},indent=2))

if __name__=='__main__':
    try:main()
    except Exception as e:save(V,dict(status='FAIL',error=repr(e),checks=checks));raise
