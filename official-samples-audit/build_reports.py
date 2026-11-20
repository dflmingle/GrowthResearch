"""First-round reports: license gates and reuse only; not a static SDK analyzer."""
from pathlib import Path
import csv,datetime,hashlib,json,re

R=Path(__file__).resolve().parent.parent
D=Path(__file__).resolve().parent
NOW=datetime.datetime.now(datetime.timezone.utc).isoformat()
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,s):
    assert not p.exists(),p
    p.write_text(s.rstrip()+'\n',encoding='utf-8')
def save(p,x):write(p,json.dumps(x,ensure_ascii=False,indent=2))
def table(p,rs):
    assert rs and not p.exists()
    with p.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rs[0]));w.writeheader();w.writerows(rs)

h=load(D/'HISTORY_BEFORE.json')
for p,s in h.items():assert sha(R/p)==s,p
g=load(D/'EVIDENCE_GRAPH.before.json')
source_map={s['id']:s for s in g['sources']}
fetch={x['id']:x for x in load(D/'FETCH_MANIFEST.json')}
samples=list(csv.DictReader((D/'ACQUIRED_SAMPLE_CATALOG.csv').open(encoding='utf-8-sig')))
assert len(samples)==47
for x in samples:assert sha(R/x['path'])==x['sha256']

candidates=[]
for key,product,fmt in [('al-ios-release','AppLovin MAX iOS','XCFramework_NOT_ACQUIRED'),
                       ('al-unity-release','AppLovin MAX Unity','unitypackage'),
                       ('lp-unity-release','Unity LevelPlay Unity','unitypackage')]:
    f=fetch[key];j=load(R/f['path']);assets=j.get('assets',[])
    # GitHub source zip is not an XCFramework binary; do not substitute it.
    asset=assets[0] if assets else {}
    candidates.append(dict(product=product,version=j['tag_name'],format=fmt,official_release_url=j['html_url'],
      publication_date=j['published_at'],official_download_url=asset.get('browser_download_url','UNKNOWN_NO_CORE_BINARY_ASSET_IN_RELEASE'),
      publisher_digest=asset.get('digest','UNKNOWN'),local_sdk_sha256='NOT_ACQUIRED',
      source_response=f['path'],source_sha256=f['sha256'],
      license_scope='UNKNOWN_EULA_SCOPE' if key.startswith('al-') else 'STOP_UNITY_TERMS_SCOPE_REVIEW',
      acquisition_status='METADATA_ONLY_NO_PACKAGE_DOWNLOAD',analysis_status='NOT_STARTED'))
candidates.append(dict(product='Google official Android mediation adapters',version='UNPINNED_REPOSITORY_SNAPSHOT',format='source_not_acquired',
 official_release_url='https://github.com/googleads/googleads-mobile-android-mediation',publication_date='UNKNOWN',official_download_url='COMMIT_NOT_SELECTED_NO_BUNDLE_DOWNLOAD',
 publisher_digest='NOT_APPLICABLE',local_sdk_sha256='NOT_ACQUIRED',source_response=fetch['google-adapter-repo']['path'],
 source_sha256=fetch['google-adapter-repo']['sha256'],license_scope='Apache-2.0 repository license;pin code commit and per-file notices before analysis',
 acquisition_status='LICENSE_METADATA_ONLY',analysis_status='NOT_STARTED'))
table(D/'OFFICIAL_DOWNLOAD_CANDIDATES.csv',candidates)

inventory=load(R/'identity72-experiments73/IDENTIFIER_INVENTORY.json')
maps=load(R/'cross-sdk/IDENTITY_MAPPINGS.json')
reused_refs={}
rows=[]
for i,x in enumerate(inventory,1):
    ids=x['evidence_ids'];missing=[sid for sid in ids if sid not in source_map]
    for sid in ids:
        if sid in source_map:reused_refs[sid]=source_map[sid]
    rows.append(dict(reuse_id=f'OSF{i:02}',field=x['field'],kind=x['kind'],producer=x['producer'],reader=x['reader'],
      destination_or_serialization=x['upload_and_destination'],lifecycle=x['lifecycle_reset'],namespace_scope=x['cross_app_scope'],
      privacy_conditions=x['privacy_conditions'],relationship_contract=json.dumps(x['association_contract'],ensure_ascii=False),
      source_ids=';'.join(ids),unresolved_source_ids=';'.join(missing),
      evidence_stages=';'.join(x['evidence_stages']),origin_file='identity72-experiments73/IDENTIFIER_INVENTORY.json',
      origin_file_sha256=sha(R/'identity72-experiments73/IDENTIFIER_INVENTORY.json'),
      reuse_scope='HISTORICAL_CAPABILITY_OR_CONTRACT_NOT_NEW_CODE_ANALYSIS',
      new_analysis_permission='NOT_INFERRED_FROM_HISTORICAL_FINDING;see sample license gate',
      actual_upload_observed=x['actual_upload_observed'],production_match_proven=x['production_match_proven'],
      value_model_consumption_proven=x['value_model_consumption_proven']))
