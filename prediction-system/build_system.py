"""Evidence graph: disclosed use, static capability and observed production are separate."""
from pathlib import Path
import json,re,hashlib,datetime,html
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parent.parent;R=ROOT/'prediction-system'
NOW=datetime.datetime.now(datetime.timezone.utc).isoformat()
old=json.loads((ROOT/'EVIDENCE_MANIFEST.json').read_text(encoding='utf-8'))
origins={}
for e in old['entries']:
 for s in e.get('sources',[]):
  if s.get('path') and s.get('url'):origins[s['path']]=s
fetches=[x for p in R.glob('fetches-*.json') for x in json.loads(p.read_text(encoding='utf-8'))]
for p in (ROOT/'axon').glob('fetches-*.json'):
 for x in json.loads(p.read_text(encoding='utf-8')):
  for ext in ['html','txt']:origins['axon/'+x['id']+'.'+ext]=x
for x in fetches:
 for ext in ['raw','txt']:origins['prediction-system/'+x['id']+'.'+ext]=x
sources=[]
def excerpt(id,path,pattern,before=2,after=8,tier='A',url=None,date=None,product=None):
 p=ROOT/path;lines=p.read_text(encoding='utf-8').splitlines()
 hits=[i for i,x in enumerate(lines) if re.search(pattern,x,re.I)]
 if not hits:raise ValueError((id,path,pattern))
 i=hits[0];a=max(0,i-before);b=min(len(lines),i+after)
 meta=origins.get(path,{})
 d=dict(id=id,path=path,url=url or meta.get('url'),source_date=date or 'not stated; snapshot date is not publication date',
  acquired_utc=meta.get('utc',meta.get('fetched_utc')),reviewed_utc=NOW,product=product,
  evidence_priority=tier,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),start_line=a+1,end_line=b,
  excerpt='\n'.join(f'{j+1}: {lines[j]}' for j in range(a,b)))
 sources.append(d);return id
def code(id,catalog,key,product):
 a=next(x for x in json.loads((ROOT/catalog).read_text(encoding='utf-8')) if x['id']==key)
 d={**a,'id':id,'evidence_priority':'B','product':product,'source_date':'SDK version in path',
    'reviewed_utc':NOW,'url':None,'excerpt':a.get('text',a.get('excerpt',''))}
 sources.append(d)

# Reuse exact original snapshots, never mutate them.
excerpt('S01','nongame/applovin-axon-about.txt',r'What data does Axon AI use',2,15,product='Axon')
excerpt('S02','nongame/applovin-axon-about.txt',r'How does Axon AI work',0,7,product='Axon')
excerpt('S03','nongame/applovin-axon-about.txt',r'How does Axon AI continue',0,5,product='Axon')
excerpt('S04','nongame/applovin-policy-direct.txt',r'collected automatically across mobile apps',3,12,product='AppLovin services')
excerpt('S05','axon/gaming-apps.txt',r'Should I expect to grow',0,10,product='AppLovin Ads gaming')
excerpt('S06','axon/max-ilrd.txt',r'Impression-level user revenue API',0,24,tier='B',product='MAX')
excerpt('S07','axon/max-ilrd.txt',r'This precision takes',2,12,tier='B',product='MAX')
excerpt('S08','axon/doc-in-app-purchase-revenue-sharing.txt',r'Please only send revenue',0,15,product='AppLovin Ads MMP')
excerpt('S09','axon/doc-adjust.txt',r'Enable data sharing for AppLovin',0,35,product='Adjust / AppLovin')
excerpt('S10','axon/doc-appsflyer.txt',r'In-app event postbacks window',2,46,product='AppsFlyer / AppLovin')
excerpt('S11','nongame/doc-order-history.txt',r'model|high.value',2,12,product='Axon ecommerce')
excerpt('S12','vector/unity-vector-correct.txt',r'Vector AI goes beyond',1,7,product='Vector')
excerpt('S13','vector/unity-vector-correct.txt',r'Send attributed',2,8,product='Vector')
excerpt('S14','vector/doc-intro-to-roas-campaigns.txt',r'With a ROAS campaign',0,6,product='Unity Ads ROAS')
excerpt('S15','vector/doc-intro-to-roas-campaigns.txt',r'After you select your optimization',2,19,product='Unity Ads ROAS')
excerpt('S16','vector/doc-intro-to-roas-campaigns.txt',r'### Data cohorts and maturity',0,15,product='Unity Ads ROAS')
excerpt('S17','vector/doc-intro-to-roas-campaigns.txt',r'#### Learning phase thresholds',0,23,product='Unity Ads ROAS')
excerpt('S18','vector/doc-send-postbacks.txt',r'### User identification',0,13,tier='B',date='2026-01-30',product='Unity Ads custom S2S')
excerpt('S19','vector/doc-send-postbacks.txt',r'### Event identification',0,19,tier='B',date='2026-01-30',product='Unity Ads custom S2S')
excerpt('S20','vector/ddf-end-user-consent.txt',r'ads_intent',2,15,product='Developer Data Framework')
excerpt('S21','vector/unity-2026-keynote.txt',r'purchase data collected',0,2,date='2026-07-21',product='Unity IAP / D2C / Vector')
excerpt('S22','vector/d28-blog.txt',r'D28 Ad Revenue ROAS is designed',0,13,date='2026-05-21',product='Vector D28')
excerpt('S23','vector/d28-blog.txt',r'Based on internal Unity closed.beta',0,3,date='2026-05-21',product='Vector D28 paired evaluation')
excerpt('S24','prediction-system/applovin-excluded-rival-data.txt',r'We do not build user or device profiles',1,3,date='2026-09-16',product='AppLovin Ad Review / Axon exclusion')

