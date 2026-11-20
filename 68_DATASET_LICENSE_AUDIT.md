# 68号：数据许可与实际可下载性审计

2026-11-20。本轮不使用UCI Online Retail，不训练模型。核验17个候选：许可、真实性和预测准入分开判断。**可公开下载不等于CC0；页面许可不等于数据许可；文件存在不等于足以预测成熟真实价值。**

## 本轮实际取得

| 发行物 | 实际取得与解析 | 许可证据 | 本轮允许范围 |
|---|---|---|---|
| Complete Journey | 官方数据包作者仓库全量RDS，12,775,661字节，1,469,307行；不是75,000行sample | R数据包DESCRIPTION明示CC0，README明确数据包和原84.51°来源；原门户本轮连接失败 | 本地结构/金额/完整性审计；记录上游CC0声明，未把无法访问原门户写成已核验原合同 |
| REES46 Jewelry | 官方平台所链接的发布者Kaggle完整ZIP，CRC通过，95,911行无表头 | Kaggle通用licenseName为“Data files © Original Authors”，但description明确免费使用并要求数据页+REES46双署名 | 符合公开文字的本地使用和聚合审计；不是CC0，不自行授予原始数据再分发/再识别权限 |
| REES46 Electronics | 完整ZIP，52,914,925字节，2,633,521行，CRC通过 | 同上；REES46原站也列出电子交易、珠宝、化妆品等不同数据源 | 聚合审计；缺键/日期/金额问题导致训练STOP |
| Vibrent | 仅3个相关CSV完整下载：original_orders、spot_rentals、subscription_plan | 原作者研究卡声明CC BY4并给出RecSys2024论文 DOI 10.1145/3640457.3688174 | 带论文署名的租赁行为/字段审计，不将套餐价格视为扣款 |
| Cosmetics | October ZIP HTTP200，仅读取262,144压缩字节后停止；提取表头，未保存事件行 | REES46同一免费使用/双署名条款 | 只证明该URL可取到ZIP前缀与字段结构，不是全量下载、时间连续或质量核验 |

准确URL、时间、字节和SHA256见[下载记录](public-experiments/round68/ASSET_ACQUISITION.json)、[电子交易下载](public-experiments/round68/ASSET_ELECTRONICS.json)；原件位于round68/raw，只读使用，不向报告输出原始匿名键。

## 必须停止或保持未知的授权

- Criteo Sponsored Search官方明示CC BY-NC-SA4。本项目商业增长研发不擅自等同NonCommercial，未下载数据；即使获准，它也是广告主转化销售额，不是媒体IAA。
- Olist官方数据为CC BY-NC-SA4。本轮未下载、未训练；多seller不自动构成独立产品/完整用户账本。
- Ta Feng第三方Kaggle页声明CC0，但原始数据授权链未建立。没有用上传者徽章替代原始权利；未下载。
- Google Flood-It!/GA4/UA样本需要可用Cloud项目。未检查或使用任何现有账号凭证、未启用计费、未提交查询。文档页CC BY4/代码Apache2不能代替BigQuery数据条款核验。
- KKBox竞赛data/rules页面HTTP200只返回网页壳，未取得规则正文和文件，不绕过登录/点击同意。
- “Mobile Game IAP 2025”虽CC0但明确合成；Gamelytics虽Apache2但来源仅“real-world-inspired”，累计收入无时间契约；均不准入真实收入研究。
- TikTok Shop第三方卡片声称CC0及多种收入/CAC/ROAS字段，但不是TikTok官方数据，真实经济来源无法核实。不能因字段齐全或营销措辞判为B级。

## 使用与证据范围

仅在各来源内部聚合其既有匿名household/customer/user键；不同来源的同名数字绝不比较或匹配，也不构造个人跨产品ID。不导出逐行键/预测，不抓取真实账号或广告标识。

每次原GET的公开URL、HTTP状态、采集时间、保存文档SHA256和原响应SHA256保留在FETCH_LEDGER系列；保存的是元数据/可见文档转换件，明确区分原响应哈希。二进制跳转仅记主机，不保存临时签名URL。

所有原00—67报告及66/67结果哈希封存。未修改、训练或重新调优UCI数据；未用合成数据补齐任何缺失金额。