table(D/'IDENTITY_FIELD_REUSE_MATRIX.csv',rows)
maprows=[]
for x in maps:
    for sid in x['refs']:
        if sid in source_map:reused_refs[sid]=source_map[sid]
    maprows.append(dict(relation_id=x['id'],source=x['source'],target=x['target'],relation_kind=x['kind'],scope=x['scope'],
      evidence_ids=';'.join(x['refs']),origin='cross-sdk/IDENTITY_MAPPINGS.json',origin_sha256=sha(R/'cross-sdk/IDENTITY_MAPPINGS.json'),
      status='REUSED_STATIC_MAPPING_ONLY',new_static_analysis=False,production_graph_or_model_use='UNKNOWN'))
table(D/'CALL_RELATION_REUSE_MATRIX.csv',maprows)
save(D/'REUSED_SOURCE_REFERENCES.json',list(reused_refs.values()))

licenses=[]
for key in ['adjust-version-license','adjust-550-license','adjust-570-license','google-adapter-license',
            'al-android-license','al-ios-license','lp-unity-license','lp-android-license','unity-operate-terms','unity-general-terms']:
    f=fetch[key]
    decoded=D/'sources'/(key+'.decoded.txt')
    textfile=decoded if decoded.exists() else R/f['text_path']
    text=textfile.read_text(encoding='utf-8-sig')
    if key.startswith('adjust'):
        quote='Permission is hereby granted, free of charge, to any person obtaining'
        conclusion='MIT permission verified at matching version tag;notice obligations and per-file/dependency scope remain'
    elif key=='google-adapter-license':
        quote='TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION'
        conclusion='Apache-2.0 repo license;not permission for proprietary dependency SDKs or unpinned source artifact'
    elif key.startswith('al-'):
        quote='This software is subject to, and made available under, the AppLovin Software Development Kit End User License Agreement'
        conclusion='Custom SDK EULA reference;linked current URL returns homepage;analysis grant UNKNOWN'
    elif key.startswith('lp-'):
        quote='This software is subject to, and made available under, the Unity Advertising Terms of Service'
        conclusion='Service Asset under advertising plus incorporated general terms;not MIT/Apache'
    elif key=='unity-general-terms':
        start=text.index('Engage in any decompiling')
        end=text.index('; (f)',start) if '; (f)' in text[start:] else start+620
        quote=text[start:end].strip()
        conclusion='General restrictions include decompilation/reverse engineering with express legal exception;no applicable exception or special grant established here'
    else:
        quote='Unity Advertising Additional Terms'
        conclusion='Current advertising terms June30,2026 incorporate general terms;historical applicability not assumed'
    assert quote in text,(key,quote)
    licenses.append(dict(id=key,url=f['url'],final_url=f['final_url'],acquired_utc=f['acquired_utc'],raw_path=f['path'],raw_sha256=f['sha256'],
      readable_path=textfile.relative_to(R).as_posix(),readable_sha256=sha(textfile),quote=quote,
      quote_line=text[:text.index(quote)].count('\n')+1,conclusion=conclusion))
save(D/'LICENSE_EVIDENCE.json',licenses)

mechanisms=[
 ('M1','Namespace and same-device cross-app boundary','IG72C01;IG72C02;IG72C04;IG72C27','Versioned namespace/key/reset and typed edges;no IP/model-based person merge',
  'Synthetic same-value keys in two namespaces,reset,reinstall and purpose denial','No cross-namespace equality inference;reset does not silently relink',
  'False merge FP/(TP+FP);false split FN/(TP+FN),pair and entity counts,truth scope','Own-fixture design only;SDK path awaits per-file license gate'),
 ('M2','Account links across devices with entity grain preserved','IG72S02;IG72S03;IG72C10;IG72C14','Authenticated account-device assertion edges;account is not person',
  'Two devices one own account;one device two accounts;logout,unlink and shared-family device','Authorized link grants only account relationship;no transitive person union',
  'Account-edge precision/recall,wrong-person merges and unlink propagation','Own fixture needs no third-party identity data;UGS runtime needs correct terms and authorization'),
 ('M3','Third-party resolution result semantics and quality','IG72S04;IG72S05;IV74S01;IV74S02','Provider result adapter separates derived/maintained,entity grain and quality claims',
  'Locally authored contract records for derived,maintained,failed,ambiguous and stale mapping;NOT vendor responses','Derived is not existing match;maintained not person truth;confidence not calibrated probability',
  'State transition correctness;real accuracy STOP without lawful independent truth','No external resolver query;future real test needs rights holder and environment scope'),
 ('M4','Temporal event/attribution/revenue correlation','L71C01;L71C02;L71C15;L71C16;XS30;XS34','Owner+namespace+typed receipts and bitemporal event linker;dedup separate from identity',
  'One request multiple candidates;retries,clicks,impressions,revenue callbacks,duplicate MMP reports and late arrival','Request ID is not economic impression primary key;one economic event counted once under explicit contract',
  'Wrong-link rate,duplicate/false-dedup rate,late-event exclusion,ledger reconciliation','Adjust MIT sources are next-phase candidates;closed MAX/Unity paths remain gated'),
 ('M5','Graph feature lineage,revocation and value-consumer interface','EN76S04;EC78S01;EC78S04','As-of graph query,consent checks,dependency invalidation and explicit model input receipt',
  'Relationship revoked/deleted after feature materialization;late facts;stale cache;model masks or defaults','No revoked/default/masked input consumption;feature/materialization/read/decision distinct',
  'Revocation propagation latency,stale-read count,query p50/p95/p99 only after actual local run;D requires real labels','Independent future local prototype only;no76 modification or new experiment this round')]
