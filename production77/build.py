"""Round 77 evidence packaging. Offline only; never rerun prepare.py."""
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urlsplit, parse_qs
import csv, datetime, hashlib, json, re

R = Path(__file__).resolve().parent.parent
D = R / 'production77'
NOW = datetime.datetime.now(datetime.timezone.utc).isoformat()
def load(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p, s):
    content=(s.rstrip()+'\n').encode('utf-8')
    if p.exists():
        assert p.read_text(encoding='utf-8')==s.rstrip()+'\n', f'Refuse changed overwrite: {p}'
        return
    p.write_bytes(content)
def save(p, x): write(p, json.dumps(x, ensure_ascii=False, indent=2))

history = load(D/'HISTORY_BEFORE.json')
for name, digest in history.items(): assert sha(R/name) == digest, name
base = load(D/'EVIDENCE_GRAPH.before.json')
prior = load(D/'PRIOR_URL_CATALOG.json')
all_fetch = []
for f in sorted(D.glob('FETCH_*.json')): all_fetch.extend(load(f))
assert len(all_fetch) == 21
fetch = {x['id']: x for x in all_fetch}
assert len(fetch) == len(all_fetch)

def identity_url(url):
    p = urlsplit(url)
    if 'greenhouse.io' in p.netloc:
        m = re.search(r'/jobs/(\d+)', p.path)
        if m: return 'greenhouse:applovin:'+m[1]
    if 'myworkdayjobs.com' in p.netloc:
        m = re.search(r'JOBREQ-(\d+)', p.path)
        if m: return 'unity:JOBREQ-'+m[1]
    if 'patents.google.com' in p.netloc and '/patent/' in p.path:
        return 'patent:'+p.path.split('/patent/')[1].split('/')[0]
    return p.netloc.lower()+p.path.rstrip('/')

sources=[]
def source(sid, key, company, title, team, product, kind, quote, date=None):
    x=fetch[key]
    assert x['status']==200 and sha(R/x['path'])==x['sha256']
    raw=R/x['path']
    if key.startswith('al-'):
        j=load(raw)
        content=BeautifulSoup(j['content'],'html.parser').get_text('\n',strip=True)
        dates={'first_published':j.get('first_published'),'updated_at':j.get('updated_at')}
        canonical=j['absolute_url']
        locator='$.content (HTML text)'
    elif key.endswith('-job'):
        j=load(D/'sources'/(key+'.jobposting.json'))
        content=BeautifulSoup(j['description'],'html.parser').get_text('\n',strip=True)
        dates={'datePosted':j['datePosted']}
        canonical=x['url'];locator='HTML script[type=application/ld+json] $.description'
    else:
        content=(R/x['text_path']).read_text(encoding='utf-8')
        dates=date;canonical=x['url'];locator='Published description and Claims 1,7,12'
    assert quote in content, (sid,quote)
    normalized=D/'sources'/(key+'.verified.txt')
    write(normalized,content)
    overlaps=[p['id'] for p in prior if identity_url(p['url'])==identity_url(canonical)]
    out=dict(id=sid,fetch_id=key,company=company,publisher=company if kind!='patent_scheme' else 'US patent publication reproduced by Google Patents',
      title=title,team=team,product=product,evidence_kind=kind,url=x['url'],canonical_url=canonical,
      path=x['path'],sha256=x['sha256'],text_path=normalized.relative_to(R).as_posix(),text_sha256=sha(normalized),
      source_dates=dates,acquired_utc=x['acquired_utc'],reviewed_utc=NOW,exact_quote=quote,locator=locator,
      new_url=not bool(overlaps),prior_equivalent_source_ids=overlaps,production_match_proven=False,
      prediction_model_consumption_proven=False,independent_real_identity_lift_proven=False,
      permission_conditions='Public engineering documents only;no authorized platform matching,model access or decision experiments',
      evidence_stages=[],production_actual_proven=False)
    sources.append(out)
    return out

source('PE77S01','al-infra-job','AppLovin','ML Infrastructure Engineer','Software engineering infrastructure',
 'AppLovin bidding ecosystem;Axon-specific model UNKNOWN','job_requirement_and_team_description',
 'Our infra team is responsible for providing and maintaining scalable infrastructure with high throughput and low latency to our bidding ecosystem.')
source('PE77S02','al-analytics-job','AppLovin','Data Scientist – Analytics','Analytics;works with engineering and research',
 'AppLovin ad and app ecosystem;Axon-specific model UNKNOWN','job_requirement_and_team_description',
 'petabyte-scale datasets across our ad and app ecosystem')
source('PE77S03','unity-modeling-job','Unity','Principal Machine Learning Engineer, Ads Modeling','Vector Ads Modeling',
 'Unity Vector','job_requirement_and_team_description',
 'Leverage rich user data and large-scale compute to validate models rapidly.')
source('PE77S04','unity-data-job','Unity','Senior Machine Learning Engineer, Data Infrastructure','Vector data infrastructure',
 'Unity Vector','job_requirement_and_team_description',
 'our platform also supports large-scale model training, feature generation, and experimentation workflows that power production ML systems.')
source('PE77S05','unity-vector-job','Unity','Senior Machine Learning Engineer, Vector Bidding Science','Vector Bidding Science;Vector AI org',
 'Unity Vector','job_requirement_and_team_description',
 'By harnessing massive datasets and rich signals, you will develop state-of-the-art bidding and pacing algorithms that automatically maximize advertisers’ returns.')
