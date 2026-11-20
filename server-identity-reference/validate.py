"""Document/provenance checks only. Never runs a matching or feature service."""
from pathlib import Path
from urllib.parse import unquote,urlsplit
import csv,hashlib,json,re
from datetime import datetime,timezone
R=Path(__file__).resolve().parent.parent;D=Path(__file__).resolve().parent
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rows(p):return list(csv.DictReader(p.open(encoding='utf-8-sig',newline='')))
checks=[]
def check(name,ok):checks.append(dict(check=name,passed=bool(ok)))
history=load(D/'HISTORY_BEFORE.json')
check('153 numbered history files',sum(p[:2].isdigit() for p in history)==153)
for p,h in history.items():check('history:'+p,(R/p).is_file() and sha(R/p)==h)
basehash=load(D/'BASELINE_HASHES.json')
check('frozen index hash',sha(D/'EVIDENCE_INDEX.before.md')==basehash['EVIDENCE_INDEX.md'])
check('frozen graph hash',sha(D/'EVIDENCE_GRAPH.before.json')==basehash['prediction-system/EVIDENCE_GRAPH.json'])
fetch=load(D/'FETCH_MANIFEST.json');fetchmap={x['id']:x for x in fetch}
check('42 documented public GETs',len(fetch)==42 and len(fetchmap)==42)
allowed_hosts={'api.github.com','raw.githubusercontent.com','openid.net','www.w3.org','arxiv.org'}
for f in fetch:
    check('public metadata/doc URL:'+f['id'],urlsplit(f['url']).hostname in allowed_hosts)
    check('HTTP200:'+f['id'],f['status']==200)
    check('response hash:'+f['id'],sha(R/f['path'])==f['sha256'])
for x in load(D/'DERIVED_TEXTS.json'):
    check('derived raw:'+x['source_id'],sha(R/x['raw_path'])==x['raw_sha256'])
    check('derived text:'+x['source_id'],sha(R/x['path'])==x['sha256'])
components=load(D/'OPEN_SOURCE_COMPONENTS.json');pins=load(D/'COMPONENT_PINS.json')
check('4 pinned components',len(components)==len(pins)==4)
for c in components:
    check('license bytes:'+c['component'],sha(R/c['license_path'])==c['license_sha256'])
    pin=next(x for x in pins if x['component']==c['component'])
    check('commit identity:'+c['component'],pin['commit']==c['commit'] and bool(re.fullmatch('[a-f0-9]{40}',pin['commit'])))
    readme=fetchmap[c['component']+'-readme']
    check('pinned raw URLs:'+c['component'],all('/'+c['commit']+'/' in fetchmap[c['component']+z]['url'] for z in ['-license','-readme','-version']))
    meta=load(R/fetchmap[pin['pin_source']]['path'])[0]
    check('official commit metadata:'+c['component'],meta['sha']==c['commit'] and meta['commit']['committer']['date']==c['commit_date'])
    check('no package runtime claim:'+c['component'],c['review_status']=='REFERENCE_REVIEW_ONLY;NOT_INSTALLED_OR_RUN')
ev=load(D/'SOURCE_EVIDENCE.json');check('19 scoped excerpts',len(ev)==19 and len({e['id'] for e in ev})==19)
for x in ev:
    check('evidence raw:'+x['id'],sha(R/x['source_path'])==x['source_sha256'])
    check('evidence text:'+x['id'],sha(R/x['text_path'])==x['text_sha256'])
    ls=(R/x['text_path']).read_text(encoding='utf-8-sig').splitlines()
    check('quote+lines:'+x['id'],x['excerpt']=='\n'.join(ls[x['start_line']-1:x['end_line']]))
    check('scoped evidence:'+x['id'],all(x[k] for k in ['url','collected_utc','evidence_level','scope','license_scope']))
    check('no model/prod upgrade:'+x['id'],not any(x[k] for k in ['production_actual_proven','production_match_proven','prediction_model_consumption_proven','independent_real_identity_lift_proven']))
for x in load(D/'REUSED_SOURCE_REFERENCES.json'):check('reuse hash:'+x['id'],sha(R/x['path'])==x['sha256'])
for x in load(D/'REUSED_VENDOR_EXCERPTS.json'):
    check('reused vendor raw:'+x['id'],sha(R/x['path'])==x['sha256'])
    check('reused vendor text:'+x['id'],sha(R/x['text_path'])==x['text_sha256'])
