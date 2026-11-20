# SDK生态与版本矩阵

2026-11-19。本轮优先补齐客户端连接：新增官方Unity IAP 5.4.0/5.5.1、UGS Analytics 6.3.0、Singular 12.17.0；其余复用并验哈希。未重复下载已取得的相同SDK发行包。

完整[版本/原包SHA256/来源/时间/状态矩阵](cross-sdk/SDK_MATRIX.json)包含49项选定SDK版本记录；不是49项全部完成深度逆向。每条代码证据在[CODE_CATALOG](cross-sdk/CODE_CATALOG.md)关联准确原包及文件哈希。

## 分析投入与版本含义

| SDK | 本轮范围 | 结论上限 |
|---|---|---|
| MAX 13.2.0/13.6.2/13.6.3/13.6.4/13.7.0 | 复用旧版本证据；新反编译13.7 EventService/队列，javap公共API差分 | 四款游戏匹配前四版；13.7只是独立参照 |
| 独立Axon 1.3.4 | 复用已有AAR和身份/API分析 | 未证明四款游戏集成独立Axon SDK |
| Unity Ads 4.17.0/4.18.1及MAX Unity适配器 | 复用发行包；反编译两版adapter，核实token和同意转换 | 中介调用链，不是Vector获客已启用 |
| LevelPlay 9.3.0/9.4.0/9.5.0 | 复用既有请求/状态分析 | 未重新完整逆向；不把AUID当UPA PlayerId |
| Adjust 5.5.0/5.7.0/5.8.1 | 复用源码；新增远程触发/标识限制/API差分 | Car5.5/Jewel5.7匹配；5.8.1独立参照 |
| AppsFlyer 6.14.2/6.17.5 | 复用收入包/缓存证据；核对Rotate原版赋值 | 不证明MMP→网络后台postback启用 |
| Singular 12.17.0 | 官方vendor Maven AAR/POM；有限反编译事件/CUID入口 | 未取得sources JAR，未证明目标游戏使用，内部队列链未完全恢复 |
| Firebase Remote Config24.0.1/Analytics各已存版本 | 深读RC官方源码：FID、分析属性、personalization、ABT | 只是独立SDK实现，不冒充目标游戏确切RC版本 |
| Meta Core18.0.3/Audience Network、Google Mobile Ads | 复用已有包与分析；新增MAX Google25.4.0.0适配器请求ID映射 | 不把广告网络适配器认定为实际买量渠道 |
| Authentication3.9.0/Analytics6.3.0/IAP5.4.0及5.5.1 | 复用Auth原源码，新增后两者；追踪明确组件赋值与请求序列化 | Unity产品之间有客户端桥接；不证明Vector训练 |
| Pixel1.5.46/CAPI | 复用31号公开网页/官方接口证据 | cookie/点击/去重ID用途不同；本轮未运行网页或提交事件 |

## 新增包及时间

| 包 | 版本 | 发布日期证据 | 原包SHA256 |
|---|---|---|---|
| com.unity.purchasing | 5.4.0 | CHANGELOG 2026-06-29 | `f66ac4f26ef96346b34c63c920512d6e981430712a2d5092544bc66cb7a278ef` |
| com.unity.purchasing | 5.5.1 | CHANGELOG 2026-11-13 | `cf382958920ef886c51998988153ac55d6682fbd79d79cfb34362d7973ca9403` |
| com.unity.services.analytics | 6.3.0 | CHANGELOG 2026-03-05 | `bc1f64b7c3432aa7209ed37d0db5a53e3044507d77326845069de891d57b8910` |
| Singular Android | 12.17.0 | 未独立确认；保留HTTP Last-Modified | `fc126a348b9b9fb9bb56425a8210da41dc98a660930b2e8467b58615adfc7924` |

UPM包同时核对registry SHA1与下载内容；SHA256用于本地追溯。HTTP Last-Modified、registry获取日期和正式发布日期分别保留，不能互换。源码可读不代表开源许可证：UPM条款见各包LICENSE/Third Party Notices，闭源AAR只称反编译视图。

## 获取限制与复用边界

Singular的Maven Central坐标404，改由官方`maven.singular.net`取得12.17.0 AAR；sources JAR404，未伪称开源。MAX/Unity Ads候选GitHub changelog404，保留失败；MAX插件更新说明不能代替Android核心更新说明。成功和失败记录见[ACQUISITION](cross-sdk/ACQUISITION.json)、[Singular](cross-sdk/packages/singular/12.17.0/provenance.json)。

公共API差分来自实际JAR的javap：[API_DELTAS](cross-sdk/API_DELTAS.json)。只比较选定类，不证明所有方法体相同。Amaze GO!仍无可验证游戏包；本轮新增SDK不改变此状态。
