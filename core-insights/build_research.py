"""Auditable static research artifacts. Does not import/initialize any SDK."""
from pathlib import Path
import json, hashlib, re, datetime

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'core-insights'
NOW = datetime.datetime.now(datetime.timezone.utc).isoformat()
CORE = 'core-insights/sdk/core/1.19.0/extracted/package/'
IAP = 'cross-sdk/packages/purchasing/5.5.1/extracted/package/'
AN = 'cross-sdk/packages/services.analytics/6.3.0/extracted/package/'
AUTH = 'identity-graph/sdk/authentication/3.9.0/extracted/package/'

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def dump(p, obj):
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', 'utf-8')

def text(rel):
    return (ROOT / rel).read_text('utf-8-sig')

packages = {}
for name, folder, version in [
    ('Core', 'core-insights/sdk/core/1.19.0', '1.19.0'),
    ('IAP', 'cross-sdk/packages/purchasing/5.5.1', '5.5.1'),
    ('Analytics', 'cross-sdk/packages/services.analytics/6.3.0', '6.3.0'),
    ('Authentication', 'identity-graph/sdk/authentication/3.9.0', '3.9.0'),
]:
    b = ROOT / folder
    archive = next(b.glob('*.tgz'))
    prov = json.loads((b / 'provenance.json').read_text('utf-8'))
    assert sha(archive) == prov['sha256'], name
    package_meta = json.loads((b / 'extracted/package/package.json').read_text('utf-8-sig'))
    assert package_meta['version'] == version
    packages[name] = dict(sdk=package_meta['name'], version=version,
        path=archive.relative_to(ROOT).as_posix(), sha256=sha(archive),
        url=prov['url'], registry_time=prov.get('registry_time'),
        dependencies=package_meta.get('dependencies'),
        license=package_meta.get('license', 'see package LICENSE.md'),
        scope='official standalone SDK; not proof of target-game integration')

