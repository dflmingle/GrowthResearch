"""First-round architecture evidence, exact excerpts and bounded claims."""
from pathlib import Path
import copy,csv,datetime,hashlib,json,re
from bs4 import BeautifulSoup

R=Path(__file__).resolve().parent.parent;O=R/'model-architecture'
NOW=datetime.datetime.now(datetime.timezone.utc).isoformat()
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
g=load(O/'EVIDENCE_GRAPH.before60.json');prior={s['id']:s for s in g['sources']}
sources=[];claims=[]

def add(ident,company,product,path,a,b,claim,quote,level,scope,deploy,limits,origin=None,url=None,date=None,kind=None):
    p=R/path;lines=p.read_text(encoding='utf-8-sig').splitlines()
    ref=prior.get(origin,{})
    if ref:assert sha(p)==ref['sha256'],f'Prior source changed: {origin}'
    url=url or ref.get('url');date=date or ref.get('source_date') or 'not stated; reviewed 2026-11-19'
    assert 1<=a<=b<=len(lines),(ident,len(lines),a,b)
    excerpt='\n'.join(f'{i}: {lines[i-1]}' for i in range(a,b+1))
    assert quote in '\n'.join(lines[a-1:b]),f'Quote missing: {ident}'
    record=dict(id=ident,company=company,product=product,path=path,sha256=sha(p),url=url,source_date=date,
      start_line=a,end_line=b,excerpt=excerpt,short_quote=quote,claim=claim,evidence_level=level,
      applicable_product=scope,production_deployment_statement=deploy,limits_and_counterevidence=limits,
      evidence_kind=kind or ('job' if 'job-' in path else 'official product/integration document'),
      original_source_id=origin,reviewed_utc=NOW,
      production_actual_proven=False,independent_production_audit=False,
      observed_target_game_delivery=False,server_model_training=False)
    if origin:
        for k in ['official_package','official_packages','sdk','version','class_or_method','public_source','raw_origin','raw_locator']:
            if k in ref:record[k]=copy.deepcopy(ref[k])
    if path.startswith('model-architecture/public/'):
        meta=load(p.with_suffix('.meta.json'));raw=R/meta['raw_path'];assert sha(raw)==meta['sha256']
        record['fetch_provenance']=meta
        soup=BeautifulSoup(raw.read_bytes(),'html.parser')
        record['page_dates']={m.get('property',m.get('name')):m.get('content') for m in soup.find_all('meta')
            if re.search('date|time|publish',m.get('property',m.get('name','')),re.I)}
    sources.append(record)
    claims.append(dict(id=ident,company=company,product=product,publication_date=date,original_url=url or '',
      local_file=path,sha256=record['sha256'],start_line=a,end_line=b,short_quote=quote,technical_claim=claim,
      applicable_product=scope,evidence_level=level,explicit_production_deployment=deploy,
      evidence_kind=record['evidence_kind'],counterevidence_and_unknowns=limits,original_source_id=origin or ''))

OFF='【官方公开证实】';IND='【间接技术线索】';SDK='【SDK代码证实】'
add('MA60S01','AppLovin','Axon 2','model-architecture/public/al-business.txt',31,34,
 '官方称Axon2已于2023-04推出，预测互动/转化/支付/金额/复购，并预测未来多日的价值分布用于实时资本配置',
 'These models now predict expected value distributions many days into the future',OFF,
 'Axon2；原段重点解释游戏玩家对非游戏offer的价值评估，不证明每种手游目标都有相同预测头',
 'vendor states rollout April 2023 and current prediction; not independently audited',
 'CEO署名产品/商业解释，不公开概率分布族、独立heads、loss、参数量、特征表或四款游戏使用。',
 url='https://www.applovin.com/en/blog/applovin-business-model',date='2026-02-02; metadata modified 2026-07-28',kind='official CEO product/technical assertion')
add('MA60S02','AppLovin','Axon','nongame/applovin-axon-about.txt',54,73,
 '官方明确模型持续训练优化的数据类别、广告主特定展示价值出价及排除项',
 'train and optimize on a continual basis',OFF,'Axon总体，不是特定游戏字段血缘',
 'vendor describes current model data use and bidding',
 '不公开每字段join、模型结构、训练频率；排除其他bidder出价/用户数据、敏感/受保护/儿童数据。',origin='S01')
