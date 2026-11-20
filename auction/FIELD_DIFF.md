# 规范化字段全量差分

只表示本轮取得文档是否列出，不代表平台独有或生产启用。字段同名不代表条件、类型和语义相同；原始描述、章节及哈希在PROTOCOL_FIELDS.json。Unity pmp/source.schain严格保留取得文档的路径，不静默改成通用标准位置。SKAN专页、loss及宏表另见原始目录。

## request

| 路径 | 文档覆盖 | AppLovin原始章节 | Unity原始章节 |
|---|---|---|---|
| `app` | both_documented | Bid request object | request objects |
| `app.bundle` | both_documented | App object | app objects |
| `app.cat` | only_AppLovin_documented | App object |  |
| `app.content` | only_AppLovin_documented | App object |  |
| `app.content.ext` | only_AppLovin_documented | App object |  |
| `app.content.url` | only_AppLovin_documented | App object |  |
| `app.ext` | only_AppLovin_documented | App object |  |
| `app.ext.orientation_lock` | only_AppLovin_documented | App object |  |
| `app.id` | both_documented | App object | app objects |
| `app.name` | both_documented | App object | app objects |
| `app.publisher` | both_documented | App object | app objects |
| `app.publisher.ext` | only_AppLovin_documented | App object |  |
| `app.publisher.id` | both_documented | App object | publisher objects |
| `app.publisher.name` | only_AppLovin_documented | App object |  |
| `app.storeurl` | both_documented | App object | app objects |
| `app.ver` | only_AppLovin_documented | App object |  |
| `at` | both_documented | Bid request object | request objects |
| `badv` | only_AppLovin_documented | Bid request object |  |
| `bapp` | both_documented | Bid request object | request objects |
| `bcat` | both_documented | Bid request object | request objects |
| `device` | both_documented | Bid request object | request objects |
| `device.carrier` | both_documented | Device object | device objects |
| `device.connectiontype` | both_documented | Device object | device objects |
| `device.devicetype` | both_documented | Device object | device objects |
| `device.dnt` | only_AppLovin_documented | Device object |  |
| `device.ext` | only_AppLovin_documented | Device object |  |
| `device.ext.atts` | only_AppLovin_documented | Device object |  |
| `device.ext.ifv` | only_AppLovin_documented | Device object |  |
| `device.geo` | both_documented | Device object | device objects |
| `device.geo.city` | only_AppLovin_documented | Geo object |  |
| `device.geo.country` | only_AppLovin_documented | Geo object |  |
| `device.geo.dma` | only_AppLovin_documented | Geo object |  |
| `device.geo.ext` | only_AppLovin_documented | Geo object |  |
| `device.geo.ext.isp` | only_AppLovin_documented | Geo object |  |
| `device.geo.ext.org` | only_AppLovin_documented | Geo object |  |
| `device.geo.ipservice` | only_AppLovin_documented | Geo object |  |
| `device.geo.locale` | only_AppLovin_documented | Geo object |  |
| `device.geo.metro` | only_AppLovin_documented | Geo object |  |
| `device.geo.region` | only_AppLovin_documented | Geo object |  |
| `device.geo.type` | only_AppLovin_documented | Geo object |  |
| `device.geo.zip` | only_AppLovin_documented | Geo object |  |
| `device.h` | only_AppLovin_documented | Device object |  |
| `device.hwv` | both_documented | Device object | device objects |
| `device.ifa` | both_documented | Device object | device objects |
| `device.ip` | both_documented | Device object | device objects |
| `device.ipv6` | only_AppLovin_documented | Device object |  |
| `device.js` | only_AppLovin_documented | Device object |  |
| `device.language` | both_documented | Device object | device objects |
| `device.lmt` | both_documented | Device object | device objects |
| `device.make` | both_documented | Device object | device objects |
| `device.mccmnc` | only_AppLovin_documented | Device object |  |
| `device.model` | both_documented | Device object | device objects |
| `device.os` | both_documented | Device object | device objects |
| `device.osv` | both_documented | Device object | device objects |
| `device.pxratio` | only_AppLovin_documented | Device object |  |
| `device.ua` | both_documented | Device object | device objects |
| `device.w` | only_AppLovin_documented | Device object |  |
| `ext` | only_AppLovin_documented | Bid request object |  |
| `id` | both_documented | Bid request object | request objects |
| `imp` | both_documented | Bid request object | request objects |
| `imp[].banner` | both_documented | Impression object | imp objects |
| `imp[].banner.api` | both_documented | Banner object | banner objects |
| `imp[].banner.battr` | both_documented | Banner object | banner objects |
| `imp[].banner.btype` | only_AppLovin_documented | Banner object |  |
| `imp[].banner.ext.bannertype` | only_AppLovin_documented | Banner object |  |
| `imp[].banner.format` | both_documented | Banner object | banner objects |
| `imp[].banner.h` | both_documented | Banner object | banner objects |
| `imp[].banner.id` | only_AppLovin_documented | Banner object |  |
| `imp[].banner.pos` | both_documented | Banner object | banner objects |
| `imp[].banner.w` | both_documented | Banner object | banner objects |
| `imp[].bidfloor` | both_documented | Impression object | imp objects |
| `imp[].displaymanager` | both_documented | Impression object | imp objects |
| `imp[].displaymanagerver` | both_documented | Impression object | imp objects |
| `imp[].exp` | only_AppLovin_documented | Impression object |  |
| `imp[].ext` | only_AppLovin_documented | Impression object |  |
| `imp[].ext.ad_unit_name` | only_AppLovin_documented | Impression object |  |
| `imp[].ext.skadn` | both_documented | Impression object | imp objects |
| `imp[].ext.skadn.ext.ask` | only_Unity_documented |  | imp objects |
| `imp[].ext.skadn.productpage` | only_Unity_documented |  | imp objects |
| `imp[].ext.skadn.skadnetids` | only_AppLovin_documented | Impression object |  |
| `imp[].ext.skadn.skadnetlist.excl` | only_AppLovin_documented | Impression object |  |
| `imp[].ext.skadn.skadnetlist.max` | only_AppLovin_documented | Impression object |  |
| `imp[].ext.skadn.skoverlay` | only_Unity_documented |  | imp objects |
| `imp[].ext.skadn.sourceapp` | only_AppLovin_documented | Impression object |  |
| `imp[].ext.skadn.version` | only_AppLovin_documented | Impression object |  |
| `imp[].ext.skadn.versions` | only_AppLovin_documented | Impression object |  |
| `imp[].ext.skadnetids` | only_AppLovin_documented | Impression object |  |
| `imp[].id` | both_documented | Impression object | imp objects |
| `imp[].instl` | both_documented | Impression object | imp objects |
| `imp[].metric` | only_AppLovin_documented | Impression object |  |
| `imp[].metric[].type` | only_AppLovin_documented | Metric object |  |
| `imp[].metric[].value` | only_AppLovin_documented | Metric object |  |
| `imp[].metric[].vendor` | only_AppLovin_documented | Metric object |  |
| `imp[].native` | only_AppLovin_documented | Impression object |  |
| `imp[].native.api` | only_AppLovin_documented | Native object |  |
| `imp[].native.battr` | only_AppLovin_documented | Native object |  |
| `imp[].native.eventtrackers` | only_AppLovin_documented | Native object |  |
| `imp[].native.request` | only_AppLovin_documented | Native object |  |
| `imp[].native.request.assets` | only_AppLovin_documented | Native object |  |
| `imp[].native.request.assets[«n»].data` | only_AppLovin_documented | Native object |  |
| `imp[].native.request.assets[«n»].id` | only_AppLovin_documented | Native object |  |
| `imp[].native.request.assets[«n»].img.hmin` | only_AppLovin_documented | Native object |  |
| `imp[].native.request.assets[«n»].img.type` | only_AppLovin_documented | Native object |  |
| `imp[].native.request.assets[«n»].img.wmin` | only_AppLovin_documented | Native object |  |
| `imp[].native.request.assets[«n»].required` | only_AppLovin_documented | Native object |  |
| `imp[].native.request.context` | only_AppLovin_documented | Native object |  |
| `imp[].native.request.privacy` | only_AppLovin_documented | Native object |  |
| `imp[].native.request.seq` | only_AppLovin_documented | Native object |  |
| `imp[].native.ver` | only_AppLovin_documented | Native object |  |
| `imp[].rwdd` | only_AppLovin_documented | Impression object |  |
| `imp[].secure` | both_documented | Impression object | imp objects |
| `imp[].tagid` | both_documented | Impression object | imp objects |
| `imp[].video` | both_documented | Impression object | imp objects |
| `imp[].video.api` | both_documented | Video object | video objects |
| `imp[].video.battr` | both_documented | Video object | video objects |
| `imp[].video.companiontype` | both_documented | Video object | video objects |
| `imp[].video.ext.videotype` | only_AppLovin_documented | Video object |  |
| `imp[].video.h` | both_documented | Video object | video objects |
| `imp[].video.linearity` | both_documented | Video object | video objects |
| `imp[].video.maxbitrate` | only_AppLovin_documented | Video object |  |
| `imp[].video.maxduration` | both_documented | Video object | video objects |
| `imp[].video.mimes` | both_documented | Video object | video objects |
| `imp[].video.minbitrate` | only_AppLovin_documented | Video object |  |
| `imp[].video.minduration` | both_documented | Video object | video objects |
| `imp[].video.placement` | both_documented | Video object | video objects |
| `imp[].video.playbackmethod` | only_AppLovin_documented | Video object |  |
| `imp[].video.plcmt` | only_AppLovin_documented | Video object |  |
| `imp[].video.pos` | both_documented | Video object | video objects |
| `imp[].video.protocols` | both_documented | Video object | video objects |
| `imp[].video.sequence` | only_Unity_documented |  | video objects |
| `imp[].video.skip` | only_Unity_documented |  | video objects |
| `imp[].video.skipafter` | only_AppLovin_documented | Video object |  |
| `imp[].video.skipmin` | only_AppLovin_documented | Video object |  |
| `imp[].video.startdelay` | only_AppLovin_documented | Video object |  |
| `imp[].video.w` | both_documented | Video object | video objects |
| `pmp` | only_Unity_documented |  | request objects |
| `pmp.deals` | only_Unity_documented |  | pmp objects |
| `pmp.deals[].at` | only_Unity_documented |  | deal objects |
| `pmp.deals[].id` | only_Unity_documented |  | deal objects |
| `pmp.private_auction` | only_Unity_documented |  | pmp objects |
| `regs` | both_documented | Bid request object | request objects |
| `regs.coppa` | only_Unity_documented |  | regs object and extensions |
| `regs.ext.ccpa` | only_AppLovin_documented | Bid request object |  |
| `regs.ext.consent` | only_AppLovin_documented | Bid request object |  |
| `regs.ext.gdpr` | both_documented | Bid request object | regs object and extensions |
| `regs.ext.lgpd` | only_Unity_documented |  | regs object and extensions |
| `regs.ext.us_privacy` | both_documented | Bid request object | regs object and extensions |
| `source` | both_documented | Bid request object | request objects |
| `source.ext` | only_AppLovin_documented | Bid request object |  |
| `source.ext.fd` | only_Unity_documented |  | source objects |
| `source.ext.header_bidding` | only_Unity_documented |  | source objects |
| `source.ext.omidpn` | only_Unity_documented |  | source objects |
| `source.ext.omidpv` | only_Unity_documented |  | source objects |
| `source.pchain` | only_Unity_documented |  | source objects |
| `source.schain` | only_Unity_documented |  | source objects |
| `source.schain.complete` | only_Unity_documented |  | schain objects |
| `source.schain.nodes` | only_Unity_documented |  | schain objects |
| `source.schain.nodes[].asi` | only_Unity_documented |  | nodes objects |
| `source.schain.nodes[].hp` | only_Unity_documented |  | nodes objects |
| `source.schain.nodes[].rid` | only_Unity_documented |  | nodes objects |
| `source.schain.nodes[].sid` | only_Unity_documented |  | nodes objects |
| `source.schain.ver` | only_Unity_documented |  | schain objects |
| `tmax` | both_documented | Bid request object | request objects |
| `user` | both_documented | Bid request object | request objects |
| `user.data` | only_AppLovin_documented | Bid request object |  |
| `user.data.name` | only_AppLovin_documented | Bid request object |  |
| `user.data.segment` | only_AppLovin_documented | Bid request object |  |
| `user.ext` | only_AppLovin_documented | Bid request object |  |
| `user.ext.consent` | both_documented | Bid request object | user object extension |
| `user.ext.gdpr` | only_AppLovin_documented | Bid request object |  |
| `user.id` | only_AppLovin_documented | Bid request object |  |