specs = [
 ('01','Core',CORE+'Runtime/Registration/CorePackageInitializer.cs','CorePackageInitializer.InitializeComponents/InitializeInstallationId',111,199,'Core registers two separate installation providers; initializes installation before project configuration.'),
 ('02','Core',CORE+'Runtime/Device/InstallationId.cs','InstallationId.CreateIdentifier/GetOrCreateIdentifier',7,91,'Existing UnityInstallationId wins; otherwise copy engine ID; legacy fallback only when engine ID empty.'),
 ('03','Core',CORE+'Runtime/Device/EngineInstallationId.cs','EngineInstallationId.GetOrCreateIdentifier/CreateIdentifier',7,53,'Engine API under compile symbol; otherwise unity_connect.installation_id or new GUID.'),
 ('04','Core',CORE+'Runtime/Device/UserIdProviders/UnityEngineIdentifier.cs','UnityEngineIdentifier.UserId',5,18,'Explicit wrapper reads injected IEngineInstallationId; setter is no-op.'),
 ('05','Core',CORE+'Runtime/Core/ExternalUserIdProperty.cs','ExternalUserIdProperty.UserId/Dispose',8,55,'Conditional native userId alias vs memory-only fallback; subscription disposed.'),
 ('06','Core',CORE+'Runtime/Configuration/ExternalUserId.cs','ExternalUserId.UserId/UserIdChanged',6,14,'IExternalUserId resolves shared UnityServices.ExternalUserIdProperty.'),
 ('07','Core',CORE+'Runtime/Core/Unity.Services.Core.asmdef','versionDefines',1,None,'Exact version intervals for UNITY_SUPPORTS_IDENTIFIERS_USER_ID; platform flag separately required.'),
 ('08','Core',CORE+'Runtime/Core/UnityServices.cs','UnityServices.ExternalUserId/ResetStaticsOnLoad',79,106,'Native branch persistence is documented; fallback memory; reset disposes/replaces property.'),
 ('09','Core',CORE+'Runtime/Device/UserIdProviders/UnityAdsIdentifier.cs','UnityAdsIdentifier.UserId',3,47,'Legacy Ads IDFI uses application private preferences, not GAID.'),
 ('10','Core',CORE+'Runtime/Device/UserIdProviders/UnityAnalyticsIdentifier.cs','UnityAnalyticsIdentifier.UserId',6,25,'Legacy unity.cloud_userid read/write fallback.'),
 ('11','Core',CORE+'Runtime/Device/UserIdProviders/AndroidUtils.cs','AndroidUtils.GetSharedPreferences/SharedPreferencesPutString',7,74,'current Activity context; MODE_PRIVATE; not shared cross-app storage.'),
 ('12','Authentication',AUTH+'Runtime/Core/AuthenticationPackageInitializer.cs','AuthenticationPackageInitializer.InitializeService',77,149,'PlayerIdComponent registered by Authentication, not Core; Engine ID also used by network client.'),
 ('13','Authentication',AUTH+'Runtime/Models/Components/PlayerIdComponent.cs','PlayerIdComponent',6,None,'player_id cache; Clear/Refresh/set and change callback.'),
 ('14','Authentication',AUTH+'Runtime/Utilities/Cache/AuthenticationCache.cs','AuthenticationCache.Prefix/GetKey',7,76,'Cache prefix is CloudProjectId.Profile; not global account/device scope.'),
 ('15','Authentication',AUTH+'Runtime/AuthenticationServiceInternal.cs','AuthenticationServiceInternal.SignOut/SwitchProfile',224,261,'SignOut clears PlayerId only if clearCredentials; profile switch refreshes cache.'),
 ('16','Authentication',AUTH+'Runtime/AuthenticationServiceInternal.cs','AuthenticationServiceInternal sign-in completion',425,450,'PlayerId assigned from decoded token Subject, distinct from engine installation ID.'),
 ('17','Analytics',AN+'Runtime/AnalyticsService.cs','AnalyticsService.Initialize',49,105,'IInstallationId/IPlayerId/IExternalUserId consumers and project/environment collect URL.'),
 ('18','Analytics',AN+'Runtime/IdentityManager.cs','IdentityManager constructor/Initialize/ExternalUserIdChanged',22,139,'InstallId captured; UserId external-first; PlayerId live read; local migration and identity change.'),
 ('19','Analytics',AN+'Runtime/Runtime/BufferX.cs','BufferX.PushStandardEventStart/PushCommonEventStart',366,414,'Standard-event installationID/playerID vs common userID/sessionID/eventUUID; not every custom event contains every ID.'),
 ('20','IAP',IAP+'Runtime/Stores/ServicesCore/CoreRegistryHelper.cs','CoreRegistryHelper.InstallationId/Resolve',27,56,'IAP InstallationId property explicitly resolves IEngineInstallationId; optional player/external components.'),
 ('21','IAP',IAP+'Runtime/Stores/Data/PlayerData.cs','PlayerData.CreatePlayerIdentityAsync/FetchEnabledFirebaseIdsAsync',90,215,'AdsIntent/allowlist gated GAID/IDFA/Firebase; IDFV independent; session preference; per-instance caches.'),
 ('22','IAP',IAP+'Runtime/Stores/Data/Insights/PurchaseEventEmitter.cs','PurchaseEventEmitter.Send*Event',44,162,'Intent/paid/failed/fulfilled/payment options SDK callbacks; fire-and-forget.'),
 ('23','IAP',IAP+'Runtime/Stores/Data/Insights/PurchaseEventEmitter.cs','PurchaseEventEmitter.Forward/ForwardModule/ForwardGateway',188,239,'Compile-time exclusive routes; protobuf POST vs base64 LogEvent(1000); no per-event ACK/retry in wrapper.'),
 ('24','IAP',IAP+'Runtime/Stores/Data/Insights/PurchaseEventEmitter.cs','PurchaseEventEmitter.BuildEnvelope/MapIdentity/BuildSku',243,423,'UUID/time; identity mappings; metadata price * 1e6; quantity separate; UnityAdsIdfi not assigned.'),
 ('25','IAP',IAP+'Runtime/Stores/Data/Insights/PurchaseEventProtobufWriter.cs','PurchaseEventProtobufWriter complete serializer',14,None,'Exact emitted field numbers/wire forms and submessages; no original .proto bundled.'),
 ('26','IAP',IAP+'Runtime/Stores/Data/Insights/Models/IAPSDKEvent.cs','IAPSDKEvent and lifecycle variants',1,None,'Envelope and enum definitions; six oneof alternatives, not six revenue events.'),
 ('27','IAP',IAP+'Runtime/Stores/Data/Insights/Models/PlayerIdentity.cs','PlayerIdentity',1,None,'Optional identity DTO fields; schema presence alone does not populate them.'),
 ('28','IAP',IAP+'Runtime/Stores/Data/ConnectionsSettingsClient.cs','ConnectionsSettingsClient.CachedEnabledAttributes/ParseEnabledAttributes/PostAsync',15,186,'Fail-closed per-session allowlist and project/install request; not event-level ACK.'),
 ('29','IAP',IAP+'Runtime/Purchasing/Stores/Android/AAR/FirebaseAnalyticsClient.cs','FirebaseAnalyticsClient getters',60,156,'Firebase Analytics AppInstanceId/SessionId and Firebase App options ApplicationId; not FirebaseInstallations FID.'),
 ('30','IAP',IAP+'Runtime/Stores/Data/Insights/SessionEventEmitter.cs','SessionEventEmitter.SendAuthenticationCompleteEvent/BuildEnvelope',18,80,'SignedIn creates a real DTO/writer path; no store/order; not a purchase label.'),
 ('31','IAP',IAP+'Runtime/Stores/ServicesCore/IapCoreInitializeCallback.cs','IapCoreInitializeCallback.InitializeSessionEvents/PrefetchConnectionsSettings',24,113,'Conditional Authentication.SignedIn subscription and reset cleanup; allowlist prefetch.'),
 ('32','IAP',IAP+'Runtime/Purchasing/Insights/ImpressionScope.cs','ImpressionScope',8,116,'impression_id is AsyncLocal purchase-journey GUID, not an ad impression ID.'),
 ('33','IAP',IAP+'Editor/AssemblyInfo.cs','RequiresInsights assembly declaration',9,17,'Conditional package requirement registration.'),
 ('34','IAP',IAP+'Runtime/Stores/Unity.Purchasing.Stores.asmdef','versionDefines',1,None,'Exact SDK feature/Insights compile-time version definitions.'),
 ('35','Runtime','core-insights/EngineDiagnostics-6000-7.raw','EngineDiagnostics.LogEvent/IsEventAllowed/SetBlockedEventTypes',14,79,'Pinned 6000.7 C# boundary; native queue/receiver/ACK not public.'),
 ('36','Runtime','core-insights/Identifiers-6000-7.raw','Identifiers.installationId/userId',13,55,'Native installation getter/userID setter; 1024-char limit; persistence documented but native store invisible.'),
 ('37','Runtime','core-insights/RequiresInsights-6000-7.raw','RequiresInsightsAttribute/CollectionRequirement',11,70,'Package requirement kept even if Engine Diagnostics project setting disabled; unsupported platforms excluded.'),
 ('38','Runtime','core-insights/Identifiers-6000-6.raw','Identifiers 6000.6 binding',10,57,'Separate pinned 6000.6 branch, not assumed identical to target-engine patch.'),
 ('39','Runtime','core-insights/EngineDiagnostics-6000-6.raw','EngineDiagnostics 6000.6 binding',11,39,'Public native interface exists before IAP new routing gate; availability != chosen SDK route.'),
 ('40','Document','core-insights/iap-privacy-overview.txt','Unity IAP privacy overview',24,145,'Default purchase telemetry; optional consent-gated IDs; IAP operation and revenue reporting; 6000.7 Insights; retention and roles.'),
 ('41','Core',CORE+'CHANGELOG.md','Core 1.19.0 official changelog',1,65,'Official ExternalUserId engine delegation release statement.'),
 ('42','IAP',IAP+'CHANGELOG.md','IAP 5.5.1/5.4.x official changelog',1,115,'Firebase session serialization fix and Core1.19 dependency; optional connections restrictions.'),
 ('43','Analytics',AN+'Runtime/SessionManager.cs','SessionManager.StartNewSession',12,28,'Analytics session is generated GUID; no equality to IAP unity_connect.session_id.'),
 ('44','IAP',IAP+'Runtime/Purchasing/Core/Purchasing/Android/GooglePlay/Extensions/GooglePlayStoreExtendedPurchaseService.cs','GooglePlayStoreExtendedPurchaseService.Send*Event',45,95,'Actual SDK purchase service overrides invoke emitter.'),
 ('45','IAP',IAP+'Runtime/Stores/Data/AppInstallInfo.cs','AppInstallInfo.GetInstallTimestamp/FetchInstallTimestamp',24,75,'Android firstInstallTime ms -> UTC; iOS directory time approximation; null other platforms.'),
 ('46','IAP',IAP+'Runtime/Purchasing/Insights/PaymentOption.cs','PaymentOption enum',5,20,'Payment options wire values including Webshop; not proof each provider used.'),
 ('47','IAP',IAP+'Runtime/Stores/Data/Insights/Models/Consent.cs','ConsentState/DataCollectionMode',1,None,'Proto consent enum differs from UnityConsent API ordinal values; explicit mapping required.'),
 ('48','IAP',IAP+'Runtime/Stores/Data/Insights/Models/DeviceInfo.cs','DeviceInfo',1,None,'Complete public device-info model; byte quantities and boot-time source require native provider context.'),
 ('49','IAP',IAP+'Runtime/Stores/Data/Insights/Models/OrderData.cs','OrderData/Sku/Store/ProductType',1,None,'Complete public SKU/order schema types and enum values.'),
 ('50','IAP',IAP+'Runtime/Stores/Data/Insights/Models/StorePayload.cs','StorePayload/OwnershipType',1,None,'Store-specific transaction evidence fields and ownership enumeration.'),
 ('51','IAP',IAP+'Runtime/Stores/Data/Insights/Models/EventType.cs','EventType.IapSdk',1,None,'IAP producer type is 1000, distinct from lifecycle oneof field numbers.'),
 ('52','IAP',IAP+'Runtime/Stores/Data/Insights/Models/Reporting.cs','Reporting',1,None,'Platform and bundle ID; application context, not individual identity.'),
 ('53','IAP',IAP+'Runtime/Stores/Data/PlayerData.cs','PlayerData session preference and optional Analytics getter',23,55,'IAP reads engine session preference; Analytics ID getter optional and handles uninitialized services.'),
 ('54','Core',CORE+'Runtime/Registration/CorePackageInitializer.cs','CorePackageInitializer.InitializeExternalUserId',255,273,'Compatibility analytics-user-id option only fills empty ExternalUserId.'),
 ('55','IAP',IAP+'Runtime/Purchasing/Core/Purchasing/PurchaseService.cs','PurchaseService.Purchase/InvokePurchasePendingEvent',250,330,'Real SDK entry starts a purchase journey and intent; pending callback reports paid.'),
]

