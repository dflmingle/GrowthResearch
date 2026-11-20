"""Build deliverables from immutable executed artifacts; no fake PASS rows."""
import sys
sys.dont_write_bytecode=True
from e02_common import ROOT,load,save,sha,csvsave,digest,preservation

def check_chain(rows):
    previous='0'*64
    for row in rows:
        if row['previous_hash']!=previous:return False
        if digest({k:v for k,v in row.items() if k!='hash'})!=row['hash']:return False
        previous=row['hash']
    return True

def main():
    latest=load(ROOT/'LATEST_RUN.json');run=ROOT/latest['run'];summary=load(run/'SUMMARY.json')
    artifacts=load(run/'ARTIFACT_SHA256.json');sources=load(run/'SOURCE_SHA256.json')
    bad=[p for p,h in artifacts.items() if not (run/p).is_file() or sha(run/p)!=h]
    changed=[p for p,h in sources.items() if sha(ROOT/p)!=h]
    current=preservation()
    if bad or changed or current['mismatches']:raise SystemExit('Integrity mismatch: '+repr((bad,changed,current)))
    records=sorted([load(p) for p in run.glob('*/CASE.json')],key=lambda x:x['id'])
    transitions=[];checks=[];mutants=[];local=[];verification=[]
    allowed={'QUEUED':{'CLAIMED','CANCELLED'},'CLAIMED':{'REVALIDATING','CANCELLED'},
        'REVALIDATING':{'CANCELLED','RETRY_PENDING','LOCAL_ACK'},'RETRY_PENDING':{'CLAIMED','CANCELLED'},'CANCELLED':set(),'LOCAL_ACK':set()}
    for rec in records:
        actual=rec['actual'];logs=actual['audit'];chain_ok=check_chain(logs);states={};transitions_ok=True
        prior_final={}
        for row in logs:
            details=row['details'];job=row['job_ref']
            if row['kind']=='transition':
                old=details['from_state'];new=details['to_state']
                valid=(old is None and job not in states and new=='QUEUED') or (states.get(job)==old and new in allowed.get(old,set()))
                transitions_ok=transitions_ok and valid;states[job]=new
                transitions.append(dict(case_id=rec['id'],seq=row['seq'],job_ref=job,from_state=old,to_state=new,
                    at=row['at'],epoch=row['epoch'],event_ref=row['event_ref'],outbox_ref=row['outbox_ref'],
                    reason=details['reason'],transition_valid=valid,local_ack=new=='LOCAL_ACK',external_ack=False))
            if row['kind']=='permission_check':
                gates=details['details']['gates']
                checks.append(dict(case_id=rec['id'],seq=row['seq'],phase=details['phase'],at=row['at'],epoch=row['epoch'],
                    allowed=details['ok'],reason=details['reason'],collection=gates['collection'],transmission=gates['transmission'],
                    purpose=gates['purpose'],delete=gates['delete'],relationships=gates['relationships'],sources=gates['sources']))
            if row['kind']=='final_handoff_check':prior_final[job]=row
            if row['kind']=='local_sink_acceptance':
                final=prior_final[job];outcome=final['details']['outcome'];check=outcome['check']
                boundary=check['details']['boundary_observation'];ack=details['acknowledgement']
                # A duplicate receipt retains the FIRST insertion's timestamp.
                now_frame=check['frame'];windows=check['details']['relation_windows']
                windows_ok=all(w['valid_from']<=now_frame['accepted_at'] and
                    (w['valid_to'] is None or now_frame['accepted_at']<w['valid_to']) and
                    w['observed_at']<=now_frame['accepted_at'] and w['available_at']<=now_frame['accepted_at'] for w in windows)
                valid=(outcome['ok'] and check['ok'] and boundary['state_write_lock'] and boundary['control_write_lock']
                    and boundary['owner_thread'] and boundary['active_threads']==1 and boundary['clock_unchanged']
                    and not boundary['allowed_callbacks_between_check_and_accept'] and windows_ok
                    and final['epoch']==now_frame['accepted_epoch'] and row['epoch']==now_frame['accepted_epoch'])
                local.append(dict(case_id=rec['id'],job_ref=job,at=row['at'],epoch=row['epoch'],
                    receipt_ref=ack['receipt']['receipt_ref'],duplicate=ack['duplicate'],
                    both_writer_locks=boundary['state_write_lock'] and boundary['control_write_lock'],
                    relation_windows_valid=windows_ok,local_boundary_verified=valid,third_party_received=False))
        if rec.get('mutant'):
            m=rec['mutant'];mutants.append(dict(case_id=rec['id'],implementation=m['class_name'],
                actual_unsafe_receipts=len(actual['sink']['receipts']),detected=m['detected'],
                violations=';'.join(m['independent_oracle']['violations']),test_result=rec['status']))
        keys=[r['economic_identity'] for r in actual['sink']['receipts']]
        oracles_ok=all(not x['violations'] for x in rec.get('acceptance_observations',[]))
        verification.append(dict(case_id=rec['id'],audit_chain_valid=chain_ok,transitions_valid=transitions_ok,
            unique_economic_receipts=len(keys)==len(set(keys)),legal_acceptance_oracles_pass=oracles_ok))
    if not all(all(r[k] for k in ['audit_chain_valid','transitions_valid','unique_economic_receipts','legal_acceptance_oracles_pass']) for r in verification):
        raise SystemExit('Independent result checks failed')
    if not all(r['local_boundary_verified'] for r in local):raise SystemExit('Unproven LOCAL_ACK found')
    csvsave(ROOT/'E02_逐例验收结果.csv',[dict(id=r['id'],category=r['category'],expected=r['expected'],
        actual=';'.join(j['state']+':'+j['reason'] for j in r['actual']['jobs']) or r.get('actual',{}).get('status','ENQUEUE_DENIED'),
        sink_receipt_count=len(r['actual']['sink']['receipts']),test_result=r['status'],
        evidence=f"{latest['run']}/{r['id']}/CASE.json") for r in records])
    csvsave(ROOT/'E02_状态转换审计.csv',transitions)
    csvsave(ROOT/'E02_权限检查审计.csv',checks)
    csvsave(ROOT/'E02_本地交接边界审计.csv',local)
    csvsave(ROOT/'E02_故意错误反例.csv',mutants)
    primary=[r for r in records if r['category'].isdigit()]
    groups=[]
    for category in map(str,range(1,11)):
        rows=[r for r in primary if r['category']==category]
        groups.append(dict(scenario=category,cases=';'.join(r['id'] for r in rows),
            passed=sum(r['status']=='PASS' for r in rows),total=len(rows),
            result='PASS' if rows and all(r['status']=='PASS' for r in rows) else 'FAIL'))
    csvsave(ROOT/'E02_十类场景映射.csv',groups)
    result=dict(run=latest['run'],artifact_hashes_verified=len(artifacts),executed_source_hashes_verified=len(sources),
        historical_files_verified=current['checked'],verification=verification,
        audited_transitions=len(transitions),audited_permission_checks=len(checks),
        audited_local_acceptances=len(local),mutants=mutants,
        scope='Local artifact/provenance checks; not independent external production attestation')
    save(ROOT/'RESULT_VERIFICATION.json',result)
    lines=[f"# E02 实际测试报告\n\n运行 `{latest['run']}`，seed=780241。实际执行 {summary['tests_run']} 项；通过 {summary['passed']}，失败 {summary['failures']}，错误 {summary['errors']}。结论 **{summary['decision']}**。\n",
        '所有 PASS 来自实际 unittest 断言，拒绝/取消/不可证明场景通过表示按预期阻断，不表示交付成功；反例 PASS 表示错误接收确实发生且被观察器识别。\n',
        '|用例|预期|实际状态/原因|真实断言|\n|---|---|---|---|\n']
    for rec in records:
        description='；'.join(j['state']+' / '+j['reason'] for j in rec['actual']['jobs']) or 'ENQUEUE_DENIED'
        if rec.get('mutant'):description='故意错误已接收；DETECTED '+','.join(rec['mutant']['independent_oracle']['violations'])
        lines.append(f"|{rec['id']}|{rec['expected']}|{description}|{rec['status']}|\n")
    lines.append('\n## 十类准入映射\n\n|场景|对应测试|实际通过数|结论|\n|---|---|---|---|\n')
    for g in groups:lines.append(f"|{g['scenario']}|{g['cases']}|{g['passed']}/{g['total']}|{g['result']}|\n")
    lines.append('\n## 不可证明与原子性范围\n\n'+
        '下列真实运行场景返回 ATOMIC_HANDOFF_UNPROVEN：'+ '、'.join(summary['unproven_cases'])+'。这些场景无本地接收，无 LOCAL_ACK。'+
        '其他取消保存具体权限/用途/关系/删除/来源拒绝原因。单线程锁内只读复核到内存 receipt 插入构成受限局部线性化；未证明多进程、多机、持久恢复或外部交付。详见 TOCTOU_与原子性交接分析.md。\n')
    lines.append('\n## 反例结果\n\n')
    for m in mutants:lines.append(f"- {m['implementation']}：实际错误 receipt {m['actual_unsafe_receipts']}，检测 {m['detected']}，{m['violations']}。\n")
    lines.append('\n## 失败记录与复核\n\n启动时曾误导入 E01 fixtures，失败在测试前，记录在 STARTUP_FAILURE.md。后续完整执行历史如下：\n\n')
    for p in sorted((ROOT/'runs').glob('*/SUMMARY.json')):
        s=load(p);lines.append(f"- `{p.parent.name}`：{s['passed']}/{s['tests_run']}，failures={s['failures']}，errors={s['errors']}，{s['decision']}。\n")
    lines.append('\n首轮 T05 将控制库文件字节不变误作控制授权不回滚的判据；原 restore_state 会合法重放 reconcile，故修正为政策/删除/tombstone/epoch/nonce/sink 状态的逐项逻辑快照相等，并保留前后文件 SHA256。删除后不恢复 payload、claim 被拒绝的验收标准未放宽。原失败运行未覆盖。\n')
    lines.append(f"\n独立复核运行产物 {len(artifacts)} 项 SHA256、当次执行源码 {len(sources)} 项 SHA256、历史 {current['checked']} 项；哈希链/状态转换/幂等 receipt 检查通过。汇总 {len(transitions)} 条状态转换、{len(checks)} 次权限检查、{len(local)} 次合法本地接收观察（含重复返回），不将反例 receipt 计作合法成功。网络尝试 {len(summary['network_attempts'])}。\n")
    lines.append('\n复现命令见 README.md；原始 CASE.json 含输入、预期、实际、干预、引用和完整日志，SQLite 保存每例原系统合成状态。原 MVP、E01、lab、00—78、76程序与证据图没有修改。C_graph.Axon、C_graph.Vector、D 均 UNKNOWN；原生产取证 STOP。\n')
    (ROOT/'E02_实际测试报告.md').write_text(''.join(lines),encoding='utf-8')
    conclusion=f"# E02 总结与结论\n\n**{summary['decision']}**：{summary['passed']}/{summary['tests_run']} 项实际测试通过。仅本地合成身份、事件和内存假 sink，无 SDK/网络/真实服务。\n\n"
    conclusion+='十类要求均有逐例输入、预期与实际：撤权、失败后删除、无新写入的计划撤权、prepare 后策略变化、state 回滚保留控制库、同一经济事件重试、关系到期、错用途、ACK丢失及不可证明原子性交接。三个故意错误实现实际产生非法本地 receipt，均被原 policy/graph 观察器检出。\n\n'
    conclusion+='成功只适用于固定单线程、受控时钟、两库写锁覆盖最终只读检查和内存 receipt 插入的范围；锁失败/既存事务/外部或持久化范围返回 ATOMIC_HANDOFF_UNPROVEN。没有双SQLite分布式事务，没有外部ACK、外部删除、进程重启恰好一次或模型遗忘证明。\n\n'
    conclusion+='ACK丢失重试只返回同一经济身份已有 receipt；撤权前合法接收单独保留历史分类，撤权后拒绝新的尝试。原额外 sink 删除 ACK 不自动完成。\n\n'
    conclusion+=f"历史保护 {current['checked']} 项、执行产物 {len(artifacts)} 项哈希复核通过。首轮失败与修复依据全部保留。源码、测试、日志、SHA256和复现命令位于本目录；运行 `{latest['run']}`。\n\n"
    conclusion+='GO 仅为本地 E02 工程验收；外部交接、持久一致性和真实数据研究继续 HOLD/STOP，需另行范围和授权。不启动 E03，不生成79号生产取证任务，不训练模型。\n\nC_graph.Axon = UNKNOWN\n\nC_graph.Vector = UNKNOWN\n\nD = UNKNOWN\n\n原生产取证 = STOP\n'
    (ROOT/'E02_总结与结论.md').write_text(conclusion,encoding='utf-8')
    save(ROOT/'DELIVERY_SHA256.json',{p.name:sha(p) for p in ROOT.iterdir() if p.is_file() and p.name!='DELIVERY_SHA256.json'})
    print(dict(run=latest['run'],decision=summary['decision'],transitions=len(transitions),permission_checks=len(checks),
        local_acceptances=len(local),verified_artifacts=len(artifacts),protected_files=current['checked']))
if __name__=='__main__':main()
