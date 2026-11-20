"""Deliver round 65 identity and public-data admission audit, not model training."""
from pathlib import Path
from datetime import datetime,timezone
import json,csv,io,hashlib,re
ROOT=Path(r'D:\GrowthResearch');PUB=ROOT/'public-evidence';EXP=ROOT/'public-experiments'
NOW=datetime.now(timezone.utc).isoformat()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(rel,text):
 p=ROOT/rel
 if p.exists():raise RuntimeError('Refuse overwrite '+rel)
 p.write_text(text.strip()+'\n',encoding='utf-8',newline='\n')
def dump(rel,obj):write(rel,json.dumps(obj,ensure_ascii=False,indent=2))
def table(rel,rows):
 b=io.StringIO(newline='');w=csv.DictWriter(b,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows);write(rel,b.getvalue())

fetches=json.loads((PUB/'ALL_FETCHES.json').read_text(encoding='utf-8'));fetchmap={x['id']:x for x in fetches}
samples=json.loads((ROOT/'SAMPLE_CATALOG.json').read_text(encoding='utf-8-sig'))
assets=json.loads((EXP/'audit/ASSET_VERIFICATION.json').read_text(encoding='utf-8'));assetmap={x['id']:x for x in assets}
obd=json.loads((EXP/'audit/OBD_SAMPLE_VERIFICATION.json').read_text(encoding='utf-8'))
games=[
 ('car','Car Race','com.dino.race.master','iKame Games - Zego Studio','1.348.2','13.6.4','2021-09','1.349.0','2026-11-04','2026-11-12',380000000,3600000,'100,000,000+','Car Race/Race Master等同名赛车很多；仅接受精确包名'),
 ('meow','Meowdoku: Brain Puzzle Games','com.oakever.meowdoku','Oakever Games','1.25.1','13.2.0','2026-04','1.25.0','2026-11-13','2026-11-16',36000000,9300000,'10,000,000+','猫主题数独/逻辑游戏众多；Meowku/KittyDoku不是本包'),
 ('rotate','Rotate Rings','com.nebula.rotaterings','Nebula Studio','1.2.4; history 1.2.2','13.6.2','2026-07','1.2.4','2026-11-16','2026-11-16',16000000,8500000,'10,000,000+','同名转环产品较多；Nebula与其他发行商不得合并'),
 ('jewel','Jewel Coloring','color.number.paint.pixle.art.sort.jigsaw','TaTa Game Technology Limited','1.24.1','13.6.3','2026-02','1.24.1','2026-09-17','2026-09-17',14000000,800000,'10,000,000+','珠宝填色/数字填色产品众多；不能按图标/品类认定'),
]
registry=[];timelines=[]
def event(slug,pkg,kind,date,precision,value,grade,source,coverage_start='',coverage_end='',limit=''):
 timelines.append(dict(event_id=f'PE65-{slug}-{len(timelines)+1:02}',game_slug=slug,package_name=pkg,event_type=kind,event_date=date,date_precision=precision,
  value=value,evidence_grade=grade,source_ids=source,observation_utc=NOW,coverage_start=coverage_start,coverage_end=coverage_end,
  continuous_history='false',paid_acquisition_proven='false',profit_proven='false',limitations=limit))
for g in games:
 slug,name,pkg,dev,ver,maxver,launch,abver,abdate,playdate,total,recent,band,risk=g
 sample=next(s for s in samples if s.get('package')==pkg)
 meta=json.loads((PUB/f'raw/{slug}-play.metadata.json').read_text(encoding='utf-8'))
 ld=meta['jsonld'][0]
 assert pkg in ld['url'] and ld['name']==name
 assert re.sub(r'\s+',' ',ld['author']['name'])==dev
 registry.append(dict(game_slug=slug,game_name=name,package_name=pkg,developer_current_play=dev,store_url=f'https://play.google.com/store/apps/details?id={pkg}',
  known_apk_versions=ver,original_sample_sha256=sample['sha256'],current_appbrain_version=abver,current_appbrain_update_date=abdate,current_play_update_date=playdate,
  verified_release_date='UNKNOWN; current updated date is not a verified per-version original publication date',
  earliest_verified_public_presence_in_existing_evidence='2026-11-18',appbrain_claimed_launch_month=launch,
  appbrain_launch_month_status='Third-party historical metadata claim, not independently verified original release',
  identity_status='VERIFIED_PACKAGE_AND_DEVELOPER',same_name_confusion=risk,
  date_conflict='AppBrain/current Play update dates disagree; do not force version/date join' if abdate!=playdate else 'Current metadata dates agree; still not historical rollout proof',
  raw_source_ids=f'{slug}-play;{slug}-appbrain;SAMPLE_CATALOG;P01',public_expansion_tracking_status='LIMITED_SINGLE_SNAPSHOT',sudden_expansion_status='UNKNOWN',
  complete_historical_rank_series='false',verified_paid_creative_record='false'))
 event(slug,pkg,'third_party_claimed_launch_month',launch,'month',launch,'【间接迹象】',slug+'-appbrain',limit='AppBrain claims availability since this month; not an independently verified original release')
 event(slug,pkg,'earliest_verified_presence_in_local_public_evidence','2026-11-18','day','Existing Play snapshot by exact package','【直接观察】','P01;public-research',limit='Earliest retained verified observation, not necessarily earliest public appearance')
 event(slug,pkg,'current_play_last_updated',playdate,'day','Official current listing update field; version rollout not exposed','【直接观察】',slug+'-play',limit='Current requested region US; not paid market evidence or per-version launch date')
 event(slug,pkg,'appbrain_version_update_pair',abdate,'day',abver,'【间接迹象】',slug+'-appbrain',limit='Third-party current version/date claim; may lag or differ from Play')
 event(slug,pkg,'appbrain_recent_download_estimate','2026-11-19','observation_day',str(recent),'【第三方估算】',slug+'-appbrain','approximately 2026-10-20; exact vendor window watermark UNKNOWN','observation 2026-11-19; vendor data cutoff UNKNOWN','Rolling last-30-day total, not daily series, paid installs or attribution; no preceding matched window')
 event(slug,pkg,'appbrain_lifetime_download_estimate','2026-11-19','observation_day',str(total),'【第三方估算】',slug+'-appbrain',limit='Rounded estimate, no uncertainty supplied; not Google official exact installs')
 event(slug,pkg,'store_download_band_observed','2026-11-19','observation_day',band,'【直接观察】',slug+'-play',limit='Store cumulative threshold, not current velocity or paid attribution')
 event(slug,pkg,'apk_and_sdk_static_evidence','2026-11-18','audit_day',f'APK {ver}; MAX {maxver}','【直接观察】','SAMPLE_CATALOG;20;22',limit='Reused previously verified sample; date is audit, not SDK integration or production activation')
 event(slug,pkg,'first_verified_paid_creative','','UNKNOWN','UNKNOWN','【无法确认】','P03;ads-google;ads-meta;ads-tiktok',limit='No exact target advertiser+creative+date record obtained; past advertising coverage UNKNOWN, current access tests not exhaustive for all games')
 event(slug,pkg,'creative_or_paid_market_change','','UNKNOWN','UNKNOWN','【无法确认】','04;20;ALL_FETCHES',limit='Store images are not paid creative records; ranking country is not purchased market')
 event(slug,pkg,'sudden_expansion_change_point','','UNKNOWN','UNKNOWN','【无法确认】',slug+'-appbrain',limit='No sufficiently covered daily/weekly preceding/following comparable series; single rolling total cannot identify changepoint')

event('rotate','com.nebula.rotaterings','historical_distribution_catalog_added','2026-11-10','day','Aptoide 1.2.2 added 01:00:40','【间接迹象】','rotate-aptoide;H01',limit='Catalog ingestion time, not original release; reused signed 1.2.2 sample validated separately')
event('rotate','com.nebula.rotaterings','historical_code_delta_observed','2026-11-18','audit_day','1.2.2→1.2.4 adds country×install-day revenue gate; AF/Firebase versions unchanged in prior audit','【直接观察】','05;H01;R06',limit='No integration/activation date or paid growth onset; cannot infer causal direction')
table('public-evidence/GAME_IDENTITY_REGISTRY.csv',registry);table('public-evidence/EXTERNAL_UA_TIMELINES.csv',timelines)

defaults=dict(multiple_game_ids='NO',complete_zero_revenue_installs='NO',genuine_IAA_revenue='NO',genuine_IAP_revenue='NO',bid_time_feature_availability='UNKNOWN',event_time='UNKNOWN',available_at='ABSENT',opportunity_and_price='NO',D7_D28_install_mature_labels='NO',privacy='Use source-scoped anonymous keys only; no identity resolution or cross-source join',status='STOP_FOR_GAME_VALUE_TASK')
datasets=[]
def ds(ident,name,publisher,url,download,license,license_source,availability,grain,**kw):
 row=dict(dataset_id=ident,name=name,publisher=publisher,official_source_url=url,download_url=download,license=license,license_evidence=license_source,download_verified=availability,sample_grain=grain,**defaults)
 row.update(kw);datasets.append(row)
