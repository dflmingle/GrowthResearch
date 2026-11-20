from pathlib import Path
import json,re,hashlib,datetime
R=Path(__file__).resolve().parent
sources={}
for p in sorted(R.glob('fetches-*.json')):
 for row in json.loads(p.read_text(encoding='utf-8')):sources[row['id']]=row
for k,row in sources.items():
 p=R/(k+'.txt');text=p.read_text(encoding='utf-8') if p.exists() else ''
 row['content_caveat']=('HTTP error or transport failure' if row.get('status')!=200 else 'soft 404 / missing page' if 'Page not found. Check the URL' in text else 'search shell, not usable search evidence' if k.startswith('search-') and 'Google Search' in text else 'manual content verification required; HTTP 200 alone is not evidence')
(R/'PUBLIC_SOURCE_INDEX.json').write_text(json.dumps(sources,ensure_ascii=False,indent=2),encoding='utf-8')

rules={
 'doc-events':r'^(page_view|view_item|add_to_cart|begin_checkout|purchase|transaction_id|currency|shipping|tax|subscribe|generate_lead|value|user_data)$|subtotal',
 'doc-capi':r'v1/event|Authorization|dedupe_id|aleid|alart|axwrt|client_ip_address|event_source_url|attribution_share|is_claimable|at least one|Maximum batch',
 'doc-dedupe':r'thirty seconds|five minutes|dedupe_id',
 'doc-order-history':r'accurate model|new, high-value|prospecting|transaction_id|privacy compliance|SHA-256',
 'doc-data-sharing':r'consent|sensitive|children|AI-powered|privacy policy',
 'applovin-axon-about':r'our models|Our models|other bidders|advertisers’ own data|win or loss|sensitive personal',
 'applovin-policy-direct':r'e-Commerce Ads Only|previous actions|combine information|App Set IDs|Purchasing histories|Affiliates',
 'unity-policy':r'AppLovin|Applovin|bidding partners|These partners use|Personal Data to|personalized advertisements',
 'utility-zedge':r'Applovin|IronSource|Device data; Ad engagement data|withdraws consent',
 'utility-inshot':r'AppLovin|Android ID|pop up',
 'utility-flashlight-correct':r'AppLovin|Supersonic|Apps & Games|Advertising Network',
 'content-dramabox':r'Applovin|commercial monetization|AppsFlyer|product placements',
 'content-reelshort-official-policy':r'Unityads|advertisement was visible|Click-throughs|third-party advertising partners',
 'content-audiomack-official-policy':r'personalized|advertis|third parties|subscription',
 'life-winwalk':r'AppLovin|Unity Ads|Google user data|technical information|physical activity',
 'life-weward-correct':r'Applovin|Unity|never used for advertising|Navigation data is never sold|Advertising identifier|With your consent',
 'life-cashwalk':r'THIRD PARTY|third parties|Advertising and Retargeting',
 'wurl-advertising':r'viewing behavior|scene|metadata|DSP|KERV|IRIS.TV|Peer39',
 'wurl-policy-correct':r'does not apply|AdPool|ContentDiscovery|Customer Data',
}
out=[]
for k,pat in rules.items():
 p=R/(k+'.txt');lines=p.read_text(encoding='utf-8').splitlines()
 out.append({'source_id':k,'path':p.name,'url':sources[k]['url'],'hits':[{'line':i,'text':s[:1500]} for i,s in enumerate(lines,1) if re.search(pat,s,re.I)][:36]})
