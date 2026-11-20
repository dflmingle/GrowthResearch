"""Generate delivery docs from actual test outputs; never converts failures to PASS."""
from pathlib import Path
import csv,hashlib,json,sqlite3
R=Path(__file__).resolve().parent
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,t):(R/p).write_text(t.strip()+'\n',encoding='utf-8')
run=R/(R/'LATEST_RUN.txt').read_text().strip();summary=load(run/'SUMMARY.json')
if summary['status']!='PASS':raise SystemExit('Current tests failed; docs will not label completion')
mapping=list(csv.DictReader((run/'ACCEPTANCE_MAPPING_RESULTS.csv').open(encoding='utf-8-sig',newline='')))
for source in ['ACCEPTANCE_MAPPING_RESULTS.csv','SUMMARY.json']:(R/source).write_bytes((run/source).read_bytes())
relative=run.relative_to(R).as_posix()
scope='''本系统是自主的本地合成工程MVP，不是Axon/Vector逆向复现，不证明真实自然人身份、生产模型消费或LTV增益。仅使用Python标准库和SQLite；未启动MAX/LevelPlay、外部身份接口、广告网络或真实用户数据。**C_graph.Axon=UNKNOWN；C_graph.Vector=UNKNOWN；D=UNKNOWN；原生产取证STOP。** 00—78、76程序与既有研究证据不修改，主索引/证据图也不追加。'''
write('README.md',f'''# 自主身份图谱本地MVP

{scope}

已实现七组件，并执行原20项验收及{summary['regression_total']}项反例回归。当前正式结果：[SUMMARY]({relative}/SUMMARY.json)，{summary['tests_run']}项测试、{summary['assertions']}条断言，失败{summary['failures']}、错误{summary['errors']}。更早run保留，不用其PASS替代当前代码结果。

## 运行

Python3.10+，无第三方Python依赖，不需要pip或网络。Windows PowerShell：

```powershell
Set-Location D:\\GrowthResearch\\identity-graph-mvp
python -X utf8 run_tests.py --seed 760078
python -X utf8 -m identity_mvp demo --output demo/my-run --seed 760078
python -X utf8 generate_synthetic_data.py --seed 760078 --output fixtures/my-input.json
python -X utf8 verify_delivery.py
```

本机实际使用`C:\\Users\\89trillion\\anaconda3\\python.exe`。run_tests默认选择新的results/run-NNN；也可`--output results/my-run`。输出目录存在会拒绝覆盖。demo同样要求新目录。测试由标准unittest执行；runner增加断网、逐案例日志与验收映射，不是假PASS生成器。

## 源码与交付

- [七组件源码](identity_mvp/system.py)、[固定种子合成世界](identity_mvp/fixtures.py)、[CLI](identity_mvp/__main__.py)、[数据生成器](generate_synthetic_data.py)。
- [数据表Schema](identity_mvp/schema.sql)、[独立权限/删除控制Schema](identity_mvp/control_schema.sql)、[数据契约和模型边界](DATABASE_CONTRACTS.md)。
- [组件与14条规则映射](ARCHITECTURE.md)、[20项自动化验收映射](ACCEPTANCE_MAPPING_RESULTS.csv)、[自动化用例](tests/test_acceptance.py)。
- [真实执行测试报告](TEST_REPORT.md)、[失败与风险](FAILURES_AND_RISKS.md)、[后续LTV准入](LTV_FEATURE_ADMISSION.md)、[历史保全与交付核验](DELIVERY_VERIFICATION.json)。

每个`{relative}/cases/Vxx`或Rxx目录包含INPUT.json（固定种子、完整合成操作与返回/异常）、EXPECTATIONS_AND_ACTUALS.json、RESULT.json、AUDIT_LOG.json，以及实际SQLite测试数据库。RUN_MANIFEST记录Python/SQLite、源文件SHA256、原验收矩阵SHA256和禁止联网条件；UNITTEST.log为实际unittest日志。R18显式验证socket被阻断，R19以SQLite触发器注入写入失败并验证回滚。

仅demo包含数据流演示，合成金额不是模型效果。`consume_local`只是实际读取特征并记录校验和的本地探针，不是LTV模型、实时竞价或真实广告决策。
''')
classes=[('IdentityNamespaceRegistry','NS','命名空间/实体注册、scope未知拒识、显式映射许可，不自动做同人合并','V01/V02'),
 ('DeterministicIdentityResolver','DR','本地合成HMAC凭证、issuer/audience/有效期与nonce校验；仅账号控制关系','V03/V04/R13/R15'),
 ('ConfidenceAwareRelationshipGraph','RG','typed边、候选隔离、cannot-link、修订撤销/拆分和标识重置','V05–V08/R01/R02/R17'),
 ('TemporalEventLinker','EL','事件幂等、经济主键与修订、事务outbox、多时钟与观察覆盖','V09–V12/R05/R06/R08/R19'),
 ('ConsentAndDeletionManager','CD','独立控制epoch、撤销、device→app实例删除传播、逐sink确认、恢复时清理','V14–V17/R11/R14/R20'),
 ('GraphFeatureService','FS','按账号/设备/应用实例限定遍历，防共享设备污染，as-of与当前权限/版本双门控','V04/V07/V08/V11–V14/R03/R17'),
 ('ProvenanceAuditLog','PA','哈希链与独立形状/引用/产品/时间判定；缺证不可识别、来源不足不可信','V18–V20/R09/R10/R16')]
