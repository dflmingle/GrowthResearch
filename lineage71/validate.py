from pathlib import Path
import json,csv,hashlib,datetime,re
R=Path(__file__).resolve().parent.parent;D=R/'lineage71';OUT=D/'VALIDATION.json'
OUT.write_text('{"status":"RUNNING"}',encoding='utf-8')
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
checks=[]
def check(name,ok,detail):checks.append(dict(name=name,passed=bool(ok),detail=detail))
old=read(D/'HISTORY_BEFORE.json')
old={p:h for p,h in old.items() if p not in ['EVIDENCE_INDEX.md','prediction-system/EVIDENCE_GRAPH.json']}
bad=[p for p,h in old.items() if not (R/p).is_file() or sha(R/p)!=h]
check('historical_numbered_files_byte_preserved',not bad,dict(count=len(old),changed=bad))
base=read(D/'EVIDENCE_GRAPH.before.json');g=read(R/'prediction-system/EVIDENCE_GRAPH.json')
for k in ['nodes','edges','sources','unknown_breakpoints','excluded_claims']:
    check('historical_prefix_'+k,g[k][:len(base[k])]==base[k],dict(before=len(base[k]),after=len(g[k])))
for k in base:
    if k not in ['nodes','edges','sources','unknown_breakpoints','excluded_claims']:
        check('historical_metadata_'+k,g[k]==base[k],'Old graph section retained')
check('index_append_only',(R/'EVIDENCE_INDEX.md').read_text(encoding='utf-8-sig').startswith((D/'EVIDENCE_INDEX.before.md').read_text(encoding='utf-8-sig')),'Original text retained')
check('after_snapshot_matches',read(D/'EVIDENCE_GRAPH.after.json')==g,'Current graph')
for k in ['nodes','edges','sources']:
    ids=[x['id'] for x in g[k]];check('unique_ids_'+k,len(ids)==len(set(ids)),len(ids))
nodes={x['id']:x for x in g['nodes']};sources={x['id']:x for x in g['sources']}
edges=[x for x in g['edges'] if x['id'].startswith('L71E')]
for x in edges:
    check('edge_refs_'+x['id'],x['source'] in nodes and x['target'] in nodes and set(x['source_ids'])<=set(sources),x['status'])
    st=x['six_layers']
    check('no_production_upgrade_'+x['id'],not any(st[k] for k in ['production_successful_send','server_received','server_model_training']) and not x['production_actual_proven'] and not x['server_model_training'],x['missing_evidence'])
for f in ['SOURCE_EVIDENCE.json','CODE_EVIDENCE.json','REUSED_EVIDENCE.json']:
    rr=read(D/f)
    bad=[x['id'] for x in rr if not (R/x['path']).is_file() or sha(R/x['path'])!=x['sha256']]
    check('source_hashes_'+f,not bad,dict(count=len(rr),bad=bad))
    if f=='REUSED_EVIDENCE.json':continue
    for x in rr:
        p=R/x.get('excerpt_path',x['path']);ss=p.read_text(encoding='utf-8-sig').splitlines()
        excerpt='\n'.join(f'{i+1}: {s}' for i,s in enumerate(ss) if x['start_line']<=i+1<=x['end_line'])
        check('excerpt_'+x['id'],excerpt==x['excerpt'],dict(path=p.relative_to(R).as_posix(),lines=[x['start_line'],x['end_line']]))
        check('source_matches_graph_'+x['id'],sources[x['id']]==x,'Full record')
        if 'excerpt_sha256' in x:check('extracted_text_hash_'+x['id'],sha(p)==x['excerpt_sha256'],x['excerpt_sha256'])
        if 'original_packages' in x:
            check('original_package_hash_'+x['id'],all(sha(R/z['path'])==z['sha256'] for z in x['original_packages']),len(x['original_packages']))
            check('code_layer_status_'+x['id'],not any(x['six_layers'][k] for k in ['production_successful_send','server_received','server_model_training']),'No runtime evidence inferred')
