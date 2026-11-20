"""Add identity-research evidence without replacing earlier research entries."""
from pathlib import Path
import json,hashlib,datetime

R=Path(__file__).resolve().parent.parent
G=R/'identity-graph'
utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
fetches=[x for p in sorted(G.glob('fetches-*.json')) for x in json.loads(p.read_text(encoding='utf-8'))]
byid={x['id']:x for x in fetches}
def local(p):
    f=R/p
    assert f.is_file(),p
    return dict(path=p,sha256=hashlib.sha256(f.read_bytes()).hexdigest(),bytes=f.stat().st_size)

groups=[]
def add(id,title,claim,files=(),web=()):
    sources=[local(str(p)) for p in files]
    for key in web:
        q=byid[key]
        row={**q,'path':f'identity-graph/{key}.raw'}
        if (R/row['path']).exists():
            actual=local(row['path']);assert actual['sha256']==q['sha256'],key
        sources.append(row)
    groups.append(dict(id=id,title=title,claim=claim,sources=sources,utc=utc))

mx='identity-graph/sdk/max-13.6.4/java/'
ax='identity-graph/sdk/axon-1.3.4/java/'
au='identity-graph/sdk/authentication/3.9.0/'
ua='ThirdPartySDKs/Unity/Ads/4.17.0/'
add('IG01','MAX Android设备ID、App Set与发布者/客户资料','官方SDK静态代码；字段封装不是服务端图谱或目标游戏发送成功。',
 [str(p.relative_to(R)).replace('\\','/') for p in (R/mx).rglob('*.java')]+['ThirdPartySDKs/AppLovin/MAX/13.6.4/classes.jar','identity-graph/SDK_IDENTITY_AUDIT.json'])
add('IG02','独立Axon1.3.4身份能力','官方独立发行物，非目标游戏实装证明；静态分析不含网络执行。',
 [str(p.relative_to(R)).replace('\\','/') for p in (R/ax).rglob('*.java')]+['nongame/sdk/axon/1.3.4/provenance.json','nongame/sdk/axon/1.3.4/classes.jar'])
add('IG03','Pixel访客/点击/客户键与条件采集','公开网页代码证实；原始偏移和SHA保留；未执行JS或查询商家配置。',
 ['nongame/pixel-source.raw','nongame/pixel-string-table.json','identity-graph/PIXEL_IDENTITY_EXCERPTS.json','identity-graph/analyze_identity.py'])
add('IG04','CAPI及订单历史的身份与价值建模用途','官方接口要求及建模目的，不是某用户的实际匹配或训练记录。',
 ['nongame/doc-capi.raw','nongame/doc-order-history.raw','nongame/doc-attribution.raw','nongame/doc-data-sharing.raw'])
add('IG05','AppLovin跨属性结合及Axon数据使用范围','官方政策/产品说明正证据；不证明目标游戏投放或电商到游戏的逐字段训练。',
 ['nongame/applovin-policy-direct.raw','nongame/applovin-axon-about.raw'],['applovin-how-ads'])
add('IG06','平台ID作用域、ATT及cookie matching边界','Google/Apple官方资料；同设备scope与跨设备账户严格区分。',web=[
 'google-appset-guide','google-appset-correct','google-ads-id','apple-idfv-data','apple-idfa-data','apple-att','google-cookie-match'])

authfiles=[str(p.relative_to(R)).replace('\\','/') for p in (R/au).iterdir() if p.is_file()]
authfiles += [au+'extracted/package/'+p for p in [
 'LICENSE.md','package.json','Player Accounts/Runtime/PlayerAccountServiceInternal.cs','Player Accounts/Runtime/Models/IdToken.cs',
 'Runtime/AuthenticationServiceInternal.cs','Runtime/AuthenticationServiceInternal.External.cs','Runtime/Network/AuthenticationNetworkClient.cs',
 'Runtime/Models/Identity.cs','Runtime/Models/PlayerInfo.cs','Runtime/Models/Security/AccessToken.cs']]
unityfiles=[ua+'provenance.json',ua+'unity-ads-4.17.0-sources.jar']
unityfiles += [ua+'sources/com/unity3d/ads/core/'+p for p in [
 'data/datasource/AndroidAnalyticsDataSource.kt','data/datasource/AndroidStaticDeviceInfoDataSource.kt',
 'data/datasource/AndroidPrivacyDeviceInfoDataSource.kt','data/datasource/AndroidAppSetIdDataSource.kt',
 'data/repository/AndroidDeviceInfoRepository.kt','domain/AndroidGetInitializationRequestPayload.kt','domain/AndroidGetUniversalRequestSharedData.kt']]
