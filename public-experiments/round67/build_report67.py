"""Package the fixed independent retail experiment without altering model results/history."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,re,csv,shutil
import numpy as np
import pandas as pd
ROOT=Path(r'D:\GrowthResearch');OUT=ROOT/'public-experiments/round67';NOW=datetime.now(timezone.utc).isoformat()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(rel,content):
 p=ROOT/rel
 if p.exists():raise RuntimeError('Refuse overwrite '+rel)
 p.write_text(content.strip()+'\n',encoding='utf-8',newline='\n')
def dump(rel,obj):write(rel,json.dumps(obj,ensure_ascii=False,indent=2))
run=json.loads((OUT/'RUN_MANIFEST.json').read_text(encoding='utf-8'))
assert json.loads((OUT/'BOUNDARY_AND_PROVENANCE_TESTS.json').read_text(encoding='utf-8'))['status']=='PASS'
results=pd.read_csv(OUT/'MODEL_RESULTS.csv');test=results.loc[results.split=='test'].copy()
paired=pd.read_csv(OUT/'PAIRED_COMPARISONS.csv');strata=pd.read_csv(OUT/'STRATIFIED_ERRORS.csv');cal=pd.read_csv(OUT/'CALIBRATION_ANALYSIS.csv')
distribution=json.loads((OUT/'LABEL_DISTRIBUTIONS.json').read_text(encoding='utf-8'))
split=json.loads((OUT/'SPLIT_AND_LEAKAGE_CHECKS.json').read_text(encoding='utf-8'))
dataq=json.loads((OUT/'DATA_QUALITY_AND_MATURITY.json').read_text(encoding='utf-8'))
for rel,src in [('67_模型对照结果.csv','MODEL_RESULTS.csv'),('67_预测校准分析.csv','CALIBRATION_ANALYSIS.csv')]:
 p=ROOT/rel;assert not p.exists();shutil.copyfile(OUT/src,p)
# A ratio with zero observed sum is undefined. The inherited round66 metric used a
# zero sentinel internally; normalize only final stratified presentation, not fits.
root_strata=strata.copy();zero=root_strata.observed_mean.eq(0)
root_strata.loc[zero,['total_prediction_ratio','total_bias_pct','abs_ratio_bias']]=np.nan
root_strata['ratio_status']=np.where(zero,'N/A observed amount denominator is zero','defined')
assert not (ROOT/'67_分层预测误差.csv').exists()
root_strata.to_csv(ROOT/'67_分层预测误差.csv',index=False,encoding='utf-8',lineterminator='\n')
dump('public-experiments/round67/OUTPUT_SEMANTICS.json',{'derived_output':'67_分层预测误差.csv','zero_denominator_cells_blank':int(zero.sum()),'source_metrics_not_overwritten':True,
 'reason':'Inherited helper zero-denominator ratio sentinel is not an estimate; final CSV marks N/A. No model/feature/data/metric-for-nonzero-cohort changes.',
 'available_probabilities':['B0_GLOBAL','B2_ZERO','M3','M4'],'direct_model_probability':'N/A; no probability inferred from amount',
 'precheck_note':'PRECHECK is initial maturity-only check. A wording cleanup in protocol occurred before model execution; RUN_START/RUN_MANIFEST bind final pre-fit protocol SHA256.',
 'reported_ci':'2000 paired customer cluster draws, fixed fitted model/calibrator and dates'})

def f(x):return 'N/A' if pd.isna(x) else f'{x:.2f}'
def pc(x):return 'N/A' if pd.isna(x) else f'{100*x:.2f}%'
def main_table():
 lines=['| 模型 | MAE £ | RMSE £ | 中位绝对误差 £ | Recall@10% | Top10%金额捕获 | 预测/实际总额 |','|---|---:|---:|---:|---:|---:|---:|']
 for _,x in test.iterrows():lines.append(f'| {x.model} | {f(x.mae)} | {f(x.rmse)} | {f(x.median_ae)} | {pc(x.top10_recall)} | {pc(x.top10_value_capture)} | {x.total_prediction_ratio:.3f} |')
 return '\n'.join(lines)
def primary_table():
 d=paired.loc[paired.simultaneous_primary_8.eq(True)]
 lines=['| 预定比较 | 指标改善%（正为更好） | 点估计 | 客户配对95% CI | 8项同时控制对应99.375% CI |','|---|---|---:|---|---|']
 for _,x in d.iterrows():lines.append(f'| {x.model} 对 {x.reference} | {x.metric} | {f(x.estimate)} | [{f(x.ci95_low)}, {f(x.ci95_high)}] | [{f(x.ci99_375_low)}, {f(x.ci99_375_high)}] |')
 return '\n'.join(lines)
def probability_table():
 lines=['| 模型 | 平均购买概率 | 实际观察购买率 | Brier | Logloss | 固定10箱ECE |','|---|---:|---:|---:|---:|---:|']
 for _,x in test.loc[test.model.isin(['B0_GLOBAL','B2_ZERO','M3','M4'])].iterrows():lines.append(f'| {x.model} | {pc(x.mean_probability)} | {pc(1-distribution["test"]["no_positive_record_fraction"])} | {x.brier:.4f} | {x.logloss:.4f} | {x.ece10:.4f} |')
 return '\n'.join(lines)
tail=strata.loc[(strata.dimension=='observed_amount_tier')&(strata['group']=='positive_top1')]
tails=['| 模型 | 正额top1%时点行数 / 独立客户数 | 实际均额 £ | 预测均额 £ | 预测/实际 | 该层RMSE £ | 占全体平方误差 |','|---|---:|---:|---:|---:|---:|---:|']
for _,x in tail.loc[tail.model.isin(['FROZEN66_M2','M2','M3','M4'])].iterrows():
 overall=test.loc[test.model==x.model].iloc[0];share=x.n*x.rmse*x.rmse/(overall.n*overall.rmse*overall.rmse)
 tails.append(f'| {x.model} | {int(x.n)} / {int(x.customers)} | {f(x.observed_mean)} | {f(x.predicted_mean)} | {x.total_prediction_ratio:.3f} | {f(x.rmse)} | {pc(share)} |')
weeks=['| 测试周 | 历史日均MAE £ | 冻结66 M2 MAE £ | 67 M2 MAE £ | M3 MAE £ | M4 MAE £ | M3 Recall@10% | M4总额比 |','|---|---:|---:|---:|---:|---:|---:|---:|']
for week in split['splits']['test']['landmarks']:
 d=strata.loc[(strata.dimension=='test_week')&(strata['group']==week)].set_index('model')
 weeks.append(f'| {week} | {f(d.loc["B1_HISTORY_RATE","mae"])} | {f(d.loc["FROZEN66_M2","mae"])} | {f(d.loc["M2","mae"])} | {f(d.loc["M3","mae"])} | {f(d.loc["M4","mae"])} | {pc(d.loc["M3","top10_recall"])} | {d.loc["M4","total_prediction_ratio"]:.3f} |')
groups=['| 真实金额层（仅事后评价） | 行数 | M2 MAE £ | M3 MAE £ | M4 MAE £ | M3总额比 |','|---|---:|---:|---:|---:|---:|']
for tier in ['no_positive_record','positive_0_50','positive_50_90','positive_90_99','positive_top1']:
 d=root_strata.loc[(root_strata.dimension=='observed_amount_tier')&(root_strata['group']==tier)].set_index('model')
 groups.append(f'| {tier} | {int(d.loc["M2","n"])} | {f(d.loc["M2","mae"])} | {f(d.loc["M3","mae"])} | {f(d.loc["M4","mae"])} | {f(d.loc["M3","total_prediction_ratio"])} |')

report=r'''# 用户价值预测独立时间验证：UCI零售发票金额

2026-11-20 · 第67号。**66号28天MAE相对历史日均基线的优势在新时段复现；两阶段与校准模型没有获得“金额误差和高消费识别同时更好”的统计支持。零金额基线不再在MAE点估计上战胜每个模型，但M3仅略优且差异不确定，不能宣布零值问题已解决。**

本轮仅执行零售实验，不恢复Rotate/Meow外部搜索。数据不是IAA/IAP，客户不是玩家；没有安装前机会、广告成本、多游戏或平台训练数据，不能据此证明Axon/Vector或游戏盈利。

## 1. 数据与时间是否足够

复用Daqing Chen/UCI [Online Retail](https://archive.ics.uci.edu/dataset/352/online+retail)，[DOI 10.24432/C5BW33](https://doi.org/10.24432/C5BW33)，CC BY4，原ZIP SHA256：`f5385cbb54bbebf7196389109c6b0621faab0c304e3702548165e71c84aede8b`。读前/读后相同，未重新下载、未改原件。数据末事件为2011-12-09 12:50，支持末测试时点2011-11-07的28天标签到12-05；不把更晚未成熟的11月窗口纳入。

[67_独立实验协议](67_独立实验协议.md)在拟合前保存，最终协议SHA256绑定于[RUN_START](public-experiments/round67/RUN_START.json)/[RUN_MANIFEST](public-experiments/round67/RUN_MANIFEST.json)。最初PRECHECK只是时间范围检查，协议在执行前删除过一句含糊重复数措辞；正式拟合严格使用最后固定版2000次，不是测试后修订。无超参搜索，无测试数据校准、无测试裁尾。

### 清洗与金额语义

严格复用66号主分析：原541909行，去完全重复5268行；去重后536641行，缺CustomerID135037行另审计并剔除；非正单价2512行、取消单9251行、负金额9253行分开记录。只有有键、时间有效、单价>0、数量>0、非取消记录进入正向金额任务。**标签为本商家文件内正向发票销售额GBP，不是净现金、退款后经济利润或完整消费。**[DATA_QUALITY](public-experiments/round67/DATA_QUALITY_AND_MATURITY.json)

“未来无正向记录”与“数据没有记录”在此源不可辨：不把0写成永久流失/真实停止消费。原数据没有available_at、明确时区或迟到水位，只能确认event-time窗口完整，不能确认真实生产到达及时或全渠道交易完整。特征严格`InvoiceDate<t`，标签`[t,t+28天)`；无未来购买筛选，不给缺键行造身份。

## 2. 独立时间与客户隔离

| 集合 | 时点 | 客户数 | 客户×时点行数 | 最晚28天标签结束 |
|---|---|---:|---:|---|
| 训练 | 01-03—07-25每周一，30时点 | 1840 | 38724 | 08-22 |
| 验证/校准 | 08-29、09-05 | 657 | 1308 | 10-03 |
| 新测试 | 10-10、10-17、10-24、10-31、11-07 | 839 | 4037 | 12-05 |

客户沿用66号固定SHA256分桶，训练/验证/测试交集**0**；ID只用于源内历史聚合和隔离，不作为特征、不输出逐客户原键/预测。测试客户t前自身历史是合法输入，其记录从不参与拟合或校准。前一阶段标签在下一阶段开始前成熟：08-22<08-29、10-03<10-10；66测试最后标签09-26也早于本轮10-10。

**独立的是新时间，不是全新商家或全新人群。**839测试客户中690曾在66号测试出现，149未出现（587新客户时点行）；训练/验证客户仍完全隔离。这个关系在协议中预先说明，不能叫独立数据集复制。[SPLIT_AND_LEAKAGE_CHECKS](public-experiments/round67/SPLIT_AND_LEAKAGE_CHECKS.json)

同客户5周标签可重叠，4037行不是4037独立样本。区间采用客户cluster带走全部时点；只有5个测试周，不声称识别宏观季节变化。

## 3. 模型固定与66参照

| 模型 | 输入和规则 | 训练/校准边界 |
|---|---|---|
| B1_HISTORY_RATE | 历史正额/已观察天数×28 | 无新拟合，与66日均定义一致 |
| B2_ZERO | 金额0、购买概率0 | 完整零值基线 |
| B0_GLOBAL | 67训练金额均值、购买率常数 | 仅训练 |
| FROZEN66_M2 | 66的18特征/原训练期/原超参重建后冻结 | 不用67数据更新；重算66旧MAE/RMSE/排序等与历史结果一致 |
| M0 | 累计金额、发票购买次数 | 67训练 |
| M1 | M0＋7/28/90天金额/频率，共8项 | 67训练 |
| M2 | 66同样18项：加间隔、recency、商品件数、趋势 | 67训练；不能把更多训练历史的效应叫纯架构变化 |
| M3 | 18特征分类预测有正向购买概率p；训练正额样本预测条件均值μ；输出p×μ | 分类器和金额器均仅训练 |
| M4 | M3概率Platt校准＋条件正额乘数 | 仅1308验证行、其中357正额；未读取测试总额定乘子 |

M0—M2及M3金额器使用与66一致的固定浅树Poisson回归超参；分类器同容量/160轮。Poisson是均值损失，不假设货币真的离散Poisson。M3/M4组件数和校准数据更多，比较是预测管线对照，不是严格相同算力的架构净效应。M4正额乘数**1.07429**，Platt斜率**0.81991**、截距**-0.11630**，验证标签结束10-03后才用于10-10预测。[CALIBRATION_FIT](public-experiments/round67/CALIBRATION_FIT.json)

本轮重建的66 M2先复现旧测试MAE225.1191、RMSE1170.7791及修正后的排序指标，才在新时间测试；没有覆盖或再次调66测试。[FROZEN66_RECONSTRUCTION](public-experiments/round67/FROZEN66_RECONSTRUCTION.json)

## 4. 全指标测试结果：不选单项胜者

MAIN_TABLE

金额单位£为GBP。排序沿用66修正：实际目标仅含正额，边界同值使用期望权重；常数模型约10%随机召回/金额捕获，不借固定行序获利。[完整结果及每指标CI](67_模型对照结果.csv)

- 冻结66 M2的MAE269.55，相对历史日均425.05改善**36.58%**；本轮重训M2为264.33，改善**37.81%**。不是把旧22.74%直接拿来当新的效果量，也不能称误差绝对变小：新cohort更重尾、均额更高。
- M3相对本轮M2的MAE仅改善**1.30%**，RMSE改善**2.38%**；召回反降约0.50个百分点，金额捕获也略降。不能称同时改善。
- M4相对M2的MAE差**1.26%**，RMSE点估计改善**2.71%**；总额比从M2的0.755到0.878，但没有全指标胜出。
- 零基线MAE264.31，与M2几乎相同；M3的260.89只略低，M4的267.67反更高。零基线中位误差0，是高零值分布的结果；其总额漏掉100%、排序随机、概率也不佳，不是适合所有目标的业务模型。

### 哪些改善有统计支持

PRIMARY_TABLE

2000次固定seed6701的客户级配对cluster bootstrap，固定模型、校准器和5个测试时点；区间不包含重训/跨季节不确定性。4对比较×MAE/RMSE共8个主要检验，逐项99.375%区间为Bonferroni家族5%控制的近似百分位区间，不把普通95%当确认性结论。[全部配对比较](public-experiments/round67/PAIRED_COMPARISONS.csv)

**可确认：**冻结66 M2与重训67 M2相对日均的MAE优势在这个新时段复现（同时区间分别[17.45%,56.41%]、[17.07%,57.57%]）。**不能确认：**相对日均的RMSE改善（区间跨0）；M3/M4相对直接M2的金额误差优势（MAE/RMSE均跨0）。

探索性结果也必须限定：M3相对零基线MAE改善1.30%的95% CI **[-13.48%,11.82%]**，不足以拒绝零基线；M3相对零基线RMSE改善19.86%的95% CI[12.91%,34.50%]，但不是主要家族结论。M4相对M3的MAE改善为-2.60%，普通95% CI[-3.71%,-1.77%]，说明这次校准有可见代价，不能因总额更近而隐藏。

## 5. 零值与分布变化

训练/验证/测试无正向记录比例为**73.84% / 72.71% / 69.41%**；测试有正向记录率30.59%。66的28天测试零记录为75.90%，本轮已改变，不能按原比例推断永久流失。

均额从训练169.77到验证244.65、测试264.31 GBP，单个客户时点最大44738.82；正额P99约11096.68，明显高于训练4804.49。全体时点top1%承载约41.88%金额。没有删除这些极端值；出现分布漂移并不自动说明季节性是唯一原因，也可能有人群/历史长度变化。

## 6. 长尾：高消费金额仍系统性低估

TIER_TABLE

TAIL_TABLE

“positive_top1”是**正额样本中的top1%**，13行；与全体时点top1%的约41行不是同一集合。模型在这一层均只预测到实际均额的约23%—27%，对未来大额有明显低估；该层少量客户反复出现，不能把13行当13独立客户。它对平方误差的贡献很大，RMSE不稳不是已解决。

按真实金额层分组是事后诊断：条件均值模型按实际尾部看会产生选择效应，低估并不能单凭此证明所有条件特征下都失准。需要额外独立时间/足够正额样本才能检验单独高额概率头是否有增益；本轮未据测试再加tail模型或裁尾。

层间错误并不稳定：零记录层M3平均预测122.74 GBP高于M2的106.47；在90—99%正额层M3误差较低，尾部仍很大。更多尾部金额与更多零值假阳性同时存在，不能只挑一层宣布成功。[分层CSV](67_分层预测误差.csv)

## 7. 校准：总额更近不等于每客户预测更准

PROBABILITY_TABLE

只有B0/B2/M3/M4具有明确概率定义；B1、直接金额模型和冻结M2的购买概率为**N/A**，不从金额硬造概率。B2 logloss只在计算时clip到1e-8避免无穷，真实预测仍0。

M3平均概率27.39%，M4为28.16%，仍低于实际观察购买率30.59%。M4 ECE从0.0320到0.0270更近，但Brier从0.1698到0.1707、logloss从0.5156到0.5179变差；M4对M3的Brier/logloss/ECE差区间均跨0，**没有统计支持的整体概率校准改善**。固定10箱ECE受分箱/样本量影响，不替代proper score。

测试总额低估：冻结66 M2约21.26%、M2约24.47%、M3约16.84%、M4约12.17%。M4绝对总额比例偏差较M3减少4.66个百分点，95% CI[-6.25,5.93]跨0。M0总额比1.008看似最接近，但MAE/RMSE较大，进一步说明总额接近不证明个体排序/预测更好。

[67_预测校准分析.csv](67_预测校准分析.csv)列固定GBP预测区间与概率区间的计数、预测/实际均额/购买率；空箱留空。零实际总额的分层比例无定义，根分层CSV明确N/A，未把内部复用函数的零哨兵当真实比例；该输出语义修正没有改变拟合或任何非零分母指标。[OUTPUT_SEMANTICS](public-experiments/round67/OUTPUT_SEMANTICS.json)

## 8. 高消费排序与每周表现

WEEK_TABLE

冻结66 M2在旧8月Recall@10%为48.38%，新时段为46.72%；本轮M2为49.26%，M3/M4为48.76%。这些点估计显示排序信号延续，但不是相同表现的等效性检验。冻结M2对日均的召回差95% CI约[10.15,24.82]个百分点；本轮M2约[12.90,26.67]，均为探索性次要指标。

M3对M2召回差约-0.50个百分点，95% CI[-3.00,3.17]；金额捕获差约-0.41个百分点，CI[-1.30,1.46]，无新增识别增益证据。各周M3召回约43.59%—50.00%、金额捕获约53.12%—66.29%，不是完全稳定；校准后也未持续更好。

每周冻结66/新M2的MAE都优于日均，但日均在11-07 RMSE6124.84，表明比较基线本身受少数高估影响，不能将总体RMSE点估计巨幅改善写成稳健模型突破。按国家≥50行、以及未在66测试出现的149客户子集也已输出，只是描述性敏感性，没有据此另挑赢家。[分层结果](67_分层预测误差.csv)

## 9. 完整性、验证与研究边界

原数据、00—66报告与66全部结果均保留；模型、协议与起始哈希绑定。边界测试使用小型合成fixture核验t/t+28、未来金额污染不影响历史特征、客户分桶、常数平分与概率指标；**模型证据来自真实公开零售数据，不来自fixture**。[验证](public-experiments/round67/BOUNDARY_AND_PROVENANCE_TESTS.json)

没有发现要求放宽隔离/成熟标准的数据障碍；迟到水位/真实零消费仍未知。本轮未调测试，不执行游戏调查、不采集真实个人标识、不联网或提交生产事件。外部游戏线继续STOP。

## 10. 最终七个答案

1. **66号28天MAE能否复现？**能，在新时间冻结66 M2及重训M2相对历史日均均有家族校正支持；不能外推成对所有基线/指标都优。
2. **两阶段是否更优？**未证实。M3金额误差仅小幅点改善、排序略降，主要比较区间跨0；M4总体校准更近但MAE付出代价。
3. **零值基线仍更好？**不是每项/每模型都如此。M3 MAE点估计略好于0但不显著；零基线仍是强MAE对照，却漏掉全部金额且排序随机。
4. **高价值排序是否稳定？**信号延续、明显强于随机和日均，但逐周波动且新模型无确认增益；不声称跨季节/跨商家稳定。
5. **哪些有统计支持？**主要是冻结/重训M2对日均MAE的时间外复制；其他排序/对零基线RMSE是探索性。两阶段/校准全面改进无支持。
6. **跨游戏迁移值得现在做吗？**目前不具备准入数据。单零售商不能验证跨游戏迁移，不能造game_id；应先有合法多游戏、零收入分母、同口径成熟标签和as-of历史。
7. **对手游买量提供什么？**证明一种独立研究方法：时间/客户隔离、两阶段分解、零/尾/校准多指标、按客户估不确定性和保留负结果。不能证明手游LTV、安装前排序、跨App身份增益、Axon/Vector实现/优势或真实ROAS。

下一步若继续零售机制验证，应在**另一份合法、真正未用过且时间覆盖更长的数据**上预注册季节漂移/高额概率和校准对照，而不是继续优化本次10—11月测试。现有UCI末尾不支持再安排同样长度的更晚28天独立五周测试；不可悄悄缩短窗口或复用已看的日期充当新发现。
'''
report=report.replace('MAIN_TABLE',main_table()).replace('PRIMARY_TABLE',primary_table()).replace('PROBABILITY_TABLE',probability_table())
report=report.replace('TIER_TABLE','\n'.join(groups)).replace('TAIL_TABLE','\n'.join(tails)).replace('WEEK_TABLE','\n'.join(weeks))
write('67_用户价值预测独立时间验证.md',report)

# Machine-readable evidence is independent experiment scope, never target-game delivery/model use.
graphpath=ROOT/'prediction-system/EVIDENCE_GRAPH.json';idxpath=ROOT/'EVIDENCE_INDEX.md'
before=json.loads((OUT/'EVIDENCE_GRAPH.before67.json').read_text(encoding='utf-8-sig'))
current=json.loads(graphpath.read_text(encoding='utf-8-sig'));assert current==before
sources=[]
for ident,rel,kind in [
 ('IV67S_protocol','67_独立实验协议.md','pre-fit preregistration'),('IV67S_raw','public-experiments/audit/retail352.download','public UCI original'),
 ('IV67S_run','public-experiments/round67/RUN_MANIFEST.json','actual fixed independent time retail run'),('IV67S_results','public-experiments/round67/MODEL_RESULTS.csv','actual model results and customer CI'),
 ('IV67S_pairs','public-experiments/round67/PAIRED_COMPARISONS.csv','paired customer bootstrap comparisons'),('IV67S_rebuild','public-experiments/round67/FROZEN66_RECONSTRUCTION.json','frozen original reconstruction checks'),
 ('IV67S_cal','public-experiments/round67/CALIBRATION_FIT.json','validation-only calibration fit'),('IV67S_split','public-experiments/round67/SPLIT_AND_LEAKAGE_CHECKS.json','actual split/maturity audit')]:
 sources.append(dict(id=ident,path=rel,sha256=sha(ROOT/rel),source_date=NOW,url='https://archive.ics.uci.edu/dataset/352/online+retail' if ident=='IV67S_raw' else None,
  evidence_kind=kind,evidence_level='【真实公开零售数据实验】 or pre-fit protocol as stated',production_actual_proven=False,observed_target_game_delivery=False,server_model_training=False,
  scope='Independent retail customer experiment; no game/platform production model or causal revenue fact'))
nodes=[dict(id=i,label=l,stage=s,company='independent public retail research') for i,l,s in [
 ('IV67_inputs','UCI fixed cleaning and customer/date-disjoint historic input','public_data'),('IV67_frozen','Frozen66 M2 faithfully reconstructed','independent_reconstruction'),
 ('IV67_test','Oct10-Nov07 28-day event-time test','independent_future_period'),('IV67_mae','MAE improvement vs history-rate replicated, other superiority limited','scoped_statistical_result'),
 ('IV67_twostage','Two-stage and validation calibration, no confirmed overall superiority','scoped_negative_result'),('IV67_game','Game transfer / Axon Vector / bidding profit UNKNOWN','unsupported_domain_bridge')]]
edges=[]
def edge(ident,a,b,claim,refs,status,missing):
 edges.append(dict(id=ident,source=a,target=b,claim=claim,source_ids=refs,status=status,evidence_level='【真实公开零售数据实验】' if status=='experiment_scoped' else '【无法确认】',
  diagram_style='solid' if status=='experiment_scoped' else 'dashed',edge_type='independent_time_retail_validation',
  permission_conditions='UCI CC BY4; source-scoped grouping only; no personal matching or production calls',reviewed_utc=NOW,
  production_actual_proven=False,observed_target_game_delivery=False,independent_production_audit=False,
  six_layers={'sdk_capability':False,'actual_game_business_callsite':False,'request_construction_code':False,'production_successful_send':False,'server_received':False,'server_model_training':False},
  missing_evidence=missing))
edge('IV67E1','IV67_inputs','IV67_frozen','Exact old-period M2 amount/ranking metrics rebuilt before new-time evaluation',['IV67S_raw','IV67S_rebuild'],'experiment_scoped','Only within same retail dataset, not independently deployed system')
edge('IV67E2','IV67_frozen','IV67_test','Stable customer partitions and mature later labels; 690 old-test and 149 new customers explicitly separated',['IV67S_split','IV67S_protocol'],'experiment_scoped','available_at and full retailer data completeness unknown')
edge('IV67E3','IV67_test','IV67_mae','Frozen and refit M2 improve 28d MAE vs history-rate under 8-comparison familywise intervals; RMSE superiority not confirmed',['IV67S_results','IV67S_pairs'],'experiment_scoped','Unseen retailer/seasons and stronger baselines; fixed-calendar bootstrap not refit uncertainty')
edge('IV67E4','IV67_test','IV67_twostage','M3/M4 do not confirm simultaneous amount and high-consumer ranking improvement; validation calibration may worsen MAE',['IV67S_pairs','IV67S_cal'],'experiment_scoped','Larger independent calibration/long-tail samples and new-data validation')
edge('IV67E5','IV67_mae','IV67_game','Retail temporal validation cannot prove game LTV, transfer, platform consumption or advertising ROAS',['IV67S_raw','IV67S_protocol'],'unknown','Licensed multi-game installation/revenue/as-of features, opportunity prices and authorized platform evidence')
for k,vals in [('nodes',nodes),('edges',edges),('sources',sources)]:
 assert not ({x['id'] for x in vals}&{x['id'] for x in current[k]});current[k].extend(vals)
current['independent_retail_time_round67']=dict(reviewed_utc=NOW,report='67_用户价值预测独立时间验证.md',protocol='67_独立实验协议.md',
 primary_test='2011-10-10 to 2011-11-07; 28d labels mature by 2011-12-05',customer_overlap_between_splits=0,
 frozen66_rebuild_verified=True,retail_mae_replication=True,two_stage_superiority_confirmed=False,game_platform_profit_claims=False,
 new_node_ids=[x['id'] for x in nodes],new_edge_ids=[x['id'] for x in edges],new_source_ids=[x['id'] for x in sources])
graphpath.write_text(json.dumps(current,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
dump('public-experiments/round67/NEW_EVIDENCE_OBJECTS.json',dict(nodes=nodes,edges=edges,sources=sources))

oldindex=(OUT/'EVIDENCE_INDEX.before67.md').read_bytes();assert idxpath.read_bytes()==oldindex
addition='''\n\n<a id="iv67"></a>\n\n## IV67 · UCI独立时间验证（非手游/平台生产证据）\n\n- [67号独立时间报告](67_用户价值预测独立时间验证.md) / [拟合前协议](67_独立实验协议.md)\n- [模型结果与CI](67_模型对照结果.csv) / [金额概率分箱](67_预测校准分析.csv) / [分层周别与新客户](67_分层预测误差.csv)\n- [运行代码](public-experiments/round67/run67.py) / [原66冻结重建](public-experiments/round67/FROZEN66_RECONSTRUCTION.json)\n- [主要及探索性配对比较](public-experiments/round67/PAIRED_COMPARISONS.csv) / [运行哈希](public-experiments/round67/RUN_MANIFEST.json)\n- [边界与历史保留验证](public-experiments/round67/BOUNDARY_AND_PROVENANCE_TESTS.json) / [最终交付校验](public-experiments/round67/VALIDATION67.json)\n\n新事实：10-10—11-07共839客户/4037时点行，原66冻结M2的MAE相对历史日均改善36.58%，重训M2改善37.81%，8项家族比较支持；两阶段/校准相对直接M2的MAE与RMSE优势未确认。零基线MAE仍很强，M3仅略优且CI跨0；高消费排序有信号但尾部低估、总额漂移及校准代价仍在。概率不从直接金额模型伪造。保留旧00—66与原数据，未恢复游戏搜索，未证明Axon/Vector或游戏盈利。\n'''
with idxpath.open('ab') as f:f.write(addition.encode('utf-8'))
experimentindex=ROOT/'public-experiments/EXPERIMENT_INDEX.md'
indexentry='''\n\n## 67：独立未来时间，零售发票，不是手游LTV\n\n- [报告](../67_用户价值预测独立时间验证.md)、[预注册](../67_独立实验协议.md)\n- [复现代码](round67/run67.py)、[实际运行](round67/RUN_MANIFEST.json)、[冻结66重建](round67/FROZEN66_RECONSTRUCTION.json)\n- [结果与CI](../67_模型对照结果.csv)、[配对比较](round67/PAIRED_COMPARISONS.csv)、[校准](../67_预测校准分析.csv)、[分层](../67_分层预测误差.csv)\n- 结论：原M2对历史日均MAE复制；两阶段/校准无确认整体优势；跨游戏与广告ROAS不获准入。外部游戏线保持STOP。\n'''
if experimentindex.exists():
 oldexp=experimentindex.read_bytes();(OUT/'EXPERIMENT_INDEX.before67.md').write_bytes(oldexp)
 with experimentindex.open('ab') as f:f.write(indexentry.encode('utf-8'))
else:
 oldexp=None;experimentindex.write_text('# 公开数据独立实验索引\n\n历史入口：[65号准入](../65_公开扩量证据与模型实验可行性审计.md)、[66号实验](../66_UCI用户未来消费金额预测实验.md)。\n'+indexentry,encoding='utf-8')

# Preserve historic bytes, original graph objects, immutable protocol/run provenance.
errors=[];history=json.loads((OUT/'HISTORY_BEFORE67.json').read_text(encoding='utf-8'))
for rel,s in history.items():
 if rel in ['EVIDENCE_INDEX.md','prediction-system/EVIDENCE_GRAPH.json']:continue
 if sha(ROOT/rel)!=s:errors.append('Historical file changed '+rel)
for k in ['nodes','edges','sources']:
 if current[k][:len(before[k])]!=before[k]:errors.append('Old graph object changed '+k)
 ids=[x['id'] for x in current[k]]
 if len(ids)!=len(set(ids)):errors.append('Duplicate graph ids '+k)
for k,v in before.items():
 if k not in ['nodes','edges','sources'] and current[k]!=v:errors.append('Old metadata changed '+k)
if not idxpath.read_bytes().startswith(oldindex):errors.append('Old index bytes modified')
if sha(ROOT/run['protocol_path'])!=run['protocol_sha256']:errors.append('Protocol changed after fitting')
if sha(OUT/'run67.py')!=run['script_sha256']:errors.append('Run script changed after execution')
deliverables=['67_用户价值预测独立时间验证.md','67_模型对照结果.csv','67_预测校准分析.csv','67_分层预测误差.csv','67_独立实验协议.md']
links=0
for rel in deliverables+['public-experiments/EXPERIMENT_INDEX.md']:
 p=ROOT/rel;txt=p.read_text(encoding='utf-8')
 if '\ufffd' in txt:errors.append('Encoding loss '+rel)
 if p.suffix=='.md':
  for t in re.findall(r'\]\(([^)]+)\)',txt):
   if t.startswith(('https:','http:','#')):continue
   if not (p.parent/t.split('#')[0]).is_file():errors.append('Broken local link '+rel+' '+t)
   links+=1
 else:
  with p.open(encoding='utf-8',newline='') as f:rows=list(csv.DictReader(f))
  if not rows:errors.append('Empty CSV '+rel)
if len(results)!=18:errors.append('Wrong number model result rows')
if len(test)!=9:errors.append('Wrong number fixed models')
if split['pairwise_customer_overlap']!=0 or not split['all_labels_mature']:errors.append('Split/maturity violation')
if not root_strata.loc[zero,'total_prediction_ratio'].isna().all():errors.append('Undefined ratio not blank')
for s in sources:
 if sha(ROOT/s['path'])!=s['sha256']:errors.append('Evidence source hash mismatch '+s['id'])
for e in edges:
 if any(e['six_layers'].values()):errors.append('Experiment promoted to game/platform production '+e['id'])
validation=dict(status='PASS' if not errors else 'FAIL',reviewed_utc=NOW,scope='Independent actual retail experiment, maturity/customer isolation, source hashes and deliverables; not gaming/platform/ROAS validation',
 deliverable_count=5,model_result_rows=len(results),test_models=len(test),bootstrap_customer_replicates=2000,primary_money_comparisons=8,
 test_customers=839,test_customer_time_rows=4037,labels_end='2011-12-05',source_end='2011-12-09',customer_split_overlap=0,
 original_data_hash_preserved=True,old_round66_outputs_and_source_preserved=True,historical_files_hash_verified=len(history)-2,
 historical_report_count=sum(rel.endswith('.md') and '/' not in rel for rel in history),
 frozen66_reconstruction_pass=True,protocol_unchanged_since_fitting=True,model_script_matches_execution_hash=True,
 historical_graph_preserved={k:len(before[k]) for k in ['nodes','edges','sources']},new_graph_objects={k:len(v) for k,v in [('nodes',nodes),('edges',edges),('sources',sources)]},
 local_links_checked=links,zero_denominator_output_cells_marked_na=int(zero.sum()),external_game_searches=0,network_requests=0,
 production_ad_or_attribution_events=0,no_cross_source_person_identity_matching=True,errors=errors,
 final_artifact_sha256={rel:sha(ROOT/rel) for rel in deliverables})
dump('public-experiments/round67/VALIDATION67.json',validation)
print(json.dumps({k:v for k,v in validation.items() if k!='final_artifact_sha256'},ensure_ascii=True,indent=2))
if errors:raise SystemExit(1)
