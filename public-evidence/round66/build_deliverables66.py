"""66 delivery: bounded external observations + independent real-retail experiment."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,csv,io,re,shutil
import numpy as np
import pandas as pd
ROOT=Path(r'D:\GrowthResearch');EXT=ROOT/'public-evidence/round66';EXP=ROOT/'public-experiments/round66';NOW=datetime.now(timezone.utc).isoformat()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(rel,text):
 p=ROOT/rel
 if p.exists():raise RuntimeError('Refuse overwrite '+rel)
 p.write_text(text.strip()+'\n',encoding='utf-8',newline='\n')
def dump(rel,obj):write(rel,json.dumps(obj,ensure_ascii=False,indent=2))
def csvwrite(rel,rows):
 keys=[]
 for row in rows:
  for k in row:
   if k not in keys:keys.append(k)
 b=io.StringIO(newline='');w=csv.DictWriter(b,fieldnames=keys,lineterminator='\n');w.writeheader();w.writerows(rows);write(rel,b.getvalue())
protected={}
for p in ROOT.glob('*.md'):
 if re.match(r'\d\d_',p.name) and int(p.name[:2])<=65:protected[p.relative_to(ROOT).as_posix()]=sha(p)
for p in ROOT.glob('public-experiments/audit/*.download'):protected[p.relative_to(ROOT).as_posix()]=sha(p)
protected['SAMPLE_CATALOG.json']=sha(ROOT/'SAMPLE_CATALOG.json')
dump('public-evidence/round66/HISTORY.before66.json',protected)
graphpath=ROOT/'prediction-system/EVIDENCE_GRAPH.json';indexpath=ROOT/'EVIDENCE_INDEX.md'
oldgraph=json.loads(graphpath.read_text(encoding='utf-8-sig'));oldindex=indexpath.read_bytes()
shutil.copyfile(graphpath,EXT/'EVIDENCE_GRAPH.before66.json');shutil.copyfile(indexpath,EXT/'EVIDENCE_INDEX.before66.md')

records=[]
for p in (EXT/'sources').glob('*.json'):
 if p.name.endswith('.metadata.json'):continue
 obj=json.loads(p.read_text(encoding='utf-8'))
 if 'id' in obj and 'url' in obj:records.append(obj)
rm={x['id']:x for x in records}
dump('public-evidence/round66/ALL_SOURCES.json',records)
oldtimes=pd.read_csv(ROOT/'public-evidence/EXTERNAL_UA_TIMELINES.csv',keep_default_na=False)
times=oldtimes.loc[oldtimes.game_slug.isin(['rotate','meow'])].to_dict('records')
for row in times:row['round66_status']='reused_round65_evidence'

versionrows=[]
for slug,name,pkg in [('rotate','Rotate Rings','com.nebula.rotaterings'),('meow','Meowdoku','com.oakever.meowdoku')]:
 txt=(EXT/f'sources/{slug}-apkpure-history.txt').read_text(encoding='utf-8').splitlines()
 for i,line in enumerate(txt):
  v=line.strip()
  if not re.fullmatch(r'\d+\.\d+\.\d+',v):continue
  dat=next((txt[j].strip() for j in range(i+1,min(i+8,len(txt))) if re.fullmatch(r'[A-Z][a-z]{2} \d{1,2}, \d{4}',txt[j].strip())),None)
  if not dat:continue
  date=str(pd.to_datetime(dat).date())
  versionrows.append(dict(game=slug,package=pkg,version=v,directory_date=date,source_id='EXT66-'+slug+'-apkpure-history',source_text_line=i+1,
    semantics='Public distribution-directory version/date claim; NOT verified original rollout or SDK integration date',apk_downloaded=False,signature_checked_for_this_row=False))
  times.append(dict(event_id=f'EXT66-{slug}-version-{v}',game_slug=slug,package_name=pkg,event_type='third_party_version_directory',event_date=date,date_precision='day',value=v,evidence_grade='【间接迹象】',source_ids='EXT66-'+slug+'-apkpure-history',observation_utc=NOW,coverage_start='',coverage_end='',continuous_history='false',paid_acquisition_proven='false',profit_proven='false',limitations='Directory date only; sample signatures reused only for earlier audited versions, no new APK/SDK scan',round66_status='new_public_version_metadata'))
for event_type,value in [('historic_total_download_estimate','21000000'),('historic_last30_download_estimate','5700000'),('historic_version_claim','1.19.1')]:
 times.append(dict(event_id='EXT66-meow-'+event_type,game_slug='meow',package_name='com.oakever.meowdoku',event_type=event_type,event_date='2026-10-03',date_precision='archive_capture_day',value=value,evidence_grade='【第三方估算】' if 'estimate' in event_type else '【间接迹象】',source_ids='EXT66-meow-archive-20261003',observation_utc=NOW,coverage_start='page marked last updated 2026-10-02; last30 precise cutoff UNKNOWN',coverage_end='capture 2026-10-03; latest version update claim 2026-09-28',continuous_history='false',paid_acquisition_proven='false',profit_proven='false',limitations='Exact package/canonical verified in archived page; only one old capture, not daily trajectory',round66_status='new_historical_snapshot'))
csvwrite('public-evidence/round66/VERSION_DIRECTORY_ROWS.csv',versionrows)
csvwrite('66_外部推广证据时间线.csv',times)

sourcecatalog=['# 第66号外部公开来源与停止记录','',f'采集汇总：{NOW}。本轮仅11次公开URL请求，无生产广告/归因事件、无登录/挑战绕过。原始response哈希和保留产品元数据哈希分列；评论文本不用于证据且不保留。当前页面壳和空CDX不是没有广告或没有历史。','']
for x in sorted(records,key=lambda x:x['id']):
 sourcecatalog += [f'<a id="{x["id"].lower()}"></a>',f'## {x["id"]}','',f'- URL：{x["url"]}',f'- 最终：{x.get("final_url","UNKNOWN")}；HTTP {x.get("status","UNKNOWN")}；采集 {x["observed_utc"]}',f'- 原HTTP响应SHA256：`{x.get("response_sha256","UNKNOWN")}`；字节 {x.get("response_bytes","UNKNOWN")}']
 if x.get('path'):sourcecatalog += [f'- 保留原响应或脱敏元数据：[{x["path"]}](../../{x["path"]})；SHA256 `{x["sha256"]}`',f'- 可读抽取：[{x["text_path"]}](../../{x["text_path"]})']
 sourcecatalog += [f'- 限制：{x.get("error") or x.get("minimization") or "Only scoped public material; no advertiser spend, complete rank trajectory or model deployment evidence"}','']
sourcecatalog += ['## 实际覆盖','',
 '- Rotate CDX精确AppBrain URL：空列表；不能扩成整个互联网不存在归档。Meow同URL仅返回2026-10-03一条，已合法读取并核canonical/Play包名。',
 '- APKPure两款版本目录可读；按包名URL与开发者对应。日期是分发站目录声明，不把它当官方商店发布时间；见VERSION_DIRECTORY_ROWS.csv的行号。',
 '- AppBrain当前页仍需登录看完整排名历史，所查public chart脚本未给连续数值；AppMagic只有产品标题壳。开发商网站无可归属付费素材、日期、国家记录。',
 '- Meta/Google/TikTok复用65号已经保存的失败/页面壳证据，不重复同类受限查询。没有声称本轮穷尽每个平台、国家、日期。',
 '- 发现有界版本历史和一个旧快照后仍无连续前后各4周数据，停止A线追加搜索；不使用营销案例补因果。']
write('public-evidence/round66/SOURCE_CATALOG.md','\n'.join(sourcecatalog))

aranges={slug:(min(v['directory_date'] for v in versionrows if v['game']==slug),max(v['directory_date'] for v in versionrows if v['game']==slug),sum(v['game']==slug for v in versionrows)) for slug in ['rotate','meow']}
external=r'''# Rotate Rings / Meowdoku历史买量轨迹调查

2026-11-20 · 第66号A线。精确包名分别为`com.nebula.rotaterings`（Nebula Studio）与`com.oakever.meowdoku`（Oakever Games），沿用65号身份与已核原包。**新增：两款公开版本目录；Meow一个2026-10-03历史下载估算快照。未取得任何新增连续下载/排名序列或可核验的AppLovin/Unity获客记录。**

来源URL、采集时间、原response/保留内容SHA256和范围见[原始目录](public-evidence/round66/SOURCE_CATALOG.md)，逐事件日期见[根时间线CSV](66_外部推广证据时间线.csv)。原00—65报告和样本不修改、不重复逆向。

## 1. Rotate Rings：版本历史变多，不等于付费扩量已证

【间接迹象】APKPure精确包名版本目录目前可公开取得，DATE_RANGE_ROTATE。可见1.1.8/10-28、1.2.0/11-04、1.2.2/11-07、1.2.3/11-13、1.2.4/11-17等。日期为第三方分发记录，不是已核的官方灰度/首次上线日，也没有逐版签名或SDK新审计。[EXT66-rotate-apkpure-history]

【直接观察（既有静态证据）】此前1.2.2→1.2.4同签名差分新增国家×安装day0—6收益规则；对应AF/Firebase版本在该跨度仍同，MAX13.6.2为既有1.2.4包内版本。**没有为所有目录版本补造SDK/adapter版本，也没有把目录体积变化解释成SDK升级。**[05号](05_历史版本策略演进.md)、[20号](20_Axon实际事件调用链.md)

【第三方估算】65号的近30天850万、累计1600万仍为当前页所列数值；本次页面同值可能因四舍五入/缓存，不能据一天间同值说明没增长。精确AppBrain URL的CDX查询为空；当前AppBrain排名历史需登录，AppMagic是标题壳，开发商主页只给身份，均未产生连续量。

**裁决：没有找到足以确定历史突然扩量起点、持续时间或真实预算变化的新证据。**可以说有大规模近期下载估算和频繁版本目录记录；不能说付费素材增加、国家扩张、预算提高或某SDK升级造成扩量。版本跨度长不代表下载曲线有同等覆盖。

## 2. Meowdoku：新增两个时点可比估算，支持较晚窗口量更高

【直接观察】Internet Archive CDX精确AppBrain canonical返回capture `20261003145311`；归档页面canonical与Google Play链接均指本包。页面标last updated=2026-10-02，称版本1.19.1/9-28。页面含评论的无关HTML不保留，仅保存产品/聚合片段及原响应哈希。[EXT66-meow-cdx、EXT66-meow-archive-20261003]

| 归档/观察时点 | 供应商所称累计量 | 所称最近30天量 | 性质 |
|---|---:|---:|---|
| 2026-10-03归档（页面更新10-02） | 2100万 | 570万 | AppBrain历史估算，不是归因或投放花费 |
| 2026-11-19已有快照 / 11-20复核 | 3600万 | 930万 | 同供应商当前滚动估算，准确数据截止未知 |

【第三方估算＋派生算术】后一个滚动总量比前一个约高**63.2%**；累计估算差约1500万。只能确认“两个历史时点的供应商估算差异”，算法/覆盖/误差和精确窗口水位未公开，**不是真实安装增长率、统计显著性、付费量、增量量或盈利增长**。不能用两点插出逐日轨迹、定位突增日期；也不能以累计差抵消估算口径问题。

【间接迹象】APKPure版本目录DATE_RANGE_MEOW，含1.19.1/9-29、1.20.0/10-13、1.21.0/10-16、1.23.0/10-29、1.25.0/11-14、1.25.1/11-16。它与历史AppBrain1.19.1/9-28有一天差异；65号AppBrain1.25.0/11-13与目录/Play也有差异，逐个保留，不硬校成官方发布日。[EXT66-meow-apkpure-history]

**裁决：新增“历史近期下载估算增加”的有限证据，仍没有连续前后各4周或能确定突然扩量的证据。**目录证明有版本迭代，但无法知道增长发生在何次更新之前或之后。所查CDX只一个旧捕获，不是某事件前后连续覆盖。

## 3. 真实素材、国家、渠道与平台角色

| 要确认的事 | Rotate | Meow |
|---|---|---|
| 精确包名的版本目录 | 已取得，第三方日期 | 已取得，第三方日期 |
| 连续日/周下载或历史榜单 | 未取得 | 未取得，仅新增一份旧快照 |
| paid creative ID＋advertiser＋包名落地页＋日期 | UNKNOWN | UNKNOWN |
| 素材创意类型/数量演变及首次展示 | UNKNOWN | UNKNOWN |
| 可核投放国家或新市场 | UNKNOWN | UNKNOWN；商店榜单国家不算投放国家 |
| AppLovin或Unity作为广告展示来源 | 没有新增可归属付费展示记录 | 同左 |
| AppLovin或Unity实际获客渠道、时间与预算 | UNKNOWN | UNKNOWN |
| 真实盈利/成熟ROAS/模型贡献 | UNKNOWN | UNKNOWN |

既有Meta403、Google/TikTok页面壳/通用页没有提供目标创意记录，本轮按65号停止纪律不重复受限搜索。网站或SDK存在、MAX变现枚举、Unity广告适配器、网络需求方或MMP可配partner均不能证明目标游戏实际购买该网络流量。[65号](65_公开扩量证据与模型实验可行性审计.md)、[64号](64_普通游戏盈利跃迁最终机制判断.md)

## 4. 竞争解释与先后关系

- **H1 素材/市场变化：**缺创意与市场时间序列；两款未知，不能由下载估算或版本数支持。
- **H2 价值优化变化：**Rotate收入规则差分、Meow GRT早期信号是已有代码事实；没有后台启用日/实际目标/平台消费，不能连接到量变因果。
- **H3 变现/留存变化：**无固定cohort真实收益/留存对照，UNKNOWN；版本变化和更多安装均不能代替ARPU。
- **H4 商店推荐/自然传播/外部需求/归因或估算变化：**与现有两点完全相容，无法排除；无法将“估算增加”唯一归给买量。

Meow旧快照时间先于11月版本，但没有中间量/配置生效表；Rotate旧版入库/目录/当前Play/审计时间不等价。因此不能说“版本升级后扩量”，也不能说“扩量促使升级”。

## 5. A线停止与下一份材料

本轮限定10个发现入口＋1个明确归档读取，已完成；没有连续历史，**停止重复搜索**，不登录或绕过访问控制、不继续换站凑结论。若恢复，需要同包名同口径前后各4周以上日/周量/排名，或带creative/advertiser/日期/国家/落地页的真实记录；平台获客与盈利还需授权campaign/成本/成熟收入。B线零售实验不能填补这些缺口。
'''
for slug,token in [('rotate','DATE_RANGE_ROTATE'),('meow','DATE_RANGE_MEOW')]:
 lo,hi,n=aranges[slug];external=external.replace(token,f'共{n}条版本记录，日期跨度{lo}—{hi}')
write('66_Rotate与Meow历史买量轨迹调查.md',external)

results=pd.read_csv(EXP/'MODEL_RESULTS.csv');test=results[(results['split']=='test')&(results.arm=='dedup_positive_sales')].copy()
quality=json.loads((EXP/'DATA_QUALITY.json').read_text(encoding='utf-8'));manifest=json.loads((EXP/'RUN_MANIFEST.json').read_text(encoding='utf-8'))
dist=json.loads((EXP/'LABEL_DISTRIBUTIONS.json').read_text(encoding='utf-8'));splits=json.loads((EXP/'SPLIT_AND_LEAKAGE_CHECKS.json').read_text(encoding='utf-8'))
assert json.loads((EXP/'BOUNDARY_TESTS.json').read_text(encoding='utf-8'))['status']=='PASS'
assert json.loads((EXP/'EVALUATION_FIX_CHECK.json').read_text(encoding='utf-8'))['mae_rmse_median_unchanged']
dest=ROOT/'66_模型实验结果.csv';assert not dest.exists();shutil.copyfile(EXP/'MODEL_RESULTS.csv',dest)
def pct(x):return f'{100*x:.2f}%'
def ci(row,metric):return f'[{row[metric+"_ci_low"]:.2f}, {row[metric+"_ci_high"]:.2f}]'
tablelines=['| 窗口 | 模型 | MAE GBP | RMSE GBP | 中位绝对误差 GBP | 高消费召回@10%预算 | 金额捕获@10%预算 |','|---|---|---:|---:|---:|---:|---:|']
for _,x in test.iterrows():tablelines.append(f'| {int(x.horizon_days)}天 | {x.model} | {x.mae:.2f} | {x.rmse:.2f} | {x.median_ae:.2f} | {pct(x.top10_recall)} | {pct(x.top10_value_capture)} |')
cilines=['| 窗口 | 模型 | MAE相对历史日均B1改善 | 配对95% CI | 六主比较同时区间对应逐项99.1667% CI |','|---|---|---:|---|---|']
for _,x in test.loc[test.model.isin(['M0','M1','M2'])].iterrows():cilines.append(f'| {int(x.horizon_days)}天 | {x.model} | {x.mae_gain_vs_history_pct:.2f}% | {ci(x,"mae_gain_vs_history_pct")} | {ci(x,"mae_gain_vs_history_familywise99_1667")} |')
tier=pd.read_csv(EXP/'STRATIFIED_ERRORS.csv');tier=tier[(tier.arm=='dedup_positive_sales')&(tier.dimension=='value_tier')&(tier.model=='M2')]
tierlines=['| 窗口 | 真实金额层（仅事后评价） | 客户时点行数 | M2 MAE GBP | M2 RMSE GBP |','|---|---|---:|---:|---:|']
for _,x in tier.iterrows():tierlines.append(f'| {int(x.horizon_days)}天 | {x.group} | {int(x.n)} | {x.mae:.2f} | {x.rmse:.2f} |')
experiment=r'''# UCI用户未来7天/28天发票金额预测实验

2026-11-20 · 第66号B线。**本实验真实执行了零售发票金额预测，未使用任何手游数据，也没有恢复Axon/Vector。**历史行为包含有用排序信息，28天近期/间隔特征模型相对历史日均基线的MAE改善有统计支持；但RMSE未获改善，全部模型MAE仍差于零金额诊断基线，不能概括成“全面准确预测未来消费”。

## 1. 数据、许可与可复现入口

数据为Daqing Chen发表于UCI的Online Retail（2010-12-01—2011-12-09，DOI [10.24432/C5BW33](https://doi.org/10.24432/C5BW33)，CC BY4）。复用65号已下载ZIP，原SHA256 `f5385cbb54bbebf7196389109c6b0621faab0c304e3702548165e71c84aede8b`；读前读后相同，未下载或改原件。原厂商资料、许可与65号结构审计保持不变。

- 拟合前固定：[PREREGISTERED_PROTOCOL](public-experiments/round66/PREREGISTERED_PROTOCOL.md)；代码：[run_experiment66.py](public-experiments/round66/run_experiment66.py)；环境/运行哈希：[RUN_MANIFEST](public-experiments/round66/RUN_MANIFEST.json)。
- 结果与全部CI：[66_模型实验结果.csv](66_模型实验结果.csv)；分层：[STRATIFIED_ERRORS](public-experiments/round66/STRATIFIED_ERRORS.csv)；标签：[LABEL_DISTRIBUTIONS](public-experiments/round66/LABEL_DISTRIBUTIONS.json)。
- 清洗：[DATA_QUALITY](public-experiments/round66/DATA_QUALITY.json)；拆分：[SPLIT_AND_LEAKAGE_CHECKS](public-experiments/round66/SPLIT_AND_LEAKAGE_CHECKS.json)；边界测试：[BOUNDARY_TESTS](public-experiments/round66/BOUNDARY_TESTS.json)。

可以运行`python public-experiments/round66/run_experiment66.py`在本研究根目录复现（先读initial-run修正说明；会更新本轮运行结果，不触碰原件）。模型超参冻结，未按测试调参、裁尾或重选金额口径。最终18个固定模型（3清洗/金额臂×2窗口×3模型），不含常数与日均基线；评价修正前18次原拟合也保留，总共两遍相同模型，不能把它伪称超参搜索。

## 2. 清洗与两种金额语义

| 项目 | 实际结果 | 处理 |
|---|---:|---|
| 原始行 | 541909 | ZIP只读 |
| 所有原始列完全重复 | 5268 | 主分析keep-first，清后536641；保留不去重正额臂作为预定敏感性 |
| 去重后缺CustomerID | 135037 | 计国家分布后剔除；不造客户、不补真实零消费 |
| 去重后取消前缀C行 | 9251 | 另审计，签名额约-893979.73 GBP |
| 去重后负金额 | 9253 | 其中2行无C前缀且为负单价；不混同所有取消单 |
| 去重后非正单价 | 2512 | 明确排除金额任务；其中2行负价额-22124.12 GBP单列，不能称漏掉了已核购买收入 |

**主目标＝未来正向发票销售额GBP。**只用有CustomerID、单价>0、数量>0且非取消单记录；不是到账、净利润或全渠道消费。**次目标＝记录内签名发票净额GBP**，使用有键/单价>0的记录含负数量/取消；不能凭客户端发票把退款逐笔匹配到原订单，也没有税费/银行对账。

原数据存在同一经济行是否真重复的歧义，本轮按明确要求主分析清理，但不隐瞒保留重复敏感性。缺键剔除造成选择偏差，结果仅适用于可分组、过去在该商家出现过正向购买的客户；完整未购买人群不在数据中。

## 3. 预测时点与防泄漏

特征`InvoiceDate < t`；标签`[t,t+7天)`或`[t,t+28天)`。t为文件时钟的周一零点；原件无可确认时区/available_at，**只认证event-time离线假设，不认证实时数据已到达**。

| 集合 | 固定时点 | 独立客户数 | 客户×时点行 |
|---|---|---:|---:|
| 训练 | 2011-01-03—04-25每周一（17时点） | 1423 | 17058 |
| 验证 | 2011-06-06/13/20/27 | 571 | 2220 |
| 测试 | 2011-08-01/08/15/22/29 | 690 | 3386 |

客户按固定SHA256分桶6:2:2，所有事件/时点永远留在一个集合；三集合客户交集**0**。这不是随机拆事件：同时严格时间外、客户外。ID只作源内历史聚合/隔离，不输入模型、不写逐客户预测或ID导出。测试客户的合法t前自身历史允许作为输入，但其标签/记录不参与训练预处理和拟合。

训练最后28天标签结束5-23<验证6-06；验证最后28天结束7-25<测试8-01；测试最后28天结束9-26<源文件末12-09。不同测试时点标签可重叠，所以3386行不是3386独立客户，使用客户cluster CI并单列每周表现。

边界fixture独立检查：t当时事件不进历史、t+7/t+28不进对应标签；把未来金额改极大值不改变所有特征；常数预测不能因行序获得排序收益。合成fixture仅验证边界代码，不是模型增益数据。

## 4. 三个固定模型与对照

- **M0：**累计正向金额、去重发票购买次数（2特征）。
- **M1：**M0加7/28/90天金额与发票次数（8特征）。
- **M2：**M1加购买间隔均值/标准差、最近购买距今、累计及窗口商品件数、日均金额/次数趋势（18特征）。
- **B0_GLOBAL：**训练目标均值常数；**B1_HISTORY_RATE：**客户历史金额÷已观察天数×窗口；**B2_ZERO_EXPLORATORY：**零金额常数诊断，见评价修正。

M0—M2使用相同浅层HistGradientBoostingRegressor（160轮、learning_rate=.05、leaf≤7、depth≤3、min_leaf40、L2=10、bins64、seed6601，early_stopping=False）；正额Poisson损失、签名敏感性平方损失。固定样本、迭代和特征版本，不利用测试改超参。Poisson是条件均值损失，不代表发票金额真服从离散Poisson分布；与MAE最优中位数预测目标不同，必须结合零基线解读。

## 5. 实际测试结果

RESULT_TABLE

高消费recall的真实目标集合只含正金额：人数=min(ceil(N×10%),正额人数)，预测选择预算仍为ceil(N×10%)。7天正额仅239/3386行，不能把零行塞进“高消费”集合。边界平分以期望权重处理；常数预测召回约10.01%，不是排序能力。金额捕获衡量选出的10%样本占测试正额的份额，不是利润或广告增量。

### MAE相对历史均值基线：哪些有统计支持

CI_TABLE

区间单位为改善百分比（正数误差下降）。500次配对**客户cluster bootstrap**，同一次抽样同时带入所有模型/基线及该客户全部时点。95%区间条件于固定训练与这5个测试时点；主预定6项MAE比较另用Bonferroni逐项99.1667%区间控制家族5%。500次用于极尾分位数较粗，不能把临界结果说得精确。

- **28天M1/M2的MAE优于B1有家族校正支持。**M2改善22.74%，95% CI[13.69,32.30]，同时区间[9.40,34.64]；M1改善19.31%，同时区间[10.14,31.57]。这是对较弱历史日均基线的具体指标结论，不是所有模型/指标均有效。
- **7天M2改善11.71%的普通95% CI为[2.60,21.66]，但校正后[-0.96,22.90]跨0，主要检验不充分。**M0/M1的7天和M0的28天也不能确认MAE改善。
- **RMSE没有稳健改善。**M2对B1在7/28天反而点估计差7.73%/9.38%，改善CI均跨0；对极端大额预测不稳定，不把MAE改善冒充长尾已解决。
- **高消费识别有局部探索性支持：**M2对B1召回提高7天6.28个百分点（95% CI[0.44,12.34]），28天7.08个百分点（[2.21,15.38]）；M0也有排序信号，不能从点估计断言增加特征后每一步都更好。该次要指标未作全部多重校正，不能升级主要确认性结论。

### 零值、长尾和总体校准

测试7天**92.94%**、28天**75.90%**客户时点没有观察到正向购买；这不是在别处真实零消费。top1%客户时点承载正额约53.29%/42.89%。正额7/28天P99约5068.04/8202.75 GBP，大额尾部决定RMSE波动。

M2总预测/总真实正额在7天为1.563、28天1.065；7天明显高估，不能说校准已好。**零基线MAE为40.93/186.83，均优于M0—M2；B0的7天MAE79.57也低于M2的84.17。**高零值任务可通过预测全0获得低MAE但没有有用排序，条件均值模型可有排序又牺牲MAE，所以“能预测”必须分为金额误差、尾部和排序，不是单一胜负。

### 分消费层误差

TIER_TABLE

分层使用真实未来金额，仅作评价，不作为模型输入；细层样本少，不称统计稳健。按country（至少50行）和5个landmark的全部误差已导出。M2的28天MAE在5个测试时点都低于B1；7天8-29反而高于B1，不能隐藏时间漂移。只有5周，CI不覆盖宏观季节变化/拟合波动，不能宣称跨年度稳定。

## 6. 质量修正、敏感性与失败结果保留

**发现并修复的是评价问题，不是改成绩。**首轮按固定行序处理Top10平分且将零值包含在真实Top10，导致7天B0常数recall假象35.40%。[EVALUATION_CORRECTION](public-experiments/round66/EVALUATION_CORRECTION.md)记录修正，初始代码/协议/全部结果保留[initial-run](public-experiments/round66/initial-run/MODEL_RESULTS.csv)。改为正额集合与平分期望权重，并新增零基线诊断；未改特征、样本、模型、超参、金额口径。

[EVALUATION_FIX_CHECK](public-experiments/round66/EVALUATION_FIX_CHECK.json)核对首轮与修正后所有旧60结果行MAE/RMSE/中位误差相同。指标fixture首次因隔离函数测试缺hashlib导入失败，补齐测试环境后通过；实验本身无此缺陷。无未来信息泄漏被发现；available_at缺失是数据边界，不声称已补齐。

预定敏感性：M2签名发票净额7/28天对B1 MAE改善12.99%/18.33%；不去重正额臂12.34%/23.44%，方向未由清重复操作制造。但签名任务的负数/退款及其模型损失不同，不能互相合并求一个“最好值”。所有失败/负改善均保留在根CSV（72行：含验证、测试、3口径及6模型/基线）。没有按结果放宽验证目标。

## 7. 可下结论与不可外推

1. **历史行为能否预测7/28天？**有真实的排序信号，28天近期/间隔模型对历史日均MAE有支持；7天主要误差结论较弱，零值和长尾使全面准确性不成立。
2. **哪些统计支持？**上文指定的28天MAE家族比较；高消费召回为局部探索性支持。RMSE、特征每次增加的独立增益、跨季节/跨商家泛化没有确认。
3. **不能外推：**这是同一零售商已观察客户的文件内发票金额，不是IAA/IAP或手游LTV；没有安装前曝光特征、跨游戏ID、广告价格/预算/因果选择机制，不换算买量ROAS，不解释四款盈利，不证明Axon/Vector架构或效果。
4. **下一步：**若继续方法研究，预先固定新时间段/新客户，区分条件均值与零值中位数目标、先校准/两阶段零值模型及长尾误差，再做独立时间外确认。不能在本测试上继续调参并重新宣称独立发现。要回答手游问题仍需合法游戏安装与成熟收入，而非再扩零售模型复杂度。
'''
experiment=experiment.replace('RESULT_TABLE','\n'.join(tablelines)).replace('CI_TABLE','\n'.join(cilines)).replace('TIER_TABLE','\n'.join(tierlines))
write('66_UCI用户未来消费金额预测实验.md',experiment)

# Reuse scoped source types; experimental observations are not SDK or production evidence.
sources=[];nodes=[];edges=[]
for rec in records:
 if rec.get('path'):
  sources.append(dict(id=rec['id'],url=rec['url'],path=rec['path'],sha256=rec['sha256'],source_date=rec['observed_utc'],
   evidence_kind='bounded public history observation',evidence_level='【直接观察】 response; underlying estimate/catalog is third-party',
   original_response_sha256=rec.get('response_sha256'),production_actual_proven=False,observed_target_game_delivery=False,server_model_training=False,
   scope='Public product/history only; no actual advertiser spend, paid attribution or platform training proof'))
for ident,path in [('RE66S_data','public-experiments/audit/retail352.download'),('RE66S_protocol','public-experiments/round66/PREREGISTERED_PROTOCOL.md'),('RE66S_results','public-experiments/round66/MODEL_RESULTS.csv'),('RE66S_run','public-experiments/round66/RUN_MANIFEST.json'),('RE66S_fix','public-experiments/round66/EVALUATION_CORRECTION.md')]:
 sources.append(dict(id=ident,path=path,sha256=sha(ROOT/path),source_date=NOW,evidence_kind='independent actual public-retail experiment' if ident!='RE66S_data' else 'UCI public original data',
  evidence_level='【真实公开零售数据实验】',url='https://archive.ics.uci.edu/dataset/352/online+retail' if ident=='RE66S_data' else None,
  production_actual_proven=False,observed_target_game_delivery=False,server_model_training=False,scope='Retail invoices only; no game-model, ad-delivery or profit inference'))
for ident,label,stage in [('EXT66_rotate','Rotate version metadata, no continuous growth curve','external_history'),('EXT66_meow_old','Meow Oct3 estimated recent downloads 5.7M','third_party_historical_estimate'),('EXT66_meow_current','Meow Nov19/20 estimated recent downloads 9.3M','third_party_current_estimate'),('EXT66_paid','AppLovin/Unity actual acquisition UNKNOWN','unknown_paid_channel'),('RE66_data','Authorized public retail invoice records','public_dataset'),('RE66_predictions','Customer/time-disjoint 7/28-day invoice predictions','independent_retail_experiment'),('RE66_mae28','M1/M2 28-day MAE gain versus history-rate, scoped statistical support','retail_statistical_result'),('RE66_gameprofit','Game/Axon/Vector profitability inference unavailable','unknown_cross_domain')]:nodes.append(dict(id=ident,label=label,stage=stage,company='public independent research'))
def edge(ident,a,b,claim,refs,status,grade,missing):
 edges.append(dict(id=ident,source=a,target=b,claim=claim,source_ids=refs,status=status,evidence_level=grade,diagram_style='solid' if status in ['observed_scoped','experiment_scoped'] else 'dashed',
  edge_type='external_history_or_independent_retail_experiment',data_provider=a,data_receiver=b,permission_conditions='Public metadata or UCI CC BY4; source-scoped anonymized keys, no production calls',
  missing_evidence=missing,reviewed_utc=NOW,production_actual_proven=False,observed_target_game_delivery=False,independent_production_audit=False,
  six_layers=dict(sdk_capability=False,actual_game_business_callsite=False,request_construction_code=False,production_successful_send=False,server_received=False,server_model_training=False)))
edge('EXT66E1','EXT66_meow_old','EXT66_meow_current','Two rounded AppBrain snapshots show estimated last30 total 5.7M to 9.3M, not continuous growth or paid-attributed installs',['EXT66-meow-archive-20261003','EXT66-meow-appbrain'],'observed_scoped','【第三方估算】','Daily/weekly history, stable estimate methodology, actual attribution and cost')
edge('EXT66E2','EXT66_meow_current','EXT66_paid','Estimate difference cannot identify actual AppLovin/Unity acquisition',['EXT66-meow-appbrain'],'unknown','【无法确认】','Advertiser/creative/campaign/date evidence with exact landing app; paid-channel records')
edge('EXT66E3','EXT66_rotate','EXT66_paid','Version directory and MAX/Unity capabilities do not prove paid acquisition',['EXT66-rotate-apkpure-history'],'unknown','【无法确认】','Continuous history, paid creatives, exact channel/campaign and spend')
edge('RE66E1','RE66_data','RE66_predictions','Actual public invoices used for fixed time-and-customer-disjoint forecasting; no game data',['RE66S_data','RE66S_protocol','RE66S_run','RE66S_fix'],'experiment_scoped','【真实公开零售数据实验】','available_at absent; no real-time availability or cash-net label verification')
edge('RE66E2','RE66_predictions','RE66_mae28','M1/M2 28-day MAE versus history-rate improves with paired cluster familywise interval; RMSE not improved and zero-baseline MAE lower',['RE66S_results','RE66S_protocol'],'experiment_scoped','【真实公开零售数据实验】','Independent future seasons, refit uncertainty, tail robustness, stronger decision-aligned baselines')
edge('RE66E3','RE66_mae28','RE66_gameprofit','Retail prediction results cannot explain target games or Axon/Vector acquisition profit',['RE66S_results','RE66S_data'],'unknown','【无法确认】','Game-specific mature true revenue, ad opportunities/cost, platform consumer lineage and causal experiment')
g=json.loads(json.dumps(oldgraph))
for key,vals in [('nodes',nodes),('edges',edges),('sources',sources)]:
 assert not ({v['id'] for v in vals}&{v['id'] for v in g[key]})
 g[key].extend(vals)
g['public_history_retail_round66']=dict(reviewed_utc=NOW,scope='Bounded game public-history follow-up and independent retail forecasts; no further SDK research',
 source_catalog='public-evidence/round66/SOURCE_CATALOG.md',retail_run='public-experiments/round66/RUN_MANIFEST.json',
 historical_meow_estimate_increase=True,continuous_before_after_growth_verified=False,paid_channel_proven=False,
 retail_primary_result='28-day M1/M2 MAE improves vs history-rate under familywise cluster intervals; no broad RMSE or zero-baseline superiority',
 new_node_ids=[x['id'] for x in nodes],new_edge_ids=[x['id'] for x in edges],new_source_ids=[x['id'] for x in sources])
graphpath.write_text(json.dumps(g,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
dump('public-evidence/round66/NEW_GRAPH_OBJECTS.json',dict(nodes=nodes,edges=edges,sources=sources))
append='''\n\n<a id="round66"></a>\n\n## ROUND66 · 两款公开轨迹与真实零售预测（不外推游戏）\n\n- [66号外部轨迹报告](66_Rotate与Meow历史买量轨迹调查.md) / [外部时间线](66_外部推广证据时间线.csv)\n- [66号UCI预测实验报告](66_UCI用户未来消费金额预测实验.md) / [全部模型/基线结果及CI](66_模型实验结果.csv)\n- [新外部来源URL/日期/哈希](public-evidence/round66/SOURCE_CATALOG.md) / [版本目录原位置](public-evidence/round66/VERSION_DIRECTORY_ROWS.csv)\n- [预固定协议](public-experiments/round66/PREREGISTERED_PROTOCOL.md) / [真实运行源码](public-experiments/round66/run_experiment66.py) / [运行清单](public-experiments/round66/RUN_MANIFEST.json)\n- [评价修正与初始结果保留](public-experiments/round66/EVALUATION_CORRECTION.md) / [泄漏边界fixture](public-experiments/round66/BOUNDARY_TESTS.json)\n- [最终校验](public-evidence/round66/VALIDATION66.json)\n\nA线新事实：Meow精确包名10月3日归档近30天估570万，当前930万；两个时点的估算差异约63.2%，不是付费安装、突然变点、真实预算或利润。两款版本目录可读，但无连续前后各4周量、paid creative或AppLovin/Unity渠道证据；停止重复搜索。B线实际UCI发票实验：客户与时间完全隔离，28天M1/M2相对历史日均MAE有家族校正支持；7天主要检验不足、RMSE未改善、零基线MAE更低。修复Top10零值/平分假象，保留初始结果；未改模型或金额口径。零售预测不证明任何目标游戏/平台生产消费或盈利。\n'''
with indexpath.open('ab') as f:f.write(append.encode('utf-8'))

errors=[]
for rel,s in protected.items():
 if sha(ROOT/rel)!=s:errors.append('historical file modified '+rel)
for key in ['nodes','edges','sources']:
 if g[key][:len(oldgraph[key])]!=oldgraph[key]:errors.append('old graph objects changed '+key)
 if len({v['id'] for v in g[key]})!=len(g[key]):errors.append('duplicate graph IDs '+key)
for key,val in oldgraph.items():
 if key not in ['nodes','edges','sources'] and g[key]!=val:errors.append('old metadata changed '+key)
if not indexpath.read_bytes().startswith(oldindex):errors.append('old index bytes changed')
if not manifest['raw_unchanged']:errors.append('raw data modified')
if not manifest['checks']['temporal_embargo'] or manifest['checks']['customer_overlap']!=0:errors.append('leakage guard failed')
if len(results)!=72:errors.append('unexpected result rows')
for rec in records:
 if rec.get('path') and sha(ROOT/rec['path'])!=rec['sha256']:errors.append('source hash mismatch '+rec['id'])
newdeliverables=['66_Rotate与Meow历史买量轨迹调查.md','66_UCI用户未来消费金额预测实验.md','66_外部推广证据时间线.csv','66_模型实验结果.csv','public-evidence/round66/SOURCE_CATALOG.md']
links=0
for rel in newdeliverables:
 p=ROOT/rel;text=p.read_text(encoding='utf-8')
 if '\ufffd' in text:errors.append('new encoding loss '+rel)
 if p.suffix=='.md':
  for t in re.findall(r'\]\(([^)]+)\)',text):
   if t.startswith(('https:','http:','#')):continue
   if not (p.parent/t.split('#')[0]).is_file():errors.append('broken link '+rel+' -> '+t)
   links+=1
for e in edges:
 if any(e['six_layers'].values()):errors.append('retail evidence promoted to platform production '+e['id'])
v=dict(status='PASS' if not errors else 'FAIL',reviewed_utc=NOW,scope='Artifact integrity, static leakage guards, actual fixed retail run, public-source hashes; not game profitability or production platform validation',
 historical_files_hash_verified=len(protected),historical_report_count=sum(rel.endswith('.md') for rel in protected),
 source_data_unchanged=manifest['raw_unchanged'],result_rows=len(results),final_models_fitted=18,retail_eval_correction_core_metrics_unchanged=True,
 external_new_requests=len(records),external_version_rows=len(versionrows),external_timeline_rows=len(times),continuous_growth_verified=False,paid_channel_verified=False,
 historical_graph_preserved={k:len(oldgraph[k]) for k in ['nodes','edges','sources']},new_graph_objects={k:len(val) for k,val in [('nodes',nodes),('edges',edges),('sources',sources)]},
 source_lookup_and_history_complete=False,local_links_checked=links,production_ad_events_sent=0,access_controls_bypassed=0,no_real_person_identity_matching=True,errors=errors,
 artifact_sha256={rel:sha(ROOT/rel) for rel in newdeliverables})
dump('public-evidence/round66/VALIDATION66.json',v)
print(json.dumps({k:val for k,val in v.items() if k!='artifact_sha256'},ensure_ascii=True,indent=2))
if errors:raise SystemExit(1)