source('PE77S06','unity-is-patent','Unity/ironSource','US12353873B2','Inventors Arnon Harish;Sagi Ben Basat',
 'OS-version-specific application recommendation;NOT identified as Vector','patent_scheme',
 '1. A content recommendation system for providing each of a set of mobile client devices with operating system (OS) version specific application recommendations, said system comprising:',
 dict(priority='2015-08-11',filing='2021-03-26',publication_and_grant='2025-07-08'))
sources[-1]['patent_metadata']=dict(application='US17/301,134',inventors=['Arnon Harish','Sagi Ben Basat'],
 current_assignees_as_displayed=['IronSource Ltd','Unity Technologies SF'],original_assignee_as_displayed='Unity Technologies SF',
 assignment_event='2021-12-09 assigned to IRONSOURCE LTD.;recorded names do not prove product integration',
 status_as_displayed='Active;Google legal status and assignee accuracy disclaimers apply;not independently legally verified',
 claims_count=20,independent_claims=[1,7,12],claim_scope='OS-change-triggered app recommendations using application inventory,ancillary data and compatibility;not a claimed Vector identity-value-model chain')
save(D/'SOURCE_EVIDENCE.json',sources)
save(D/'FETCH_MANIFEST.json',all_fetch)

old={s['id']:s for s in base['sources']}
new={s['id']:s for s in sources}
rows=[]
def claim(cid, sid, company, product, team, kind, scope, receipt, features, quote, explanation, missing, reused=''):
    s=(new|old)[sid]
    path=s.get('text_path') or s['path']
    text=(R/path).read_text(encoding='utf-8-sig')
    assert quote in text, (cid,quote)
    pos=text.index(quote);line=text[:pos].count('\n')+1
    rows.append(dict(claim_id=cid,source_id=sid,company=company,product=product,team=team,
      evidence_category=kind,original_url=s['url'],canonical_url=s.get('canonical_url',s.get('final_url',s['url'])),
      publisher=s.get('publisher',company),source_dates=json.dumps(s.get('source_dates',s.get('source_date')),ensure_ascii=False),
      acquired_utc=s.get('acquired_utc','see original source record'),applicable_time='Only stated publication/update and observed snapshot;no retroactive deployment claim',
      raw_file=s['path'],raw_sha256=s['sha256'],excerpt_file=path,excerpt_sha256=sha(R/path),excerpt_start_line=line,
      exact_quote=quote,entity_granularity=scope,cross_app_history_actual_receipt=receipt,
      resolved_identity_feature_use=features,specific_Axon_Vector_production_consumption='UNKNOWN',
      identity_component='UNSPECIFIED;patent inventory or RampID scope where explicitly noted',
      receiving_product=product,feature_consumer='UNKNOWN for resolved identity feature',
      deployment_classification=kind,bridge_complete=False,production_match_proven=False,
      prediction_model_consumption_proven=False,independent_identity_lift_proven=False,
      duplicate_status='REUSED' if reused else 'NEW_URL_BUT_NO_C_GRAPH_UPGRADE',
      existing_evidence_refs=reused,competing_explanation=explanation,missing_evidence=missing,
      c_graph_upgrade=False))

gap='Named resolver output/namespace/granularity -> actual product receipt -> available_at feature group -> specific model version/read trace'
claim('PE77C01','S25','AppLovin','Advertising platform;Axon unspecified','User signal/recommendation ML',
 'job_requirement_and_team_description','User representation;device/person/household scope UNKNOWN','NOT_ESTABLISHED','UNKNOWN',
 'Develop and improve user signals, features, and representations used by large-scale machine learning models for advertising and recommendation.',
 'App-local or device-local signals,context embeddings,aggregate patterns and shared model parameters also fit',gap,'S25;MA60S06')
claim('PE77C02','S26','AppLovin','Advertising platform;Axon unspecified','ML Data Infrastructure',
 'job_requirement_and_team_description','Entity scope UNKNOWN','NOT_ESTABLISHED','UNKNOWN',
 'Design and build data processing infrastructure for model training and feature serving, optimizing for performance, reproducibility, and traceability',
 'Generic model data delivery;not an identity-resolution service',gap,'S26;MA60S07')
claim('PE77C03','PE77S01','AppLovin',sources[0]['product'],sources[0]['team'],sources[0]['evidence_kind'],
 'Entity scope UNKNOWN','NOT_ESTABLISHED','UNKNOWN',sources[0]['exact_quote'],
 'Context/cohort models need the same low-latency infrastructure;no identity graph named',gap)
claim('PE77C04','PE77S02','AppLovin',sources[1]['product'],sources[1]['team'],sources[1]['evidence_kind'],
 'DAU/data ecosystem scope;entity-resolution grain UNKNOWN','NOT_ESTABLISHED','UNKNOWN',sources[1]['exact_quote'],
 'Across-ecosystem datasets may be separate analytics tables or aggregates;not a personal join',gap)
claim('PE77C05','S31','AppLovin','Pre-Axon patent US20130159103A1','Patent inventors;not modern Axon team',
 'patent_scheme','Device application inventory -> profile;not demonstrated cross-device person resolution','DESIGN_ONLY_NOT_RECEIPT','UNKNOWN',
 'a list of mobile applications installed on the mobile device 105',
 'App inventory/profile ad-selection design,not deployed modern value model',gap+';modern lawful implementation/deployment evidence','S31;MA60S11;MA60S12')
