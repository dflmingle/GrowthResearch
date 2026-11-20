# 来源目录与复核范围

原始JAR未改；源码副本按归档成员字节核对，MIT LICENSE保留在每个版本目录。正式发布日期未确认，不能以HTTP Last-Modified替代。完整逐方法证据见CODE_EVIDENCE.json，附源码SHA及调用方法/行号；没有SDK执行证据。

| 样本 | 版本 | 原始下载URL | 本地归档 | SHA256 |

|---|---|---|---|---|

| OSM034 | 5.5.0 | https://repo.maven.apache.org/maven2/com/adjust/sdk/adjust-android/5.5.0/adjust-android-5.5.0-sources.jar | ThirdPartySDKs/Adjust/Android/5.5.0/adjust-android-5.5.0-sources.jar | `e76d574c1155d74dbc11db8ee6fd043a10b41062c722e590ac8663f30edd7792` |

| OSM036 | 5.7.0 | https://repo.maven.apache.org/maven2/com/adjust/sdk/adjust-android/5.7.0/adjust-android-5.7.0-sources.jar | ThirdPartySDKs/Adjust/Android/5.7.0/adjust-android-5.7.0-sources.jar | `6e92756c8419253619aa57dbf6a7127e6533f8c3fecd42c672f84772d7b8c8be` |

| OSM038 | 5.8.1 | https://repo.maven.apache.org/maven2/com/adjust/sdk/adjust-android/5.8.1/adjust-android-5.8.1-sources.jar | ThirdPartySDKs/Adjust/Android/5.8.1/adjust-android-5.8.1-sources.jar | `dfee5dda1f80d86b1e0af56af77e04568f7929462a5fe09ffd6b75254180030b` |


## 本轮新增公开法律响应

只有以下5次GET，没有新SDK下载或广告/身份服务请求。所有URL、时间及重定向见license-review/FETCH_MANIFEST.json。

| ID | 原始URL | HTTP | SHA256 |

|---|---|---|---|

| max-1320-license | https://raw.githubusercontent.com/AppLovin/AppLovin-MAX-SDK-Android/release_13_2_0/LICENSE.md | 200 | `e736ae9fee62d3e70c9325b848aaf1b37351117889fab3472dee84acec0612f8` |

| max-1364-license | https://raw.githubusercontent.com/AppLovin/AppLovin-MAX-SDK-Android/release_13_6_4/LICENSE.md | 200 | `e736ae9fee62d3e70c9325b848aaf1b37351117889fab3472dee84acec0612f8` |

| max-1370-license | https://raw.githubusercontent.com/AppLovin/AppLovin-MAX-SDK-Android/release_13_7_0/LICENSE.md | 200 | `e736ae9fee62d3e70c9325b848aaf1b37351117889fab3472dee84acec0612f8` |

| lp-unity-930-license | https://raw.githubusercontent.com/ironsource-mobile/Unity-sdk/UnityLevelPlay_9.3.0/LICENSE | 200 | `4aa74c09508382bcf26b4d62928ece88bb268fff609f901aee999e102e8a070e` |

| max-eula-trailing-slash | https://www.applovin.com/eula/ | 200 | `67becda1a1c415680cbafe118796a2da519b826b521b3b5563224f91a7cf9f53` |


## 复用证据

[首轮许可与版本证据](../official-samples-audit/LICENSE_EVIDENCE.json)、[版本元数据](../official-samples-audit/VERSION_PROVENANCE.json)、[47样本目录](../official-samples-audit/ACQUIRED_SAMPLE_CATALOG.csv)。没有改写首轮报告或旧结论。

本轮代码辅助器只做读取、定位、文本差分、哈希和文档写入；初始词法定位有泛型返回方法盲区，补定位已经显式写入CODE_EVIDENCE。不能用本工具证明完整调用图或无其他服务端机制。
