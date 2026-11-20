"""E02 local reference scheduler. No network or original outbox modifications.

Only the exact MemorySink and a trusted single-thread harness are supported.
The linearization point is in-memory receipt insertion, NOT a database commit,
external ACK, durable delivery, or a transaction spanning the two MVP files.
"""
from dataclasses import dataclass,field
import copy,sqlite3,threading
from e02_common import TaskAwareAdapter,PURPOSE,Rejected,ManualClock,canonical,digest

class Audit:
    def __init__(self,system):self.s=system;self.records=[]
    def emit(self,kind,job=None,**details):
        row=dict(seq=len(self.records)+1,kind=kind,at=self.s.clock.now,epoch=self.s.store.epoch,
            graph_version=self.s.store.graph_version,job_ref=job.ref if job else None,
            state=job.state if job else None,event_ref=job.event_ref if job else None,
            outbox_ref=job.outbox_ref if job else None,details=details,
            previous_hash=self.records[-1]['hash'] if self.records else '0'*64)
        row['hash']=digest(row);self.records.append(row)
    def verify(self):
        previous='0'*64
        for row in self.records:
            body={k:v for k,v in row.items() if k!='hash'}
            if body['previous_hash']!=previous or digest(body)!=row['hash']:return False
            previous=row['hash']
        return True

@dataclass
class Job:
    ref:str
    outbox_ref:str
    event_ref:str
    ledger_ref:str
    purpose:str
    request:dict
    prior:dict
    source_hash:str
    enqueued_at:int
    state:str='QUEUED'
    reason:str='ENQUEUED_LOCALLY'
    claims:int=0
    sends:int=0
    checked_epoch:int|None=None
    checked_graph:int|None=None
    last_ack:dict|None=None
    transmission_enabled:bool=True
    dependencies:dict=field(default_factory=dict)

class MemorySink:
    """Idempotent acceptance receipts, not an economic accounting engine.

    Retains only local synthetic receipt metadata. The dictionary and receipts
    are process-lifetime objects, not a crash-safe ledger. ACK loss is simulated
    AFTER this insertion and cannot turn the receipt into an external ACK.
    """
    def __init__(self):self.receipts={};self.calls=0
    def accept(self,frame):
        self.calls+=1
        key=frame['economic_identity']
        if key in self.receipts:
            old=self.receipts[key]
            if old['source_hash']!=frame['source_hash']:raise Rejected('SINK_IDEMPOTENCY_CONFLICT')
            return dict(receipt=copy.deepcopy(old),duplicate=True)
        receipt=dict(frame,receipt_ref=f'synth:local-ack:{len(self.receipts)+1}',
            receiver='E02_PROCESS_MEMORY_ONLY',third_party_received=False)
        self.receipts[key]=receipt  # The ONLY successful handoff linearization point.
        return dict(receipt=copy.deepcopy(receipt),duplicate=False)