# Extract job descriptions from original public JSON, preserving JSON pointers as locators.
jobs=json.loads((R/'applovin-public-jobs.raw').read_text(encoding='utf-8'))['jobs']
for id,jid in [('S25',4712559006),('S26',4716524006),('S27',4705264006)]:
 j=next(x for x in jobs if x['id']==jid);txt=html.unescape(j['content'])
 path='prediction-system/applovin-job-'+str(jid)+'-clean.txt'
 (ROOT/path).write_text(BeautifulSoup(txt,'html.parser').get_text('\n',strip=True),encoding='utf-8')
 pattern={4712559006:r'representation learning',4716524006:r'model training and feature serving',4705264006:r'triangulate'}[jid]
 excerpt(id,path,pattern,1,15,tier='D',url=j['absolute_url'],date='updated_at='+j['updated_at'],product='AppLovin advertising platform; not explicitly Axon')
 sources[-1]['raw_origin']='prediction-system/applovin-public-jobs.raw'
 sources[-1]['raw_locator']=f'jobs[id={jid}].content'
 sources[-1]['acquired_utc']=origins['prediction-system/applovin-public-jobs.raw'].get('utc')
for id,jid in [('S28','JOBREQ-2616286'),('S29','JOBREQ-2615964'),('S30','JOBREQ-2616596')]:
 path='prediction-system/unity-job-'+jid+'.raw';j=json.loads((ROOT/path).read_text(encoding='utf-8'))['jobPostingInfo']
 clean='prediction-system/unity-job-'+jid+'-clean.txt'
 (ROOT/clean).write_text(BeautifulSoup(j['jobDescription'],'html.parser').get_text('\n',strip=True),encoding='utf-8')
 excerpt(id,clean,r'The opportunity',0,28,tier='D',url=origins[path].get('url'),
  date='startDate='+str(j.get('startDate'))+'; postedOn='+str(j.get('postedOn')),product='Vector '+j['title'])
 sources[-1].update(raw_origin=path,raw_locator='jobPostingInfo.jobDescription',official_listing='https://unity.com/careers/positions?department=ai-machine-learning')
 sources[-1]['acquired_utc']=origins[path].get('utc')
excerpt('S31','prediction-system/applovin-historical-patent.txt',r'list of mobile applications installed',3,9,tier='D',date='priority 2011-12-16; publication 2013-06-20',product='AppLovin pre-Axon patent US20130159103A1')

