"""Verify bounded claims and preservation, not production model performance."""
from pathlib import Path
import csv,datetime,hashlib,importlib.util,json,re,zipfile
R=Path(__file__).resolve().parents[2];O=Path(__file__).resolve().parent
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
errors=[]
old=load(O/'EVIDENCE_GRAPH.before.json');new=load(R/'prediction-system/EVIDENCE_GRAPH.json')
for key in ['nodes','edges','sources']:
    current={x['id']:x for x in new[key]}
    if len(current)!=len(new[key]):errors.append('Duplicate '+key)
    for x in old[key]:
        if current.get(x['id'])!=x:errors.append('Historical graph object changed: '+key+'/'+x['id'])
for key in ['unknown_breakpoints','excluded_claims']:
    if new[key]!=old[key]:errors.append('Historical boundary changed: '+key)
nodes={x['id'] for x in new['nodes']};sourceids={x['id'] for x in new['sources']}
for e in new['edges']:
    if e['source'] not in nodes or e['target'] not in nodes:errors.append('Broken edge '+e['id'])
    if not set(e.get('source_ids',[]))<=sourceids:errors.append('Broken source reference '+e['id'])
edges=load(O/'NEW_EDGES.json')
for e in edges:
    six=e['six_layers']
    if any(six[k] for k in ['actual_game_business_callsite','production_successful_send','server_received','server_model_training']):
        errors.append('Unsupported evidence promotion '+e['id'])
    if e['production_actual_proven']:errors.append('Unsupported production observation '+e['id'])
    if e['status']=='unknown' and e['diagram_style']!='dashed':errors.append('Unknown not dashed '+e['id'])

ss=load(O/'SOURCE_EVIDENCE.json');raws=set();artifacts=set()
for s in ss:
    p=R/s['path'];ls=p.read_text(encoding='utf-8-sig').splitlines()
    if sha(p)!=s['sha256']:errors.append('Source hash '+s['id'])
    excerpt='\n'.join(f'{i}: {ls[i-1]}' for i in range(s['start_line'],s['end_line']+1))
    if excerpt!=s['excerpt']:errors.append('Excerpt/line mismatch '+s['id'])
    if s['short_quote'] not in '\n'.join(ls[s['start_line']-1:s['end_line']]):errors.append('Quote mismatch '+s['id'])
    if 'fetch_provenance' in s:
        m=s['fetch_provenance'];raws.add(m['raw_path'])
        if sha(R/m['raw_path'])!=m['raw_sha256'] or m.get('status')!=200:errors.append('Raw source '+s['id'])
        if 'Page not found' in '\n'.join(ls[:35]):errors.append('Soft404 cited '+s['id'])
    for a in s.get('official_packages',[]):
        p=R/a['path'];artifacts.add(a['path'])
        if sha(p)!=a['sha256']:errors.append('Official artifact hash '+a['path'])
        if p.name.endswith('sources.jar'):
            with zipfile.ZipFile(p) as z:
                if z.read(s['source_archive_member'])!=(R/s['path']).read_bytes():errors.append('Source archive member mismatch')

oldbytes=(O/'CLAIM_MATRIX.before.csv').read_bytes();matrix=R/'model-architecture/CLAIM_MATRIX.csv'
if not matrix.read_bytes().startswith(oldbytes):errors.append('Historical matrix bytes changed')
with (O/'CLAIM_MATRIX.before.csv').open(encoding='utf-8-sig',newline='') as f:oldrows=list(csv.DictReader(f))
with matrix.open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
if rows[:len(oldrows)]!=oldrows:errors.append('Historical matrix rows changed')
if len(rows)!=len(oldrows)+len(ss):errors.append('Matrix row count')
for s,row in zip(ss,rows[len(oldrows):]):
    if row['id']!=s['id'] or row['sha256']!=s['sha256'] or row['short_quote']!=s['short_quote']:errors.append('Matrix appended row mismatch '+s['id'])

checked=0
for x in load(O/'HISTORY.before.json'):
    # The sole intentionally updated historical research file is the append-only matrix.
    if x['path']=='model-architecture/CLAIM_MATRIX.csv':continue
    p=R/x['path']
    if not p.exists() or sha(p)!=x['sha256']:errors.append('Historical file changed '+x['path'])
    checked+=1
if not (R/'EVIDENCE_INDEX.md').read_bytes().startswith((O/'EVIDENCE_INDEX.before.md').read_bytes()):errors.append('Historical index prefix changed')
oldm=load(O/'EVIDENCE_MANIFEST.before.json');m=load(R/'EVIDENCE_MANIFEST.json')
if m['entries'][:-1]!=oldm['entries']:errors.append('Historical manifest entries changed')
for x in m['entries'][-1]['sources']:
    if sha(R/x['path'])!=x['sha256']:errors.append('Current manifest hash mismatch '+x['path'])

files=[R/'61_收入标签与价值分布预测.md',R/'63_预测价值到实时竞价与预算约束.md']+[p for p in O.glob('*.md') if '.before.' not in p.name]
link_count=0
for p in files:
    body=p.read_text(encoding='utf-8-sig')
    if '\ufffd' in body:errors.append('Replacement Unicode '+p.name)
    for target in re.findall(r'\]\(([^)]+)\)',body):
        if '://' in target:continue
        link_count+=1;rel,_,anchor=target.partition('#');q=(p.parent/rel).resolve() if rel else p
        if not q.exists():errors.append('Missing local link '+p.name+':'+target)
        elif anchor.startswith(('ma60','rv61')) and f'id="{anchor}"' not in q.read_text(encoding='utf-8-sig'):
            errors.append('Missing evidence anchor '+p.name+':'+target)

spec=importlib.util.spec_from_file_location('independent_math',O/'math_examples.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
if module.run()!=load(O/'MATH_EXAMPLES.json'):errors.append('Math output stale/mismatch')
for prefix in ['62_','64_']:
    if list(R.glob(prefix+'*.md')):errors.append('Unexpected later report '+prefix)

result=dict(status='PASS' if not errors else 'FAIL',reviewed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
  scope='61/63 static evidence, contract boundaries and independent arithmetic; no model/ROAS production validation',
  exact_source_records=len(ss),new_public_raws_cited=len(raws),reused_official_artifacts_verified=len(artifacts),
  historical_files_hash_verified=checked,historical_matrix_rows_preserved=len(oldrows),matrix_total_rows=len(rows),
  graph_before={k:len(old[k]) for k in ['nodes','edges','sources']},graph_after={k:len(new[k]) for k in ['nodes','edges','sources']},
  new_edges=len(edges),local_links_checked=link_count,math_arithmetic='PASS',
  production_ad_or_event_requests=0,real_identifiers_collected=0,sdk_executed=False,
  recovered_production_model_architecture=False,new_target_game_delivery_or_training_proof=False,errors=errors)
(O/'VALIDATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2));raise SystemExit(bool(errors))
