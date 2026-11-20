from pathlib import Path
import csv,json

R=Path(__file__).resolve().parent.parent;D=R/'blackbox75'
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
definitions=[
 dict(id='H0',training='T0: target/context-only supervised knowledge',online='D0: no individual source-app history query',scope='Context/device and pre-frozen baseline statistics;no source-game-trained delta in the operational build'),
 dict(id='H3_cohort',training='T1: multi-product aggregate cohort knowledge',online='D0: no individual source-app history query',scope='Aggregate tables fixed during primary window;small-cell or dynamic cohort leakage must be audited'),
 dict(id='H3_shared',training='T1: multi-product shared parameters/representations',online='D0: no individual source-app history query',scope='Training provenance differs from H0;frozen prediction mapping can be identical'),
 dict(id='H1',training='T0 or T1',online='D1: same-device source-app history;D2 absent',scope='Cross-app device relation,not cross-device or person identity'),
 dict(id='H2_account',training='T0 or T1',online='D2: cross-device account-linked history;D1 optional',scope='Account-level link and source->target use;not natural-person identity'),
 dict(id='H2_person',training='T0 or T1',online='D2 plus independently authorized person-level truth/contract',scope='Additional entity claim;self-owned shared test login alone cannot establish person granularity'),
 dict(id='HH_household',training='Any',online='Household/network association,not individual equality',scope='Competing nuisance mechanism;shared IP does not establish a household truth')]
save(D/'HYPOTHESES.json',dict(definitions=definitions,mutual_exclusivity='H0 vs H3 differ on source-training provenance;H1 excludes D2;H2 permits D1. H2_person is nested in H2,not independently separable by ad outputs. HH is a competing layer and can coexist.',
 operational_nonpersonal_null='D0 with frozen aggregate/model state includes H0 and H3;ad-only tests generally target D0 vs online transfer,not T0 vs T1',
 identifiability='Output equality of two feasible worlds makes the internal mechanism non-identifiable at that observation level'))
observations=[
 ('O1_creative','广告素材变化','Same-device randomized source history;time/inventory/frequency blocks','Raw authorized creative hash or local mock category;no landing-page tracking',
  'Material selection can change under any hypothesis;no change also possible under any','Campaign eligibility,auction noise,creative rotation,caching,context mediation','Frozen-state source-history perturbation plus provenance/selection audit','不可识别（仅素材）'),
 ('O2_frequency','广告出现频率','Equal eligible opportunity schedule and pre-period exposure;separate cap policy','Counts per all eligible opportunities including no-fill and failures',
  'Cross-app/cross-device caps can change frequency without any value-model history','Earlier exposure,cap namespace,rate limits,reinstall cache,anti-fraud','Cap-state/cap-entity/eligible inventory and authorized feature-consumption logs','不可识别（频次不等于图谱入模）'),
 ('O3_advertiser_category','广告主或类别变化','Random source-history assignment with fixed target context and model/stock','Authorized advertiser/category mix;all candidates only if permitted',
  'Compositional shift is compatible with history use,cohort,policy or stock shift','New advertisers,country/daypart,auction price,reporting classification','Randomized provenance-positive receiver audit,stock and policy frozen','条件支持跨App因果影响；不唯一识别图谱'),
 ('O4_audience','测试账户可见受众状态','Platform-approved source canary and destination scope;no real PII','Audience membership/change time in an explicitly authorized test console',
  'Could show a receiver processed an inclusion rule;not independent proof of learned value','Async refresh,retention,manual list upload,household eligibility,wrong namespace','Receiver/product/granularity/version and event-receipt mapping','条件识别受众处理；不识别Axon/Vector模型使用'),
 ('O5_match','获授权匹配成功/失败状态','Authorized sandbox known mapping/derived/no-match controls;partner translation permissions','Maintained/derived/status/namespace/granularity/quality flags;no raw identity',
  'Service-specific matching may be established;no inference about consuming platform without receipt','Derived fallback,multiple candidates,stale/deleted result,partner encoding,account sharing','Authorized service result truth plus target-platform actual receipt and purpose','条件识别服务关联；不自动识别人或模型'),
 ('O6_feature','获授权匿名化特征消费记录','Same shadow request with allowed individual feature family on/off;fixed graph/model state','Non-null source-app history lineage,feature group/version/time,consumer and decision trace',
  'Can identify that the specified recipient model read the matched feature;not its benefit','Logged-but-not-read flags,zero/imputed features,selection-only use,future availability','Attested actual non-null read,source lineage,entity scope and feature-version-to-model map','条件识别指定模型消费；收益仍未知'),
 ('O7_score','授权影子分数/报价差分','Replay fixed candidate set/context/controller;feature or lookup gating randomized','Score/bid before selection and candidate/cap/stock versions in sandbox',
  'Score change establishes sensitivity to intervention only under audited exclusion','Calibration/version changes,audience rules,budget pacing,missingness fallback','Verified perturbation touched only matched-history input;test control-plane audit','条件识别分数依赖；不能单凭分数证明价值优势'),
 ('O8_increment','固定条件身份增益消融','M4 vs M3: same samples,capacity,time,source data,policy and accurate authorized links','Independent mature real value labels/calibration/ranking;paired uncertainty',
  'Distinguishes incremental predictive benefit in data scope;not vendor deployment without provenance','Extra data/parameters,coverage selection,identity leakage,label maturity,policy changes','74 protocol gates plus model lineage and independent test;causal UA needs separate authorized trial','条件识别预测独立增益；本轮STOP真实实验')]