code('S32','identity-graph/IDENTITY_CODE_EXCERPTS.json','MAX-device-payload','MAX 13.6.4')
code('S33','identity-graph/IDENTITY_CODE_EXCERPTS.json','MAX-cuid-manager','MAX 13.6.4')
code('S34','identity-graph/IDENTITY_CODE_EXCERPTS.json','UNITY-ads-idfi-auid','Unity Ads 4.17.0')
code('S35','identity-graph/IDENTITY_CODE_EXCERPTS.json','UNITY-ads-PII-gates','Unity Ads 4.17.0')
code('S36','auction/CODE_EVIDENCE.json','Unity-shared-data','Unity Ads 4.17.0')
excerpt('S37','vector/exchange-rampid.txt',r'RampID is now available across Unity Exchange in',1,18,product='Unity Exchange / LiveRamp',date='2026-04-02')
excerpt('S38','identity-graph/unity-player-accounts.txt',r'organization.level player pool',2,10,product='Unity Player Accounts')
excerpt('S39','20_Axon实际事件调用链.md',r'完整显式业务链',1,7,tier='B',product='Four game static audit; links to original SDK/DEX evidence')
excerpt('S40','10_买量优化机制最终对比.md',r'已证明预测未来LTV吗',1,8,tier='B',product='Four game static audit; not training-use evidence')

nodes=[];edges=[]
def node(id,label,company,stage):nodes.append(dict(id=id,label=label,company=company,stage=stage))
for c,p in [('AppLovin','A'),('Unity','U')]:
 for k,label,stage in [
  ('context','设备 应用 广告位 创意与广告互动','data_source'),('ids','受限标识及事件关联','association'),
  ('features','安装前特征处理与表示','feature_processing'),('labels','IAA IAP成熟价值标签','training_label'),
  ('predict','广告主特定价值预测','prediction'),('bid','动态出价与预算控制','bidding'),
  ('exchange','展示机会及拍卖','auction'),('feedback','自身互动及结果反馈','feedback'),
  ('mmp','授权MMP安装及后续事件','measurement'),('revenue','游戏实际IAA IAP','data_source')]:node(p+'_'+k,label,c,stage)
for id,label,c,stage in [
 ('A_max','MAX ILRD与变现请求','AppLovin','data_source'),('A_web','商家Pixel CAPI订单历史','AppLovin','data_source'),
 ('A_review','Ad Review其他网络用户级输出','AppLovin','excluded_source'),('A_rival','其他bidder出价及用户数据','AppLovin','excluded_source'),
 ('A_canonical','统一跨设备自然人图谱','AppLovin','unproven_association'),
 ('U_runtime','Runtime Developer Data','Unity','data_source'),('U_purchase','IAP SDK D2C购买数据','Unity','data_source'),
 ('U_accounts','Player Accounts登录身份','Unity','association'),('U_ramp','RampID Exchange受众激活','Unity','association'),
 ('U_ads','Ads请求 token及广告事件','Unity','data_source'),('U_canonical','UPA RampID与Vector统一用户图','Unity','unproven_association')]:node(id,label,c,stage)

def edge(id,src,dst,claim,status,refs,provider,receiver,conditions,missing,hypotheses=(),production='not independently observed',scope='platform capability'):
 levels={'official_use':'【官方公开证实】','sdk':'【SDK代码证实】','indirect':'【间接技术线索】','inference':'【合理推断】','unknown':'【无法确认】','excluded':'【官方明确排除】'}
 edges.append(dict(id=id,source=src,target=dst,claim=claim,status=status,evidence_level=levels[status],
  source_ids=refs,data_provider=provider,data_receiver=receiver,permission_conditions=conditions,
  production_actual_proven=False,production_evidence=production,applies_to=scope,
  missing_evidence=missing,hypotheses=list(hypotheses),reviewed_utc=NOW,
  diagram_style='solid' if status in ['official_use','sdk'] else 'barred' if status=='excluded' else 'dashed',
  observed_target_game_delivery=False))

edge('A01','A_context','A_predict','设备/网络及应用 广告 其他数字属性互动进入Axon训练优化','official_use',['S01'],
 'AppLovin与授权伙伴','Axon models','合法收集 伙伴权限及隐私选择','具体逐App联合样本 schema和安装前截断时间',['H1','H3'],production='official broad model-use disclosure; not audited logs')
