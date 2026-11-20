"""Actual local lifecycle interventions plus explicit rejected leakage probes."""
from .common import BASE,DAY,LabWorld,to_time,save,guard_feature,Rejected,PURPOSE
from .adapter import GraphAdapter
def maturity_admission(rows,horizon):
    train=[r for r in rows if r['split']=='train'];validation=[r for r in rows if r['split']=='validation'];test=[r for r in rows if r['split']=='test']
    failures=[]
    if not train or not validation or not test:failures.append('EMPTY_STAGE')
    else:
        if max(r[f'mature_D{horizon}'] for r in train)>=min(r['prediction_at'] for r in validation):failures.append('TRAIN_LABEL_NOT_MATURE_BEFORE_VALIDATION')
        if max(r[f'mature_D{horizon}'] for r in validation)>=min(r['prediction_at'] for r in test):failures.append('VALIDATION_LABEL_NOT_MATURE_BEFORE_TEST')
    return dict(status='STOP' if failures else 'GO_SYNTHETIC_ONLY',failures=failures,horizon=horizon,
        train_last_mature=max([r[f'mature_D{horizon}'] for r in train],default=None),validation_first_prediction=min([r['prediction_at'] for r in validation],default=None),
        validation_last_mature=max([r[f'mature_D{horizon}'] for r in validation],default=None),test_first_prediction=min([r['prediction_at'] for r in test],default=None))
def run_engine_probes(out):
    probes=[];paths=[]
    def check(name,expected,actual,inputs):
        row=dict(name=name,inputs=inputs,expected=expected,actual=actual,passed=expected==actual);probes.append(row)
        if expected!=actual:raise AssertionError(row)
    def rejected(call):
        try:call()
        except Rejected as exc:return str(exc)
        return 'NOT_REJECTED'
    # Confidence changes never turn an uncalibrated candidate into an active edge.
    w=LabWorld(out/'probes/confidence',731,BASE);s=w.system
    try:
        d=w.entity('target','device');donor=w.entity('donor','device');app=w.install('donor-app',donor);w.revenue(app,5000000)
        for confidence in [.2,.6,.99]:
            e=s.graph.add(d,donor,'candidate_same_entity',source_ref='synth:uncalibrated-candidate',confidence=confidence)
            f=GraphAdapter(s).extract(d,s.clock.now,BASE)
            check('candidate_'+str(confidence),dict(status='CANDIDATE',eligible=False),dict(status=e['status'],eligible=f['eligible']),dict(confidence=confidence,edge=e))
        save(out/'probes/confidence/AUDIT.json',s.audit.records())
    finally:w.close()
    # Wrong merge cannot be detected from a falsely attested but otherwise valid
    # relation alone. Show both this limitation and an explicit cannot-link guard.
    w=LabWorld(out/'probes/wrong-merge',732,BASE);s=w.system
    try:
        target=w.entity('target','device');donor=w.entity('donor','device');app=w.install('donor-app',donor);w.revenue(app,9000000)
        s.graph.add(target,donor,'same_device',source_ref='synth:deliberately-wrong-attestation')
        f=GraphAdapter(s).extract(target,s.clock.now,BASE)
        check('wrong_attestation_can_contaminate_without_truth',True,f['eligible'],dict(injected_false_relation=True,claim='NOT_DETECTABLE_WITHOUT_EXTRA_EVIDENCE'))
        s.graph.add(target,donor,'cannot_link',source_ref='synth:known-distinct-counterevidence')
        f=GraphAdapter(s).extract(target,s.clock.now,BASE)
        check('explicit_counterevidence_breaks_bad_component',False,f['eligible'],dict(cannot_link=True))
        save(out/'probes/wrong-merge/AUDIT.json',s.audit.records())
    finally:w.close()
    for action in ['revoke','delete','consent']:
        w=LabWorld(out/'probes'/action,733,BASE);s=w.system
        try:
            target=w.entity('target','device');donor=w.entity('donor','device');app=w.install('donor-app',donor);w.revenue(app,3000000)
            edge=s.graph.add(target,donor,'same_device',source_ref='synth:authorized-alias')
            before=GraphAdapter(s).extract(target,s.clock.now,BASE);bid=before['bundle']['bundle_ref']
            check(action+'_before_eligible',True,before['eligible'],dict(bundle_ref=bid))
            s.clock.advance()
            if action=='revoke':s.graph.revoke(edge['edge_ref'],reason='synth:relation-revoked')
            elif action=='delete':s.policy.delete(donor)
            else:s.policy.set(target,PURPOSE,False,source_ref='synth:consent-revoked')
            result=rejected(lambda:s.features.read(bid))
            check(action+'_old_bundle_denied','BUNDLE_INVALIDATED_OR_DELETED',result,dict(action=action,effective_at=s.clock.now))
            check(action+'_new_query_denied_or_missing',False,GraphAdapter(s).extract(target,s.clock.now,BASE)['eligible'],dict(action=action))
            save(out/'probes'/action/'AUDIT.json',s.audit.records())
        finally:w.close()
    # Shared-device task ambiguity: actual MVP device view has both accounts;
    # adapter refuses to relabel this as installation/account-specific value.
    w=LabWorld(out/'probes/shared',734,BASE);s=w.system
    try:
        d=w.entity('shared-device','device');app=w.install('shared-app',d)
        for name,value in [('account-A',1000000),('account-B',9000000)]:
            a=w.entity(name,'account');w.login(a,app,d);w.revenue(app,value,account=a)
        f=GraphAdapter(s).extract(d,s.clock.now,BASE)
        check('shared_device_account_ambiguity','SHARED_DEVICE_ACCOUNT_AMBIGUITY',f['reason'],dict(account_count=2,raw_device_observed_micros=f['bundle']['values']['observed_revenue_micros']))
        save(out/'probes/shared/AUDIT.json',s.audit.records())
    finally:w.close()
    for name,observed,available,cutoff in [('future_observed',BASE+1,BASE+1,BASE),('late_available',BASE-1,BASE+1,BASE)]:
        check(name,'FUTURE_INFORMATION_BLOCKED',guard_feature(observed,available,cutoff),dict(observed_at=observed,available_at=available,prediction_at=cutoff))
    save(out/'ENGINE_PROBES.json',probes);return probes
