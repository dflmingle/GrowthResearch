"""Evidence-integrity checks only; never a runtime/delivery/model test."""
from pathlib import Path
import json, hashlib, tarfile, re, datetime

R=Path(__file__).resolve().parent.parent
O=R/'core-insights'
def load(p):return json.loads(p.read_text('utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
checks=[]
def check(name,condition,detail=None):
    checks.append(dict(check=name,passed=bool(condition),detail=detail))
    if not condition:print('FAIL',name,detail)

packages=load(O/'PACKAGE_PROVENANCE.json')
archives={}
for k,p in packages.items():
    path=R/p['path']
    check(k+' original package SHA256',sha(path)==p['sha256'])
    archives[k]=tarfile.open(path,'r:gz')
sources=load(O/'CODE_EVIDENCE.json')
for s in sources:
    p=R/s['path'];check(s['id']+' file hash',sha(p)==s['sha256'])
    lines=p.read_text('utf-8-sig').splitlines()
    actual='\n'.join(f'{i}: {lines[i-1]}' for i in range(s['start_line'],s['end_line']+1))
    check(s['id']+' exact source excerpt',actual==s['excerpt'])
    if s['sdk'] in packages:
        member='package/'+s['path'].split('/extracted/package/',1)[1]
        check(s['id']+' matches official archive member',archives[s['sdk']].extractfile(member).read()==p.read_bytes())
    if 'public_source' in s:
        check(s['id']+' public source HTTP success',s['public_source']['status']==200)

check('IAP package contains no canonical .proto',not any(m.name.endswith('.proto') for m in archives['IAP'].getmembers()))
schema=load(O/'PROTOCOL_SCHEMA.json');m=schema['writer_methods']
check('Schema 20 non-oneof top fields',set(x['number'] for x in m['SerializeIaps']['fields'])==set(list(range(1,17))+[21,24,100,101]))
check('Schema six event oneof variants',set(x['number'] for x in m['WriteEventVariant']['fields'])=={17,18,19,20,22,23})
check('Schema all nine identity fields',set(x['number'] for x in m['WritePlayerIdentity']['fields'])==set(range(1,10)))
check('Schema all ten SKU fields',set(x['number'] for x in m['WriteSku']['fields'])==set(range(1,11)))
check('Schema complete inspected writer field count',sum(len(x['fields']) for x in m.values())==68)

before=load(O/'EVIDENCE_GRAPH.before53.json');graph=load(R/'prediction-system/EVIDENCE_GRAPH.json')
for key in ['nodes','edges','sources']:
    current={x['id']:x for x in graph[key]}
    check(key+' unique IDs',len(current)==len(graph[key]))
    check('All original '+key+' unchanged',all(current.get(x['id'])==x for x in before[key]))
ids={x['id'] for x in graph['nodes']};sids={x['id'] for x in graph['sources']}
check('Graph all node references valid',all(e['source'] in ids and e['target'] in ids for e in graph['edges']))
check('Graph all source references valid',all(set(e.get('source_ids',[])).issubset(sids) for e in graph['edges']))
new_edges=[e for e in graph['edges'] if e['id'].startswith('C53E')]
check('13 appended edges',len(new_edges)==13)
check('No production/training upgrade',all(not any(e['six_layers'][k] for k in ['actual_game_business_callsite','production_successful_send','server_received','server_model_training']) for e in new_edges))
check('Native network construction remains unproven',next(e for e in new_edges if e['id']=='C53E12')['six_layers']['request_construction_code']==False)
check('Original XU07 training edge remains unchanged',next(e for e in graph['edges'] if e['id']=='XU07')==next(e for e in before['edges'] if e['id']=='XU07'))
check('Graph snapshot current',sha(R/'prediction-system/EVIDENCE_GRAPH.json')==sha(O/'EVIDENCE_GRAPH.after55.json'))

lineage=load(O/'FIELD_LINEAGE.json')
check('28 field lineage rows',len(lineage)==28)
check('Lineage sources valid',all(set(x['source_ids']).issubset(sids) for x in lineage))
check('Lineage evidence includes file/package hashes',all(x['evidence_records'] and all(y['sha256'] and y['path'] for y in x['evidence_records']) for x in lineage))
for x in lineage:
    for s in x['evidence_records']:
        check(x['field']+' referenced file '+s['id'],sha(R/s['path'])==s['sha256'])
        if s['official_package']:
            p=s['official_package'];check(x['field']+' referenced package '+s['id'],sha(R/p['path'])==p['sha256'])

reports=[next(R.glob(str(n)+'_*.md')) for n in [53,54,55]]
for p in reports+[O/'CODE_CATALOG.md']:
    txt=p.read_text('utf-8')
    check(p.name+' no encoding replacement', '\ufffd' not in txt)
    for m in re.finditer(r'\]\(([^)#]+)(?:#([^)]*))?\)',txt):
        link,anchor=m.groups()
        if link.startswith(('http://','https://')):continue
        dest=(p.parent/link).resolve()
        # Validation is intentionally generated at end of this script.
        check(p.name+' local link '+link,dest.exists() or dest==O/'VALIDATION.json')
        if anchor and dest.exists():check(p.name+' anchor '+anchor, f'id="{anchor}"' in dest.read_text('utf-8'))

# Preserve prior manifest entries; freeze this phase's artifact references.
manifest_path=R/'EVIDENCE_MANIFEST.json';manifest=load(manifest_path)
artifact_paths=reports+[O/n for n in ['CODE_CATALOG.md','CODE_EVIDENCE.json','PACKAGE_PROVENANCE.json','PROTOCOL_SCHEMA.json','FIELD_LINEAGE.json','ACQUISITION.json','RUNTIME_PUBLIC_PROVENANCE.json','BOUNDARY_ACQUISITION.json','EVIDENCE_GRAPH.before53.json','EVIDENCE_GRAPH.after55.json']]
entry=dict(id='CI53',title='53—55 Unity Core身份提供者与Insights数据血缘',
    claim='Official SDK conditional static paths only; no production delivery or field-level Vector training proof',
    utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    sources=[dict(path=p.relative_to(R).as_posix(),sha256=sha(p),bytes=p.stat().st_size) for p in artifact_paths])
existing=next((i for i,x in enumerate(manifest['entries']) if x['id']=='CI53'),None)
if existing is None:manifest['entries'].append(entry)
else:manifest['entries'][existing]=entry
manifest['core_insights_audit_utc']=entry['utc']
manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n','utf-8')
result=dict(utc=entry['utc'],scope='Static source/archive/link/graph integrity only; no SDK run, no device, no production requests',
    passed=all(c['passed'] for c in checks),check_count=len(checks),checks=checks,
    counts=dict(source_fragments=len(sources),lineage_rows=len(lineage),graph_nodes=len(graph['nodes']),graph_edges=len(graph['edges']),graph_sources=len(graph['sources'])))
(O/'VALIDATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf-8')
print(json.dumps({k:v for k,v in result.items() if k!='checks'},ensure_ascii=False))
for t in archives.values():t.close()
raise SystemExit(0 if result['passed'] else 1)