edge('A02','A_context','A_ids','SDK按配置共封装广告ID AppSetID及限制跟踪信息','sdk',['S32'],
 'MAX collector','AppLovin SDK请求接收层','可用广告ID AppSet scope 配置开关及隐私限制','生产启用和服务端join',['H1'])
edge('A03','A_ids','A_features','关联历史可能形成安装前用户特征','inference',['S01','S04','S25'],
 'AppLovin授权数据处理','未公开特征管线','标识有效 scope合法 时间点早于出价','join键 时效 去重 快照schema',['H1','H3'])
edge('A04','A_features','A_predict','用户表示 多任务和特征服务为招聘中的工程方向','indirect',['S25','S26'],
 'AppLovin ML团队','广告推荐系统','公司级招聘范围 不等于Axon部署','Axon模型版本 特征登记和真实推断trace',['H3'])
edge('A05','A_revenue','A_max','展示收入可通过onAdRevenuePaid与precision返回','sdk',['S06','S07'],
 'MAX及变现网络','游戏收入回调','监听注册 有效展示 非测试 金额精度按字段解释','目标单展示送达及最终结算',['H2'])
edge('A06','A_max','A_mmp','ILRD可共享给MMP','official_use',['S06'],
 'MAX/游戏','获授权MMP','MMP集成和共享配置','目标游戏生产接收日志',['H2'])
edge('A07','A_revenue','A_mmp','真实用户付费通过purchase收入链','official_use',['S08','S09','S10'],
 '广告主/游戏','Adjust或AppsFlyer','真实支付 正确币种金额 授权','验单 退款 回调幂等及到账日志',['H2'])
edge('A08','A_mmp','A_labels','MMP按伙伴授权映射事件/收入到AppLovin','official_use',['S09','S10'],
 '授权MMP','AppLovin partner integration','partner启用 来源范围 事件映射 Lifetime窗口按指南','五款游戏后台开关与送达ACK；IAA不是checkout',['H2'],scope='supported integration, not target game activation')
edge('A09','A_max','A_predict','MAX与IAA ROAS产品有明确关联 但未公开标签内部表','official_use',['S05','S06'],
 '广告主授权MAX变现数据','AppLovin Ads Ad ROAS','live app MAX MMP 目标及素材','ILRD进训练表的逐字段映射 精度过滤及成熟窗口',['H2','H4'],production='official product description, not row-level training evidence')
edge('A10','A_labels','A_predict','收入记录如何构造成具体训练标签仍未公开','unknown',['S01','S05','S08'],
 'AppLovin收入事件管线','Axon训练任务','区分IAA IAP 代理及预测值；授权','label schema loss 退款 时区 延迟和缺失处理',['H2','H3'])
edge('A11','A_predict','A_bid','按特定广告主展示价值及return goals出价','official_use',['S02'],
 'Axon预测','AppLovin bidder','有广告主目标和可参与库存','实际数值函数 出价校准 pacing/shading',['H4'],production='official current product-use disclosure')
edge('A12','A_bid','A_exchange','CPM报价参与拍卖；协议证明交易接口','official_use',['S02'],
 'AppLovin bidder','可参与的广告库存','满足隐私 创意 底价 超时及预算；协议复用35—40','具体库存选择 每次真实报价和赢家trace',['H4'])
edge('A13','A_exchange','A_feedback','Axon使用自身收到的MAX赢输标通知','official_use',['S01'],
 'MAX对该bidder的结果通知','AppLovin/Axon','仅自身通知；不能扩大成竞争者用户及出价数据','通知字段的训练用途与更新延迟',['H4'],production='official direct model-use disclosure')
edge('A14','A_feedback','A_predict','官方称持续数据摄入 自学习及工程更新','official_use',['S03'],
 '允许的反馈数据','Axon模型系统','允许的数据类别和用途','在线/离线更新频率 replay/反事实策略',['H4'])
edge('A15','A_web','A_predict','订单历史用于客户建模和寻找高价值新客','official_use',['S11'],
 '授权商家','AppLovin ecommerce模型','商家授权 正确哈希 真实订单及同意','客户数据实际训练作业或性能归因',['H1','H2','H3'],scope='ecommerce; not games by default')
