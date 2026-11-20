"""Offline artifact/source audit. Does not run SDKs, simulations or experiments."""
from pathlib import Path
import csv,hashlib,json,re,datetime

ROOT=Path(__file__).resolve().parent
PARENT=ROOT.parent
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def save(p,obj):p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()
def readcsv(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))

def main():
    # The report is a declared output, not evidence of successful data admission.
    save(ROOT/'VALIDATION.json',dict(status='IN_PROGRESS_DOCUMENTS_ONLY'))
    checks=[]
    def check(name,expected,actual):checks.append(dict(name=name,expected=expected,actual=actual,passed=expected==actual))
    baseline=load(ROOT/'PRESERVATION_BASELINE.json')
    for name,h in baseline.items():
        p=PARENT/name;check('PRESERVED:'+name,h,sha(p) if p.is_file() else 'MISSING')
    for s in load(ROOT/'REUSED_SOURCES.json'):check('REUSED_SOURCE:'+s['id'],s['sha256'],sha(PARENT/s['path']))
    evidence=readcsv(ROOT/'MECHANISM_EVIDENCE.csv');check('MECHANISM_ROWS',15,len(evidence))
    ids={r['id'] for r in evidence}
    for r in evidence:
        check('STATUS_ENUM:'+r['id'],True,r['status'] in ['CONFIRMED','INFERRED','UNKNOWN'])
        check('SOURCE_HASH:'+r['id'],r['source_sha256'],sha(PARENT/r['source_file']))
        for key in ['product','version_or_time_scope','direct_observation','technical_interpretation','alternative_explanation','missing_evidence','independent_implementation_guidance']:
            check('SCOPED_FIELD:'+r['id']+':'+key,True,bool(r[key].strip()))
        check('NO_NEW_VENDOR_MECHANISM:'+r['id'],'False',r['new_vendor_mechanism'])
        check('NO_PRODUCTION_UPGRADE:'+r['id'],'UNKNOWN',r['production_graph_consumption'])
    matrix=readcsv(ROOT/'01_Axon_Vector机制差异矩阵.csv');check('COMPARISON_LAYERS',6,len(matrix))
    for row in matrix:
        for vendor in ['Axon','Vector']:
            check('CELL_STATUS:'+row['level_id']+vendor,True,row[vendor+'_status'] in ['CONFIRMED','INFERRED','UNKNOWN'])
            for id in row[vendor+'_evidence'].split('/'):check('CELL_EVIDENCE:'+row['level_id']+vendor+id,True,id in ids)
        for name in ['C_graph_Axon','C_graph_Vector','D']:check('UNKNOWN:'+row['level_id']+name,'UNKNOWN',row[name])
    check('VECTOR_INPUT_NOT_INHERITED_FROM_UPA','UNKNOWN',matrix[0]['Vector_status'])
    candidates=readcsv(ROOT/'02_最值得复制的机制清单.csv');check('CANDIDATES',4,len(candidates))
    check('NO_FOURTH_MINIMUM_EXPERIMENT',True,candidates[-1]['recommendation'].startswith('HOLD'))
    designs=load(ROOT/'EXPERIMENT_DESIGNS.json');check('AT_MOST_THREE_EXPERIMENTS',True,len(designs)<=3)
    check('DESIGN_IDS',['E01','E02','E03'],[r['id'] for r in designs])
    for r in designs:
        check('NOT_EXECUTED:'+r['id'],'NOT_EXECUTED',r['status'])
        check('NO_FAKE_RESULTS:'+r['id'],None,r['actual_results'])
        check('FIXED_SEED:'+r['id'],780241,r['seed'])
        for key in ['hypothesis','inputs','expected_observations','failure_criteria','stop_conditions']:
            check('PLAN_COMPLETE:'+r['id']+key,True,bool(r[key]))
    fetch=load(ROOT/'FETCH_MANIFEST.json');check('BOUNDED_TARGETS',2,len(fetch))
    for r in fetch:
        check('METADATA_ONLY:'+r['id'],False,r['sdk_download'])
        check('NOT_PRODUCTION:'+r['id'],False,r['production_evidence'])
        if r.get('raw_path'):check('RAW_RESPONSE_HASH:'+r['id'],r['sha256'],sha(ROOT/r['raw_path']))
    notes=load(ROOT/'RELEASE_NOTES_REVIEW.json');check('RELEASE_NOTE_COUNT',10,len(notes))
    for r in notes:check('NO_FALSE_NOTE_BREAKTHROUGH:'+r['source_id']+r['tag'],'NO_NEW_IDENTITY_MECHANISM_OR_MODEL_MAPPING_IN_REVIEWED_NOTE',r['novelty'])
    status=load(ROOT/'STATUS.json')
    for key in ['new_vendor_mechanisms','new_C_graph_evidence','experiments_executed','models_trained']:check('ZERO:'+key,0,status[key])
    for key in ['C_graph_Axon','C_graph_Vector','D']:check('CLAIM_STILL_UNKNOWN:'+key,'UNKNOWN',status[key])
    check('PRODUCTION_STOP','STOP',status['production_forensics'])
    for path in ROOT.glob('*.md'):
        for target in re.findall(r'\]\(([^)]+)\)',path.read_text(encoding='utf-8')):
            if not target.startswith(('http://','https://','#')):check('LOCAL_LINK:'+path.name+':'+target,True,(path.parent/target).exists())
    failures=[x for x in checks if not x['passed']]
    result=dict(status='FAIL' if failures else 'PASS_DOCUMENTS_AND_PRESERVATION_ONLY',
      verified_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),checks=len(checks),failures=failures,
      protected_files=len(baseline),evidence_rows=len(evidence),comparison_layers=len(matrix),minimum_plans=len(designs),
      experiments_run=0,new_vendor_mechanisms=0,production_graph_evidence=0,
      C_graph_Axon='UNKNOWN',C_graph_Vector='UNKNOWN',D='UNKNOWN',production_forensics='STOP',checks_detail=checks)
    save(ROOT/'VALIDATION.json',result)
    save(ROOT/'ARTIFACT_MANIFEST.json',{p.relative_to(ROOT).as_posix():sha(p) for p in sorted(ROOT.rglob('*'))
        if p.is_file() and p.name!='ARTIFACT_MANIFEST.json' and '__pycache__' not in p.parts})
    print(json.dumps({k:result[k] for k in ['status','checks','protected_files','evidence_rows','comparison_layers','minimum_plans','experiments_run','new_vendor_mechanisms']},ensure_ascii=False))
    if failures:print(json.dumps(failures,ensure_ascii=False));raise SystemExit(1)

if __name__=='__main__':main()
