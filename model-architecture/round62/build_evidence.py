"""Author/source trace and scope-specific claims; no model implementation inference."""
from pathlib import Path
from bs4 import BeautifulSoup
import csv,datetime,hashlib,json,re,copy
R=Path(__file__).resolve().parents[2];O=Path(__file__).resolve().parent
NOW=datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def save(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
old=load(O/'EVIDENCE_GRAPH.before.json');prior={s['id']:s for s in old['sources']}

# Trace the original page, not a search snippet or invented author profile.
raw=R/'model-architecture/public/unity-d7-d28.raw';soup=BeautifulSoup(raw.read_bytes(),'html.parser')
blog=next(json.loads(t.get_text()) for t in soup.find_all('script',type='application/ld+json')
          if json.loads(t.get_text()).get('@type')=='BlogPosting')
links=[dict(text=t.get_text(' ',strip=True),url=t['href']) for t in soup.find_all('a',href=True)]
trace=dict(original_url=blog['url'],raw_path=raw.relative_to(R).as_posix(),raw_sha256=sha(raw),
 author_jsonld=blog['author'],date_published=blog['datePublished'],headline=blog['headline'],
 author_role_visible='Senior Content Marketing Manager',
 author_hyperlinks=[x for x in links if re.search('Godley|author|profile',x['text']+' '+x['url'],re.I)],
 relevant_body_links=[x for x in links if x['url'] in ['https://unity.com/blog/uads-march-updates','https://unity.com/products/unity-ads/vector']],
 architecture_paper_or_conference_link_found=False,
 boundary='No research-paper/GDC/model architecture reference observed in article text or its two relevant product links; not proof no external talk exists',
 reviewed_utc=NOW)
assert blog['author'][0]['name']=='Daniel Godley' and blog['datePublished']=='2026-06-25'
save(O/'AUTHOR_TRACE.json',trace)

ss=[]
def add(n,company,product,path,a,b,quote,claim,scope,limits,origin=None,url=None,date=None):
    p=R/path;ls=p.read_text(encoding='utf-8-sig').splitlines();assert 1<=a<=b<=len(ls)
    assert quote in '\n'.join(ls[a-1:b]),n
    orig=prior.get(origin,{})
    if orig:assert sha(p)==orig['sha256'],origin
    m=None
    if path.startswith('model-architecture/round62/public/'):
        m=load(p.with_suffix('.meta.json'));assert m['status']==200
        assert sha(R/m['raw_path'])==m['raw_sha256'];assert sha(p)==m['sha256']
        url=url or m['url']
    date=date or orig.get('source_date') or next((l.split(': ',1)[1] for l in ls[:10] if l.startswith('last_updated: ')),None)
    x=dict(id=f'CT62S{n:02d}',company=company,product=product,path=path,sha256=sha(p),start_line=a,end_line=b,
      excerpt='\n'.join(f'{i}: {ls[i-1]}' for i in range(a,b+1)),short_quote=quote,claim=claim,
      url=url or orig.get('url'),source_date=date or 'publication date not stated; reused cached official source reviewed2026-11-19',
      evidence_level='【官方公开证实】',applicable_product=scope,limits_and_counterevidence=limits,
      evidence_kind='official source scope/author/cold-start contract',original_source_id=origin,
      production_deployment_statement='official author/product/data-use assertion; no independently observed model implementation',
      reviewed_utc=NOW,production_actual_proven=False,observed_target_game_delivery=False,server_model_training=False)
    if m:x['fetch_provenance']=m
    ss.append(x)

add(1,'Unity','Vector cross-game article authorship','model-architecture/public/unity-d7-d28.txt',123,130,
 'Senior Content Marketing Manager',
 '原文及JSON-LD确认作者Daniel Godley、2026-06-25及内容营销职务；无可见作者工程论文/演讲引用',
 '文章身份/证据类型，不否定官方用途声明',
 '作者职务本身既不证明技术主张错误，也不使其成为独立部署审计；未发现引用不证明外部材料不存在',
 url=blog['url'],date='2026-06-25')
add(2,'Unity','Cross-game use at bid decision','model-architecture/public/unity-d7-d28.txt',208,223,
 'cross-game behavioral patterns and aggregate cohort insights',
 '官方将跨游戏行为模式/聚合cohort洞察与bid-time玩家区分连接；未区分统计、共享参数或个人历史',
 'Vector D7/D28 IAP用途；B有明确聚合洞察陈述，C/D未定',
 '样本比较来自2024-04至2025-02；不能证明2026模型消融或个人级join，也不能指定embedding',
 origin='MA60S17')
add(3,'Unity','Linked ROAS onboarding announcement','model-architecture/round62/public/unity-march-linked.txt',123,150,
 'data enablement and validation steps',
 '原文章链接的官方发布仍要求数据准备/验证，并保留Learning到Live门槛；简化开户不等于无数据学习',
 '2026-03-06 Vector ROAS onboarding，作者Danielle Shevchuk/产品营销',
 '不是模型论文，也没有公开B/C/D实现；Homa案例不能补迁移因果',
 date='2026-03-06')
add(4,'Unity','Same-app cross-source prelaunch learning','vector/doc-roas-campaign-best-practices.txt',36,70,
 'at least two weeks before you create your new ROAS campaign',
 '同目标App可在新活动前提供SDK和未归因事件帮助训练；无需等待这些样本来自本平台付费安装',
 '机制A；预启动数据不计入学习退出门槛',
 '不等于跨游戏个人数据、模型共享或无自身历史时已能准确预测；非自动历史回填',origin='MA60S14')
add(5,'Unity','No prerequisite install campaign','vector/doc-intro-to-roas-campaigns.txt',91,95,
 'without first running an Install campaign',
 '官方明确可直接启动ROAS不必先跑Install campaign，但仍在Learning收集相关post-install数据',
 '新活动/新网络冷启动，不是零数据高精度保证',
 '不能取消该文成熟及样本阈值，也不证明全新游戏直接有优质价值识别',
 url='https://docs.unity.com/en-us/grow/acquire/campaigns/roas/intro-to-roas-campaigns.md',date='2026-05-21')
add(6,'Unity','Unattributed source scope','model-architecture/round62/public/unity-acquire-attribution.txt',26,36,
 'Unity counts organic installs as **Unattributed**',
 '此MMP契约的unattributed是目标App来自其他广告网络/自然量，不是跨游戏个人历史的同义词',
 '机制A来源分类；不把文章泛称跨游戏数据与该字段自动判等',
 '只定义来源；不说明训练样本混合权重或join成功')
add(7,'AppLovin','Axon public training categories','nongame/applovin-axon-about.txt',60,73,
 'As more advertisers use our performance-based advertising solutions, the models improve through additional data',
 '缓存官方说明称额外广告主数据/洞察改善模型，持续训练使用允许的互动与广告主自愿数据；未披露跨游戏学习契约',
 '一般系统级数据学习声明，不特指B/C/D；此次刷新403，使用保留旧官方快照',
 '不证明统一权重、跨游戏feature store、每用户历史或新游戏冷启动提升；不获取受限页面',origin='MA60S02')
add(8,'AppLovin','Advertiser-owned all-source sharing','axon/adjust-applovin.txt',113,127,
 'Data from all attribution sources',
 'Axon partner可选择全部来源或只Axon来源，session/revenue/事件映射须配置；最直接支持A可用',
 '同一广告主App归因来源；文档说may optimize，不保证某游戏生产学习',
 '不是将别的游戏个人行为授权给本游戏；没有明确跨游戏参数/统计/个人特征契约',origin='CGS50')
add(9,'AppLovin','Cross-category prospective gaming benefit','model-architecture/public/al-introducing.txt',47,50,
 'the incremental data will materially improve',
 '官方预期更多广告主数据将改善游戏伙伴效果；前瞻承诺不等于明确跨游戏共享实现',
 '系统增长方向与未来受益，不是游戏个人级轨迹授权',
 'will/believe不能升级实际部署；无法区分聚合/参数共享/个人历史贡献',origin='MA60S04')
add(10,'Unity','Developer Data privacy gating','vector/ddf-end-user-consent.txt',20,38,
 'ads_intent = denied',
 'Developer Data个性化广告用途及广告专用标识受ads_intent约束；未知状态默认denied',
 '排除默认无限收集/训练个人广告历史；不是全部SDK统一闸门',
 '无广告ID不证明完全无关联；B/C也需合法训练用途，聚合不能洗白未经授权原始数据',origin='MA60S23')
add(11,'AppLovin','Ad Review data exclusion','prediction-system/applovin-excluded-rival-data.txt',14,17,
 'do not feed it into Axon',
 '官方排除Ad Review输出建用户/设备档案或供给Axon；不能用广告审查观察来补跨游戏D',
 '特定数据来源/用途排除；不否定允许的广告主收入反馈',
 '不排除Axon用其他合法来源的B/C/D；只能否定该来源链',origin='MA60S08')

save(O/'SOURCE_EVIDENCE.json',ss)
matrix=R/'model-architecture/CLAIM_MATRIX.csv';before=(O/'CLAIM_MATRIX.before.csv').read_bytes()
assert matrix.read_bytes()==before
with matrix.open(encoding='utf-8-sig',newline='') as f:fields=csv.DictReader(f).fieldnames
with matrix.open('a',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields)
    for s in ss:w.writerow(dict(id=s['id'],company=s['company'],product=s['product'],publication_date=s['source_date'],
      original_url=s['url'],local_file=s['path'],sha256=s['sha256'],start_line=s['start_line'],end_line=s['end_line'],
      short_quote=s['short_quote'],technical_claim=s['claim'],applicable_product=s['applicable_product'],evidence_level=s['evidence_level'],
      explicit_production_deployment=s['production_deployment_statement'],evidence_kind=s['evidence_kind'],
      counterevidence_and_unknowns=s['limits_and_counterevidence'],original_source_id=s.get('original_source_id') or ''))

cat=['# 62号冷启动证据目录','','本轮11条限定主张：新增作者/关联发布溯源，复用已核验原文检验A/B/C/D，不能按主张数量解释研究突破。','']
for s in ss:
    cat += [f'<a id="{s["id"].lower()}"></a>',f'## {s["id"]} · {s["company"]} / {s["product"]}','',
      f'- 原文URL：{s["url"]}',f'- 日期：{s["source_date"]}；查阅：{NOW}',
      f'- 本地：[{s["path"]}:L{s["start_line"]}](../../{s["path"]})；L{s["start_line"]}—L{s["end_line"]}',
      f'- SHA256：`{s["sha256"]}`',f'- 短摘录：{s["short_quote"]}',
      f'- {s["evidence_level"]} {s["claim"]}',f'- 范围：{s["applicable_product"]}',
      f'- 限制：{s["limits_and_counterevidence"]}','']
    if s.get('original_source_id'):cat += [f'复用原对象：{s["original_source_id"]}；旧记录不变。','']
    if 'fetch_provenance' in s:
        m=s['fetch_provenance'];cat += [f'原始HTTP：[{m["raw_path"]}](../../{m["raw_path"]})；SHA256 `{m["raw_sha256"]}`。','']
(O/'SOURCE_CATALOG.md').write_text('\n'.join(cat),encoding='utf-8')
print('Author trace and',len(ss),'scoped source claims; matrix prefix preserved.')
