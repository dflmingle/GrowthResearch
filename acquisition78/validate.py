"""Local document/provenance validation only. No platform evidence evaluator."""
from pathlib import Path
from urllib.parse import unquote,urlsplit
import csv,datetime,hashlib,json,re

R=Path(__file__).resolve().parent.parent
D=Path(__file__).resolve().parent
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def rows(p):return list(csv.DictReader(p.open(encoding='utf-8-sig',newline='')))
checks=[]
def check(name,ok):checks.append(dict(check=name,passed=bool(ok)))
h=load(D/'HISTORY_BEFORE.json')
numbered={k:v for k,v in h.items() if k[:2].isdigit()}
check('148_numbered_inputs',len(numbered)==148)
for path,digest in numbered.items():check('history:'+path,(R/path).is_file() and sha(R/path)==digest)
legacy=load(D/'LEGACY_ARTIFACTS_BEFORE.json')
for path,digest in legacy.items():check('old_artifact:'+path,(R/path).is_file() and sha(R/path)==digest)
for x in load(D/'INPUT_CATALOG.json'):check('read_input:'+x['path'],sha(R/x['path'])==x['sha256'])

before=load(D/'EVIDENCE_GRAPH.before.json')
after=load(R/'prediction-system/EVIDENCE_GRAPH.json')
for k,v in before.items():
    check('graph_old:'+k,after[k][:len(v)]==v if k in ['nodes','edges','sources'] else after.get(k)==v)
check('graph_counts',[len(after[k])-len(before[k]) for k in ['nodes','edges','sources']]==[5,4,5])
check('index_append_only',(R/'EVIDENCE_INDEX.md').read_bytes().startswith((D/'EVIDENCE_INDEX.before.md').read_bytes()))
check('before_index_hash',sha(D/'EVIDENCE_INDEX.before.md')==h['EVIDENCE_INDEX.md'])
check('before_graph_hash',sha(D/'EVIDENCE_GRAPH.before.json')==h['prediction-system/EVIDENCE_GRAPH.json'])
sid={s['id'] for s in after['sources']}
nid={n['id'] for n in after['nodes']}
for kind in ['nodes','edges','sources']:
    prior_ids={x['id'] for x in before[kind]}
    new_ids=[x['id'] for x in after[kind][len(before[kind]):]]
    check('unique_new_ids:'+kind,len(new_ids)==len(set(new_ids)) and not(set(new_ids)&prior_ids))
for edge in after['edges'][len(before['edges']):]:
    check('edge_refs:'+edge['id'],edge['source'] in nid and edge['target'] in nid and set(edge['source_ids'])<=sid)
    check('no_production_edge:'+edge['id'],all(edge.get(k) is False for k in ['production_actual_proven','production_match_proven',
       'prediction_model_consumption_proven','independent_real_identity_lift_proven']) and edge['evidence_stages']==[])
for source in after['sources'][len(before['sources']):]:
    check('spec_hash:'+source['id'],sha(R/source['path'])==source['sha256'])
    check('spec_not_vendor:'+source['id'],source['url'] is None and source['evidence_stages']==[]
      and 'NOT_vendor_production_evidence' in source['evidence_kind'] and source['production_actual_proven'] is False)

readiness=load(D/'READINESS.json')
check('execution_STOP',readiness['execution']=='STOP' and readiness['Axon_C_graph']=='UNKNOWN' and readiness['Vector_C_graph']=='UNKNOWN' and readiness['D_independent_gain']=='UNKNOWN')
check('no_new_platform_evidence',all(readiness[k]==0 for k in ['direct_production_evidence_packages','new_vendor_sources',
 'authorized_test_environments','verified_new_acquisition_opportunities','platform_interfaces_called','public_gets','SDK_scans',
 'job_patent_privacy_partner_searches','mock_runs','synthetic_experiments','model_training_runs']))
