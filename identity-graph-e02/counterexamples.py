"""Intentionally unsafe implementations. Never called by HandoffMachine.

The detector consults original policy/graph independently of the implementation's
reported permission result. A mutant test PASS means its bad send was detected.
"""
from e02_common import PURPOSE

class EnqueueOnly:
    def __init__(self,machine,job):
        self.m=machine;self.job=job
        check=machine._inspect(job,job.purpose)
        if not check['ok']:raise AssertionError(check)
        self.frame=check['frame'];self.cached_epoch=machine.s.store.epoch
    def attempt(self):
        # WRONG: no current policy, dependencies or deletion recheck.
        frame=dict(self.frame,accepted_at=self.m.s.clock.now)
        result=self.m.sink.accept(frame)
        self.m.audit.emit('INTENTIONALLY_UNSAFE_ACCEPT',self.job,mutation='enqueue_only',
            cached_epoch=self.cached_epoch,acknowledgement=result)
        return result

class StaleRetryEpoch(EnqueueOnly):
    def first_failure(self):
        self.m.audit.emit('INTENTIONALLY_UNSAFE_RETRY',self.job,mutation='stale_retry_epoch',cached_epoch=self.cached_epoch,
            injected_failure='BEFORE_SINK_ACCEPT',cached_permission=True)
    def attempt(self):
        result=self.m.sink.accept(dict(self.frame,accepted_at=self.m.s.clock.now))
        self.m.audit.emit('INTENTIONALLY_UNSAFE_ACCEPT',self.job,mutation='stale_retry_epoch',
            cached_epoch=self.cached_epoch,actual_epoch=self.m.s.store.epoch,acknowledgement=result)
        return result

class CheckThenRevoke(EnqueueOnly):
    def attempt(self,intervention):
        check=self.m._inspect(self.job,self.job.purpose)
        if not check['ok']:raise AssertionError(check)
        intervention()
        # WRONG: valid precheck is not atomic with this later accept.
        result=self.m.sink.accept(dict(check['frame'],accepted_at=self.m.s.clock.now))
        self.m.audit.emit('INTENTIONALLY_UNSAFE_ACCEPT',self.job,mutation='check_then_revoke_commit',
            actual_epoch=self.m.s.store.epoch,acknowledgement=result)
        return result

def observe_acceptance(fixture,receipt,*,requested_purpose=PURPOSE):
    """Run immediately after accept, BEFORE any later intervention.

    The fixture has an independently specified device/app/account and login
    relation; do not trust the worker's asserted policy or dependency list.
    """
    s=fixture.s;t=s.clock.now;failures=[]
    refs=[fixture.device,fixture.app,fixture.account]
    allowed={e:s.policy.allowed(e,requested_purpose,as_of=t) for e in refs}
    deleted={e:s.policy.deleted(e) for e in refs}
    active=s.graph.active(t,requested_purpose)
    if not all(allowed.values()):failures.append('UNAUTHORIZED_AT_ACTUAL_HANDOFF')
    if any(deleted.values()):failures.append('DELETED_AT_ACTUAL_HANDOFF')
    if not any(e['id']==fixture.login_edge for e in active):failures.append('AUTH_RELATION_NOT_ACTIVE_AT_HANDOFF')
    if receipt['purpose']!=requested_purpose:failures.append('PURPOSE_MISMATCH')
    if receipt['accepted_epoch']!=s.store.epoch:failures.append('STALE_ACCEPTANCE_EPOCH')
    return dict(observed_at=t,actual_epoch=s.store.epoch,receipt_epoch=receipt['accepted_epoch'],
        original_policy_results=allowed,original_deleted_results=deleted,violations=failures,
        note='Local fixture oracle; not an independent external attestation')