table(D/'MECHANISM_TEST_DESIGN.csv',[dict(mechanism_id=i,mechanism=n,legacy_refs=refs,independent_design=design,proposed_test=test,
    falsifier_or_expected_boundary=bound,metrics=metric,required_conditions=conditions,execution='NOT_RUN_DESIGN_ONLY',vendor_model_use='UNKNOWN')
    for i,n,refs,design,test,bound,metric,conditions in mechanisms])

reports={
'官方样本清单与许可核验.md':'''# 官方样本清单与许可核验

2026-11-20。本轮先做样本与许可准入，未启动新增SDK功能分析。**已核验30个版本、47份已有技术包：26份AAR、17份sources.jar、4份UPM tgz。** 未重复下载SDK，新增22次请求仅为官方许可、仓库及发布元数据；不是生产广告/身份请求。

这是相关子集，不是对全部103个AAR/67个源码包的新扫描。范围覆盖MAX、MAX的Unity/ironSource/Google适配器、Unity Ads、LevelPlay、Adjust、AppsFlyer、Singular、Google AppSet/AdsIdentifier及Unity Authentication/Analytics/IAP。

## 已取得样本及哈希

完整逐文件[47行清单](ACQUIRED_SAMPLE_CATALOG.csv)列官方下载URL、版本、SHA256、原始provenance及哈希、文件大小、许可声明、发布日期/类型和准入。所有47份文件与既有记录哈希一致。POM不算SDK包，记录于[版本来源](VERSION_PROVENANCE.json)。sources.jar这个文件名不证明开源、实现完整或允许反编译。

| 样本族 | 已有版本 | 当前分析门槛 |
|---|---|---|
| AppLovin MAX Android | 13.2.0、13.6.2、13.6.3、13.6.4、13.7.0 | POM声明SDK EULA；许可范围未补齐，不新增分析 |
| MAX Unity Ads适配器 | 4.17.0.0、4.18.1.0 | 不能因是适配器就默认开源；新分析HOLD |
| MAX ironSource适配器 | 9.3.0.0.0、9.4.0.0.0、9.5.0.0.0 | 同上，依赖核心另有许可 |
| MAX Google适配器 | 25.1.0.0、25.2.0.0、25.4.0.0 | AppLovin发布的适配器不继承Google开源仓库许可 |
| LevelPlay Android | 9.3.0、9.4.0、9.5.0 | 当前条款/分析范围需确认；不反编译 |
| Unity Ads Android | 4.17.0、4.18.1 | POM为Unity Ads License，不因有source jar而开放所有用途 |
| Adjust Android | 5.5.0、5.7.0、5.8.1 | 对应tag完整MIT许可已取得；3份source jar可列下一阶段优先 |
| AppsFlyer Android | 6.14.2、6.17.5 | POM写Proprietary且链接隐私页，不能视为分析授权 |
| Singular Android | 12.17.0 | 有AAR；source jar旧请求404，不计为取得 |
| Google身份依赖 | AdsIdentifier17.1.0、AppSet16.0.0 | 仅来源/依赖与元数据盘点，未清除分析许可门槛 |
| UGS及收入组件 | Authentication3.9.0、Analytics6.3.0、IAP5.4.0/5.5.1 | 包内LICENSE指Unity Terms/服务条款，不假定MIT或Apache |

HTTP Last-Modified单独记录，**不等同原始发布日期**。多数Maven样本发布日期UNKNOWN；有官方UPM registry_time才作明确类型记录。不同平台同版本不能互相借用发布日期。

## 新确认的官方发布入口，未下载SDK包

见[候选下载清单](OFFICIAL_DOWNLOAD_CANDIDATES.csv)：

| 产品 | 官方发布记录 | 取得状态 |
|---|---|---|
| MAX iOS | release_13_7_0，2026-10-30；官方repo与许可文件已核对 | release未列core二进制asset；没有已取得XCFramework或本地SDK哈希。仓库源码zip不能冒充核心框架 |
| MAX Unity | release_8_6_6，2026-09-15；asset含Android/iOS13.6.4 | 已记录官方unitypackage URL和发布方SHA256，未下载；发布方digest不是本地验证结果 |
| LevelPlay Unity | UnityLevelPlay_9.3.0，2026-01-20 | 官方unitypackage URL及发布方SHA256已记录，未下载 |
| Google官方Android mediation源码 | googleads/googleads-mobile-android-mediation | 官方仓库Apache-2.0许可已保存；代码commit未固定、源码包未下载 |

本轮没有取得新的JAR/AAR/XCFramework/Unity包，不将许可文件下载计作SDK取得。

## 许可核验的实质结果

1. **Adjust有明确可用的开源路径。** 三个对应版本tag的LICENSE均为MIT，POM也声明MIT。允许软件使用/修改等并要求保留版权和许可声明；下一阶段仍按文件检查第三方例外，不将它扩展为平台后台访问或真实用户数据授权。
2. **Google官方适配器仓库为Apache-2.0。** 许可仅覆盖该仓库适用源码，不能覆盖AppLovin发布的同名适配器、Google/其他广告核心二进制或其网络服务。先固定具体源码commit及文件许可再分析，本轮不下载或查看实现。
3. **MAX不是已核验的MIT/Apache开源样本。** Android/iOS仓库LICENSE明确指SDK EULA；POM也指相同条款。当前EULA URL重定向到官网首页，没拿到有效全文，故分析授权UNKNOWN。不能凭自定义许可名称断言所有行为违法，也不能假定已获允许。
4. **Unity/ironSource公开repo不等于开源授权。** 仓库LICENSE指Unity Advertising Terms且归为Service Asset；当前Advertising条款纳入Unity总条款。总条款有反编译/逆向限制及明确法律例外；本项目未证明适用例外或特别授权，因此本轮停止这些新增分析。当前条款不被倒填成历史版本的唯一合同。
5. MAX Unity repo标准license端点404/metadata无license，只说明未从该端点得到许可，不能证明所有文件都无许可。源码包和具体版本尚未取得，不自动推进。

## 旧资产纠错，不覆盖历史

`ThirdPartySDKs/Discovery/applovin-adapters-license.txt`正文是`404: Not Found`，不能当许可证据。Singular来源记录中的source jar也是404，不能计入样本。两项已在本轮[勘误](CORRECTIONS.md)记录；00—78原文件不修改。旧静态发现不因复用就获得新的分析授权，也不作追溯法律判断。

原始URL、采集日期、原文位置及SHA256见[来源目录](SOURCE_CATALOG.md)、[许可证据](LICENSE_EVIDENCE.json)。仅有出处、可下载性和哈希不满足许可准入。
''',
'静态分析可行性报告.md':'''# 静态分析可行性报告

2026-11-20。**本轮实际新增功能静态分析为0。** 已做的是合法来源/许可文件读取、POM及包元数据盘点、哈希核对；没有读classes.dex/class实现、导出新类方法清单、反编译或重新扫描旧SDK字符串。

## 按许可决定下一阶段文件范围

| 状态 | 文件范围 | 可做/待做 | 本轮动作 |
|---|---|---|---|
| GO_SOURCE_REVIEW_ONLY_NEXT_PHASE，3份 | Adjust5.5.0/5.7.0/5.8.1的sources.jar | 对应tag MIT已核实；可优先设计身份字段生成/重置、包构造、去重与权限调用链的限文件审查；注意文件/依赖例外和notice | 不执行分析 |
| LIMITED，3份 | 相同Adjust版本AAR | MIT出处明确，但有源码时优先源码，无需重复反编译二进制 | 不执行 |
| STOP_SCOPE_OR_REVERSE_PERMISSION_UNRESOLVED，10份 | Unity Ads/LevelPlay及UGS/IAP/Analytics相关包 | 需确认具体版本、合同适用范围、静态分析方法及授权/例外依据；不能用CLI检查性能的有限例外当广告身份逆向通行证 | 不新增分析 |
| UNKNOWN_EULA_SCOPE_NO_NEW_ANALYSIS，26份 | MAX及所选AppLovin适配器 | 明确EULA全文/适配器逐文件许可及历史适用性，再决定允许范围 | 暂停 |
| UNKNOWN_LICENSE_SCOPE_NO_NEW_ANALYSIS，5份 | AppsFlyer、Singular、Google身份依赖所选包 | 获取有权许可与具体文件范围；隐私页/POM名字不足以授权实现分析 | 暂停 |
| 候选源码未固定 | Google官方Apache-2.0适配器repo | 先选commit、取得具体源码及文件许可/依赖notice，后续可只看桥接层 | 仅许可核验 |

GO是下一阶段的**许可候选**，不是已完成分析，也不是本轮自动继续执行的指令。二进制来自官方仓库不等于有反编译许可。源码来源可见也不等于许可分析、修改或复用。

## 允许之后的限范围分析设计

每个获准文件才依次记录：版本/哈希→包/符号→输入来源与namespace→生成或reset→权限分支→序列化/接收接口→时间及生命周期→调用者。每条边都引用文件、类/方法、代码位置与分支；不把搜索到字符串当完整调用链，不提取密钥或尝试解密生产Token。

版本对照只比较已准入、明确对应的版本和具体方法；公共API、实现代码、平台约束分别报告。sources.jar可能仅有API壳，先在获准范围内核对覆盖，不将其与闭源native等价。iOS XCFramework未取得时不虚构符号/架构分析；Unity wrapper许可不能扩张到其中捆绑的Android/iOS核心。

本轮旧30字段/10映射全部来自既有结构化证据，没有新读受限实现。图中标注“旧代码能力/官方契约”是历史证明范围，不代表新分析许可或生产接收。

## 客户端无法补齐的环节

客户端最多支撑字段生成/读取、请求构造、回调和明确接口映射。它不能单独证明服务端成功匹配、指定产品接收、图谱粒度、模型实际消费、独立增益。实际网络观察、后台或授权测试属于另一阶段，当前不执行。加密Token不当解码特征，native闭源止于未知。

保留：C_graph.Axon=UNKNOWN，C_graph.Vector=UNKNOWN，D=UNKNOWN，原生产取证执行=STOP。开源样本能帮助自主参考设计，不替代厂商生产证据。
''',
'身份字段及调用关系图.md':'''# 身份字段及调用关系图：复用证据，不新增代码分析

2026-11-20。已逐行复用[30字段矩阵](IDENTITY_FIELD_REUSE_MATRIX.csv)与[10条调用映射](CALL_RELATION_REUSE_MATRIX.csv)。来源编号、原始scope、权限、生命周期和模型未知边界保留；[原始证据记录](REUSED_SOURCE_REFERENCES.json)保存文件/哈希/版本/位置。没有把同一公司或同包ID自动连成个人图谱。

## 字段与实体粒度

| 字段组 | 既有可证范围 | 禁止推断 |
|---|---|---|
| GAID/AAID/IDFA、App Set ID、IDFV、Android ID | 各有OS、设备/发布者/签名/安装作用域及隐私条件；部分SDK有读取/请求构造 | 永久人ID、跨设备自然人、所有发行商共享 |
| Installation ID、Firebase FID/App Instance ID | 安装/应用实例等不同组件身份；Firebase App ID本身是项目/App上下文 | FID、会话、项目ID彼此相同或跨应用个人键 |
| Customer/Publisher/External User ID、UGS Player ID、UPA账号 | 开发者显式命名空间、UGS项目身份、组织账号链接的各自契约 | 任意Unity游戏都自动互通；账号等于自然人；不同MMP实际设置同值 |
| hash email/phone、IP/网络/设备属性 | 特定入口的构造或用途披露，受许可/同意门控 | 哈希天然匿名、网络相似即同人、已有完整fingerprint服务 |
| token/request/event/waterfall/opportunity/tracking/attribution ID | 请求、机会、事件、会话或归因的局部关联 | 经济展示唯一账本主键、真实跨设备身份、token已解码模型特征 |
| RampID、UID2及Pixel字段 | 各自公开契约/入口和范围；Exchange激活可用性属特定产品 | 已成功个人匹配，或Axon/Vector实际读取相应结果 |

30字段不是30个生产入模特征。字段矩阵中的E1/E2/E3/E4、实际上传/匹配/入模false只是“未证明”，不是厂商不存在能力。

## 产品隔离的证据链图

```mermaid
flowchart LR
  OS[OS或开发者身份来源] --> MAX[MAX客户端字段/请求构造：旧代码能力]
  MAX -. 接收/身份解析未证 .-> AX[Axon服务端图谱/价值特征 UNKNOWN]
  OS --> UA[Unity Ads客户端token/机会事件：旧代码能力]
  UA -. 服务端映射与入模未证 .-> V[Vector个人图谱特征 UNKNOWN]
  UPA[Unity组织账号链接契约] --> UGS[UGS项目/账号身份]
  UGS --> AN[Analytics分字段序列化]
  FB[Firebase AppInstance/Session/App ID] --> IAP[IAP受门控的分字段构造]
  UGS --> IAP
  AN -. 未有Vector消费桥 .-> V
  IAP -. 未有Vector个人身份消费桥 .-> V
  LR[LiveRamp解析服务公开契约] --> EX[Unity Exchange RampID激活可用：官方披露]
  EX -. 不等于Vector接收/消费 .-> V
  MM[MMP自定义ID/归因/收入构造] -. partner配置与服务端接收另证 .-> ADV[广告平台接收 UNKNOWN]
  ADV -. 指定模型读取未证 .-> AX
  ADV -. 指定模型读取未证 .-> V
```

实线仅表示各边注明的旧代码能力或官方契约，不是本项目观测到的生产发送/接收。广告机会上下文、模型输入、归因、收入四种时点分开；安装后收入不能倒灌同次安装前机会。

## 已知明确调用映射与不能混同之处

ID01/02：Authentication PlayerId→Analytics unityPlayerID、ExternalUserId→Analytics UserId及InstallId回退，不说明字段互等。ID03—06：IAP5.5.1的Firebase/UGS/Analytics身份分字段与权限/远程门控，不能把旧5.4.0可构造字段升级为实际发送。

ID07：MAX adapter event_id→Google placement_req_id是请求关联，不是人级匹配。ID08：MAX consent/doNotSell→Unity隐私字段是布尔配置传递，不证明初始化成功。ID09：Adjust的Facebook AttributionIdProvider aid→fb_id是受签名检查的归因字段，不是Facebook账号ID。ID10：Singular customUserId setter是开发者控制入口，不证明目标游戏实际设置或与其他ID相等。

本轮主结论：可复用的是字段作用域、明确接口映射和反误判边界；**没有恢复Axon/Vector闭源身份图谱或生产特征消费链。** 新的解析/实际接收/读取仍按78号十组契约验收。
''',
'五项优先机制与反证测试.md':'''# 五项优先机制与反证测试

2026-11-20，设计稿。下面是独立重建的研究优先级，不是厂商实现清单。所有测试均NOT_RUN，没有新的合成数字、预测收益、查询延迟或匹配准确率结果。细项见[测试设计矩阵](MECHANISM_TEST_DESIGN.csv)。

## M1：命名空间与同设备跨App边界

复用GAID/AppSet/安装ID等不同作用域，设计`tenant+issuer+namespace+kind+epoch`注册，不让相同字符串自动成为同一人。旧SDK能读取/构造ID，不证明跨App接收或成功解析。

未来仅用自有fixture检验：两命名空间同值、一个设备多个安装、广告标识重置、卸载重装及用途关闭。预期：重置不静默复联；IP/设备型号只作环境或候选上下文，不作确定性人级合并依据。统计已知真值下的pair precision/recall、FMR=`FP/(TP+FP)`、false split=`FN/(TP+FN)`，并声明候选对采样与实体数；不能把无匹配当拆分真值。

许可优先文件：3份Adjust MIT源码候选，后续仅限明确输入/持久化/reset/包字段范围；闭源广告SDK许可未清除则不继续分析。

## M2：跨设备账号关系，避免账号冒充自然人

复用UGS项目/组织账号契约；参考实现用合法第一方登录的签认account-device边，不用设备传递闭包生成person节点。一个人可多账号，一个账号也可能共享；登录证明控制关系，不证明自然人唯一性。

未来自有测试：两设备同账号、一设备多账号、家庭共享设备、登出/解绑和会话过期；验证权限生效时间、链接撤销与查询范围。账号关系precision/recall与人级准确性分开。测试真实UGS环境需其条款和环境授权；本轮不启动。

## M3：第三方解析结果状态与关系质量

独立适配器应保留provider、namespace、result_type、match_status、entity grain、版本和质量定义，不把返回ID直接当成功匹配。LiveRamp maintained/derived、confidence语义作为反误判契约，不自动对应Vector。

未来只构造由自己定义、明确标注为本地合同fixture的derived/maintained/failed/ambiguous/stale记录，不伪造厂商生产返回。测试粒度不提升、失败路径默认拒绝、过期映射失效。概率匹配仅输出候选关系/不确定性，不强制union所有设备；真实准确性必须有合法独立真值，不能拿matchConfidence作概率校准或重识别。

## M4：事件、归因和收入关联

复用71号MAX/Unity机会ID及10条明确接口映射。独立Temporal Event Linker按owner+namespace+typed receipt和有效时间做关联，身份键、广告请求键与经济事件账本键分别存储。

未来测试一请求多候选、click/load/raw impression/viewability/reward/revenue回调、MMP重复与迟到/退款。预期：不将request ID当经济展示唯一键，不把奖励/代理value当真实收入，同一经济事件按明确契约去重。错误关联、漏关联、重复/误去重与账本核对分别评价。服务端实际接收及标签构成仍未知。

## M5：图谱特征、撤销与LTV消费接口

复用76号审计原则和78号生产证据规范，**不修改或重跑76程序**。独立图谱应保留关系事实与断言来源，采用有效时间/记录时间两个维度；特征返回as-of快照、用途/权限、关系质量、graph/feature版本、available_at和血缘。

未来检验物化后撤权、删除生效、边失效、迟到事实、旧缓存与备份恢复。依赖图使关系失效传播到派生特征及缓存；读取前再次校验，不把在线删除宣称模型遗忘。用输入消费receipt区分取出、物化、实际非默认/未mask的模型输入和active决策引用；合法0值不被误判缺失。

延迟只在真实本地运行后按固定硬件/规模报告p50/p95/p99及撤销传播延迟，本轮不填数。图谱对LTV的D必须另获真实授权样本、完整观察/零值定义、成熟金额标签和时间外测试，固定数据量/模型容量/策略做个人特征对群体/共享参数消融；合成结果不能充当真实D。

## 独立参考实现的接口候选，尚未实现

八模块仍是自主设计目标：Namespace Registry→Resolver→Relationship Graph Store→Temporal Event Linker→Graph Feature Service→LTV Feature Consumer；Consent and Deletion Manager贯穿写入/查询/撤销，Audit and Provenance Service贯穿每一步。图存储用类型化、带时间/出处的边，不采用无条件全局人ID或不可撤销union-find。

只从公开契约抽取语义需求，不复制受限实现；任何未来开源代码复用须遵守其许可，且不称厂商代码重建。本轮只提交这些机制与测试条件，不展开实现、模型训练或生产适配。
''',
'下一轮授权与测试条件.md':'''# 下一轮授权与测试条件

2026-11-20。首轮盘点与许可审查完成；**不自动扩大到SDK实现分析、下载大型包、参考原型或联网测试。** 原生产取证执行STOP继续有效，C_graph.Axon、C_graph.Vector和D均UNKNOWN。

## 推荐的最小后续范围

如果继续，优先只选已有Adjust5.5.0/5.7.0/5.8.1的3份MIT sources.jar，分析明确的身份命名空间、生成/reset、权限和事件包映射及版本差异，先形成有限文件/符号计划。它能帮助独立事件/身份组件设计，不能证明Axon/Vector模型消费。

第二候选为Google官方Apache-2.0 mediation源码：先固定具体commit、获取该源码和文件级notice，再只看许可覆盖的桥接层。不能把Apache许可套给MAX适配器或第三方核心SDK。本轮没有选定commit或下载实现，不能报告已经可运行的样本。

## 继续前的闸门

| 路径 | 必须补齐 | 未补齐时处理 |
|---|---|---|
| Adjust下一阶段源码审查 | 有限文件/方法目标、MIT及文件例外/依赖边界、结果输出范围 | 保持仅盘点；不为了获得好结果扩大代码扫描 |
| MAX核心/适配器 | 对应版本的有效SDK EULA全文与可分析/引用范围；必要时权利方明确静态分析许可 | UNKNOWN/HOLD；不假定官网首页即许可，也不借第三方开源许可 |
| Unity/LevelPlay/UGS | 具体样本与条款适用性、允许的方法/用途及相关授权/例外依据 | 不新增反编译或内部协议研究；CLI有限性能检查许可不能扩大到身份逆向 |
| iOS XCFramework/Unity package | 真实官方二进制下载位置、版本、许可、实际取得后本地SHA256与发布方digest核对 | 不把release元数据或仓库zip当已取得核心框架 |
| 概率/人级身份实验 | 合法自有身份或权利方许可的准确真值、实体粒度、错误合并风险/退出处理 | 不采集真实第三方身份、不构造真实跨App个人图谱 |
| 授权SDK运行 | 测试App/设备/账号权利、SDK许可允许、允许的网络/环境、测试数据范围 | 默认不运行。SDK初始化可能联网，需明确环境与阻断方案；不沿用Python hook保证原生SDK隔离 |
| 生产C_graph | 78号组件→指定产品实际接收→指定价值模型非空有效输入/机会引用，且有出处/授权/时间/生命周期 | UNKNOWN及生产取证STOP；本地实现不能替代 |
| 真实D | 真实授权成熟收入/观察分母、独立时间外测试、等数据/容量/控制器消融 | STOP真实效果；不使用合成数字冒称收益 |

这些是条件，不代表已确认渠道、已获得授权或要求用户立即批准某个后台动作。本轮没有对外发送申请、签署许可或NDA、建立账号、访问身份商、执行广告请求。

## 清楚区分四种结果

1. 旧源码/SDK能力：只能说存在某构造、读取或接口映射。
2. 自有参考实现：只能说自己的系统在明确fixture/授权样本下通过哪些测试。
3. 授权环境运行：范围限环境、产品、版本和数据，不自动外推生产。
4. 厂商生产实际消费/独立增益：必须另有78号所要求的生产链和真实实验；不能用前三者替代。

因此下一步最值得验证的是**许可明确的身份/事件生命周期机制**，不是再扩大SDK数量或宣称恢复闭源图谱。若受限核心许可不能明确，停止其分析，独立语义设计仍可在不复制受限实现的范围内另行开展。
'''}
for name,content in reports.items():write(D/name,content)

