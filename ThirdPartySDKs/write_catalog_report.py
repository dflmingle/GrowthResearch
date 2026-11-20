from pathlib import Path
import json,collections,hashlib
R=Path(__file__).resolve().parent;ROOT=R.parent
entries=json.loads((R/'CATALOG.json').read_text(encoding='utf-8'));v=json.loads((R/'COLLECTION_VALIDATION.json').read_text(encoding='utf-8'))
no_binary=sum(not any(a['path'].endswith('.aar') or (a['path'].endswith('.jar') and not a['path'].endswith('-sources.jar')) for a in x.get('artifacts',[])) for x in entries)
lines=['# 第三方 SDK 收集清单与来源验证','',
'2026-11-18。原始发行包统一存放于 `D:/GrowthResearch/ThirdPartySDKs/<供应商>/<SDK>/<版本>/`。本轮只下载公开发行材料并静态分析，没有初始化SDK、运行广告请求或修改原包/游戏工程。','',
f'**已收集 {v["aar_count"]} 个 AAR、{v["source_jar_count"]} 个 Maven/JitPack sources JAR，覆盖 {v["distribution_versions"]} 个有 provenance 的版本目录；另有 TikTok 两个准确标签的官方 GitHub 源码 ZIP。**原始已登记发行材料约 {v["raw_artifact_bytes"]/1024/1024:.1f} MiB（不含提取副本/GitHub ZIP）。其中{no_binary}个目录未取得二进制，不算成功收集SDK。完整结果包括失败尝试，不是目录数量等于SDK数量。','',
'这是一份按本轮优先级实际取得的全量清单，**不是所有适配器及传递依赖均已下载的宣称**。归因/MAX主链已深入；其余网络已收集发行包/部分源码和适配器，但没有逐个恢复全部闭源内部实现。','',
'原包已有BuildConfig证据覆盖的**45个MAX适配器版本现均已取得AAR**（含Bigo坐标纠正）；见[ADAPTER_COVERAGE](ThirdPartySDKs/ADAPTER_COVERAGE.json)。未取得的是部分网络的独立核心或其他传递依赖，不是把适配器当作网络完整SDK。','',
'## 来源、版本和许可如何核验','',
'- 【官方 SDK 代码证实】匹配版本来自原包 `AppLovinSdk.getVersion()`、Adjust `Constants.CLIENT_SDK`、AF版本签名等；适配器版本另存，不能替代core版本。','- 下载来源：Maven Central、Google Maven、厂商公开Maven、官方GitHub/JitPack标签；不是二次打包站。每个版本目录保留AAR/POM/sources、提取的classes.jar、provenance、归档索引；无classes.jar的依赖壳保留其POM。','- SHA256、完整URL、UTC、HTTP状态、Last-Modified、POM许可证与依赖详见[CATALOG](ThirdPartySDKs/CATALOG.json)。下载成功不自动等于可自由再分发；闭源SDK按其EULA，公开sources也不自动等于宽松开源。','- HTTP Last-Modified是仓库对象时间，metadata lastUpdated是索引更新时间，**都不伪装成首次发布日期**。已另存Adjust GitHub release的published_at；其他没有可信日期的记为未知。','- 【无法确认】未取得AppsFlyer sources JAR；已下载的AAR可反编译。AppLovin sources JAR主要公开API，内部实现来自官方AAR反编译，不称完整源码。','',
'## 与游戏匹配的关键版本','',
'| 游戏 | MAX | MMP | 其他已定位版本 |','|---|---|---|---|',
'| Car Race | 13.6.4 | Adjust5.5.0 | Firebase22.4.0；Metica核心准确版本本轮未证实 |',
'| Meowdoku | 13.2.0 | AF6.14.2 | TikTok1.6.1、Firebase22.1.2、GRT1.3.2.0、UniKit2.6.1.3 |',
'| Rotate Rings | 13.6.2 | AF6.17.5 | TikTok1.7.1、Firebase22.4.0 |',
'| Jewel | 13.6.3 | Adjust5.7.0 | Firebase23.2.0；AdWorth配置内部版本不当成独立SDK发版 |',
'| Amaze GO! | 无包体 | 无包体 | 不从同发行商推定 |','',
'依据：[TP01](EVIDENCE_INDEX.md#tp01)、[TP02](EVIDENCE_INDEX.md#tp02)、[V01](EVIDENCE_INDEX.md#v01)。额外下载MAX13.7/Adjust5.8.1/Metica2.5.4/FirebaseRC24.0.1只是公开参照，未匹配游戏内版本。','',
'## 全部版本目录','',
'下列状态中的“取得”仅证明官方发行材料已下载与校验；游戏内所有依赖版本仍应逐项看匹配证据。完整SHA256在各provenance的artifacts条目。','',
'| 供应商 / SDK | 版本 | AAR / sources | 许可（POM原文） | 原始来源与完整哈希 |','|---|---|---|---|---|']
for x in entries:
 arts=x.get('artifacts',[]);a=any(z['path'].endswith('.aar') for z in arts);s=any(z['path'].endswith('-sources.jar') for z in arts)
 lic='；'.join(y.get('name') or '未声明' for y in x.get('licenses',[])) or 'POM未取得/未声明'
 version=x.get('version','未解析');prov='ThirdPartySDKs/'+x['provenance'];lines.append(f'| {x["vendor"]} / {x["sdk"]} | {version} | {"AAR" if a else "无AAR"} / {"sources" if s else "无sources"} | {lic.replace("|","/")} | [provenance]({prov}) |')