runtime_manifest = json.loads((OUT/'RUNTIME_PUBLIC_PROVENANCE.json').read_text('utf-8'))
boundary_manifest = json.loads((OUT/'BOUNDARY_ACQUISITION.json').read_text('utf-8'))
public = {x['id']: x for x in runtime_manifest['fetches'] + boundary_manifest}
public['iap-privacy-overview'] = next(x for x in json.loads((OUT/'ACQUISITION.json').read_text('utf-8')) if x['id']=='iap-privacy-overview')
sources=[]
for ident, package, rel, method, first, last, meaning in specs:
    p=ROOT/rel; lines=p.read_text('utf-8-sig').splitlines(); last = min(last or len(lines),len(lines))
    assert 0 < first <= last
    row=dict(id='C53S'+ident,sdk=package,version=packages[package]['version'] if package in packages else 'pinned public branch or dated document',
        path=rel,sha256=sha(p),class_or_method=method,start_line=first,end_line=last,
        excerpt='\n'.join(f'{i}: {lines[i-1]}' for i in range(first,last+1)),meaning=meaning,
        reviewed_utc=NOW,evidence_level='【SDK代码证实】' if package!='Document' else '【官方公开证实】',
        evidence_priority='B' if package!='Document' else 'A',game_business_callsite=False,
        production_delivery=False,server_received=False,model_training_proven=False)
    if package in packages:row['official_package']=packages[package]
    else:
        key=p.stem if package=='Runtime' else 'iap-privacy-overview'
        row['public_source']=public[key]
        row['url']=public[key]['url']
        row['source_date']='2026-11-05' if package=='Document' else 'branch snapshot acquired 2026-11-19; exact patch version not asserted'
    sources.append(row)