fetch=read(D/'FETCH_MANIFEST.json')
check('fetch_unique',len({(x['id'],x['url']) for x in fetch})==len(fetch),len(fetch))
bad=[x['id'] for x in fetch if x.get('path') and (not (R/x['path']).is_file() or sha(R/x['path'])!=x['sha256'])]
check('fetch_response_hashes',not bad,bad)
accepted={x.get('url') for x in read(D/'SOURCE_EVIDENCE.json')}
check('failed_fetches_not_source_evidence',all(x['url'] not in accepted for x in fetch if x.get('status')!=200),'404/failed redirect excluded')
t=read(D/'TARGETED_ANALYSIS.json')
check('single_class_original_jar',sha(R/t['input'])==t['input_sha256'],t['input'])
check('targeted_analysis_exit',t['decompile_exit']==0 and t['bytecode_exit']==0,t['class_name'])
check('targeted_bytecode_hash',sha(R/t['bytecode_path'])==t['bytecode_sha256'],t['bytecode_path'])
check('sdk_getter_signature',sha(R/t['sdk_getter_signature_path'])==t['sdk_getter_signature_sha256'] and t['sdk_getter_signature'] in (R/t['sdk_getter_signature_path']).read_text(encoding='utf-8'),t['sdk_getter_signature'])
bc=(R/t['bytecode_path']).read_text(encoding='utf-8-sig')
check('bytecode_identity_overlay_publish_anchors',all(x in bc for x in ['max_revenue_events','String id','c3.T','putAll','publish']), 'Original bytecode cross-check,not runtime SDK test')
meta=g['training_lineage_round71'];artifacts=meta['reports']
check('eight_deliveries',len(artifacts)==8,len(artifacts))
for p in artifacts:check('delivery_'+p,(R/p).is_file() and (R/p).stat().st_size>1000,(R/p).stat().st_size if (R/p).is_file() else 0)
local=read(R/next(p for p in artifacts if p.endswith('.json')))
check('local_graph_edges_match',local['edges']==edges,len(edges))
check('local_graph_nodes_match',all(nodes[x['id']]==x for x in local['nodes']),len(local['nodes']))
check('local_graph_sources_match',all(sources[x['id']]==x for x in local['sources']),len(local['sources']))
localids={x['id'] for x in local['sources']}
check('local_graph_source_refs',all(set(x['source_ids'])<=localids for x in edges),'Self-contained source references')
rows=read(D/'FIELD_LINEAGE.json')
with (D/'FIELD_LINEAGE.csv').open(encoding='utf-8-sig',newline='') as h:csvrows=list(csv.DictReader(h))
check('field_csv_exact_roundtrip',len(rows)==22 and rows==csvrows,len(rows))
check('field_matrix_evidence_refs',all(set(x['evidence_ids'].split(';'))<=set(sources) for x in rows),'Each row cites original sources')
check('field_matrix_no_training_or_receipt_upgrade',all(all(x[k]=='UNKNOWN' for k in ['production_send','server_received','physical_training_column']) for x in rows),'22 rows retain boundaries')
drafts=['APPLICANT_INFORMATION.md','UKEN_REVIEW_EMAIL.md','SFU_REVIEW_EMAIL.md','ACCESS_OPTIONS_AND_MINIMUM_SCHEMA.md']
check('application_package_present',all((D/'application'/p).is_file() for p in drafts),drafts)
contacts=read(D/'CONTACT_REGISTRY.json')
check('contacts_unsent_unlicensed',all(x['sent'] is False and x['current_2015_custodian_confirmed'] is False and x['application_identity_complete'] is False for x in contacts),len(contacts))
check('applicant_placeholders_explicit',all('[ACTUAL NAME]' in (D/'application'/p).read_text(encoding='utf-8') for p in ['UKEN_REVIEW_EMAIL.md','SFU_REVIEW_EMAIL.md']),'No applicant affiliation invented')
missing=[]
mds=[R/p for p in artifacts if p.endswith('.md')]+list((D/'application').glob('*.md'))+[D/'SOURCE_CATALOG.md']
for p in mds:
    for target in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
        if target.startswith(('https://','http://')):continue
        target=target.split('#')[0].strip('<>')
        if target and not (R/target).exists() and not (p.parent/target).exists():missing.append([p.relative_to(R).as_posix(),target])
check('local_links_resolve',not missing,missing)
check('new_reports_utf8_no_replacement',all('\ufffd' not in p.read_text(encoding='utf-8') for p in mds),'Original source pages may have their own encoding;new reports checked')
check('no_training_data_or_production_experiment',all(meta[k]==0 for k in ['applications_sent','models_trained','new_licensed_game_datasets','production_requests']),'Metadata and generated artifacts only;not a traffic audit')
check('round_csv_is_metadata_only',all(p.name=='FIELD_LINEAGE.csv' for p in D.rglob('*.csv')),'No downloaded player rows')
result=dict(status='PASS' if all(x['passed'] for x in checks) else 'FAIL',reviewed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),checks=checks,counts=dict(historical_numbered_files=len(old),deliveries=len(artifacts),new_code_excerpts=len(read(D/'CODE_EVIDENCE.json')),new_source_records=len(read(D/'SOURCE_EVIDENCE.json')),reused_records=len(read(D/'REUSED_EVIDENCE.json')),field_rows=len(rows),graph_nodes=len(nodes),graph_edges=len(g['edges']),graph_sources=len(sources),applications_sent=0,models_trained=0),limits=['Static evidence integrity,not SDK runtime/delivery/accounting verification','Final MAX broadcast id can be overridden;S2S ID mapping unknown','No observed partner receipt or physical training columns','Current Uken rights-holder/data licence/files unknown;no training'])
OUT.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(dict(status=result['status'],checks=len(checks),failed=[x for x in checks if not x['passed']],counts=result['counts']),ensure_ascii=False,indent=2))
assert result['status']=='PASS'