table='\n| 组件 | 已实现机制 | 验收 |\n|---|---|---|\n'+'\n'.join(f'| {a} | {c} | {d} |' for a,b,c,d in classes)
rules=[('R01','NS','V01/V02'),('R02','DR','V03/R15'),('R03','PA','V18派生ID反例'),('R04','RG','V05'),('R05','RG','V06/R01'),
 ('R06','DR/FS','V04'),('R07','RG/CD','R02'),('R08','RG/FS','V07'),('R09','EL/FS','V08–V13/R06/R19'),
 ('R10','CD/FS','V14/R20'),('R11','CD','V15/V16/R14'),('R12','CD','V17'),('R13','PA/CD','V20/R09；仅合成元数据，不证明真实删除合规'),('R14','PA','V18–V20/R10/R16')]
rule_table='\n| 原规则 | 实现 | 测试/限制 |\n|---|---|---|\n'+'\n'.join(f'| {a} | {b} | {c} |' for a,b,c in rules)
write('ARCHITECTURE.md','# 七组件与14条规则的工程映射\n\n'+scope+table+'''

## 核心不变量

Person、Account、Device、App Instance分别是实体粒度；Event是不可混用的事件实例；Identity Edge是独立、有版本的关系。另保留household粒度以避免与person混淆。本MVP不建立任何person自动推断关系。

命名空间键包括tenant、issuer、app、sector、entity_type、scope和version。相同裸token不跨命名空间比较；显式映射权限也不是同人证据。所有issuer和标识输入限synthetic:/syn:，事件/来源限synth:。这只是合成输入防误用护栏，不是生产安全隔离。

认证只使用公开、固定种子的本地HMAC密钥，绝不能作为真实认证服务。nonce和范围保存在独立privacy.sqlite；graph公开写账号边必须引用已认证且scope匹配的回执。Account→多Device和Device→多Account允许存在，但feature不能沿共享设备扩散到另一个账号。

candidate_same_entity无论分数多高都不激活。same_device用于合成已知设备别名的显式声明，可构造可撤销连通视图；不是概率候选传递闭包。加入cannot-link先检查约束，迟到约束可隔离已存在错误边。原始edge revisions保留；撤销改变当前视图而非不可逆union。

事件发生、接收、本地观察、消费者可用时间分别保存。只读取当时已知关系和经济修订；原始经济时间用于窗口，更正按已知版本选最新净额，不把所有revision相加。未来available_at被排除。历史重放在今天物化，不允许伪造过去的active消费。

授权epoch与graph_version全局保守失效：任何源数据/关系变化可清除全部旧bundle，牺牲性能以降低MVP遗漏失效风险。实际read还核对当前授权及边有效/撤销/到期状态，即使时钟变化而未写新图，也不能消费过期关系。

## 删除与恢复

privacy.sqlite独立保存撤销、删除、key tombstone、nonce和单调ID计数；state.sqlite保存图/事件/特征。支持的备份/恢复只回滚state，之后按保留的控制状态重放删除/失效。若操作员同时回滚/丢失privacy.sqlite，当前MVP不能保证防复活，必须STOP，详见风险。

设备删除覆盖其已知App Instance及其事件/账本/outbox，绝不沿账号扩展到其他设备；账号删除只清其明确归属的记录，保留另一个账号在共享设备上的数据。派生bundle采取全局清空。删除输出逐sink状态；未确认导出为ACK_PENDING；关联已训模型的合成血缘标记MODEL_ERASURE_UNKNOWN，不伪称参数已遗忘。

上述是逻辑清理与局部恢复协议，不能证明磁盘取证级擦除、真实partner执行或训练权重遗忘。不存在真实外部export/训练服务；相关状态是合成契约测试。
'''+rule_table)