ds('DS65-01','UCI Online Retail','Daqing Chen / UCI','https://archive.ics.uci.edu/dataset/352/online+retail','https://archive.ics.uci.edu/static/public/352/online+retail.zip','CC BY 4.0','uci-retail official dataset license link','FULL_200_SHA256_AND_541909_ROWS','Invoice line / one retailer',
 genuine_economic_amount='Quantity × UnitPrice in GBP; actual published transaction values, not independently verified cash/net revenue',event_time='InvoiceDate 2010-12-01 to 2011-12-09',
 zero_outcome_scope='Future zero spend among previously observed customers possible; missing non-buyers/install population',
 D7_D28_install_mature_labels='NO; rolling 7/28-day future invoiced amount possible after existing-customer landmark',status='LIMITED_GENERIC_POST_PURCHASE_VALUE',license_current_use='ADMIT_WITH_ATTRIBUTION',multi_source_or_overlap='DS65-02 overlaps this period; not independent replication',
 quality='Actual 135080 CustomerID missing, 5268 exact duplicate rows, 2517 price<=0 and 10624 quantity<=0; API says no missing but file disagrees',
 evidence='audit/ASSET_VERIFICATION.json;uci-retail;uci-retail-api')
ds('DS65-02','UCI Online Retail II','Daqing Chen / UCI','https://archive.ics.uci.edu/dataset/502/online+retail+ii','https://archive.ics.uci.edu/static/public/502/online+retail+ii.zip','CC BY 4.0','uci-retailii official license link','METADATA_ONLY_NOT_BINARY_VERIFIED','Invoice line / same retailer',
 genuine_economic_amount='Documented transaction prices/quantities; file not audited',event_time='Documented 2009-12 to 2011-12',status='HOLD_OVERLAP_NO_ADDITIONAL_GAME_COVERAGE',license_current_use='PERMITTED_BUT_NOT_DOWNLOADED',multi_source_or_overlap='Overlaps DS65-01; never train on one and treat overlapping other as independent test',evidence='uci-retailii')
ds('DS65-03','Open Bandit Dataset repository random/all sample','ZOZO / st-tech official release','https://github.com/st-tech/zr-obp/tree/master/obd','https://raw.githubusercontent.com/st-tech/zr-obp/master/obd/random/all/all.csv','Apache-2.0 within official repository release','obd-root-license;openbandit-repo L345;obd-readme','FULL_200_SHA256_10000_ROWS','Fashion item recommendation exposure',
 genuine_economic_amount='NONE; binary click only',event_time='timestamp 2019-11-24 to 2019-11-30 UTC',bid_time_feature_availability='Exposure-context proxy only; user/item aggregate as-of not certified, omit from first protocol',
 opportunity_and_price='Logged exposures/actions and propensity_score; NO money price/auction win/cost',zero_outcome_scope='9962 non-clicks, not zero-LTV game users',
 status='LIMITED_CONTEXT_CTR_AND_CLICK_OPE',license_current_use='ADMIT_OFFICIAL_REPOSITORY_SAMPLE_ONLY; no external full-dataset license inference',
 quality='README calls probability action_prob; actual CSV uses propensity_score; 10000 rows/38 clicks, uniform p=0.0125, weak precision',
 evidence='audit/OBD_SAMPLE_VERIFICATION.json;obd-readme;obd-root-license;openbandit-repo')
ds('DS65-04','KuaiRand-Pure','Chongming Gao et al. / official repository and Zenodo','https://github.com/chongminggao/KuaiRand','https://zenodo.org/api/records/10439422/files/KuaiRand-Pure.tar.gz/content','CC BY-SA 4.0 embedded archive LICENSE','audit/KUAI_DATA_LICENSE.txt; kuairand-license; kuairand-record portal says CC BY 4.0, stricter embedded license retained','FULL_200_SHA256_ARCHIVE_AND_HEADERS','Kuaishou video exposures/interactions, one app',
 genuine_economic_amount='NONE; play/like/etc are engagement, not revenue',event_time='time_ms; logs Apr08-Apr21 and Apr22-May08 as documented',bid_time_feature_availability='Context/history may be usable; snapshot statistics and same-impression playtime are not as-of certified',
 opportunity_and_price='Random exposure flag and interaction logs; no bid/cost/revenue; exact policy propensities not certified in audited schema',
 status='LIMITED_NONMONETARY_BEHAVIOR_ONLY',license_current_use='ADMIT_UNDER_EMBEDDED_CC_BY_SA4; attribute and comply with ShareAlike for redistributed adaptations',
 quality='Verified 47432272-byte archive and seven CSV headers; no full per-row DQ or model training; tab/policy != game ID',
 evidence='audit/ASSET_VERIFICATION.json;audit/KUAI_DATA_LICENSE.txt;kuairand;kuairand-record')
ds('DS65-05','Criteo Attribution Modeling for Bidding','Criteo AI Lab','https://ailab.criteo.com/criteo-attribution-modeling-bidding-dataset/','http://go.criteo.net/criteo-research-attribution-dataset.zip','CC BY-NC-SA 4.0','criteo-attribution DATA TERMS','LINK_ONLY_NOT_BINARY_VERIFIED','Displayed banner / 30-day anonymized sampled traffic',
 genuine_economic_amount='NO true currency: cost and cpo explicitly transformed; cpo is not game IAA/IAP LTV',event_time='Impression and conversion timestamps documented',
 opportunity_and_price='Shown impressions only; transformed cost/cpo, no complete lost opportunities or causal price response',status='STOP_COMMERCIAL_SCOPE_AND_GAME_LABELS',license_current_use='NC purposes only; current commercial growth R&D not presumed eligible; no dataset download/training',
 evidence='criteo-attribution L47-L90 and L114 onward')
ds('DS65-06','Criteo Uplift v2.1','Criteo AI Lab','https://ailab.criteo.com/criteo-uplift-prediction-dataset/','http://go.criteo.net/criteo-research-uplift-v2.1.csv.gz','CC BY-NC-SA 4.0','criteo-uplift DATA TERMS','LINK_ONLY_NOT_BINARY_VERIFIED','Randomized treatment/control conversion outcome',
 genuine_economic_amount='NONE certified; conversion/visit/treatment binary outcomes',status='STOP_COMMERCIAL_SCOPE_AND_GAME_LABELS',license_current_use='NC scope unresolved for current use; no dataset training/download',
 evidence='criteo-uplift')
ds('DS65-07','iPinYou RTB original competition logs','iPinYou; Weinan Zhang official research integration','https://github.com/wnzhang/make-ipinyou-data','http://bunwell.cs.ucl.ac.uk/ipinyou.contest.dataset.zip','Original dataset license not established; integration code Apache license is insufficient','ipinyou-repo;ipinyou-license;ipinyou-original','ORIGINAL_PUBLIC_LINK_CONNECT_TIMEOUT_STOP_NO_BYPASS','RTB log/campaign; original data not obtained',
 opportunity_and_price='README documents winning price/click; actual file not verified; no game install LTV',status='STOP_LICENSE_AND_ACCESS',license_current_use='NOT_ADMITTED',evidence='ipinyou-repo;ipinyou-license;ipinyou-original')
ds('DS65-08','mobile_games_LTV / LTV Lens repository','rizz045 third-party project author','https://github.com/rizz045/mobile_games_LTV','NO_PUBLIC_RAW_EXPORT_ESTABLISHED','No dataset reuse license established in audited README/root listing','mobile-ltv-files;mobile-ltv-readme;ltv-data-audit','CODE_AND_CLAIMS_ONLY_NO_VERIFIED_RAW_DATA','Claims one casual-game event log; no verified export',
 genuine_economic_amount='README claims revenue; no raw dataset/file/ownership/usage authority verified',status='STOP_NO_DATA_OR_DATA_LICENSE',license_current_use='NOT_ADMITTED; GitHub public visibility is not dataset authorization',evidence='mobile-ltv-files;mobile-ltv-readme;ltv-data-audit')
