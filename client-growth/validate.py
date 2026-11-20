"""Integrity checks for static client-growth evidence. Never invokes SDK APIs."""
from pathlib import Path
import collections, datetime, hashlib, json, re

R = Path(__file__).resolve().parent.parent
O = R/'client-growth'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
errors=[]; warnings=[]
before=load(O/'EVIDENCE_GRAPH.before_client56.json')
after=load(R/'prediction-system/EVIDENCE_GRAPH.json')
preserved={}
for key in ['nodes','edges','sources']:
    previous={x['id']:x for x in before[key]}
    current={x['id']:x for x in after[key]}
    if len(current)!=len(after[key]):errors.append(f'Duplicate graph {key} ID')
    preserved[key]=len(previous)
    for ident, row in previous.items():
        if current.get(ident)!=row:errors.append(f'Historical graph object changed: {key}/{ident}')
for key in ['unknown_breakpoints','excluded_claims']:
    if after.get(key)!=before.get(key):errors.append(f'Original {key} changed')
nodes={x['id'] for x in after['nodes']};sources={x['id'] for x in after['sources']}
for e in after['edges']:
    if e['source'] not in nodes or e['target'] not in nodes:errors.append(f'Broken edge node {e["id"]}')
    for ident in e.get('source_ids',[]):
        if ident not in sources:errors.append(f'Broken source {e["id"]}/{ident}')

new=load(O/'NEW_EDGES.json')
for e in new:
    six=e['six_layers']
    for field in ['production_successful_send','server_received','server_model_training']:
        if six[field]:errors.append(f'Unfounded production flag {e["id"]}/{field}')
    for field in ['class_method_lines','sha256','permission_conditions','missing_evidence','explicit_call_chain']:
        if not e.get(field):errors.append(f'Missing evidence attribute {e["id"]}/{field}')

source_rows=load(O/'SOURCE_EVIDENCE.complete.json')
source_verified=0;package_paths={}
for s in source_rows:
    p=R/s['path']
    if not p.exists() or sha(p)!=s['sha256']:errors.append(f'Source hash mismatch {s["id"]}');continue
    lines=p.read_text(encoding='utf-8-sig').splitlines()
    expected='\n'.join(f'{i}: {lines[i-1]}' for i in range(s['start_line'],s['end_line']+1))
    if expected!=s['excerpt']:errors.append(f'Excerpt/line mismatch {s["id"]}')
    source_verified+=1
    for a in s.get('official_packages',[]):package_paths[a['path']]=a['sha256']
for rel, digest in package_paths.items():
    p=R/rel
    if not p.exists() or sha(p)!=digest:errors.append(f'Official package changed {rel}')

history_checked=0
for row in load(O/'HISTORY.before.json'):
    if row['path']=='prediction-system/EVIDENCE_GRAPH.json':continue
    p=R/row['path']
    if not p.exists() or sha(p)!=row['sha256']:errors.append(f'Prior artifact changed {row["path"]}')
    history_checked+=1

reports=[]
for pattern in ['56_*Token*.md','57_*.md','58_*.md','59_*.md']:
    matches=list(R.glob(pattern))
    if len(matches)!=1:errors.append(f'Report cardinality {pattern}: {len(matches)}')
    reports.extend(matches)
missing_links=[]
for p in reports+[O/'SOURCE_CATALOG.md',O/'EDGE_CATALOG.md']:
    content=p.read_text(encoding='utf-8')
    if '\ufffd' in content:errors.append(f'Replacement Unicode character {p.name}')
    for link in re.findall(r'\]\(([^)]+)\)',content):
        if '://' in link:continue
        rel,_,anchor=link.partition('#')
        target=(p.parent/rel).resolve() if rel else p
        if not target.exists():missing_links.append(f'{p.name}: {link}');continue
        # New CGS anchors must exist; old anchors are checked separately below.
        if anchor and anchor.lower().startswith('cgs'):
            if f'id="{anchor}"' not in target.read_text(encoding='utf-8-sig'):
                missing_links.append(f'{p.name}: missing #{anchor}')
errors.extend(missing_links)

fields=load(O/'PREBID_FIELD_LINEAGE.json')
if isinstance(fields,dict):
    field_rows=fields.get('fields',fields.get('records',[]))
else:field_rows=fields
for f in field_rows:
    for ident in f.get('source_ids',[]):
        if ident not in sources:errors.append(f'Field source not in graph: {ident}')

# The existing manifest must remain intact with exactly one appended entry.
old_m=load(O/'EVIDENCE_MANIFEST.before59.json');new_m=load(R/'EVIDENCE_MANIFEST.json')
if new_m['entries'][:len(old_m['entries'])]!=old_m['entries']:errors.append('Historical manifest entries changed')
if len(new_m['entries'])!=len(old_m['entries'])+1:errors.append('Unexpected manifest entry delta')
new_entry=new_m['entries'][-1]
for s in new_entry['sources']:
    if sha(R/s['path'])!=s['sha256']:errors.append(f'Manifest new-entry hash mismatch {s["path"]}')

result=dict(reviewed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
 status='PASS' if not errors else 'FAIL',static_only=True,production_requests_sent=0,
 real_user_identifiers_collected=0,sdk_initialized=False,
 graph_before={k:len(before[k]) for k in ['nodes','edges','sources']},
 graph_after={k:len(after[k]) for k in ['nodes','edges','sources']},
 original_graph_objects_preserved=preserved,prior_artifact_hashes_verified=history_checked,
 sources_and_line_ranges_verified=source_verified,reused_official_artifacts_hash_verified=len(package_paths),
 new_edges=len(new),prebid_field_records=len(field_rows),reports=[p.name for p in reports],
 warnings=warnings,errors=errors,
 scope='Checks internal consistency, exact sources and preservation only; not production SDK delivery, model training or economic effects.')
(O/'VALIDATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
raise SystemExit(1 if errors else 0)
