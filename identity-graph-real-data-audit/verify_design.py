"""Validate documents and preservation only; never admit or inspect real records."""
from pathlib import Path
import csv,hashlib,json,re,datetime
from urllib.parse import unquote

ROOT=Path(__file__).resolve().parent
PARENT=ROOT.parent
def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()
def load(path):return json.loads(path.read_text(encoding='utf-8-sig'))
def save(path,value):path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def main():
    # Preserve each prior outcome. Create the declared report before checking
    # local links, so a first-ever run does not fail on its own output link.
    output=ROOT/'VALIDATION.json'
    history=ROOT/'validation-runs';history.mkdir(exist_ok=True)
    if output.exists():
        attempt=1
        while (history/f'attempt-{attempt:03d}.json').exists():attempt+=1
        (history/f'attempt-{attempt:03d}.json').write_bytes(output.read_bytes())
    save(output,dict(status='IN_PROGRESS_NOT_ADMISSION',scope='LOCAL_DESIGN_AND_HASHES_NOT_DATA_ADMISSION'))
    checks=[]
    def check(name,expected,actual):checks.append(dict(name=name,expected=expected,actual=actual,passed=expected==actual))
    protected=load(ROOT/'PRESERVATION_BASELINE.json')
    for path,h in protected.items():
        file=PARENT/path
        check('PRESERVED:'+path,h,sha(file) if file.is_file() else 'MISSING')
    sources=load(ROOT/'SOURCE_REUSE_CATALOG.json')
    for source in sources:
        check('SOURCE_HASH:'+source['id'],source['sha256'],sha(PARENT/source['path']))
        check('NO_NEW_PRIMARY_EVIDENCE:'+source['id'],False,source['new_external_evidence'])
    with (ROOT/'01_真实数据来源及授权可行性矩阵.csv').open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
    check('MATRIX_ENTRIES',14,len(rows));check('UNIQUE_SOURCE_IDS',len(rows),len({r['source_id'] for r in rows}))
    check('CONDITIONAL_NON_DATASET',1,sum(r['source_kind']=='CONDITIONAL_NOT_A_DATASET' for r in rows))
    for row in rows:
        for key in ['existing_license_and_purpose','device_account_app_scope','authorized_cross_app_or_device_links','event_received_available_time',
                    'mature_D1_D7_D30_labels','deletion_revocation_retention','coverage_quality_independent_audit','minimum_new_input','source_refs']:
            check('NONEMPTY:'+row['source_id']+':'+key,True,bool(row[key].strip()))
        for key in ['real_record_processing','real_graph_gain_training']:check('NO_EXECUTION:'+row['source_id']+':'+key,'STOP',row[key])
        for key in ['C_graph_Axon','C_graph_Vector','D']:check('UNCHANGED_CLAIM:'+row['source_id']+':'+key,'UNKNOWN',row[key])
        check('NO_NEW_NETWORK:'+row['source_id'],'False',row['external_recheck_this_round'])
        check('NO_RECORDS_PARSED:'+row['source_id'],'False',row['personal_records_read_this_round'])
        for ref in row['source_refs'].split(';'):
            if '/' in ref or ref.endswith('.md') or ref.endswith('.csv') or ref.endswith('.json'):
                check('REFERENCE_EXISTS:'+ref,True,(PARENT/ref).is_file())
    ready=load(ROOT/'CURRENT_READINESS.json');check('NO_QUALIFYING_REAL_DATA',0,ready['qualifying_real_graph_gain_datasets'])
    check('NO_TRAINING','STOP',ready['real_training']);check('NO_PRODUCTION','STOP',ready['production_forensics'])
    check('BASELINE_COUNT',len(protected),ready['preserved_files'])
    protocol=load(ROOT/'PREREGISTRATION_MANIFEST.json')
    check('PROTOCOL_NOT_FALSLY_EXECUTABLE','CONDITIONAL_PROTOCOL_LOCKED_EXECUTION_STOP',protocol['status'])
    check('NO_DATA_RECEIVED',False,protocol['data_package_received'])
    check('FINAL_DATES_NOT_INVENTED',None,protocol['time_split']['anchor_utc'])
    check('POWER_NOT_INVENTED',None,protocol['quality_and_power']['required_independent_cluster_count'])
    check('SYNTHETIC_EFFECT_NOT_PRIOR',False,protocol['quality_and_power']['real_effect_prior_from_synthetic'])
    check('NO_FALSE_FREEZE',False,protocol['freeze']['all_required_fields_verified'])
    md_files=sorted(ROOT.glob('*.md'))
    check('SIX_MAIN_DELIVERABLES',6,len(list(ROOT.glob('0[1-6]_*'))))
    for path in md_files:
        content=path.read_text(encoding='utf-8')
        for target in re.findall(r'\]\(([^)]+)\)',content):
            if target.startswith(('https://','http://','#')):continue
            link=unquote(target.split('#',1)[0].strip('<>'))
            check('LOCAL_LINK:'+path.name+':'+link,True,(path.parent/link).exists())
    # Gate names are deliberately distinct from inherited G01-G12 evidence gaps.
    checker=(ROOT/'04_数据准入和STOP检查器设计.md').read_text(encoding='utf-8')
    for i in range(12):check('GATE_SPEC:'+str(i),True,f'RA{i:02d}' in checker)
    gaps=(ROOT/'05_Axon_Vector关键证据缺口及突破条件.md').read_text(encoding='utf-8')
    for value in ['C_graph.Axon=UNKNOWN','C_graph.Vector=UNKNOWN','D=UNKNOWN','原生产取证STOP','C_GRAPH_CONFIRMED_SCOPED','Exchange']:
        check('CLAIM_BOUNDARY:'+value,True,value in gaps)
    failures=[c for c in checks if not c['passed']]
    validation=dict(status='FAIL' if failures else 'PASS_DOCUMENT_INTEGRITY_ONLY',
      verified_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),scope='LOCAL_DESIGN_AND_HASHES_NOT_DATA_ADMISSION',
      checks=len(checks),failures=failures,protected_files=len(protected),reused_metadata_sources=len(sources),
      matrix_entries=len(rows),real_records_loaded=0,real_models_trained=0,external_requests=0,
      C_graph_Axon='UNKNOWN',C_graph_Vector='UNKNOWN',D='UNKNOWN',production_forensics='STOP',checks_detail=checks)
    save(ROOT/'VALIDATION.json',validation)
    manifest={p.relative_to(ROOT).as_posix():sha(p) for p in sorted(ROOT.rglob('*'))
        if p.is_file() and p.name!='ARTIFACT_MANIFEST.json' and '__pycache__' not in p.parts}
    save(ROOT/'ARTIFACT_MANIFEST.json',dict(scope='DESIGN_ARTIFACTS_ONLY',files=manifest))
    print(json.dumps({k:validation[k] for k in ['status','checks','protected_files','reused_metadata_sources','matrix_entries','real_records_loaded','real_models_trained','external_requests']},ensure_ascii=False))
    if failures:raise SystemExit(1)

if __name__=='__main__':main()