ds('DS65-09','Mobile-game hierarchical probabilistic forecast replication code','Yu-Chin Chen / Zenodo official deposit','https://zenodo.org/records/24211987','https://zenodo.org/api/records/24211987/files/code_R1_v1.zip/content','Code MIT; event calendar CC BY 4.0; commercial market panel NOT redistributable','audit/GAME_FRAMEWORK_README.md L13-L27/L101; embedded LICENSE','FULL_CODE_ARCHIVE_200_NO_VALUE_PANEL','Two-game monthly country/platform panel schema only; included public event calendar',
 multiple_game_ids='Only public calendar has PoGO/Pikmin; value panel not supplied',genuine_economic_amount='NO public revenue/download panel; monthly estimates require own vendor license',
 status='STOP_NO_PUBLIC_VALUE_PANEL',license_current_use='Code/calendar reusable; cannot inherit commercial panel rights from MIT',
 quality='Archive inspection overturns tempting abstract/title: explicitly code only, no data or results derived from licensed export',
 evidence='audit/GAME_CODE_DATA_GAP.json;audit/GAME_FRAMEWORK_README.md;zenodo-ltv-paper-code')
# Uniform keys make CSV parse unambiguous.
keys=[]
for row in datasets:
 for k in row:
  if k not in keys:keys.append(k)
table('public-experiments/DATASET_CATALOG.csv',[{k:row.get(k,'UNKNOWN') for k in keys} for row in datasets])

admissions=[
 dict(experiment='E0',requested_task='安装前上下文/价值排序基线',required='全广告机会、bid_time、as-of上下文、安装/未安装分母、成熟收入标签',candidates='DS65-03; optional DS65-04',status='LIMITED',full_requested_task='STOP',allowed_alternative='曝光上下文→点击/参与，非安装前LTV',time_leakage='No available_at; use only timestamp/position/item context fixed before decision; omit post-exposure outcome/history snapshots',selection_bias='Logged recommendation exposures, not mobile ad bid opportunities; action/position and logging-policy support',privacy_license='DS03 official repo Apache sample; DS04 embedded CC BY-SA4; source-scoped anonymous keys only',allowed_metrics='Click logloss/Brier/calibration; click-policy IPS with valid support and ESS',forbidden_metrics='pInstall validation, D7/D28 game LTV error, high-value-game recall, Axon/Vector ranking gain',minimum_new_data='All-game-install opportunities with mature true revenue and as-of lawful features'),
 dict(experiment='E1',requested_task='同App历史真实价值学习',required='全安装用户含零收入、安装时间、逐笔真实IAA/IAP、成熟7/28天、available_at',candidates='DS65-01',status='LIMITED',full_requested_task='STOP',allowed_alternative='单零售商已观察客户landmark后7/28天发票金额预测；不是安装cohort LTV',time_leakage='History strictly before landmark; labels through horizon; embargo maturity; no future counts; available_at absent limits production claim',selection_bias='Previously observed buyers only, missing never-buyers/installs; missing CustomerID selection; returns/censoring',privacy_license='CC BY4 attribution; do not reidentify or join customer keys across datasets',allowed_metrics='Rolling invoiced-GBP MAE/RMSE/calibration/zero-tail recall with temporal CI and precise amount semantics',forbidden_metrics='Game IAA/IAP D28 LTV, net profit/cash ROAS, full-install population performance',minimum_new_data='Licensed mature single-game all-install event export with verified revenue and timing'),
 dict(experiment='E2',requested_task='跨游戏聚合cohort先验',required='>=2真实游戏ID、同口径真实价值、目标游戏冷启动时间窗、cohort粒度',candidates='NONE; DS09 only public calendar, no panel',status='STOP',full_requested_task='STOP',allowed_alternative='NONE; do not relabel countries/campaigns/videos as games',time_leakage='Target-test labels cannot enter source statistics or app similarity',selection_bias='No multi-game value population established',privacy_license='No cross-app personal join; licensed aggregate data still required',allowed_metrics='None for current data',forbidden_metrics='Cross-game value transfer gain or Axon/Vector cold-start improvement',minimum_new_data='Licensed multi-game standardized mature value cohorts with availability dates'),
 dict(experiment='E3',requested_task='跨游戏共享模型与目标游戏适配',required='多游戏真实训练样本、统一价值定义、held-out game、固定适配样本量及训练预算',candidates='NONE',status='STOP',full_requested_task='STOP',allowed_alternative='NONE',time_leakage='No test-game future statistics, labels, normalizers or tuning',selection_bias='No game ID/value population; country transfer is not game transfer',privacy_license='Aggregate/parameter sharing still requires legitimate data rights; no natural-person graph',allowed_metrics='None for current data',forbidden_metrics='Shared-model gaming LTV benefit, identity-feature incremental gain',minimum_new_data='Authorized >=3 games preferably for LOOG with mature as-of value records'),
 dict(experiment='E4',requested_task='固定分数的预算/报价策略比较',required='机会集合、真实竞价/支付价格、胜负、记录策略/propensity、被选与未选结果可识别、成熟价值',candidates='DS65-03 for click policy only; DS05 transformed cost/NC not admitted; DS07 missing',status='LIMITED',full_requested_task='STOP',allowed_alternative='Fixed-score recommendation click-policy OPE; NO monetary budget/bid/ROAS',time_leakage='Train/freeze score before validation/test days; same opportunities and action support across policies',selection_bias='Only displayed recommendations; marginal position propensity not joint-slate probability; sparse 38 clicks',privacy_license='Apache official sample; no production traffic or real identity lookup',allowed_metrics='IPS/SNIPS click value, DR if outcome model cross-fit, ESS/overlap, wide block bootstrap intervals',forbidden_metrics='True or causal monetary ROAS, marginal profit, auction win simulations labeled real, Axon/Vector policy gain',minimum_new_data='Authorized full opportunity/cost/propensity/mature revenue log or randomized budget experiment'),
]
table('public-experiments/EXPERIMENT_ADMISSION_MATRIX.csv',admissions)

license_doc=r'''# 数据许可、可下载性与真实标签审计

2026-11-19。本轮检查9个候选，**3个已实际取得并核验的数据发行物允许开展受限通用研究**：UCI Online Retail、官方仓库Open Bandit小样本、KuaiRand-Pure。没有一个同时满足本项目手游D7/D28真实收入、全安装分母、多游戏或真实竞价收益的准入要求。另一个下载成功的是代码包，不算收入数据集。

## 1. 实际取得与可用范围

| 编号 | 下载与许可证据 | 当前准入边界 |
|---|---|---|
| DS65-01 | UCI352官方页CC BY4；23715478字节ZIP、541909行Excel，原包SHA256见[ASSET_VERIFICATION](audit/ASSET_VERIFICATION.json) | 可做已观察零售客户的未来发票金额预测；Quantity×UnitPrice为GBP，不是IAA/IAP、验真银行到账或游戏净LTV。允许使用需署名，不作个人识别或跨源join |
| DS65-03 | ZOZO官方st-tech/zr-obp仓库含obd样本，项目明示Apache2；实际下载random/all/all.csv、10000行，见[样本核验](audit/OBD_SAMPLE_VERIFICATION.json) | 准入**仓库发行样本**，保留许可/版权及修改说明；不把代码许可证外推外部26M全量ZIP。可做点击/策略OPE，不是收入或竞价 |
| DS65-04 | Zenodo官方发行47432272字节tar.gz实际可下载；内置[LICENSE](audit/KUAI_DATA_LICENSE.txt)为CC BY-SA4，仓库亦为SA4 | portal元数据写CC BY4，**不据此丢弃归档内ShareAlike条件**；本轮采用内置较严格条款，保留出处、修改说明及适用再分发要求。只做非货币行为研究，无游戏收入 |

公开匿名化键仅在本数据集内分组；不得反查、跨数据集匹配或重建自然人身份。本轮结构审计不导出用户行值、账号/广告ID或评论者姓名；下载的研究数据保留发布方匿名键，不是访问真实账号。原始公开发行物只读保存，审计输出是schema/聚合质量而非个人画像。

## 2. 三个只有看真实文件才发现的风险

1. **UCI metadata不替代数据质量。**API称has_missing_values=no，但实际CustomerID缺135080行，Description缺1454行；完全相同行5268条，非正单价2517条、非正数量10624条。相同行不一定是重复经济事件，缺少行幂等键时不得盲删；取消/负数不是自动清洗成0，需定义退款和发票口径。不得悄悄只留付费高价值者。
2. **OBD文档与文件字段有版本差异。**README称`action_prob`，实际为`propensity_score`；本样本2019-11-24—30，仅38点击，p=0.0125。不能伪造真实金额或声称稳定的模型增益；静态用户/视频统计的available_at未证，默认排除以免未来泄漏。
3. **KuaiRand的portal许可和包内许可不同。**实际归档LICENSE和6份CSV表头已核；保留SA义务。`play_time_ms`、`is_click`、`long_view`都是参与信号；tab/policy不是不同游戏。曝光后的playtime不能当同次曝光前特征，汇总statistic表也不能未经as-of审计入模。

## 3. 没有通过的候选

| 编号 | 真实取得了什么 | 停止原因 |
|---|---|---|
| DS65-02 Online Retail II | 官方元数据/许可与下载链接；未下载二进制 | 与352同一商家且时间重叠；不提供跨游戏，也不能当独立复制验证。为避免重复下载，本轮未取另一个大包 |
| DS65-05/06 Criteo | 官方完整数据定义与CC BY-NC-SA4条款、公开链接；未下载数据 | 当前商业增长研发不能擅自视为非商业用途，暂停下载/训练；Attribution的cost/cpo还明确是transformed，不是真实币种；二者无手游IAA/IAP标签。不是“许可不明”，而是用途限制明确但当前适用未获确认 |
| DS65-07 iPinYou | 作者整合仓库README/代码LICENSE；原UCL公开地址连接超时 | 代码Apache不自动授权原竞赛数据；原数据未取得，不绕过访问限制，也不从二手镜像推定数据许可 |
| DS65-08 mobile_games_LTV | 第三方仓库声称2100万游戏事件、代码/分析文档；根目录无已核验原始数据和数据许可 | GitHub公开不是数据授权，README效果不是本地真实样本；未取作者个人文档或联系作者，不算可用游戏数据 |
| DS65-09 Zenodo游戏预测框架 | 下载189171字节代码ZIP；README L13—19明确商业月度估计不可再分发、包内code only；有两游戏公共事件日历 | **MIT只授权代码，日历CC BY4不提供收入标签**。标题/摘要看似多游戏收入可复现，实际商业panel缺失；即使有月度总额也不是用户D28安装标签。见[缺口原文](audit/GAME_CODE_DATA_GAP.json)与[README](audit/GAME_FRAMEWORK_README.md) |

本轮候选搜索使用官方UCI/Criteo/ZOZO仓库、Zenodo/DataCite API和公开仓库；Bing宽查询返回无关词典结果，不算覆盖完整。候选数量和成功下载量都不是研究质量；**可执行手游价值预测数据集数仍为0**。未登录Kaggle/商业情报后台，未绕过登录、挑战、支付或权限。

## 4. 保留与再分发

原始数据包位于audit目录，不修改，不向报告附个人行；公开分享衍生数据前按具体许可复核署名、NOTICE/修改及SA条款，不直接把本地全部audit目录推送到外部。许可不授予再识别、商标或额外隐私权；本轮不执行真实广告或归因请求。

逐候选字段和准入结论见[DATASET_CATALOG.csv](DATASET_CATALOG.csv)，E0—E4见[EXPERIMENT_ADMISSION_MATRIX.csv](EXPERIMENT_ADMISSION_MATRIX.csv)。本轮没有训练模型、报告增益或把合成数据替代真实标签。
'''
write('public-experiments/DATASET_LICENSE_AUDIT.md',license_doc)

