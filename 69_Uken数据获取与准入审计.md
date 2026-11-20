# Uken真实游戏数据：获取与准入审计

2026-11-20。**Uken“30万行”有可追溯的2015年SFU竞赛参与者材料，但原始数据没有公开再分发权限。本轮未取得玩家文件，训练STOP。**

## 已定位来源与证据层级

原参与者仓库：[nathanesau-academic/ukencompetition](https://github.com/nathanesau-academic/ukencompetition)。README说明竞赛为SFU统计部门2015年秋季活动，团队Nathan Esau、Steve Kane；分析代码头部写Updated December 6, 2015，海报写September 2015。这些分别是作者声称的活动/代码时间，不能替代原始玩家事件起止日期。

【参与者一手材料；非数据权利方授权】README原文：

> “I do not have permission to upload the Data to GitHub.”

> “300,000 rows (250,000 training rows with known target variables and 50,000 test rows with unknown target variables).”

另一仓库jtatineni/ukencompetition的README字节与上述相同，不能算独立数据源或第二款游戏。原件、SHA256和位置：GI69S_uken_participant；树清单GI69S_uken_tree；代码GI69S_uken_code；海报GI69S_uken_poster，均见[证据索引](game-industry69/SOURCE_CATALOG.md)。未下载Predictions/predictions.csv，因为预测输出不是原始真实标签，也无明确再利用许可。

## 44字段究竟说明什么

| 字段组 | 参与者给出的含义 | 预测可用性边界 |
|---|---|---|
| obs、user_id | 行ID、用户ID | 不能直接作预测特征；跨安装/跨游戏稳定性无原契约 |
| install_date、platform、platform2_install_date、country、gender | 安装日期、iPad/iPhone、第二次平台安装日期、国家、性别 | 只有预测前已知部分可用；第二平台时间可能晚于预测时点；不需要收集敏感/真实身份字段 |
| return_player | 观察期末是否玩；海报进一步写安装后30日是否返回 | 不是收入；README与海报粒度不同，需原题定义确认D30具体区间 |
| revenue、engagement | 花钱多少、游玩时间多少的“measure” | 未给币种、缩放/归一化公式、累计窗口、退款或收入净额；不得称美元D28 LTV |
| fb_connect、tutorial_completed、first_game_played | 首次Facebook连接、教程完成、首局日期 | 只证明字段描述，不证明可访问第三方账号；不能利用预测时点后的事件 |
| first_type_1_game至first_type_4_game、first_win、first_bonus | 首次模式、胜利、奖励事件日期 | 可作为早期行为候选；缺少完整重复事件、时长与available_at |
| first_purchase_a、first_special_purchase、first_purchase_b至h | 各种购买首次发生日期 | 不能恢复每笔金额/收入序列；整期首次购买可能泄漏未来标签 |
| first_gift_sent/received、first_gift2_received、first_uken_gift_received | 首次赠礼/收礼日期 | 不是收入，也不证明社交身份图谱 |
| first_collection、first_prize_a至c、stage1至7 | 首次收藏、奖品、关卡日期 | 必须按as-of裁切；不能用全观察期“到过第七关”预测更早收入 |
| training0validation1 | 原竞赛训练/测试标记 | 不证明时间外切分、客户独立或标签已成熟 |

README原始字典完整保存在[原文](game-industry69/sources/uken-case2-readme.html)，不通过名称擅自扩充。原文说未发生的事件为空；国家/性别也可缺失，测试集三个目标为空。**事件为空、未知人口属性、无测试标签是不同缺失机制**；目标缺失不能当零消费。

## 缩放、时间窗与泄漏审计

【无法确认】未取得NDA、原始竞赛题目、权利方字段字典、revenue/engagement缩放方式、观察起止和退出规则。海报均值/偏态图没有货币单位，不能反推缩放因子或训练真实收入精度。

【代码证实；仅参与者处理方法】analysis.R读取Data/user_stats.csv，把首事件日期减install_date得到天数，未发生事件填-1，StageCount统计stage列非空；原始文件未上传。该流程不是已证明无泄漏的早期预测：若首次购买、全部关卡或再次安装发生在观察截止后的未来，而仍被用于预测，模型就看到了未来。本轮未运行这段代码，也未采纳海报“特征重要所以改关卡可提高收入”的因果结论。

“安装后第k日早期行为→D28收入”的实验需要原方明确：输入事件仅到k日；标签是同一固定区间的实际收入；标签窗口成熟；每个用户在整个标签窗确实被覆盖。若只拿到一行整期摘要而无裁切规则，只能研究该摘要与该目标的统计关联，不能宣称未来收入预测。

## 申请前材料与待确认问题（未发送）

建议准备一页研究说明：申请主体/负责人、非商业或商业目的如实填写、仅游戏内匿名键、禁止跨来源个人联结、受控存储与访问者、保存/销毁期限、仅发布聚合结果、是否允许模型产物及论文公开、伦理/合同审查状态。不得预先承诺不符合实际的学术身份或用途。

向Uken权利方及SFU活动机构确认以下问题，而不是默认竞赛参与者能转授权：

1. 原始2015竞赛数据是否仍可申请？谁是许可人，现行协议/NDA全文与申请入口是什么？
2. 30万行代表独立用户、安装、账号还是其他单位？250k/50k如何抽样，是否含完整零收入人群？
3. revenue/engagement的单位、缩放、截尾、目标日期、金额币种、IAP/IAA构成及退款口径是什么？
4. 每个输入事件观察到哪天，目标观察到哪天？是否可提供事件时间、可用时间、覆盖水位和退出说明？
5. 可否提供脱敏的安装cohort与D0/D7/D28实际收入，以及不含个人跨游戏键的至少第二款独立游戏？
6. 是否允许当前用途、模型训练、派生成果发布与删除验证？不得把软件MIT/GitHub可见性当作原数据许可。

可核验的公司入口：[Uken](https://uken.com/)，但本轮试查/data返回404；没有确认专门的研究申请通道。作者仓库只用于追踪原活动与题目，不发邮件、不签约、不索取个人标识。

## 最终准入

来源可追溯性：参与者层面LIMITED；完整字段原契约/缩放/用户稳定性/真实零值/观察完整性/固定未来窗口：UNKNOWN；实际文件和现行数据许可：未取得。**STOP**。

另有项目宣称310K Uken-inspired玩家，README明确“synthetically generated”，已排除，不作为可绕开权限的替代品。若下一步无法获得权利方协议与时间定义，应停止Uken训练方向，保留文献价值。
