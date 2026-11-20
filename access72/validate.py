from pathlib import Path
import json,csv,hashlib,datetime,re
R=Path(__file__).resolve().parent.parent;D=R/'access72';OUT=D/'VALIDATION.json'
OUT.write_text('{"status":"RUNNING"}',encoding='utf-8')
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
checks=[]
def check(n,ok,detail):checks.append(dict(name=n,passed=bool(ok),detail=detail))
old=read(D/'HISTORY_BEFORE.json');old={p:h for p,h in old.items() if p not in ['EVIDENCE_INDEX.md','prediction-system/EVIDENCE_GRAPH.json']}
bad=[p for p,h in old.items() if not (R/p).is_file() or sha(R/p)!=h]
check('historical_numbered_files_unchanged',not bad,dict(count=len(old),changed=bad))
base=read(D/'EVIDENCE_GRAPH.before.json');g=read(R/'prediction-system/EVIDENCE_GRAPH.json')
for k in ['nodes','edges','sources','unknown_breakpoints','excluded_claims']:
    check('historical_'+k+'_prefix',g[k][:len(base[k])]==base[k],dict(before=len(base[k]),after=len(g[k])))
for k in base:
    if k not in ['nodes','edges','sources','unknown_breakpoints','excluded_claims']:check('old_metadata_'+k,g[k]==base[k],'Preserved')
check('index_append_only',(R/'EVIDENCE_INDEX.md').read_text(encoding='utf-8-sig').startswith((D/'EVIDENCE_INDEX.before.md').read_text(encoding='utf-8-sig')),'Original text retained')
check('graph_snapshot_matches',read(D/'EVIDENCE_GRAPH.after.json')==g,'Current root graph')
for k in ['nodes','edges','sources']:
    ids=[x['id'] for x in g[k]];check('unique_'+k,len(ids)==len(set(ids)),len(ids))
nodes={x['id']:x for x in g['nodes']};sources={x['id']:x for x in g['sources']}
edges=[x for x in g['edges'] if x['id'].startswith('L72E')]
for e in edges:
    check('edge_refs_'+e['id'],e['source'] in nodes and e['target'] in nodes and set(e['source_ids'])<=set(sources),e['status'])
    check('edge_no_production_'+e['id'],not any(e['six_layers'][k] for k in ['sdk_capability','actual_game_business_callsite','request_construction_code','production_successful_send','server_received','server_model_training']) and not e['server_model_training'] and not e['production_actual_proven'],e['missing_evidence'])
for fname in ['SOURCE_EVIDENCE.json','REUSED_EVIDENCE.json']:
    rr=read(D/fname)
    bad=[x['id'] for x in rr if not (R/x['path']).is_file() or sha(R/x['path'])!=x['sha256']]
    check('hashes_'+fname,not bad,dict(count=len(rr),bad=bad))
    if fname!='SOURCE_EVIDENCE.json':continue
    for x in rr:
        check('source_matches_graph_'+x['id'],sources[x['id']]==x,'Exact object')
        if 'text_path' in x:
            p=R/x['text_path'];ls=p.read_text(encoding='utf-8').splitlines()
            excerpt='\n'.join(f'{i+1}: {s}' for i,s in enumerate(ls) if x['start_line']<=i+1<=x['end_line'])
            check('excerpt_'+x['id'],excerpt==x['excerpt'] and sha(p)==x['text_sha256'],dict(path=x['text_path'],lines=[x['start_line'],x['end_line']]))
        else:
            ss=(R/x['path']).read_text(encoding='utf-8')
            check('public_contact_offsets',ss[x['offset_start']:x['offset_end']]==x['excerpt'] and 'info@yokozunadata.com' in x['excerpt'],'Official public contact component only')
        check('source_no_training_receipt_'+x['id'],not x['production_received_observed'] and not x['physical_training_consumption_proven'],x['authorization_scope'])
fetch=read(D/'FETCH_MANIFEST.json')
check('fetch_unique',len({(x['id'],x['url']) for x in fetch})==len(fetch),len(fetch))
for x in fetch:
    if not x.get('path'):continue
    check('fetch_raw_'+x['id'],sha(R/x['path'])==x['sha256'],x.get('status'))
    check('fetch_text_'+x['id'],sha(R/x['text_path'])==x['text_sha256'],x['text_path'])