# Reconstruct every field actually handled by the public writer. This is an
# analyst descriptor, NOT a recovered original canonical .proto file.
writer=text(IAP+'Runtime/Stores/Data/Insights/PurchaseEventProtobufWriter.cs')
methods={}
matches=list(re.finditer(r'^        static void (\w+)\(([^\n]+)\)\s*$',writer,re.M))
for j,m in enumerate(matches):
    part=writer[m.end():matches[j+1].start() if j+1<len(matches) else len(writer)]
    fields=[]
    pattern=r'Write(OptionalString|String|TimestampField|VarintField|UInt64Field|MessageField)\(s,\s*(\d+),\s*([^\n]+)'
    for f in re.finditer(pattern,part):
        typ,number,expression=f.groups()
        fields.append(dict(number=int(number),wire_type=0 if typ in ('VarintField','UInt64Field') else 2,
            writer=typ,expression=expression.strip().rstrip(';'),
            source_line=writer[:m.end()+f.start()].count('\n')+1))
    if fields:methods[m.group(1)] = dict(signature=m.group(2),fields=fields)
enums={}
models=ROOT/IAP/'Runtime/Stores/Data/Insights/Models'
for p in list(models.glob('*.cs'))+[ROOT/IAP/'Runtime/Purchasing/Insights/PaymentOption.cs']:
    for m in re.finditer(r'enum\s+(\w+)\s*\{([^}]+)\}',p.read_text('utf-8-sig'),re.S):
        enums[m.group(1)] = {k:int(v) for k,v in re.findall(r'(\w+)\s*=\s*(\d+)',m.group(2))}
