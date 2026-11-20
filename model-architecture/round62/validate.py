"""Consistency/preservation checks for cold-start evidence, not model validation."""
from pathlib import Path
import csv,datetime,hashlib,json,re
R=Path(__file__).resolve().parents[2];O=Path(__file__).resolve().parent
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
errors=[]
before=load(O/'EVIDENCE_GRAPH.before.json');after=load(R/'prediction-system/EVIDENCE_GRAPH.json')
for key in ['nodes','edges','sources']:
    cur={x['id']:x for x in after[key]}
    if len(cur)!=len(after[key]):errors.append('Duplicate '+key)
    for x in before[key]:
        if cur.get(x['id'])!=x:errors.append('Historical object changed '+key+'/'+x['id'])
for key in ['unknown_breakpoints','excluded_claims']:
    if before[key]!=after[key]:errors.append('Historical boundary changed '+key)
nodes={x['id'] for x in after['nodes']};sourceids={x['id'] for x in after['sources']}
for e in after['edges']:
    if e['source'] not in nodes or e['target'] not in nodes:errors.append('Broken edge '+e['id'])
    if not set(e.get('source_ids',[]))<=sourceids:errors.append('Broken source '+e['id'])
for e in load(O/'NEW_EDGES.json'):
    if any(e['six_layers'].values()) or e['production_actual_proven']:errors.append('Evidence layer promoted '+e['id'])
    if e['status'] in ['unknown','inference'] and e['diagram_style']!='dashed':errors.append('Unknown not dashed '+e['id'])
    if not e.get('mechanism') or not e.get('training_or_bidding_stage'):errors.append('Missing mechanism/stage '+e['id'])
ss=load(O/'SOURCE_EVIDENCE.json');rawpaths=set()
for s in ss:
    p=R/s['path'];lines=p.read_text(encoding='utf-8-sig').splitlines()
    if sha(p)!=s['sha256']:errors.append('Source hash mismatch '+s['id'])
    excerpt='\n'.join(f'{i}: {lines[i-1]}' for i in range(s['start_line'],s['end_line']+1))
    if excerpt!=s['excerpt']:errors.append('Excerpt mismatch '+s['id'])
    if s['short_quote'] not in '\n'.join(lines[s['start_line']-1:s['end_line']]):errors.append('Quote mismatch '+s['id'])
    if 'fetch_provenance' in s:
        m=s['fetch_provenance'];rawpaths.add(m['raw_path'])
        if m.get('status')!=200 or sha(R/m['raw_path'])!=m['raw_sha256']:errors.append('Cited failed/raw mismatch '+s['id'])
trace=load(O/'AUTHOR_TRACE.json')
if sha(R/trace['raw_path'])!=trace['raw_sha256']:errors.append('Author raw hash mismatch')
if trace['author_jsonld'][0]['name']!='Daniel Godley':errors.append('Author mismatch')

matrix=R/'model-architecture/CLAIM_MATRIX.csv';oldbytes=(O/'CLAIM_MATRIX.before.csv').read_bytes()
if not matrix.read_bytes().startswith(oldbytes):errors.append('Old matrix bytes changed')
with (O/'CLAIM_MATRIX.before.csv').open(encoding='utf-8-sig',newline='') as f:oldrows=list(csv.DictReader(f))
with matrix.open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
if rows[:len(oldrows)]!=oldrows or len(rows)!=len(oldrows)+len(ss):errors.append('Matrix rows mismatch')
for s,row in zip(ss,rows[len(oldrows):]):
    if s['id']!=row['id'] or s['sha256']!=row['sha256']:errors.append('Matrix new row mismatch '+s['id'])

checked=0
for x in load(O/'HISTORY.before.json'):
    if x['path']=='model-architecture/CLAIM_MATRIX.csv':continue
    p=R/x['path']
    if not p.exists() or sha(p)!=x['sha256']:errors.append('Prior artifact changed '+x['path'])
    checked+=1
if not (R/'EVIDENCE_INDEX.md').read_bytes().startswith((O/'EVIDENCE_INDEX.before.md').read_bytes()):errors.append('Old index prefix changed')
oldm=load(O/'EVIDENCE_MANIFEST.before.json');m=load(R/'EVIDENCE_MANIFEST.json')
if m['entries'][:-1]!=oldm['entries']:errors.append('Historical manifest entries changed')
for x in m['entries'][-1]['sources']:
    if sha(R/x['path'])!=x['sha256']:errors.append('Current manifest hash mismatch '+x['path'])

comp=load(O/'FOUR_MECHANISMS.json')
if {(x['company'],x['mechanism']) for x in comp}!={(co,m) for co in ['AppLovin','Unity'] for m in ['A','B','C','D']}:errors.append('Comparison coverage')
for x in comp:
    for k in ['necessary_data','train_input','bid_input','personal_crossapp_id_required','permissions','experiment','cold_start_role','counterevidence_and_production_gaps','time_condition']:
        if not x.get(k):errors.append('Incomplete comparison '+k)
    if x['experiment_executed'] or x['production_impl_proven']:errors.append('Comparison capability promoted')
    if not set(x['evidence_refs'].split(';'))<=sourceids:errors.append('Comparison source ref '+x['company']+x['mechanism'])

files=[R/'62_跨游戏知识迁移与冷启动机制.md',O/'SOURCE_CATALOG.md']
links=0
for p in files:
    body=p.read_text(encoding='utf-8-sig')
    if '\ufffd' in body:errors.append('Replacement Unicode '+p.name)
    for target in re.findall(r'\]\(([^)]+)\)',body):
        if '://' in target:continue
        links+=1;rel,_,anchor=target.partition('#');q=(p.parent/rel).resolve() if rel else p
        if not q.exists():errors.append('Missing local link '+p.name+':'+target)
        elif anchor and anchor.startswith('ct62') and f'id="{anchor}"' not in q.read_text(encoding='utf-8-sig'):
            errors.append('Missing source anchor '+target)
body=files[0].read_text('utf-8')
for label in ['A 同App','B 聚合','C 共享','D 合法','训练阶段','竞价阶段']:
    if label not in body:errors.append('Missing required distinction '+label)
if not re.search(r'```mermaid\nflowchart',body):errors.append('Missing evidence-chain diagram')

result=dict(status='PASS' if not errors else 'FAIL',reviewed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
  scope='62 cold-start claims, authorship, stage/identity distinctions and historical preservation; not production model proof',
  exact_source_claims_verified=len(ss),new_public_raws_cited=len(rawpaths),historical_files_hash_verified=checked,
  historical_matrix_rows_preserved=len(oldrows),matrix_total_rows=len(rows),comparison_company_mechanism_rows=len(comp),
  graph_before={k:len(before[k]) for k in ['nodes','edges','sources']},graph_after={k:len(after[k]) for k in ['nodes','edges','sources']},
  local_links_checked=links,production_ad_requests=0,real_identifiers_collected=0,sdk_executed=False,
  new_shared_parameter_or_personal_history_production_proof=False,
  public_architecture_broad_search_recommendation='stop pending a specific new primary technical source',errors=errors)
(O/'VALIDATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2));raise SystemExit(bool(errors))
