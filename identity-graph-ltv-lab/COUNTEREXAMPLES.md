# 十项反证实验

全部仅使用合成数据。工程断言是否通过，与模型误差是否改善分开评价。

### C1 图谱特征随机置换

每个切分内置换可用历史值，保留覆盖位。

限制：不能保证每个种子都恶化；统计波动照报。

D30全部世界均值：`[{'world': 'history_informative', 'MAE': 62.75334407244103, 'RMSE': 123.07411888554323, 'graph_coverage': 0.92}, {'world': 'no_graph_information', 'MAE': 22.978318718095025, 'RMSE': 40.66095591228174, 'graph_coverage': 0.92}]`。

### C2 错误身份合并

20%错误值替换UNSAFE与已知错误拒绝GUARDED；另有实际图谱错误断言探针。

限制：无额外真值无法识别有效格式的错误关系；GUARDED不表示自动发现。

D30全部世界均值：`[{'world': 'history_informative', 'MAE': 46.423334511918554, 'RMSE': 94.38606289596744, 'graph_coverage': 0.92}, {'world': 'no_graph_information', 'MAE': 22.752299111907014, 'RMSE': 39.95366176883901, 'graph_coverage': 0.92}]`。

### C3 关系置信度变化

0.2/0.6/0.99候选均不激活；全拒绝模型与M1等价。

限制：未校准score不是匹配概率；不主张概率匹配增益。

D30全部世界均值：`[{'world': 'history_informative', 'MAE': 65.7846964123789, 'RMSE': 127.40338146098725, 'graph_coverage': 0.0}, {'world': 'no_graph_information', 'MAE': 22.623447875729376, 'RMSE': 40.05637406450098, 'graph_coverage': 0.0}]`。

### C4 关系撤销

实际MVP撤销使旧bundle失效、新查询不可用；全拒绝输入回退。

限制：生命周期探针与整批输入消融分开记录。

D30全部世界均值：`[{'world': 'history_informative', 'MAE': 65.7846964123789, 'RMSE': 127.40338146098725, 'graph_coverage': 0.0}, {'world': 'no_graph_information', 'MAE': 22.623447875729376, 'RMSE': 40.05637406450098, 'graph_coverage': 0.0}]`。

### C5 删除后特征失效

实际MVP删除传播与旧bundle拒绝；全删除输入回退。

限制：保留的合成审计快照不是真实数据删除实现。

D30全部世界均值：`[{'world': 'history_informative', 'MAE': 65.7846964123789, 'RMSE': 127.40338146098725, 'graph_coverage': 0.0}, {'world': 'no_graph_information', 'MAE': 22.623447875729376, 'RMSE': 40.05637406450098, 'graph_coverage': 0.0}]`。

### C6 时间泄漏注入及拦截

未来标签注入在设计矩阵前拒绝；晚可用探针拒绝。

限制：未训练故意泄漏模型；不存在泄漏收益数字。

### C7 标签成熟不足

训练标签延后到验证开始后，准入必须STOP。

限制：STOP不是训练失败，不填造模型结果。

### C8 图谱覆盖下降

独立随机mask到原可用样本的50%/20%，保留缺失标志。

限制：不是总体覆盖强制等于20%；重训而非固定模型漂移。

D30全部世界均值：`[{'world': 'history_informative', 'MAE': 63.95923206881185, 'RMSE': 124.2980784058601, 'graph_coverage': 0.18222222222222223}, {'world': 'no_graph_information', 'MAE': 22.74128866113927, 'RMSE': 40.70067710159788, 'graph_coverage': 0.18222222222222223}]`。

### C9 共享设备歧义

两个账号的原始设备汇总存在；适配器拒绝账号级解释；UNSAFE另示。

限制：不能只凭设备关系认定自然人。

D30全部世界均值：`[{'world': 'history_informative', 'MAE': 36.702092403496586, 'RMSE': 80.19875067527241, 'graph_coverage': 1.0}, {'world': 'no_graph_information', 'MAE': 22.59868102585979, 'RMSE': 40.18538157719183, 'graph_coverage': 1.0}]`。

### C10 无图谱真实增益世界

响应生成系数中历史latent项严格为0；同协议全流程。

限制：有限样本差值不保证0；不把偶然负差认作真实增益。

D30全部世界均值：`[{'world': 'history_informative', 'MAE': 39.947605176152834, 'RMSE': 85.13048645052088, 'graph_coverage': 0.92}, {'world': 'no_graph_information', 'MAE': 22.50226272913137, 'RMSE': 39.1925467589778, 'graph_coverage': 0.92}]`。

实际MVP探针17项，通过17项；全图谱缺失回退90组，均检验预测与M1的最大绝对差≤1e-8。原始结果位于[当前运行](results/run-002/SUMMARY.json)、[探针](results/run-002/ENGINE_PROBES.json)、[反证汇总](results/run-002/TEN_COUNTEREXAMPLES.json)。