for num,sid,scope,explain in [
 (6,'PE77S03','User behavior modeling;person/device scope UNKNOWN','Rich user data may be first-party behavior,context or aggregate statistics;productionalize is a task,not a graph launch record'),
 (7,'PE77S04','Training dataset/feature pipeline;entity grain UNKNOWN','Production ML pipeline statement does not name identity input columns,resolver or model consumers'),
 (8,'PE77S05','Marketplace/bidding context;entity grain UNKNOWN','Bidding/pacing can improve from market-price and budget models without cross-app identity')]:
    s=new[sid]
    legacy={'PE77S03':('S30','S30;MA60S19'),'PE77S05':('S28','S28;MA60S20')}.get(sid)
    claim(f'PE77C{num:02}',legacy[0] if legacy else sid,'Unity',s['product'],s['team'],s['evidence_kind'],scope,
      'NOT_ESTABLISHED','UNKNOWN',s['exact_quote'],explain,gap,legacy[1] if legacy else '')
claim('PE77C09','MA60S17','Unity','Unity Vector IAP ROAS','Official optimization article',
 'REUSED_official_product_use_disclosure','Cross-game behavior patterns AND aggregate cohorts;individual join scope UNKNOWN',
 'CATEGORY_USE_DISCLOSED;NO_INSTANCE_RECEIPT','CATEGORY_USE_DISCLOSED;RESOLVED_GRAPH_UNKNOWN',
 'It uses both attributed data and unattributed data, like cross-game behavioral patterns and aggregate cohort insights, to distinguish between these player types at the moment of bid decision.',
 'Aggregate cohort priors or shared representations also satisfy this disclosure',gap,'MA60S17')
claim('PE77C10','IG72S05','Unity','Unity Exchange;NOT Vector','Exchange/LiveRamp integration',
 'REUSED_official_partner_integration_disclosure','RampID-enabled audiences;Unity-specific person/device/household grain UNKNOWN',
 'EXCHANGE_AVAILABILITY_DISCLOSED;NO_VECTOR_RECEIPT','UNKNOWN',
 'LiveRamp’s durable, interoperable identifier, RampID is now available across Unity Exchange in the U.S. and Canada.',
 'Exchange passes an audience identity for external buyers without Vector reading it',gap+';maintained/derived and actual match state','IG72S05')
claim('PE77C11','PE77S06','Unity/ironSource',sources[-1]['product'],sources[-1]['team'],'patent_scheme',
 'Mobile-device inventory/OS;not personal/cross-device graph','DESIGN_ONLY_APP_INVENTORY_NOT_BEHAVIOR_RECEIPT','UNKNOWN',
 sources[-1]['exact_quote'],'OS compatibility app recommendation is sufficient for claimed design;Vector is not named',
 gap+';actual deployment and identity resolver evidence')
claim('PE77C12','IV74S09','AppLovin','Axon AI','Official ad-factor disclosure',
 'REUSED_official_product_use_disclosure','Advertising/user IDs and histories;resolved graph scope UNKNOWN',
 'CATEGORY_USE_DISCLOSED;NO_INSTANCE_RECEIPT','C_ID_DISCLOSED;C_GRAPH_UNKNOWN',
 'Advertising IDs or User IDs (e.g., IDFA/GAID);',
 'Device ID/local ad history/context and cohort learning fit;ID usage does not establish an identity resolver',gap,'IV74S09')

matrix_name='77_生产身份图谱工程证据矩阵.csv'
assert not (R/matrix_name).exists()
with (R/matrix_name).open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
save(D/'CLAIMS.json',rows)

coverage=dict(reviewed_utc=NOW,scope='Four permitted engineering material categories only;bounded discovery and primary-document follow-up',
 public_get_records=len(all_fetch),new_admitted_primary_sources=4,retained_primary_snapshots=6,new_c_graph_upgrades=0,
 AppLovin_jobs=dict(listed=45,new_details=2,old_detail_refetches=0,old_roles_reused=['4712559006','4716524006','4705264006']),
 Unity_jobs=dict(old_board_status=404,actual_official_positions=129,selected_details=3,new_entities=1,
  duplicate_fetches=['2616596 is S30/MA60S19','2616286 is S28/MA60S20'],
  extraction='Official careers Next.js payload -> external Workday URLs -> JobPosting JSON-LD;empty visible text was NOT treated as empty vacancy'),
 patents=dict(narrow_AppLovin_identity_graph_results=0,narrow_Unity_cross_device_results=1,
  off_topic_Unity_result='US20250028580A1 Polyspatial application interaction;not admitted',
  assignee_only_AppLovin='US20130159103A1 already archived;not refetched',
  ironSource_identity_results=4,new_full_document='US12353873B2;read claims 1,7,12;not Vector graph proof'),
 papers_talks=dict(discovery='Four bounded OpenAlex query result pages;no relevant official engineering paper admitted',
  limitation='Metadata search is not an exhaustive conference/blog/full-text search;no broad search expansion'),
 integration=dict(google_cloud_pages='Two HTTP200 soft404 pages;no architecture admitted',
  investor_pages='Two guessed acquisition URLs HTTP404;no integration evidence admitted',
  legacy='IG72S05 reused solely to bound Exchange vs Vector;no new partner-list survey'),
 forbidden_actions=dict(SDK_scans=0,privacy_policy_surveys=0,partner_list_surveys=0,synthetic_experiments=0,
  mock_development=0,identity_queries=0,production_ad_requests=0,emails=0,signups=0),
 stop='No new complete component -> actual receiving product -> actual identity feature-read bridge. Stop current round;not evidence of nonexistence.')
save(D/'SEARCH_COVERAGE.json',coverage)