protocol=r'''# 通过受限准入的实验方案：不启动66号训练

2026-11-19。E0/E1/E4仅允许下列**重新限定问题的通用替代实验**；原始手游安装前LTV/同App安装收入/真实预算竞价问题均STOP。E2/E3无合格多游戏价值数据，STOP。方案不是实验结果，当前无模型精度、增益、ROAS或因果利润输出。

## A. E1受限替代：已观察零售客户的未来7/28天发票金额

数据：DS65-01，CC BY4。问题定义为`E(未来(t,t+7/28天]发票金额 | t前已观察该客户的历史)`，不是自安装D7/D28，也不是全访问用户或游戏付费概率。只在数据源内使用匿名CustomerID分组，禁用ID本身作为模型特征，不外部匹配。

1. **样本/金额：**全量已观察客户在固定landmark进入分母，未来未购买者为0；CustomerID缺失行不可随意补成独立客户。记录缺失剔除比例及国家分布变化。Quantity×UnitPrice按GBP，销售额与签名发票净额分为两个任务；取消/负数单独核验。没有验单/现金对账不称真实净利润。完全重复行因缺经济行键，保留/去重两种敏感性口径，不能任意选择使结果更好者。
2. **时间切分：**训练landmark为2011-01—04、验证2011-06、测试2011-08，全部目标窗口成熟后才评分；各训练标签结束早于下一段预测时点，留足28天隔离。每个客户/landmark的统计只读t前记录；测试模型/参数冻结，晚期数据不用于归一化、缺失填补或阈值选择。数据开头历史左截断显式标注，末尾不足28天标签不用。
3. **基线与预算：**训练期全局均值/国家先验→同客户历史RFM简单线性/两阶段零值+金额模型→轻量树模型，固定样本、特征窗口、随机种子、调参次数和CPU预算。聚合统计与个体历史分开消融，但这是**同商家历史**，不叫跨游戏共享参数。数据无available_at，event-time offline假设必须单列；不能认证生产bid-time。
4. **评价：**MAE/RMSE、均值校准、分桶校准、Top10%未来发票价值召回、零未来金额/长尾单列；按国家及日历cohort分层，小层不排名。对同一固定测试样本配对bootstrap，按客户与日历块检查依赖，95%区间；不预设增益，报告负迁移与宽区间。
5. **禁止：**IAA/IAP游戏D28准确率、全安装高价值召回、广告平台训练效果、净利润/真实ROAS或跨App身份增益。没有机会/成本不能做真实扩量模拟。

## B. E0/E4受限替代：曝光上下文点击与固定分数的点击策略OPE

数据：DS65-03官方仓库sample Apache2。10000曝光、38点击，仅7天，适合复核评估方法/有限探索，样本不足以作稳健价值结论。选择item/position是推荐，不是RTB报价；无安装与收入。

1. **时间外切分：**2019-11-24—27训练、28验证、29—30测试；先确认各段动作和位置有共同支持。不足有效点击/ESS即停止优势结论。相同机会、分数与动作集合用于所有策略。只使用决策时曝光上下文，事后点击、未来亲和度和未证as-of用户统计禁止作为特征。
2. **分数冻结：**可先预注册常数/仅训练期item CTR平滑分数，验证期定规则后冻结。所有策略使用同一分数和同一测试集；数据不变时不再以换模型解释策略差异。本轮不训练或执行OPE。
3. **识别与指标：**核对实际`propensity_score`而非README旧名；按位置conditional action估计IPS/SNIPS，DR需交叉拟合结果模型；不把单位置边际propensity相乘当已知联合slate概率。报告overlap、ESS、权重分布、截断敏感性、按日块bootstrap区间及直接回放/IPS差别。无支持的目标动作不得外推。
4. **预算停止边界：**没有货币价格/完整未选竞价机会，不能评估CPM/CPI、bid shading、现金pacing、边际ROAS或利润。曝光配额与模型自定义价格不是实际广告预算；若另用合成值，只验证代码和会计，不报告模型或平台收益增益。
5. **KuaiRand补充：**DS65-04可研究随机曝光的非货币参与，但其发布静态统计需逐字段as-of审计、分布/propensity需另核。它不补安装/货币标签，故本轮不为它启动新模型。CC BY-SA4义务保持。

## C. E2/E3：停止，不用同类数据假装多游戏

当前无多游戏真实玩家收入/成熟cohort数据。国家≠游戏、campaign≠游戏、KuaiRand tab≠游戏、公共两游戏事件日历≠两游戏用户价值样本。不构造伪game_id来通过leave-one-game-out。

恢复后才采用：按目标游戏留出、源游戏时间水位严格早于目标预测时点；测试游戏的未来均值/分位数/相似度不进入聚合；相同适配样本量/训练预算，对照目标单游戏、源聚合先验、共享参数+适配，并分别消融；包含零收入与长尾、国家/游戏/覆盖层及配对区间。需要合法作用域，不必须跨App个人ID。

## D. 两条证据线不自动相连

公开游戏估算的近期下载集中度，不能验证上述零售/推荐模型；通用实验即便有真实增益，也不能证明四款使用该模型、Axon/Vector更优或利润提高。66号是否开展由本轮审计后的下一轮决策确定，本轮不越过准入开展训练。
'''
write('public-experiments/EXPERIMENT_PROTOCOL.md',protocol)

