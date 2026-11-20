# 五款游戏 AppLovin 真实投放证据登记

2026-11-18。**【无法确认】本轮未取得任何一款目标游戏经 AppLovin 付费获客的可核验记录。**这是一项公开证据缺口，不是“未投放”结论。[AX04](EVIDENCE_INDEX.md#ax04)

## 核验标准与结果

有效的产品级记录需能核验目标包名/落地商店身份、广告主、AppLovin 媒体来源，并具有素材或活动/展示时间等上下文。单纯标题重名、媒体适配器、商店下载量、政策合作伙伴清单不满足标准。

| 目标 | 产品级 AppLovin 记录 | campaign/地区/日期/素材 |
|---|---|---|
| com.dino.race.master | 【无法确认】未取得 | 未取得 |
| com.oakever.meowdoku | 【无法确认】未取得 | 未取得 |
| com.nebula.rotaterings | 【无法确认】未取得 | 未取得 |
| color.number.paint.pixle.art.sort.jigsaw | 【无法确认】未取得 | 未取得 |
| com.oakever.arrows | 【无法确认】未取得；亦无原包 | 未取得 |

## 实际查过的公开来源

| 来源 | 保存的实际结果 | 可支持什么 |
|---|---|---|
| AppLovin 当前 gaming-apps 页 | 【AppLovin官方资料证实】Happybits/Serena Sa 的广告与 MAX 业务引述 | 其他公司案例，不能代替五款 |
| AppLovin game-inventory 页 | 【AppLovin官方资料证实】图片资源路径含 Oakever Tile Explorer、iKame Screwdom 等 | 库存营销页面的其他产品素材；不是 Meowdoku/Car 的获客案例，甚至不能由路径证明付费活动 |
| 官方 Top Creative Library | 【AppLovin官方资料证实】称素材由 AppLovin 为客户创作；保存页面没有目标包名 | 泛类目展示，不是目标投放凭据 |
| Bing / Google / DuckDuckGo / Brave | 错配查询/通用页面、challenge、202 challenge、429 | 已记录失败/不相干结果；不引用搜索噪声作证据 |
| Sensor Tower / AppMagic Car 页面 | HTTP200，但正文只取到标题/前端壳，无投放网络和素材明细 | 不能把成功取到 URL 视为取到广告情报 |
| 既有 Meta/Google/TikTok 广告库尝试 | 访问受限或通用入口；没有目标产品+AppLovin 记录 | 即使取得这些平台广告，也需另证 AppLovin，不能移植渠道结论 |

可复核原文、请求时间、HTTP/重定向见[AX04](EVIDENCE_INDEX.md#ax04)。`inventory-asset-observations.json`只保留可观察公开资源路径，未下载用户数据；旧 `/axon/`、`/success-stories/` 等地址重定向到通用首页，不当作案例文章引用。

## 后续只需什么证据

【合理推断】最有价值的是开发者自愿提供的脱敏 MMP AppLovin attribution / postback 配置和送达导出，或合法广告情报中的精确游戏×媒体记录。即使 partner 共享覆盖 organic，也不能据“发送给 AppLovin”反推它贡献了安装。当前不推算预算、实际 ROAS、CPI、受众国家或投放起始日期。
