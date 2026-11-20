"""Precise new claims; preserve the existing matrix prefix and historical graph."""
from pathlib import Path
import csv,datetime,hashlib,json,re,zipfile
from bs4 import BeautifulSoup
R=Path(__file__).resolve().parents[2];O=Path(__file__).resolve().parent
NOW=datetime.datetime.now(datetime.timezone.utc).isoformat()
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
new=[]
def add(n,company,product,path,a,b,quote,claim,limits,scope,level='【官方公开证实】',url=None,kind='official product/integration documentation',sdk=None):
    p=R/path;ls=p.read_text(encoding='utf-8-sig').splitlines();assert 1<=a<=b<=len(ls),(n,len(ls))
    assert quote in '\n'.join(ls[a-1:b]),(n,quote)
    date=next((x.split(': ',1)[1] for x in ls[:10] if x.startswith('last_updated: ')),None)
    m=None
    if path.startswith('model-architecture/round61-63/public/'):
        m=load(p.with_suffix('.meta.json'));assert m.get('status')==200
        assert 'Page not found' not in '\n'.join(ls[:35])
        assert sha(R/m['raw_path'])==m['raw_sha256'] and sha(p)==m['sha256']
        url=url or m['url']
        soup=BeautifulSoup((R/m['raw_path']).read_bytes(),'html.parser')
        pub=soup.find('meta',attrs={'property':'article:published_time'})
        if pub:date=pub.get('content')
    ident=f'RV61S{n:02d}'
    x=dict(id=ident,company=company,product=product,path=path,sha256=sha(p),start_line=a,end_line=b,
      excerpt='\n'.join(f'{i}: {ls[i-1]}' for i in range(a,b+1)),short_quote=quote,claim=claim,
      url=url,source_date=date or 'not stated; retrieved/reviewed 2026-11-19',reviewed_utc=NOW,
      evidence_level=level,evidence_kind=kind,applicable_product=scope,limits_and_counterevidence=limits,
      production_deployment_statement='public behavioral contract; not independently observed production' if level=='【官方公开证实】' else 'official standalone SDK code; not observed production',
      production_actual_proven=False,observed_target_game_delivery=False,independent_production_audit=False,
      server_model_training=False)
    if m:x['fetch_provenance']=m
    if sdk:x.update(sdk=sdk[0],version=sdk[1],class_or_method=sdk[2])
    new.append(x)

base='model-architecture/round61-63/public/'
add(1,'Unity','Post-install event data',base+'u-appdata-direct.txt',10,28,
 'Post-install event data informs Unity\'s models',
 '正式数据契约把session/purchase/ad_revenue/level_complete与相应目标分开，并建议额外事件数据',
 '收到事件种类不证明所有字段实际用于每个模型；level_complete不是收入',
 'Unity Ads UA MMP事件契约，不是逐行训练label')
add(2,'Unity','Post-install data loss',base+'u-appdata-direct.txt',38,59,
 'your servers can\'t retroactively send data from events',
 '官方警告错误集成会丢失事件且不能靠服务器retroactive发送补回；MMP事件种类和订阅支持有条件',
 '该产品契约不证明一般技术上无法补数，或所有MMP永不支持backfill；不等于训练标签迟到窗口',
 'Unity所述MMP集成，不扩展为所有收入平台的绝对限制')
add(3,'Unity','Revenue event mapping',base+'u-integration-best.txt',60,88,
 'Sending ad revenue as a different event type can cause campaign optimization to stop working',
 'Unity明确IAA要走专用收入通道；不支持时不能伪装purchase，否则可能破坏优化',
 '此处不能推断具体损失函数；真正Hybrid组合目标不等于混淆事件语义',
 'Adjust及除Singular外所述集成契约')
add(4,'Unity','Singular mapping exception',base+'u-integration-best.txt',107,124,
 'Singular is the only MMP that supports sending ad revenue and in-app purchase events together',
 'Unity文档对Singular给出__REVENUE__*及Send all ad monetization events的特定例外',
 '不证明任意MMP可混报；例外不允许把代理value当收入；不证明游戏已启用',
 'Unity-Singular partner配置，仅限文档表述')
add(5,'Unity','Budget hierarchy/throttling',base+'u-budget-intro.txt',20,61,
 'use the target budget to throttle your campaign',
 '公开组织/活动/日预算分层；日预算为目标/平均值，接近限制会throttle且可超支，UTC重置',
 '预算不是逐请求硬上限；不公开控制器系数或每bid multiplier；部分设置页与总览需核对具体产品',
 'Unity UA预算行为，非特定模型公式')