for k,pat in {
 'site-hexclad':r'applovin-shop-integration[^"<]*',
 'site-resparked':r'applovin-shop-integration[^"<]*|.{0,120}AppLovin \(Axon\).{0,100}',
 'site-trueclassic':r'applovin-shop-integration[^"<]*',
 'site-gruns':r'<!-- Start of Applovin scripts -->[\s\S]{0,650}<!-- End of Applovin scripts -->',
 'site-blissy':r'applovin: \{[\s\S]{0,250}\},',
 'site-hexclad-embed':r'[^\n]*(?:_axon_event_id|QUERY_PARAM_ALEID|PIXEL_LOG_ENDPOINT|_axUpdateCartAttributes)[^\n]*',
}.items():
 p=R/(k+'.raw');t=p.read_text(encoding='utf-8');hits=[]
 for m in re.finditer(pat,t,re.I):
  s=m.group(0)
  s=re.sub(r"(event_key:\s*)'[^']*'",r"\1'[PUBLIC_EVENT_KEY_NOT_REPRODUCED]'",s)
  s=re.sub(r'(data-consent-id=)"[^"]*"',r'\1"[CMP_CATEGORY_ID]"',s)
  hits.append({'character_offset':m.start(),'text':s[:1200]})
 out.append({'source_id':k,'path':p.name,'url':sources[k]['url'],'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'hits':hits[:15]})
(R/'SOURCE_EXCERPTS.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')

unknown='未取得该应用APK/发行包；准确SDK版本、初始化、逐事件调用和生产送达尚未验证'
def sample(sid,category,product,package,policy,components,fields,purpose,limits,level):
 return {'id':sid,'category':category,'product':product,'android_package':package,'policy_source_ids':policy,'public_store_source_id':{'U01':'utility-zedge-play','U02':'utility-inshot-play','U03':'utility-flashlight-play','C01':'content-dramabox-play','C02':'content-reelshort-play','C03':'content-audiomack-play','L01':'life-winwalk-play','L03':'life-cashwalk-play'}.get(sid),'technical_components':components,'sdk_version':unknown,'fields_or_events':fields,'purpose':purpose,'limitations':limits,'evidence_grade':level,'source_urls':{k:sources[k]['url'] for k in policy}}
rows=[
 sample('U01','工具/个性化','Zedge Wallpapers & Ringtones','net.zedge.android',['utility-zedge'],['AppLovin','IronSource','AppsFlyer'],['device data','ad engagement data'],'展示广告；AppsFlyer另列统计用途','政策明确列名及字段，但没有证明每个产品/地域均启用；不等于MAX准确版本','【公开资料证实】'),
 sample('U02','工具/视频编辑','InShot','com.camerasideas.instashot',['utility-inshot'],['AppLovin Ads SDK','AdMob','Firebase'],['Android ID（按政策表述）','app-use tracking choices'],'加载/展示广告、个性化；政策称弹窗征求跟踪选择','未验证实际标识是否改用GAID；不能把编辑的照片/视频/音频推定交给广告SDK','【公开资料证实】'),
 sample('U03','工具/手电筒','Flashlight: Torch Light — RV AppStudios','com.rvappstudios.flashlight',['utility-flashlight-correct','utility-flashlight-play'],['发行商成人Apps & Games政策列AppLovin、Supersonic/IronSource'],['政策总体列设备/广告标识、设备环境'],'广告及服务优化','Play指向同一发行商政策；其多产品广告名单不能证明该APK实际含每个SDK','【公开资料证实】（共享政策范围）；【无法确认】单应用接入'),
 sample('C01','内容/短剧','DramaBox','com.storymatrix.drama',['content-dramabox'],['AppLovin MAX SDK','AppsFlyer SDK'],['政策未给MAX逐字段表；通用设备/使用数据与广告用途分列'],'MAX commercial monetization；AF product-placement effectiveness','不能把视频观看记录、安装应用列表等政策总体类别全部归给MAX','【公开资料证实】'),
 sample('C02','内容/短剧','ReelShort','com.newleaf.app.android.victor',['content-reelshort-official-policy','content-reelshort-play'],['Unityads（政策原文）'],['广告展示位置/时长','广告尺寸','点击/广告响应','设备广告标识等政策类别'],'广告交付、效果衡量、相关广告及targeting/measurement改善','政策包含游戏通用模板措辞；不能据此判定本体Unity引擎、Vector或每字段已发送','【公开资料证实】'),
 sample('C03','内容/音乐','Audiomack','com.audiomack',['content-audiomack-official-policy'],['政策描述广告/分析技术，未取得Unity或AppLovin明确接入证据'],['IP/device/browser','播放/互动/访问时长','订阅信息（均为Audiomack政策总体类别）'],'内容服务、广告和分析','AppLovin/Unity链缺失；不得把Audiomack自身知道的数据写成两广告平台已获得','【无法确认】目标平台接入'),
 sample('L01','生活服务/步行奖励','Winwalk','com.winwalk.android',['life-winwalk'],['AppLovin','Unity Ads','Kochava'],['设备标识/IP','广告互动/技术信息（政策共享类别）'],'广告、survey/rewards和效果追踪','Google Fit/Google用户数据明确不与第三方共享；步数/健康数据不据此成为平台输入','【公开资料证实】'),
 sample('L02','生活服务/步行与购物返奖','WeWard',None,['life-weward-correct'],['AppLovin','Unity','ironSource','Adjust（非穷尽伙伴名单）'],['广告ID','账号创建日期/国家/应用导航/点击/设备环境等共享类别'],'经同意的广告定向/效果衡量；激励视频奖励','不是每个伙伴收到整张字段表；定位区域和非商家浏览数据存在明确用途排除，不能用于广告/训练；SDK版本未知','【公开资料证实】'),
 sample('L03','生活服务/计步奖励','CashWalk','com.cashwalklabs.cashwalk',['life-cashwalk'],['未具名第三方广告/分析技术'],['IP/device identifiers','browser/user activity（总体类别）'],'广告、分析与奖励','取得页面标2019；没有AppLovin/Unity具名证据；不将通用条款当接入','【无法确认】目标平台接入'),
]
for sid,product,k in [('W01','HexClad','site-hexclad'),('W02','Resparked','site-resparked'),('W03','True Classic','site-trueclassic')]:
 rows.append({'id':sid,'category':'电商网站','product':product,'source_urls':{k:sources[k]['url']},'policy_source_ids':[k],'technical_components':['公开HTML含AppLovin Shopify app-embed.js','Shopify pixel配置（仅Resparked另有明确描述）' if sid=='W02' else 'Shopify主题扩展'],'sdk_version':'路径applovin-shop-integration-103是扩展构建标识，不作为SDK语义版本；JS原文SHA256已存','fields_or_events':['静态共享资产：URL aleid/axeid、_axeid、本地存储、购物车_axon_event_id；/v1/log可含当前URL'],'purpose':'连接点击归因标记与购物车/订单链；日志诊断','limitations':'只取公开HTML/JS未执行、未读购物车或cookie、未下单、未验证Pixel/CAPI事件生产发送；共享JS不等于所有网站运行配置相同','evidence_grade':'【公开网页代码证实】嵌入；【无法确认】生产送达'})
(R/'SAMPLE_CATALOG.json').write_text(json.dumps({'scope':'12 primary public samples; not 12 verified SDK binaries','samples':rows,'summary':{'apps_reviewed':9,'apps_named_target_partner_disclosure':6,'apps_shared_publisher_policy_only':1,'apps_no_named_target_evidence':2,'sites_public_embed_verified':3},'supplemental':{'Gruns':'AppLovin-labelled loader blocked in text/plain CMP markup; not execution proof','Blissy':'Northbeam generic platform parameter map; not AppLovin Pixel integration proof'},'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()},ensure_ascii=False,indent=2),encoding='utf-8')
print('source records',len(sources),'excerpt groups',len(out),'samples',len(rows))