competition=r'''# 四款扩量时间线：竞争性解释，不归因模型盈利

2026-11-19。四款身份均按包名和开发者核验；近期量的唯一新增来源是AppBrain滚动30天估算。未取得可比较的前后两个窗口或连续历史榜单，因此**突然扩量起点UNKNOWN，任何平台的利润贡献UNKNOWN**。不是没有投放，而是公开覆盖不足。

| 游戏 | H1 素材/市场变化 | H2 价值优化变化 | H3 变现/留存变化 | H4 归因/外部市场变化 |
|---|---|---|---|---|
| Car Race | 无可核验付费创意/地区时间序列，无法支持或反驳；商店截图不是广告 | 既有ILRD与国家阈值代码存在，但无启用时点/campaign记录；无法区分 | 无同类cohort收益/留存前后数据；无法区分 | Play更新11-12与AppBrain1.349.0/11-04不一致，证明元数据不能强拼，不证明下载估算上涨原因 |
| Meowdoku | 近30天估930万是活动线索，不能说明换了素材/市场；需要稳定creative ID和日期/地区 | GRT/时间窗规则已存在，缺上线表与实际优化目标；不能把估算活跃解释成模型改进 | 无收入/广告策略/留存历史；高下载也可能来自自然传播 | Play11-16与AppBrain1.25.0/11-13及本地1.25.1存在滞后/分区可能，但原因未知；商店推荐或外部需求未证 |
| Rotate Rings | 近30天估850万、约占估算累计53.1%，值得追踪，但不能定位素材或渠道变化 | 1.2.2→1.2.4增加国家×安装日收入事件是实际变化；首次生产启用和下载变点均未知，因果不可判 | 真实变现回调存在，不能证明每用户收益/留存改善；亦不能反驳 | 发布时间/分发入库/审计时间不同；排名国家不是投放国家，季节性/商店推荐也未区分 |
| Jewel Coloring | 近30天估80万，未取得付费素材/地区变化；不是“从未买量” | AdWorth90默认规则是静态设计，无热更时序/活动目标；不证明近期优化升级 | 价格/广告策略可能改变收益，但无成熟cohort对照；未知 | 当前更新时间一致9-17，只能说明当前字段一致；不能排除归因口径或市场变化 |

表内代码锚点复用[05号](../05_历史版本策略演进.md)、[20号](../20_Axon实际事件调用链.md)、[49号](../49_行为价值事件端到端调用链.md)、[64号](../64_普通游戏盈利跃迁最终机制判断.md)；新增外部来源按包名见[身份表](GAME_IDENTITY_REGISTRY.csv)和[时间线](EXTERNAL_UA_TIMELINES.csv)。除Rotate版本变化是代码事实外，四类解释均未识别出独立因果贡献。

## 如何区分，而不是继续凑证据

- **H1：**合法取得同包名的日期化素材、落地页和可核验展示市场，再与连续下载/排名前后窗口对齐。数量只能表示被采集素材量，不能代表花费；商店图变化不自动表示广告变化。
- **H2：**需要广告主授权目标、映射/启用日志、模型/策略变更与成本收益对照。SDK版本或收入规则变化只能作为候选解释，不能作为优化启用证据。
- **H3：**需要固定获客cohort的广告机会/收益/留存时序或变现随机实验；下载曲线不能推导ARPU或eCPM。
- **H4：**需要版本化归因窗口/来源、商店推荐与外部市场事件。只有报告指标跳跃、独立净收入不变会反驳“盈利改善”；当前没有这些数据。

## 时间关系的硬限制

AppBrain的30天窗口与11月版本更新时间相交，只证明“同一广义日历期”，不证明更新先于增长或反之。Aptoide的1.2.2 added=2026-11-10是入库；1.2.4当前商店更新=11-16；本地差分审计=11-18。缺少历史滚动发布、生效表和增长起点，不能确定收入规则改变的因果顺序。Meow旧版目录和Car更新日期的冲突必须保留，不强行校正。

公开搜索未得到某条广告不表示当时没有广告。此轮Google查询Rotate包名、Meta/TikTok查询Meow，结合旧研究覆盖；没有宣称本轮对四款所有国家/时间/平台进行了穷尽查询。Meta403、Aptoide版本页403停止；Google/TikTok仅壳或通用页，无creative/advertiser/date配对。AppBrain历史提示登录，未绕过。营销文案“strong momentum”不单独证明突增。
'''
write('public-evidence/COMPETING_EXPLANATIONS.md',competition)

stop=r'''# 第65号停止条件与下一轮准入

2026-11-19。本轮停止在身份与数据准入审计，不启动66号训练或无界时间线深挖。

| 条件 | 当前结果 | 决定 |
|---|---|---|
| 包名/开发者无法精确对应 | 四款当前Play与AppBrain canonical均已对应；其他同名产品不纳入 | 只有已核四包继续，未知来源不拼接 |
| 历史排名/下载无前后覆盖 | 四款只有单次滚动估算和当前榜单；历史登录/覆盖缺失 | **STOP突然扩量/变点结论**，可以保留当前活跃估算 |
| 付费创意无稳定ID/日期/产品落地页 | 尚无匹配记录；403/壳/通用页不算证据 | **UNKNOWN首次投放/素材变化**，不解释为无广告 |
| 数据许可不覆盖用途 | Criteo NC不默认为当前商业研发许可；iPinYou/第三方游戏原始数据权未核 | 相应数据STOP下载/训练；不能用代码许可替代数据许可 |
| 无真实游戏价值标签 | 3个可用通用数据发行物均无IAA/IAP安装标签 | **STOP游戏D7/D28预测精度和模型优势** |
| 无多游戏收入 | 日历/视频/tab/国家/campaign不能代替game ID和收入 | **STOP E2/E3**，不合成伪game ID |
| 无真实机会、价格和可识别选择机制 | OBD有曝光/propensity/点击，无货币；Criteo价格变换且受NC限制 | **STOP真实竞价/预算/边际ROAS**；E4仅点击策略OPE受限替代 |
| 需要登录、反爬绕过或授权账号 | Meta/Aptoide版本页403；AppBrain历史需登录；UCL超时 | 不绕过、不无限重试；记录缺失和实际查询范围 |
| 只有营销案例/代码包 | 第三方LTV项目声称有数据但未提供许可原始样本；Zenodo框架明确商业panel不可再分发 | 不把案例/代码/合成panel计作真实游戏数据 |

## 值得恢复的最小材料

**外部线：**先尝试合法、已公开且精确包名对应的Meow/Rotate至少前后各4周、同国家/榜单口径的日/周序列，带数据日/采集日/估算定义；付费素材若可得需creative ID、advertiser、落地包名、展示时间/地区。若只有单点或商业登录，不扩大旁路搜索，停止。未来每日采样能建立未来序列，不能回填过去，未经另行任务不启动自动监控。

**实验线：**要回答手游价值问题，优先取得合法公开或授权的全安装分母、零收入、逐笔IAA/IAP及退款、install/event/available时间和成熟28天；要做迁移需多游戏同口径，预算需全机会/成本/策略支持。公开匿名键仅用于本数据范围，不构建跨App个人图谱。

当前只有E0/E1/E4通用替代的LIMITED方案，不是原任务GO；若下一轮选择方法验证，可从真实发票金额的零值/长尾校准或点击OPE小样本开始，明确外推边界。只有合成数据时只测代码与会计恒等式，不报告模型增益。
'''
write('public-evidence/STOP_CONDITIONS.md',stop)

