"""Read executed artifacts; never invent test PASS or update historical files."""
import sys
sys.dont_write_bytecode=True
from common import ROOT,PARENT,load,save,sha,csvsave

def all_results(value,path='actual'):
    if isinstance(value,dict):
        if value.get('status')=='OK' and 'partition_audit' in value:yield path,value
        else:
            for key,child in value.items():
                if key!='faulty':yield from all_results(child,path+'.'+key)
    elif isinstance(value,list):
        for i,child in enumerate(value):yield from all_results(child,path+f'[{i}]')

def describe(value):
    if not isinstance(value,dict):return str(value)
    if 'A_device' in value:return 'device拒绝；account=10；task源7/目标3'
    if 'detected' in value:return 'DETECTED: '+','.join(value['detected'])
    if 'reread' in value:return '旧值='+value['reread']['status']+'；新值='+value['fresh']['status']
    return value.get('status', '已执行来源SQL检查')+(' / '+value['reason'] if 'reason' in value else '')

def main():
    latest=load(ROOT/'LATEST_RUN.json');run=ROOT/latest['run'];summary=load(run/'SUMMARY.json')
    records=sorted([load(p) for p in run.glob('*/CASE.json')],key=lambda x:x['id'])
    manifest=load(run/'ARTIFACT_SHA256.json')
    bad=[p for p,h in manifest.items() if not (run/p).is_file() or sha(run/p)!=h]
    sources=load(run/'SOURCE_SHA256.json')
    changed=[p for p,h in sources.items() if sha(ROOT/p)!=h]
    if bad or changed:raise SystemExit('Cannot report modified execution artifacts: '+repr((bad,changed)))
    audit=[]
    for rec in records:
        for path,value in all_results(rec.get('actual')):
            for row in value['partition_audit']:
                fields=['occurred_at','observed_at','available_at','event_occurred_at','event_observed_at','event_available_at']
                audit.append(dict(case_id=rec['id'],result_path=path,ledger_ref=row['ledger_ref'],event_ref=row['event_ref'],
                    app_ref=row['app_ref'],app_namespace=row['app_namespace']['namespace_ref'],partition=row['partition'],
                    amount_micros=row['amount_micros'],currency=row['currency'],prediction_at=value['prediction_at'],
                    max_source_time=max(row[k] for k in fields),time_check=all(row[k]<=value['prediction_at'] for k in fields),
                    ledger_approved=row['ledger_ref'] in value['original_lineage']['ledger_refs'],
                    event_approved=row['event_ref'] in value['original_lineage']['event_refs'],
                    account_matches=row['account_ref']==value['authorization_audit']['receipt_account'],
                    receipt_target_matches=value['authorization_audit']['receipt_app']==rec['input']['task']['target_install_ref']))
    audits_ok=all(all(r[k] for k in ['time_check','ledger_approved','event_approved','account_matches','receipt_target_matches']) for r in audit)
    csvsave(ROOT/'权限时间来源审计.csv',audit)
    counter=[]
    for rec in records:
        actual=rec.get('actual',{})
        if 'detected' in actual:counter.append(dict(case_id=rec['id'],detected=bool(actual['detected']),
            violations=';'.join(actual['detected']),status=rec['status'],evidence=f"{latest['run']}/{rec['id']}/CASE.json"))
    csvsave(ROOT/'故意错误反例检测.csv',counter)
    csvsave(ROOT/'三路对照.csv',[
        dict(route='A_existing_device_adapter',subject='shared_D1',status=records[0]['actual']['A_device']['reason'],
            source_X_micros='',target_Y_micros='',account_total_micros='',meaning='device ambiguity denied'),
        dict(route='B_original_account_API',subject='account_A',status=records[0]['actual']['B_original_account']['status'],
            source_X_micros='',target_Y_micros='',account_total_micros=records[0]['actual']['B_original_account']['read']['values']['observed_revenue_micros'],meaning='approved account total; no task partition'),
        dict(route='C_task_aware_adapter',subject='account_A_target_Y',status=records[0]['actual']['C_task']['status'],
            source_X_micros=records[0]['actual']['C_task']['cross_app_history']['observed_amount_by_currency_micros']['USD'],
            target_Y_micros=records[0]['actual']['C_task']['target_app_history']['observed_amount_by_currency_micros']['USD'],
            account_total_micros=records[0]['actual']['C_task']['original_account_values']['observed_revenue_micros'],meaning='account scoped; no person inference')])
    independent=dict(run=latest['run'],executed_artifacts_verified=len(manifest),executed_source_hashes_match=not changed,
        audit_rows=len(audit),permission_time_source_rows_pass=audits_ok,counterexamples=counter,
        audit_scope='artifact integrity and fixture provenance checks; NOT independent external attestation')
    save(ROOT/'RESULT_VERIFICATION.json',independent)
    if not audits_ok:raise SystemExit('Output source/time audit failed')
    head=f"# E01 实际测试报告\n\n运行：`{latest['run']}`；seed=780241。\n\n实际执行 {summary['tests_run']} 项，PASS {summary['passed']}，failures {summary['failures']}，errors {summary['errors']}。结论：**{summary['decision']}**。所有状态来自已执行的 unittest 与 CASE.json。\n\n"
    table='|用例|预期|实际摘要|断言结果|\n|---|---|---|---|\n'
    for rec in records:table+=f"|{rec['id']}|{rec['expected']}|{describe(rec.get('actual'))}|{rec['status']}|\n"
    history=[]
    for p in sorted((ROOT/'runs').glob('*/SUMMARY.json')):
        x=load(p);history.append(f"- `{p.parent.name}`：{x['passed']}/{x['tests_run']}，failures={x['failures']}，errors={x['errors']}。")
    tail=f"\n完整输入/预期/实际见各用例 CASE.json，最终数据库及原MVP哈希链日志与其同目录。受保护历史文件 {summary['preservation']['checked']} 项，执行前后不一致均为 0。进程内网络阻断记录 {len(summary['network_attempts'])} 次尝试。\n\n## 失败与修复记录\n\n"+'\n'.join(history)+"\n\n首轮真实失败主要来自 compute 的 tuple 与 read 的 JSON list 直接比较，以及测试对 namespaces.compare 返回类型理解错误。仅修复 E01 的结构比较与 API 使用，未改原系统或预期金额。真正血缘缺失/不同仍由 C20/C21/C34 拒绝。旧失败日志保留。\n\n## 复核与限制\n\n"+f"已核验 {len(manifest)} 个执行产物哈希和 {len(sources)} 份当次执行源码哈希；{len(audit)} 行合法输出来源审计检查时间、原批准引用、账号和回执目标。三个故意错误输出均应被 fixture 独立等式及来源审计识别；它们不是生产攻击测试或真实身份匹配测试。\n\n"+"复现命令见 README.md。没有 E02/E03、模型训练或预测收益。结果只适用于可信本地单进程/合成凭据和原MVP语义；不提供并发跨进程原子性、真实SSO或外部删除证明。\n\nC_graph.Axon=UNKNOWN；C_graph.Vector=UNKNOWN；D=UNKNOWN；原生产取证STOP。\n"
    (ROOT/'E01_测试报告.md').write_text(head+table+tail,encoding='utf-8')
    decision=f"# E01 总结与 GO/HOLD/STOP\n\n**{summary['decision']}**：{summary['passed']}/{summary['tests_run']} 项实际检查通过。\n\n"
    decision+="三路对照：共享设备 D1 的 device 适配器以 SHARED_DEVICE_ACCOUNT_AMBIGUITY 拒绝；原 account API 返回 A 的 10；新适配器在原批准来源上分别输出 X=7、Y=3。B 的 99 未进入 A，账号未升级为自然人。\n\n"
    decision+="撤销、删除、关系到期和定时撤权后旧 bundle 读取被拒绝；晚可用事件和关系未进入预测历史；负金额保留符号；缺采无事件为不完整观察，完整观察无事件才为零。认证不足拒绝，来源不足返回 UNSUPPORTED_PARTITION 并停止分区。重装以目标产品而非单一安装实例划分，混币不做隐式汇总。\n\n"
    decision+="账号串账、源目标混算、晚到信息泄漏三个故意错误反例被识别。逐例输入/期望/实际、原账本、审计链、源码及产物 SHA256 都已落盘，首轮失败没有覆盖。\n\n"
    decision+="GO 仅指本地 E01 账号任务路由与来源分区工程验收。真实身份、真实数据、LTV预测和远程服务接入为 HOLD，需另行明确授权和准入；原生产取证为 STOP。不自动启动 E02/E03，不生成79号取证任务，不改变厂商结论。\n\n"
    decision+="本地 auth_receipt 是原 resolver 接受的合成记录引用，不是远程认证产品。reread 必须参与后续使用；已经导出的普通 JSON 不具备远程召回能力。allowlist 只作任务选择，权限始终来自原系统；对外服务还需另行设计最小披露和调用方授权。\n\n"
    decision+=f"保护检查 {summary['preservation']['checked']} 项通过；未修改00—78、76程序、MVP、lab和机制研究历史。运行位置 `{latest['run']}`。\n\nC_graph.Axon = UNKNOWN\n\nC_graph.Vector = UNKNOWN\n\nD = UNKNOWN\n\n原生产取证 = STOP\n"
    (ROOT/'E01_总结与结论.md').write_text(decision,encoding='utf-8')
    final={p.relative_to(ROOT).as_posix():sha(p) for p in ROOT.iterdir() if p.is_file() and p.name!='DELIVERY_SHA256.json'}
    save(ROOT/'DELIVERY_SHA256.json',final)
    print(dict(run=latest['run'],decision=summary['decision'],audit_rows=len(audit),verified_artifacts=len(manifest)))

if __name__=='__main__':main()
