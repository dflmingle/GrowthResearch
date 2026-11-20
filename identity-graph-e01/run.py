"""Execute only E01; unittest checks and immutable per-run local artifacts."""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import json, datetime, argparse, unittest, traceback, copy, io
from common import ROOT,PARENT,SEED,PURPOSE,Rejected,GraphAdapter,save,load,sha,csvsave
from fixtures import Scenario
from adapter import TaskAwareAdapter
from counterexamples import faulty,partition_violations

NETWORK_EVENTS=[]
def network_guard(event,args):
    if event in {'socket.connect','socket.connect_ex','socket.sendto','socket.bind','socket.getaddrinfo','subprocess.Popen','os.system'}:
        NETWORK_EVENTS.append(event)
        raise RuntimeError('E01_OFFLINE_ONLY:'+event)

def equal(actual,expected):
    if actual!=expected:raise AssertionError(f'expected {expected!r}, got {actual!r}')

def status(result,value):equal(result.get('status'),value)

def approved(result,source=7_000_000,target=3_000_000):
    equal(partition_violations(result,source=source,target=target),[])
    return result

def original(s,account,since):
    try:
        b=s.features.compute(account,as_of=s.clock.now,since_at=since,purpose=PURPOSE)
        return dict(status='OK',bundle=b,read=s.features.read(b['bundle_ref'],purpose=PURPOSE))
    except Rejected as exc:return dict(status='DENIED',reason=str(exc))

def cases():
    return [
      ('C01_three_routes','A rejects shared device; B account total=10; C source=7,target=3,B99 excluded',{}),
      ('C02_missing_receipt','DENIED without accepted resolver receipt',{}),
      ('C03_bare_account','DENIED bare account_ref input',{}),
      ('C04_wrong_receipt_app','DENIED receipt from source installation',{}),
      ('C05_other_account_receipt','DENIED unrelated account receipt',{}),
      ('C06_namespace_collision','different namespaces same token stay separate; source=7',{}),
      ('C07_bad_signature','original resolver rejects altered signature',{}),
      ('C08_expired_assertion','original resolver rejects expired login proof',{}),
      ('C09_revoke_source','old snapshot denied; fresh source unobserved',{}),
      ('C10_revoke_target','old snapshot and new request denied',{}),
      ('C11_revoke_consent','old snapshot denied; fresh excludes revoked source',{}),
      ('C12_delete_source','old snapshot denied; fresh excludes deleted source',{}),
      ('C13_expiry_no_write','at valid_to with no graph/epoch change old snapshot denied; fresh excludes source',{'expiry':True}),
      ('C14_scheduled_revoke_no_write','at effective_at with no subsequent write old snapshot denied; source excluded',{}),
      ('C15_late_event','future-available 41 excluded at prediction; source=7',{}),
      ('C16_late_relation','future-available login excluded; no source history',{}),
      ('C17_negative_amount','source=-7 preserved; target=3',{'source_amount':-7_000_000}),
      ('C18_missing_observation','no source rows and MISSING coverage != complete zero',{'source_amount':None,'source_coverage':'MISSING'}),
      ('C19_complete_zero','no source rows and COMPLETE coverage = known zero',{'source_amount':None}),
      ('C20_missing_lineage','UNSUPPORTED_PARTITION; no fallback',{}),
      ('C21_lineage_disagreement','UNSUPPORTED_PARTITION; no fallback',{}),
      ('C22_source_policy_exclusion','approved source refs never include revoked source',{}),
      ('C23_wrong_purpose','DENIED purpose mismatch',{}),
      ('C24_wrong_context','DENIED environment mismatch',{}),
      ('C25_backdated_prediction','DENIED late feature materialization/backdated task',{}),
      ('C26_future_prediction','DENIED future task',{}),
      ('C27_mutant_account','deliberately faulty account adapter detected',{}),
      ('C28_mutant_partition','deliberately faulty mixed-app adapter detected',{}),
      ('C29_mutant_late','deliberately faulty late-information adapter detected',{}),
      ('C30_target_reinstall','same product reinstall remains target history; source=7,target=5',{}),
      ('C31_reset_target_device','reset blocks old and current target task',{}),
      ('C32_receipt_after_assertion_ttl','accepted receipt not incorrectly treated as expired login proof',{}),
      ('C33_delete_account','old snapshot and current task denied',{}),
      ('C34_missing_account_values','UNSUPPORTED_PARTITION on incomplete original API schema',{}),
      ('C35_multi_currency','no implicit currency conversion; signed amounts partitioned by currency',{}),
      ('C36_only_approved_pk_reads','partition SQL reads exact approved primary keys only',{}),
      ('C37_expired_target_relation','target relation expiry rejects current and old read',{}),
      ('C38_no_target_auth_fallback','revoked target auth cannot fall back to shared-device identity',{}),
    ]

