from pathlib import Path
import csv, datetime, hashlib, json, re

R = Path(__file__).resolve().parent.parent
D = R / 'closure70'
OUT = D / 'VALIDATION.json'
OUT.write_text('{"status":"RUNNING"}', encoding='utf-8')

def read(p):
    return json.loads(p.read_text(encoding='utf-8-sig'))

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

checks = []
def check(name, passed, detail):
    checks.append(dict(name=name, passed=bool(passed), detail=detail))

old = read(D / 'HISTORY_BEFORE.json')
historical = {p: h for p, h in old.items() if p not in
              ['EVIDENCE_INDEX.md', 'prediction-system/EVIDENCE_GRAPH.json']}
bad = [p for p, h in historical.items() if not (R/p).is_file() or sha(R/p) != h]
check('historical_numbered_files_byte_preserved', not bad,
      dict(count=len(historical), changed=bad))
base = read(D / 'EVIDENCE_GRAPH.before.json')
g = read(R / 'prediction-system/EVIDENCE_GRAPH.json')
for k in ['nodes', 'edges', 'sources', 'unknown_breakpoints', 'excluded_claims']:
    check('historical_prefix_' + k, g[k][:len(base[k])] == base[k],
          dict(before=len(base[k]), after=len(g[k])))
for k in base:
    if k not in ['nodes', 'edges', 'sources', 'unknown_breakpoints', 'excluded_claims']:
        check('historical_metadata_' + k, g[k] == base[k], 'Preserved original section')
check('graph_snapshot_matches', read(D/'EVIDENCE_GRAPH.after.json') == g, 'Current graph')
idx0 = (D/'EVIDENCE_INDEX.before.md').read_text(encoding='utf-8-sig')
check('index_append_only', (R/'EVIDENCE_INDEX.md').read_text(encoding='utf-8-sig').startswith(idx0),
      'Original index text retained')
for k in ['nodes', 'edges', 'sources']:
    ids = [x['id'] for x in g[k]]
    check('unique_' + k, len(ids) == len(set(ids)), len(ids))
nodes = {x['id'] for x in g['nodes']}
sources = {x['id'] for x in g['sources']}
newedges = [x for x in g['edges'] if x['id'].startswith('CL70E')]
check('new_graph_references', all(x['source'] in nodes and x['target'] in nodes
      and set(x['source_ids']) <= sources for x in newedges), len(newedges))
for x in newedges:
    check('no_production_upgrade_' + x['id'], not any(x['six_layers'].get(k) for k in
          ['production_successful_send', 'server_received', 'server_model_training'])
          and not x['production_actual_proven'] and not x['observed_target_game_delivery']
          and not x['server_model_training'], x['status'])

for fname in ['SOURCE_EVIDENCE.json', 'CODE_EVIDENCE.json', 'REUSED_EVIDENCE.json']:
    records = read(D/fname)
    bad = [x['id'] for x in records if not (R/x['path']).is_file()
           or sha(R/x['path']) != x['sha256']]
    check('source_hashes_' + fname, not bad, dict(count=len(records), bad=bad))
    if fname != 'CODE_EVIDENCE.json':
        continue
    for x in records:
        lines = (R/x['path']).read_text(encoding='utf-8').splitlines()
        expected = '\n'.join(f'{i+1}: {s}' for i, s in enumerate(lines)
                             if x['start_line'] <= i+1 <= x['end_line'])
        check('exact_excerpt_' + x['id'], expected == x['excerpt'],
              dict(path=x['path'], lines=[x['start_line'], x['end_line']]))
        packages = x['original_packages']
        check('original_sdk_hash_' + x['id'], bool(packages) and all(
              (R/a['path']).is_file() and sha(R/a['path']) == a['sha256'] for a in packages),
              len(packages))
        st = x['evidence_status']
        check('code_layer_boundary_' + x['id'], not any(st.get(k) for k in
              ['production_successful_send', 'server_received', 'model_training']), st)
        check('source_matches_graph_' + x['id'], all(v == next(s for s in g['sources']
              if s['id'] == x['id']).get(k) for k, v in x.items()), 'Full source record')

bytecode = read(D/'BYTECODE_CHECK.json')
for x in bytecode:
    check('bytecode_' + x['id'], x['exit'] == 0 and sha(R/x['input']) == x['input_sha256']
          and sha(R/x['path']) == x['sha256'], x['class_name'])
