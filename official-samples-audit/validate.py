"""Hash/document/license-provenance checks only. Not SDK analysis or a test run."""
from pathlib import Path
from urllib.parse import unquote,urlsplit
import csv,datetime,hashlib,json,re

R=Path(__file__).resolve().parent.parent
D=Path(__file__).resolve().parent
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rows(p):return list(csv.DictReader(p.open(encoding='utf-8-sig',newline='')))
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
checks=[]
def check(name,ok):checks.append(dict(check=name,passed=bool(ok)))
h=load(D/'HISTORY_BEFORE.json')
numbered={p:s for p,s in h.items() if p[:2].isdigit()}
check('153 historical numbered files',len(numbered)==153)
for p,s in numbered.items():check('historical:'+p,(R/p).is_file() and sha(R/p)==s)
old=load(D/'EVIDENCE_GRAPH.before.json');new=load(R/'prediction-system/EVIDENCE_GRAPH.json')
for key,value in old.items():check('old graph:'+key,new[key][:len(value)]==value if key in ['nodes','edges','sources'] else new.get(key)==value)
check('graph append counts',[len(new[k])-len(old[k]) for k in ['nodes','edges','sources']]==[5,5,13])
check('index byte prefix',(R/'EVIDENCE_INDEX.md').read_bytes().startswith((D/'EVIDENCE_INDEX.before.md').read_bytes()))
check('frozen index hash',sha(D/'EVIDENCE_INDEX.before.md')==h['EVIDENCE_INDEX.md'])
check('frozen graph hash',sha(D/'EVIDENCE_GRAPH.before.json')==h['prediction-system/EVIDENCE_GRAPH.json'])
old_sources={x['id']:x for x in old['sources']}
check('76 auditor untouched',sha(R/old_sources['EN76S04']['path'])==old_sources['EN76S04']['sha256'])
for x in load(R/'acquisition78/ARTIFACT_MANIFEST.json'):
    shared={'EVIDENCE_INDEX.md':D/'EVIDENCE_INDEX.before.md','prediction-system/EVIDENCE_GRAPH.json':D/'EVIDENCE_GRAPH.before.json'}
    target=shared.get(x['path'],R/x['path'])
    check('round78 artifact:'+x['path'],target.is_file() and sha(target)==x['sha256'])
for p,s in load(D/'REUSED_ARTIFACT_HASHES.json').items():check('sample/metadata:'+p,(R/p).is_file() and sha(R/p)==s)
samples=rows(D/'ACQUIRED_SAMPLE_CATALOG.csv')
check('47 samples',len(samples)==47)
check('30 versions',len(load(D/'VERSION_PROVENANCE.json'))==30)
check('sample paths unique',len({x['path'] for x in samples})==47)
check('formats', {fmt:sum(s['format']==fmt for s in samples) for fmt in ['aar','sources.jar','tgz']}==dict(aar=26,**{'sources.jar':17},tgz=4))
for s in samples:
    check('sample hash:'+s['sample_id'],sha(R/s['path'])==s['sha256']==s['recorded_sha256'])
    check('sample source:'+s['sample_id'],bool(s['official_download_url']) and sha(R/s['provenance'])==s['provenance_sha256'])
    check('not new analysis:'+s['sample_id'],s['new_functional_analysis']=='NOT_STARTED' and s['production_model_consumption']=='UNKNOWN')
    check('date typed:'+s['sample_id'],s['publication_date_type'] in ['Official UPM registry timestamp','UNKNOWN;HTTP Last-Modified is separate'])
ready=[s for s in samples if s['permission_gate']=='GO_SOURCE_REVIEW_ONLY_NEXT_PHASE']
check('only3 MIT source candidates',len(ready)==3 and all(s['sdk']=='Adjust/Android' and s['format']=='sources.jar' for s in ready))
for x in rows(D/'OFFICIAL_DOWNLOAD_CANDIDATES.csv'):
    check('candidate not acquired:'+x['product'],x['local_sdk_sha256']=='NOT_ACQUIRED' and x['analysis_status']=='NOT_STARTED')
for x in load(D/'FETCH_MANIFEST.json'):
    check('public response:'+x['id'],sha(R/x['path'])==x['sha256'])
    check('response text:'+x['id'],sha(R/x['text_path'])==x['text_sha256'])
check('22 metadata GETs',len(load(D/'FETCH_MANIFEST.json'))==22)
for x in load(D/'LICENSE_EVIDENCE.json'):
    text=(R/x['readable_path']).read_text(encoding='utf-8-sig')
    check('license raw:'+x['id'],sha(R/x['raw_path'])==x['raw_sha256'])
    check('license text:'+x['id'],sha(R/x['readable_path'])==x['readable_sha256'])
    check('license quote:'+x['id'],x['quote'] in text and text[:text.index(x['quote'])].count('\n')+1==x['quote_line'])
