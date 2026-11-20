"""Read-only evidence checks (writes only round77 manifest/validation). No network."""
from pathlib import Path
from urllib.parse import urlsplit, unquote
import csv, datetime, hashlib, json, re

R=Path(__file__).resolve().parent.parent
D=R/'production77'
def load(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x): p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
checks=[]
def check(name,ok,detail=None):
    checks.append(dict(check=name,passed=bool(ok),detail=detail))

h=load(D/'HISTORY_BEFORE.json')
numbered={k:v for k,v in h.items() if k[:2].isdigit()}
check('historical_numbered_count',len(numbered)==143,len(numbered))
for name,digest in numbered.items():
    check('history:'+name,(R/name).is_file() and sha(R/name)==digest)
for item in load(R/'engineering76/ARTIFACT_MANIFEST.json'):
    # Shared index/graph are explicitly required to grow. Check round76 versions
    # against the frozen pre77 copies, then separately verify append-only growth.
    shared={'EVIDENCE_INDEX.md':D/'EVIDENCE_INDEX.before.md',
            'prediction-system/EVIDENCE_GRAPH.json':D/'EVIDENCE_GRAPH.before.json'}
    target=shared.get(item['path'],R/item['path'])
    check(('round76_frozen_shared:' if item['path'] in shared else 'round76:')+item['path'],target.is_file() and sha(target)==item['sha256'])
before=load(D/'EVIDENCE_GRAPH.before.json')
after=load(R/'prediction-system/EVIDENCE_GRAPH.json')
for key,value in before.items():
    if key in ('nodes','edges','sources'):
        check('append_only:'+key,after[key][:len(value)]==value)
    else: check('old_metadata:'+key,after.get(key)==value)
new_sources=after['sources'][len(before['sources']):]
new_edges=after['edges'][len(before['edges']):]
check('graph_new_counts',(len(after['nodes'])-len(before['nodes']),len(new_edges),len(new_sources))==(5,4,4))
check('index_byte_prefix',(R/'EVIDENCE_INDEX.md').read_bytes().startswith((D/'EVIDENCE_INDEX.before.md').read_bytes()))
check('baseline_graph_hash',sha(D/'EVIDENCE_GRAPH.before.json')==h['prediction-system/EVIDENCE_GRAPH.json'])
check('baseline_index_hash',sha(D/'EVIDENCE_INDEX.before.md')==h['EVIDENCE_INDEX.md'])
for key in ('nodes','edges','sources'):
    ids=[x['id'] for x in after[key]]
    # Historical duplicate IDs, if any, are outside this round's modification scope.
    new=ids[len(before[key]):]
    check('new_unique_ids:'+key,len(new)==len(set(new)) and not(set(new)&set(ids[:len(before[key])])))
source_map={s['id']:s for s in after['sources']}
node_ids={n['id'] for n in after['nodes']}
for edge in new_edges:
    check('edge_nodes:'+edge['id'],edge['source'] in node_ids and edge['target'] in node_ids)
    check('edge_sources:'+edge['id'],all(sid in source_map for sid in edge['source_ids']))
    check('no_production_upgrade:'+edge['id'],all(edge.get(f) is False for f in [
        'production_actual_proven','production_match_proven','prediction_model_consumption_proven','independent_real_identity_lift_proven']))

snapshots=load(D/'SOURCE_EVIDENCE.json')
check('snapshots_new_reused',(len(snapshots),sum(x['new_url'] for x in snapshots))==(6,4))
check('duplicate_ids_explicit',next(s for s in snapshots if s['id']=='PE77S03')['prior_equivalent_source_ids']==['S30','MA60S19']
    and next(s for s in snapshots if s['id']=='PE77S05')['prior_equivalent_source_ids']==['S28','MA60S20'])
for s in snapshots:
    check('source_raw:'+s['id'],sha(R/s['path'])==s['sha256'])
    check('source_text:'+s['id'],sha(R/s['text_path'])==s['text_sha256'])
    check('source_quote:'+s['id'],s['exact_quote'] in (R/s['text_path']).read_text(encoding='utf-8'))
    check('source_dates:'+s['id'],bool(s['source_dates']) and bool(s['acquired_utc']))
for f in load(D/'FETCH_MANIFEST.json'):
    check('fetch_raw:'+f['id'],bool(f.get('path')) and sha(R/f['path'])==f['sha256'])
    check('fetch_text:'+f['id'],bool(f.get('text_path')) and sha(R/f['text_path'])==f['text_sha256'])
check('fetch_count',len(load(D/'FETCH_MANIFEST.json'))==21)

