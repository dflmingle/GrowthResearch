from pathlib import Path
import json
import pandas as pd

R=Path(__file__).resolve().parent.parent;D=R/'blackbox75';t=pd.read_csv(D/'results/DESIGN_SUMMARY.csv')
run=json.loads((D/'results/RUN.json').read_text('utf-8'))
lines=['# 75号：合成实验设计验证','',
 '2026-11-20。**仅本地合成设计验证，不是Axon/Vector调用、真实身份图谱、广告效果、LTV或买量收益实验。** 没有新真实数据，没有训练预测模型；执行前冻结协议、完整参数和种子，全部场景保留。','',
 '## 范围与复现','',
 f"seed=750031；每情景300次独立重复，80设备块/设备对块，每单元24机会。S1十二场景、S2七场景，共{run['replicates_rows']}条重复结果、19行摘要；第0重复保存全部{run['raw_observation_rows']}条逐机会外部观测，所有重复保存效应/区间/p值。另1536行精确等价世界观测。",'',
 '原始逐机会记录只保存每场景第0重复，其余重复的逐机会记录由固定代码/随机种子重建，不声称已保存所有重复的原始事件。生成器真值放TRUTH，外部观察放OBSERVATIONS；分析结果带mechanism_truth是合成解释元数据，现实黑盒不会提供它。', '',
 '[预注册](blackbox75/PREREGISTRATION.md)、[参数](blackbox75/CONFIG.json)、[代码](blackbox75/simulate.py)、[完整重复结果](blackbox75/results/REPLICATE_RESULTS.csv)、[19场景摘要](blackbox75/results/DESIGN_SUMMARY.csv)、[运行哈希](blackbox75/results/RUN.json)。', '',
 '## S1：同设备源历史设计','',
 '结局是每次合格模拟机会出现目标类别的比例，no-fill计0并单独报告fill。S1主要p值按设备块sign-flip随机化，199次；区间另用块差值t近似，二者不混称精确区间。逐机会IID z检验作为刻意错误对照；其拒绝率不是有效功效。','',
 '| 情景 | 平均比例差 | 拒绝率 | 拒绝率95% Monte Carlo CI | 错误IID检验拒绝率 |','|---|---|---|---|---|']
for _,x in t[t.module=='S1'].iterrows():
 lines.append(f"| {x.scenario} | {x.mean_estimate:+.4f} | {x.reject_rate:.3f} | [{x.reject_rate_mc_ci_low:.3f},{x.reject_rate_mc_ci_high:.3f}] | {x.naive_iid_reject_rate:.3f} |")
lines+=['',
 'H0随机分配下块检验假阳性约4%，错误逐机会检验约21%；同一设备机会相关，重复请求不能替代独立设备。H3冻结零通路结果相近，不能因均值微差判别训练来源。', '',
 '在无个体跨App通路的H0中，只给处理臂增加库存偏移或减少既往频次可用性，块检验也能100%“检出变化”。这些情景的处理与干扰变量共变，设计无效；检验检测到真实响应差，不是统计错误，却会造成**身份归因假阳性**。模拟称sequential/prior-frequency是结构化臂间偏移，不是实际纵向广告日志；repair场景取消该偏移，不代表现实已能观测/修复所有混杂。', '',
 'H1低库存下只有25%重复检出，而正常场景接近100%；未显著可能是外部选择遮蔽。频控压低响应差；漂移场景令当前历史系数反号，显著差也可能方向相反。漂移是生成器明确切换历史关系，不是从真实日期估计的漂移。', '',
 '20% false_route指20%历史路由被独立随机0/1供体替换，同值时观察值可能不变；它不是BPID的FP/(TP+FP)，也不是最终错误自然人匹配比例。隐私gate关闭直接令历史系数为0，架构潜在通路与实际允许使用分开。','',
 '## S2：跨设备历史×账号链接','',
 '每块四独立目标单元，源历史与链接随机化。主要效应为两链接层的历史差中差；采用块级交互t近似双侧检验，不冒称Fisher精确随机化。账号登录状态的主效应是预设当前上下文因素，**没有跨设备历史也能改变响应**。','',
 '| 情景 | 平均交互比例差 | 交互拒绝率 | 95% Monte Carlo CI | 账号主效应拒绝率 |','|---|---|---|---|---|']