catalog=['# 77号原始工程材料目录','',f'采集/核对日期：2026-11-20；整理时间：{NOW}。6份正文快照中真正新增4项：3份官方岗位、1份专利；另2份为旧岗位的URL别名重复获取，不计新增。新URL不等于新机制，更不等于生产升级。','',
 '21份公开GET响应均保留在FETCH_MANIFEST.json；HTTP200但正文为空/soft404不得当有效技术证据。Unity岗位从原始HTML中的JobPosting JSON-LD提取，未绕过登录或调用招聘申请接口。','']
for s in sources:
    catalog += [f"## {s['id']}：{s['title']}",'',f"- 发布方：{s['publisher']}；团队：{s['team']}；产品：{s['product']}。",
     f"- 原始URL：{s['url']}",f"- 人类页面：{s['canonical_url']}",f"- 发布/更新字段：`{json.dumps(s['source_dates'],ensure_ascii=False)}`；采集：`{s['acquired_utc']}`。",
     f"- 原始文件：[{Path(s['path']).name}](../{s['path']})；SHA256：`{s['sha256']}`。",
     f"- 可读文本：[{Path(s['text_path']).name}](../{s['text_path']})；SHA256：`{s['text_sha256']}`。",
     f"- 原文位置：`{s['locator']}`。短摘录：\n\n> {s['exact_quote']}",'',
     f"- 去重：{'新增来源' if s['new_url'] else '重复快照；复用旧ID '+','.join(s['prior_equivalent_source_ids'])}。",
     '- 层级：岗位/团队职责或专利方案；实际身份匹配、指定价值模型消费及独立增益均未证实。原始日期字段不冒称上线日期。','']
catalog += ['## 复用与去重','',
 '复用S25/MA60S06（同一岗位），S26/MA60S07（同一岗位），S31/MA60S11/MA60S12（同一旧专利），MA60S17、IG72S05及IV74S09。原路径、SHA256和原证据编号见REUSED_EVIDENCE.json。EN76S04仅用于审计门槛，不是厂商事实。',
 '材料以Greenhouse job ID、Workday JOBREQ及专利公开号去重。校验发现PE77S03实际为S30/MA60S19、PE77S05实际为S28/MA60S20的Workday HTML别名；此前CXS JSON正文已覆盖。两次重复获取是执行偏差，保留记录并从新增计数与主图新来源中排除。主矩阵直接引用旧ID；没有把同一岗位重算。4项真正新来源也不构成C_graph升级。','',
 '## 覆盖与失败','',
 '只对原始来源正文作结论。Google Patents的0条窄查询结果不等于没有专利；OpenAlex无命中不等于没有工程演讲；旧Unity招聘板404不等于没有岗位；投资者URL404及云客户页soft404不证明收购或架构不存在。详见SEARCH_COVERAGE.json与21份原始响应。']
write(D/'SOURCE_CATALOG.md','\n'.join(catalog))