edge('A16','A_web','A_labels','电商订单能否默认加入手游IAA标签','unknown',['S11','S01'],
 '电商广告主','手游Axon训练任务','跨业务用途需独立合法授权','跨业务schema 数据隔离及训练用途文件',['H2','H5'])
edge('A17','A_ids','A_canonical','客户端共封装不证明统一自然人跨设备图谱','unknown',['S32','S33','S04'],
 '设备/发布者标识','未知服务端图谱','AppSet开发者scope ID重置 同意条件','生产join 命名空间 置信度及误匹配率',['H1'])
edge('A18','A_review','A_predict','Ad Review数据不建用户/设备档案 不进入Axon或其他模型','excluded',['S24'],
 'Ad Review','Axon/其他AppLovin模型','官方明确否认该用途','这是官方排除声明 非独立服务端审计',['H1','H3'],scope='specific excluded ad-quality source')
edge('A19','A_rival','A_predict','其他竞价者出价及用户数据被官方排除','excluded',['S01'],
 '其他bidder','Axon模型','不得由MAX可见字段推定进入训练','未独立审计；保留官方排除边界',['H3','H4'])
edge('A20','A_context','A_features','旧专利包含安装应用特征 不能认定现代Axon采用','indirect',['S31'],
 '2011/2013专利构想','历史广告选择设计','现代平台权限与用途另行限制','现代Axon产品连接和启用记录',['H1','H3'],scope='historical patent, not current architecture')

edge('U01','U_context','U_ads','请求与token包含设备 会话 广告位等上下文','sdk',['S34','S35','S36'],
 'Unity Ads SDK','Unity Ads gateway','PII允许开关 TCF/developerConsent 数据可用','gateway转码后实际模型特征',['H3'])
edge('U02','U_context','U_predict','官方称游戏DNA 真实玩家行为和生态数据驱动匹配','official_use',['S12'],
 'Unity允许的数据来源','Vector','相应权限与产品使用条件','具体游戏 行为schema 训练集范围及日期',['H1','H3'],production='official model-purpose description')
edge('U03','U_ads','U_ids','安装ID AUID Analytics/外部ID和隐私状态可进请求','sdk',['S34','S35','S36'],
 'Ads/LevelPlay或应用设置','Unity Ads请求层','字段可用且隐私允许；安装ID不是跨设备人ID','与MMP join的生产实现',['H1','H3'])
edge('U04','U_ids','U_features','广告请求标识与历史行为形成模型特征的具体映射未公开','inference',['S12','S18','S34'],
 'Unity Ads测量','Vector特征任务','同意 scope 时间一致','join字典 版本 特征水位和安装前snapshot',['H1','H3'])
edge('U05','U_revenue','U_mmp','实际广告收入和购买可由MMP接收','official_use',['S13','S19'],
 '游戏/中介/支付','授权MMP','真实事件 正确金额 去重及授权','目标游戏的送达/结算流水',['H2'])
edge('U06','U_mmp','U_labels','S2S支持gamer/ad ID campaign install时间 归因标记和金额','sdk',['S18','S19'],
 '授权MMP或广告主服务器','Unity Ads secondary events','授权配置 正确标识 隐私标记 广告主Game ID','实际接收及幂等 延迟/重归因处理',['H2'],scope='documented API, not sent by this study')
edge('U07','U_labels','U_predict','ROAS学习使用安装后数据与成熟cohort 支持IAA/IAP/Hybrid窗口','official_use',['S13','S15','S16','S17','S22'],
 '允许的安装及收入反馈','Unity Ads/Vector ROAS学习','MMP配置 选定窗口和学习门槛','具体loss/标签聚合权重和缺失建模',['H2','H3'],production='official learning workflow; no internal row-level logs')
edge('U08','U_runtime','U_predict','Runtime全部字段默认训练Vector的连接未证明','unknown',['S20','S12'],
 'Unity引擎 Developer Data','Vector训练集','Collection Usage设置与ads_intent等控制','native采集schema 生效配置 数据集血缘',['H1','H3'],scope='not all Unity apps auto-enabled')