main=r'''# 四款游戏公开扩量证据与价值预测实验可行性审计

2026-11-19 · 第65号。本轮更换方法：A线只看外部产品与扩量痕迹，B线只审计许可明确的公开实验数据；不做SDK逆向、泛化模型架构搜索或生产请求。

**结果：四款身份全部核验，四款都有近期下载量的第三方估算，但0款取得足以确定“突然扩量起点”的连续历史覆盖。9个候选中，3个数据发行物实际下载、许可可支持受限通用研究；0个满足手游真实D7/D28收入、跨游戏价值迁移或安装前价值排序的完整要求。E0/E1/E4仅LIMITED替代，E2/E3 STOP；没有原始手游实验获得GO。**

没有授权投放成本、成熟游戏cohort或平台训练数据。本轮不执行大规模或小规模模型训练，不报告模型增益、真实ROAS或两家平台相对优胜；停止于65号审计。

## 1. 身份消歧与版本时间：四款均可可靠对应

| 游戏 / 精确包名 | 当前Play开发者 | 既有APK证据 | 当前版本/更新字段 |
|---|---|---|---|
| Car Race / `com.dino.race.master` | iKame Games - Zego Studio | 原版1.348.2 / MAX13.6.4 | AppBrain称1.349.0/11-04；当前Play更新11-12；不能强行视为同次发布 |
| Meowdoku: Brain Puzzle Games / `com.oakever.meowdoku` | Oakever Games | 1.25.1 / MAX13.2.0 | AppBrain仍1.25.0/11-13；Play11-16，保留目录滞后/分区等未知 |
| Rotate Rings / `com.nebula.rotaterings` | Nebula Studio（原页双空格） | 1.2.2与1.2.4，同签名旧证据；新版MAX13.6.2 | AppBrain1.2.4/11-16，Play11-16；日期一致也不证明实际用户覆盖 |
| Jewel Coloring / `color.number.paint.pixle.art.sort.jigsaw` | TaTa Game Technology Limited | 1.24.1 / MAX13.6.3 | AppBrain1.24.1/9-17，Play9-17 |

【直接观察】新Play JSON-LD的名称、author与包名URL；AppBrain canonical也含精确包名。既有样本SHA256/版本只复用[SAMPLE_CATALOG](SAMPLE_CATALOG.json)，不修改/重复下载APK。表内SDK是既有审计状态，不是本轮推定接入日期。[身份表](public-evidence/GAME_IDENTITY_REGISTRY.csv)、[原始来源目录](public-evidence/EXTERNAL_SOURCE_CATALOG.md)

**首次出现日期必须分层：**本地已核验公开商店观察可追至2026-11-18，并不代表实际首次上线。AppBrain称Car自2021-09、Meow自2026-04、Rotate自2026-07、Jewel自2026-02可用；这是【间接迹象】历史元数据声明，未独立核原始发布。当前“Updated on”也不是版本首发/SDK上线/远程规则生效日期。同名赛车、转环、猫谜题或填色产品一律不合并。

## 2. 外部扩量：出现了活动线索，尚未证明突然跃迁

| 游戏 | AppBrain累计估算 | AppBrain近30天估算 | 近30天占累计（派生比例） | 最终等级 |
|---|---:|---:|---:|---|
| Car Race | 3.8亿 | 360万 | 约0.95% | 【第三方估算】近期活跃；突然扩量UNKNOWN |
| Meowdoku | 3600万 | 930万 | 约25.8% | 【第三方估算】近期量较集中，值得追踪；突然扩量UNKNOWN |
| Rotate Rings | 1600万 | 850万 | 约53.1% | 【第三方估算】近期量最集中，值得追踪；突然扩量UNKNOWN |
| Jewel Coloring | 1400万 | 80万 | 约5.7% | 【第三方估算】近期活跃；突然扩量UNKNOWN |

原始来源：四个按包名跳转到canonical的AppBrain页面，采集2026-11-19；页面原文和response哈希、聚合元数据片段见[来源目录](public-evidence/EXTERNAL_SOURCE_CATALOG.md)。比例是四舍五入估算数的算术，不是独立观测，也不等于增长率。**不能将30天量/累计量解释成相对上月增长，或据此宣称四款都在突然扩量。**不确定区间、估算算法/数据截止水位未公开。

Google Play当前下载档位分别为100M+、10M+、10M+、10M+，属于【直接观察】商店累计门槛；不能与AppBrain估计混成日度数据。当前榜单/摘要不构成历史排名，也不代表付费投放国家或实际盈利。

### 实际覆盖与缺失

- **下载/排名：**本轮每款只取得一个页面快照和“last 30 days”总量，约对应观察前30天，但供应商准确起止水位未知。未取得前一相同窗口、逐日下载或连续国家榜单；AppBrain历史提示登录，停止。商店“自某月上线”的声明不是从该月起完整历史覆盖。
- **真实付费素材：**仍无同包名稳定creative ID＋广告主＋日期/地区的完整记录。复用旧研究的五款访问边界；本轮额外Google查询Rotate包名、Meta/TikTok查询Meow。Meta403，Google/TikTok为壳/通用页，无可核匹配，不声明穷尽全部平台或国家。
- **版本：**Rotate Aptoide公开API仍给1.2.2 added=2026-11-10 01:00:40，历史版本页403即停止；这是入库日期。既有1.2.2→1.2.4差分证明新增国家×安装日收入事件，AF/Firebase版本在该跨度仍相同；**没有生产生效日期，不能和滚动下载窗口建立因果顺序**。[05号](05_历史版本策略演进.md)
- **素材/国家/运营变化：**当前商店图文不能冒充历史付费素材。没有完整更新/实验/国家预算日志，无法确认重大运营变化或是哪一网络导量。

完整事件表（含UNKNOWN空日期和覆盖边界）见[EXTERNAL_UA_TIMELINES.csv](public-evidence/EXTERNAL_UA_TIMELINES.csv)。没有检索到广告≠没有投放，排名上升≠盈利，素材数量≠花费，估算下载≠真实归因安装。

## 3. 时间关系与四类竞争解释

每款均比较H1素材/市场、H2价值优化、H3变现/留存、H4归因/外部市场，见[逐案矩阵](public-evidence/COMPETING_EXPLANATIONS.md)。

**目前能支持的只有：**身份明确、当前近期量估算存在、部分版本元数据/代码发生变化。Rotate是唯一已有签名一致的原包历史差分案例，但缺增长变点和规则生效日，无法确定谁先谁后；Meow与Car当前目录/Play时间冲突进一步阻止强拼时间线。

**目前不能辨识：**下载来自新素材、自然传播、商店推荐、国家组合、预算扩大、收入目标，还是其他原因；不能据SDK接入或规则精细度判断Axon/Vector利润贡献。H1—H4均未获可区分的因果验证，也未整体被否定。

## 4. 公开数据：看到了真实文件，也看到了不能做什么

| 数据 | 许可/实际取得 | 有用之处 | 缺失的关键条件 |
|---|---|---|---|
| DS65-01 UCI Online Retail | CC BY4；实际下载ZIP并读541909行 | 真正的交易数量、GBP单价和时间，可做已观察客户未来7/28天发票金额 | 无游戏/安装/全访问零收入分母，无as-of到达时间、广告成本；不是手游LTV |
| DS65-03 Open Bandit官方仓库样本 | 官方项目Apache2，限该repo发行样本；实际10000曝光、38点击 | 有曝光时间、动作/位置及真实logging propensity，可研究点击策略OPE | 无安装、价格、收入或完整RTB机会；38点击不足支撑稳健效果结论 |
| DS65-04 KuaiRand-Pure | 实际47432272字节归档；包内CC BY-SA4 | 非货币行为/随机曝光，具时间和历史线索 | 一款视频App；无IAA/IAP/游戏ID/广告价格；静态统计as-of未证 |

这是**3个可用于限定研究的数据发行物，不是3个手游价值数据集**。许可均需按范围保留署名/版权、修改说明及适用再分发条件；不收集自然人身份或跨源匹配。KuaiRand门户写BY4，但归档LICENSE为BY-SA4，本轮保留包内较严格条款，不无条件放宽。

其余6个候选：Online Retail II与352同一商家并重叠、未重复下载；Criteo两集有NC限制且无手游真实价值，当前商业研发不擅自认作符合；iPinYou原地址超时且原数据许可未核；第三方mobile_games_LTV仅有数据声称、无核验原始出口和数据授权；Zenodo多游戏收入预测框架虽MIT代码可下，**README明确收入panel为不可再分发商业估计，发行物只有代码与公共事件日历**，不能拿摘要当真实数据。

【直接观察】UCI API声称无缺失，但实际CustomerID缺135080行；还存在5268完全相同行与退款/非正金额问题。OBD README的`action_prob`在实际CSV叫`propensity_score`。这些差异说明只读摘要/文档不足以准入。

逐候选必需字段、可下载状态、许可、零收入范围、价格、时间与成熟标签均见[DATASET_CATALOG.csv](public-experiments/DATASET_CATALOG.csv)及[许可审计](public-experiments/DATASET_LICENSE_AUDIT.md)。原发行物SHA256与结构统计见[audit](public-experiments/audit/ASSET_VERIFICATION.json)，未运行下载包代码。

## 5. E0—E4准入结论

| 实验 | 状态 | 现在允许的受限问题 | 必须停止的原目标 |
|---|---|---|---|
| E0 安装前上下文 | **LIMITED** | OBD曝光上下文→点击，时间/动作支持审计后仅通用方法 | 安装概率、安装前真实D28价值排序；没有安装/收入标签 |
| E1 同App历史价值 | **LIMITED** | UCI已观察零售客户→landmark后7/28天发票金额 | 手游全安装IAA/IAP D7/D28价值，未买者/未安装分母不能补造 |
| E2 跨游戏聚合先验 | **STOP** | 无 | 无多游戏真实价值cohort；不得把国家/视频/广告campaign当game_id |
| E3 跨游戏共享模型 | **STOP** | 无 | 无多游戏收入/适配样本；两游戏公共日历不是收入panel |
| E4 固定分数预算/报价 | **LIMITED** | OBD固定分数的点击策略IPS/SNIPS等OPE，满足支持假设才算 | 无真实价格/机会/收入，不报告货币预算、真实/因果竞价ROAS或利润 |

**原始手游问题全部未通过GO。**LIMITED表示问题已经缩小到别的、可解释的研究场景，不代表原问题“差一点就验证”。模型本轮尚未训练，表中允许指标不是已产生结果。[准入矩阵](public-experiments/EXPERIMENT_ADMISSION_MATRIX.csv)

## 6. 下一轮可执行方案与优先级

[实验协议](public-experiments/EXPERIMENT_PROTOCOL.md)已定义时间外切分、28天标签成熟/隔离、同数据量/训练预算、零值/长尾校准、国家层及bootstrap；OBD限定单位置/动作支持和稀疏点击，不能把边际propensity当联合slate概率。available_at普遍缺失，不能认证生产bid-time。

**下一轮最值得先做外部线的有界补证：Rotate，其次Meow。**它们有较高近期下载集中度，Rotate另有可核历史版本变化。只寻找合法公开、精确包名、至少前后各4周的同口径历史量/排名及日期化素材；没有覆盖或遇登录即停，不重复SDK或架构搜索。若只能未来连续采样，应明确它只建立未来基线，不能重建此前扩量。

**若选择66号方法实验：**E1零售未来发票金额是现有最贴近真实“金额预测”的限定任务；E4点击OPE可检验评估纪律，但不是预算/ROAS。二者只能验证通用机制，不能证明跨游戏迁移、身份增益或Axon/Vector生产效果。E2/E3与真实竞价利润等待合格公开或授权游戏/机会数据，不用合成panel填结果。

## 7. 两条独立证据链与最终回答

```mermaid
flowchart LR
 A[精确包名/开发者] -->|直接观察| B[公开版本与当前元数据]
 A -->|第三方估算 单窗口| C[近期下载活跃]
 C -.->|历史覆盖不足 UNKNOWN| D[突然扩量与发生日期]
 B -.->|时间关系未辨识| D
 L[公开许可与真实文件] -->|下载/schema/许可审计| P[限定通用实验准入]
 P -.->|本轮尚未训练| E[独立方法实验结果]
 E -.->|无目标游戏/平台生产连接| G[Axon或Vector提高四款利润]
 D -.->|无实际成本/收入/实验| G
```

1. **可可靠追踪几款？**身份/当前快照4/4；已证突然扩量起点0/4。Meow/Rotate有值得追的估算集中度线索，不能升格付费扩量。
2. **多少真正可用数据集？**3个已下载且许可支持限定通用研究；满足本项目完整手游价值/多游戏迁移/安装前价值问题的0个。代码包、链接或论文声称不计入。
3. **E0—E4？**LIMITED、LIMITED、STOP、STOP、LIMITED；无原目标GO，无真实ROAS或平台增益结果。
4. **下一轮投入？**优先有界补Rotate/Meow公开历史覆盖；若不可得即停止扩量因果深挖。可另选E1做独立金额预测方法验证，必须接受它不能回答四款盈利原因。

停止细则见[STOP_CONDITIONS](public-evidence/STOP_CONDITIONS.md)。00—64与原关系对象保留；仅追加本轮观察、准入与未知连接。商业许可、完整标签和服务端生产断点没有因公开数据出现而消失。
'''
main=main.replace('归档LICENSE和7份CSV表头','归档LICENSE和6份CSV表头')
write('65_公开扩量证据与模型实验可行性审计.md',main)

