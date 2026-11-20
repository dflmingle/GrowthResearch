"""Descriptive reporting only; never fits or selects a model."""
import sys
sys.dont_write_bytecode=True
import csv,collections,statistics
from lab.common import ROOT,load,save,csvsave

def read(path):
    with path.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))

def main():
    run=ROOT/(ROOT/'LATEST_RUN.txt').read_text().strip()
    rows=read(run/'MODEL_METRICS.csv');summary=load(run/'SUMMARY.json')
    grouped=collections.defaultdict(list)
    for r in rows:grouped[(r['world'],r['horizon'],r['variant'])].append(r)
    means=[]
    metrics=['MAE','RMSE','median_AE','total_prediction_ratio','Recall_at_10pct','Top10pct_value_capture','graph_coverage','observed_zero_fraction']
    for (world,h,variant),rs in grouped.items():
        row=dict(world=world,horizon=h,variant=variant,seeds=len(rs))
        for metric in metrics:
            vals=[float(r[metric]) for r in rs if r[metric]!='']
            row[metric+'_mean']=statistics.mean(vals) if vals else None
            row[metric+'_seed_std']=statistics.stdev(vals) if len(vals)>1 else None
        means.append(row)
    csvsave(run/'AGGREGATED_METRICS.csv',means)
    lines=['# M0/M1/M2合成实验对照报告','',
        '仅验证预注册生成器下的工程与实验方法。金额是生成器定义的合成USD单位，不是实际收入。以下均值保留所有5个种子；每个世界测试450个独立合成安装，D1/D7/D30共享安装。','',
        '|世界|窗口|模型|MAE|RMSE|预测/实际总额|Recall@10%|Top10%金额捕获|图谱覆盖|',
        '|---|---|---|---:|---:|---:|---:|---:|---:|']
    for r in means:
        if r['variant'] in ['M0','M1','M2']:
            lines.append('|'+ '|'.join([r['world'],'D'+r['horizon'],r['variant']]+[f"{r[m+'_mean']:.4f}" for m in ['MAE','RMSE','total_prediction_ratio','Recall_at_10pct','Top10pct_value_capture','graph_coverage']])+'|')
    lines+=['','## 配对不确定性','',
        'M2−M1，负误差差值表示M2较小；500次分层配对Bootstrap，先抽种子，再在该种子内抽独立安装。仅条件于生成机制与这5个种子；不代表真实商业置信区间。两个D30 MAE对照是预注册主指标，其余描述性，不做择优显著性结论。','',
        '|世界|窗口|指标|平均差值|95%区间|','|---|---|---|---:|---|']
    for r in read(run/'PAIRED_INTERVALS.csv'):
        lines.append(f"|{r['world']}|D{r['horizon']}|{r['metric']}|{float(r['mean_delta']):.4f}|[{float(r['ci95_low']):.4f}, {float(r['ci95_high']):.4f}]|")
    lines+=['','## 解释边界','',
        '有信息世界明确把独立潜变量同时写入历史金额与未来金额，检验框架是否能发现已植入的信息；无信息世界将该通路系数固定为0，任何有限样本差值都必须原样保留。两种世界不混合训练或统计。',
        '相同样本、标签、时间切分与4次alpha试验；中位数填补、标准化、反变换smearing只用训练集。验证集选alpha，测试集仅评价。M2多两个输入列；这里没有容量完全相等的非线性模型消融，不能把一切差异都归因于图结构。',
        '图谱特征是已有GraphFeatureService按设备查询的观察历史净金额，不是新增训练玩家、更不是闭源身份图谱。跨应用历史App与目标App是本地合成对象；多账号共享设备被任务适用性门控拒绝。账号从未自动升格为自然人。',
        '覆盖下降、置换与错误合并情景分别重新训练并保持同一测试样本；不是固定已部署模型遇到分布漂移的效果估计。零值表示有限合成账本内无净金额，不能外推真实缺失、流失或完整LTV。',
        'D1/D7/D30是安装起有限窗口净现金流，预测发生在安装6小时；生成器第一笔购买在12小时，故所有预测标签金额在预测后发生。退款按发生日期计入，窗口后退款不追溯改写窗口。未模拟IAA广告展示收入。',
        '校准详情：[CALIBRATION.csv](results/'+run.name+'/CALIBRATION.csv)；国家、共享设备、覆盖分组：[GROUPED_ERRORS.csv](results/'+run.name+'/GROUPED_ERRORS.csv)。零购买比例、全部种子标准差、12种变体均见[聚合指标](results/'+run.name+'/AGGREGATED_METRICS.csv)。',
        '保持C_graph.Axon=UNKNOWN、C_graph.Vector=UNKNOWN、D=UNKNOWN；原生产取证STOP。']
    (ROOT/'MODEL_COMPARISON.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    checks=[]
    definitions=[
      ('C1','图谱特征随机置换','每个切分内置换可用历史值，保留覆盖位','C1_permuted_graph','不能保证每个种子都恶化；统计波动照报'),
      ('C2','错误身份合并','20%错误值替换UNSAFE与已知错误拒绝GUARDED；另有实际图谱错误断言探针','C2_wrong_merge_UNSAFE','无额外真值无法识别有效格式的错误关系；GUARDED不表示自动发现'),
      ('C3','关系置信度变化','0.2/0.6/0.99候选均不激活；全拒绝模型与M1等价','C3_candidates_rejected','未校准score不是匹配概率；不主张概率匹配增益'),
      ('C4','关系撤销','实际MVP撤销使旧bundle失效、新查询不可用；全拒绝输入回退','C4_relation_revoked','生命周期探针与整批输入消融分开记录'),
      ('C5','删除后特征失效','实际MVP删除传播与旧bundle拒绝；全删除输入回退','C5_deleted_history','保留的合成审计快照不是真实数据删除实现'),
      ('C6','时间泄漏注入及拦截','未来标签注入在设计矩阵前拒绝；晚可用探针拒绝',None,'未训练故意泄漏模型；不存在泄漏收益数字'),
      ('C7','标签成熟不足','训练标签延后到验证开始后，准入必须STOP',None,'STOP不是训练失败，不填造模型结果'),
      ('C8','图谱覆盖下降','独立随机mask到原可用样本的50%/20%，保留缺失标志','C8_coverage20','不是总体覆盖强制等于20%；重训而非固定模型漂移'),
      ('C9','共享设备歧义','两个账号的原始设备汇总存在；适配器拒绝账号级解释；UNSAFE另示','C9_shared_device_UNSAFE','不能只凭设备关系认定自然人'),
      ('C10','无图谱真实增益世界','响应生成系数中历史latent项严格为0；同协议全流程','M2','有限样本差值不保证0；不把偶然负差认作真实增益')]
    probes=load(run/'ENGINE_PROBES.json');controls=load(run/'CONTROL_EQUIVALENCE.json')
    for cid,name,method,variant,limit in definitions:
        entry=dict(id=cid,name=name,method=method,status='EXECUTED',limitation=limit,evidence='ENGINE_PROBES.json / CONTROL_EQUIVALENCE.json / data/',variant=variant)
        if variant:
            rs=[r for r in means if r['horizon']=='30' and r['variant']==variant]
            entry['D30_results']=[dict(world=r['world'],MAE=r['MAE_mean'],RMSE=r['RMSE_mean'],graph_coverage=r['graph_coverage_mean']) for r in rs]
        checks.append(entry)
    save(run/'TEN_COUNTEREXAMPLES.json',checks)
    (ROOT/'COUNTEREXAMPLES.md').write_text('# 十项反证实验\n\n全部仅使用合成数据。工程断言是否通过，与模型误差是否改善分开评价。\n\n'+
        '\n\n'.join('### '+c['id']+' '+c['name']+'\n\n'+c['method']+'。\n\n限制：'+c['limitation']+'。'+
            ('\n\nD30全部世界均值：`'+str(c.get('D30_results'))+'`。' if c.get('D30_results') else '') for c in checks)+
        f'\n\n实际MVP探针{len(probes)}项，通过{sum(p["passed"] for p in probes)}项；全图谱缺失回退{len(controls)}组，均检验预测与M1的最大绝对差≤1e-8。原始结果位于[当前运行](results/{run.name}/SUMMARY.json)、[探针](results/{run.name}/ENGINE_PROBES.json)、[反证汇总](results/{run.name}/TEN_COUNTEREXAMPLES.json)。\n',encoding='utf-8')
    print(summary)

if __name__=='__main__':main()
