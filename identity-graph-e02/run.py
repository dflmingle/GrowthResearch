"""Actual unittest execution; all artifacts written to a NEW E02 run folder."""
import sys
sys.dont_write_bytecode=True
import argparse,datetime,unittest,io,traceback,copy,sqlite3
from pathlib import Path
from e02_common import ROOT,PARENT,SEED,PURPOSE,Rejected,save,load,sha,csvsave,preservation,digest
from fixtures import Fixture
from machine import HandoffMachine,MemorySink
from counterexamples import EnqueueOnly,StaleRetryEpoch,CheckThenRevoke,observe_acceptance

NETWORK_ATTEMPTS=[]
def offline_guard(event,args):
    if event.startswith('socket.') or event in ['subprocess.Popen','os.system']:
        NETWORK_ATTEMPTS.append(event);raise RuntimeError('E02_OFFLINE_ONLY:'+event)

def eq(actual,expected):
    if actual!=expected:raise AssertionError(f'expected {expected!r}, got {actual!r}')

def cancelled(m,j,reason=None):
    eq(j.state,'CANCELLED');eq(len(m.sink.receipts),0)
    if reason:eq(j.reason,reason)

CASES=[
 ('T00_legal_local_accept','CONTROL','LOCAL_ACK; exactly one local receipt; original outbox still pending',{}),
 ('T01_revoke_after_enqueue','1','CANCELLED before claim; no receipt',{}),
 ('T02_delete_before_retry','2','failure then delete then retry CANCELLED; no receipt',{}),
 ('T03_scheduled_revoke_no_write','3','policy effective boundary observed even without new write; CANCELLED',{'scheduled_revoke':True}),
 ('T04_policy_between_prepare_and_commit','4','late revoke detected inside final boundary; CANCELLED',{}),
 ('T05_restore_old_state_keep_control','5','old state restored but durable deletion retained; no revived send',{}),
 ('T06_repeated_economic_retries','6','two failures then success; repeated economic callback stays one ledger and one acceptance',{}),
 ('T07_relation_expiry','7','at relation valid_to with no new write; CANCELLED',{'expires':True}),
 ('T08_wrong_purpose','8','other purpose cannot claim queued authorization',{}),
 ('T09_ack_loss_retry','9','sink acceptance then lost ACK; retry deduplicates to one local receipt',{}),
 ('T10_unproven_external_boundary','10','ATOMIC_HANDOFF_UNPROVEN, never LOCAL_ACK',{}),
 ('T11_mutant_enqueue_only','MUTANT','unsafe accept actually occurs; independent oracle detects unauthorized delivery',{}),
 ('T12_mutant_stale_retry_epoch','MUTANT','unsafe retry actually occurs; independent oracle detects stale epoch and revoke',{}),
 ('T13_mutant_check_revoke_commit','MUTANT','unsafe postcheck send actually occurs; independent oracle detects TOCTOU',{}),
 ('T14_final_check_relation_expiry','7','expiry inserted after prepare blocked by final check without epoch change',{'expires':True}),
 ('T15_final_check_scheduled_revoke','3','scheduled revocation inserted after prepare blocked without epoch change',{'scheduled_revoke':True}),
 ('T16_final_check_delete','4','delete between prepare and final acceptance blocked',{}),
 ('T17_transmission_disabled','EXTRA','local transmission switch can narrow but not grant policy',{}),
 ('T18_ack_loss_then_revoke','9','prior valid receipt retained as historical; retry after revoke CANCELLED; no new accept',{}),
 ('T19_state_lock_busy','10','cannot acquire original state writer exclusion: ATOMIC_HANDOFF_UNPROVEN',{}),
 ('T20_control_lock_busy','10','cannot acquire privacy writer exclusion: ATOMIC_HANDOFF_UNPROVEN',{}),
 ('T21_pending_transaction','10','pre-existing transaction not owned by handoff: ATOMIC_HANDOFF_UNPROVEN',{}),
 ('T22_terminal_replay','EXTRA','LOCAL_ACK and CANCELLED are terminal; scheduler refuses replay',{}),
 ('T23_epoch_change_revalidate','EXTRA','policy epoch changes while permissions ultimately granted; no stale snapshot fallback',{}),
 ('T24_no_account_auth_at_enqueue','EXTRA','missing accepted receipt rejected before shadow queue',{}),
 ('T25_delete_after_claim','2','claim passed then delete; pre-handoff recheck blocks old payload',{}),
 ('T26_event_payload_tamper','EXTRA','modified local outbox payload mismatches original event; reject',{}),
 ('T27_later_economic_revision','EXTRA','new source revision invalidates old snapshot; no stale economic handoff',{}),
 ('T28_unsupported_durable_restart','10','durable/restart boundary claim rejected ATOMIC_HANDOFF_UNPROVEN',{}),
 ('T29_declined_claim_is_not_delivery','EXTRA','revoked relation blocks claim; no sink attempt',{}),
]