# Source catalog: only actually fetched artifacts, not claims that every target was searched exhaustively.
catalog=['# 第65号外部与公开数据原始来源目录','',f'查阅/汇总：{NOW}。所有请求公开只读，无登录、绕过或生产广告事件。HTTP200不等于得到目标广告记录。游戏页只保留产品/聚合元数据，排除评论者与无关脚本；原响应哈希与保留片段哈希分别记录。','',
 '游戏页采用当前产品片段，`.txt`中AppBrain的数字前缀为原页面文本抽取行，不是现在物理行号。原始发布日期、估算数据水位及历史覆盖未知时保留UNKNOWN。下载/排名均不得外推真实付费投放或盈利。','']
for x in sorted(fetches,key=lambda x:x['id']):
 catalog += [f'<a id="{x["id"]}"></a>',f'## {x["id"]}','',f'- 原始URL：{x["url"]}',f'- 最终URL：{x.get("final_url","UNKNOWN")}',f'- 采集时间：{x.get("observed_utc","UNKNOWN")}；HTTP：{x.get("status","UNKNOWN")}',f'- 结果限制：{x.get("error") or x.get("minimization") or "Public source access only; relevance/data scope must be evaluated separately"}']
 if x.get('path'):catalog += [f'- 保留文件：[{x["path"]}](../{x["path"]})；SHA256 `{x["sha256"]}`']
 if x.get('response_sha256'):catalog += [f'- 原HTTP响应SHA256 `{x["response_sha256"]}`；完整含评论HTML未保留，只留产品元数据。']
 if x.get('text_path'):catalog += [f'- 可读抽取：[{x["text_path"]}](../{x["text_path"]})']
 catalog += ['']
catalog += ['## 实际数据发行物与结构核验','',
 '- [UCI/KuaiRand/代码包下载、原包SHA256与结构](../public-experiments/audit/ASSET_VERIFICATION.json)',
 '- [OBD实际样本、SHA256/字段/时间/propensity核验](../public-experiments/audit/OBD_SAMPLE_VERIFICATION.json)',
 '- [KuaiRand包内LICENSE](../public-experiments/audit/KUAI_DATA_LICENSE.txt)',
 '- [Zenodo代码包明确缺商业数据的原文位置](../public-experiments/audit/GAME_CODE_DATA_GAP.json)',
 '- [本地旧版样本与哈希，复用不重新逆向](../SAMPLE_CATALOG.json)',
 '- [旧公开商店/广告访问边界](../04_真实广告素材与投放证据.md)',
 '- [Rotate旧版本签名与代码变化](../05_历史版本策略演进.md)',
 '- 搜索边界：GitHub/Zenodo/DataCite查询结果只有候选发现作用；Bing宽查询回词典/不相关，不算完整覆盖。没有付费下载/账号访问。']
write('public-evidence/EXTERNAL_SOURCE_CATALOG.md','\n'.join(catalog))

# Append new observation/data-admission nodes while leaving all previous graph objects intact.
graphpath=ROOT/'prediction-system/EVIDENCE_GRAPH.json';g=json.loads(graphpath.read_text(encoding='utf-8-sig'))
old=json.loads((PUB/'EVIDENCE_GRAPH.before65.json').read_text(encoding='utf-8-sig'))
assert g==old,'Graph changed unexpectedly during the round'
new_sources=[];new_nodes=[];new_edges=[]
def source_from_fetch(key):
 x=fetchmap[key];sid='PE65S_'+key
 if not any(s['id']==sid for s in new_sources):
  new_sources.append(dict(id=sid,url=x['url'],path=x.get('path'),sha256=x.get('sha256'),source_date=x.get('observed_utc'),evidence_level='public observation, source-specific scope',
    evidence_kind='public metadata/terms/availability observation',raw_response_sha256=x.get('response_sha256'),
    production_actual_proven=False,observed_target_game_delivery=False,server_model_training=False,
    limits='Current snapshot/metadata or explicit source documentation; no paid spend, mature game income, production training or causal profit'))
 return sid
def nd(ident,label,stage):new_nodes.append(dict(id=ident,label=label,stage=stage,company='public evidence and independent experiment audit'))
def ed(ident,a,b,claim,refs,status,grade,missing):
 new_edges.append(dict(id=ident,source=a,target=b,claim=claim,source_ids=refs,status=status,evidence_level=grade,
  edge_type='public_observation_or_experiment_admission',diagram_style='solid' if status in ['observed_scoped','third_party_estimate'] else 'dashed',
  data_provider=a,data_receiver=b,permission_conditions='Public source within license; no real-identity resolution or production ad requests',
  production_actual_proven=False,observed_target_game_delivery=False,independent_production_audit=False,
  six_layers=dict(sdk_capability=False,actual_game_business_callsite=False,request_construction_code=False,production_successful_send=False,server_received=False,server_model_training=False),
  scope='Public observations/data audit only; not platform production proof',reviewed_utc=NOW,missing_evidence=missing))
for slug,*rest in games:
 play=source_from_fetch(slug+'-play');ab=source_from_fetch(slug+'-appbrain')
 nd('PE65_'+slug+'_id',slug+' exact package and developer','identity_verified')
 nd('PE65_'+slug+'_recent',slug+' last-30-day download estimate','public_third_party_estimate')
 nd('PE65_'+slug+'_surge',slug+' sudden growth onset UNKNOWN','unknown_change_point')
 ed('PE65E_'+slug+'_1','PE65_'+slug+'_id','PE65_'+slug+'_recent','Exact-package current store identity and AppBrain canonical permit attribution of this rounded estimate to product',[play,ab],'third_party_estimate','【第三方估算】','No vendor full history/uncertainty or paid-attribution data')
 ed('PE65E_'+slug+'_2','PE65_'+slug+'_recent','PE65_'+slug+'_surge','Single rolling total cannot identify sudden expansion or its onset',[ab],'unknown','【无法确认】','Comparable before/after continuous rank/download history')