check('no_outreach_or_adapter',all(readiness[k] is False for k in ['external_actions_authorized','outreach_sent',
 'actual_contact_or_program_confirmed','engineering76_code_modified','production_adapter_implemented','next_task_created']))
spec=load(D/'ADAPTER_SPEC.json')
check('adapter_design_only',spec['status']=='DESIGN_ONLY_NOT_IMPLEMENTED' and not spec['production_adapter_implemented'] and not spec['production_adapter_connected'])
check('nine_designed_gates',len(spec['gates'])==9 and all(x['executed'] is False for x in spec['gates']))
check('ten_groups',len(rows(D/'CONTRACT_GROUPS.csv'))==10 and spec['required_groups']==[f'F{i:02}' for i in range(1,11)])
channels=rows(D/'CHANNEL_MATRIX.csv')
check('ten_channels_UNKNOWN',len(channels)==10 and all(x['current_feasibility']=='UNKNOWN' and x['authorization_received']=='False' and x['outreach_sent']=='False' for x in channels))

original=rows(R/'75_黑盒可识别性矩阵.csv')
crosswalk=rows(D/'MATRIX75_CROSSWALK.csv')
check('56_design_rows',len(original)==len(crosswalk)==56)
for old,new in zip(original,crosswalk):
    check('75_original_columns:'+old['row_id'],all(new[k]==v for k,v in old.items()))
    check('75_not_execution:'+old['row_id'],new['round78_execution']=='NOT_EXECUTED_DESIGN_CROSSWALK_ONLY' and new['real_evidence_received']=='False')
audit_lines=(R/'engineering76/mock76/auditor.py').read_text(encoding='utf-8').splitlines()
for x in load(D/'CODE_LOCATORS.json'):
    check('exact_code_line:'+str(x['line']),audit_lines[x['line']-1].strip()==x['exact_line'])
reports=sorted(R.glob('78_*.md'))
check('five_reports',len(reports)==5)
for p in reports:
    text=p.read_text(encoding='utf-8')
    check('report_valid_utf8:'+p.name,'\ufffd' not in text and len(text)>1000)

files=reports+[R/'EVIDENCE_INDEX.md',R/'prediction-system/EVIDENCE_GRAPH.json']
files+=sorted(p for p in D.rglob('*') if p.is_file() and p.name not in ['VALIDATION.json','ARTIFACT_MANIFEST.json'] and '__pycache__' not in p.parts)
manifest=[dict(path=p.relative_to(R).as_posix(),bytes=p.stat().st_size,sha256=sha(p)) for p in files]
save(D/'ARTIFACT_MANIFEST.json',manifest)
if not (D/'VALIDATION.json').exists():save(D/'VALIDATION.json',dict(status='RUNNING_LOCAL_INTEGRITY_CHECK'))
for p in reports+[D/'README.md',D/'SOURCE_CATALOG.md']:
    for link in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
        target=link.strip('<>').split('#')[0]
        if not target or urlsplit(target).scheme:continue
        check('link:'+p.name+':'+target,(p.parent/unquote(target)).exists())
for x in manifest:check('manifest:'+x['path'],sha(R/x['path'])==x['sha256'])
result=dict(reviewed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
 status='PASS' if all(x['passed'] for x in checks) else 'FAIL',checks=len(checks),passed=sum(x['passed'] for x in checks),
 failed=[x for x in checks if not x['passed']],historical_numbered_unchanged=len(numbered),legacy_artifacts_unchanged=len(legacy),
 graph_before={k:len(before[k]) for k in ['nodes','edges','sources']},graph_after={k:len(after[k]) for k in ['nodes','edges','sources']},
 crosswalk_rows=56,execution='STOP',new_production_evidence=0,real_C_graph_upgrades=0,
 meaning='Local document/hash/reference preservation only;NOT a run of76,production evidence acceptance or model experiment',details=checks)
save(D/'VALIDATION.json',result)
print(json.dumps({k:v for k,v in result.items() if k!='details'},ensure_ascii=False))
raise SystemExit(0 if result['status']=='PASS' else 1)