add(6,'Unity','Multi-country allocation',base+'u-budget-intro.txt',63,86,
 'distributes spend across the countries in each group in real time',
 '公开国家组预算实时按赢标/转化分配；Daily/Geo Capped会暂停全部或部分交付',
 '按performance分配不等于每次按D28预测值排序，也不证明共享模型参数',
 '全部campaign types公开预算产品行为')
add(7,'Unity','ROAS automated bidding',base+'u-budget-best.txt',14,32,
 'with CPI billing, the campaign automatically uses Automated bidding',
 '官方明确CPI计费ROAS自动使用Automated bidding，并描述按日调整/周级预算和约7日适应',
 '限定计费和产品条件；不把安装量自动竞价目标外推为所有ROAS策略；不是生产源码',
 'Unity ROAS+CPI billing预算策略')
add(8,'Unity','Exploration budget',base+'u-budget-best.txt',34,40,
 'explore your campaign and creatives',
 '官方明确先探索campaign/creatives，建议campaign预算至少为日预算5倍以提供探索资金',
 '5倍是运营建议不是模型样本阈值；不证明UCB/Thompson/RL或用方差调价',
 'Unity UA预算建议；产品条件见原文')
add(9,'Unity','Seven-day pacing',base+'u-budget-best.txt',73,83,
 'operates on a 7-day rolling window rather than enforcing hard daily limits',
 '预算文档明确7日滚动窗口补偿超支/欠支，含国家组预算；是可核验的pacing产品行为',
 '不是每自然日保证硬cap，也没有公开单次出价的pacing因子或控制算法',
 'Unity日预算管理说明；非Vector网络架构')
add(10,'Unity','Country ROAS and budget setup',base+'u-create-roas.txt',16,42,
 'set a [ROAS goal]',
 '官方配置要求选择优化类型/窗口、按国家设ROAS目标、campaign预算和归因链接',
 '配置存在不证明某目标游戏已配置；不是国家用户价值训练特征已证',
 'Unity ROAS campaign设置')
add(11,'Unity','CVR/CPI/eCPM exposure',base+'u-bid-intro.txt',20,36,
 'determined by the CVR',
 '官方将展示到安装CVR与CPI连接到eCPM/曝光，列收入目标动态竞价',
 '不证明独立pInstall神经head；表中tCPM/Target cost per install标签不一致不能自行修成真实模型',
 'Unity UA竞价术语与产品关系，不是报价公式')
add(12,'AppLovin','Scale and budget recommendations',base+'al-scale-right.txt',47,66,
 'at least 15–20 conversions',
 '官方建议每天15–20目标转化、跨国单一全局预算及符合利润目标的goal；缺失conversion会影响未来campaign',
 '转化数是稳定表现建议，不是Axon训练门槛；全球预算建议不暴露pacing算法；未证明四款实际设置',
 'AppLovin apps UA运营契约')
add(13,'AppLovin','Pixel/SDK/S2S deduplication',base+'al-website-dedup.txt',13,50,
 'no more than thirty seconds apart',
 '网站文档给同事件跨Pixel/site-to-site/SDK共享dedupe_id：30秒内merge，超过5分钟的后到副本drop',
 '30秒至5分钟间行为未写清；不证明退款回滚、IAA/MMP去重或训练exactly-once；不能套到四款',
 'AppLovin网站事件多通路去重文档，含SDK options示例')
add(14,'Adjust','Android5.8.1 revenue validation',
 'ThirdPartySDKs/Adjust/Android/5.8.1/sources/com/adjust/sdk/AdjustEvent.java',142,164,
 'revenue < 0.0',
 'AdjustEvent.checkRevenue对负金额返回false，零不被该比较拒绝；需非空currency',
 'setRevenue不赋负金额不代表整事件必被丢弃；不证明退款永不支持/零收入玩家成为训练样本；非四款具体集成版',
 '独立Adjust Android5.8.1 SDK',level='【SDK代码证实】',
 url='https://repo.maven.apache.org/maven2/com/adjust/sdk/adjust-android/5.8.1/adjust-android-5.8.1-sources.jar',
 kind='official SDK source',sdk=('Adjust Android','5.8.1','AdjustEvent.checkRevenue/setRevenue'))
add(15,'AppLovin','MAX unified first-price auction','auction/al-dynamics.txt',13,40,
 'unified first-price auction',
 '官方协议明确MAX收集有效SDK/DSP报价，与waterfall合并按最高CPM选取；render后触发billing',
 '供给侧机制不是Axon私有价值→报价公式；第一价格本身不证明bid shading或竞争者数据进入Axon训练',
 'MAX Exchange需求伙伴拍卖协议；复用已取得原文',
 url='https://support.applovin.com/en/max/demand-partners/auction-dynamics')