reports={
'77_Axon身份图谱工程证据.md':'''# 77号：Axon身份图谱工程证据

2026-11-20。**没有取得Axon生产价值模型实际读取跨App或跨设备身份图谱特征的直接工程证据；本轮C_graph升级为零。** 有官方岗位说明用户表示、模型训练/服务和竞价基础设施，也有既有Axon标识/历史行为类别用途披露。这些正证据成立，但没有闭合“解析组件→实际接收产品→价值模型读取”。不据此判断图谱不存在。

## 判定范围与原有起点

沿用74号：A是能力/契约，B是特定产品接收，C_id是标识/历史类别用途，C_graph是具体身份解析结果或关联历史进入指定价值模型，D是固定条件下身份独立增益。75号证明仅观察广告变化不能识别个人图谱；76号本地审计验证了检查时间、权限、实际读取及决策引用的方法，不能当厂商生产日志。

本轮只核对岗位、专利、技术论文/文章及整合架构。未重扫SDK、重搜隐私政策、整理伙伴名单或进行实验；完整矩阵含原URL、日期、摘录、文件哈希、实体粒度及未证环节。

## 最接近的工程线索仍是已有用户表示岗位

S25/MA60S06为同一官方Software Engineer ML岗位4712559006，原文件第7—21行描述user signals、representation learning、ranking、retrieval及从特征开发到production的职责：

> Develop and improve user signals, features, and representations used by large-scale machine learning models for advertising and recommendation.

这明确连接“用户信号/表示研发”与“广告推荐模型职责”，比普通AI宣传具体。但user不提供设备/账号/人/家庭的粒度定义；岗位未指定identity resolver、跨设备join、映射namespace、输入列或Axon价值模型版本。第一方历史、设备内互动、上下文embedding和群体共享参数同样相容。岗位任务也不是某特征已经上线的运行证明。PE77C01明确标REUSED，没有重复下载这份正文。

S26/MA60S07（4716524006）涉及model training、feature serving以及raw ingestion到feature delivery，说明数据基础设施职责，不说明谁做身份解析。不能将两份岗位拼接为“已知图谱通过feature store进入Axon”。

## 本轮两份新增岗位提供了什么

| 新证据 | 原文与具体范围 | 能支持什么 | 不能支持什么 |
|---|---|---|---|
| PE77S01 / PE77C03，ML Infrastructure Engineer 4655740006 | high throughput and low latency to our bidding ecosystem；training、serving、online models | 官方团队描述竞价模型交付基础设施 | 没有解析组件、跨App接收列或Axon专属消费记录 |
| PE77S02 / PE77C04，Data Scientist – Analytics 4705263006 | petabyte-scale datasets across our ad and app ecosystem；模型稳定性/校准评估 | 生态数据分析与模型评估职责 | across ecosystem不等于按个人join，DAU也不定义身份粒度 |

两岗位发布者均为AppLovin官方Greenhouse；API的first_published分别为2026-02-18与2026-08-13，updated_at均为2026-11-05；采集日2026-11-20。日期是招聘元数据，不能回填为架构上线日。原文、完整时间及SHA256见[原始目录](production77/SOURCE_CATALOG.md)。两份是新URL、旧主题的补充，生产图谱结论未升级。

## 专利和整合材料的边界

已有US20130159103A1（S31/MA60S11/12），优先权2011-12-16、公开2013-06-20，Google档案状态为Abandoned。其应用列表→用户profile→广告选择是历史方案；不能当现代Axon图谱部署或价值模型输入。未重复获取，也不从过时实施例推导当前合法可用字段。

本轮AppLovin assignee及identity graph窄查询没有新增相关公报；查询覆盖有限，不证明其他专利不存在。云客户候选页返回soft404，猜测的Adjust收购完成URL404，均未收入技术证据。收购事实即使成立，也不自动给出Adjust身份结果流入Axon价值特征的映射。

既有IV74S09明确Axon广告因素可包含广告ID、设备与互动/购买历史。这是C_id官方用途披露，不因缺少图谱证据而抹去；本轮仅复用范围判断，未重搜隐私材料。广告ID被使用可以只是设备键，不等于自然人跨设备实体或图谱特征。

## Axon剩余断点及结论

尚缺合法可引用的：解析服务/版本、输出namespace及实体粒度、Axon实际接收、特征组与当时available_at、模型版本及实际读取trace。若要证明优势，还要身份开关对照中固定数据量、模型容量和竞价控制器；当前没有D层结果。

因此最强工程线索仍是“用户表示→广告模型研发职责”，新增的是竞价服务及评估职责。**没有生产身份图谱读取证据，没有独立增益证据。** 停止同义搜索；待具体一手架构文档或授权匿名审计包出现再恢复。完整竞争解释见[缺口报告](77_关键证据缺口与竞争解释.md)。
''',
'77_Vector身份图谱工程证据.md':'''# 77号：Vector身份图谱工程证据

2026-11-20。**核对3份明确属于Vector的官方工程岗位，其中2份已由旧证据覆盖，真正新增1份数据基础设施岗位；没有找到Vector生产价值模型读取个人跨App/跨设备身份解析结果的直接证据。C_graph和独立增益D仍UNKNOWN。** 不将岗位别名重新计算为新成果。

## Vector工程团队材料与别名去重

官方Unity careers页面的Next.js公开载荷列出129个职位，随后只读取3个相关Workday岗位。普通可见正文为空不代表岗位不存在；原始HTML内有JobPosting JSON-LD，描述及datePosted已保存，未登录、申请或调用身份接口。

| 证据 | 团队及日期 | 原文短摘录 | 正确结论 |
|---|---|---|---|
| 复用S30/MA60S19 / PE77C06，JOBREQ-2616596 | Vector Ads Modeling；2026-09-28 | Leverage rich user data and large-scale compute to validate models rapidly. | 用户行为建模/广告推荐研发职责明确对应Vector；未定义身份图谱输入 |
| PE77S04 / PE77C07，JOBREQ-2616462 | Vector Data Infrastructure；2026-11-13 | our platform also supports large-scale model training, feature generation, and experimentation workflows that power production ML systems. | 官方描述支持production ML的训练/特征平台；未给出身份输入列、join或消费模型 |
| 复用S28/MA60S20 / PE77C08，JOBREQ-2616286 | Vector Bidding Science / Vector AI org；2026-09-28 | ...bidding and pacing algorithms that automatically maximize advertisers’ returns. | 明确竞价/pacing团队和在线A/B职责；不是图谱特征已部署或收益证明 |

本轮HTML快照采集均为2026-11-20。PE77S03/05在实体去重时发现与旧CXS接口归档是同一JOBREQ，属于两次重复获取的执行偏差；保留快照但不计新增，主矩阵引用旧ID。字段datePosted不是模型上线日期。岗位用“productionalize research”“will develop”表述任务，不能直接写成已上线实现。Data Infrastructure对现有平台的陈述可作为官方团队架构描述，但不能升级为某项图谱特征生产消费。来源URL、正文位置及SHA256见[目录](production77/SOURCE_CATALOG.md)和[矩阵](77_生产身份图谱工程证据矩阵.csv)。

## 与既有用途披露如何连接

MA60S17（官方D7/D28文章，2026-06-25）已有原文：

> It uses both attributed data and unattributed data, like cross-game behavioral patterns and aggregate cohort insights, to distinguish between these player types at the moment of bid decision.

这确实说明Vector的跨游戏/cohort知识和bid-time用途，不能说完全没有用途证据。但cross-game behavioral patterns未定义为同一自然人记录；aggregate cohort insights明确也相容于非个人机制。新岗位的rich user data没有补充这些数据怎样关联、何时可用或具体由哪个线上模型读取。

不能把三岗位串起来便声称“身份解析服务→特征库→Vector报价器”已经恢复。训练数据基础设施、广告排序和竞价优化本来就可以由上下文、同App历史、聚合先验和共享参数驱动。

## 最近的身份组件线索属于Exchange，不属于Vector

IG72S05为2026-04-02官方Unity Exchange/RampID整合公告，明确美加库存的身份受众激活可用性及接收方支持条件。本轮复用，不重做伙伴名单。它比双方拥有相似ID字段更强，但实际接收产品是Exchange；没有Exchange→Vector特征表、模型版本及实际读取的桥接材料。

仍继承74号反误判：返回RampID可能只是derived输出，不代表已有实体匹配；maintained/derived必须区分；matchConfidence不是自动校准概率；月活设备数不是匹配人数。即使接收成功，也可能只支持第三方DSP受众激活，而非Vector价值预测。岗位未排除这一解释。

## 新专利：与身份图谱的实质距离

PE77S06 / PE77C11，US12353873B2，标题为Methods circuits devices systems and functionally associated machine executable code for recommendation and distribution of digital content。

- 发明人：Arnon Harish、Sagi Ben Basat；申请号US17/301,134。
- Google公报所列优先权2015-08-11、申请2021-03-26、授权/公开2025-07-08。
- Current Assignee同时列IronSource Ltd和Unity Technologies SF，Original Assignee列Unity Technologies SF；事件表记录2021-12-09向IRONSOURCE LTD.转让。保留原始元数据，不凭此重建产品整合史或作法律意见。
- 状态显示Active，Google明确提示状态/权利人可能不准确，本研究未独立法律核验。
- 共20项权利要求；独立项1为系统、7为方法、12为计算机可读介质。权利要求正文围绕OS版本变化、应用inventory及附加信息来产生适配应用推荐。

设备监测/应用列表提供的是**专利方案中的设备上下文**，不说明跨设备个人图谱；也没有Vector、LTV输入列或生产模型消费。不能因专利属于相关公司且含device/recommendation就认定其为Vector身份架构。另一个窄查询命中的Polyspatial application interaction属于空间交互，未进入正证据矩阵。

## 判断

Vector最接近价值模型的工程材料是既有Ads Modeling的用户行为建模职责和新增Data Infrastructure的production ML特征管道描述；最接近身份组件的是既有Exchange/RampID合作。**两端都存在范围内的正证据，中间“Exchange/解析结果→Vector实际接收→当时模型读特征”仍缺失，不能拼接补齐。** 不排除个人机制，也无法排除聚合/共享参数解释。当前停止公开架构扩搜。
''',
'77_关键证据缺口与竞争解释.md':'''# 77号：关键证据缺口与竞争解释

2026-11-20。本轮保留6份工程正文快照，经实体去重真正新增4项（另2份为旧岗位的URL别名），但**零项生产身份图谱结论升级**。评估对象是Axon与Vector指定价值模型，不是广告行业是否普遍存在身份服务。

## 必须连接的三项及当前断点

| 公司 | 身份解析组件 | 实际接收产品 | 价值模型特征消费 | 缺口 |
|---|---|---|---|---|
| AppLovin | 特定个人/跨设备resolver、namespace及返回契约仍未知 | Axon有标识/历史类别用途；没有具体匹配结果接收审计 | 用户表示/特征研发岗位；无resolved feature读记录 | 三项尚未在同一可核对链上连接 |
| Unity | LiveRamp通用解析及Unity Exchange受众激活已有材料 | Exchange的官方可用性声明；非Vector实例接收 | Vector有跨游戏/cohort用途及具体ML团队；无图谱列消费 | Exchange与Vector之间缺接收/特征/模型桥 |

官方描述、岗位、专利、实际接收及实际消费分层保存。矩阵中的False表示“本项未证明”，不是“厂商不具备能力”；UNKNOWN保留尚未取得的事实，不把文档未提及当反证。

```mermaid
flowchart LR
  AL[AppLovin用户表示研发职责] --> AP[广告模型工程线索]
  AR[具体身份解析输出未知] -. 缺接收与namespace .-> AX[Axon价值模型特征]
  AP -. 缺具体图谱列与模型读trace .-> AX
  LR[LiveRamp身份服务契约] --> UE[Unity Exchange官方激活可用]
  UE -. 未证明Vector接收 .-> VF[Vector身份特征]
  VD[Vector训练与特征平台职责] -. 未给出图谱列 .-> VF
  VG[跨游戏模式与聚合cohort官方用途] --> VV[Vector bid-time用途类别]
  VF -. 缺指定模型消费 .-> VV
```

实线限于声明范围内的职责/契约/用途，不表示本项目观察过生产接收。虚线标示待证断点。

## 竞争解释与可区分材料

| 表面观察/工程措辞 | 图谱解释 | 同样相容的解释 | 真正有区分力的下一份材料 |
|---|---|---|---|
| user representations、rich user data | 个人图谱embedding | 设备内序列、同App特征、上下文/群体embedding | resolver输出类型→特征组的明确血缘及实际读取审计 |
| across ad and app ecosystem | 跨App个人历史被join | 各产品独立表、汇总分析、共享训练参数 | 实体粒度、namespace、join键语义与合法接收记录 |
| feature generation、production ML | 图谱列上线 | 任意训练/特征管道 | 非PII字段字典、available_at、graph/model版本及线上消费trace |
| bidding、pacing、marketplace intelligence | 图谱提高报价 | 市场价格预测、预算控制、库存/频控改进 | 固定控制器的身份特征消融；再另做策略对照 |
| RampID可用于Exchange | Vector使用个人关系 | 仅外部买方受众激活或Exchange透传 | 明确Vector接收和resolved feature物化/读取证明 |
| 专利里的应用列表与推荐 | 已部署跨游戏个人模型 | 未上线方案；OS兼容或设备库存推荐 | 独立实现/部署证据及实际产品映射，不能再靠其他专利拼接 |

这些替代解释目前没有被排除；也没有证据排除个人关联机制存在。H0/H3按75号训练来源/在线依赖分别界定，不能仅因预测相近选出唯一机制。76号D1与上下文泄漏输出相同的工程反例仍适用：观察响应变化不定位数据路径。

## 最小补证包

1. **身份与接收包**：系统/产品名、合法用途、namespace、设备/账号/人/家庭粒度、maintained/derived及匹配成败、冲突/重置/撤销、接收时间和版本。匿名schema说明能力；授权审计才说明实际接收。
2. **消费包**：源记录引用、available_at、特征组/图谱/模型版本、实际读取及decision trace。必须是指定Axon或Vector价值模型，不能用Exchange或泛称广告模型替代；时间与权限需像76号契约一样可核验。
3. **独立增益包**：合法真实成熟收入/完整分母、等样本/等容量/等计算/等策略的个人特征开关对照，并测试错误匹配与关系漂移。预测改善也不自动等于真实盈利，获客成本和增量收益需另证。

研究不需要也不申请PII、真实用户重识别或导出个人图谱。材料须可合法引用；本轮未发送申请、签NDA、查询身份或测试生产接口。

## 证据不足与真正反证

招聘未提graph只是缺失；专利未提Vector只限制其证明范围；搜索0命中和URL失败不是图谱不存在的反证。只有具明确范围/日期的排除性架构说明、授权feature lineage/消费审计或固定条件实验，才可能排除特定实现/效果。即便某模型版本未读取图谱，也不能外推所有产品、国家和时期。
''',
'77_最终判断与停止条件.md':'''# 77号：最终判断与停止条件

2026-11-20。**没有取得直接证据证明Axon或Vector的生产价值模型实际读取跨App或跨设备身份图谱特征。本轮C_graph零突破；不等于证明它们没有图谱。**

## 最接近结论的工程证据

| 平台 | 当前最接近的工程材料 | 还缺哪一环 |
|---|---|---|
| Axon | 已有AppLovin用户信号/表示岗位S25/MA60S06把user representations连到广告模型研发和production职责；新增PE77S01补充低延迟竞价模型训练/服务 | 未指定身份解析组件、实体粒度、跨App匹配输出及Axon模型实际读取；岗位不等于部署 |
| Vector | 既有Vector Ads Modeling S30/MA60S19与新增训练/特征平台PE77S04明确对应产品；已有MA60S17说明bid-time跨游戏模式/cohort用途；IG72S05明确Exchange/RampID激活可用 | 没有解析结果→Vector实际接收→特征组/available_at→模型版本/读取trace；Exchange不能替代Vector |

三类命题不能混同：标识/历史因素类别用途已有官方正证据C_id；特定图谱结果入模C_graph仍UNKNOWN；超出聚合统计/共享参数的身份独立增益D仍UNKNOWN。不能因Unity披露更多岗位而判断其技术更强，也不能用AppLovin跨应用组合用途替代图谱消费链。

## 本轮实际覆盖

- 保留21份公开GET响应及采集时间/哈希。读取AppLovin官方列表45个岗位；复用旧用户表示/数据基础设施岗位，仅新增2份详情。Unity官方公开载荷129个岗位，仅跟进3个明确Vector团队详情。
- 6份正文快照按job ID/公开号去重后真正新增4项：3份官方岗位、1份专利。Vector的Ads Modeling/Bidding两份HTML实际已由旧CXS正文覆盖，属于本轮重复获取偏差，保留记录但排除新增。12行主矩阵包含4行新来源与8行复用证据；“新来源”不按突破计数。
- 专利核到US12353873B2完整正文、元数据及20项权利要求，独立项1/7/12为OS变化与应用推荐，不是Vector身份图谱。旧AppLovin专利复用，无重复下载。
- 4个论文元数据窄查询没有准入官方工程论文；一个Unity窄查询命中空间交互专利，未误收为身份图谱。两云客户页soft404、两个收购候选URL404，未当工程证据。

这不是穷尽互联网/专利家族/会议资料的检索结论。失败页面、空可见正文和0结果均不作否定证据；完整边界见[SEARCH_COVERAGE](production77/SEARCH_COVERAGE.json)。所有新增证据可溯原URL、原始响应、提取文本和SHA256。

## 停止与恢复

当前停止旧SDK扫描、旧伙伴名单/隐私政策复搜、招聘同义词扩搜和泛化架构搜索；不开展新合成实验或本地mock。没有新证据时继续增加材料数量不会改善可识别性。

仅在出现以下具体材料之一时恢复：

1. 一手架构/技术演讲明确命名解析组件、接收产品和价值模型特征映射，且区分上线与设计。
2. 权利方允许引用的匿名接收/特征消费审计，含用途、namespace、实体粒度、时间、版本和actual read；不用真实个人值。
3. 真实授权数据上的固定条件身份特征消融，能够与等数据群体学习比较。消费和效果分别判断，不能由效果反推唯一架构。

本轮未进行SDK扫描、隐私泛搜、身份服务伙伴列表整理、合成或mock开发、真实广告请求、身份查询、生产后台访问、个人数据采集及对外申请发送。00—76历史文件以冻结哈希核验；主索引/主图只追加，旧对象保留。

## 交付与核验

[12行工程矩阵](77_生产身份图谱工程证据矩阵.csv)、[Axon](77_Axon身份图谱工程证据.md)、[Vector](77_Vector身份图谱工程证据.md)、[竞争解释与缺口](77_关键证据缺口与竞争解释.md)。[原始目录](production77/SOURCE_CATALOG.md)、[来源记录](production77/SOURCE_EVIDENCE.json)、[验证](production77/VALIDATION.json)与[产物清单](production77/ARTIFACT_MANIFEST.json)支持复核。

下一步最有价值的是取得合法匿名的“解析结果→指定产品接收→价值特征读取”审计包，先补消费链；不是再搜一个identity graph词条。本轮未取得这份材料，明确报告零突破。
'''}
for name,content in reports.items(): write(R/name,content)

