"""Metadata-only delivery verification and standalone review-kit packaging."""
from pathlib import Path
import csv,hashlib,json,re,datetime,zipfile

ROOT=Path(__file__).resolve().parent
PARENT=ROOT.parent
def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()
def load(path):return json.loads(path.read_text(encoding='utf-8-sig'))
def save(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def readcsv(path):
    with path.open(encoding='utf-8-sig',newline='') as f:
        reader=csv.DictReader(f);return reader.fieldnames,list(reader)

def main():
    checks=[]
    def check(name,expected,actual):checks.append(dict(name=name,expected=expected,actual=actual,passed=expected==actual))
    baseline=load(ROOT/'internal/PRESERVATION_BASELINE.json')
    for name,expected in baseline.items():
        path=PARENT/name
        check('PRESERVED:'+name,expected,sha(path) if path.is_file() else 'MISSING')
    for source in load(ROOT/'internal/SOURCE_REUSE.json'):
        check('SOURCE_REUSED:'+source['path'],source['sha256'],sha(PARENT/source['path']))
    build=load(ROOT/'internal/BUILD_SUMMARY.json')
    columns,rows=readcsv(ROOT/'02_最小Schema审核模板.csv')
    check('EXACT_FIVE_SCHEMA_COLUMNS',['field_name','type','semantics','constraints','synthetic_example'],columns)
    check('SCHEMA_FIELD_COUNT',90,len(rows));check('UNIQUE_FIELD_NAMES',90,len({r['field_name'] for r in rows}))
    check('BUILD_MATCHES_FIELDS',len(rows),build['schema_rows'])
    for row in rows:
        for column in columns:check('NONEMPTY:'+row['field_name']+':'+column,True,bool(row[column].strip()))
        example=row['synthetic_example']
        # These checks support generated-field consistency, not real anonymization.
        if row['type'].startswith(('object','array')):
            value=json.loads(example)
            check('EXAMPLE_CONTAINER:'+row['field_name'],True,isinstance(value,(dict,list)))
        if row['type']=='int64':check('EXAMPLE_INTEGER:'+row['field_name'],True,isinstance(int(example),int))
        if row['type']=='utc':check('FICTIONAL_TIME:'+row['field_name'],True,example.startswith('2035-') and example.endswith('Z'))
        check('NO_EMAIL_IN_EXAMPLE:'+row['field_name'],False,bool(re.search(r'\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b',example)))
        check('NO_UUID_AD_ID_EXAMPLE:'+row['field_name'],False,bool(re.search(r'\b[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}\b',example,re.I)))
    for i in range(10):
        group=f'P{i}';header,group_rows=readcsv(ROOT/'schema'/f'{group}_字段审核模板.csv')
        check('GROUP_HEADERS:'+group,columns,header)
        check('GROUP_EXACT_MASTER_SUBSET:'+group,[r for r in rows if r['field_name'].startswith(group+'.')],group_rows)
    _,gates=readcsv(ROOT/'04_真实实验准入判定表.csv')
    check('GATE_IDS',[f'RA{i:02d}' for i in range(12)],[g['gate_id'] for g in gates])
    for gate in gates:
        check('UNANSWERED:'+gate['gate_id'],'UNANSWERED',gate['partner_answer'])
        check('NOT_VERIFIED:'+gate['gate_id'],'UNKNOWN',gate['verification_status'])
        check('DEFAULT_DENY:'+gate['gate_id'],'STOP' if gate['gate_id'] in ['RA00','RA06','RA08'] else 'HOLD',gate['gate_decision'])
    template=load(ROOT/'04_准入结论填写模板.json')
    for key in ['partner_submission_received','explicit_authority_verified','legal_relationship_basis_verified','mature_labels_verified','all_RA00_RA11_verified']:
        check('NO_FALSE_APPROVAL:'+key,False,template[key])
    check('OVERALL_STOP','STOP',template['overall_experiment_decision'])
    for key in ['C_graph_Axon','C_graph_Vector','D']:check('UNKNOWN:'+key,'UNKNOWN',template[key])
    check('PRODUCTION_STOP','STOP',template['production_forensics'])
    question=(ROOT/'01_合作方技术问卷.md').read_text(encoding='utf-8')
    check('SIX_SHORT_QUESTIONS',6,len(re.findall(r'^\d+\. \*\*Q[1-6]',question,re.M)))
    names=[
      'README.md','01_合作方技术问卷.md','02_最小Schema审核说明.md','02_最小Schema审核模板.csv',
      '03_权限及数据处理边界清单.md','04_真实实验准入填写说明.md','04_真实实验准入判定表.csv',
      '04_准入结论填写模板.json','05_合作方环境内评估方案.md','06_尚待合作方确认的问题.md'
    ]+[f'schema/P{i}_字段审核模板.csv' for i in range(10)]
    for name in names:check('DELIVERABLE_EXISTS:'+name,True,(ROOT/name).is_file())
    allowed=set(names)
    for name in names:
        if name.endswith('.md'):
            text=(ROOT/name).read_text(encoding='utf-8')
            for target in re.findall(r'\]\(([^)]+)\)',text):
                check('SELF_CONTAINED_LINK:'+name+':'+target,True,target in allowed)
            for banned in ['65.7847','39.9476','-25.8371']:
                check('NO_SYNTHETIC_GAIN_MARKETING:'+name+':'+banned,False,banned in text)
    failures=[c for c in checks if not c['passed']]
    if failures:
        save(ROOT/'internal/VALIDATION.json',dict(status='FAIL',scope='DOCUMENTS_ONLY_NOT_ADMISSION',failures=failures,checks_detail=checks))
        print(json.dumps(failures,ensure_ascii=False));raise SystemExit(1)
    # Strict allowlist: no scripts, prior reports, preservation hashes or raw rows.
    archive=ROOT/'partner-review-kit.zip'
    with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        z.comment=b'Metadata forms and synthetic field examples only; not authorization.'
        for name in sorted(names):
            info=zipfile.ZipInfo(name,date_time=(2026,11,20,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
            info.external_attr=0o100644<<16
            z.writestr(info,(ROOT/name).read_bytes())
    with zipfile.ZipFile(archive) as z:
        check('ZIP_CRC',None,z.testzip());check('ZIP_EXACT_ALLOWLIST',sorted(names),sorted(z.namelist()))
        for name in names:
            check('ZIP_MEMBER_BYTES:'+name,hashlib.sha256((ROOT/name).read_bytes()).hexdigest(),hashlib.sha256(z.read(name)).hexdigest())
    failures=[c for c in checks if not c['passed']]
    validation=dict(status='FAIL' if failures else 'PASS_DOCUMENTS_AND_ARCHIVE_ONLY',
      scope='NOT_REAL_DATA_ADMISSION_NOT_PRODUCTION_EVIDENCE',verified_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
      checks=len(checks),failures=failures,preserved_files=len(baseline),schema_fields=len(rows),schema_packages=10,gates=12,
      partner_kit_files=len(names),archive=archive.name,archive_sha256=sha(archive),archive_bytes=archive.stat().st_size,
      real_records_read=0,third_parties_contacted=0,applications_sent=0,real_models_trained=0,
      actual_experiment_admission='STOP',C_graph_Axon='UNKNOWN',C_graph_Vector='UNKNOWN',D='UNKNOWN',production_forensics='STOP',
      checks_detail=checks)
    save(ROOT/'internal/VALIDATION.json',validation)
    save(ROOT/'internal/PARTNER_KIT_MANIFEST.json',dict(archive=archive.name,sha256=sha(archive),
      files={name:sha(ROOT/name) for name in sorted(names)},excluded=['internal/*','*.py','historical evidence','real record files']))
    save(ROOT/'internal/ARTIFACT_MANIFEST.json',{p.relative_to(ROOT).as_posix():sha(p) for p in sorted(ROOT.rglob('*'))
      if p.is_file() and p.name!='ARTIFACT_MANIFEST.json' and '__pycache__' not in p.parts})
    print(json.dumps({k:validation[k] for k in ['status','checks','preserved_files','schema_fields','schema_packages','gates','partner_kit_files','archive_bytes','actual_experiment_admission']},ensure_ascii=False))
    if failures:raise SystemExit(1)

if __name__=='__main__':main()