for x in load(D/'DECODED_LICENSES.json'):check('decoded license:'+x['id'],sha(R/x['path'])==x['sha256'])
for x in load(D/'REUSED_SOURCE_REFERENCES.json'):check('legacy ref:'+x['id'],sha(R/x['path'])==x['sha256'])
fields=rows(D/'IDENTITY_FIELD_REUSE_MATRIX.csv');maps=rows(D/'CALL_RELATION_REUSE_MATRIX.csv')
check('30 fields/10 mappings',(len(fields),len(maps))==(30,10))
check('all old field refs located',all(not f['unresolved_source_ids'] for f in fields))
original=load(R/'identity72-experiments73/IDENTIFIER_INVENTORY.json')
for oldrow,row in zip(original,fields):
    check('field scope:'+row['reuse_id'],row['field']==oldrow['field'] and row['namespace_scope']==oldrow['cross_app_scope']
      and row['source_ids']==';'.join(oldrow['evidence_ids']) and row['value_model_consumption_proven']=='False')
mechanisms=rows(D/'MECHANISM_TEST_DESIGN.csv')
check('5 unexecuted designs',len(mechanisms)==5 and all(m['execution']=='NOT_RUN_DESIGN_ONLY' and m['vendor_model_use']=='UNKNOWN' for m in mechanisms))
for m in mechanisms:check('mechanism refs:'+m['mechanism_id'],all(sid in old_sources for sid in m['legacy_refs'].split(';')))
status=load(D/'STATUS.json')
check('no execution',all(status[k]==0 for k in ['current_new_functional_static_analyses','new_SDK_bundles','new_core_decompiles','production_SDK_runs','identity_queries','real_ad_requests','official_repo_implementation_files_read']))
check('78 states retained',status['Axon_C_graph']==status['Vector_C_graph']==status['D']=='UNKNOWN' and status['original_production_forensics']=='STOP' and not status['engineering76_modified'] and not status['reference_implementation_started'])
ns={s['id'] for s in new['sources']};nn={n['id'] for n in new['nodes']}
for e in new['edges'][len(old['edges']):]:
    check('edge refs:'+e['id'],e['source'] in nn and e['target'] in nn and set(e['source_ids'])<=ns)
    check('no graph upgrade:'+e['id'],all(e[k] is False for k in ['production_actual_proven','production_match_proven','prediction_model_consumption_proven','independent_real_identity_lift_proven']))
for s in new['sources'][len(old['sources']):]:check('new source hash:'+s['id'],sha(R/s['path'])==s['sha256'])
files=sorted(p for p in D.rglob('*') if p.is_file() and p.name not in ['VALIDATION.json','ARTIFACT_MANIFEST.json'] and '__pycache__' not in p.parts)
manifest=[dict(path=p.relative_to(R).as_posix(),bytes=p.stat().st_size,sha256=sha(p)) for p in files]
save(D/'ARTIFACT_MANIFEST.json',manifest)
if not (D/'VALIDATION.json').exists():save(D/'VALIDATION.json',dict(status='RUNNING_INTEGRITY_CHECK'))
for p in D.glob('*.md'):
    if p.name=='EVIDENCE_INDEX.before.md':continue
    text=p.read_text(encoding='utf-8')
    check('UTF8:'+p.name,'\ufffd' not in text)
    for link in re.findall(r'\]\(([^)]+)\)',text):
        target=link.strip('<>').split('#')[0]
        if not target or urlsplit(target).scheme:continue
        check('link:'+p.name+':'+target,(p.parent/unquote(target)).exists())
for x in manifest:check('manifest:'+x['path'],sha(R/x['path'])==x['sha256'])
result=dict(checked_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),status='PASS' if all(x['passed'] for x in checks) else 'FAIL',
 checks=len(checks),passed=sum(x['passed'] for x in checks),failed=[x for x in checks if not x['passed']],historical_numbered_unchanged=153,
 artifacts=47,versions=30,next_phase_MIT_source_candidates=3,new_static_analysis=0,new_SDK_downloads=0,
 graph_before={k:len(old[k]) for k in ['nodes','edges','sources']},graph_after={k:len(new[k]) for k in ['nodes','edges','sources']},
 meaning='Document/hash/source consistency checks;not legal advice,SDK execution,identity matching or production consumption proof',details=checks)
save(D/'VALIDATION.json',result)
print(json.dumps({k:v for k,v in result.items() if k!='details'},ensure_ascii=False))
raise SystemExit(0 if result['status']=='PASS' else 1)
