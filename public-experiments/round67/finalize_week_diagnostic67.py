from pathlib import Path
from datetime import datetime, timezone
import json, hashlib, re, csv
import pandas as pd
ROOT=Path(r'D:\GrowthResearch'); OUT=ROOT/'public-experiments/round67'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
now=datetime.now(timezone.utc).isoformat()
report=ROOT/'67_用户价值预测独立时间验证.md'
d=pd.read_csv(OUT/'WEEK_BY_TIER_DIAGNOSTIC.csv')
m=json.loads((OUT/'WEEK_TIER_DIAGNOSTIC_MANIFEST.json').read_text())
assert m['all_9_predictors_match_original_67_test_metrics'] and len(d)==225
lines=['### 周别与尾层交叉诊断（预定描述性分析）','','| 测试周 | 正额top1%行数 | M2尾层预测/实际 | M3尾层预测/实际 | M4尾层预测/实际 |','|---|---:|---:|---:|---:|']
for week,g in d[d.observed_tier.eq('positive_top1')].groupby('week'):
    g=g.set_index('model'); lines.append(f"| {week} | {int(g.loc['M2','n'])} | {g.loc['M2','total_prediction_ratio']:.3f} | {g.loc['M3','total_prediction_ratio']:.3f} | {g.loc['M4','total_prediction_ratio']:.3f} |")
lines.extend(['','使用全测试固定的正额分位数边界，逐周仅有2—3名尾层客户；五周合计仍只有3名不同客户，不能据此检验跨周显著性。M2尾层预测/实际为0.084—0.348，M3为0.111—0.436；M3在11-07反而低于M2，不能称尾部误差稳定改善。零记录层五周M3的MAE均高于M2，M4又均高于M3。这里的零记录仍仅指本数据源内未观察到正向购买。','','[完整周×消费层225行结果](public-experiments/round67/WEEK_BY_TIER_DIAGNOSTIC.csv)及[诊断清单](public-experiments/round67/WEEK_TIER_DIAGNOSTIC_MANIFEST.json)。首轮没有保存逐客户预测，因此只以完全相同固定代码重建9个预测器，并逐一确认原测试全部金额/排序指标一致；原运行结果未覆盖，未调参或增加确认性检验，不输出逐客户标识或预测。',''])
text=report.read_text(encoding='utf-8'); marker='## 9. 完整性、验证与研究边界'
assert '### 周别与尾层交叉诊断' not in text and marker in text
report.write_text(text.replace(marker,'\n'.join(lines)+'\n'+marker),encoding='utf-8')
for rel,addition in [('EVIDENCE_INDEX.md','\n\nIV67补充核验：预定周×消费层描述诊断已补齐，9个固定预测器全部重建一致；[225行交叉诊断](public-experiments/round67/WEEK_BY_TIER_DIAGNOSTIC.csv)、[重建边界](public-experiments/round67/WEEK_TIER_DIAGNOSTIC_MANIFEST.json)。每周尾层仅2—3客户、总体仅3不同客户，未获得稳定长尾改善或新增确认性结论。\n'),('public-experiments/EXPERIMENT_INDEX.md','\n\n67号补充：[周×消费层描述诊断](round67/WEEK_BY_TIER_DIAGNOSTIC.csv)、[固定重建一致性](round67/WEEK_TIER_DIAGNOSTIC_MANIFEST.json)。未调参，原运行结果保留；尾层仍不稳定，未新增模型优势结论。\n')]:
    with (ROOT/rel).open('a',encoding='utf-8') as f: f.write(addition)
