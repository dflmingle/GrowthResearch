"""Append evidence for auction research; keep prior studies unchanged."""
from pathlib import Path
import json,hashlib,datetime
ROOT=Path(__file__).resolve().parent.parent
R=ROOT/'auction';utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
fetches=[x for p in sorted(R.glob('fetches-*.json')) for x in json.loads(p.read_text())]
valid={'al-request','al-response','al-introduction','al-dynamics','al-creatives','al-changelog','al-demand-privacy',
       'al-sdk-bidder','unity-response','unity-overview','unity-get-started','unity-ios','unity-loss'}
for x in fetches:
 x['usable_as_requested_document']=x['id'] in valid and x.get('status')==200
 if not x['usable_as_requested_document']:
  x['limitation']='Failed candidate: HTTP error, soft-404 or redirect to generic/home page; not protocol evidence.'
(R/'PUBLIC_SOURCE_INDEX.json').write_text(json.dumps(fetches,ensure_ascii=False,indent=2),encoding='utf-8')
byid={x['id']:x for x in fetches}
mfile=ROOT/'EVIDENCE_MANIFEST.json'
m=json.loads(mfile.read_text(encoding='utf-8'))
old={s.get('path'):s for e in m['entries'] if not e.get('id','').startswith('BP') for s in e.get('sources',[]) if s.get('path')}
def source(path):
 p=ROOT/path
 assert p.is_file(),path
 h=hashlib.sha256(p.read_bytes()).hexdigest()
 row=dict(path=path,sha256=h,bytes=p.stat().st_size)
 if path in old:
  prev=old[path]
  if prev.get('sha256'):assert h==prev['sha256'],path
  for key in ['url','final_url','utc','fetched_utc','http_status','status','kind']:
   if key in prev:row[key]=prev[key]
 return row
groups=[]
def add(id,title,claim,paths=(),web=()):
 ss=[source(p) for p in paths]
 for k in web:
  q=byid[k];p='auction/'+k+'.raw';row={**source(p),**q,'path':p}
  assert row['sha256']==hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
  ss.append(row)
 groups.append(dict(id=id,title=title,claim=claim,utc=utc,sources=ss))
add('BP01','AppLovin官方oRTB请求、响应、创意和版本记录','官方协议证实；只针对取得文档，不是Axon服务器实现。',web=[
 'al-introduction','al-request','al-response','al-creatives','al-changelog'])
add('BP02','Unity Exchange请求/响应/超时/loss/隐私与SKAN','官方协议证实；记录版本/tmax/multi-seat歧义，非抓包。',paths=[
 'identity-graph/unity-exchange-identity.raw','identity-graph/unity-exchange-privacy.raw'],web=[
 'unity-overview','unity-response','unity-get-started','unity-ios','unity-loss'])
add('BP03','MAX统一竞价、waterfall合并和SDK bidder入驻','官方公开规则；并非所有中介服务器调度或throttling算法。',web=['al-dynamics','al-sdk-bidder'])
maxfiles=[p.relative_to(ROOT).as_posix() for p in (R/'sdk/MAX-13.6.4').rglob('*.java')]
add('BP04','MAX13.6.4私有请求、signal、waterfall、expiration与反馈','官方SDK静态代码；不是OpenRTB原样透传，没有生产执行。',paths=maxfiles+[
 'ThirdPartySDKs/AppLovin/MAX/13.6.4/classes.jar','auction/MAX_LITERAL_HITS.json','auction/SDK_AUDIT.json','auction/CODE_EVIDENCE.json'])
u='ThirdPartySDKs/Unity/Ads/4.17.0/'
ufiles=[u+'sources/com/unity3d/ads/core/domain/'+n+'.kt' for n in [
 'AndroidGetAdRequest','AndroidBuildHeaderBiddingToken','CommonGetHeaderBiddingToken','AndroidGetUniversalRequestSharedData']]
add('BP05','Unity Ads protobuf请求、竞价token与隐私共享层','官方SDK源码；token为序列化输入，不是模型权重；逐字段服务器转码未知。',paths=ufiles+[
 u+'provenance.json',u+'unity-ads-4.17.0-sources.jar','vector/SDK_AUDIT.json','vector/CODE_EVIDENCE.json'])
