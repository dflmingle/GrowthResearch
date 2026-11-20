from pathlib import Path
import json,csv,statistics
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

R=Path(__file__).resolve().parent/'output'
data=json.loads((R/'results.json').read_text());rows=data['rows']
metrics=['top10_value_recall','top10_revenue_capture','ltv_predicted_to_actual','ltv_decile_calibration_error',
         'decision_score_top10_recall','decision_score_top10_revenue_capture',
         'install_auc','install_brier','realized_D28_ROAS','expected_D28_ROAS','budget_utilization','spend_usd']
summary=[]
for shape in data['shapes']:
 for arm in sorted(set(x['arm'] for x in rows)):
  a=[x for x in rows if x['shape']==shape and x['arm']==arm]
  out=dict(shape=shape,arm=arm,seeds=len(a),kind=a[0]['kind'])
  for m in metrics:
   vals=[x[m] for x in a if x[m] is not None]
   out[m]=dict(mean=float(np.mean(vals)),min=float(np.min(vals)),max=float(np.max(vals)))
  summary.append(out)
paired=[]
for shape in data['shapes']:
 for before,after in [('install_only','context_ltv'),('context_ltv','context_behavior'),
                       ('context_behavior','context_behavior_identity'),('context_ltv','context_identity'),
                       ('context_behavior_identity','identity_removed'),('context_behavior_identity','wrong_links_30pct'),
                       ('context_behavior_identity','privacy_limited')]:
  d=dict(shape=shape,before=before,after=after)
  for m in ['top10_value_recall','realized_D28_ROAS','ltv_decile_calibration_error','budget_utilization']:
   changes=[];relative=[]
   for seed in data['seeds']:
    a=next(x for x in rows if x['shape']==shape and x['seed']==seed and x['arm']==before)
    b=next(x for x in rows if x['shape']==shape and x['seed']==seed and x['arm']==after)
    changes.append(b[m]-a[m]);relative.append(b[m]/a[m]-1 if a[m] else None)
   d[m]=dict(mean_delta=float(np.mean(changes)),seed_min_delta=float(min(changes)),seed_max_delta=float(max(changes)),
             mean_relative_change=float(np.mean([x for x in relative if x is not None])))
  paired.append(d)
(R/'summary.json').write_text(json.dumps(dict(summary=summary,paired=paired,scope='Three seeds; empirical ranges, NOT confidence intervals or vendor uplift'),indent=2))
flat=[]
for x in summary:
 flat.append({**{k:x[k] for k in ['shape','arm','seeds','kind']},**{m:x[m]['mean'] for m in metrics}})
with (R/'summary.csv').open('w',newline='',encoding='utf-8-sig') as f:
 w=csv.DictWriter(f,fieldnames=list(flat[0]));w.writeheader();w.writerows(flat)
md='# 合成实验汇总（非Axon/Vector表现）\n\n各指标为3个seed的均值；完整seed范围与配对变化在summary.json。召回以实际出价分数pInstall×预测LTV排名，评价对象为全部留出集已安装样本。install_only的条件LTV是常数，其条件LTV排名仅为行序打破平局，不具识别意义；不将该指标用于模型优势比较。\n\n| 分布 | 模型/场景 | 出价分数Top10%召回 | 价值预测/实际 | 分箱校准误差 | 实现D28 ROAS | 预算利用 |\n|---|---|---:|---:|---:|---:|---:|\n'
for x in summary:
 md+=f'| {x["shape"]} | {x["arm"]} | {x["decision_score_top10_recall"]["mean"]:.2%} | {x["ltv_predicted_to_actual"]["mean"]:.3f} | {x["ltv_decile_calibration_error"]["mean"]:.2%} | {x["realized_D28_ROAS"]["mean"]:.3f} | {x["budget_utilization"]["mean"]:.2%} |\n'
(R/'SUMMARY.md').write_text(md,encoding='utf-8')

arms=['install_only','context_ltv','context_behavior','context_behavior_identity']
labels=['Install-only','Context LTV','+Behavior','+Linked history']
fig,axs=plt.subplots(1,3,figsize=(13,4),layout='constrained')
for ax,shape in zip(axs,data['shapes']):
 a=[next(x for x in summary if x['shape']==shape and x['arm']==arm) for arm in arms]
 means=np.array([x['decision_score_top10_recall']['mean'] for x in a])*100
 lows=np.array([x['decision_score_top10_recall']['min'] for x in a])*100
 highs=np.array([x['decision_score_top10_recall']['max'] for x in a])*100
 ax.bar(np.arange(4),means,color=['#909090','#477bb5','#39a180','#d59935'])
 ax.errorbar(np.arange(4),means,yerr=[means-lows,highs-means],fmt='none',ecolor='black',capsize=3)
 ax.set_title(shape);ax.set_xticks(range(4),labels,rotation=24,ha='right');ax.set_ylim(0,85);ax.grid(axis='y',alpha=.15)
axs[0].set_ylabel('Top-value recall ranked by pInstall x LTV (%)')
fig.suptitle('Synthetic feature ablation only - three-seed ranges, NOT vendor lift',fontsize=12)
fig.savefig(R/'recall_ablation.png',dpi=170)
fig,axs=plt.subplots(1,3,figsize=(13,4),layout='constrained')
for ax,shape in zip(axs,data['shapes']):
 a=[next(x for x in summary if x['shape']==shape and x['arm']==arm) for arm in arms]
 means=np.array([x['realized_D28_ROAS']['mean'] for x in a]);lows=np.array([x['realized_D28_ROAS']['min'] for x in a]);highs=np.array([x['realized_D28_ROAS']['max'] for x in a])
 ax.bar(np.arange(4),means,color=['#909090','#477bb5','#39a180','#d59935'])
 ax.errorbar(np.arange(4),means,yerr=[means-lows,highs-means],fmt='none',ecolor='black',capsize=3)
 ax.set_title(shape);ax.set_xticks(range(4),labels,rotation=24,ha='right');ax.grid(axis='y',alpha=.15)
axs[0].set_ylabel('Synthetic realized D28 ROAS (revenue/spend)')
fig.suptitle('Synthetic economics - common inventory, budget and auction; NOT vendor ROAS',fontsize=12)
fig.savefig(R/'roas_ablation.png',dpi=170)
print(md)
print('\nPAIRED IDENTITY GAIN\n')
for x in paired:
 if x['before']=='context_behavior' and x['after']=='context_behavior_identity':print(json.dumps(x,indent=2))
