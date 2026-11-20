from pathlib import Path
import json,hashlib,datetime
R=Path(__file__).resolve().parent;ROOT=R.parent
sources=json.loads((R/'PUBLIC_SOURCE_INDEX.json').read_text(encoding='utf-8'))
sdk=[p.relative_to(ROOT).as_posix() for p in sorted((R/'sdk/axon/1.3.4').iterdir()) if p.is_file()]
groups=[
 ('NG01','AppLovin 网站事件、GTM/Shopify 接入和隐私要求','官方公开证实；接口要求不是所有商家已启用，隐私约束与事件语义单列。',['doc-events','doc-gtm','doc-shopify','app-shopify','doc-privacy','doc-data-sharing'],[]),
 ('NG02','CAPI、去重、历史客户订单和转化衡量','官方公开证实；没有向生产端点发请求，未读取或使用商家凭证。',['doc-capi','doc-dedupe','doc-order-history','doc-attribution'],[]),
 ('NG03','独立 Axon Android 1.3.4 发行包与非游戏App接口','SDK代码证实为公开API/发行物；文档哈希及匹配语义另列。不是目标App实装版本，也未完整恢复该SDK私有队列/网络。',['doc-android-axon','doc-ios-axon','axon-sdk-metadata','axon-sdk-pom'],sdk),
 ('NG04','9款非游戏 App 的官方政策与商店身份','公开资料证实6款具名、1款发行商级范围、2款未证目标接入；没有APK版本/初始化/生产流量证明。',['utility-zedge','utility-zedge-play','utility-inshot','utility-inshot-play','utility-flashlight-correct','utility-flashlight-play','content-dramabox','content-dramabox-play','content-reelshort-official-policy','content-reelshort-play','content-audiomack-official-policy','content-audiomack-play','life-winwalk','life-winwalk-play','life-weward-correct','life-cashwalk','life-cashwalk-play'],['nongame/SAMPLE_CATALOG.json']),
 ('NG05','3个商家真实网页嵌入与Gruns/Blissy反例边界','公开网页代码证实主题嵌入/配置；未执行脚本或读取购物车。CMP text/plain 和通用来源表不能冒充事件发送。',['site-hexclad','site-hexclad-home','site-resparked','site-resparked-home','site-trueclassic','site-gruns','site-gruns-home','site-blissy','site-ridge','site-obvi'],['nongame/SOURCE_EXCERPTS.json']),
 ('NG06','公开Pixel字符串表、条件采集、匹配分支及Shopify归因资产','公开网页代码证实静态实现；a/1.5.46、496项字符串唯一轮转161；没有执行JS、查询带商家key配置或收集真实邮箱/cookie。',['pixel-source','site-hexclad-embed','site-gruns-loader'],['nongame/analyze_pixel.py','nongame/pixel-string-table.json','nongame/pixel-partial-static.js','nongame/PIXEL_STATIC_EVIDENCE.json']),
 ('NG07','Wurl CTV内容情境与隐私范围','官方公开证实场景标签、观看行为受众和DSP产品能力；媒体观众政策403，企业网站政策明确不适用，不推定Wurl到Axon字段流。',['wurl-home','wurl-advertising','wurl-policy-correct','wurl-media-policy'],[]),
 ('NG08','Unity非游戏/Exchange/外部数据与具名AppLovin竞价伙伴','官方公开证实协议和共享用途声明，未取得逐笔交易；含Player Sign In跨项目能力，不证明广告训练关联。',['unity-policy','unity-exchange-bid-fields','unity-ads-android-native','unity-ddf-external','unity-analytics-correct','unity-analytics-revenue'],[]),
 ('NG09','AppLovin跨数字属性数据与Axon公开模型说明','官方公开证实跨app/网站个性化能力、广告主自愿数据及自身MAX win/loss；明示排除其他竞价者用户/出价和敏感/特定受保护类别。不是商家到游戏IAA的逐字段训练证明。',['applovin-policy-direct','applovin-axon-about','consumer-brands'],[]),
 ('NG10','本轮采集方法、候选失败与静态证据目录','包含403/429/404/搜索壳及错误重定向；抓取数量不是有效证据数量。无生产事件或设备访问。',[],['nongame/PUBLIC_SOURCE_INDEX.json','nongame/build_evidence.py','nongame/collect.py','nongame/download_axon.py']+[p.relative_to(ROOT).as_posix() for p in sorted(R.glob('fetches-*.json'))]),
]
manifest_path=ROOT/'EVIDENCE_MANIFEST.json';manifest=json.loads(manifest_path.read_text(encoding='utf-8'))
assert not any(e['id'].startswith('NG') for e in manifest['entries']), 'already registered; do not overwrite'
sections=['\n<!-- NON_GAME_ECOSYSTEM_2026_11_19 -->\n']
for eid,title,notes,ids,extra in groups:
 records=[]
 for k in ids:
  row=sources[k]
  for suffix in ['.raw','.txt','-scripts.json','-links.json']:
   p=R/(k+suffix)
   if not p.is_file():continue
   records.append({'path':p.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'url':row['url'],'final_url':row.get('final_url'),'fetched_utc':row['utc'],'http_status':row.get('status'),'scope':'raw response' if suffix=='.raw' else 'derived static artifact'})
 for rel in extra:
  p=ROOT/rel;assert p.is_file(),rel
  records.append({'path':rel,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
 manifest['entries'].append({'id':eid,'title':title,'notes':notes,'sources':records})
 sections+=['<a id="'+eid.lower()+'"></a>\n','## '+eid+' · '+title+'\n',notes+'\n']
 for k in ids:
  row=sources[k];sections.append('- ['+k+' 原始来源]('+row['url']+')；[本地快照](nongame/'+k+'.raw)；HTTP '+str(row.get('status','ERROR')))
 for rel in extra:sections.append('- ['+rel+']('+rel+')')
 sections.append('\n完整SHA256及抓取时间见 EVIDENCE_MANIFEST.json 的 '+eid+'。\n')
manifest['utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
with (ROOT/'EVIDENCE_INDEX.md').open('a',encoding='utf-8') as f:f.write('\n'.join(sections)+'\n')
print('Appended',len(groups),'groups;',sum(len(e['sources']) for e in manifest['entries'] if e['id'].startswith('NG')),'new hashes')