unityfiles += ['vector/sdk/Unity/Ads/4.18.1/java/com/unity3d/services/core/device/reader/DeviceInfoReaderWithPrivacy.java']
add('IG07','Unity Authentication3.9.0官方源包与Unity Ads身份桥接','官方代码；UPA/UGS/LevelPlay AUID/Analytics ID不混同；不是目标游戏启用。',authfiles+unityfiles+['identity-graph/IDENTITY_CODE_EXCERPTS.json'])
add('IG08','Unity账号互通、身份管理及产品专用隐私角色','官方组织级/跨设备能力；无账号到广告图谱或Vector的直接连接证明。',web=[
 'unity-player-accounts','unity-upa-doc-md','unity-anonymous','unity-code-link','unity-openid','unity-identity-management',
 'unity-auth-privacy-overview','unity-upa-privacy-overview','unity-upa-data-safety'])
add('IG09','Unity Exchange RampID及LiveRamp身份能力','官方美加受众激活，需要双方支持；不证明UPA映射、每个请求或Vector训练。',
 ['vector/exchange-rampid.html','vector/exchange-rampid.txt'],['liveramp-rampid-product','liveramp-identity','liveramp-identity-graph'])
add('IG10','Unity竞价身份字段、同意信号与IAB标准','Unity取得文档没有RampID wire字段；IAB标准不能充当Unity已用eids证明。',web=[
 'unity-exchange-identity','unity-exchange-privacy','iab-openrtb-26'])
add('IG11','既有游戏业务ID及事件路径复用','实际游戏静态调用与MMP/MAX不同路径；不把单应用关联升级成跨应用账号图谱。',
 ['20_Axon实际事件调用链.md','21_MAX用户ID与身份数据流.md','22_AppLovin事件协议版本差分.md',
 'axon/deep/native-car/method-evidence.json','axon/deep/native-car/user-id-intermediate-check.json','axon/deep/metica-car-index.json'])
add('IG12','身份专项采集记录与失败边界','包含404/403/错误候选；仅合法公开GET和静态分析，无设备/生产事件/真实ID。',
 [str(p.relative_to(R)).replace('\\','/') for p in sorted(G.glob('fetches-*.json'))]+[
 'identity-graph/collect.py','identity-graph/decompile_ids.py','identity-graph/download_auth.py','identity-graph/build_evidence.py','identity-graph/validate.py'])

# Reused sources have their URL and UTC in older groups; copy exact metadata where possible.
manifestpath=R/'EVIDENCE_MANIFEST.json'
manifest=json.loads(manifestpath.read_text(encoding='utf-8'))
oldmeta={s.get('path'):s for e in manifest['entries'] if not e.get('id','').startswith('IG') for s in e.get('sources',[]) if s.get('path')}
for e in groups:
    for s in e['sources']:
        old=oldmeta.get(s['path'],{})
        if old.get('sha256') and s.get('sha256'):assert old['sha256']==s['sha256'],s['path']
        for key in ['url','final_url','utc','status','last_modified','fetched_utc','http_status']:
            if key in old and key not in s:s[key]=old[key]
manifest['entries']=[e for e in manifest['entries'] if not e.get('id','').startswith('IG')]+groups
manifest['identity_graph_audit_utc']=utc
manifestpath.write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
indexpath=R/'EVIDENCE_INDEX.md'
text=indexpath.read_text(encoding='utf-8')
marker='<!-- IDENTITY_GRAPH_2026_11_19 -->'
text=text.split(marker)[0].rstrip()+'\n\n'+marker+'\n'
for e in groups:
    text+=f'\n<a id="{e["id"].lower()}"></a>\n\n## {e["id"]} · {e["title"]}\n\n{e["claim"]}\n\n'
    for s in e['sources']:
        text+=f'- [{s["path"]}]({s["path"]})'
        if s.get('url'):text+=f'；[原始来源]({s["url"]})'
        if 'status' in s:text+=f'；HTTP {s["status"]}'
        text+='\n'
    text+='\n完整SHA256、来源和抓取时间见EVIDENCE_MANIFEST.json本组；SDK版本边界及未知服务器连接见31–34号报告。\n'
indexpath.write_text(text,encoding='utf-8')
print('Added',len(groups),'groups;',sum(len(x['sources']) for x in groups),'sources')
