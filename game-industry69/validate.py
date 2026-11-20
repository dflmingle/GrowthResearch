from pathlib import Path
import json,hashlib,re,csv,datetime
R=Path(__file__).resolve().parent.parent;D=R/'game-industry69'
# The report intentionally links the result produced by this very run.
# Materialize a RUNNING result before checking links; never treat an older PASS as current.
(D/'VALIDATION.json').write_text(json.dumps({'status':'RUNNING'},indent=2),encoding='utf-8')
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
checks=[]
def check(name,ok,detail):
    checks.append(dict(name=name,passed=bool(ok),detail=detail))
oldhash=read(D/'HISTORY_BEFORE.json')
originals={p:h for p,h in oldhash.items() if p not in ['EVIDENCE_INDEX.md','prediction-system/EVIDENCE_GRAPH.json']}
bad=[p for p,h in originals.items() if not (R/p).exists() or sha(R/p)!=h]
check('historical_numbered_files_byte_preserved',not bad,dict(count=len(originals),changed=bad))
base=read(D/'EVIDENCE_GRAPH.before.json');g=read(R/'prediction-system/EVIDENCE_GRAPH.json')
for k in ['nodes','edges','sources']:
    check('historical_'+k+'_objects_unchanged',g[k][:len(base[k])]==base[k],dict(before=len(base[k]),after=len(g[k])))
for k in base:
    if k in ['nodes','edges','sources','unknown_breakpoints','excluded_claims']:continue
    check('historical_metadata_'+k,g[k]==base[k],'Original section preserved')
for k in ['unknown_breakpoints','excluded_claims']:
    check('historical_'+k+'_prefix',g[k][:len(base[k])]==base[k],'Append only')
idx=(R/'EVIDENCE_INDEX.md').read_text(encoding='utf-8-sig');idx0=(D/'EVIDENCE_INDEX.before.md').read_text(encoding='utf-8-sig')
check('index_append_only',idx.startswith(idx0),'All original index text preserved')
for k in ['nodes','edges','sources']:
    ids=[x['id'] for x in g[k]]
    check('unique_'+k+'_ids',len(ids)==len(set(ids)),len(ids))
nodes={x['id'] for x in g['nodes']};sources={x['id'] for x in g['sources']}
newedges=[x for x in g['edges'] if x['id'].startswith('GI69')]
badrefs=[x['id'] for x in newedges if x['source'] not in nodes or x['target'] not in nodes or not set(x['source_ids'])<=sources]
check('new_graph_refs',not badrefs,badrefs)
layers=['production_successful_send','server_received','server_model_training']
inflated=[x['id'] for x in newedges if any(x['six_layers'].get(k) for k in layers) or x.get('production_actual_proven') or x.get('observed_target_game_delivery')]
check('no_production_evidence_upgrade',not inflated,inflated)
for fname in ['SOURCE_EVIDENCE.json','CODE_EVIDENCE.json','REUSED_EVIDENCE.json']:
    records=read(D/fname)
    bad=[x['id'] for x in records if not (R/x['path']).exists() or x.get('sha256') and sha(R/x['path'])!=x['sha256']]
    check('source_hashes_'+fname,not bad,dict(count=len(records),bad=bad))
    if fname=='CODE_EVIDENCE.json':
        for x in records:
            lines=(R/x['path']).read_text(encoding='utf-8').splitlines()
            expected='\n'.join(f'{i+1}: {s}' for i,s in enumerate(lines) if x['start_line']<=i+1<=x['end_line'])
            check('exact_code_excerpt_'+x['id'],expected==x['excerpt'],dict(path=x['path'],lines=[x['start_line'],x['end_line']],sdk_version=x['version']))
            check('original_sdk_hash_'+x['id'],all(sha(R/a['path'])==a['sha256'] for a in x['verified_original_packages']),len(x['verified_original_packages']))
artifacts=g['game_industry_round69']['report_paths']
for p in artifacts:check('report_present_'+p,(R/p).exists() and (R/p).stat().st_size>1000,(R/p).stat().st_size if (R/p).exists() else 0)
missinglinks=[]
for p in artifacts:
    text=(R/p).read_text(encoding='utf-8')
    for target in re.findall(r'\]\(([^)]+)\)',text):
        if re.match(r'https?://',target):continue
        path=target.split('#')[0]
        if path and not (R/path).exists():missinglinks.append((p,target))
check('report_local_links_resolve',not missinglinks,missinglinks)
timeline=read(D/'SDK_FIELD_TIMELINE.json')
check('timeline_24_fields',len(timeline)==24,len(timeline))
check('timeline_no_production_or_model_use_claim',all(x['production_receipt']=='UNKNOWN' and x['model_consumption']=='UNKNOWN' for x in timeline),'24 rows preserve receiver vs receipt distinction')
catalog=read(D/'DATASET_ADMISSION.json')
check('no_unlicensed_training_admitted',all(x['admission'] in ['STOP','EXCLUDED'] for x in catalog),[{'id':x['id'],'admission':x['admission']} for x in catalog])
for f in ['SDK_FIELD_TIMELINE.csv','DATASET_ADMISSION.csv']:
    with (D/f).open(encoding='utf-8-sig',newline='') as h:rows=list(csv.DictReader(h))
    check('csv_roundtrip_'+f,len(rows)==(24 if f.startswith('SDK') else 6),len(rows))
fetch=read(D/'FETCH_MANIFEST.json')
check('fetch_manifest_unique',len({(x['id'],x['url']) for x in fetch})==len(fetch),len(fetch))
check('fetch_raw_hashes',all(x.get('sha256_verified',True) for x in fetch),'Includes denied/error responses,not all evidence')
files_meta=read(D/'sources/unity-osf-files.html')['data']
download_map={'Technical Appendix.docx':D/'sources/unity-technical-appendix.docx','Code for Publication.R':D/'sources/unity-analysis-code.R'}
for x in files_meta:
    name=x['attributes']['name'];expected=x['attributes']['extra']['hashes']['sha256']
    check('osf_published_hash_'+name,sha(download_map[name])==expected,expected)
check('osf_paper_published_hash',sha(D/'sources/unity-full-paper.pdf')==read(D/'sources/unity-file-meta.html')['data']['attributes']['extra']['hashes']['sha256'],'PDF matches public OSF metadata')
prohibited=list(D.rglob('*.csv'))
check('no_downloaded_player_rows',all(x.name in ['SDK_FIELD_TIMELINE.csv','DATASET_ADMISSION.csv'] for x in prohibited),'No Uken prediction/user rows,transaction rows,or game identifiers collected')
result=dict(status='PASS' if all(x['passed'] for x in checks) else 'FAIL',reviewed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),checks=checks,counts=dict(reports=len(artifacts),timeline=len(timeline),new_game_training_datasets=0,models_trained=0,applications_sent=0,graph_nodes=len(g['nodes']),graph_edges=len(g['edges']),graph_sources=len(g['sources'])),limits=['Evidence integrity audit only;not SDK runtime or production receipt test','MAG original paper/data identity remains unresolved','Uken permission/scaling/observation window unresolved','No new legal real player training data acquired'])
(D/'VALIDATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(dict(status=result['status'],checks=len(checks),failed=[x for x in checks if not x['passed']],counts=result['counts']),ensure_ascii=False,indent=2))
assert result['status']=='PASS'