lines += ['', '## 独立发行包缺口与嵌入组件','',
'| 组件 | 实际获取状态 | 保留证据与限制 |','|---|---|---|',
'| Bulldog / AdWorth | 【实际游戏代码证实】游戏内集成样本 | Jewel原始native函数、解出的默认90规则/31权重表、JNI桥和资源出处均沿用D01–D07；未找到可验证独立官方发行包、许可证或商业所有权证据 |',
'| Meevii / UniKit / Learnings GRT | 【实际游戏代码证实】游戏内集成样本 | Meow DEX、BuildConfig、GDScript桥、GRT处理器已保存；未取得可信独立发行包，不能把游戏提取物命名成官方SDK |',
'| Metica | 官方Maven2.5.4取得 | 官方文档给坐标；Maven搜索索引零命中不代表不存在；Car桥另已提取，准确游戏内core版待确认 |',
'| AppDiscovery/Axon | MAX新事件分支+公开集成文档 | 没有找到可核验的独立“Axon模型SDK”发行包；服务端模型不在已取得材料中 |',
'| MobileAdsLite/Base25.1 | POM可取，AAR404 | 不将旧版组件拆分惯例套用到当前版本；已取得play-services-ads25.1/25.2主体 |',
'| FirebaseAnalytics | 22.1/22.4/23.2主体AAR只有约786B | 是依赖壳；已追加22.4 measurement-api/sdk/impl/base/sdk-api，避免把空壳当完整分析实现 |',
'| Firebase RemoteConfig | 取得24.0.1+官方GitHub公开实现参照 | 当前参照版，未证明与四款嵌入core准确一致；main源码非游戏版本锁定 |','',
'原始嵌入证据不复制为假独立SDK；完整引用见[EMBEDDED_ONLY](ThirdPartySDKs/EMBEDDED_ONLY.json)。下载失败/路径发现过程见各 `*_MANIFEST.json`，TikTok最初错误Maven坐标已由官方GitHub标签→JitPack成功补齐，不将最初404当最终缺包。','',
'## 验证结果与分析深度','',
'[COLLECTION_VALIDATION](ThirdPartySDKs/COLLECTION_VALIDATION.json)核对已登记发行材料SHA256；[API_COMPARISON](ThirdPartySDKs/API_COMPARISON.json)核对183个选定声明，未证明整个库相同。','',
'深入机制：MAX/Axon事件与收入、Adjust包构建/队列、AF收入编码/缓存、适配器信号、AppLovin用户匹配字段与InMobi条件式UnifiedID。其余SDK保留发行包及明确分析边界，不宣称已完成每家全部逆向。新原始证据索引：[TP01–TP09](EVIDENCE_INDEX.md#tp01)。','']
(ROOT/'14_第三方SDK全量清单.md').write_text('\n'.join(lines),encoding='utf-8')
embedded={
 'Bulldog-AdWorth':{'kind':'游戏内集成样本','independent_distribution':'未取得可验证官方独立发行包','references':['jewel-coloring/deep/adworth-method-inventory.csv','jewel-coloring/deep/method-index.json','jewel-coloring/deep/rule-catalog.json','jewel-coloring/deep/resources/decoded-config-provenance.json']},
 'Meevii-UniKit-GRT':{'kind':'游戏内集成样本','independent_distribution':'未取得可验证官方独立发行包','references':['SDK_VERSION_EVIDENCE.json','meowdoku/static/dex-audit.json','SDK_INTERNALS_INDEX.json','identity-deep/api-callers.json']},
}
for x in embedded.values():x['source_hashes']=[{'path':p,'sha256':hashlib.sha256((ROOT/p).read_bytes()).hexdigest()} for p in x['references']]
(R/'EMBEDDED_ONLY.json').write_text(json.dumps(embedded,ensure_ascii=False,indent=2),encoding='utf-8')
print('wrote catalog report',len(entries))
