# 69：Complete Journey原始来源、处理血缘与观察覆盖

2026-11-20。**不能区分真实零消费、发布账本无记录和家庭退出观察。新增代码证据还证明：当前RDS是人工映射日历、合成秒数、删除一个假定停业日后的处理版本，不能当作2017真实自然日历或原始到达时间。**本轮无训练、无UCI使用。

## 1. 来源链：确证与断点

| 层次 | 已取得材料 | 可以证明 | 不可以证明 |
|---|---|---|---|
| 数据包发行者 | Brad Boehmke/Steven Mortimer的DESCRIPTION、README、vignette、data-raw/prep-data.R、历史commit与issue | 数据包作者、字段说明、加工与原84.51°研究引用，包声明CC0 | 原始研究全量合同、原采集年份、家庭进入/退出 |
| 原始经营数据来源 | 包作者指向84.51° Complete Journey，prep读取本地Complete_Journey_UV_Version/transaction_data.csv | 作者明确承认来自该源，并公开处理脚本 | 本地原CSV没有随包核验；没有原导出到RDS的完整逐行对账 |
| 原运营方门户 | 84.51° area51两个公开URL连接失败；dunnhumby source-files页面可读 | 后者同名研究描述2500常客家庭、两年、店内全品类采购 | 不把同名页面当作当前2469家庭RDS的逐字节同源证明 |
| 当前网站User Guide | source-files指向PDF已下载 | PDF自身是2023“Let's get sort-of-real”dummy data | **不是Complete Journey原始指南**，不能引用其匿名客户/时间定义来补原研究 |

公开仓库issue #9称曾使用“original 84.51 Word document”完成vignette，但本轮当前/历史树中未取得该原Word。未找到可直接核验家庭入样/退样的原论文附录或观察台账。包作者的描述与代码比同名教程更强，但不能补齐未发布合同。

## 2. 2017与秒数：代码和原件双重核验

来源：[prep-data.R](public-experiments/round69/sources/journey-prep.txt)；原URL和哈希见[来源索引](69_原始数据来源及作者证据索引.csv)。以下均为【发布者代码证实】，不是研究者猜测：

| 位置 | 实际操作 | 对价值研究的影响 |
|---|---|---|
| lines8—12 | 取原day>=285且day<650，用2017-01-01+(day-285)映射 | 文件年份2017是重基准，不证明真实采集年份。不能凭它与REES46的2020建立真实跨来源时间先后 |
| lines15—16 | 删除映射2017-12-25的“一条零散交易”，作者注释是假定闭店 | 无记录日是发布加工产生，不能当原始真实零消费、真实闭店或系统停采证据 |
| lines17—22 | 秒数取basket_id末两位×60/100后取整数 | 注释称random，但公式为**确定性构造**；秒级先后不是原始采集精度 |
| lines24—29 | 改映射DST日02点→03点，使用America/New_York构造POSIXct | 时区来自作者处理；不能称原店铺所在时区或原服务器到达时间 |
| lines30—37 | 正的retail_disc设0，再把三种discount取绝对值 | 折扣字段已改写，不能套原CSV负数公式或直接加减得到验真现金 |
| lines39—50 | household_key重命名household_id，ID转字符，排序并保存RDS | 源内键转换明确；没有跨零售商或自然人关联契约 |

[原件验证](public-experiments/round69/JOURNEY_PREPROCESSING_VERIFICATION.json)对全部1,469,307行核验：秒数100%匹配该公式；转换到作者指定时区后全在映射2017年，范围01-01 06:53:26至12-31 23:01:20。UTC末端2018-01-01只是时区表示，**不是第二年观察期**；映射全年唯一无交易日为12-25，恰与代码删除一致。原件哈希不变。

issue #8由作者讨论“fictitious starting date”、前100天销售渐增，并建议裁一年；维护者评论给出完成commit a26f1578c7c2ad69e3198b9b86f922f1019759a5。NEWS亦明确裁至2017以删除异常消费模式。不能把处理后的平稳一年称为原研究无选择的完整面板。

这些发现**细化并纠正68号**“2017全年”“时区未证”的解释。68号原文件保留；当前能证明映射日历和处理时区，仍不知道真实原始日历。

## 3. sales_value是什么

作者vignette Transactions段原文：

> “It is not the actual price paid by the customer.”

说明sales_value是零售商在该商品销售获得的dollars，考虑coupon match及loyalty card discount；若顾客使用manufacturer coupon，其实付额低于sales_value，因为制造商补偿零售商。【发布者文档证实】

所以，sales_value不是顾客个人实际现金消费，也不是单品标价、净利润或广告IAA/IAP。字段文档写dollars，但没有ISO币种字段、财务对账、税费/退款/结算完整说明；不自行把“美元”或“已净退款”写成已证结论。quantity、basket_id、product_id等名称明确，原件sales_value无负数不证明没有退款；赠品/零量/冲销原因也未知。

作者vignette还含折扣价格公式及示例，prep随后已将符号改为绝对值。没有在本轮套公式生成替代收入标签，更没有把sales_value再次扣减成“真现金”。

## 4. 三种不同的无记录

| 状态 | 当前可见性 | 允许结论 |
|---|---|---|
| 发布账本窗口内没留下行 | 可查询这个文件 | 仅“此文件在该窗口没有记录”；处理曾删日/选期 |
| 家庭在完整观察时确实没在此零售商购买 | 无逐户观察风险集或漏采标记 | 无法认证；更不能推出全市场零消费 |
| 家庭退出、换卡、换户、漏传或不再可观测 | 没有entry/exit、卡绑定变化、采集健康或到达日志 | 无法与第二种状态区分 |

原站/README说frequent shoppers和all purchases within store，没有说明“每个家庭从期初到期末都持续可观测”。最早/最晚保留购买日期只代表活动边界，不是入样/退样时间。首次出现在6月不能据此认定6月入样；末次购买在9月不能证明9月流失。

[聚合验证](public-experiments/round69/JOURNEY_PREPROCESSING_VERIFICATION.json)只输出首次/末次购买月份家庭计数，不输出ID，也不把这些月份转成观察区间。全年完整无字段缺失与“无缺事件”是不同命题。

transaction_timestamp为加工后的事件时间；没有received_at、available_at、水位或延迟记录。未来7/28相对窗口可在文件上定义，但不是已认证真实完整成熟收入。

## 5. 八项准入及剩余最小材料

| 维度 | 当前判断 |
|---|---|
| 来源真实性 | 作者发行与所称原研究可追溯；原始CSV未核验，RDS明确是处理物 |
| 字段语义 | 核心字段明确；sales_value已确认不是顾客实付 |
| 用户键稳定 | household_key→household_id转换明确；长期换卡/成员变化/退出稳定性未知 |
| 金额真实性 | 文档称实际零售销售值；未独立财务核验，不能替代顾客现金 |
| 币种/退款 | dollars声明；ISO及退款/税费/净额未证 |
| 观察起止 | 处理窗已证，家庭真实入样/退样未证 |
| 零值/缺失 | 不可区分 |
| D7/D28成熟 | 文件相对时间可算；真实完整目标未认证 |

**完整真实用户未来价值预测：STOP。**可GO的仅是源内字段/加工/发布账本审计。若另开受限问题，应命名为“Complete Journey处理后发布账本的未来7/28相对日零售商sales_value预测”，不得称完整消费LTV，不在本轮训练或默认批准训练。

恢复至少需要原day与真实日期映射、原始CSV及其退款/货币说明、逐家庭可观测起止/换卡/退出、漏采与到达记录。现有公开源码已给出加工边界，没有上述材料就不继续用首末购买猜观察资格。
