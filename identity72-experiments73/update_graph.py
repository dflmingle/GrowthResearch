"""Append bounded identity and synthetic-experiment evidence to a frozen baseline."""
from pathlib import Path
import csv, datetime, hashlib, json, re

R = Path(__file__).resolve().parent.parent
D = R / 'identity72-experiments73'
NOW = datetime.datetime.now(datetime.timezone.utc).isoformat()

def read(p):
    return json.loads(p.read_text(encoding='utf-8-sig'))

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def save(p, x):
    p.write_text(json.dumps(x, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

g = read(D / 'EVIDENCE_GRAPH.before.json')
code = read(D / 'CODE_EVIDENCE.json')
pixel = read(D / 'PIXEL_EVIDENCE.json')
docs = read(D / 'SOURCE_EVIDENCE.json')
auth = R / 'identity-graph/sdk/authentication/3.9.0/authentication-3.9.0.tgz'
for x in code:
    x['class_name'] = Path(x['path']).stem
    # These are names visible in the retained excerpt, not inferred execution.
    methods = re.findall(r'(?:public|private|internal|protected|override|suspend|static|final|async)\s+(?:[\w<>?,.\[\]]+\s+){0,5}(\w+)\s*\(', x['excerpt'])
    x['method_names_in_excerpt'] = list(dict.fromkeys(methods))
    x['call_chain_reference'] = x['legacy_id'] + '; related explicit edges in IG72 graph; no runtime observation'
    if 'authentication/3.9.0/' in x['path']:
        x['original_packages'] = [{'path': auth.relative_to(R).as_posix(), 'sha256': sha(auth)}]
        x['version'] = '3.9.0'
save(D / 'CODE_EVIDENCE.json', code)

# Include substantive contract text, not only navigation or partial sentences.
ranges = {'IG72S10': (77, 156), 'IG72S11': (1, 171), 'IG72S13': (1, 80), 'EX73S01': (33, 165)}
for x in docs:
    if x['id'] in ranges:
        a, b = ranges[x['id']]
        ls = (R / x['text_path']).read_text(encoding='utf-8').splitlines()
        x.update(start_line=a, end_line=min(len(ls), b), excerpt='\n'.join(f'{i+1}: {s}' for i, s in enumerate(ls) if a <= i+1 <= b))
save(D / 'SOURCE_EVIDENCE.json', docs)

new_sources = code + pixel + docs
artifact_specs = [
    ('EX73R01', 'PREREGISTRATION.md', 'Frozen B/D protocol before first results'),
    ('EX73R02', 'BPID_ARCHIVE_AUDIT.json', 'Original synthetic ZIP integrity and published checksum'),
    ('EX73R03', 'results/B_DATA_AUDIT.json', 'Synthetic paired-profile schema/split audit'),
    ('EX73R04', 'results/B_RESULTS.csv', '35 synthetic BPID baseline/stress rows;not production matches'),
    ('EX73R05', 'PROTOCOL_AMENDMENT_FS.md', 'Frozen supplementary independent likelihood baseline'),
    ('EX73R06', 'results/B_FS_RESULTS.csv', '7 synthetic BPID probabilistic baseline/stress rows'),
    ('EX73R07', 'results/D_RESULTS.csv', '360 independent synthetic value predictions;generated units'),
    ('EX73R08', 'results/D_CONFIG.json', 'Fixed synthetic generator and model configuration'),
    ('EX73R09', 'results/D_CHECKS.json', 'D0 equals oracle and exact injected-link error counts'),
]
for sid, rel, claim in artifact_specs:
    p = D / rel
    new_sources.append(dict(id=sid, path=p.relative_to(R).as_posix(), sha256=sha(p), claim=claim,
        source_date=datetime.datetime.fromtimestamp(p.stat().st_mtime, datetime.timezone.utc).isoformat(),
        evidence_stages=[], data_type='SYNTHETIC_MECHANISM_OR_PROTOCOL_ONLY',
        production_match_proven=False, prediction_model_consumption_proven=False))

labels = {
 'os_ids': 'OS-scoped advertising/AppSet identifiers;not a natural person',
 'max_local': 'MAX/Axon local IDs and normalized user data',
 'max_payload': 'MAX explicit device/app request fields',
 'axon_match': 'Unknown AppLovin production identity mapping',
 'axon_value': 'Axon disclosed model categories;physical feature lineage unknown',
 'pixel': 'Website Pixel local identifiers/optional contact processing',
 'capi': 'Merchant conversion API contract',
 'wurl': 'CTV/Wurl public business scope',
 'cross_business': 'Unknown ecommerce/CTV personal join to game value',
 'upa': 'Explicit Unity organization-scoped Player Accounts',
 'ugs': 'Project-scoped UGS PlayerId/external provider links',
 'ugs_consumers': 'Analytics/IAP consuming provider interfaces',
 'ads_payload': 'Unity Ads identity/privacy initialization and shared request fields',
 'unity_opportunity': 'Unity opportunity/event/tracking-token snapshots',
 'rampid': 'LiveRamp third-party identity resolution contract',
 'exchange': 'US/Canada Exchange RampID activation contract',
 'vector_match': 'Unknown Vector personal history identity mapping',
 'vector_value': 'Vector cross-game/cohort value disclosures;physical lineage unknown',
 'mixpanel': 'Customer-project Mixpanel ID merge contract',
 'amplitude': 'Customer Amplitude user/device profile contract',
 'branch': 'Branch explicit developer alias contract;no PII in setIdentity',
 'firebase': 'Firebase developer user_id/BigQuery grouping;not automatic cross-customer resolution',
 'uid2': 'UID2 deterministic framework;participation and privacy controls',
 'mmp': 'MMP source/config/partner forwarding contracts',
 'aggregate': 'Aggregate cohort knowledge and shared parameters;no personal cross-app join required',
 'profit': 'Unknown causal game acquisition/profit effect',
}
nodes = [dict(id='IG72N_' + k, label=v, stage='unknown' if k in ['axon_match','cross_business','vector_match','profit'] else 'bounded_public_evidence',
              contains_real_identity_values=False) for k, v in labels.items()]
edges = []
def edge(a, b, claim, ids, grades=(), status='supported_with_limits', missing='', capability=False, request=False):
    edges.append(dict(id=f'IG72E{len(edges)+1:02}', source='IG72N_'+a, target='IG72N_'+b, claim=claim,
        source_ids=ids, identity_evidence_stages=list(grades), status=status,
        evidence_level='UNKNOWN' if status=='unknown' else 'bounded code/document/contract evidence', reviewed_utc=NOW,
        permission_conditions='Source-specific OS/privacy/consent/project/partner scope applies;public analysis only',
        production_match_proven=False, prediction_model_consumption_proven=False,
        production_successful_send=False, server_received_observed=False,
        six_layers=dict(sdk_capability=capability, actual_game_business_callsite=False,
            request_construction_code=request, production_successful_send=False,server_received=False,server_model_training=False),
        missing_evidence=missing or 'Authorized production activation,receipt/match and physical model lineage not observed'))

edge('os_ids','max_local','Explicit allowed OS identifier reads and result/cache;scope/reset does not imply all-app or cross-device person identity', ['IG72C01','IG72C02','IG72C03','IG72C09','IG72S01'], ['E1','E3'], capability=True)
edge('max_local','max_payload','Explicit device/app payload construction;user_data normalization fragment alone is not upload evidence', ['IG72C04','IG72C05','IG72C06','IG72C08','IG72C20'], ['E1','E2'], capability=True,request=True)
edge('max_payload','axon_match','Co-occurring IDs are mapping candidates only;no observed server namespace/match output', ['IG72C04','IG72C05'], status='unknown',missing='Identity mapping schema,conflict/reset rules and authorized successful match record')
edge('axon_match','axon_value','No proof a specific resolved personal identity/history becomes Axon model input', ['CGS51'],status='unknown',missing='Authorized resolved-key -> available-at feature/label -> model-version lineage')
edge('pixel','capi','Pixel constructs website events and optional user_data;CAPI documents merchant conversion fields;not a verified shared resolved identity', ['IG72P04','IG72P05','IG72P06','IG72P09','IG72S06'],['E1','E2','E3'],capability=True,request=True)
edge('capi','axon_match','Merchant/click/contact fields support potential conversion matching;no project-specific successful match', ['IG72S06','IG72S07'],status='unknown')
edge('wurl','cross_business','Public CTV business description is not a household/person-to-game join schema', ['IG72S08'],status='unknown')
edge('capi','cross_business','Website events do not establish ecommerce -> game-model personal reuse', ['IG72S06','IG72S07'],status='unknown')
edge('cross_business','axon_value','Cross-business data availability cannot establish game-specific physical feature consumption', ['CGS51','IG72S07'],status='unknown')
edge('upa','ugs','Explicit OAuth/token and external provider link/project PlayerId contracts;requires actual login and project setup', ['IG72C10','IG72C11','IG72C12','IG72C14','IG72C15','IG72C18','IG72C28','IG72S02','IG72S03'],['E1','E2','E3','E4'],capability=True,request=True)
edge('ugs','ugs_consumers','Registered providers and explicit consumers are code-proven;installation/account scope and runtime equality remain separate', ['C53S12','C53S15','C53S17','C53S18','C53S24','C53S27'],['E1','E2'],capability=True,request=True)
edge('os_ids','ads_payload','AllowedPii gates advertising/fId/AppSet;initialization/shared data explicitly assigns identity fields;not all IDs always sent', ['IG72C22','IG72C23','IG72C24','IG72C25','IG72C26','IG72C27'],['E1','E2'],capability=True,request=True)
edge('ads_payload','unity_opportunity','AdObject opportunity and current token copied into separate operative event and persisted request;not a person or revenue PK', ['L71C15','L71C16','L71C18','L71C19'],['E1','E2'],capability=True,request=True)
edge('ugs','vector_match','No explicit UPA/UGS project-player -> Vector personal identity mapping', ['IG72S02','IG72S03','C53S27'],status='unknown')
edge('ads_payload','vector_match','Advertising/context ID construction alone does not prove cross-device personal resolution', ['IG72C25','IG72C26','IG72C27'],status='unknown')
edge('rampid','exchange','Official third-party identity activation on eligible US/Canada inventory and supporting demand partners', ['IG72S04','IG72S05'],['E3','E4'])
edge('exchange','vector_match','Exchange RampID activation is not proof Vector uses RampID or UPA-resolved histories', ['IG72S05'],status='unknown')
edge('vector_match','vector_value','Specific personal resolved history -> D7/D28 model consumption remains unknown', ['MA60S17'],status='unknown',missing='Authorized feature/label dictionary and resolved identity consumption traces')
for key,sid in [('mixpanel','IG72S10'),('amplitude','IG72S11'),('branch','IG72S12'),('firebase','IG72S13'),('uid2','IG72S09')]:
    edge(key,key,'Explicit provider-specific identity/grouping contract;customer namespace,login and reset/participation constraints apply', [sid],['E3','E4'])
    edge(key,'axon_match','No proof this independent identity service is integrated into Axon personal graph', [sid],status='unknown')
    edge(key,'vector_match','No proof this independent identity service is integrated into Vector personal graph', [sid],status='unknown')
edge('mmp','axon_value','Partner mapping and voluntary sharing contracts;outgoing placeholders are not physical training columns', ['L71D01','CGS49','CGS50','CGS51'],['E3'])
edge('mmp','vector_value','Official sharing/receiver and attributed/unattributed learning categories;not observed delivery or per-row training', ['L72S05','L72S06','L72S07','L72S08','MA60S17'],['E3'])
edge('aggregate','vector_value','Official cross-game behavior/cohort disclosure is compatible with shared knowledge;does not uniquely select personal-history implementation', ['MA60S17'],['E3'])
edge('aggregate','axon_value','Shared-statistic/parameter implementation remains possible;not uniquely disclosed by model-category claims', ['CGS51'],status='unknown')
edge('axon_value','profit','No controlled target-game acquisition/profit outcome,identity ablation or marginal scaling evidence', ['CGS51'],status='unknown')
edge('vector_value','profit','No controlled target-game acquisition/profit outcome or personal-identity contribution estimate', ['MA60S17'],status='unknown')

defs = {
 'E1':'SDK reads/generates/normalizes;not upload', 'E2':'Request/upload construction code;not observed delivery',
 'E3':'Official receiver/purpose document;not observed receipt', 'E4':'Explicit service association contract;not actual project activation',
 'E5':'Authorized production match success;none obtained', 'E6':'Authorized model consumption of matched identity;none obtained'}
identity = dict(schema_version='identity-audit-72-v1', reviewed_utc=NOW, evidence_stages=defs,
    scope='Static/public identity mechanisms only;no real identity values or graph reconstruction',
    nodes=nodes,edges=edges,sources=new_sources[:56]+read(D/'REUSED_EVIDENCE.json'),
    unknown_breakpoints=[e for e in edges if e['status']=='unknown'],
    exclusions=['No production E5/E6','No common-ID implies cross-device person','No UPA/Exchange implies Vector','No synthetic result implies vendor effect'])
assert len(new_sources[:56]) == 56
save(R/'72_跨应用身份关联证据图.json',identity)

experimental_nodes = [
 ('talkingdata','A real device-App experiment STOP;no files/licence'),
 ('bpid','B synthetic human-annotated pairs;Apache-2.0'),
 ('b_results','42 synthetic baseline/stress rows;false merges explicit'),
 ('criteo','C STOP;NC eligibility and 30-day maturity separation unresolved'),
 ('generator','D independent synthetic 8-app/2-device generator'),
 ('d_results','360 generated-value mechanism results;not LTV or ROAS'),
]
en = [dict(id='EX73N_'+k,label=v,data_type='AUDIT_OR_SYNTHETIC_ONLY') for k,v in experimental_nodes]
ee=[]
for a,b,claim,ids,status in [
 ('talkingdata','talkingdata','STOP is not an experiment result;datasets never joined',['EX73S04','EX73S05'],'STOP_NOT_JOINED'),
 ('bpid','b_results','Endpoint-separated synthetic benchmark;F1 and false-merge/stress metrics only',['EX73S02','EX73S03','EX73R02','EX73R03','EX73R04','EX73R05','EX73R06'],'SYNTHETIC_MEASURED'),
 ('criteo','criteo','No Criteo training;D is independent,not imputation or joined identity',['EX73S01'],'STOP_NOT_JOINED'),
 ('generator','d_results','Oracle vs noisy links vs aggregate/shared rules under fixed generated assumptions',['EX73R01','EX73R07','EX73R08','EX73R09'],'SYNTHETIC_MEASURED')]:
    ee.append(dict(id=f'EX73E{len(ee)+1:02}',source='EX73N_'+a,target='EX73N_'+b,claim=claim,source_ids=ids,
        status=status,evidence_level='Independent synthetic mechanism or STOP audit;not identity E5/E6',
        identity_evidence_stages=[],production_match_proven=False,prediction_model_consumption_proven=False,
        cross_dataset_identity_join=False,missing_evidence='Real authorized device/game data and platform production lineage;not supplied by this experiment'))

for name, old, added in [('nodes',g['nodes'],nodes+en),('edges',g['edges'],edges+ee),('sources',g['sources'],new_sources)]:
    old_ids={x['id'] for x in old};assert not old_ids.intersection(x['id'] for x in added)
    assert len({x['id'] for x in added})==len(added)
    g[name]=old+added
g['identity_and_experiments_72_73']=dict(reviewed_utc=NOW,identity_stages=defs,
    new_node_ids=[x['id'] for x in nodes+en],new_edge_ids=[x['id'] for x in edges+ee],new_source_ids=[x['id'] for x in new_sources],
    baseline=dict(nodes=211,edges=250,sources=525),
    preserved_previous_round72='access_and_validation_round72;no historical report rewritten',
    no_production_match_or_model_consumption=True,real_data_model_training=False,
    validation_path='identity72-experiments73/VALIDATION.json')
all_nodes={x['id'] for x in g['nodes']};all_sources={x['id'] for x in g['sources']}
assert all(e['source'] in all_nodes and e['target'] in all_nodes and set(e['source_ids'])<=all_sources for e in edges+ee)
save(R/'prediction-system/EVIDENCE_GRAPH.json',g)

baseline=(D/'EVIDENCE_INDEX.before.md').read_bytes()
historical=read(D/'HISTORY_BEFORE.json')
deliveries=sorted(p for p in R.glob('72_*') if p.is_file() and p.name not in historical)+sorted(R.glob('73_*'))
assert len(deliveries)==16, [p.name for p in deliveries]
section=['','', '## 72身份专题与73独立实验（2026-11-20）','',
 '本节为新增专题，保留此前access72及00—71历史文件。E1读取、E2构造、E3官方接收/用途、E4服务关联契约；E5生产匹配/E6匹配结果入预测均未取得。', '',
 'TalkingData/Criteo STOP；BPID和独立价值实验均为合成。42行B＋360行D＋2行STOP，共404行；不证明真实LTV、ROAS、个人跨App图谱或两家相对优势。', '', '| 交付 | 内容 |','|---|---|']
for p in deliveries:
    section.append(f'| [{p.name}]({p.name}) | '+('机器可读证据/结果' if p.suffix in ['.json','.csv'] else '边界、方法和最终判断')+' |')
section+=['','来源：[SOURCE_CATALOG](identity72-experiments73/SOURCE_CATALOG.md)；复现：[README](identity72-experiments73/README.md)；完整性：[VALIDATION](identity72-experiments73/VALIDATION.json)。', '',
 f'主图仅追加{len(nodes+en)}节点、{len(edges+ee)}边、{len(new_sources)}来源；原211节点/250边/525来源和所有旧元数据保留。72自包含图标明未知边，合成实验不使用E5/E6。', '',
 '下一步优先授权真实游戏cohort和匿名化身份/标签/模型血缘；停止同版本重复扫描和受限来源镜像。未经指示未发送申请、签约或发布。','']
(R/'EVIDENCE_INDEX.md').write_bytes(baseline+'\n'.join(section).encode('utf-8'))
print(json.dumps(dict(deliveries=len(deliveries),new_sources=len(new_sources),nodes=len(g['nodes']),edges=len(g['edges']),sources=len(g['sources'])),indent=2))