corrections='''# 本轮勘误与边界

保留00—78全部原件，仅在本目录补充，不追溯改写历史结论。

- `ThirdPartySDKs/Discovery/applovin-adapters-license.txt`是`404: Not Found`，不是MIT或其他许可。它的文件名不能作为许可证据。
- Singular12.17.0 provenance中sources.jar请求404，未取得文件；本轮不计作成功样本，不重复下载。
- AppLovin EULA地址返回官网首页，不是许可正文；许可范围UNKNOWN，不判定“无许可”或“明确禁止全部行为”。
- Unity Ads旧条款URL重定向到当前Advertising条款；不能将旧地址与新地址算两份独立许可证据。当前总条款日期2026-11-16、Advertising条款日期2026-06-30；历史适用性另核。
- MAX Unity license标准端点404不证明仓库所有路径无许可；具体版本包未取得，保持UNKNOWN。
- UPM源码可下载与MIT/Apache授权不是同一件事；包内LICENSE指向Unity条款。
- 发布方给unitypackage的SHA256与本地取得文件后算出的SHA256不同层次；本轮只有前者，不计作本地取得。
'''
write(D/'CORRECTIONS.md',corrections)

cat=['# 官方来源及许可证据目录','',f'采集/整理日期2026-11-20；本轮22次官方metadata/legal GET，SDK新下载0，新增功能静态分析0。整理时间：{NOW}。','',
 '## 实质许可证据','']