for _,x in t[t.module=='S2'].iterrows():
 lines.append(f"| {x.scenario} | {x.mean_estimate:+.4f} | {x.reject_rate:.3f} | [{x.reject_rate_mc_ci_low:.3f},{x.reject_rate_mc_ci_high:.3f}] | {x.account_main_effect_reject_rate:.3f} |")
lines+=['',
 'H0没有跨设备历史通路，账号主效应仍在98%重复中显著；交互拒绝率约6.7%，其Monte Carlo CI包含5%。H2正常场景交互检出97%，20%路由替换约81.3%，不能把这些模拟检测率当真实平台功效。', '',
 'H3_target_context_leak没有身份历史存储，却让源处理经未受控当前上下文与账号资格联动，96.7%重复也检出交互。这违反隔离/排除假设；说明**统计交互不是身份解析指纹**。所有四单元均值和来源路径需要额外观察。','',
 '## 逐行完全相同的竞争世界','',
 '| 两世界 | 相同外部观察 | 区分它们所需信息 |','|---|---|---|',
 '| H0与H3同一冻结映射 | 512条类别、广告主代理、fill逐行完全相同；频数可由相同行推导 | 训练来源/参数血缘，而非更多广告 |',
 '| H1源历史lookup与H3未观测上下文中介 | 512条外部结果完全相同 | 目标上下文/聚合冻结及源→目标路径隔离审计；若真正满足这些限制，随机扰动可排除此特定中介反例 |',
 '| H2账号历史特征与直接账号受众规则 | 512条外部结果完全相同 | 指定接收产品、特征实际读取与受众/选择审计 |','',
 '这些是共享相同输出概率和外部随机数的构造性反例，不是两个样本“p>.05”。它们不声称H3在所有干预下都与H1等价，而是明确在缺少相应可观察/排除约束的实验集合下不可识别。', '',
 '[等价外部观测](blackbox75/results/OBSERVATIONS/EQUIVALENT_WORLDS.csv)与[单列内部真值](blackbox75/results/TRUTH/EQUIVALENT_WORLDS.json)分开。另[VALUE_SCALE_COUNTEREXAMPLE](blackbox75/results/VALUE_SCALE_COUNTEREXAMPLE.json)令分数B=7A+3而赢家全部相同：仅见广告赢家不能恢复绝对价值尺度。此为研究者构造，不是厂商分数/报价公式。','',
 '## 可以与不能得出的结论','',
 '可以：验证簇级统计比逐机会伪独立更合理；说明库存/频控/目标上下文干扰如何造成身份误判；展示通路关闭、误路由、弱库存和漂移的漏检/反向结果；构造不具可识别性的严格反例。', '',
 '不能：这些不估计Axon/Vector使用图谱的概率，不是现实设备匹配准确率、游戏价值或平台相对优势。没有自然人实体、IAA/IAP、D7/D28真实标签、真实成本或机会日志。此模拟的beta、N、库存和干扰强度全部由研究者指定。', '',
 '拒绝率CI为300次Monte Carlo重复的Wilson区间，不是现实平台效应CI；单重复的块t区间只针对该生成机制。弱效应漏检、无效设计与负方向完整报告，不选择好看场景，不据结果重选种子。','',
 '12项本地授权/解释门禁测试见[CHECKS](blackbox75/ADMISSION_AND_INTERPRETATION_CHECKS.json)，假设授权用例不代表真实获权。全套文件/历史/统计一致性见[VALIDATION](blackbox75/VALIDATION.json)。下一步是本地mock可观测性先导及L2授权，详见[最小方案](75_下一步最小可执行方案.md)。','']
(R/'75_合成实验设计验证.md').write_text('\n'.join(lines),encoding='utf-8')
print(json.dumps(dict(report_written=True,scenarios=len(t))))
