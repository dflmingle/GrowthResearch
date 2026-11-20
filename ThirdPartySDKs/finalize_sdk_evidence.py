from pathlib import Path
import json,hashlib,datetime,re,collections
R=Path(__file__).resolve().parent;ROOT=R.parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,o):p.write_text(json.dumps(o,ensure_ascii=False,indent=2),encoding='utf-8')
# Current hashes of original archives, independent of previous reports.
samples=[]
for x in json.loads((ROOT/'SAMPLE_CATALOG.json').read_text(encoding='utf-8')):
 if not x.get('sample_path') or not x.get('sha256'):continue
 p=Path(x['sample_path'])
 if not p.is_absolute():p=ROOT/p
 if not p.exists():raise FileNotFoundError(p)
 h=sha(p);samples.append({'slug':x['slug'],'path':str(p),'expected':x['sha256'],'sha256':h,'unchanged':h==x['sha256']})
write(R/'ORIGINAL_SAMPLE_INTEGRITY.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'samples':samples,'pass':all(x['unchanged'] for x in samples)})

# Public sources are saved with substantive excerpts and line numbers, not just HTTP 200.
ax=ROOT/'axon';fetches=[]
for p in sorted(ax.glob('fetches-*.json')):fetches+=json.loads(p.read_text(encoding='utf-8'))
ids={x['id']:x for x in fetches}
terms={
 'doc-set-up-mmp-tracking':['must configure mobile tracking'],
 'doc-adjust':['Map your events','Predicted revenue','showing advertisements','data sharing'],
 'doc-appsflyer':['Activate partner','No values & no revenue','Predicted revenue','showing advertisements'],
 'adjust-applovin':['Map events','all attribution','not automatically','gps_adid'],
 'af-campaign':['ALL-Installs','Activate partner','organic'],
 'af-max-revenue':['device level','aggregate'],
 'doc-scale-your-campaign':['must be on MAX','IAA ROAS','conversions'],
 'gaming-apps':['COST PER EVENT','automatically optimizes','Max integrated'],
 'game-inventory':['inventory spans','between levels','in-game rewards'],
 'applovin-privacy':['across mobile apps','App Set IDs','if provided','other apps or websites'],
 'blog-data-boundary':['do not feed it into Axon','do not build user','publisher turns it on'],
 'doc-tracking-url-macros':['{CAMPAIGN_ID}','{PACKAGE_NAME}','{EVENT_ID}','{PLACEMENT_ID}'],
}
public=[]
for key,ts in terms.items():
 x=dict(ids[key]);p=ax/(key+'.txt');s=p.read_text(encoding='utf-8').splitlines();snips=[]
 for term in ts:
  found=[i for i,t in enumerate(s) if term.lower() in t.lower()]
  for i in found[:2]:snips.append({'query':term,'start_line':max(0,i-2)+1,'end_line':min(len(s),i+5),'text':'\n'.join(s[max(0,i-2):i+5])})
 x.update(text_path=str(p.relative_to(ROOT)).replace('\\','/'),sha256=sha(p),excerpts=snips);public.append(x)
write(ax/'VERIFIED_SOURCES.json',public)

manifest=json.loads((ROOT/'EVIDENCE_MANIFEST.json').read_text(encoding='utf-8'));entries=[]
def add(id,title,paths,notes):
 sources=[]
 for rel in dict.fromkeys(paths):
  p=ROOT/rel
  if not p.is_file():raise FileNotFoundError(p)
  sources.append({'path':rel.replace('\\','/'),'sha256':sha(p)})
 entries.append({'id':id,'title':title,'notes':notes,'sources':sources})
def sdkpaths(pattern):return [str(p.relative_to(ROOT)).replace('\\','/') for p in R.glob(pattern) if p.is_file()]
def axpaths(keys):return ['axon/'+k+s for k in keys for s in ['.html','.txt'] if (ax/(k+s)).exists()]
add('AX01','AppLovin与MMP官方partner配置、事件映射与checkout语义',
 ['axon/VERIFIED_SOURCES.json']+axpaths(['doc-set-up-mmp-tracking','doc-adjust','doc-appsflyer','adjust-applovin','af-campaign','af-max-revenue']),
 '通用集成文档，不是目标游戏投放记录。AppLovin自身文档明确checkout排除广告收入/预测LTV；Adjust/AF后台需partner启用、来源范围及映射。')
add('AX02','当前AppLovin获客目标、MAX前提与流量类型',axpaths(['gaming-apps','game-inventory','doc-scale-your-campaign']),
 'IAA/IAP/Blended/CPP/CPE及MMP流程、视频/关间/奖励库存；官网营销数字不是目标游戏投放量。')
add('AX03','AppLovin隐私披露与Ad Review用途边界',axpaths(['applovin-privacy','blog-data-boundary']),
 '政策披露跨应用/设备及MMP数据类别；2026-09-16公司明确声明Ad Review不进入Axon。公开声明非独立生产审计。')
add('AX04','真实投放证据搜索范围、失败与不可移植的其他产品记录',
 ['axon/fetches-initial.json','axon/fetches-discovery.json','axon/fetches-focused.json','axon/fetches-final.json','axon/inventory-asset-observations.json','axon_final_sources.py']+
 axpaths(['doc-top-creative-library','bing-ikame','bing-meow','bing-car','bing-rotate','bing-jewel','bing-amaze','bing-zego','search-ddg-oakever','search-ddg-car','search-ddg-jewel','search-ddg-rotate','search-ddg-meow','search-ddg-amaze','brave-oakever','brave-targets','sensortower-car','appmagic-car']),
 '未取得五款目标游戏×AppLovin的可靠付费投放记录；搜索挑战/429/错配/前端壳不能作正面证据。inventory的Oakever/iKame资源是其他产品和供给页线索。')
add('AX05','AppLovin追踪宏字段',axpaths(['doc-tracking-url-macros']),
 'campaign/创意/国家/展示应用/placement/eventID为公开支持宏，不证明目标活动使用。')
add('TP01','独立官方SDK原始材料、来源、许可与SHA256',
 sdkpaths('*/*/*/provenance.json')+sdkpaths('*/*/*/*.aar')+sdkpaths('*/*/*/*-sources.jar')+sdkpaths('*/*/*/github-source-*.zip')+
 ['ThirdPartySDKs/CATALOG.json','ThirdPartySDKs/COLLECTION_VALIDATION.json','ThirdPartySDKs/ARTIFACT_VALIDATION.json','ThirdPartySDKs/ORIGINAL_SAMPLE_INTEGRITY.json','ThirdPartySDKs/EMBEDDED_ONLY.json','ThirdPartySDKs/ADAPTER_COVERAGE.json','ThirdPartySDKs/collect_sdk.py','ThirdPartySDKs/collect_more.py','ThirdPartySDKs/collect_matched.py','ThirdPartySDKs/collect_discovered.py','ThirdPartySDKs/collect_detected_adapters.py','ThirdPartySDKs/finish_dependency_collection.py','ThirdPartySDKs/DETECTED_ADAPTER_MANIFEST.json','ThirdPartySDKs/DETECTED_DEPENDENCY_MANIFEST.json'],
 '公开Maven/厂商仓库/JitPack及官方GitHub来源；POM许可证≠任意再分发授权。Last-Modified与仓库lastUpdated非首次发布日期。Bulldog/Meevii为嵌入样本，Amaze无包。')
audits=sdkpaths('Embedded/*/audit.json');bodies=sdkpaths('Embedded/*/method-bodies/**/*.txt')
add('TP02','四款内置SDK版本、原始DEX方法与官方API声明差分',
 audits+bodies+['ThirdPartySDKs/VERSION_MATCHES.json','ThirdPartySDKs/API_COMPARISON.json','ThirdPartySDKs/compare_and_index.py','ThirdPartySDKs/embedded_scan.py','ThirdPartySDKs/repair_overload_evidence.py']+sdkpaths('*/*/*/api-comparison/*.txt'),
 'MAX分别13.6.4/13.2.0/13.6.2/13.6.3；Adjust5.5/5.7；AF6.14.2/6.17.5。183个选定声明匹配，不宣称方法体或整个SDK相同；方法文件包含descriptor哈希防重载覆盖。')
add('TP03','MAX收入/公开API与13.2/13.6.4 Axon事件协议差分',
 sdkpaths('AppLovin/MAX/*/decompiled/**/*.java')+sdkpaths('AppLovin/MAX/13.6.4/focused/**/*.java')+sdkpaths('AppLovin/MAX/13.6.4/sources/com/applovin/mediation/*.java'),
 '13.6.4 EventServiceImpl条件化v1/app Axon载荷、axon_events默认表、dedupe/user_data/visitInfo；旧4.0/pix分支仍保留。13.2同类无新分支。MAX收入需保留precision；库能力不等于业务启用或Axon模型。')
add('TP04','Adjust匹配发行版源码的收入/事件/归因包与持久队列',
 [f'ThirdPartySDKs/Adjust/Android/{v}/sources/com/adjust/sdk/{c}.java' for v in ['5.5.0','5.7.0'] for c in ['PackageBuilder','PackageHandler','ActivityHandler','AdjustConfig','Adjust','AdjustAttribution','DeviceInfo','Constants']],
 '独立原始sources；/ad_revenue、partner_params、标识条件、队列落盘/backoff；不等于目标游戏partner送达。')
add('TP05','AppsFlyer匹配发行版API、广告收入载荷和磁盘缓存',
 sdkpaths('AppsFlyer/Android/*/decompiled/**/*.java')+sdkpaths('AppsFlyer/Android/*/focused/**/*.java')+sdkpaths('AppsFlyer/Android/*/final-java/**/*.java')+sdkpaths('AppsFlyer/Android/*/revenue-java/**/*.java')+sdkpaths('AppsFlyer/Android/*/cache-candidates.json'),
 '官方AAR反编译，不称官方开源。AF6.17.5 logAdRevenue数据校验/状态检查，AFf1tSDK adrevenue_sdk编码，APPLOVIN_MAX仅mediation；AFRequestCache分类/限额/淘汰，不宣称恰好一次。')
add('TP06','官方MAX适配器源码与网络依赖POM',
 sdkpaths('AppLovin/Adapter-*/*/sources/**/*.java')+sdkpaths('AppLovin/Adapter-*/*/*.pom'),
 'collectSignal、Google QueryInfo与各网络token、bid response载入能证中介协作；不能证明开发商通过适配网络买量。')
add('TP07','官方SDK用户匹配/标识与隐私条件能力',
 sdkpaths('InMobi/Android/11.1.1/decompiled/**/*.java')+sdkpaths('Meta/FacebookCore/18.0.3/decompiled/**/*.java')+
 ['ThirdPartySDKs/AppLovin/MAX/13.6.4/focused/com/applovin/impl/r7.java','ThirdPartySDKs/AppLovin/MAX/13.6.4/focused/com/applovin/impl/sdk/m.java','ThirdPartySDKs/AppLovin/MAX/13.6.4/focused/com/applovin/sdk/AppLovinUserData.java']+
 [f'ThirdPartySDKs/TikTok/Business/{v}/sources/com/tiktok/appevents/{c}.java' for v in ['1.6.1','1.7.1'] for c in ['TTIdentifierFactory','TTRequestBuilder','TTAppEventLogger','TTAppEventStorage']]+['ThirdPartySDKs/Discovery/tiktok-readme-master.txt'],
 'AppLovin user_data规范化/哈希是条件化能力；InMobi UnifiedID与TikTok标识/队列/受众能力不等于游戏启用；无实际身份数据采集。')
add('TP08','实际游戏到MAX的事件桥/用户ID、来源枚举追踪',
 ['ThirdPartySDKs/BUSINESS_TRACES.json','ThirdPartySDKs/BRIDGE_ANALYSIS.json','ThirdPartySDKs/trace_business.py']+
 sdkpaths('Embedded/*/business-trace/**/*.txt')+sdkpaths('Embedded/*/bridge-java/**/*.java'),
 'Car UnityBridge→MeticaApplovinFunctions.trackEvent但具体游戏价值事件未知；Meow AdUuid→MAX、MediaSourceTag applovin_int枚举；Rotate ThinkingData distinctId→MAX。主DEX未建立AppLovinUserData业务链，负面范围不覆盖native/服务器。')
add('TP09','Metica公开发行渠道、SDK与缺包/来源发现记录',
 ['ThirdPartySDKs/DISCOVERY_MANIFEST.json','ThirdPartySDKs/DISCOVERY_ADDITIONAL.json','ThirdPartySDKs/DISCOVERED_MANIFEST.json','ThirdPartySDKs/METICA_MANIFEST.json']+
 sdkpaths('Discovery/*')+sdkpaths('Metica/Android/2.5.4/final-java/**/*.java'),
 'Metica文档给Maven Central com.metica:metica-sdk；取到2.5.4，未证明Car内准确同版；Learnings/Bulldog独立官方发行包未取得。TikTok官方标签与JitPack匹配。')
new={e['id'] for e in entries};manifest['entries']=[e for e in manifest['entries'] if e['id'] not in new]+entries;manifest['sdk_axons_audit_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();write(ROOT/'EVIDENCE_MANIFEST.json',manifest)
p=ROOT/'EVIDENCE_INDEX.md';s=p.read_text(encoding='utf-8');marker='<!-- SDK_AXON_AUDIT_20261118 -->';s=s.split(marker)[0].rstrip()+'\n\n'+marker+'\n\n## AppLovin与独立SDK增量证据\n\n本轮新增11–19，不改写00–10历史结论；SDK内部能力、游戏业务调用、后台启用、实际投放分别证明。新标签：实际游戏代码/官方SDK代码/官方文档/公开投放证据/合理推断/无法确认；11–13沿用AppLovin专项标签。没有目标产品的已证实AppLovin投放记录。\n\n'
for e in entries:
 s+=f'<a id="{e["id"].lower()}"></a>\n## {e["id"]} · {e["title"]}\n\n{e["notes"]}\n\n'
 # Keep the human index compact; complete file hashes are in the manifest.
 refs=e['sources'];chosen=[x for x in refs if x['path'].endswith('.json') and '/provenance.json' not in x['path']][:12]
 chosen+= [x for x in refs if x['path'].endswith('.java')][:6]
 if not chosen:chosen=refs[:12]
 for x in dict((x['path'],x) for x in chosen).values():s+=f'- [{x["path"]}]({x["path"]})\n'
 s+=f'\n完整逐文件来源及SHA256：EVIDENCE_MANIFEST.json 的 {e["id"]}（{len(refs)}份材料）。\n\n'
p.write_text(s,encoding='utf-8')
print('registered',len(entries),'new groups;',sum(len(e['sources']) for e in entries),'hashed sources')