for x in licenses:
    cat += [f"### {x['id']}",'',f"URL：{x['url']}；最终URL：{x['final_url']}。",f"采集：`{x['acquired_utc']}`。",
      f"原响应：[{Path(x['raw_path']).name}](../{x['raw_path']})；SHA256：`{x['raw_sha256']}`。",
      f"可读原文：[{Path(x['readable_path']).name}](../{x['readable_path']})；SHA256：`{x['readable_sha256']}`；第{x['quote_line']}行。",
      f"> {x['quote']}",'',x['conclusion'],'']
cat+=['## 全部请求/样本与复用出处','',
 '[全部22份响应](FETCH_MANIFEST.json)保留URL/日期/状态/重定向/原始哈希；[47份已有样本](ACQUIRED_SAMPLE_CATALOG.csv)的URL/哈希直接来自旧provenance并重新哈希核对；[原样本元数据哈希](REUSED_ARTIFACT_HASHES.json)不改变旧件。',
 '[库许可解码记录](DECODED_LICENSES.json)保留API响应、license git blob及解码文本哈希；不是固定整个实现仓库commit。',
 '[30字段](IDENTITY_FIELD_REUSE_MATRIX.csv)和[10调用映射](CALL_RELATION_REUSE_MATRIX.csv)只复用旧结构化报告，不重新读取受限代码实现；其原始文件、版本、SHA256及位置见[原引用](REUSED_SOURCE_REFERENCES.json)。',
 '旧字段/代码能力不被升级为生产接收、成功匹配、Axon/Vector读取或身份独立增益。读取许可文件不意味着已准许所有后续分析。']
write(D/'SOURCE_CATALOG.md','\n'.join(cat))
save(D/'STATUS.json',dict(stage='FIRST_ROUND_INVENTORY_LICENSE_COMPLETE',acquired_existing_artifacts=47,versions=30,
 next_phase_source_candidates=3,current_new_functional_static_analyses=0,new_SDK_bundles=0,public_metadata_gets=22,
 new_core_decompiles=0,reference_implementation_started=False,production_SDK_runs=0,identity_queries=0,real_ad_requests=0,
 official_repo_implementation_files_read=0,engineering76_modified=False,
 Axon_C_graph='UNKNOWN',Vector_C_graph='UNKNOWN',D='UNKNOWN',original_production_forensics='STOP',
 next_phase='Select limited MIT Adjust sources or pinned Apache bridge sources;do not automatically execute',
 restricted_paths='HOLD/STOP until actual license scope is established;current terms not retroactive legal conclusions'))
save(D/'REPORT_PATHS.json',list(reports))
print(json.dumps(dict(reports=len(reports),field_reuse=len(rows),call_mappings=len(maprows),license_documents=len(licenses),new_analysis=0),ensure_ascii=False))