node_specs=[('al_jobs','AppLovin representation and bidding infrastructure job clues;not graph deployment'),
 ('v_jobs','Explicit Vector modeling,data infrastructure and bidding team descriptions;not graph feature reads'),
 ('patent','Unity/ironSource OS-specific application recommendation patent;not Vector graph proof'),
 ('missing','Specific resolver -> actual Axon/Vector receiver -> production identity feature consumption UNKNOWN'),
 ('stop','Round77 zero C_graph upgrades;stop repeated public searches')]
nodes=[dict(id='PE77N_'+a,label=b,stage='public_engineering_evidence_review',contains_real_personal_data=False) for a,b in node_specs]
edges=[]
for i,(a,b,sids,claim_text) in enumerate([
 ('al_jobs','missing',['S25','S26','PE77S01','PE77S02'],'Official ML team duties do not identify graph resolver,Axon feature lineage or actual reads'),
 ('v_jobs','missing',['S30','S28','PE77S04','MA60S17'],'Vector teams and cohort use disclosure do not establish resolved identity feature consumption'),
 ('patent','missing',['PE77S06'],'OS/app-inventory recommendation patent is a scheme,not Vector identity model deployment'),
 ('missing','stop',['IG72S05','IV74S09','EN76S04'],'Keep category-use positives and Exchange scope;C_graph and independent gain remain UNKNOWN')],1):
    edges.append(dict(id=f'PE77E{i:02}',source='PE77N_'+a,target='PE77N_'+b,source_ids=sids,claim=claim_text,
      status='unknown',evidence_level='D indirect jobs/patent;legacy official disclosures limited to named scope',
      reviewed_utc=NOW,production_actual_proven=False,production_match_proven=False,prediction_model_consumption_proven=False,
      independent_real_identity_lift_proven=False,evidence_stages=[],
      six_layers={k:False for k in ['sdk_capability','actual_game_business_callsite','request_construction_code','production_successful_send','server_received','server_model_training']},
      missing_evidence=gap))