proto=dict(scope='Analyst reconstruction of all fields emitted by IAP5.5.1 public serializer; original Schemas~ .proto not present in tarball',
    package=packages['IAP'],schema_name='insights.producers.iapsdk.v1alpha1.IAPSDKEvent',schema_version='1',proto_sdk_version='1',
    primitive_rules='proto3 default omission, varint0 and LEN2; timestamp seconds/nanos; one active event variant',
    writer_methods=methods,enums=enums,timestamp={'1':'int64 seconds since Unix epoch','2':'int32 nanos; .NET ticks * 100; precision is not native nanosecond clock precision'},unknown='Canonical proto reserved fields/options and server validation/normalization are not recovered')
dump(OUT/'PROTOCOL_SCHEMA.json',proto)
dump(OUT/'CODE_EVIDENCE.json',sources)
dump(OUT/'PACKAGE_PROVENANCE.json',packages)
catalog=['# 53—55 原始代码证据目录','', '仅静态读取官方发行包与固定提交公开绑定；未运行 SDK，未读取设备标识，未发送生产事件。', '']
for s in sources:
    catalog += [f"<a id=\"{s['id'].lower()}\"></a>",f"## {s['id']} · {s['class_or_method']}", '',
        f"[{s['path']}:L{s['start_line']}]({s['path'].removeprefix('core-insights/') if s['path'].startswith('core-insights/') else '../'+s['path']}) · {s['sdk']} {s['version']}",
        '',s['meaning'],'',f"文件 SHA256：`{s['sha256']}`。",'']
    if 'official_package' in s:catalog += [f"原包 SHA256：`{s['official_package']['sha256']}`；[官方来源]({s['official_package']['url']})。",'']
    else:catalog += [f"[公开来源]({s['url']})。",'']
(OUT/'CODE_CATALOG.md').write_text('\n'.join(catalog),'utf-8')
print('Evidence:',len(sources),'serializer groups:',len(methods),'fields:',sum(len(m['fields']) for m in methods.values()))