accepted={x['url'] for x in read(D/'SOURCE_EVIDENCE.json')}
check('failed_sources_excluded',all(x['url'] not in accepted for x in fetch if x.get('status')!=200),'404 not promoted to evidence')
tables=read(D/'PARTNER_TABLE_EXTRACT.json')
receiver=next(x for x in tables if x['table_index']==2)
check('unity_receiver_table_exact',receiver['unity_rows']==[['Unity Ads','✓','✓']],'Separate source and receiver tables')
check('axon_absence_limited_to_snapshot',receiver['applovin_or_axon_rows']==[],'Not universal lack-of-support conclusion')
contact=read(D/'YOKOZUNA_CONTACT_EXCERPT.json')
check('contact_excerpt_hash_source',contact['excerpt'] in (R/contact['path']).read_text(encoding='utf-8'),'New public route,not dataset access')
routes=read(D/'ACCESS_ROUTES.json')
check('all_routes_unsent_unlicensed',all(x['sent'] is False and x['data_access_permitted'] is False for x in routes),len(routes))
design=read(D/'EXPERIMENT_ADMISSION.json')
check('all_three_designs_stop',len(design)==3 and all(x['status']=='STOP' and x['currently_admitted_games']==0 and x['training_executed'] is False for x in design),[x['id'] for x in design])
check('independent_product_requirements',[(x['id'],x['minimum_independent_games']) for x in design]==[('A',1),('B',2),('C',2)],'Independent games,not platforms')
causal=read(D/'CAUSAL_MATRIX.json')
csvpath=next(R.glob('72_*.csv'))
with csvpath.open(encoding='utf-8-sig',newline='') as h:rows=list(csv.DictReader(h))
check('causal_csv_roundtrip',len(rows)==7 and rows==causal,len(rows))
check('causal_unknown_no_experiments',all(x['current_four_game_causal_evidence']=='UNKNOWN' and x['current_real_experiment_result']=='NOT_RUN' for x in rows),'No invented results')
check('causal_refs_valid',all(set(filter(None,x['evidence_ids'].split(';')))<=set(sources) for x in rows),'Empty references explicitly design-only')
meta=g['access_and_validation_round72'];artifacts=meta['reports']
check('six_deliveries',len(artifacts)==6,len(artifacts))
for p in artifacts:check('delivery_'+p,(R/p).is_file() and (R/p).stat().st_size>1000,(R/p).stat().st_size if (R/p).exists() else 0)
local=read(D/'RELATION_GRAPH.json')
check('local_graph_matches',local['edges']==edges and all(nodes[x['id']]==x for x in local['nodes']) and all(sources[x['id']]==x for x in local['sources']),'Self-contained subset')
localids={x['id'] for x in local['sources']}
check('local_graph_refs',all(set(x['source_ids'])<=localids for x in edges),'Sources resolved')
missing=[]
mds=[R/p for p in artifacts if p.endswith('.md')]+list(D.glob('*.md'))
for p in mds:
    txt=p.read_text(encoding='utf-8');check('new_text_utf8_'+p.name,'\ufffd' not in txt,'No replacement characters')
    for target in re.findall(r'\]\(([^)]+)\)',txt):
        if target.startswith(('https://','http://')):continue
        target=target.split('#')[0].strip('<>')
        if target and not (R/target).exists() and not (p.parent/target).exists():missing.append([p.name,target])
check('local_links_resolve',not missing,missing)
boundary=read(D/'SEARCH_BOUNDARY.json')
zero=['new_sdk_scans','new_sdk_downloads','emails_sent','data_applications_sent','nda_signed','models_trained','player_data_downloads','authorized_game_datasets_admitted','authorized_production_receipt_materials']
check('declared_action_boundaries',all(boundary[k]==0 for k in zero) and not boundary['sample_report_downloaded'] and not boundary['private_application_routes_called'],'Artifact/declared audit,not packet-capture proof')
check('strict_goal_gap_recorded',meta['strict_access_or_authorized_production_completion_met'] is False and meta['new_licensed_game_datasets']==0 and meta['authorized_production_materials']==0,'Public-contract progress distinguished from actual permission/production evidence')
check('no_player_data_file_artifacts',not list(D.rglob('*.csv')) and not list(D.rglob('*.parquet')) and not list(D.rglob('*.xlsx')),'Metadata JSON and official pages only;root causal CSV')
result=dict(status='PASS' if all(x['passed'] for x in checks) else 'FAIL',reviewed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),checks=checks,counts=dict(historical_numbered_files=len(old),deliveries=len(artifacts),new_source_records=len(read(D/'SOURCE_EVIDENCE.json')),reused_records=len(read(D/'REUSED_EVIDENCE.json')),causal_rows=len(rows),designs=len(design),graph_nodes=len(nodes),graph_edges=len(g['edges']),graph_sources=len(sources),sdk_scans=0,emails_sent=0,models_trained=0,licensed_game_datasets=0,authorized_production_materials=0),limits=['Integrity/references/admission validation only;no real model effect validation','New public MMP contracts not actual app configuration or received training rows','No new licensed game cohort or confirmed current Uken custodian','Strict access/authorized-production-material objective remains unmet'])
OUT.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(dict(status=result['status'],checks=len(checks),failed=[x for x in checks if not x['passed']],counts=result['counts']),ensure_ascii=False,indent=2));assert result['status']=='PASS'