g=load(D/'EVIDENCE_GRAPH.before.json')
admitted_sources=[s for s in sources if s['new_url']]
g['nodes'].extend(nodes);g['edges'].extend(edges);g['sources'].extend(admitted_sources)
g['production_identity_engineering_round77']=dict(reviewed_utc=NOW,source_catalog='production77/SOURCE_EVIDENCE.json',
 coverage='production77/SEARCH_COVERAGE.json',matrix=matrix_name,reports=list(reports),new_node_ids=[n['id'] for n in nodes],
 new_edge_ids=[e['id'] for e in edges],new_sources=[s['id'] for s in admitted_sources],c_graph_upgrades=0,
 Axon_C_graph='UNKNOWN',Vector_C_graph='UNKNOWN',independent_identity_gain='UNKNOWN',
 verdict='No direct production identity graph feature consumption evidence obtained;not evidence graphs do not exist')
graph_path=R/'prediction-system/EVIDENCE_GRAPH.json'
assert sha(graph_path)==history['prediction-system/EVIDENCE_GRAPH.json']
graph_path.write_text(json.dumps(g,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
addition='''

## 77号：生产身份图谱工程证据（2026-11-20）

结论：**Axon/Vector生产价值模型读取跨App/跨设备身份图谱特征仍UNKNOWN；C_graph零突破。** 真正新增3份官方岗位及1份专利，不能升级为部署；另2份Vector岗位为旧URL别名重复获取，已排除新增。Vector训练特征管道有团队描述，但Exchange/RampID不能推成Vector消费；AppLovin用户表示岗位仍不指定解析组件。

| 交付 | 内容 |
|---|---|
| [77_生产身份图谱工程证据矩阵.csv](77_生产身份图谱工程证据矩阵.csv) | 12行：4新来源、8复用；URL/日期/摘录/SHA256/粒度/消费断点 |
| [77_Axon身份图谱工程证据.md](77_Axon身份图谱工程证据.md) | 用户表示、竞价基础设施与图谱消费的界限 |
| [77_Vector身份图谱工程证据.md](77_Vector身份图谱工程证据.md) | 明确Vector岗位、OS推荐专利及Exchange范围 |
| [77_关键证据缺口与竞争解释.md](77_关键证据缺口与竞争解释.md) | 组件→接收产品→模型消费缺口与非图谱解释 |
| [77_最终判断与停止条件.md](77_最终判断与停止条件.md) | 零突破、搜索覆盖与恢复条件 |

[原始目录](production77/SOURCE_CATALOG.md)、[21份GET记录](production77/FETCH_MANIFEST.json)、[搜索边界](production77/SEARCH_COVERAGE.json)、[完整性验证](production77/VALIDATION.json)。未新增SDK扫描、模拟、mock、身份查询或生产请求。00—76共143份编号文件及76产物哈希核验保留；主图仅追加5节点/4边/4来源，旧288/345/635对象及旧元数据不变。
'''
index_path=R/'EVIDENCE_INDEX.md'
assert sha(index_path)==history['EVIDENCE_INDEX.md']
index_path.write_bytes((D/'EVIDENCE_INDEX.before.md').read_bytes()+addition.encode('utf-8'))
print(json.dumps(dict(new_sources=len(admitted_sources),primary_snapshots=len(sources),claims=len(rows),c_graph_upgrades=0,new_nodes=len(nodes),new_edges=len(edges)),ensure_ascii=False))