anchors = {'max-q': ['Map.put', 'Map.get'], 'max-o3': ['JSONObject'],
           'max-g6': ['_urls', 'POST'], 'adapter417': ['randomUUID', 'setObjectId']}
for x in bytecode:
    txt = (R/x['path']).read_text(encoding='utf-8-sig')
    check('bytecode_anchors_' + x['id'], all(a in txt for a in anchors[x['id']]), anchors[x['id']])
for x in read(D/'DECOMPILE.json'):
    check('decompile_' + x['name'], x['exit'] == 0 and sha(R/x['input']) == x['input_sha256']
          and (R/x['output']).is_dir() and (R/x['log']).is_file(), x['input'])

fetch = read(D/'FETCH_MANIFEST.json')
check('fetch_unique', len({(x['id'], x['url']) for x in fetch}) == len(fetch), len(fetch))
bad = [x['id'] for x in fetch if x.get('path') and
       (not (R/x['path']).is_file() or sha(R/x['path']) != x['sha256'])]
check('fetched_raw_hashes', not bad, bad)
artifacts = g['closed_loop_round70']['reports']
for p in artifacts:
    check('delivery_' + p, (R/p).is_file() and (R/p).stat().st_size > 1000,
          (R/p).stat().st_size if (R/p).exists() else 0)
missing = []
for p in artifacts + ['closure70/SOURCE_CATALOG.md']:
    if not p.endswith('.md'):
        continue
    for target in re.findall(r'\]\(([^)]+)\)', (R/p).read_text(encoding='utf-8')):
        if re.match(r'https?://', target):
            continue
        target = target.split('#')[0].strip('<>')
        if target and not (R/target).exists() and not ((R/p).parent/target).exists():
            missing.append([p, target])
check('local_links_resolve', not missing, missing)
timeline = read(D/'EVENT_ASSOCIATIONS.json')
csvpath = next(R.glob('70_*.csv'))
with csvpath.open(encoding='utf-8-sig', newline='') as f:
    rows = list(csv.DictReader(f))
check('timeline_csv_exact_roundtrip', rows == timeline and len(rows) == 22, len(rows))
check('timeline_no_delivery_training_claim', all(all(x[k] == 'UNKNOWN' for k in
      ['production_send', 'server_received', 'model_training']) for x in rows), 'All 22 rows')
check('timeline_evidence_references', all(set(x['evidence_ids'].split(';')) <= sources for x in rows),
      'All cited IDs exist')
drafts = ['UKEN_INQUIRY_DRAFT.md', 'SFU_ARCHIVE_INQUIRY_DRAFT.md',
          'RESEARCH_BRIEF_AND_DATA_REQUEST.md', 'PERMISSION_AND_NDA_REVIEW.md']
check('application_drafts_present', all((D/'application'/p).is_file() for p in drafts), drafts)
contacts = read(D/'CONTACT_REGISTRY.json')
check('no_application_sent', len(contacts) == 4 and all(x['sent'] is False for x in contacts), len(contacts))
roundmeta = g['closed_loop_round70']
check('no_new_dataset_training_or_production_test', all(roundmeta[k] == 0 for k in
      ['new_licensed_real_player_datasets', 'applications_sent', 'models_trained', 'production_requests']),
      'Metadata reflects static-only work;not a network-traffic audit')
check('no_player_data_csv_in_round_directory', not list(D.rglob('*.csv')),
      'Round70 contains code/document metadata;only root timeline CSV added')
result = dict(status='PASS' if all(x['passed'] for x in checks) else 'FAIL',
              reviewed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), checks=checks,
              counts=dict(historical_numbered_files=len(historical), deliveries=len(artifacts),
                          new_code_excerpts=38, new_official_sources=6, reused_sources=27,
                          event_rows=len(rows), graph_nodes=len(g['nodes']), graph_edges=len(g['edges']),
                          graph_sources=len(g['sources']), applications_sent=0, models_trained=0),
              limits=['Static evidence integrity only;not runtime SDK or delivery verification',
                      'No raw game dataset or permission obtained;training STOP',
                      'Event identity is not economic deduplication or model consumption',
                      'No new production receipt,training-column,or real ROAS evidence'])
OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(dict(status=result['status'], checks=len(checks),
      failed=[x for x in checks if not x['passed']], counts=result['counts']), ensure_ascii=False, indent=2))
assert result['status'] == 'PASS'