graphpath=ROOT/'prediction-system/EVIDENCE_GRAPH.json'; graph=json.loads(graphpath.read_text(encoding='utf-8-sig'))
source={'id':'IV67S_week_tier','path':'public-experiments/round67/WEEK_BY_TIER_DIAGNOSTIC.csv','sha256':sha(OUT/'WEEK_BY_TIER_DIAGNOSTIC.csv'),'source_date':now,'evidence_kind':'Preregistered descriptive week by observed consumption tier, exact fixed predictor reconstruction','evidence_level':'【真实公开零售数据实验】','production_actual_proven':False,'observed_target_game_delivery':False,'server_model_training':False,'scope':'225 aggregate rows; only 3 distinct positive-top1 customers across five weeks; not new model selection or confirmatory evidence','permission_conditions':'UCI CC BY 4.0; source-local grouping only; no individual identifiers exported','manifest_path':'public-experiments/round67/WEEK_TIER_DIAGNOSTIC_MANIFEST.json','manifest_sha256':sha(OUT/'WEEK_TIER_DIAGNOSTIC_MANIFEST.json')}
assert not any(s['id']==source['id'] for s in graph['sources']); graph['sources'].append(source)
graph['independent_retail_time_round67']['new_source_ids'].append(source['id'])
graph['independent_retail_time_round67']['week_tier_diagnostic']={'source_id':source['id'],'all_original_metrics_reproduced':True,'additional_confirmatory_tests':0,'model_tuning':False,'distinct_tail_customers':3}
graphpath.write_text(json.dumps(graph,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
objects=json.loads((OUT/'NEW_EVIDENCE_OBJECTS.json').read_text(encoding='utf-8')); objects['sources'].append(source)
(OUT/'NEW_EVIDENCE_OBJECTS.json').write_text(json.dumps(objects,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
# Final verification without refitting, rewriting historical evidence, or touching preregistration.
v=json.loads((OUT/'VALIDATION67.json').read_text(encoding='utf-8')); errors=[]
history=json.loads((OUT/'HISTORY_BEFORE67.json').read_text(encoding='utf-8'))
for rel,h in history.items():
    if rel in ['EVIDENCE_INDEX.md','prediction-system/EVIDENCE_GRAPH.json']: continue
    if sha(ROOT/rel)!=h: errors.append('Historical byte hash changed: '+rel)
before=json.loads((OUT/'EVIDENCE_GRAPH.before67.json').read_text(encoding='utf-8-sig'))
for key in ['nodes','edges','sources']:
    if graph[key][:len(before[key])]!=before[key]: errors.append('Historical graph changed: '+key)
    ids=[x['id'] for x in graph[key]]
    if len(ids)!=len(set(ids)): errors.append('Duplicate ids: '+key)
for key,value in before.items():
    if key not in ['nodes','edges','sources'] and graph.get(key)!=value: errors.append('Historical metadata changed: '+key)
if not (ROOT/'EVIDENCE_INDEX.md').read_bytes().startswith((OUT/'EVIDENCE_INDEX.before67.md').read_bytes()): errors.append('Historical index changed')
run=json.loads((OUT/'RUN_MANIFEST.json').read_text(encoding='utf-8'))
for path,h in [(ROOT/run['protocol_path'],run['protocol_sha256']),(OUT/'run67.py',run['script_sha256']),(ROOT/'public-experiments/audit/retail352.download',run['raw_sha256'])]:
    if sha(path)!=h: errors.append('Provenance mismatch: '+str(path))
links=0
for rel in list(v['final_artifact_sha256'])+['public-experiments/EXPERIMENT_INDEX.md']:
    p=ROOT/rel; content=p.read_text(encoding='utf-8')
    if '\ufffd' in content: errors.append('Encoding damage '+rel)
    if p.suffix=='.md':
        for target in re.findall(r'\]\(([^)]+)\)',content):
            if target.startswith(('https:','http:','#')): continue
            if not (p.parent/target.split('#')[0]).is_file(): errors.append('Broken link '+target)
            links+=1
for s in graph['sources']:
    if s['id'].startswith('IV67S_') and sha(ROOT/s['path'])!=s['sha256']: errors.append('Source hash mismatch '+s['id'])
assert d.loc[d.observed_tier.eq('no_positive_record'),'total_prediction_ratio'].isna().all()
v.update(status='PASS' if not errors else 'FAIL',reviewed_utc=now,local_links_checked=links,new_graph_objects={k:len(objects[k]) for k in ['nodes','edges','sources']},week_tier_diagnostic_rows=225,week_tier_exact_reconstruction_verified=True,errors=errors)
v['final_artifact_sha256']={rel:sha(ROOT/rel) for rel in v['final_artifact_sha256']}
v['supplementary_sha256']={p.name:sha(p) for p in [OUT/'WEEK_BY_TIER_DIAGNOSTIC.csv',OUT/'WEEK_TIER_DIAGNOSTIC_MANIFEST.json',OUT/'diagnose_week_tiers67.py']}
(OUT/'VALIDATION67.json').write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':v['status'],'history_hashes_verified':v['historical_files_hash_verified'],'links_checked':links,'new_graph_objects':v['new_graph_objects'],'errors':errors},indent=2))
if errors: raise SystemExit(1)