lfiles=[p.relative_to(ROOT).as_posix() for p in (R/'sdk/LevelPlay-9.4.0').rglob('*.java')]
add('BP06','LevelPlay9.4.0候选、auction结果、状态和fallback','官方发行包静态代码；JADX大小写重命名保留；未恢复服务器定价。',paths=lfiles+[
 'ThirdPartySDKs/Unity/Dependency-mediation-sdk/9.4.0/classes.jar','auction/sdk/LevelPlay-9.4.0/FOLLOWUP.json'])
add('BP07','身份与隐私字段证据复用','设备广告ID、AppSet、CUID、UPA/RampID分开；未证任意ID自动映射到DSP。',paths=[
 'identity-graph/IDENTITY_CODE_EXCERPTS.json','identity-graph/SDK_IDENTITY_AUDIT.json','vector/exchange-rampid.html',
 '31_AppLovin设备身份图谱.md','32_Unity身份互通与RampID.md','34_跨设备身份关联证据链.md'])
add('BP08','Axon/Vector价值竞价与反馈公开说明','官方定性用途与产品条件；无闭源模型/权重/真实效果排名。',paths=[
 'nongame/applovin-axon-about.raw','nongame/applovin-policy-direct.raw','nongame/doc-order-history.raw',
 'axon/gaming-product.html','axon/gaming-apps.html','axon/doc-set-up-mmp-tracking.html',
 'vector/doc-revenue-bids.html','vector/doc-intro-to-roas-campaigns.html','24_Unity与AppLovin技术对比.md',
 '25_Unity_Runtime数据优势调查.md','20_Axon实际事件调用链.md'])
add('BP09','全部原表字段、规范化差分及文档示例解析','444原表行含辅助表；234核心路径/91双方列出；不是生产字段量或优势排名。',paths=[
 'auction/extract_protocol.py','auction/PROTOCOL_FIELDS.json','auction/PROTOCOL_FIELDS.md',
 'auction/build_diff.py','auction/FIELD_DIFF.json','auction/FIELD_DIFF.md','auction/DOCUMENT_EXAMPLES.json'])
model=[p.relative_to(ROOT).as_posix() for p in (R/'model').glob('*.py')]
model += [p.relative_to(ROOT).as_posix() for p in (R/'model/output').iterdir() if p.is_file()]
add('BP10','本地合成竞价模拟器及实际实验产物','人为模型与协议规则分开；不连接广告网络，结果不代表供应商表现。',paths=model)
add('BP11','采集与逆向范围、失败候选、可重跑验证','合法公开GET/既有SDK静态分析；soft404/跳首页不算协议证据；无生产事件。',paths=[
 'auction/PUBLIC_SOURCE_INDEX.json','auction/collect.py','auction/follow_sources.py','auction/fetch_additional.py',
 'auction/sdk_audit.py','auction/code_evidence.py','auction/build_evidence.py','auction/validate.py']+
 [p.relative_to(ROOT).as_posix() for p in sorted(R.glob('fetches-*.json'))])
m['entries']=[e for e in m['entries'] if not e.get('id','').startswith('BP')]+groups
m['auction_protocol_audit_utc']=utc
mfile.write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf-8')
index=ROOT/'EVIDENCE_INDEX.md';text=index.read_text(encoding='utf-8');marker='<!-- AUCTION_PROTOCOL_2026_11_19 -->'
text=text.split(marker)[0].rstrip()+'\n\n'+marker+'\n'
for e in groups:
 text+=f'\n<a id="{e["id"].lower()}"></a>\n\n## {e["id"]} · {e["title"]}\n\n{e["claim"]}\n\n'
 for s in e['sources']:
  text+=f'- [{s["path"]}]({s["path"]})'
  if s.get('url'):text+=f'；[原始来源]({s["url"]})'
  if 'status' in s:text+=f'；HTTP {s["status"]}'
  text+='\n'
 text+='\n完整SHA256/获取时间/版本与范围见EVIDENCE_MANIFEST.json本组；原代码行号见auction/CODE_EVIDENCE.json。\n'
index.write_text(text,encoding='utf-8')
print('registered',len(groups),'groups',sum(len(g['sources']) for g in groups),'sources')