rows=list(csv.DictReader(next(R.glob('77_*.csv')).open(encoding='utf-8-sig',newline='')))
check('matrix_count',len(rows)==12)
check('matrix_reuse_count',sum(r['duplicate_status']=='REUSED' for r in rows)==8)
check('matrix_new_count',sum(r['duplicate_status']=='NEW_URL_BUT_NO_C_GRAPH_UPGRADE' for r in rows)==4)
for row in rows:
    cid=row['claim_id'];s=source_map[row['source_id']]
    check('matrix_source:'+cid,row['raw_file']==s['path'] and row['raw_sha256']==s['sha256'] and sha(R/s['path'])==s['sha256'])
    text=(R/row['excerpt_file']).read_text(encoding='utf-8-sig')
    check('matrix_quote:'+cid,row['exact_quote'] in text)
    check('matrix_text_hash:'+cid,sha(R/row['excerpt_file'])==row['excerpt_sha256'])
    check('matrix_locator:'+cid,text[:text.index(row['exact_quote'])].count('\n')+1==int(row['excerpt_start_line']))
    check('matrix_no_upgrade:'+cid,all(row[f]=='False' for f in ['c_graph_upgrade','bridge_complete','production_match_proven','prediction_model_consumption_proven','independent_identity_lift_proven']))
    check('matrix_unknown:'+cid,row['specific_Axon_Vector_production_consumption']=='UNKNOWN')

alias_ids=['S28','S30','MA60S19','MA60S20']
aliases=[]
for sid in alias_ids:
    s=source_map[sid]
    check('reused_alias_hash:'+sid,sha(R/s['path'])==s['sha256'])
    aliases.append(s)
save(D/'ALIAS_REVIEW.json',dict(reason='Two public Workday HTML URLs duplicated already archived CXS job entities;no new evidence credit',legacy_sources=aliases,
    duplicate_snapshots=[s for s in snapshots if not s['new_url']]))

reports=sorted(R.glob('77_*'))
check('five_deliverables',len(reports)==5 and sum(p.suffix=='.md' for p in reports)==4)
check('no_corrupt_filenames',all('?' not in p.name for p in reports))
coverage=load(D/'SEARCH_COVERAGE.json')
check('no_forbidden_actions',all(v==0 for v in coverage['forbidden_actions'].values()))
check('zero_upgrades',coverage['new_c_graph_upgrades']==0 and after['production_identity_engineering_round77']['c_graph_upgrades']==0)

# Exclude this output and the self-referential manifest; include all inputs/code/raw snapshots.
paths=reports+[R/'EVIDENCE_INDEX.md',R/'prediction-system/EVIDENCE_GRAPH.json']
paths+=sorted(p for p in D.rglob('*') if p.is_file() and p.name not in ('ARTIFACT_MANIFEST.json','VALIDATION.json') and '__pycache__' not in p.parts)
manifest=[dict(path=p.relative_to(R).as_posix(),bytes=p.stat().st_size,sha256=sha(p)) for p in paths]
save(D/'ARTIFACT_MANIFEST.json',manifest)
# Reserve output path for self-referential documentation link existence checks.
if not (D/'VALIDATION.json').exists(): save(D/'VALIDATION.json',dict(status='RUNNING'))
for p in reports+[D/'SOURCE_CATALOG.md',D/'README.md']:
    if p.suffix!='.md':continue
    for link in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
        target=link.strip('<>').split('#')[0]
        if not target or urlsplit(target).scheme:continue
        check('markdown_link:'+p.name+':'+target,(p.parent/unquote(target)).exists())
for x in manifest:
    check('manifest:'+x['path'],sha(R/x['path'])==x['sha256'])
result=dict(reviewed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
 status='PASS' if all(x['passed'] for x in checks) else 'FAIL',checks=len(checks),passed=sum(x['passed'] for x in checks),
 failed=[x for x in checks if not x['passed']],historical_numbered_unchanged=len(numbered),
 round76_artifacts_checked=len(load(R/'engineering76/ARTIFACT_MANIFEST.json')),
 graph_before={k:len(before[k]) for k in ['nodes','edges','sources']},
 graph_after={k:len(after[k]) for k in ['nodes','edges','sources']},
 claims=12,new_primary_sources=4,duplicate_primary_snapshots=2,c_graph_upgrades=0,
 meaning='Integrity/provenance and append-only checks;NOT production matching or model-performance tests',details=checks)
save(D/'VALIDATION.json',result)
print(json.dumps({k:v for k,v in result.items() if k!='details'},ensure_ascii=False))
raise SystemExit(0 if result['status']=='PASS' else 1)