class HandoffMachine:
    TRANSITIONS={
        'QUEUED':{'CLAIMED','CANCELLED'},
        'CLAIMED':{'REVALIDATING','CANCELLED'},
        'REVALIDATING':{'CANCELLED','RETRY_PENDING','LOCAL_ACK'},
        'RETRY_PENDING':{'CLAIMED','CANCELLED'},
        'CANCELLED':set(),'LOCAL_ACK':set(),
    }
    def __init__(self,system,*,boundary='single_thread_memory'):
        self.s=system;self.adapter=TaskAwareAdapter(system);self.sink=MemorySink()
        self.audit=Audit(system);self.jobs={};self.owner=threading.get_ident();self.boundary=boundary
        self.busy=False
        # Only runtime-owned fixture connections; do not change original source.
        system.store.db.execute('PRAGMA busy_timeout=0')
        system.store.control.execute('PRAGMA busy_timeout=0')

    def _transition(self,job,state,reason,**details):
        old=job.state
        if state not in self.TRANSITIONS[old]:raise Rejected('INVALID_STATE_TRANSITION:'+old+'->'+state)
        job.state=state;job.reason=reason
        self.audit.emit('transition',job,from_state=old,to_state=state,reason=reason,**details)

    def _cancel(self,job,reason,**details):
        self._transition(job,'CANCELLED',reason,**details)
        return False

    def _current_request(self,job,purpose=None):
        r=copy.deepcopy(job.request);r['prediction_at']=self.s.clock.now
        if purpose is not None:r['purpose']=purpose
        return r

    def enqueue(self,outbox_ref,request,*,transmission_enabled=True):
        if self.busy:raise Rejected('REENTRANT_SCHEDULER_FORBIDDEN')
        prior=self.adapter.extract(copy.deepcopy(request))
        if prior['status']!='OK':
            self.audit.emit('enqueue_denied',reason=prior['reason'],outbox_ref=outbox_ref)
            raise Rejected(prior['reason'])
        row=self.s.store.db.execute('SELECT * FROM outbox WHERE id=?',(outbox_ref,)).fetchone()
        if not row:raise Rejected('OUTBOX_NOT_FOUND')
        event_ref=row['event_ref']
        if event_ref not in prior['original_lineage']['event_refs']:raise Rejected('OUTBOX_NOT_ACCOUNT_APPROVED')
        ledger=self.s.store.db.execute('SELECT * FROM ledger WHERE event_ref=?',(event_ref,)).fetchone()
        if not ledger or ledger['id'] not in prior['ledger_refs']:raise Rejected('ECONOMIC_LINEAGE_NOT_APPROVED')
        if row['status']!='LOCAL_ONLY_PENDING' or row['payload_json'] is None:raise Rejected('OUTBOX_NOT_LOCALLY_PENDING')
        job=Job(ref=f'synth:e02:job:{len(self.jobs)+1}',outbox_ref=outbox_ref,event_ref=event_ref,
            ledger_ref=ledger['id'],purpose=request['purpose'],request=copy.deepcopy(request),prior=prior,
            source_hash=digest(dict(payload=json_payload(row['payload_json']),semantic_hash=ledger['semantic_hash'])),
            enqueued_at=self.s.clock.now,transmission_enabled=transmission_enabled,
            dependencies=copy.deepcopy(prior['original_lineage']))
        self.jobs[job.ref]=job
        self.audit.emit('transition',job,from_state=None,to_state='QUEUED',reason='ORIGINAL_OUTBOX_COLLECTION_APPROVED',
            gates=dict(collection='APPROVED_AT_ENQUEUE_BY_ORIGINAL_API',transmission=transmission_enabled,
                purpose=job.purpose,delete='CHECKED_BY_ORIGINAL_API'),
            policy_epoch=prior['policy_epoch'],graph_version=prior['graph_version'],dependencies=job.dependencies,
            bundle_ref=prior['bundle_ref'],payload_persisted_in_shadow_queue=False)
        return job

    def _inspect(self,job,purpose,*,final=False):
        """Pure reads and ORIGINAL policy/graph checks, including current time.

        Does not mint permissions, authenticate assertions, select alternative
        relations, rebuild a ledger, or refresh an invalid old feature bundle.
        """
        now=self.s.clock.now
        gates=dict(collection='APPROVED_AT_ENQUEUE',transmission='ALLOW' if job.transmission_enabled else 'DISABLED',
            purpose='CHECKING',delete='CHECKING',policy='CHECKING',relationships='CHECKING',sources='CHECKING')
        details=dict(gates=gates,policy_observation_at=now,dependencies=job.dependencies)
        try:
            if not job.transmission_enabled:raise Rejected('LOCAL_TRANSMISSION_DISABLED')
            if purpose!=job.purpose:raise Rejected('TASK_PURPOSE_NOT_REUSABLE')
            gates['purpose']='BOUND_TO_ORIGINAL_TASK'
            deleted=[e for e in job.dependencies['entity_refs'] if self.s.policy.deleted(e)]
            if deleted:
                gates['delete']='DELETED';details['deleted_refs']=deleted
                raise Rejected('DEPENDENCY_DELETED')
            gates['delete']='NOT_DELETED_AT_READ'
            allowed={e:self.s.policy.allowed(e,purpose,as_of=job.enqueued_at) for e in job.dependencies['entity_refs']}
            details['policy_results']=allowed
            self.s.policy.require(job.dependencies['entity_refs'],purpose,as_of=job.enqueued_at)
            gates['policy']='ORIGINAL_POLICY_ALLOWED_NOW_AND_COLLECTION_TIME'
            # Reuse E01's task binding (original receipt, target, namespace and
            # policy/graph). It is read-only and does not commit either DB.
            self.adapter._binding(self._current_request(job,purpose))
            active=self.s.graph.active(now,purpose)
            byref={(e['id'],e['revision']):e for e in active}
            missing=[r for r in job.dependencies['edge_revisions'] if tuple(r) not in byref]
            details['missing_relation_revisions']=missing
            if missing:raise Rejected('DEPENDENCY_RELATION_REVOKED_OR_EXPIRED')
            gates['relationships']='ORIGINAL_GRAPH_ACTIVE'
            details['relation_windows']=[{k:byref[tuple(r)][k] for k in ['id','revision','valid_from','valid_to','observed_at','available_at','revoked_at']} for r in job.dependencies['edge_revisions']]
            # Proof continuity: original reread occurred outside locks; now check
            # the same bundle remains unchanged while both writers are excluded.
            bundle=self.s.store.db.execute('SELECT * FROM feature_bundles WHERE id=?',(job.prior['bundle_ref'],)).fetchone()
            if not bundle or bundle['status']!='ACTIVE' or bundle['values_json'] is None:raise Rejected('ORIGINAL_BUNDLE_INVALIDATED')
            if bundle['policy_epoch']!=self.s.store.epoch or bundle['graph_version']!=self.s.store.graph_version:
                raise Rejected('ORIGINAL_BUNDLE_VERSION_STALE')
            if final and (job.checked_epoch!=self.s.store.epoch or job.checked_graph!=self.s.store.graph_version):
                raise Rejected('PREPARED_VERSION_CHANGED')
            out=self.s.store.db.execute('SELECT * FROM outbox WHERE id=?',(job.outbox_ref,)).fetchone()
            event=self.s.store.db.execute('SELECT * FROM events WHERE id=?',(job.event_ref,)).fetchone()
            ledger=self.s.store.db.execute('SELECT * FROM ledger WHERE id=?',(job.ledger_ref,)).fetchone()
            if not out or out['status']!='LOCAL_ONLY_PENDING' or out['event_ref']!=job.event_ref or out['payload_json'] is None:
                raise Rejected('ORIGINAL_OUTBOX_NOT_USABLE')
            if not event or not ledger or event['deleted'] or ledger['deleted'] or event['payload_json'] is None:
                raise Rejected('ORIGINAL_EVENT_DELETED_OR_MISSING')
            if event['purpose']!=purpose:raise Rejected('EVENT_PURPOSE_MISMATCH')
            if event['account_ref']!=job.prior['account_ref'] or ledger['account_ref']!=job.prior['account_ref']:
                raise Rejected('EVENT_ACCOUNT_MISMATCH')
            if event['app_ref']!=ledger['app_ref'] or ledger['event_ref']!=event['id']:raise Rejected('EVENT_LEDGER_REFERENCE_MISMATCH')
            if any(row[k]>now for row in [event,ledger] for k in ['occurred_at','observed_at','available_at']):
                raise Rejected('SOURCE_NOT_YET_AVAILABLE')
            # Original economic revision visibility / de-duplication oracle.
            if job.ledger_ref not in {r['id'] for r in self.s.events.visible_ledger(now)}:
                raise Rejected('ECONOMIC_REVISION_NO_LONGER_CURRENT')
            payload=json_payload(out['payload_json'])
            if digest(payload)!=event['payload_hash'] or canonical(payload)!=canonical(json_payload(event['payload_json'])):
                raise Rejected('OUTBOX_EVENT_PAYLOAD_MISMATCH')
            if (ledger['amount_micros']!=payload['amount_micros'] or ledger['currency']!=payload['currency'] or
                ledger['economic_key']!=payload['economic_key'] or ledger['revision']!=payload['revision']):
                raise Rejected('EVENT_LEDGER_VALUE_MISMATCH')
            if digest(dict(payload=payload,semantic_hash=ledger['semantic_hash']))!=job.source_hash:
                raise Rejected('QUEUED_SOURCE_CHANGED')
            gates['sources']='ORIGINAL_APPROVED_REFS_AND_CURRENT_PAYLOAD'
            frame=dict(economic_identity=canonical([ledger['app_ref'],ledger['source'],ledger['economic_key'],ledger['revision']]),
                event_ref=job.event_ref,outbox_ref=job.outbox_ref,ledger_ref=job.ledger_ref,job_ref=job.ref,
                source_hash=job.source_hash,amount_micros=ledger['amount_micros'],currency=ledger['currency'],
                purpose=purpose,accepted_at=now,accepted_epoch=self.s.store.epoch,accepted_graph=self.s.store.graph_version)
            return dict(ok=True,reason='ORIGINAL_GATES_ALLOW',details=details,frame=frame)
        except Rejected as exc:
            return dict(ok=False,reason=str(exc),details=details)

    def _revalidate(self,job,phase,purpose):
        check=self._inspect(job,purpose)
        if check['ok']:
            reread=self.adapter.reread(self._current_request(job,purpose),job.prior)
            check['details']['e01_reread']=reread
            if reread['status']!='READABLE':check.update(ok=False,reason=reread['reason'])
        self.audit.emit('permission_check',job,phase=phase,**check)
        if not check['ok']:return self._cancel(job,check['reason'],phase=phase)
        job.checked_epoch=self.s.store.epoch;job.checked_graph=self.s.store.graph_version
        return True

    def claim(self,job,*,purpose=None):
        if self.busy:raise Rejected('REENTRANT_SCHEDULER_FORBIDDEN')
        if job.state not in ['QUEUED','RETRY_PENDING']:raise Rejected('JOB_NOT_CLAIMABLE')
        retry=job.state=='RETRY_PENDING';job.claims+=1
        if not self._revalidate(job,'retry' if retry else 'claim',job.purpose if purpose is None else purpose):return False
        self._transition(job,'CLAIMED','CURRENT_ORIGINAL_POLICY_AND_DEPENDENCIES_ALLOW',retry=retry)
        return True

    def _atomic_accept(self,job,*,fail_before=False):
        # No user-provided callbacks, no yields, no clock advancement, no
        # original write APIs inside this section. BEGIN IMMEDIATE is used as
        # writer exclusion, NOT as a transaction coordinating sink + two DBs.
        if (self.boundary!='single_thread_memory' or type(self.sink) is not MemorySink or
            threading.get_ident()!=self.owner or threading.active_count()!=1 or
            type(self.s.clock) is not ManualClock or self.busy):
            return dict(ok=False,reason='ATOMIC_HANDOFF_UNPROVEN',boundary_detail='unsupported execution or sink scope')
        db=self.s.store.db;control=self.s.store.control
        if db.in_transaction or control.in_transaction:
            return dict(ok=False,reason='ATOMIC_HANDOFF_UNPROVEN',boundary_detail='pre-existing transaction')
        locked=[];self.busy=True;result=None
        try:
            for connection in [control,db]:
                connection.execute('BEGIN IMMEDIATE');locked.append(connection)
            at=self.s.clock.now
            check=self._inspect(job,job.purpose,final=True)
            check['details']['boundary_observation']=dict(state_write_lock=db.in_transaction,
                control_write_lock=control.in_transaction,owner_thread=threading.get_ident()==self.owner,
                active_threads=threading.active_count(),at=at,clock_unchanged=self.s.clock.now==at,
                allowed_callbacks_between_check_and_accept=False)
            if not check['ok']:return dict(ok=False,reason=check['reason'],check=check)
            if self.s.clock.now!=at:
                return dict(ok=False,reason='ATOMIC_HANDOFF_UNPROVEN',boundary_detail='clock changed inside boundary')
            if fail_before:return dict(ok=True,failed_before_accept=True,check=check)
            result=self.sink.accept(check['frame'])
            return dict(ok=True,acceptance=result,check=check,boundary='DUAL_WRITER_EXCLUSION_SINGLE_THREAD_MEMORY')
        except sqlite3.Error as exc:
            return dict(ok=False,reason='ATOMIC_HANDOFF_UNPROVEN',boundary_detail=type(exc).__name__+': '+str(exc))
        except Rejected as exc:return dict(ok=False,reason=str(exc))
        finally:
            # Read-only critical section. There is no two-database commit here.
            for connection in reversed(locked):connection.rollback()
            self.busy=False

    def deliver(self,job,*,before_commit=None,fail_before=False,lose_ack=False):
        if self.busy:raise Rejected('REENTRANT_SCHEDULER_FORBIDDEN')
        if job.state!='CLAIMED':raise Rejected('CLAIM_REQUIRED')
        self._transition(job,'REVALIDATING','PREPARE_HANDOFF')
        if not self._revalidate(job,'pre_handoff',job.purpose):return False
        prepared=dict(at=self.s.clock.now,epoch=job.checked_epoch,graph_version=job.checked_graph)
        self.audit.emit('handoff_prepared',job,prepared=prepared)
        # Deliberate interleaving occurs OUTSIDE the atomic section, and must
        # subsequently be detected by the under-lock original checks.
        if before_commit is not None:
            self.audit.emit('scheduled_intervention',job,stage='AFTER_PREPARE_BEFORE_ATOMIC_SECTION')
            before_commit()
        outcome=self._atomic_accept(job,fail_before=fail_before)
        self.audit.emit('final_handoff_check',job,prepared=prepared,outcome=outcome)
        if not outcome['ok']:return self._cancel(job,outcome['reason'],outcome=outcome)
        job.sends+=1
        if outcome.get('failed_before_accept'):
            self._transition(job,'RETRY_PENDING','INJECTED_LOCAL_FAILURE_BEFORE_ACCEPT');return False
        acknowledgement=outcome['acceptance']
        self.audit.emit('local_sink_acceptance',job,acknowledgement=acknowledgement,
            linearization='MEMORY_RECEIPT_INSERTION_OR_EXISTING_RECEIPT_LOOKUP',external_delivery=False)
        if lose_ack:
            self._transition(job,'RETRY_PENDING','INJECTED_LOCAL_ACK_LOSS_AFTER_ACCEPT');return False
        job.last_ack=acknowledgement
        self._transition(job,'LOCAL_ACK','LOCAL_MEMORY_ACK_ONLY',acknowledgement=acknowledgement)
        return True

    def run(self,job,**kw):
        if self.claim(job):return self.deliver(job,**kw)
        return False

    def export(self):
        from dataclasses import asdict
        return dict(jobs=[asdict(j) for j in self.jobs.values()],sink=dict(calls=self.sink.calls,
            receipts=list(self.sink.receipts.values()),scope='PROCESS_MEMORY_ONLY_NOT_EXTERNAL_OR_DURABLE'),
            audit=self.audit.records,audit_chain_valid=self.audit.verify())

def json_payload(text):
    import json
    return json.loads(text)
