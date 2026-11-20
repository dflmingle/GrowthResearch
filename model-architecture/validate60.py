"""Validate citations, source hashes, historical preservation and evidence scope."""
from pathlib import Path
import csv,datetime,hashlib,json,re
R=Path(__file__).resolve().parent.parent;O=R/'model-architecture'
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
errors=[];before=load(O/'EVIDENCE_GRAPH.before60.json');after=load(R/'prediction-system/EVIDENCE_GRAPH.json')
for key in ['nodes','edges','sources']:
    new={x['id']:x for x in after[key]}
    if len(new)!=len(after[key]):errors.append('Duplicate graph ID '+key)
    for x in before[key]:
        if new.get(x['id'])!=x:errors.append('Old object changed '+key+'/'+x['id'])
for key in ['unknown_breakpoints','excluded_claims']:
    if before.get(key)!=after.get(key):errors.append('Old unknown/excluded changed '+key)
nodes={x['id'] for x in after['nodes']};sourceids={x['id'] for x in after['sources']}
for e in after['edges']:
    if e['source'] not in nodes or e['target'] not in nodes:errors.append('Broken graph edge '+e['id'])
    if not set(e.get('source_ids',[]))<=sourceids:errors.append('Broken source reference '+e['id'])
for e in load(O/'NEW_EDGES.json'):
    if any(e['six_layers'].values()):errors.append('Unsupported layer promotion '+e['id'])
    if e['production_actual_proven']:errors.append('Unsupported production observation '+e['id'])
    if e['modality']=='forward-looking' and e['diagram_style']!='dashed':errors.append('Future claim drawn solid '+e['id'])

sources=load(O/'SOURCE_EVIDENCE.json');raws=set()
for s in sources:
    p=R/s['path'];ls=p.read_text(encoding='utf-8-sig').splitlines()
    if sha(p)!=s['sha256']:errors.append('Source changed '+s['id'])
    excerpt='\n'.join(f'{i}: {ls[i-1]}' for i in range(s['start_line'],s['end_line']+1))
    if excerpt!=s['excerpt']:errors.append('Wrong excerpt/line '+s['id'])
    if s['short_quote'] not in '\n'.join(ls[s['start_line']-1:s['end_line']]):errors.append('Quote mismatch '+s['id'])
    if 'fetch_provenance' in s:
        m=s['fetch_provenance'];raw=R/m['raw_path'];raws.add(m['raw_path'])
        if sha(raw)!=m['sha256']:errors.append('Raw HTTP changed '+s['id'])
        if m.get('status')!=200:errors.append('Cited failed fetch '+s['id'])
    if s['evidence_kind']=='job' and s['evidence_level']!='【间接技术线索】':errors.append('Job promoted '+s['id'])

matrix=list(csv.DictReader((O/'CLAIM_MATRIX.csv').open(encoding='utf-8-sig',newline='')))
if len(matrix)!=len(sources) or {x['id'] for x in matrix}!={x['id'] for x in sources}:errors.append('Matrix mismatch')
for s,c in zip(sources,matrix):
    if s['sha256']!=c['sha256'] or s['short_quote']!=c['short_quote']:errors.append('CSV content mismatch '+s['id'])

history=load(O/'HISTORY.before60.json');checked=0
for x in history:
    if x['path'] in ['prediction-system/EVIDENCE_GRAPH.json','EVIDENCE_INDEX.md','EVIDENCE_MANIFEST.json']:continue
    p=R/x['path']
    if not p.exists() or sha(p)!=x['sha256']:errors.append('Prior artifact changed '+x['path'])
    checked+=1
oldidx=(O/'EVIDENCE_INDEX.before60.md').read_bytes();idx=(R/'EVIDENCE_INDEX.md').read_bytes()
if not idx.startswith(oldidx):errors.append('Prior evidence index prefix changed')
oldmanifest=load(O/'EVIDENCE_MANIFEST.before60.json');m=load(R/'EVIDENCE_MANIFEST.json')
if m['entries'][:len(oldmanifest['entries'])]!=oldmanifest['entries']:errors.append('Prior manifest changed')
for x in m['entries'][-1]['sources']:
    if sha(R/x['path'])!=x['sha256']:errors.append('Manifest current hash mismatch '+x['path'])

files=[R/'60_Axon_Vector模型架构公开证据.md']+[p for p in O.glob('*.md') if '.before60.' not in p.name]
for p in files:
    text=p.read_text(encoding='utf-8-sig')
    if '\ufffd' in text:errors.append('Invalid Unicode '+p.name)
    for target in re.findall(r'\]\(([^)]+)\)',text):
        if '://' in target:continue
        rel,_,anchor=target.partition('#');q=(p.parent/rel).resolve() if rel else p
        if not q.exists():errors.append('Missing link '+p.name+':'+target)
        elif anchor and anchor.startswith('ma60') and f'id="{anchor}"' not in q.read_text(encoding='utf-8-sig'):
            errors.append('Missing anchor '+p.name+':'+target)

for n in ['61','62','63','64']:
    if list(R.glob(n+'_*.md')):errors.append('Unexpected final later report '+n)

result=dict(status='PASS' if not errors else 'FAIL',reviewed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
  round='60 first round only',sources_verified=len(sources),csv_claims=len(matrix),new_public_raws_cited=len(raws),
  previous_artifacts_hash_verified=checked,graph_before={k:len(before[k]) for k in ['nodes','edges','sources']},
  graph_after={k:len(after[k]) for k in ['nodes','edges','sources']},new_edges=14,
  historical_objects_unchanged=True if not errors else 'see errors',production_ad_requests=0,
  sdk_executed=False,real_identifiers_collected=0,errors=errors,
  limitation='Internal integrity and evidence scope checks only. Not a production model, delivery or causal ROAS validation.')
(O/'VALIDATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2));raise SystemExit(bool(errors))