add('MA60S03','AppLovin','AppLovin AppsFlyer partner','axon/doc-appsflyer.txt',183,241,
 'all-source含organic事件共享，landing/checkout/postinstall和金额口径有不同配置',
 'All media sources, including organic',OFF,'MMP后台契约，非MAX EventService直发',
 'supported integration; target-game activation unknown',
 '未证后台启用或训练；checkout明确排除广告收入/预测LTV。',origin='CGS49')
add('MA60S04','AppLovin','AppLovin Ads / Axon','model-architecture/public/al-introducing.txt',27,50,
 '官方称实时评估展示并按return goals出价；前瞻声明更多广告主的增量数据将改善游戏伙伴效果',
 'the incremental data will materially improve AppLovin Ads',OFF,
 '平台扩展方向；不是游戏/电商逐字段共享契约',
 'real-time bidding present tense; cross-category benefit is forward-looking will/believe',
 '不能据此认定电商订单默认进入某手游模型或单一共享网络；无独立数据消融。',
 url='https://www.applovin.com/en/blog/introducing-applovin-ads',date='2025-10-01; metadata modified 2026-07-15',kind='official CEO announcement; forward-looking data benefit')
add('MA60S05','AppLovin','Discovery / Prospecting','model-architecture/public/al-discovery.txt',21,36,
 '电商Discovery与Prospecting使用同一历史购买数据，区别新访客/新买家目标',
 'uses the same historical purchase data',OFF,'电商获客，不自动适用于手游IAA',
 'official product launch and setup instructions',
 '可证历史购买作为产品输入，未公开身份join、模型、gaming迁移或线上增量。',
 url='https://www.applovin.com/en/blog/discovery-campaigns',date='2026-02-25; metadata modified 2026-07-28',kind='official product post by Member of Technical Staff')
add('MA60S06','AppLovin','Advertising platform research','prediction-system/applovin-job-4712559006-clean.txt',8,21,
 '招聘职责涉及用户表示、ranking/retrieval、feature interaction和multi-task learning',
 'representation learning, feature interaction, and multi-task learning',IND,'AppLovin广告平台招聘，未明确Axon版本',
 'research/development duties, not architecture deployment proof',
 'explore/develop及技能不证明已部署embedding/MMoE/Transformer或跨App用户图谱。',origin='S25')
add('MA60S07','AppLovin','ML data infrastructure','prediction-system/applovin-job-4716524006-clean.txt',8,21,
 '职责涉及model training和feature serving数据管道、traceability；feature store是加分项',
 'model training and feature serving',IND,'AppLovin ML平台职责，非Axon专属源码',
 'team engineering duties; concrete system implementation unknown',
 '不能据此确定已部署某feature store、Spark/Flink链路、更新周期或真实数据源。',origin='S26')
add('MA60S08','AppLovin','Ad Review vs Axon','prediction-system/applovin-excluded-rival-data.txt',14,17,
 '官方明确Ad Review不建立用户/设备画像，不供给Axon或其他模型',
 'Axon',OFF,'Ad Review数据用途排除，不排除广告主授权的自身收入反馈',
 'explicit official exclusion',
 '禁止由MAX适配器或其他网络广告输出推断竞争者用户/报价进入Axon。',origin='S24')
add('MA60S09','AppLovin','Ad ROAS / Blended ROAS','axon/gaming-apps.txt',20,40,
 '产品明确以玩家长期广告收入/IAP/Hybrid价值优化，并将MAX变现与获客关联',
 'maximizing player lifetime ad revenue',OFF,'游戏获客目标与产品关系',
 'officially offered product, not per-game selected objective',
 '不公开IAA窗口、每行训练表、收入精度处理或实际效果。',origin='CGS54')
add('MA60S10','AppLovin','IAP revenue sharing','axon/doc-in-app-purchase-revenue-sharing.txt',13,26,
 'IAP/checkout只允许真实用户支付，排除IAA、预测收入和预测LTV',
 'Predicted revenue or predicted LTV',OFF,'AppLovin IAP共享口径，不是IAA通道',
 'documented revenue contract',
 '代理value不能伪装真实purchase；该契约不证明后台验单/退款处理。',origin='CGS52')
add('MA60S11','AppLovin','Historical patent metadata','prediction-system/applovin-historical-patent.txt',28,84,
 'US20130159103A1优先权2011-12-16；申请人Applovin Corp；Google Patents列Abandoned',
 '2011-12-16',IND,'2011/2013专利构想，不是现代Axon部署',
 'patent publication only; no deployment or current legal opinion',
 'Google状态非法律意见；现代权限/数据排除不被早期专利覆盖。',origin='S31',kind='historical patent metadata')