def execute(name,f,m,case_dir,rec):
    s=f.s
    if name=='T24_no_account_auth_at_enqueue':
        req=copy.deepcopy(f.request);req['auth_receipt']=None
        rec['intervention']=dict(request=req)
        try:m.enqueue(f.outbox['id'],req)
        except Rejected as exc:rec['actual']=dict(status='DENIED',reason=str(exc))
        else:raise AssertionError('Missing receipt accepted')
        eq(len(m.jobs),0);eq(len(m.sink.receipts),0);return
    j=m.enqueue(f.outbox['id'],f.request,transmission_enabled=name!='T17_transmission_disabled')
    rec['queued_job']=copy.deepcopy(m.export()['jobs'][0]);interventions=[];rec['interventions']=interventions
    def revoke():
        interventions.append(dict(api='policy.set',entity=f.account,allowed=False,at=s.clock.now))
        s.policy.set(f.account,PURPOSE,False)
    def delete():
        interventions.append(dict(api='policy.delete',entity=f.account,at=s.clock.now,
            receipt=s.policy.delete(f.account,extra_sinks=('synthetic:e02-memory',))))
    def advance():
        old=dict(epoch=s.store.epoch,graph=s.store.graph_version)
        s.clock.advance(5);eq(dict(epoch=s.store.epoch,graph=s.store.graph_version),old)
        interventions.append(dict(api='clock.advance',seconds=5,at=s.clock.now,no_db_write=True,versions=old))
    def receipt_observer():
        receipt=next(iter(m.sink.receipts.values()))
        obs=observe_acceptance(f,receipt);rec.setdefault('acceptance_observations',[]).append(obs)
        eq(obs['violations'],[])
    if name=='T00_legal_local_accept':
        eq(m.run(j),True);eq(j.state,'LOCAL_ACK');eq(len(m.sink.receipts),1);receipt_observer()
        eq(dict(s.store.db.execute('SELECT * FROM outbox WHERE id=?',(j.outbox_ref,)).fetchone())['status'],'LOCAL_ONLY_PENDING')
    elif name=='T01_revoke_after_enqueue':revoke();eq(m.claim(j),False);cancelled(m,j)
    elif name=='T02_delete_before_retry':
        m.run(j,fail_before=True);eq(j.state,'RETRY_PENDING');delete();eq(m.claim(j),False);cancelled(m,j)
    elif name=='T03_scheduled_revoke_no_write':advance();eq(m.claim(j),False);cancelled(m,j)
    elif name=='T04_policy_between_prepare_and_commit':
        eq(m.claim(j),True);eq(m.deliver(j,before_commit=revoke),False);cancelled(m,j)
    elif name=='T05_restore_old_state_keep_control':
        backup=case_dir/'pre_delete_state.sqlite';s.backup_state(backup)
        privacy_path=s.store.directory/'privacy.sqlite';delete()
        epoch=s.store.epoch;control_hash=sha(privacy_path)
        def control_snapshot():
            return {t:[dict(x) for x in s.store.control.execute('SELECT * FROM '+t+' ORDER BY 1')]
                for t in ['control_meta','policies','deletions','erased_entities','auth_nonces','deletion_sinks']}
        authority_before=control_snapshot()
        s.restore_state(backup)
        eq(s.store.epoch,epoch);eq(s.policy.deleted(f.account),True)
        authority_after=control_snapshot()
        eq(authority_after,authority_before)
        restored=dict(s.store.db.execute('SELECT * FROM outbox WHERE id=?',(j.outbox_ref,)).fetchone())
        eq(restored['status'],'DELETED');eq(restored['payload_json'],None)
        eq(m.claim(j),False);cancelled(m,j)
        rec['restore_evidence']=dict(backup=backup.name,control_epoch=epoch,
            control_file_sha256_before=control_hash,control_file_sha256_after=sha(privacy_path),
            control_logical_before=authority_before,control_logical_after=authority_after,
            control_logical_sha256_before=digest(authority_before),control_logical_sha256_after=digest(authority_after),
            restored_outbox=restored,privacy_authority_restored=False)
    elif name=='T06_repeated_economic_retries':
        # Original event/economic de-duplication runs BEFORE enqueue snapshot:
        # same duplicate payload returns DUPLICATE_EVENT without new ledger.
        duplicate=f.w.revenue(f.app,7_000_000,account=f.account,event_id='synth:e02:event:1',economic_key='synth:e02:economic:1')
        eq(duplicate['status'],'DUPLICATE_EVENT');rec['duplicate_event']=duplicate
        duplicate_ledger=f.w.revenue(f.app,7_000_000,account=f.account,event_id='synth:e02:second-callback',economic_key='synth:e02:economic:1')
        eq(duplicate_ledger['status'],'DUPLICATE_LEDGER');rec['duplicate_economic_callback']=duplicate_ledger
        eq(s.store.db.execute('SELECT COUNT(*) FROM outbox').fetchone()[0],1)
        for _ in range(2):m.run(j,fail_before=True);eq(j.state,'RETRY_PENDING');eq(len(m.sink.receipts),0)
        eq(m.run(j),True);eq(j.claims,3);eq(j.state,'LOCAL_ACK');eq(len(m.sink.receipts),1)
        eq(s.store.db.execute('SELECT COUNT(*) FROM ledger').fetchone()[0],1);receipt_observer()
    elif name=='T07_relation_expiry':advance();eq(m.claim(j),False);cancelled(m,j)
    elif name=='T08_wrong_purpose':eq(m.claim(j,purpose='synthetic-unrelated-purpose'),False);cancelled(m,j,'TASK_PURPOSE_NOT_REUSABLE')
    elif name=='T09_ack_loss_retry':
        eq(m.run(j,lose_ack=True),False);eq(j.state,'RETRY_PENDING');eq(len(m.sink.receipts),1);receipt_observer()
        eq(m.run(j),True);eq(j.state,'LOCAL_ACK');eq(len(m.sink.receipts),1);eq(m.sink.calls,2)
        eq(j.last_ack['duplicate'],True);receipt_observer()
    elif name in ['T10_unproven_external_boundary','T28_unsupported_durable_restart']:
        m.boundary='external_sink' if name.startswith('T10') else 'durable_restart'
        eq(m.run(j),False);cancelled(m,j,'ATOMIC_HANDOFF_UNPROVEN')
    elif name in ['T11_mutant_enqueue_only','T12_mutant_stale_retry_epoch','T13_mutant_check_revoke_commit']:
        if name.startswith('T11'):
            mutant=EnqueueOnly(m,j);revoke();out=mutant.attempt()
        elif name.startswith('T12'):
            mutant=StaleRetryEpoch(m,j);mutant.first_failure();revoke();out=mutant.attempt()
        else:mutant=CheckThenRevoke(m,j);out=mutant.attempt(revoke)
        observed=observe_acceptance(f,out['receipt']);rec['mutant']=dict(class_name=type(mutant).__name__,
            unsafe_acceptance=out,independent_oracle=observed,detected=bool(observed['violations']))
        eq(len(m.sink.receipts),1);eq('UNAUTHORIZED_AT_ACTUAL_HANDOFF' in observed['violations'],True)
        eq('STALE_ACCEPTANCE_EPOCH' in observed['violations'],True)
    elif name in ['T14_final_check_relation_expiry','T15_final_check_scheduled_revoke']:
        eq(m.claim(j),True);eq(m.deliver(j,before_commit=advance),False);cancelled(m,j)
    elif name=='T16_final_check_delete':eq(m.claim(j),True);eq(m.deliver(j,before_commit=delete),False);cancelled(m,j)
    elif name=='T17_transmission_disabled':eq(m.claim(j),False);cancelled(m,j,'LOCAL_TRANSMISSION_DISABLED')
    elif name=='T18_ack_loss_then_revoke':
        m.run(j,lose_ack=True);eq(j.state,'RETRY_PENDING');receipt_observer()
        old=copy.deepcopy(list(m.sink.receipts.values()));calls=m.sink.calls;revoke()
        eq(m.claim(j),False);eq(j.state,'CANCELLED');eq(m.sink.calls,calls);eq(list(m.sink.receipts.values()),old)
        rec['prior_receipt_classification']='VALID_LOCAL_ACCEPTANCE_BEFORE_REVOKE_NOT_RETRACTED_NOT_NEW_DELIVERY'
    elif name in ['T19_state_lock_busy','T20_control_lock_busy']:
        path=s.store.directory/('state.sqlite' if name.startswith('T19') else 'privacy.sqlite')
        blocker=sqlite3.connect(str(path),timeout=0)
        def block():blocker.execute('BEGIN IMMEDIATE');interventions.append(dict(api='sqlite.BEGIN_IMMEDIATE',database=path.name))
        try:eq(m.claim(j),True);eq(m.deliver(j,before_commit=block),False)
        finally:blocker.rollback();blocker.close()
        cancelled(m,j,'ATOMIC_HANDOFF_UNPROVEN')
        eq(s.store.db.in_transaction,False);eq(s.store.control.in_transaction,False)
    elif name=='T21_pending_transaction':
        def opened():s.store.control.execute('BEGIN IMMEDIATE');interventions.append(dict(api='foreign_owned_transaction'))
        try:eq(m.claim(j),True);eq(m.deliver(j,before_commit=opened),False)
        finally:s.store.control.rollback()
        cancelled(m,j,'ATOMIC_HANDOFF_UNPROVEN')
    elif name=='T22_terminal_replay':
        m.run(j);eq(j.state,'LOCAL_ACK');receipt_observer();calls=m.sink.calls
        try:m.claim(j)
        except Rejected as exc:eq(str(exc),'JOB_NOT_CLAIMABLE')
        else:raise AssertionError('Terminal job replayed')
        eq(m.sink.calls,calls)
        denied=m.enqueue(f.outbox['id'],f.request,transmission_enabled=False)
        eq(m.claim(denied),False);eq(denied.state,'CANCELLED')
        try:m.claim(denied)
        except Rejected as exc:eq(str(exc),'JOB_NOT_CLAIMABLE')
        else:raise AssertionError('Cancelled job replayed')
        eq(m.sink.calls,calls)
    elif name=='T23_epoch_change_revalidate':
        before=s.store.epoch;s.policy.set(f.account,PURPOSE,True)
        interventions.append(dict(api='policy.set',allowed=True,old_epoch=before,new_epoch=s.store.epoch))
        eq(m.claim(j),False);cancelled(m,j,'ORIGINAL_BUNDLE_INVALIDATED')
    elif name=='T25_delete_after_claim':eq(m.claim(j),True);delete();eq(m.deliver(j),False);cancelled(m,j)
    elif name=='T26_event_payload_tamper':
        with s.store.db:s.store.db.execute('UPDATE outbox SET payload_json=? WHERE id=?',('{"synthetic_tamper":true}',j.outbox_ref))
        interventions.append(dict(api='LOCAL_DB_FAULT_INJECTION',field='outbox.payload_json'))
        eq(m.claim(j),False);cancelled(m,j,'OUTBOX_EVENT_PAYLOAD_MISMATCH')
    elif name=='T27_later_economic_revision':
        revision=f.w.revenue(f.app,2_000_000,account=f.account,event_id='synth:e02:event:revision2',
            economic_key='synth:e02:economic:1',revision=2,correction_of=f.revenue['ledger_ref'])
        interventions.append(dict(api='original.events.ingest',correction=revision))
        eq(m.claim(j),False);cancelled(m,j)
    elif name=='T29_declined_claim_is_not_delivery':
        s.graph.revoke(f.login_edge);interventions.append(dict(api='graph.revoke',edge_ref=f.login_edge))
        eq(m.claim(j),False);cancelled(m,j);eq(m.sink.calls,0)
    else:raise AssertionError('UNIMPLEMENTED_CASE:'+name)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output');args=parser.parse_args()
    runid=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    out=Path(args.output).resolve() if args.output else ROOT/'runs'/runid
    if not out.is_relative_to(ROOT) or out.exists():raise SystemExit('Need a NEW output directory inside E02')
    out.mkdir(parents=True);sys.addaudithook(offline_guard)
    before=preservation()
    if before['mismatches']:raise SystemExit('Historical files changed: '+repr(before))
    eq(sha(ROOT/'PROTOCOL.json'),load(ROOT/'PROTOCOL_SHA256.json')['sha256'])
    for r in load(ROOT/'REUSED_SOURCES.json'):eq(sha(PARENT/r['path']),r['sha256'])
    save(out/'SOURCE_SHA256.json',{p.name:sha(p) for p in ROOT.glob('*.py')})
    save(out/'PARAMETERS.json',dict(seed=SEED,run_id=runid,python=sys.version,protocol=load(ROOT/'PROTOCOL.json'),
        timing='UTC integer seconds; clock advances only through scheduled actions',network='ALL_SOCKET_AUDIT_EVENTS_AND_SUBPROCESS_DENIED'))
    suite=unittest.TestSuite();records=[]
    def build(name,category,expected,options):
        def test():
            d=out/name;d.mkdir();f=None;m=None
            rec=dict(id=name,category=category,expected=expected,options=options,seed=SEED,status='RUNNING')
            try:
                f=Fixture(d/'db',**options);m=HandoffMachine(f.s);rec['input']=f.manifest()
                execute(name,f,m,d,rec)
                eq(m.audit.verify(),True);eq(f.s.audit.verify(),True)
                rec['status']='PASS'
            except Exception:
                rec['status']='FAIL';rec['error']=traceback.format_exc();raise
            finally:
                if m:rec['actual']=m.export();save(d/'STATE_MACHINE_LOG.json',m.audit.records)
                if f:
                    save(d/'MVP_AUDIT_LOG.json',f.s.audit.records())
                    save(d/'CONTROL_STATE.json',{table:[dict(r) for r in f.s.store.control.execute('SELECT * FROM '+table)]
                        for table in ['policies','deletions','erased_entities','auth_nonces','deletion_sinks']})
                    save(d/'FINAL_SOURCE_STATE.json',{table:[dict(r) for r in f.s.store.db.execute('SELECT * FROM '+table)]
                        for table in ['outbox','events','ledger','edge_revisions']})
                    f.close()
                save(d/'CASE.json',rec);records.append(rec)
        return unittest.FunctionTestCase(test,description=name+' — '+expected)
    for row in CASES:suite.addTest(build(*row))
    stream=io.StringIO();testresult=unittest.TextTestRunner(stream=stream,verbosity=2).run(suite)
    (out/'unittest.log').write_text(stream.getvalue(),encoding='utf-8')
    after=preservation();save(out/'PRESERVATION_CHECK.json',dict(before=before,after=after))
    csvsave(out/'CASE_RESULTS.csv',[dict(id=r['id'],category=r['category'],status=r['status'],expected=r['expected'],
        actual_states=';'.join(j['state']+':'+j['reason'] for j in r.get('actual',{}).get('jobs',[])),evidence=r['id']+'/CASE.json') for r in records])
    success=testresult.wasSuccessful() and not after['mismatches'] and not NETWORK_ATTEMPTS
    mutants=[dict(id=r['id'],detected=r.get('mutant',{}).get('detected',False),status=r['status']) for r in records if r['category']=='MUTANT']
    summary=dict(scope='E02_ONLY_LOCAL_SYNTHETIC',seed=SEED,tests_run=testresult.testsRun,
        passed=sum(r['status']=='PASS' for r in records),failures=len(testresult.failures),errors=len(testresult.errors),
        mutants=mutants,network_attempts=NETWORK_ATTEMPTS,preservation=after,
        unproven_cases=[r['id'] for r in records if any(j['reason']=='ATOMIC_HANDOFF_UNPROVEN' for j in r.get('actual',{}).get('jobs',[]))],
        decision='GO_LOCAL_E02_ONLY' if success else 'HOLD',
        atomic_scope='Single trusted thread; original SQLite writer exclusion; memory insertion only. No durable/external/distributed/crash guarantee.',
        C_graph_Axon='UNKNOWN',C_graph_Vector='UNKNOWN',D='UNKNOWN',production_forensics='STOP')
    save(out/'SUMMARY.json',summary)
    save(out/'ARTIFACT_SHA256.json',{p.relative_to(out).as_posix():sha(p) for p in out.rglob('*') if p.is_file()})
    save(ROOT/'LATEST_RUN.json',dict(run=out.relative_to(ROOT).as_posix(),summary=summary))
    print(stream.getvalue());print(summary)
    return 0 if success else 1
if __name__=='__main__':raise SystemExit(main())