edge('U09','U_purchase','U_predict','官方明确购买数据可帮助丰富Vector寻找未来玩家','official_use',['S21'],
 'IAP SDK/D2C合法购买数据','Vector','适用产品与授权 不能认为每游戏启用','具体字段覆盖 数据使用设置与训练任务',['H2','H3'],production='official product linkage; can enrich, not universal collection')
edge('U10','U_features','U_predict','行为建模与在线推断有Vector招聘支持','indirect',['S29','S30'],
 'Vector Ads Modeling/Gamer AI团队','Vector推荐推断系统','团队描述及招聘职责层证据','部署模型架构 schema 线上推断日志',['H3'])
edge('U11','U_predict','U_bid','预测个人收入潜力 根据tROAS动态出价','official_use',['S14','S22'],
 'Unity Ads/Vector价值预测','Unity Ads bidder','目标国家 窗口 ROAS设置 可用反馈','单次CPM函数 校准 预算约束',['H4'],production='official product mechanics')
edge('U12','U_bid','U_exchange','实时bidding pacing和bid landscape有专项团队线索','indirect',['S28'],
 'Vector Bidding Science','实时竞价系统','招聘描述 不是公式部署证明','pacing算法 price分布估计与线上实验',['H4'])
edge('U13','U_exchange','U_feedback','竞价及广告事件可形成反馈 协议复用35—40','sdk',['S36'],
 'Unity Ads/交易接口','Unity Ads测量层','回调注册 事件排队 隐私有效','事件接收与具体Vector训练映射',['H4'])
edge('U14','U_feedback','U_predict','反馈有助持续学习 官方未给每事件训练延迟','official_use',['S12','S16'],
 '允许的行为及cohort反馈','Vector学习','成熟度和产品配置','在线更新时间 特征延迟与漂移监测',['H4'])
edge('U15','U_accounts','U_canonical','UPA组织内跨设备账号不证明自动与广告统一','unknown',['S38'],
 '用户授权UPA登录','未知广告身份映射','账号用途 同意 组织scope','UPA→Ads/Vector直接接口或服务端join',['H1'])
edge('U16','U_ramp','U_exchange','RampID有Exchange美加受众激活官方产品证据','official_use',['S37'],
 'LiveRamp及授权受众方','支持的Unity Exchange DSP','美加 双方支持 授权受众 隐私','每请求映射结果与真实成交',['H1','H5'],scope='Exchange audience activation, not Vector training')
edge('U17','U_ramp','U_predict','RampID是否进入Vector训练未知','unknown',['S37'],
 'LiveRamp/Exchange','Vector','独立用途授权','训练血缘 产品连接声明和消融实验',['H1','H3'])
edge('U18','U_canonical','U_features','UPA RampID Ads统一图未获证 不能画为已建连接','unknown',['S38','S37','S34'],
 '多个Unity身份系统','Vector特征层','作用域和授权不能因同属Unity自动合并','命名空间 key转换 server匹配与用途',['H1','H5'])

graph=dict(schema_version='1.0',reviewed_utc=NOW,scope='Public documents and static SDK evidence; no production network tests',
 levels={'A':'official explicit flow/use disclosure','B':'traceable SDK/API capability','C':'authorized/anonymous experiment','D':'patent/job/indirect clue','E':'general architecture inference'},
 production_semantics='All production_actual_proven flags are false: public assertions are stored separately and not independently audited. Solid means proven within stated scope, NOT observed production delivery.',
 nodes=nodes,edges=edges,sources=sources,
 unknown_breakpoints=['join keys and feature lineage','install-before event-time snapshots','per-row revenue label generation','cross-business training authorization','embeddings architecture/deployment','deduplication delayed feedback and missingness','per-impression value-to-CPM function','target-game partner activation and delivery'],
 excluded_claims=['other bidders user/bid data in Axon','Ad Review data in Axon','synthetic lift proves vendor lift','UPA/RampID automatically feed Vector'])
(R/'EVIDENCE_GRAPH.json').write_text(json.dumps(graph,ensure_ascii=False,indent=2),encoding='utf-8')
(R/'SOURCE_EXCERPTS.json').write_text(json.dumps(sources,ensure_ascii=False,indent=2),encoding='utf-8')
print('graph',len(nodes),'nodes',len(edges),'edges',len(sources),'sources')