add('MA60S12','AppLovin','Historical patent claims','prediction-system/applovin-historical-patent.txt',1595,1721,
 '42项公开权利要求；独立1/15/29覆盖由App存在/身份/使用及特征产生用户画像的流程/系统/存储介质',
 'A computer-implemented process to generate a user profile',IND,'US20130159103A1权利要求范围',
 'published claim text, not granted/deployed Axon design',
 '专利demographics等示例不能套用当前Axon；无LTV训练网络/label/实时CPM公式证据。',origin='S31',kind='historical patent claims')
add('MA60S13','Unity','Vector D28 IAA / Hybrid','vector/d28-blog.txt',15,43,
 '官方明确预测每用户28天广告收入并按国家tROAS动态出价；Hybrid优化组合28天收入',
 'predicts each user’s likely ad revenue over 28 days',OFF,'2026-05 D28 IAA/Hybrid产品，不是无限生命周期',
 'official product launch and closed-beta aggregate results',
 '未公开预测头/收入样本构造；配对beta非本研究随机实验，不能量化架构贡献。',origin='S22')
add('MA60S14','Unity','Unity Ads ROAS learning','vector/doc-roas-campaign-best-practices.txt',36,70,
 '官方明确预启动至少两周SDK数据及未归因事件有助训练，未计入学习阈值；建议全来源和Lifetime窗口',
 'helps to train the machine learning models',OFF,'同一广告主App跨来源样本；非跨广告主个人轨迹',
 'explicit training-purpose contract; no target-game activation',
 '未给逐字段训练血缘、样本权重、回填范围或增益；自然量与付费分布可不同。',origin='CGS42')
add('MA60S15','Unity','Unity Ads ROAS cohorts','vector/doc-intro-to-roas-campaigns.txt',79,116,
 '成熟cohort与IAA/IAP/Hybrid学习门槛公开；D28退出门槛用D7成熟数据',
 '75 unique, D7 matured purchasers',OFF,'ROAS学习退出条件，不是模型全部训练样本或D28已成熟',
 'documented optimization product behavior',
 '零收入负例采样、迟到/退款/去重/损失函数未知。',origin='CGS47')
add('MA60S16','Unity','Vector IAP D7 / D28','model-architecture/public/unity-d7-d28.txt',145,176,
 '官方说明IAP optimizers预测购买/价值并动态出价，D7/D28窗口学习速度不同',
 'use machine learning to predict which users are most likely to make purchases',OFF,'D7/D28 IAP产品级预测说明',
 'present-tense product description; architecture not disclosed',
 '不证明独立pPurchase head或多任务共享层；D28不等于无限LTV。',
 url='https://unity.com/blog/d7-vs-d28-iap-roas-campaigns',date='2026-06-25; sitemap lastmod 2026-10-26',kind='official product explanation by Senior Content Marketing Manager')
add('MA60S17','Unity','Vector bid-time player/game intelligence','model-architecture/public/unity-d7-d28.txt',208,223,
 '官方明确attributed/unattributed数据，包括cross-game behavioral patterns和aggregate cohort insights，在bid decision时区分玩家类型',
 'cross-game behavioral patterns and aggregate cohort insights',OFF,'Vector IAP D7/D28产品用途，字段/作用域不公开',
 'vendor states current bid-decision use; not independently audited',
 '未说明参数共享/聚合统计/个人级ID各占何角色；38%统计样本期2024-04到2025-02，不是Vector因果提升实验。',
 url='https://unity.com/blog/d7-vs-d28-iap-roas-campaigns',date='2026-06-25; cited data period 2024-04 to 2025-02',kind='official specific data-use assertion; not model implementation paper')
add('MA60S18','Unity','Vector Gamer AI inference','prediction-system/unity-job-JOBREQ-2615964-clean.txt',1,24,
 'Vector Gamer AI负责广告排序/竞价，招聘陈述运行低延迟高吞吐online model inference平台',
 'large-scale online model inference',IND,'明确归属Vector的团队生产职责',
 'job describes current production responsibility; implementation not independently verified',
 'Triton仅加分项；不证明实际模型、时延SLA、特征或跨App匹配。',origin='S29')