## response

| 路径 | 文档覆盖 | AppLovin原始章节 | Unity原始章节 |
|---|---|---|---|
| `bidid` | both_documented | Bid response object | response objects |
| `cur` | both_documented | Bid response object | response objects |
| `id` | both_documented | Bid response object | response objects |
| `nbr` | both_documented | Bid response object | response objects |
| `seatbid` | both_documented | Bid response object | response objects |
| `seatbid[].bid` | both_documented | Seatbid object | seatbid objects |
| `seatbid[].bid[].adid` | both_documented | Bid object | bid objects |
| `seatbid[].bid[].adm` | both_documented | Bid object | bid objects |
| `seatbid[].bid[].adomain` | both_documented | Bid object | bid objects |
| `seatbid[].bid[].api` | both_documented | Bid object | bid objects |
| `seatbid[].bid[].apis` | only_AppLovin_documented | Bid object |  |
| `seatbid[].bid[].attr` | both_documented | Bid object | bid objects |
| `seatbid[].bid[].bundle` | both_documented | Bid object | bid objects |
| `seatbid[].bid[].burl` | both_documented | Bid object | bid objects |
| `seatbid[].bid[].cat` | both_documented | Bid object | bid objects |
| `seatbid[].bid[].cid` | both_documented | Bid object | bid objects |
| `seatbid[].bid[].crid` | both_documented | Bid object | bid objects |
| `seatbid[].bid[].dealid` | both_documented | Bid object | bid objects |
| `seatbid[].bid[].ext` | only_AppLovin_documented | Bid object |  |
| `seatbid[].bid[].ext.appid` | only_Unity_documented |  | bid.ext objects |
| `seatbid[].bid[].ext.appname` | only_Unity_documented |  | bid.ext objects |
| `seatbid[].bid[].ext.clickablevideo` | only_Unity_documented |  | bid.ext objects |
| `seatbid[].bid[].ext.clicktrackers` | only_AppLovin_documented | Bid object |  |
| `seatbid[].bid[].ext.crtype` | both_documented | Bid object | bid.ext objects |
| `seatbid[].bid[].ext.duration` | only_AppLovin_documented | Bid object |  |
| `seatbid[].bid[].ext.imptrackers` | both_documented | Bid object | bid.ext objects |
| `seatbid[].bid[].ext.length` | only_Unity_documented |  | bid.ext objects |
| `seatbid[].bid[].ext.skadn` | only_AppLovin_documented | Bid object |  |
| `seatbid[].bid[].ext.skadn.campaign` | only_AppLovin_documented | Bid object |  |
| `seatbid[].bid[].ext.skadn.ext.ask` | only_Unity_documented |  | bid.ext objects |
| `seatbid[].bid[].ext.skadn.fidelities[]` | only_AppLovin_documented | Bid object |  |
| `seatbid[].bid[].ext.skadn.fidelities[«n»].fidelity` | only_AppLovin_documented | Bid object |  |
| `seatbid[].bid[].ext.skadn.fidelities[«n»].nonce` | only_AppLovin_documented | Bid object |  |
| `seatbid[].bid[].ext.skadn.fidelities[«n»].signature` | only_AppLovin_documented | Bid object |  |
| `seatbid[].bid[].ext.skadn.fidelities[«n»].timestamp` | only_AppLovin_documented | Bid object |  |
| `seatbid[].bid[].ext.skadn.itunesitem` | only_AppLovin_documented | Bid object |  |
| `seatbid[].bid[].ext.skadn.network` | only_AppLovin_documented | Bid object |  |
| `seatbid[].bid[].ext.skadn.nonce` | only_AppLovin_documented | Bid object |  |
| `seatbid[].bid[].ext.skadn.productpage` | only_AppLovin_documented | Bid object |  |
| `seatbid[].bid[].ext.skadn.productpageid` | only_Unity_documented |  | bid.ext objects |
| `seatbid[].bid[].ext.skadn.signature` | only_AppLovin_documented | Bid object |  |
| `seatbid[].bid[].ext.skadn.skoverlay` | only_AppLovin_documented | Bid object |  |
| `seatbid[].bid[].ext.skadn.skoverlay.companion_delay` | only_AppLovin_documented | Bid object |  |
| `seatbid[].bid[].ext.skadn.skoverlay.dismissable` | both_documented | Bid object | bid.ext objects |
| `seatbid[].bid[].ext.skadn.skoverlay.position` | both_documented | Bid object | bid.ext objects |
| `seatbid[].bid[].ext.skadn.skoverlay.show` | only_Unity_documented |  | bid.ext objects |
| `seatbid[].bid[].ext.skadn.skoverlay.sk_dismiss_delay` | only_AppLovin_documented | Bid object |  |
| `seatbid[].bid[].ext.skadn.skoverlay.video_delay` | both_documented | Bid object | bid.ext objects |
| `seatbid[].bid[].ext.skadn.sourceapp` | only_AppLovin_documented | Bid object |  |
| `seatbid[].bid[].ext.skadn.timestamp` | only_AppLovin_documented | Bid object |  |
| `seatbid[].bid[].ext.skadn.version` | only_AppLovin_documented | Bid object |  |
| `seatbid[].bid[].ext.storeurl` | only_Unity_documented |  | bid.ext objects |
| `seatbid[].bid[].ext.vendor` | only_AppLovin_documented | Bid object |  |
| `seatbid[].bid[].h` | both_documented | Bid object | bid objects |
| `seatbid[].bid[].id` | both_documented | Bid object | bid objects |
| `seatbid[].bid[].impid` | both_documented | Bid object | bid objects |
| `seatbid[].bid[].iurl` | only_Unity_documented |  | bid objects |
| `seatbid[].bid[].lurl` | only_AppLovin_documented | Bid object |  |
| `seatbid[].bid[].nurl` | both_documented | Bid object | bid objects |
| `seatbid[].bid[].price` | both_documented | Bid object | bid objects |
| `seatbid[].bid[].protocol` | only_AppLovin_documented | Bid object |  |
| `seatbid[].bid[].w` | both_documented | Bid object | bid objects |
| `seatbid[].seat` | both_documented | Seatbid object | seatbid objects |
