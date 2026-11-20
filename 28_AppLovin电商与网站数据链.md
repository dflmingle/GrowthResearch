# AppLovin 电商、网站与非游戏转化数据链

2026-11-19。**已取得完整的公开接口、3 个网站的真实嵌入、公开 Pixel 原文与独立 Axon SDK 1.3.4。证明了跨属性转化关联的技术入口；没有证明某商家每条事件送达，也没有恢复服务端跨业务训练。**

## 1. 来源与本轮实际分析

| 材料 | 原始位置 | 已做工作 |
|---|---|---|
| Events and objects、GTM、CAPI、dedupe、order history | [NG01](EVIDENCE_INDEX.md#ng01)、[NG02](EVIDENCE_INDEX.md#ng02) | 逐项提取事件、金额、标识和条件；不是把 API 名称当业务已启用 |
| Pixel 正式静态资源 | [pixel-source.raw](nongame/pixel-source.raw)，来自 `https://s.axon.ai/pixel.js` | 只 HTTP GET；恢复 496 项字符串表，唯一轮转161；未执行下载的 JS，未查询带商家 key 的配置 |
| Pixel 代码位置 | [PIXEL_STATIC_EVIDENCE](nongame/PIXEL_STATIC_EVIDENCE.json)、[字符串表](nongame/pixel-string-table.json)、[局部静态替换稿](nongame/pixel-partial-static.js) | 字符偏移、原始 SHA256 保留；只替换明确全局解码器，局部别名仍需原文核对，不称完整反混淆 |
| Shopify 公共扩展资产 | [app-embed 原文](nongame/site-hexclad-embed.raw) | 静态追踪 URL/cookie→购物车属性；没有请求 cart.js 或修改购物车 |
| 官方独立 Axon Android SDK | [provenance](nongame/sdk/axon/1.3.4/provenance.json)、[POM](nongame/axon-sdk-pom.raw) | Maven 官方 AAR 265,172字节，137类；6个公共API类经 javap 检查；无初始化/事件发送 |

版本边界：【公开网页代码证实】Pixel 快照内部 `F="a/1.5.46"`；【SDK代码证实】Axon 发行包1.3.4；**都不是本轮各 App 或每个商家实际在跑的版本**。完整哈希在 [NG06](EVIDENCE_INDEX.md#ng06)、[NG03](EVIDENCE_INDEX.md#ng03)。

## 2. 官方事件语义，不混入游戏代理收入

【官方公开证实】[Events and objects](https://support.applovin.com/en/growth/promoting-your-websites/track-and-optimize/events-and-objects)，[本地原文](nongame/doc-events.txt)：

| 事件 | 触发 | 主要字段/要求 |
|---|---|---|
| `page_view` | 页面导航 | 每页触发；可选 user_data |
| `view_item` | 商品详情页 | items必需；币种推荐；value可选 |
| `add_to_cart` | 加入购物车 | items必需；币种推荐；value可选，商品 price×quantity |
| `begin_checkout` | 开始结账 | currency、items、value必需；user_data可选 |
| `purchase` | 实际购买 | currency、items、transaction_id、value、shipping、tax、user_data；value是**税费和运费之前的 subtotal**，无运费/税费用0 |
| `add_payment_info` | 提交支付方式 | 推荐事件；payment_type等，不要求传卡号 |
| `generate_lead` | 合格线索 | value/currency；明确不发送重复/低质量线索；value是业务线索价值，不等于已收款 |
| `login/sign_up/search/subscribe` | 登录、注册、搜索、订阅 | 各自字段要求不同；search_term、method、可选订阅金额等 |

事件在文档中为必需/推荐，不代表 SDK 在任意商家能自动识别所有业务动作。`purchase` 的 `is_new_customer` 有 Shopify/订单历史接入相关条件，不能当所有接入均必须手填。模板中金额不能直接当本轮样本真实订单数据。

## 3. 三条技术路径

### 浏览器：Pixel / GTM

【官方公开证实】[GTM 指南](nongame/doc-gtm.txt)给出 `https://s.axon.ai/pixel.js`、`axon("init")`、`axon("track",event,data,options)` 及事件队列。它假设网站已将业务事件正确放入 dataLayer；**不是加入脚本就自动知道支付成功**。Shopify headless 文档要求结账页由 Shopify App 处理，避免 GTM 重复触发。

【公开网页代码证实】Pixel 快照中的发送目标是 `https://b.applovin.com/v1/pixel`；序列化后优先 `navigator.sendBeacon`，异常/失败分支存在 `fetch` 回退。存在 session/localStorage/cookie 与 URL 上下文、会话及页面自动事件的代码。不能从 `sendBeacon` 调用证明服务器确认接收。

【公开网页代码证实】新发现的**可配置自动采集**分支：

- 在约字符32695处，配置响应 `autoEmailCapture === true` 才设置相应开关；`Me()` 约20900处也检查该开关以及 `_emailCaptureSetup`。
- 对 dataLayer `submitEmail` 和相关表单事件有监听/处理；规范化/哈希结果可进入 `_autoEmail`。约23683处 `We` 把 `autoCapturedEmail/autoCapturedEmailV2` 合入事件相关数据。
- `autoSpaPageView === true` 的另一开关控制部分 history/SPA 监听；不能由其存在断言默认开启。
- 这些是**下载脚本中的条件能力**。本轮没有使用网站 event key 获取配置，也没有填写表单、采集邮箱或触发自动捕获。没有据此判断商家实际开启、同意机制完备或违法。

【公开网页代码证实】还存在 `https://cm.g.doubleclick.net/pixel?google_nid=aplv&google_cm...` 的匹配分支，位于会话标识相关条件处理中。它是**cookie 匹配接口能力**的原文证据；没有执行该请求，没有匹配成功或跨设备图谱证明，不能把它扩成“Google账户身份已共享”。[NG06](EVIDENCE_INDEX.md#ng06)

### 商家服务器：Conversions API

【官方公开证实】[CAPI](https://support.applovin.com/en/growth/promoting-your-websites/api/conversion-api)，[原文](nongame/doc-capi.txt)：

| 层级 | 接口与字段 | 含义 |
|---|---|---|
| 请求 | `POST https://b.applovin.com/v1/event`；Authorization为商家 Conversion API key；`pixel_id` 为 Event Key | 授权后台接入。本研究只读文档，未请求此端点、未提取/使用 key |
| 批量 | `events[]`，最多100；文档说任一非法事件使批次失败 | 200/400/401语义为接口声明，不是本轮观测响应 |
| 事件 | `name/data/event_time/event_source_url/user_data`；可选 `dedupe_id/measurement_partner_data` | 时间是毫秒 epoch，source_url为完整事件页面URL，应避免敏感信息混入 |
| 请求环境 | client_ip_address、client_user_agent、esi(web/app) | 文档要求真实用户环境；本轮未收集、未伪造 |
| 标识 | client_id、axwrt、alart、user_id、email、phone 中至少一项；aleid/alart等有“存在时传递”的条件 | 表中带星号的“required”不是要求同时提供所有联系方式。client_id为稳定第一方标识 |
| 其他匹配 | 可选ifa、idfv、sid、country_code、zip等 | 能用于匹配不等于任意网站拥有或允许发送这些字段 |
| 衡量伙伴 | accounting_mode、attribution_model、attribution_share、is_claimable；可选campaign/creative_set及新老客时间信息 | 第三方衡量结果可告知该事件给AppLovin多少归因信用，不等于服务端训练特征已公开 |

**归因链的具体证据**：点击URL带 `aleid/alart`；Pixel 可存 `_axeid/_axart`，服务器可将其回传到 user_data；`_axwrt` 是 Pixel 的第一方 visitor 标识。`dedupe_id` 是事件幂等键，**不同于点击归因 aleid**。

【官方公开证实】[dedupe 原文](nongame/doc-dedupe.txt)要求 Pixel/CAPI/Android/iOS 对同一动作使用同一 `dedupe_id`；写明30秒内合并、超过5分钟到达的后续同ID事件丢弃。**取得页面没有完整说明30秒到5分钟之间的行为，保持未确认**，不把它描述成无时限恰好一次。历史订单另按 `transaction_id` 去重，不是同一个接口规则。

### Shopify / 订单历史

【官方公开证实】[Shopify指南](nongame/doc-shopify.txt)要求安装 App、连接 Ads Manager、启用并保存主题扩展；[Shopify商店](https://apps.shopify.com/axon)提供 Pixel、目录同步、购买归因等说明。安装范围见权限条款/商家授权，不是任意网站默认进入。

【公开网页代码证实】HexClad、Resparked、True Classic 的实际 HTML 均引用 `applovin-shop-integration-103/assets/app-embed.js`。该资产明确：

1. `_axGetAleid` 从 aleid/axeid URL 参数、`_axeid` cookie或localStorage读取归因标记。
2. 有标记才调用 `_axUpdateCartAttributes`，把它写为购物车属性 `_axon_event_id`；存在校验与最多3次尝试的默认参数。
3. `/v1/log` 是诊断日志路径，可包含当前URL；**不是购买转化接口**。

这些方法是静态读取，**本研究没有执行对商家 cart/update.js 的 POST**。不能将主题脚本只追到购物车的证据写成“订单已发送成功”。[NG05](EVIDENCE_INDEX.md#ng05)

【官方公开证实】[Order history](nongame/doc-order-history.txt)是最直接的**价值建模用途证据**：为 prospecting 建模既有客户，寻找新高价值用户。CSV包含country/currency、email、event_name=purchase、event_timestamp、transaction_id、user_id、value，部分其他标识可选；按订单号去重。商家需符合自己的告知与同意义务。历史收入与实时购买不可重复累计。

## 4. 独立 Axon App SDK，不能只研究 MAX

【官方公开证实】当前[Android指南](nongame/doc-android-axon.txt)使用 `com.applovin:axon-sdk:+`，最低API24；[iOS指南](nongame/doc-ios-axon.txt)使用 `AxonSDK`，最低iOS12/Xcode15。文档注明该集成在西欧当前不可用，需要核实具体国家，不能把获取发行包理解为当地可投放授权。

【SDK代码证实】Maven1.3.4的原始公共API：

- [Axon](nongame/sdk/axon/1.3.4/Axon.javap.txt)：initialize、getEventService、setUserData、processDeepLink。
- [AxonEventService](nongame/sdk/axon/1.3.4/AxonEventService.javap.txt)：三个 trackEvent 重载，含parameters/options。
- [AxonUserData](nongame/sdk/axon/1.3.4/AxonUserData.javap.txt)：email/phone/userId。
- [AxonPrivacySettings](nongame/sdk/axon/1.3.4/AxonPrivacySettings.javap.txt)：hasUserConsent、setDoNotSell及设置状态API。

这是**公共API二进制证据，不是该独立包全部队列/网络实现逆向完成**。不能把MAX旧版本的队列实现直接套上。官方文档称 SDK 在设备上 SHA-256 处理邮箱/电话，邮箱域名明文、publisher user ID按提供值发送；CAPI在服务端可接明文后哈希，路径不同。哈希仍可匹配，**不是匿名化保证**。[NG03](EVIDENCE_INDEX.md#ng03)

## 5. 是否用于 Axon、是否用于游戏

【官方公开证实】[Axon AI官方说明](https://legal.applovin.com/about-applovins-axon-ai/)明确模型使用设备/网络、应用/广告/其他数字属性互动、广告主选择分享的数据、MAX win/loss通知；[转化衡量文档](nongame/doc-attribution.txt)说明关联广告互动与购买以报告及优化。网站目前支持D0/D7优化，展示更长报告窗口不等于对应优化窗口已启用。

【官方公开证实】[隐私政策](nongame/applovin-policy-direct.txt)公开跨app/设备/技术的收集与结合，以及将某app/网站动作与其他app/网站行为结合用于相关广告；电商专用类别单列。**所以不能说“完全没有跨场景关联公开证据”。**

但【无法确认】没有官方证据将某商家购物车/订单逐字段映射为某款游戏IAA预测特征；没有数据字典、训练边界、消融结果或目标游戏生产日志。**“授权数据可用于总体AI服务”不等于“所有电商数据默认训练游戏模型”。**商业身份匹配能力也不等于已重建个人身份或有证实的跨设备图谱。

隐私条件见[Data Sharing Requirements](nongame/doc-data-sharing.txt)：商家可访问的披露、必要同意、尊重opt-out、不得传敏感/儿童数据。本轮没有检查或改变任何真实用户的同意状态。[NG01](EVIDENCE_INDEX.md#ng01) [NG09](EVIDENCE_INDEX.md#ng09)
