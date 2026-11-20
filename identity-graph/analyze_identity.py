"""Static-only identity evidence extraction. No SDK/JS execution or device access."""
from pathlib import Path
import json, hashlib, re

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'identity-graph'
rows=[]
def excerpt(label, path, start, end):
    p=ROOT/path
    lines=p.read_text(encoding='utf-8').splitlines()
    rows.append(dict(id=label,path=path,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),
                     start_line=start,end_line=min(end,len(lines)),
                     text='\n'.join(f'{i+1}: {s}' for i,s in enumerate(lines) if start<=i+1<=end)))

mx='identity-graph/sdk/max-13.6.4/java/com/applovin/'
ax='identity-graph/sdk/axon-1.3.4/java/com/applovin/'
au='identity-graph/sdk/authentication/3.9.0/extracted/package/'
for args in [
 ('MAX-GAID',mx+'impl/v.java',87,143),
 ('MAX-AppSet-start',mx+'impl/i1.java',1,19),
 ('MAX-AppSet-result',mx+'impl/i1$a.java',1,35),
 ('MAX-device-payload',mx+'impl/sdk/m.java',1328,1366),
 ('MAX-app-payload',mx+'impl/sdk/m.java',884,925),
 ('MAX-user-normalization',mx+'impl/r7.java',24,178),
 ('MAX-structured-device',mx+'impl/y6.java',1,85),
 ('MAX-cuid-manager',mx+'impl/t7.java',1,190),
 ('AXON-appset-result',ax+'impl/g0.java',1,30),
 ('UPA-oauth-start',au+'Player Accounts/Runtime/PlayerAccountServiceInternal.cs',63,89),
 ('UPA-oauth-request',au+'Player Accounts/Runtime/PlayerAccountServiceInternal.cs',154,185),
 ('UPA-oauth-result',au+'Player Accounts/Runtime/PlayerAccountServiceInternal.cs',229,273),
 ('UPA-id-claims',au+'Player Accounts/Runtime/Models/IdToken.cs',1,70),
 ('UGS-external-link',au+'Runtime/AuthenticationServiceInternal.External.cs',327,425),
 ('UGS-project-context',au+'Runtime/Network/AuthenticationNetworkClient.cs',110,155),
 ('UGS-token-scope',au+'Runtime/Models/Security/AccessToken.cs',1,50),
 ('UGS-unity-id',au+'Runtime/Models/PlayerInfo.cs',185,250),
 ('UGS-identity-model',au+'Runtime/Models/Identity.cs',1,40),
 ('UGS-network-endpoints',au+'Runtime/Network/AuthenticationNetworkClient.cs',15,40),
 ('AXON-user-normalization',ax+'impl/l3.java',25,158),
 ('UNITY-ads-privacy','vector/sdk/Unity/Ads/4.18.1/java/com/unity3d/services/core/device/reader/DeviceInfoReaderWithPrivacy.java',20,50),
 ('UNITY-ads-identity-repository','ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/data/repository/AndroidDeviceInfoRepository.kt',20,60),
 ('UNITY-ads-idfi-auid','ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/data/datasource/AndroidStaticDeviceInfoDataSource.kt',213,246),
 ('UNITY-ads-analytics-source','ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/data/datasource/AndroidAnalyticsDataSource.kt',1,20),
 ('UNITY-ads-initialization-identities','ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/domain/AndroidGetInitializationRequestPayload.kt',26,132),
 ('UNITY-ads-shared-privacy','ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/domain/AndroidGetUniversalRequestSharedData.kt',18,40),
 ('UNITY-ads-PII-gates','ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/data/datasource/AndroidPrivacyDeviceInfoDataSource.kt',20,58),
 ('UGS-PlayerId-token','identity-graph/sdk/authentication/3.9.0/extracted/package/Runtime/AuthenticationServiceInternal.cs',434,451),
]:excerpt(*args)
(OUT/'IDENTITY_CODE_EXCERPTS.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')

# Annotated bounded snippets: replace aliases only where explicitly listed per snippet.
# The original snippet and original offsets remain authoritative. Derivative is not runnable JS.
s=(ROOT/'nongame/pixel-source.raw').read_text(encoding='utf-8')
mapping=json.loads((ROOT/'nongame/pixel-string-table.json').read_text())['mapping']
specs=[
 ('constants','j=w(182)',900,['w']),
 ('cookie-write','function Ie(',1100,['w','i']),
 ('wrt-format','function Ae(',440,['w','t']),
 ('user-data','async function Oe(',1550,['w','t']),
 ('auto-email','function Me(',1500,['w']),
 ('payload','function We(',4200,['w','l','d']),
 ('initial-ids','g.wrt=',2300,['w']),
 ('wrt-precedence','let O,N=',2000,['w']),
 ('cookie-match','let Qe=_e(K)',600,['w']),
 ('optional-config','r=(_=',650,['w','t','r']),
]
pr=[]
for label,needle,length,aliases in specs:
    pos=s.find(needle)
    if pos<0:
        if label=='initial-ids':
            pos=s.find('g[w(441)]=')
        elif label=='optional-config':
            pos=s.rfind('.then(e=>')
            length=1500;aliases=['w','t','r']
    if pos<0:
        pr.append({'id':label,'needle':needle,'found':False});continue
    raw=s[pos:pos+length]
    pattern=r'\b(?:a0_0x5ab4|'+ '|'.join(aliases) +r')\((\d+)\)' if aliases else r'\ba0_0x5ab4\((\d+)\)'
    annotated=re.sub(pattern,lambda m:json.dumps(mapping[m[1]],ensure_ascii=False),raw)
    pr.append(dict(id=label,source='nongame/pixel-source.raw',source_sha256=hashlib.sha256(s.encode()).hexdigest(),
                   character_offset=pos,original=raw,aliases_reviewed=aliases,
                   annotation=annotated,limitation='Bounded static annotations; nested aliases not listed stay unresolved. No execution; no production config.'))
(OUT/'PIXEL_IDENTITY_EXCERPTS.json').write_text(json.dumps(pr,ensure_ascii=False,indent=2),encoding='utf-8')
print('code excerpts',len(rows),'pixel excerpts',len(pr),'found',sum(x.get('found',True) for x in pr))
for x in pr:
    if x.get('found',True):print('\nPIXEL',x['id'],x['character_offset'],'\n',x['annotation'][:4300])