nd('PE65_generic','Independent non-gaming monetary/click methods, only LIMITED protocols','experiment_admission')
nd('PE65_game_value','D7/D28 game value / transfer / bid-time LTV experiment STOP','missing_dataset')
nd('PE65_profit','Target game model adoption causes incremental profit UNKNOWN','unknown_causal_effect')
for ident,key in [('DS65-01','uci-retail'),('DS65-03','obd-root-license'),('DS65-04','kuairand-license')]:
 nd('PE65_'+ident,ident+' verified public release within scoped license','public_dataset_verified')
 refs=[source_from_fetch(key)]
 # Attach binary/sample verification directly; archive source provides the definitive license for KuaiRand.
 rec=assetmap['retail352' if ident=='DS65-01' else 'kuairand-pure'] if ident!='DS65-03' else obd
 sid='PE65S_'+ident
 new_sources.append(dict(id=sid,url=rec['url'],path=rec['path'],sha256=rec['sha256'],source_date=NOW,
  evidence_level='【直接观察】',evidence_kind='Downloaded original public data, structure inspected; no training',
  production_actual_proven=False,observed_target_game_delivery=False,server_model_training=False))
 refs.append(sid)
 ed('PE65E_'+ident+'_admit','PE65_'+ident,'PE65_generic','Verified downloadable public sample supports only the explicitly narrowed non-gaming protocol',refs,'observed_scoped','【直接观察】','Actual independent model results not yet produced; original game task still STOP')
 ed('PE65E_'+ident+'_stop','PE65_'+ident,'PE65_game_value','No complete game-install revenue/multi-game/bid-value contract',refs,'unknown','【无法确认】','Licensed mature real game value labels, game IDs, zero install denominator and as-of context')
ed('PE65E_no_bridge','PE65_generic','PE65_profit','Generic public-data experiments cannot establish target game platform adoption or profitability',['PE65S_DS65-01','PE65S_DS65-03'], 'unknown','【无法确认】','Game-specific delivery/activation, true spend and mature income, identifiable controlled experiment')

for key in ['nodes','edges','sources']:
 vals={'nodes':new_nodes,'edges':new_edges,'sources':new_sources}[key]
 ids={x['id'] for x in g[key]};assert not any(x['id'] in ids for x in vals)
 g[key].extend(vals)
g['public_evidence_round65']=dict(reviewed_utc=NOW,report='65_公开扩量证据与模型实验可行性审计.md',
 source_catalog='public-evidence/EXTERNAL_SOURCE_CATALOG.md',identity_registry='public-evidence/GAME_IDENTITY_REGISTRY.csv',
 experiment_admission='public-experiments/EXPERIMENT_ADMISSION_MATRIX.csv',identity_verified=4,sudden_expansion_onsets_verified=0,
 actual_downloaded_licensed_limited_datasets=3,full_game_value_datasets_admitted=0,models_trained=0,
 new_node_ids=[x['id'] for x in new_nodes],new_edge_ids=[x['id'] for x in new_edges],new_source_ids=[x['id'] for x in new_sources],
 stop='No 66 training, causal ROAS or further unbounded architecture/SDK research in this round')
graphpath.write_text(json.dumps(g,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
dump('public-evidence/NEW_EDGES65.json',new_edges)

idx=ROOT/'EVIDENCE_INDEX.md';original=(PUB/'EVIDENCE_INDEX.before65.md').read_bytes();assert idx.read_bytes()==original
addition='''\n\n<a id="pe65"></a>\n\n## PE65 · 公开扩量与数据准入（不做SDK逆向/模型训练）\n\n- [65号审计报告](65_公开扩量证据与模型实验可行性审计.md)\n- [四款精确身份表](public-evidence/GAME_IDENTITY_REGISTRY.csv) / [事件时间线](public-evidence/EXTERNAL_UA_TIMELINES.csv)\n- [外部原始来源与访问限制](public-evidence/EXTERNAL_SOURCE_CATALOG.md) / [四类竞争解释](public-evidence/COMPETING_EXPLANATIONS.md)\n- [9候选数据目录](public-experiments/DATASET_CATALOG.csv) / [数据许可与真实文件审计](public-experiments/DATASET_LICENSE_AUDIT.md)\n- [E0—E4准入](public-experiments/EXPERIMENT_ADMISSION_MATRIX.csv) / [受限实验协议](public-experiments/EXPERIMENT_PROTOCOL.md)\n- [停止条件](public-evidence/STOP_CONDITIONS.md) / [校验](public-evidence/VALIDATION65.json)\n\n新增观察：四款当前身份与快照可核；AppBrain估算近30天Car360万、Meow930万、Rotate850万、Jewel80万，非归因安装/广告花费/利润。0个可确定突然扩量起点。3个公开发行物许可支持受限通用研究，0个满足完整手游价值/迁移/安装前LTV要求；E0/E1/E4 LIMITED替代，E2/E3 STOP，原目标均无GO，未训练模型。关系图保留旧对象，仅追加观察、准入与未知因果边。\n'''
with idx.open('ab') as f:f.write(addition.encode('utf-8'))

# Validation specific to the new audit and historical preservation.
errors=[]
history=json.loads((PUB/'HISTORY.before65.json').read_text(encoding='utf-8'))
for rel,s in history.items():
 if sha(ROOT/rel)!=s:errors.append('historical report modified '+rel)
for key in ['nodes','edges','sources']:
 if g[key][:len(old[key])]!=old[key]:errors.append('historical graph objects mutated '+key)
 ids=[x['id'] for x in g[key]]
 if len(ids)!=len(set(ids)):errors.append('duplicate graph '+key)
for key,value in old.items():
 if key not in ['nodes','edges','sources'] and g[key]!=value:errors.append('old graph metadata changed '+key)
if not idx.read_bytes().startswith(original):errors.append('old index bytes modified')
deliverables=['65_公开扩量证据与模型实验可行性审计.md','public-evidence/GAME_IDENTITY_REGISTRY.csv','public-evidence/EXTERNAL_UA_TIMELINES.csv','public-evidence/EXTERNAL_SOURCE_CATALOG.md','public-evidence/COMPETING_EXPLANATIONS.md','public-experiments/DATASET_CATALOG.csv','public-experiments/DATASET_LICENSE_AUDIT.md','public-experiments/EXPERIMENT_ADMISSION_MATRIX.csv','public-experiments/EXPERIMENT_PROTOCOL.md','public-evidence/STOP_CONDITIONS.md']
links=0
for rel in deliverables:
 p=ROOT/rel;txt=p.read_text(encoding='utf-8')
 if '\ufffd' in txt:errors.append('encoding replacement '+rel)
 if p.suffix=='.md':
  for target in re.findall(r'\]\(([^)]+)\)',txt):
   if target.startswith(('http:','https:','#')):continue
   if not (p.parent/target.split('#')[0]).is_file():errors.append('broken link '+rel+' -> '+target)
   links+=1
 else:
  with p.open(encoding='utf-8',newline='') as f:
   rr=list(csv.DictReader(f))
  if not rr:errors.append('empty CSV '+rel)
for x in fetches:
 if x.get('path') and sha(ROOT/x['path'])!=x['sha256']:errors.append('source hash changed '+x['id'])
for x in list(assetmap.values())+[obd]:
 if sha(ROOT/x['path'])!=x['sha256']:errors.append('download hash changed '+x['id'])
for e in new_edges:
 if any(e['six_layers'].values()):errors.append('public data promoted to SDK/production proof '+e['id'])
validation=dict(status='PASS' if not errors else 'FAIL',reviewed_utc=NOW,scope='Public identity, download/license/schema audit and file preservation only; not growth causality/model validation',
 deliverables=len(deliverables),identities_verified=len(registry),timeline_rows=len(timelines),dataset_candidates=len(datasets),
 fully_downloaded_licensed_limited_research_datasets=3,full_game_ltv_or_transfer_datasets=0,sudden_expansion_onsets_verified=0,
 original_requested_experiment_GO=0,limited_alternatives=['E0','E1','E4'],stopped=['E2','E3'],models_trained=0,
 historical_reports_hash_verified=len(history),old_graph_nodes_preserved=len(old['nodes']),old_graph_edges_preserved=len(old['edges']),old_graph_sources_preserved=len(old['sources']),
 new_graph_nodes=len(new_nodes),new_graph_edges=len(new_edges),new_graph_sources=len(new_sources),public_fetch_records=len(fetches),local_links_checked=links,
 raw_data_and_code_downloads_hash_verified=4,production_ad_or_attribution_events_sent=0,access_controls_bypassed=0,
 no_real_identity_matching=True,original_index_bytes_preserved=True,errors=errors,
 artifact_sha256={rel:sha(ROOT/rel) for rel in deliverables})
dump('public-evidence/VALIDATION65.json',validation)
print(json.dumps({k:v for k,v in validation.items() if k!='artifact_sha256'},ensure_ascii=True,indent=2))
if errors:raise SystemExit(1)