def execute(name,f,record):
    s=f.s;adapter=TaskAwareAdapter(s);req=f.request()
    record['input']=dict(task=req,fixture=f.manifest())
    result=None
    if name.startswith('C01'):
        a=GraphAdapter(s).extract(f.d1,s.clock.now,f.w.start)
        b=original(s,f.a,f.w.start);c=adapter.extract(req)
        record['actual']=dict(A_device=a,B_original_account=b,C_task=c)
        equal(a['eligible'],False);equal(a['reason'],'SHARED_DEVICE_ACCOUNT_AMBIGUITY')
        equal(b['read']['values']['observed_revenue_micros'],10_000_000);approved(c)
        equal(len(c['ledger_refs']),2)
        equal(c['cross_app_history']['observation_status'],'OBSERVED_COMPLETE')
        equal(c['target_app_history']['observation_status'],'OBSERVED_COMPLETE')
        return
    if name.startswith(('C02','C03','C04','C05','C23','C24','C25','C26')):
        if name.startswith('C02'):req['auth_receipt']=None
        elif name.startswith('C03'):req['account_ref']=f.a
        elif name.startswith('C04'):req['auth_receipt']=f.receipts['xa']
        elif name.startswith('C05'):req['auth_receipt']=f.receipts['xb']
        elif name.startswith('C23'):req['purpose']='synthetic-other-purpose'
        elif name.startswith('C24'):req['authorization_context']['environment']='PRODUCTION'
        elif name.startswith('C25'):s.clock.advance();req['prediction_at']=f.w.start
        elif name.startswith('C26'):req['prediction_at']+=1
        record['input']['task']=copy.deepcopy(req)
        result=adapter.extract(req);record['actual']=result;status(result,'DENIED');return
    if name.startswith('C06'):
        ns_a=s.store.entity(f.a)['namespace_id']
        stranger=f.w.entity('A_other_namespace','account',issuer='synthetic:unmapped-issuer',token='syn:account:A')
        app=f.w.install('X_stranger',f.d1,app='synthetic-X')
        f.w.login(stranger,app,f.d1);r=f.w.revenue(app,88_000_000,account=stranger)
        record['intervention']=dict(same_raw_token=True,account=f.a,stranger=stranger,namespace_a=ns_a,
            namespace_other=s.store.entity(stranger)['namespace_id'],ledger=r)
        equal(s.namespaces.compare(f.a,stranger),'DIFFERENT_NAMESPACE')
        result=adapter.extract(req);record['actual']=result;approved(result)
        equal(r['ledger_ref'] in result['ledger_refs'],False);return
    if name.startswith(('C07','C08')):
        assertion,signature=f.w.assertion(f.a,f.y,f.d2,**({'expires_at':s.clock.now} if name.startswith('C08') else {}))
        if name.startswith('C07'):signature='0'*64
        record['intervention']=dict(assertion=assertion,signature=signature)
        try:s.resolver.login(assertion,signature)
        except Rejected as exc:result=dict(status='DENIED',reason=str(exc))
        else:result=dict(status='INCORRECTLY_ACCEPTED')
        record['actual']=result;status(result,'DENIED')
        equal(result['reason'],'AUTH_TIME_INVALID' if name.startswith('C08') else 'BAD_FIXTURE_SIGNATURE');return
    if name.startswith(('C09','C10','C11','C12','C13','C14','C22','C31','C33','C37','C38')):
        if name.startswith('C14'):
            s.policy.set(f.xa,PURPOSE,False,effective_at=s.clock.now+5)
        if name.startswith('C37'):
            s.graph.revoke(f.login_refs['y'])
            s.graph.add(f.y,f.a,'logged_in_as',source_ref='synth:target-expiry',valid_to=s.clock.now+5,
                quality_kind='authenticated_account_control',auth_receipt=f.receipts['y'])
        prior=adapter.extract(req);approved(prior)
        before=dict(graph=s.store.graph_version,epoch=s.store.epoch)
        if name.startswith(('C09','C10','C38')):
            ref=f.login_refs['xa'] if name.startswith('C09') else f.login_refs['y']
            s.graph.revoke(ref);record['intervention']=dict(api='graph.revoke',edge_ref=ref)
        elif name.startswith(('C11','C22')):
            s.policy.set(f.xa,PURPOSE,False);record['intervention']=dict(api='policy.set',entity=f.xa,allowed=False)
        elif name.startswith(('C12','C33')):
            who=f.a if name.startswith('C33') else f.xa
            deletion=s.policy.delete(who);record['intervention']=dict(api='policy.delete',entity=who,receipt=deletion)
        elif name.startswith('C31'):
            record['intervention']=dict(api='graph.reset_device',actual=s.graph.reset_device(f.d2))
        else:
            s.clock.advance(5);record['intervention']=dict(api='clock.advance',seconds=5,at=s.clock.now)
            equal(dict(graph=s.store.graph_version,epoch=s.store.epoch),before)
        current=f.request();old=adapter.reread(current,prior)
        fresh=adapter.extract(current)
        record['actual']=dict(prior=prior,reread=old,fresh=fresh,versions_before=before,
            versions_after=dict(graph=s.store.graph_version,epoch=s.store.epoch))
        status(old,'DENIED')
        if name.startswith(('C10','C31','C33','C37','C38')):status(fresh,'DENIED')
        else:
            approved(fresh,source=0)
            equal(fresh['cross_app_history']['observation_status'],'UNOBSERVED')
            equal(fresh['cross_app_history']['complete_amount_by_currency_micros'],None)
        return
    if name.startswith(('C15','C16','C29')):
        if name.startswith('C16'):
            s.graph.revoke(f.login_refs['xa'])
            change=s.graph.add(f.xa,f.a,'logged_in_as',source_ref='synth:late-relation',valid_from=f.w.start,
                available_at=s.clock.now+10,quality_kind='authenticated_account_control',auth_receipt=f.receipts['xa'])
        else:change=f.w.revenue(f.xa,41_000_000,account=f.a,available_at=s.clock.now+10)
        record['intervention']=dict(available_at=s.clock.now+10,api='graph.add' if name.startswith('C16') else 'fixture.revenue',actual=change)
        result=adapter.extract(req);record['actual']=result
        approved(result,source=0 if name.startswith('C16') else 7_000_000)
        if name.startswith('C15'):equal(change['ledger_ref'] in result['ledger_refs'],False)
        if name.startswith('C29'):
            mutation=faulty(result,'late_information_leak');violations=partition_violations(mutation)
            record['actual']=dict(correct=result,faulty=mutation,detected=violations)
            equal('SOURCE_AMOUNT_MISMATCH' in violations,True)
        return
    if name.startswith('C17'):
        result=adapter.extract(req);record['actual']=result;approved(result,source=-7_000_000)
        equal(result['cross_app_history']['complete_amount_by_currency_micros'],{'USD':-7_000_000});return
    if name.startswith(('C18','C19')):
        result=adapter.extract(req);record['actual']=result;approved(result,source=0)
        group=result['cross_app_history']
        equal(group['observation_status'],'NOT_FULLY_OBSERVED' if name.startswith('C18') else 'KNOWN_ZERO')
        equal(group['complete_amount_by_currency_micros'],None if name.startswith('C18') else {'USD':0});return
    if name.startswith(('C20','C21','C34')):
        real=s.features.compute
        def incomplete(*a,**k):
            value=real(*a,**k)
            if name.startswith('C20'):value.pop('lineage')
            else:value['lineage']['event_refs']=[]
            return value
        if name.startswith('C34'):
            real_read=s.features.read
            def incomplete_read(*a,**k):
                value=real_read(*a,**k);value['values'].pop('observed_ledger_count');return value
            s.features.read=incomplete_read
        else:s.features.compute=incomplete
        record['intervention']=dict(kind='LOCAL_API_RESPONSE_DEGRADATION_ONLY',field='values' if name.startswith('C34') else 'lineage')
        result=adapter.extract(req);record['actual']=result;status(result,'UNSUPPORTED_PARTITION')
        equal(result['cross_app_history'],None);return
    if name.startswith(('C27','C28')):
        result=adapter.extract(req);approved(result)
        mutation=faulty(result,'account_contamination' if name.startswith('C27') else 'source_target_mix')
        violations=partition_violations(mutation)
        record['actual']=dict(correct=result,faulty=mutation,detected=violations)
        equal('SOURCE_AMOUNT_MISMATCH' in violations,True);return
    if name.startswith('C30'):
        install=f.w.install('Y_reinstall',f.d1,app='synthetic-Y');f.w.login(f.a,install,f.d1)
        event=f.w.revenue(install,2_000_000,account=f.a)
        record['intervention']=dict(install=install,event=event)
        result=adapter.extract(req);record['actual']=result;approved(result,target=5_000_000)
        equal(event['ledger_ref'] in result['target_app_history']['ledger_refs'],True);return
    if name.startswith('C32'):
        s.clock.advance(61);record['intervention']=dict(at=s.clock.now,assertion_expires_at=f.w.start+60)
        result=adapter.extract(f.request());record['actual']=result;approved(result);return
    if name.startswith('C35'):
        event=f.w.revenue(f.xa,-2_000_000,account=f.a,currency='EUR')
        record['intervention']=dict(event=event,currency='EUR',amount=-2_000_000)
        result=adapter.extract(req);record['actual']=result;status(result,'OK')
        equal(result['cross_app_history']['observed_amount_by_currency_micros'],{'USD':7_000_000,'EUR':-2_000_000})
        equal(result['original_account_values']['observed_revenue_micros'],None)
        equal(result['observation_status'],'MIXED_CURRENCY');return
    if name.startswith('C36'):
        binding=adapter._binding(req);bundle=s.features.compute(f.a,as_of=s.clock.now,since_at=f.w.start,purpose=PURPOSE)
        read=s.features.read(bundle['bundle_ref'],purpose=PURPOSE);sql=[]
        s.store.db.set_trace_callback(sql.append)
        try:parts=adapter._partition(req,binding,bundle,read)
        finally:s.store.db.set_trace_callback(None)
        lookups=[q for q in sql if 'FROM ledger' in q or 'FROM events' in q or 'FROM coverage' in q]
        record['actual']=dict(partitions=parts,partition_source_sql=lookups,approved_lineage=bundle['lineage'])
        equal(len(lookups)>0,True)
        for query in lookups:
            equal(' WHERE id=' in query,True)
            table=query.split('FROM ')[1].split(' ')[0]
            key={'ledger':'ledger_refs','events':'event_refs','coverage':'coverage_refs'}[table]
            equal(any("id='"+ref+"'" in query for ref in bundle['lineage'][key]),True)
        return
    raise AssertionError('UNIMPLEMENTED_CASE:'+name)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',default=None);args=parser.parse_args()
    run_id=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    out=Path(args.output).resolve() if args.output else ROOT/'runs'/run_id
    if not out.is_relative_to(ROOT) or out.exists():raise SystemExit('Output must be a NEW directory inside identity-graph-e01')
    out.mkdir(parents=True)
    sys.addaudithook(network_guard)
    baseline=load(ROOT/'PRESERVATION_BASELINE.json')
    before=[p for p,h in baseline.items() if not (PARENT/p).is_file() or sha(PARENT/p)!=h]
    if before:raise SystemExit('Historical integrity failed before execution: '+repr(before))
    equal(sha(ROOT/'PROTOCOL.json'),load(ROOT/'PROTOCOL_HASH.json')['sha256'])
    for item in load(ROOT/'REUSED_SOURCES.json'):equal(sha(PARENT/item['path']),item['sha256'])
    source_manifest={p.relative_to(ROOT).as_posix():sha(p) for p in ROOT.glob('*.py')}
    save(out/'SOURCE_SHA256.json',source_manifest)
    save(out/'PARAMETERS.json',dict(seed=SEED,protocol=load(ROOT/'PROTOCOL.json'),python=sys.version,
        scope='E01_ONLY_NO_MODELS',network_guard='DENY_SOCKET_AND_SUBPROCESS',run_id=run_id))
    allrecords=[];suite=unittest.TestSuite()
    def make_test(name,expected,options):
        def test():
            case_dir=out/name;case_dir.mkdir()
            rec=dict(id=name,seed=SEED,expected=expected,options=options,status='RUNNING')
            f=None
            try:
                f=Scenario(case_dir/'db',**options)
                execute(name,f,rec)
                equal(f.s.audit.verify(),True)
                rec['status']='PASS'
            except Exception:
                rec['status']='FAIL';rec['error']=traceback.format_exc();raise
            finally:
                if f:
                    rec['final_fixture']=f.manifest()
                    save(case_dir/'MVP_AUDIT_LOG.json',f.s.audit.records())
                    save(case_dir/'FINAL_POLICY.json',[dict(x) for x in f.s.store.control.execute('SELECT * FROM policies ORDER BY epoch')])
                    f.close()
                save(case_dir/'CASE.json',rec);allrecords.append(rec)
        return unittest.FunctionTestCase(test,description=name+' — '+expected)
    for name,expected,options in cases():suite.addTest(make_test(name,expected,options))
    stream=io.StringIO();result=unittest.TextTestRunner(stream=stream,verbosity=2).run(suite)
    (out/'unittest.log').write_text(stream.getvalue(),encoding='utf-8')
    after=[p for p,h in baseline.items() if not (PARENT/p).is_file() or sha(PARENT/p)!=h]
    preservation=dict(checked=len(baseline),before_mismatches=before,after_mismatches=after)
    save(out/'PRESERVATION_CHECK.json',preservation)
    csvsave(out/'CASE_RESULTS.csv',[dict(id=r['id'],status=r['status'],expected=r['expected'],case_json=r['id']+'/CASE.json') for r in allrecords])
    success=result.wasSuccessful() and not after and not NETWORK_EVENTS
    summary=dict(scope='E01_LOCAL_SYNTHETIC_ONLY',seed=SEED,tests_run=result.testsRun,
        passed=sum(r['status']=='PASS' for r in allrecords),failures=len(result.failures),errors=len(result.errors),
        unsupported_handling_tests=[r['id'] for r in allrecords if 'UNSUPPORTED_PARTITION' in r['expected']],
        deliberate_faults_detected=[r['id'] for r in allrecords if r['id'].startswith(('C27','C28','C29')) and r['status']=='PASS'],
        network_attempts=NETWORK_EVENTS,preservation=preservation,
        decision='GO_LOCAL_E01_ONLY' if success else 'HOLD_IMPLEMENTATION_FAILURE',
        C_graph_Axon='UNKNOWN',C_graph_Vector='UNKNOWN',D='UNKNOWN',production_forensics='STOP')
    save(out/'SUMMARY.json',summary)
    artifacts={p.relative_to(out).as_posix():sha(p) for p in out.rglob('*') if p.is_file()}
    save(out/'ARTIFACT_SHA256.json',artifacts)
    save(ROOT/'LATEST_RUN.json',dict(run=out.relative_to(ROOT).as_posix(),summary=summary))
    print(stream.getvalue());print(json.dumps(summary,ensure_ascii=False,indent=2))
    return 0 if success else 1

if __name__=='__main__':raise SystemExit(main())