add('MA60S19','Unity','Vector Ads Modeling','prediction-system/unity-job-JOBREQ-2616596-clean.txt',1,13,
 'Vector Modeling招聘涉及用户行为建模、rich user data和research→production',
 'user behavior modeling',IND,'Vector建模团队研发方向',
 'research roadmap and candidate qualifications, not deployed architecture',
 '不证明Embedding/Transformer/多任务/跨游戏共享网络或具体输入。',origin='S30')
add('MA60S20','Unity','Vector Bidding Science','prediction-system/unity-job-JOBREQ-2616286-clean.txt',1,23,
 'Vector竞价团队职责涉及bidding/pacing、bid landscape forecasting与offline/online评估',
 'bidding and pacing algorithms',IND,'Vector竞价系统研发职责',
 'development duties; next-generation systems not deployment proof',
 'RL/control theory及survival analysis属技能项，不能写成已部署算法。',origin='S28')
add('MA60S21','Unity','Vector correlations and ecosystem','vector/unity-vector-correct.txt',10,15,
 '产品披露game DNA/real behavior、IAP和广告行为相关性及生态数据/新训练方法',
 'correlations between IAP and ad behavior',OFF,'产品层关联建模用途，不是多任务网络结构',
 'public product claim',
 '不证明共用embedding或跨应用个人身份；potential不等于每款引擎游戏默认供数据。',origin='CGS53')
add('MA60S22','Unity','IAP / D2C to Vector','vector/unity-2026-keynote.txt',120,121,
 'Unite回顾明确IAP SDK/D2C购买数据可以丰富Vector',
 'Vector',OFF,'IAP/D2C产品数据用途连接，不是字段级训练表',
 'official can-help-enrich statement; per-event deployment unknown',
 '没有因此补齐Insights native接收→训练label，四款实际启用未知。',origin='S21')
add('MA60S23','Unity','Developer Data consent','vector/ddf-end-user-consent.txt',14,38,
 'Developer Data的analytics_intent与ads_intent用途独立，默认未知状态ads_intent=denied',
 'ads_intent = denied',OFF,'Developer Data框架，不自动覆盖各SDK所有读操作',
 'documented consent/usage contract',
 '可采集不等于可用于个性化广告；不能推断所有Runtime数据默认训练Vector。',origin='S20')
add('MA60S24','Unity','IAP5.5.1 Insights forwarding','cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/Insights/PurchaseEventEmitter.cs',188,239,
 'IAP protobuf的gateway/runtime转发分支可见，闭源native接收后的训练用途仍未知',
 'Forward',SDK,'官方IAP5.5.1独立包，不是四款游戏启用证据',
 'client code only; no production invocation',
 '不能由API存在证明收入验真、退款、送达/ACK或Vector训练。',origin='C53S23')
add('MA60S25','Unity','Unity Ads4.17 prebid history','ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/domain/AndroidBuildHeaderBiddingToken.kt',33,89,
 'Token外层明确写入sessionCounters、campaignState与HB seq/wins/starts',
 'campaignState = campaignRepository.getCampaignState()',SDK,'4.17源码；4.18所选外层对照见既有56',
 'serialization code only, not model-feature ingestion',
 '不能解出不透明内层或跨App轨迹；bid_time新鲜度和特征增益未知。',origin='CGS01')
add('MA60S26','Unity','MMP S2S revenue association','vector/doc-send-postbacks.txt',28,109,
 'S2S公开身份、广告主/活动、安装/事件时间、归因标记与收入字段契约',
 'game_id',OFF,'MMP→Unity接收契约',
 'interface capability, no observed matching/production receipt',
 '同包ID不等于join成功；受隐私/可用性限制，publisher ID不替代advertiser ID。',origin='CGS48')
add('MA60S27','AppLovin','Incrementality and measurement','model-architecture/public/al-measurement.txt',20,41,
 '官方强调归因报告/MTA/MMM/增量实验不是同一量，测试受holdout和预算稳定等条件约束',
 'not measuring the same thing',OFF,'电商测量讨论，用于限制收益因果外推',
 'measurement-method statement; no raw experiment dataset',
 '90% power是设计目标声明，不证明测试实际功效；不能套用四款或把相关提升当增量。',
 url='https://www.applovin.com/en/blog/measurement-lens',date='2026-06-16',kind='official measurement article')