rows=[]
for h in definitions:
 for oid,name,control,output,expect,confound,extra,status in observations:
  if h['id']=='H0':specific='Frozen contextual baseline does not respond to a privately randomized source-history bit under exclusion;current context/market still affect ads.'
  elif h['id'].startswith('H3'):specific='Fixed aggregate/shared model should not respond to an isolated source bit without a permitted aggregate update or current-context path;training origin invisible from mapping alone.'
  elif h['id']=='H1':specific='Same-device transfer may respond when consent and lookup work;cross-device transfer absent by definition;caps/audiences can mimic ads.'
  elif h['id']=='H2_account':specific='History-by-link interaction may appear across devices;link main effect alone does not identify transfer;account is not a person.'
  elif h['id']=='H2_person':specific='Same ad distribution can arise under account or household links;person-level truth and contract are additionally necessary.'
  else:specific='Shared-network/household effects can mimic cross-device co-response;must separate network group from permitted account link.'
  assumptions='Random assignment/positivity;no source->target context leakage;frozen aggregate/model/stock/caps;no interference or cluster it;known delivery latency;purpose-valid consent;valid denominator and observed receipt.'
  if oid=='O8_increment':assumptions='Real authorized mature labels;fixed effective training samples and model budget;time/entity-disjoint tests;no extra coverage/label leakage;predeclared effect and multiplicity control.'
  rows.append(dict(row_id=f'BB75M{len(rows)+1:03}',hypothesis=h['id'],training_scope=h['training'],online_link_scope=h['online'],observation_id=oid,observation=name,
   controllable_input=control,observable_output=output,expected_difference=specific+' '+expect,major_confounders=confound,additional_evidence_required=extra,
   identifiability=status,identifying_assumptions=assumptions,entity_claim_boundary=h['scope'],current_level='L0/design plus offline synthetic;no real L1/L2 execution',
   evidence_ids='IV74S01;IV74S02;IV74S04;IV74S05;IV74S09;IG72S05;MA60S17' if oid in ['O4_audience','O5_match','O6_feature'] else 'IV74R01;EX73R07;EX73R08'))
with (R/'75_黑盒可识别性矩阵.csv').open('w',newline='',encoding='utf-8-sig') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
save(D/'IDENTIFIABILITY_MATRIX.json',rows)
print(json.dumps(dict(hypotheses=len(definitions),observations=len(observations),rows=len(rows))))