connection=sqlite3.connect('file:'+(R/'demo/run-001/database/state.sqlite').as_posix()+'?mode=ro',uri=True)
schema=[]
for name,sql in connection.execute("SELECT name,sql FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name").fetchall():
    columns=[dict(cid=x[0],name=x[1],type=x[2],not_null=bool(x[3]),default=x[4],primary_key_order=x[5]) for x in connection.execute('PRAGMA table_info('+name+')')]
    schema.append(dict(database='state.sqlite',table=name,sql=sql,columns=columns))
connection.close()
connection=sqlite3.connect('file:'+(R/'demo/run-001/database/privacy.sqlite').as_posix()+'?mode=ro',uri=True)
for name,sql in connection.execute("SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name").fetchall():
    schema.append(dict(database='privacy.sqlite',table=name,sql=sql,columns=[dict(cid=x[0],name=x[1],type=x[2],not_null=bool(x[3]),default=x[4],primary_key_order=x[5]) for x in connection.execute('PRAGMA table_info('+name+')')]))
connection.close();(R/'DATABASE_SCHEMA.json').write_text(json.dumps(schema,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
schema_table='\n| 数据库 | 表 | 职责 |\n|---|---|---|\n'
roles={'namespaces':'作用域注册','namespace_mappings':'显式账号namespace映射许可，不是实体合并','entities':'分粒度实体和合成token/tombstone',
 'edge_revisions':'关系来源/scope/置信度/有效/观察/可用/撤销/版本','events':'事件幂等、时钟和修订','ledger':'经济主键、金额micros、currency、IAA/IAP及更正',
 'outbox':'与事件同事务的本地待处理记录，不发送','coverage':'COMPLETE/MISSING/EXITED观察声明','feature_bundles':'派生特征和血缘/权限/graph版本',
 'training_snapshots':'仅合成训练血缘，不训练','audit_log':'有序SHA256链','meta':'本地环境和图版本','policies':'授权/撤销effective与observed和epoch',
 'deletions':'删除范围、状态和训练影响','deletion_sinks':'逐sink确认/未确认','auth_nonces':'认证重放拒绝和app/account/purpose范围',
 'erased_entities':'删除扩展实体的控制tombstone','control_meta':'单调epoch、ID计数和删键摘要'}
schema_table+='\n'.join(f"| {x['database']} | {x['table']} | {roles.get(x['table'],'')} |" for x in schema)
write('DATABASE_CONTRACTS.md','# SQLite Schema与数据契约\n\n'+scope+schema_table+'''

实际建表语句在identity_mvp/schema.sql和control_schema.sql；DATABASE_SCHEMA.json从本轮实际运行的demo数据库PRAGMA导出，不是手写虚拟结构。源研究数据契约原字节保留在contracts/，作为参考，不宣称完整实现厂商schema或全部参考扩展。

## API契约

| 入口 | 必需输入 | 输出/拒绝 |
|---|---|---|
| namespaces.register/create | synthetic issuer、typed scope、syn token | namespace/entity引用；UNKNOWN_SCOPE拒绝 |
| resolver.login | 本地签名assertion、issuer/aud、account/app/device、nonce、iat/exp、purpose | ACCOUNT_RELATION_ESTABLISHED；错签名/时效/重放拒绝；无person升级 |
| graph.add/revoke/reset_device | typed端点、synth来源、scope、confidence/quality、有效/可用时间 | ACTIVE/CANDIDATE/CONFLICT或修订；账号边需认证回执 |
| events.ingest | app、source/event instance、revision、UTC时钟、可选明确account/economic key | ACCEPTED/DUPLICATE_EVENT/DUPLICATE_LEDGER；冲突拒绝 |
| features.compute/read | subject、as_of/since、purpose、当前clock | 观察金额/缺失状态、lineage、bundle或拒绝；不输出预测LTV |
| policy.set/delete/acknowledge | subject scope、有效时点、source、合成sink | epoch、删除逐sink状态；未确认不报完成 |
| audit.verify/assess_chain | hash链或独立匿名证据包 | 本地链一致性/UNTRUSTED/NOT_IDENTIFIABLE；所有厂商结论保持UNKNOWN |

时间统一为整数UTC epoch秒，拒绝浮点/负值/未来预测时点和本地available_at倒填。有效区间为[valid_from,valid_to)，撤销/到期从边界时刻起拒绝；可用时点≤预测as_of，当前授权必须在实际read时成立。模拟时钟仅前进，代码不调用真实服务时钟。

金额使用integer micros，不用浮点；币种分别汇总，多币种没有汇率就返回MIXED_CURRENCY/总额null。ledger唯一键(app_ref,source,economic_key,revision)，修订必须串到前一revision；事件唯一键(tenant,app_ref,source,event_id,revision)。相同幂等键不同payload报冲突，不能静默改值。

无事件且观察完整才可返回revenue_micros=0；缺采/退出/不完整时该字段null，observed_revenue_micros只代表已观察账本金额，不是完整LTV。coverage为合成声明，无自动证明真实观察完整性的能力。App/Person/Account与Event/Edge永不混用主键。

落盘隐私：本MVP只存合成token；删除清当前token/payload/amount及所有bundle，但保留合成引用与审计链。没有真实PII vault、密钥管理或介质擦除。外部回执只是带synth来源的本地声明；源码使用者不应把它当真实第三方删除/独立审核证明。
''')

accept_table='\n| ID | 原始验收 | 真实执行 | 断言数 | 逐项输入/预期/实际 |\n|---|---|---|---|---|\n'+'\n'.join(f"| {x['test_id']} | {x['original_test']} | {x['implementation_status']} | {x['assertions']} | [记录]({relative}/{x['expected_actual_path']}) |" for x in mapping)
write('TEST_REPORT.md',f'''# 本地MVP真实测试报告

{scope}

正式代码对应运行：`{relative}`；seed={summary['seed']}。标准unittest实际执行{summary['tests_run']}项（20项原验收＋{summary['regression_total']}项回归），{summary['assertions']}条断言，{summary['failures']}失败、{summary['errors']}错误。网络socket/DNS/连接在整个测试期间被禁用；不是向真实服务发送请求后的结果。

原20行需求从server-identity-reference复制，SHA记录于RUN_MANIFEST；映射保留原test/expected/rules原文，没有降低预期。[逐项矩阵](ACCEPTANCE_MAPPING_RESULTS.csv)、[实际日志]({relative}/UNITTEST.log)、[全部案例]({relative}/ALL_CASE_RESULTS.json)。
'''+accept_table+'''

## 用户十项必测的覆盖

| 要求 | 测试 |
|---|---|
| 单账号多设备 | V04 |
| 多账号共用设备且不串收入 | V04、R11 |
| 多应用实例关联 | R03及V04 |
| 标识重置 | R02 |
| 关系冲突 | V06、R01 |
| 错误关系撤销/拆分 | V07 |
| 同意撤销 | V14、R20 |
| 删除传播与恢复后不复活 | V15、V16、R14 |
| 派生特征失效/到期 | V07、V14、R17 |
| 预测时间点防泄漏 | V08、V11、R06；V13为后端准入契约 |

## 回归与证据限制

回归还覆盖auth nonce备份恢复、直接伪造账号边、错误实体粒度、经济冲突、混币、审计篡改、产品/模型/时间引用不一致、删除不误伤另一个账号、合成数据不能获准LTV实验、恶形证据fail-closed、socket确实禁用及SQLite事务失败回滚。

V13只验证自有适配器准入条件及本地时序逻辑；没有安装/运行Feast。V17只注册“合成已训模型引用”用于测试未知状态，没有真的训练或遗忘模型。V18–V20的来源/复核/引用权字段是本地fixture声明，仅检验审计判定器不跳级；不证明真实权利方真实性。R09故意破坏测试库审计链，预期verify=false，是通过的反例，不是正式运行数据损坏。

日志和结果是本轮真实执行产生；数据完全合成，所以PASS只证明指定工程行为。未报告真实匹配准确率、错误合并总体率、延迟SLA或LTV收益。复现命令见README。测试环境/版本/源SHA在RUN_MANIFEST，结果目录只新增不覆盖；开发期和旧run也保留。
''')
write('FAILURES_AND_RISKS.md','# 已修复失败与当前风险\n\n'+scope+'''

## 本轮开发失败/复核修正

| 项目 | 发现 | 修复与证据 |
|---|---|---|
| 初次smoke | feature_bundles INSERT占位符多一列，SQLite拒绝；随后临时目录清理因异常时连接未关闭报Windows文件锁 | 修正12列INSERT；所有正式用例tearDown和demo finally关闭；首轮及后续运行均重新执行。初始交互输出未冒充正式PASS |
| 数据备份恢复 | nonce/ID若随state一起回滚可能重新使用 | 控制库单独保留nonce和ID计数；R07/R13验证 |
| 设备删除范围 | 仅删device直接引用会遗漏其App Instance的事件 | typed device→instance扩展，绝不沿账号扩展其他设备；R14验证 |
| 图账户边旁路 | 直接graph.add可绕过resolver认证入口 | logged_in_as强制检查认证回执及app/account/purpose；R15验证 |
| 时间推进无新写入 | 缓存可能在边到期或计划撤权时仍存在 | read检查当前边/策略状态；R17/R20验证 |
| 异常证据包 | 畸形类型可能让审计函数抛出而非拒识 | 公共审计入口fail-closed；R16验证 |
| 事务中途失败 | 要证明不是只测成功路径 | R19实际SQLite trigger注入outbox写失败，验证events/ledger/outbox回滚，再重试一次入账 |

正式结果不是靠修改原20项预期得到；旧run-001/run-002保留各自代码哈希，只引用LATEST_RUN对应代码作为当前结果。

## 当前失败与未执行事项

正式测试的失败/错误数以SUMMARY为准；本轮没有未修复的已知验收失败。不把下列未实施能力隐藏成通过：

- 仅合成输入、本地单进程单写者；没有真实SSO/OIDC验证、生产鉴权、权限管理、KMS、多租户攻击面审计或多机一致性保证。公开HMAC测试密钥不可用于真实用户。
- 没有真实概率匹配模型和代表性校准。candidate永不自动激活；same_device仅是显式合成事实声明。未测真实误并/误拆总体率，也没有自然人身份推断。
- 删除是SQLite当前逻辑值清理，不是磁盘取证级擦除。测试原始输入、备份和旧run有意保留合成数据以便复核，不可套用成真实PII保留政策。
- 防复活依赖独立privacy.sqlite不被同时回滚/丢失。若两个数据库一起恢复旧备份，须STOP并从可信撤销/删除权威恢复；MVP未提供外部WORM或远端证明。
- 两数据库不提供分布式事务。策略/nonce先提交以fail-closed；崩溃可能消耗nonce但没有建边，需要新凭证。未做断电、文件系统损坏或多进程竞争故障测试。
- 外部sink ACK只是本地合成声明，没有真实导出/partner传输与回执真实性证明。COMPLETE仅限声明的本地范围，不能证明第三方、备份介质或模型权重遗忘。
- graph_version/policy_epoch采取全局清bundle，正确性优先但扩展性差；未做性能/高并发测试。该MVP不承诺毫秒级广告机会服务能力。
- coverage是合成输入，不自动证明真实零值/完整观察；不自动处理真实汇率、税/退款业务校验、广告精度更正来源和安装分母。
- 审计SHA链能发现修改，但哈希不证明出具方真实性。证据审查中的独立复核/引用权限是fixture元数据；不能移作真实工程取证认证器。
- 没有LTV模型、真实收入训练数据、报价/预算控制器或盈利实验；checksum consumer只证明本地代码确实读了特征。

不向生产接口扩展上述能力。后续工程需独立授权/准入和针对风险的新测试，不得用本地PASS升级厂商C_graph或D。
''')
write('LTV_FEATURE_ADMISSION.md','# 后续LTV特征实验准入\n\n'+scope+'''

当前准入：**STOP真实LTV效果实验**。现有数据完全合成，只能检查代码、时间、会计和血缘行为；revenue_micros不是预测LTV。IdentitySystem.ltv_admission在合成数据上固定拒绝，R12已执行验证。

真实实验需要逐项独立满足：

1. 权利方真实游戏数据与对应研究用途许可；稳定且合法作用域，不自行连接第三方个人身份。
2. 完整安装/玩家分母、进入和退出观察边界、缺采解释；可区分真实零收入与未观察。
3. 真实IAA展示级经济账本、IAP交易/退款、更正、币种及收入精度；D7/D28标签成熟水位可审查。
4. 事件发生、接收、模型可用及关系当时已知时间；所有特征在预测时可用，迟到/回填不能倒灌。
5. 时间外训练/验证/测试和实体簇隔离，训练标签在下一阶段预测前成熟；测试集不用来调阈值。
6. 当前与历史用途授权、撤销/删除和派生特征策略；真实生产安全/权限能力未完成前不接入。
7. 固定样本量、模型容量、训练预算和评价策略的M0–M4对照：上下文、同App历史、聚合prior、共享参数、合法个人关系特征。分离更多数据与身份关系本身的作用。
8. 金额MAE/RMSE/中位误差、Recall@10%、Top10金额捕获和校准；按合法独立实体/簇bootstrap，并报告误并/误拆、缺失/国家/游戏分层。

没有完整机会/真实成本/策略实验不计算竞价ROAS或利润；没有指定Axon/Vector接收及模型非空读取原件，不把自主模型效果当厂商架构证明。

最小可继续的本地工作：用同一合成生成器测试标签构建器、账本修订和时间切分，仍不报告真实预测提升。真正的下一步效果验证应先取得符合上述条件的授权游戏数据，当前不是自动创建新训练任务或79号生产取证。
''')
print(json.dumps(dict(documented_run=relative,tests=summary['tests_run'],assertions=summary['assertions'],schema_tables=len(schema)),ensure_ascii=False))