add('MA60S28','AppLovin','Creative and targeting','model-architecture/public/al-silos.txt',40,46,
 '官方说明素材及目标转化事件影响模型匹配，限制把全部增长归因于身份/模型架构',
 'Our models match the right user to the right ad relative to the conversion event',OFF,'AppLovin电商品牌运营语境',
 'product/operating description, not feature-level deployment proof',
 '女性/代际素材例子不是使用年龄/性别字段训练的证据；不得覆盖Axon明确排除项。',
 url='https://www.applovin.com/en/blog/silos-performance',date='2026-04-30',kind='official business-development article')

save(O/'SOURCE_EVIDENCE.json',sources)
with (O/'CLAIM_MATRIX.csv').open('w',encoding='utf-8-sig',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=list(claims[0]));writer.writeheader();writer.writerows(claims)
cat=['# 模型架构证据来源目录','','本轮为60号第一轮；公开产品声明、SDK可见路径、招聘/专利分别分级。官方发布不等于独立验证生产实现。所有quote均与本地原文逐字核验。','']
for s in sources:
    cat += [f'<a id="{s["id"].lower()}"></a>',f'## {s["id"]} · {s["company"]} / {s["product"]}','',
      f'- 原始URL：{s["url"] or "官方包来源见原包provenance"}',
      f'- 原始文件：[{s["path"]}:L{s["start_line"]}](../{s["path"]})；范围L{s["start_line"]}—L{s["end_line"]}',
      f'- 日期：{s["source_date"]}；查阅：{s["reviewed_utc"]}',
      f'- SHA256：`{s["sha256"]}`',
      f'- 短摘录：> {s["short_quote"]}',f'- 主张：{s["evidence_level"]} {s["claim"]}',
      f'- 产品范围：{s["applicable_product"]}',f'- 部署证据：{s["production_deployment_statement"]}',
      f'- 限制/反证：{s["limits_and_counterevidence"]}','']
    if 'fetch_provenance' in s:
        m=s['fetch_provenance'];cat += [f'原始HTTP文件：[{m["raw_path"]}](../{m["raw_path"]})；SHA256 `{m["sha256"]}`。','']
    if s.get('original_source_id'):cat += [f'复用既有证据：{s["original_source_id"]}；保持旧对象不变。','']
(O/'SOURCE_CATALOG.md').write_text('\n'.join(cat),encoding='utf-8')

patent=dict(publication='US20130159103A1',title='Advertisement Selection Based on Mobile Applications',
 applicant_as_original_assignee='Applovin Corp',current_assignee_as_indexed='Applovin Corp',
 inventors=['Adam Foroughi','John Krystynak','Andrew Karam','Furqan Rydhan','Matthew Bornski'],
 priority_date='2011-12-16',filing_date='2012-12-14',publication_date='2013-06-20',
 indexed_status='Abandoned; Google Patents disclaimer, not a legal opinion',claims_count=42,
 independent_claims={'1':'computer-implemented profile generation process','15':'profile generation system','29':'computer-readable storage medium'},
 claim_scope='mobile application presence/identity/usage + app characteristic -> demographics/preferences/interests/propensity profile; dependent claims add targeting/storage/etc',
 evidence=['MA60S11','MA60S12'],production_deployment_proven=False,modern_axon_model_architecture_proven=False,
 unity_patent_scope='No newly validated Unity/Vector-specific model patent obtained this round; absence not proven')
save(O/'PATENT_RECORDS.json',[patent])

# Log all search/fetch outcomes, including misleading HTTP200 shells and irrelevant results.
ledger=[]
for p in sorted((O/'public').glob('*.meta.json')):
    x=load(p);ident=x['id'];classification='public page fetched; primary use requires exact cited content'
    if ident in ['axon-production','axon-representations','axon-engineering','vector-models','vector-conference','vector-research','axon-patent','unity-patent','axon-whitepaper','vector-embeddings','unity-d28','axon-architecture']:
        classification='Google HTTP200 JavaScript/search shell; no usable result list; not substantive evidence'
    elif ident.startswith('bing-'):
        classification='empty RSS or results irrelevant to architecture; not used as evidence'
    elif ident.startswith('yahoo-'):classification='HTTP403; stopped; no bypass'
    elif ident.startswith('ddg-'):classification='HTTP202 challenge; stopped; no bypass'
    elif 'sitemap' in ident:classification='URL discovery only; lastmod is not publication/deployment date'
    x['research_disposition']=classification;ledger.append(x)
save(O/'ACQUISITION_LEDGER.json',ledger)
print('Evidence matrix:',len(sources),'sources/claims; exact quotes validated; patent metadata/claims recorded.')