add(16,'Unity','Exchange deadline/first-price','auction/unity-get-started.txt',20,34,
 '50ms is deducted',
 'Unity Exchange公开第一价格及动态tmax；waterfall seat最高1000ms，bidding按mediation配置扣50ms',
 'exchange响应预算不是Vector推断SLA或SDK加载时限；不证明bid shading算法',
 'Unity Exchange公开DSP协议；复用原文',
 url='https://docs.unity.com/en-us/grow/programmatic/unity-exchange/get-started.md')

# Tie static revenue checks to exact reused official artifacts and archive member.
s=next(x for x in new if x['id']=='RV61S14')
prov=load(R/'ThirdPartySDKs/Adjust/Android/5.8.1/provenance.json');art=[]
for a in prov['artifacts']:
    if a['path'].endswith(('.aar','sources.jar')):
        p=R/'ThirdPartySDKs'/Path(a['path'].replace('\\','/'));assert sha(p)==a['sha256']
        art.append(dict(a,path=p.relative_to(R).as_posix()))
        if p.name.endswith('sources.jar'):
            with zipfile.ZipFile(p) as z:
                member='com/adjust/sdk/AdjustEvent.java'
                assert z.read(member)==(R/s['path']).read_bytes()
                s['source_archive_member']=member
s['official_packages']=art
save(O/'SOURCE_EVIDENCE.json',new)

oldbytes=(O/'CLAIM_MATRIX.before.csv').read_bytes();matrix=R/'model-architecture/CLAIM_MATRIX.csv'
assert matrix.read_bytes()==oldbytes,'Matrix already changed; reconcile instead.'
with matrix.open(encoding='utf-8-sig',newline='') as f:fields=csv.DictReader(f).fieldnames
with matrix.open('a',encoding='utf-8',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=fields)
    for s in new:
        writer.writerow(dict(id=s['id'],company=s['company'],product=s['product'],publication_date=s['source_date'],
          original_url=s['url'],local_file=s['path'],sha256=s['sha256'],start_line=s['start_line'],end_line=s['end_line'],
          short_quote=s['short_quote'],technical_claim=s['claim'],applicable_product=s['applicable_product'],
          evidence_level=s['evidence_level'],explicit_production_deployment=s['production_deployment_statement'],
          evidence_kind=s['evidence_kind'],counterevidence_and_unknowns=s['limits_and_counterevidence'],original_source_id=''))

cat=['# 61＋63原始证据增量目录','','旧MA60对象和矩阵行不改；本轮只新增更精确的事件、预算和决策边界。文档行为不等于生产代码或独立观测。','']
for s in new:
    cat += [f'<a id="{s["id"].lower()}"></a>',f'## {s["id"]} · {s["company"]} / {s["product"]}','',
      f'- 原文：{s["url"]}',f'- 位置：[{s["path"]}:L{s["start_line"]}](../../{s["path"]})；L{s["start_line"]}—L{s["end_line"]}',
      f'- 日期：{s["source_date"]}；查阅：{NOW}',f'- 文件SHA256：`{s["sha256"]}`',f'- 短摘录：{s["short_quote"]}',
      f'- 主张：{s["evidence_level"]}{s["claim"]}',f'- 适用范围：{s["applicable_product"]}',
      f'- 部署层级：{s["production_deployment_statement"]}',f'- 未知/反证：{s["limits_and_counterevidence"]}','']
    if 'fetch_provenance' in s:
        m=s['fetch_provenance'];cat += [f'原始HTTP响应：[{m["raw_path"]}](../../{m["raw_path"]})；SHA256 `{m["raw_sha256"]}`。','']
    for a in s.get('official_packages',[]):cat += [f'官方包：[{a["path"]}](../../{a["path"]})；SHA256 `{a["sha256"]}`；来源 {a["url"]}。','']
(O/'SOURCE_CATALOG.md').write_text('\n'.join(cat),encoding='utf-8')

ledger=[]
for p in sorted((O/'public').glob('*.meta.json')):
    x=load(p);txt=(O/'public'/(x['id']+'.txt'))
    body=txt.read_text('utf-8') if txt.exists() else ''
    if 'error' in x:disp='failed public documentation request; not evidence; internal redirect not followed further'
    elif 'Page not found' in body[:700]:disp='HTTP200 soft404; excluded'
    elif x['id'] in ['u-acquire-nav','u-bids-nav','u-budgets-nav','u-budget-types','u-campaigns-nav','u-roas-setup']:disp='navigation only; not model evidence'
    else:disp='public primary document; only cited selected claims, no model architecture inferred'
    x['disposition']=disp;ledger.append(x)
save(O/'ACQUISITION_LEDGER.json',ledger)
print('New exact claims:',len(new),'matrix total rows:',28+len(new),'reused Adjust release/member verified.')