test=rows(D/'ACCEPTANCE_TEST_DESIGN.csv')
check('20 tests DESIGN ONLY',len(test)==20 and all(x['execution']=='NOT_RUN_DESIGN_ONLY' for x in test))
check('unique tests',len({x['test_id'] for x in test})==20)
comp=rows(D/'COMPONENT_CONTRACT_MATRIX.csv');check('7 architecture components',len(comp)==7 and all(x['status']=='DESIGN_ONLY' for x in comp))
rules=rows(D/'RELATIONSHIP_RULES.csv');check('14 independent rules',len(rules)==14 and all(x['kind']=='REFERENCE_POLICY_NOT_VENDOR_DEPLOYMENT' for x in rules))
check('8 routes',len(rows(D/'TECHNICAL_ROUTE_MATRIX.csv'))==8)
gaps=rows(D/'AXON_VECTOR_GAP_MATRIX.csv')
check('12 vendor gaps UNKNOWN',len(gaps)==12 and all(x['C_graph_Axon']==x['C_graph_Vector']==x['D']=='UNKNOWN' and x['production_forensics']=='STOP' for x in gaps))
contract=load(D/'REFERENCE_CONTRACTS.json')
check('reference contract not vendor/runtime',contract['status']=='DESIGN_ONLY;not vendor schema;not executed')
check('typed entities',contract['entities']['IdentityKey']['entity_type_enum']==['device','installation','account','person','household'])
check('consumption+availability+deletion contracts',all(k in contract['entities'] for k in ['RelationshipRevision','ResolutionReceipt','EventRevision','FeatureBundle','ConsumerReceipt','DeletionCase']))
for f in load(D/'REPORT_PATHS.json')+['server-identity-reference/README.md','server-identity-reference/SOURCE_CATALOG.md']:
    p=R/f;check('report exists:'+f,p.is_file() and p.stat().st_size>500)
    text=p.read_text(encoding='utf-8-sig');check('scope banner:'+f,'UNKNOWN' in text and 'STOP' in text)
    for raw in re.findall(r'\]\(([^)]+)\)',text):
        target=unquote(raw.split('#')[0])
        if target and not urlsplit(target).scheme:
            dest=(p.parent/target).resolve()
            check('local link:'+f+':'+raw,dest==(D/'VALIDATION.json').resolve() or dest.exists())
old=load(D/'EVIDENCE_GRAPH.before.json');new=load(R/'prediction-system/EVIDENCE_GRAPH.json')
for k,v in old.items():check('old graph preserved:'+k,new[k][:len(v)]==v if k in ['nodes','edges','sources'] else new.get(k)==v)
check('graph append counts 8/8/31',[len(new[k])-len(old[k]) for k in ['nodes','edges','sources']]==[8,8,31])
for k in ['nodes','edges','sources']:check('graph unique IDs:'+k,len({x['id'] for x in new[k]})==len(new[k]))
added=load(D/'ADDED_GRAPH_OBJECTS.json');ids={s['id'] for s in new['sources']};nodes={n['id'] for n in new['nodes']}
for s in added['sources']:check('added graph source hash:'+s['id'],sha(R/s['path'])==s['sha256'])
for e in added['edges']:
    check('edge refs:'+e['id'],e['source'] in nodes and e['target'] in nodes and all(s in ids for s in e['source_ids']))
    check('edge no production claims:'+e['id'],not any(e[k] for k in ['production_actual_proven','production_match_proven','prediction_model_consumption_proven','independent_real_identity_lift_proven']) and not any(e['six_layers'].values()))
check('index prefix preserved',(R/'EVIDENCE_INDEX.md').read_bytes().startswith((D/'EVIDENCE_INDEX.before.md').read_bytes()))
state=load(D/'STATUS.json')
check('Cgraph/D/prod STOP preserved',state['C_graph_Axon']==state['C_graph_Vector']==state['D']=='UNKNOWN' and state['production_forensics']=='STOP')
check('no production/data/model/runtime work',all(state[k]==0 for k in ['SDK_executions','identity_API_calls','production_ad_requests','real_identity_records_acquired','model_training_runs','resolver_or_mock_implementations','new_vendor_production_evidence']))
check('76 untouched',not state['engineering76_modified'])
check('no79 new task',not list(R.glob('79*')))
out=dict(reviewed_utc=datetime.now(timezone.utc).isoformat(),status='PASS' if all(x['passed'] for x in checks) else 'FAIL',
   check_count=len(checks),passed=sum(x['passed'] for x in checks),failed=[x for x in checks if not x['passed']],
   scope='Document, quote, license-snapshot, reference and historical-preservation checks ONLY; no algorithm/service/latency/erasure/value tests executed',checks=checks)
(D/'VALIDATION.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:out[k] for k in ['status','check_count','passed','failed']},ensure_ascii=False))
raise SystemExit(0 if out['status']=='PASS' else 1)
