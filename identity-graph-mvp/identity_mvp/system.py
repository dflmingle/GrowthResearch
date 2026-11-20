"""Seven local components. Standard library only; deliberately no network clients.

This is a synthetic-only engineering reference, not a real-person matching service.
Times are explicit integer UTC epoch seconds. Monetary values are integer micros.
"""
from pathlib import Path
import hashlib,hmac,json,math,sqlite3

PURPOSE='synthetic-value-research'
ENV='LOCAL_SYNTHETIC_ONLY'
KINDS={'person','account','device','app_instance','household'}
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False)
def digest(x):return hashlib.sha256(canonical(x).encode()).hexdigest()
def timestamp(x):
    if type(x) is not int or x<0:raise Rejected('INVALID_UTC_SECOND')
    return x
def source(x):
    if not isinstance(x,str) or not x.startswith('synth:'):raise Rejected('SYNTHETIC_SOURCE_REQUIRED')
    return x
class Rejected(ValueError):pass
class ManualClock:
    def __init__(self,now=1767225600):self.now=timestamp(now)
    def advance(self,seconds=1):
        if type(seconds) is not int or seconds<0:raise Rejected('CLOCK_REWIND')
        self.now+=seconds;return self.now

class Store:
    def __init__(self,directory,clock):
        self.directory=Path(directory);self.directory.mkdir(parents=True,exist_ok=True)
        self.clock=clock
        self.db=self.connect(self.directory/'state.sqlite')
        self.control=self.connect(self.directory/'privacy.sqlite')
        self.db.executescript(Path(__file__).with_name('schema.sql').read_text())
        self.control.executescript(Path(__file__).with_name('control_schema.sql').read_text())
        with self.db:
            for k,v in [('environment',ENV),('counter','0'),('graph_version','0')]:self.db.execute('INSERT OR IGNORE INTO meta VALUES(?,?)',(k,v))
        with self.control:self.control.execute("INSERT OR IGNORE INTO control_meta VALUES('epoch','0')")
        if self.db.execute("SELECT value FROM meta WHERE key='environment'").fetchone()[0]!=ENV:raise Rejected('ENVIRONMENT_MISMATCH')
    @staticmethod
    def connect(path):
        c=sqlite3.connect(str(path));c.row_factory=sqlite3.Row;c.execute('PRAGMA foreign_keys=ON');c.execute('PRAGMA synchronous=FULL');return c
    def id(self,prefix):
        # The counter is outside restorable state snapshots, like deletion authority.
        # Failed data transactions may leave gaps, but restore cannot reuse entity IDs.
        with self.control:
            self.control.execute("INSERT OR IGNORE INTO control_meta VALUES('id_counter','0')")
            n=int(self.control.execute("SELECT value FROM control_meta WHERE key='id_counter'").fetchone()[0])+1
            self.control.execute("UPDATE control_meta SET value=? WHERE key='id_counter'",(str(n),))
        return f'{prefix}_{n:06d}'
    @property
    def graph_version(self):return int(self.db.execute("SELECT value FROM meta WHERE key='graph_version'").fetchone()[0])
    @property
    def epoch(self):return int(self.control.execute("SELECT value FROM control_meta WHERE key='epoch'").fetchone()[0])
    def bump_graph(self):
        self.db.execute("UPDATE meta SET value=? WHERE key='graph_version'",(str(self.graph_version+1),))
        self.db.execute("UPDATE feature_bundles SET status='INVALIDATED',values_json=NULL WHERE status='ACTIVE'")
    def entity(self,eid):
        row=self.db.execute('SELECT * FROM entities WHERE id=?',(eid,)).fetchone()
        if row is None or row['deleted']:raise Rejected('ENTITY_MISSING_OR_DELETED')
        return row
    def close(self):self.db.close();self.control.close()

class ProvenanceAuditLog:
    def __init__(self,s):self.s=s
    def append(self,kind,payload):
        # Callers only provide synthetic references, never credentials or identity tokens.
        previous=self.s.db.execute('SELECT hash FROM audit_log ORDER BY seq DESC LIMIT 1').fetchone()
        prev=previous[0] if previous else '0'*64
        body=dict(at=self.s.clock.now,kind=kind,payload=payload,previous_hash=prev)
        self.s.db.execute('INSERT INTO audit_log(at,kind,payload_json,previous_hash,hash) VALUES(?,?,?,?,?)',
            (body['at'],kind,canonical(payload),prev,digest(body)))
    def verify(self):
        prev='0'*64
        for row in self.s.db.execute('SELECT * FROM audit_log ORDER BY seq'):
            body=dict(at=row['at'],kind=row['kind'],payload=json.loads(row['payload_json']),previous_hash=prev)
            if row['previous_hash']!=prev or row['hash']!=digest(body):return False
            prev=row['hash']
        return True
    def records(self):return [dict(x) for x in self.s.db.execute('SELECT * FROM audit_log ORDER BY seq')]
    @staticmethod
    def assess_chain(evidence):
        try:return ProvenanceAuditLog._assess_chain(evidence)
        except (TypeError,ValueError,KeyError,AttributeError,OverflowError):
            return dict(status='NOT_IDENTIFIABLE',reason='MALFORMED_EVIDENCE',scope=ENV,
                C_graph_Axon='UNKNOWN',C_graph_Vector='UNKNOWN',D='UNKNOWN',production_forensics='STOP')
    @staticmethod
    def _assess_chain(evidence):
        """Independent evidence-shape/consistency checker; never asserts vendor C_graph.

        Local provenance flags are fixture attestations, not real independent review.
        Missing/contradictory fields fail rather than trusting a nonempty result ID.
        """
        def result(status,reason):return dict(status=status,reason=reason,scope=ENV,
             C_graph_Axon='UNKNOWN',C_graph_Vector='UNKNOWN',D='UNKNOWN',production_forensics='STOP')
        if evidence.get('environment')!=ENV:return result('NOT_IDENTIFIABLE','UNSUPPORTED_PRODUCTION_SCOPE')
        prov=evidence.get('provenance',{})
        if not all(prov.get(k) is True for k in ['source_authenticated','independently_reviewed','quotation_permitted','coverage_complete']):
            return result('UNTRUSTED','PROVENANCE_NOT_ESTABLISHED')
        resolution=evidence.get('resolution');receiver=evidence.get('receiver');read=evidence.get('read');decision=evidence.get('decision')
        if not all(isinstance(x,dict) for x in [resolution,receiver,read,decision]):return result('NOT_IDENTIFIABLE','MISSING_CHAIN_STAGE')
        needed=[(resolution,['ref','status','grain','component_version','purpose','available_at']),
          (receiver,['ref','resolution_ref','product','received_at','available_at','purpose']),
          (read,['ref','receiver_ref','bundle_ref','product','model','model_version','feature_group','graph_version','inference_ref','nonempty_refs','read_at','purpose']),
          (decision,['ref','read_ref','inference_ref','model_version','opportunity_ref','decision_at','use','purpose'])]
        if any(any(k not in row or row[k] is None or row[k]=='' for k in keys) for row,keys in needed):return result('NOT_IDENTIFIABLE','MISSING_REQUIRED_FIELD')
        if resolution['status']!='existing_entity_asserted':return result('NOT_IDENTIFIABLE','NON_MATCH_OR_DERIVED_ID')
        if resolution['grain'] not in KINDS:return result('NOT_IDENTIFIABLE','UNKNOWN_ENTITY_GRAIN')
        if receiver['product']!=read['product']:return result('NOT_IDENTIFIABLE','PRODUCT_MISMATCH')
        if receiver['resolution_ref']!=resolution['ref'] or read['receiver_ref']!=receiver['ref'] or decision['read_ref']!=read['ref']:
            return result('NOT_IDENTIFIABLE','CROSS_SYSTEM_REFERENCE_MISMATCH')
        if decision['model_version']!=read['model_version'] or decision['inference_ref']!=read['inference_ref']:
            return result('NOT_IDENTIFIABLE','MODEL_INFERENCE_MISMATCH')
        if len({row['purpose'] for row in [resolution,receiver,read,decision]})!=1:return result('NOT_IDENTIFIABLE','PURPOSE_MISMATCH')
        if not isinstance(read['nonempty_refs'],list) or not read['nonempty_refs'] or read.get('default_fallback',False):
            return result('NOT_IDENTIFIABLE','NO_NONEMPTY_MODEL_INPUT')
        try:
            times=[resolution['available_at'],receiver['received_at'],receiver['available_at'],read['read_at'],decision['decision_at']]
            for t in times:timestamp(t)
            if times!=sorted(times):return result('NOT_IDENTIFIABLE','TEMPORAL_LEAKAGE')
            invalid=evidence.get('invalid_after')
            if invalid is not None and read['read_at']>=timestamp(invalid):return result('NOT_IDENTIFIABLE','REVOKED_OR_EXPIRED')
        except (Rejected,TypeError):return result('NOT_IDENTIFIABLE','INVALID_TIME')
        if evidence.get('policy_valid') is not True:return result('NOT_IDENTIFIABLE','POLICY_NOT_ESTABLISHED')
        if decision['use']!='active':return result('NOT_IDENTIFIABLE','NOT_AN_ACTIVE_DECISION')
        return result('LOCAL_CHAIN_VERIFIED','LOCAL_FIXTURE_CONSISTENCY_ONLY_NOT_VENDOR_OR_PERSON_TRUTH')

class IdentityNamespaceRegistry:
    def __init__(self,s,audit):self.s=s;self.audit=audit
    def register(self,*,tenant,issuer,app,sector,entity_type,scope,version='1',evidence='synth:namespace-contract'):
        if entity_type not in KINDS:raise Rejected('UNKNOWN_ENTITY_TYPE')
        if not issuer.startswith('synthetic:') or not all(isinstance(x,str) and x for x in [tenant,app,sector,scope,version]):raise Rejected('INVALID_SYNTHETIC_NAMESPACE')
        source(evidence)
        fields=(tenant,issuer,app,sector,entity_type,scope,version)
        row=self.s.db.execute('SELECT id FROM namespaces WHERE tenant=? AND issuer=? AND app=? AND sector=? AND entity_type=? AND scope=? AND version=?',fields).fetchone()
        if row:return row[0]
        with self.s.db:
            nid=self.s.id('ns');self.s.db.execute('INSERT INTO namespaces VALUES(?,?,?,?,?,?,?,?,?)',(nid,*fields,evidence))
            self.audit.append('namespace_registered',dict(namespace_ref=nid,entity_type=entity_type))
        return nid
    def create(self,namespace_ref,token):
        if not isinstance(token,str) or not token.startswith('syn:'):raise Rejected('SYNTHETIC_TOKEN_REQUIRED')
        ns=self.s.db.execute('SELECT * FROM namespaces WHERE id=?',(namespace_ref,)).fetchone()
        if ns is None or ns['scope']=='UNKNOWN':raise Rejected('UNKNOWN_SCOPE')
        row=self.s.db.execute('SELECT id,deleted FROM entities WHERE namespace_id=? AND token=?',(namespace_ref,token)).fetchone()
        if row:
            if row['deleted']:raise Rejected('DELETED_KEY')
            return row['id']
        # A deletion tombstone bans all reuse of the previous synthetic key digest.
        ban=digest(dict(namespace=namespace_ref,token=token))
        if self.s.control.execute("SELECT 1 FROM control_meta WHERE key=?",('deleted_key:'+ban,)).fetchone():raise Rejected('DELETED_KEY_REPLAY')
        with self.s.db:
            eid=self.s.id('entity');self.s.db.execute('INSERT INTO entities VALUES(?,?,?,?,?,0)',(eid,namespace_ref,token,ns['entity_type'],self.s.clock.now))
            self.audit.append('entity_created',dict(entity_ref=eid,namespace_ref=namespace_ref,grain=ns['entity_type']))
        return eid
    def compare(self,a,b):
        aa=self.s.entity(a);bb=self.s.entity(b)
        if aa['namespace_id']!=bb['namespace_id']:return 'DIFFERENT_NAMESPACE'
        return 'SCOPED_VALUES_EQUAL' if aa['token']==bb['token'] else 'DIFFERENT_SCOPED_VALUE'
    def authorize_mapping(self,a,b,*,purpose=PURPOSE,evidence):
        source(evidence)
        for n in [a,b]:
            row=self.s.db.execute('SELECT * FROM namespaces WHERE id=?',(n,)).fetchone()
            if row is None or row['entity_type']!='account':raise Rejected('ACCOUNT_NAMESPACES_REQUIRED')
        with self.s.db:
            self.s.db.execute('INSERT OR REPLACE INTO namespace_mappings VALUES(?,?,?,?,?)',(*sorted([a,b]),purpose,evidence,self.s.clock.now))
            self.audit.append('namespace_mapping_authorized',dict(namespace_refs=sorted([a,b]),purpose=purpose))
    def mapping_allowed(self,a,b,purpose=PURPOSE):
        return a==b or bool(self.s.db.execute('SELECT 1 FROM namespace_mappings WHERE a=? AND b=? AND purpose=?',(*sorted([a,b]),purpose)).fetchone())

class ConsentAndDeletionManager:
    LOCAL_SINKS=('identity','graph','events','outbox','features','coverage')
    def __init__(self,s,audit):self.s=s;self.audit=audit
    def _next_epoch(self):
        n=self.s.epoch+1;self.s.control.execute("UPDATE control_meta SET value=? WHERE key='epoch'",(str(n),));return n
    def set(self,entity,purpose,allowed,*,effective_at=None,source_ref='synth:consent'):
        self.s.entity(entity);source(source_ref);effective=self.s.clock.now if effective_at is None else timestamp(effective_at)
        if effective<self.s.clock.now:raise Rejected('RETROACTIVE_POLICY_CHANGE')
        with self.s.control:
            epoch=self._next_epoch();self.s.control.execute('INSERT INTO policies VALUES(?,?,?,?,?,?,?)',
                (epoch,entity,purpose,'GRANTED' if allowed else 'REVOKED',effective,self.s.clock.now,source_ref))
        with self.s.db:
            self.s.db.execute("UPDATE feature_bundles SET status='INVALIDATED',values_json=NULL WHERE status='ACTIVE'")
            self.audit.append('policy_changed',dict(entity_ref=entity,purpose=purpose,epoch=epoch,state='GRANTED' if allowed else 'REVOKED',effective_at=effective))
        return epoch
    def deleted(self,entity):return bool(self.s.control.execute('SELECT 1 FROM deletions WHERE entity_ref=?',(entity,)).fetchone() or
        self.s.control.execute('SELECT 1 FROM erased_entities WHERE entity_ref=?',(entity,)).fetchone())
    def allowed(self,entity,purpose,*,as_of=None,read_at=None):
        now=self.s.clock.now if read_at is None else timestamp(read_at)
        if now>self.s.clock.now or self.deleted(entity):return False
        try:self.s.entity(entity)
        except Rejected:return False
        def state(t):
            row=self.s.control.execute('SELECT state FROM policies WHERE entity_ref=? AND purpose=? AND effective_at<=? AND observed_at<=? ORDER BY epoch DESC LIMIT 1',(entity,purpose,t,t)).fetchone()
            return row is not None and row[0]=='GRANTED'
        return state(now) and (as_of is None or (timestamp(as_of)<=now and state(as_of)))
    def require(self,entities,purpose,as_of=None):
        if not all(self.allowed(e,purpose,as_of=as_of) for e in set(entities)):raise Rejected('CONSENT_DENIED_OR_UNKNOWN')
    def delete(self,entity,*,extra_sinks=(),source_ref='synth:delete'):
        e=self.s.entity(entity);source(source_ref)
        if any(not isinstance(s,str) or not s.startswith('synthetic:') for s in extra_sinks):raise Rejected('LOCAL_SINKS_ONLY')
        # Durable authority is committed first: a crash before purge must fail closed.
        with self.s.control:
            epoch=self._next_epoch();case=f'delete_{epoch:06d}'
            self.s.control.execute('INSERT INTO deletions VALUES(?,?,?,?,?,?,?,?)',(case,entity,self.s.clock.now,self.s.clock.now,epoch,source_ref,'NO_MODEL_TRAINED','READS_BLOCKED'))
            self.s.control.execute('INSERT OR REPLACE INTO control_meta VALUES(?,?)',('deleted_key:'+digest(dict(namespace=e['namespace_id'],token=e['token'])),case))
            for sink in self.LOCAL_SINKS+tuple(extra_sinks):self.s.control.execute('INSERT INTO deletion_sinks VALUES(?,?,?,NULL,NULL)',(case,sink,'PENDING'))
        self.reconcile();return self.case(case)
    def reconcile(self):
        for deletion in self.s.control.execute('SELECT * FROM deletions').fetchall():
            entity=deletion['entity_ref'];case=deletion['id']
            targets={entity}|{x[0] for x in self.s.control.execute('SELECT entity_ref FROM erased_entities WHERE case_ref=?',(case,))}
            erow=self.s.db.execute('SELECT entity_type FROM entities WHERE id=?',(entity,)).fetchone()
            if erow and erow[0]=='device':
                # An app installation is device-scoped, not an account/person alias.
                # Include all its known past installation references, never traverse
                # account edges into another device belonging to a shared account.
                targets|={x[0] for x in self.s.db.execute("SELECT DISTINCT src FROM edge_revisions WHERE kind='installed_on' AND dst=?",(entity,))}
            with self.s.control:
                for target in targets:
                    self.s.control.execute('INSERT OR IGNORE INTO erased_entities VALUES(?,?,?)',(target,case,deletion['effective_at']))
                    key=self.s.db.execute('SELECT namespace_id,token FROM entities WHERE id=?',(target,)).fetchone()
                    if key and key['token'] is not None:self.s.control.execute('INSERT OR REPLACE INTO control_meta VALUES(?,?)',
                        ('deleted_key:'+digest(dict(namespace=key['namespace_id'],token=key['token'])),case))
            with self.s.db:
                for target in targets:
                    self.s.db.execute('UPDATE entities SET token=NULL,deleted=1 WHERE id=?',(target,))
                    self.s.db.execute("UPDATE edge_revisions SET status='DELETED',revoked_at=? WHERE src=? OR dst=?",(deletion['effective_at'],target,target))
                    ids=[x[0] for x in self.s.db.execute('SELECT id FROM events WHERE app_ref=? OR account_ref=?',(target,target))]
                    for eid in ids:
                        self.s.db.execute('UPDATE events SET payload_json=NULL,deleted=1 WHERE id=?',(eid,))
                        self.s.db.execute('UPDATE ledger SET amount_micros=NULL,deleted=1 WHERE event_ref=?',(eid,))
                        self.s.db.execute("UPDATE outbox SET payload_json=NULL,status='DELETED' WHERE event_ref=?",(eid,))
                    self.s.db.execute('DELETE FROM coverage WHERE app_ref=?',(target,))
                self.s.db.execute("UPDATE feature_bundles SET values_json=NULL,status='DELETED'")
                self.s.bump_graph()
                trained=deletion['training_disposition']=='MODEL_ERASURE_UNKNOWN'
                for t in self.s.db.execute('SELECT * FROM training_snapshots').fetchall():
                    if targets.intersection(json.loads(t['entity_refs_json'])):
                        self.s.db.execute("UPDATE training_snapshots SET status='BLOCKED_DELETED_SOURCE' WHERE id=?",(t['id'],));trained|=bool(t['trained_model'])
                self.audit.append('deletion_reconciled',dict(case_ref=case,entity_ref=entity,impacted_entity_refs=sorted(targets),
                    scope='DECLARED_ENTITY_AND_ITS_DEVICE_APP_INSTANCES;NOT_OTHER_ACCOUNTS_OR_DEVICES',model_erasure='UNKNOWN' if trained else 'NO_MODEL_TRAINED'))
            with self.s.control:
                self.s.control.execute('UPDATE deletions SET training_disposition=? WHERE id=?',('MODEL_ERASURE_UNKNOWN' if trained else 'NO_MODEL_TRAINED',case))
                for sink in self.LOCAL_SINKS:self.s.control.execute("UPDATE deletion_sinks SET status='ACK',acknowledged_at=?,source_ref='synth:local-purge' WHERE case_ref=? AND sink=?",(self.s.clock.now,case,sink))
            self._refresh_case(case)
    def _refresh_case(self,case):
        row=self.s.control.execute('SELECT * FROM deletions WHERE id=?',(case,)).fetchone()
        pending=self.s.control.execute("SELECT 1 FROM deletion_sinks WHERE case_ref=? AND status!='ACK'",(case,)).fetchone()
        state='ACK_PENDING' if pending else ('EXCEPTION_OR_UNKNOWN' if row['training_disposition']!='NO_MODEL_TRAINED' else 'COMPLETE_FOR_DECLARED_SCOPE')
        with self.s.control:self.s.control.execute('UPDATE deletions SET state=? WHERE id=?',(state,case))
    def acknowledge(self,case,sink,*,source_ref):
        source(source_ref)
        if sink in self.LOCAL_SINKS:raise Rejected('LOCAL_PURGE_ACK_NOT_CALLER_SETTABLE')
        with self.s.control:
            cur=self.s.control.execute("UPDATE deletion_sinks SET status='ACK',acknowledged_at=?,source_ref=? WHERE case_ref=? AND sink=?",(self.s.clock.now,source_ref,case,sink))
            if cur.rowcount!=1:raise Rejected('UNKNOWN_SINK')
        self._refresh_case(case);return self.case(case)
    def case(self,case):
        row=self.s.control.execute('SELECT * FROM deletions WHERE id=?',(case,)).fetchone()
        if row is None:raise Rejected('UNKNOWN_DELETION_CASE')
        out=dict(row);out['sinks']=[dict(x) for x in self.s.control.execute('SELECT * FROM deletion_sinks WHERE case_ref=? ORDER BY sink',(case,))]
        out['pending_sinks']=[x['sink'] for x in out['sinks'] if x['status']!='ACK'];return out

class ConfidenceAwareRelationshipGraph:
    ACTIVE_KINDS={'installed_on','logged_in_as','same_device','cannot_link'}
    def __init__(self,s,policy,audit):self.s=s;self.policy=policy;self.audit=audit
    def active(self,as_of=None,purpose=PURPOSE):
        t=self.s.clock.now if as_of is None else timestamp(as_of)
        if t>self.s.clock.now:raise Rejected('FUTURE_AS_OF')
        rows=self.s.db.execute('''SELECT e.* FROM edge_revisions e WHERE observed_at<=? AND available_at<=?
          AND revision=(SELECT MAX(x.revision) FROM edge_revisions x WHERE x.id=e.id AND x.observed_at<=? AND x.available_at<=?)
          ORDER BY id''',(t,t,t,t)).fetchall()
        return [dict(e) for e in rows if e['status']=='ACTIVE' and e['purpose']==purpose and e['valid_from']<=t and
          (e['valid_to'] is None or t<e['valid_to']) and (e['revoked_at'] is None or t<e['revoked_at']) and
          self.policy.allowed(e['src'],purpose,as_of=t) and self.policy.allowed(e['dst'],purpose,as_of=t)]
    def component(self,start,as_of=None,purpose=PURPOSE):
        self.s.entity(start);edges=[e for e in self.active(as_of,purpose) if e['kind']=='same_device']
        found={start};changed=True
        while changed:
            changed=False
            for e in edges:
                if (e['src'] in found or e['dst'] in found) and not {e['src'],e['dst']}<=found:
                    found|={e['src'],e['dst']};changed=True
        return sorted(found)
    def add(self,src,dst,kind,*,source_ref,valid_from=None,available_at=None,valid_to=None,
            confidence=None,quality_kind='synthetic_attestation',quality_scope='synthetic-ground-truth-only',purpose=PURPOSE,auth_receipt=None):
        source(source_ref);a=self.s.entity(src);b=self.s.entity(dst);self.policy.require([src,dst],purpose)
        if src==dst:raise Rejected('SELF_EDGE_NOT_A_RELATION')
        na=self.s.db.execute('SELECT * FROM namespaces WHERE id=?',(a['namespace_id'],)).fetchone()
        nb=self.s.db.execute('SELECT * FROM namespaces WHERE id=?',(b['namespace_id'],)).fetchone()
        if na['tenant']!=nb['tenant']:raise Rejected('CROSS_TENANT_EDGE_FORBIDDEN')
        if confidence is not None and (type(confidence) not in [float,int] or not math.isfinite(confidence) or not 0<=confidence<=1):raise Rejected('INVALID_CONFIDENCE')
        vf=self.s.clock.now if valid_from is None else timestamp(valid_from)
        avail=self.s.clock.now if available_at is None else timestamp(available_at)
        if avail<self.s.clock.now:raise Rejected('BACKDATED_LOCAL_AVAILABILITY')
        if valid_to is not None and timestamp(valid_to)<=vf:raise Rejected('INVALID_VALIDITY_INTERVAL')
        allowed={'installed_on':('app_instance','device'),'logged_in_as':('app_instance','account'),'same_device':('device','device')}
        if kind in allowed and (a['entity_type'],b['entity_type'])!=allowed[kind]:raise Rejected('RELATION_GRAIN_MISMATCH')
        if kind=='logged_in_as':
            receipt=self.s.control.execute('SELECT * FROM auth_nonces WHERE nonce=?',(auth_receipt,)).fetchone()
            if receipt is None or receipt['app_ref']!=src or receipt['account_ref']!=dst or receipt['purpose']!=purpose:
                raise Rejected('AUTH_RECEIPT_REQUIRED')
        if kind in ['candidate_same_entity','cannot_link']:
            if a['entity_type']!=b['entity_type']:raise Rejected('RELATION_GRAIN_MISMATCH')
        elif kind not in allowed:raise Rejected('UNSUPPORTED_RELATION_TYPE')
        status='CANDIDATE' if kind=='candidate_same_entity' else 'ACTIVE'
        if kind=='candidate_same_entity':quality_kind='uncalibrated_score'
        existing=self.active(purpose=purpose)
        if kind=='same_device':
            members=set(self.component(src,purpose=purpose))|set(self.component(dst,purpose=purpose))
            if any(e['kind']=='cannot_link' and e['src'] in members and e['dst'] in members for e in existing):status='CONFLICT'
        if kind=='installed_on' and any(e['kind']=='installed_on' and e['src']==src and e['dst']!=dst for e in existing):status='CONFLICT'
        grain='account' if kind=='logged_in_as' else a['entity_type']
        with self.s.db:
            self.s.bump_graph();eid=self.s.id('edge')
            self.s.db.execute('INSERT INTO edge_revisions VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
              (eid,1,src,dst,kind,grain,source_ref,f'{a["namespace_id"]}->{b["namespace_id"]}',confidence,quality_kind,quality_scope,
               'independent-local-v1',status,vf,valid_to,self.s.clock.now,avail,None,purpose,self.s.epoch,self.s.graph_version))
            self.audit.append('edge_added',dict(edge_ref=eid,status=status,kind=kind,grain=grain,graph_version=self.s.graph_version))
        if kind=='cannot_link':
            # Late constraints must also break an already materialized bad component.
            members=set(self.component(src,purpose=purpose))
            if dst in members:
                for e in self.active(purpose=purpose):
                    if e['kind']=='same_device' and e['src'] in members and e['dst'] in members:self.revoke(e['id'],reason='synth:late-cannot-link',new_status='CONFLICT')
        return dict(edge_ref=eid,status=status,grain=grain,person_inference=False)
    def revoke(self,edge_ref,*,reason='synth:edge-revocation',new_status='REVOKED'):
        source(reason)
        row=self.s.db.execute('SELECT * FROM edge_revisions WHERE id=? ORDER BY revision DESC LIMIT 1',(edge_ref,)).fetchone()
        if row is None:raise Rejected('UNKNOWN_EDGE')
        if new_status not in ['REVOKED','CONFLICT']:raise Rejected('INVALID_REVOKED_STATUS')
        with self.s.db:
            self.s.bump_graph();x=dict(row);x.update(revision=x['revision']+1,status=new_status,observed_at=self.s.clock.now,
                available_at=self.s.clock.now,revoked_at=self.s.clock.now,source_ref=reason,graph_version=self.s.graph_version)
            self.s.db.execute('INSERT INTO edge_revisions VALUES('+','.join('?' for _ in x)+')',tuple(x.values()))
            self.audit.append('edge_revoked',dict(edge_ref=edge_ref,reason=reason,status=new_status,graph_version=self.s.graph_version))
        return dict(edge_ref=edge_ref,status=new_status)
    def reset_device(self,device,*,reason='synth:identifier-reset'):
        if self.s.entity(device)['entity_type']!='device':raise Rejected('DEVICE_REQUIRED')
        ids=[e['id'] for e in self.active() if device in [e['src'],e['dst']]]
        for eid in ids:self.revoke(eid,reason=reason)
        self.policy.set(device,PURPOSE,False,source_ref=reason)
        return dict(old_device=device,revoked_edges=ids,restored_old_identity=False)

class DeterministicIdentityResolver:
    def __init__(self,s,registry,policy,graph,audit,fixture_key):
        self.s=s;self.registry=registry;self.policy=policy;self.graph=graph;self.audit=audit;self.key=fixture_key
    def login(self,assertion,signature):
        # HMAC authenticates local seeded fixtures, not OIDC or a real person.
        if not isinstance(signature,str) or not hmac.compare_digest(hmac.new(self.key,canonical(assertion).encode(),hashlib.sha256).hexdigest(),signature):raise Rejected('BAD_FIXTURE_SIGNATURE')
        needed={'issuer','audience','account','app_instance','device','nonce','issued_at','expires_at','purpose','source_ref'}
        if set(assertion)!=needed:raise Rejected('AUTH_FIELDS_INVALID')
        source(assertion['source_ref']);now=self.s.clock.now
        if timestamp(assertion['issued_at'])>now or timestamp(assertion['expires_at'])<=now:raise Rejected('AUTH_TIME_INVALID')
        if assertion['expires_at']-assertion['issued_at']>3600:raise Rejected('AUTH_TTL_TOO_LONG')
        account=self.s.entity(assertion['account']);app=self.s.entity(assertion['app_instance']);device=self.s.entity(assertion['device'])
        if (account['entity_type'],app['entity_type'],device['entity_type'])!=('account','app_instance','device'):raise Rejected('AUTH_ENTITY_GRAIN')
        an=self.s.db.execute('SELECT * FROM namespaces WHERE id=?',(account['namespace_id'],)).fetchone()
        pn=self.s.db.execute('SELECT * FROM namespaces WHERE id=?',(app['namespace_id'],)).fetchone()
        if assertion['issuer']!=an['issuer'] or assertion['audience']!=pn['app']:raise Rejected('AUTH_ISSUER_OR_AUDIENCE')
        self.policy.require([account['id'],app['id'],device['id']],assertion['purpose'])
        if not any(e['kind']=='installed_on' and e['src']==app['id'] and e['dst']==device['id'] for e in self.graph.active(purpose=assertion['purpose'])):raise Rejected('INSTALL_DEVICE_RELATION_REQUIRED')
        if self.s.control.execute('SELECT 1 FROM auth_nonces WHERE nonce=?',(assertion['nonce'],)).fetchone():raise Rejected('AUTH_REPLAY')
        # Durable replay denial is committed before the state write. A crash may
        # consume a nonce without creating an edge; caller must mint a new fixture
        # assertion. We do not claim a distributed transaction across both files.
        with self.s.control:self.s.control.execute('INSERT INTO auth_nonces VALUES(?,?,?,?,?,?)',
            (assertion['nonce'],now,app['id'],account['id'],assertion['purpose'],digest(assertion)))
        with self.s.db:
            out=self.graph.add(app['id'],account['id'],'logged_in_as',source_ref=assertion['source_ref'],confidence=1.0,
                quality_kind='authenticated_account_control',quality_scope='local-synthetic-credential-control-only',purpose=assertion['purpose'],auth_receipt=assertion['nonce'])
        return dict(status='ACCOUNT_RELATION_ESTABLISHED',edge_ref=out['edge_ref'],grain='account',person_inference=False)

class TemporalEventLinker:
    def __init__(self,s,policy,graph,audit):self.s=s;self.policy=policy;self.graph=graph;self.audit=audit
    def ingest(self,*,app,source_name,event_id,event_type,occurred_at,source_ref='synth:event',purpose=PURPOSE,
               received_at=None,available_at=None,account=None,revision=1,amount_micros=None,currency='USD',
               economic_key=None,economic_kind=None,correction_of=None,opportunity_ref=None,candidate_ref=None,impression_ref=None):
        a=self.s.entity(app)
        if a['entity_type']!='app_instance':raise Rejected('APP_INSTANCE_REQUIRED')
        for name in [source_name,event_id,source_ref]:source(name)
        now=self.s.clock.now;t=timestamp(occurred_at);received=now if received_at is None else timestamp(received_at);avail=now if available_at is None else timestamp(available_at)
        if not t<=received<=now or avail<now:raise Rejected('EVENT_TIME_INVALID')
        if type(revision) is not int or revision<1:raise Rejected('INVALID_REVISION')
        self.policy.require([app]+([account] if account else []),purpose)
        if account:
            if self.s.entity(account)['entity_type']!='account':raise Rejected('ACCOUNT_REQUIRED')
            if not any(e['kind']=='logged_in_as' and e['src']==app and e['dst']==account and e['valid_from']<=t and (e['valid_to'] is None or t<e['valid_to']) for e in self.graph.active(purpose=purpose)):
                raise Rejected('ACCOUNT_EVENT_LINK_NOT_ESTABLISHED')
        if amount_micros is not None:
            if type(amount_micros) is not int or not economic_key or economic_kind not in ['IAA','IAP']:raise Rejected('INVALID_ECONOMIC_EVENT')
            source(economic_key)
            if event_type!='revenue':raise Rejected('REVENUE_EVENT_TYPE_REQUIRED')
        elif event_type=='revenue':raise Rejected('AMOUNT_REQUIRED')
        if not isinstance(currency,str) or len(currency)!=3 or not currency.isupper():raise Rejected('CURRENCY_REQUIRED')
        ns=self.s.db.execute('SELECT tenant FROM namespaces WHERE id=?',(a['namespace_id'],)).fetchone()
        payload=dict(app=app,source=source_name,event_id=event_id,event_type=event_type,occurred_at=t,account=account,revision=revision,
            amount_micros=amount_micros,currency=currency,economic_key=economic_key,economic_kind=economic_kind,correction_of=correction_of,
            opportunity_ref=opportunity_ref,candidate_ref=candidate_ref,impression_ref=impression_ref,purpose=purpose)
        ph=digest(payload)
        existing=self.s.db.execute('SELECT id,payload_hash,deleted FROM events WHERE tenant=? AND app_ref=? AND source=? AND source_event_id=? AND revision=?',
            (ns[0],app,source_name,event_id,revision)).fetchone()
        if existing:
            if existing['deleted']:raise Rejected('DELETED_EVENT_REPLAY')
            if existing['payload_hash']!=ph:raise Rejected('IDEMPOTENCY_PAYLOAD_CONFLICT')
            with self.s.db:self.audit.append('event_retry_deduplicated',dict(event_ref=existing['id']))
            return dict(status='DUPLICATE_EVENT',event_ref=existing['id'])
        economic_at=t
        semantic=digest(dict(app=app,account=account,amount_micros=amount_micros,currency=currency,economic_kind=economic_kind,correction_of=correction_of))
        prior=None
        if amount_micros is not None:
            old=self.s.db.execute('SELECT * FROM ledger WHERE app_ref=? AND source=? AND economic_key=? AND revision=?',(app,source_name,economic_key,revision)).fetchone()
            if old:
                if old['deleted']:raise Rejected('DELETED_LEDGER_REPLAY')
                if old['semantic_hash']!=semantic:raise Rejected('ECONOMIC_REVISION_CONFLICT')
                with self.s.db:self.audit.append('economic_callback_deduplicated',dict(ledger_ref=old['id']))
                return dict(status='DUPLICATE_LEDGER',ledger_ref=old['id'])
            prior=self.s.db.execute('SELECT * FROM ledger WHERE app_ref=? AND source=? AND economic_key=? ORDER BY revision DESC LIMIT 1',(app,source_name,economic_key)).fetchone()
            if revision>1:
                if not prior or prior['revision']!=revision-1 or correction_of!=prior['id'] or prior['deleted']:raise Rejected('CORRECTION_CHAIN_REQUIRED')
                if prior['currency']!=currency or prior['account_ref']!=account or prior['economic_kind']!=economic_kind:raise Rejected('CORRECTION_SCOPE_MISMATCH')
                economic_at=prior['economic_at']
            elif prior or correction_of:raise Rejected('INVALID_FIRST_REVISION')
        with self.s.db:
            eid=self.s.id('event');self.s.db.execute('INSERT INTO events VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,0)',
                (eid,ns[0],app,source_name,event_id,revision,event_type,account,t,received,now,avail,source_ref,purpose,self.s.epoch,ph,canonical(payload)))
            self.s.db.execute('INSERT INTO outbox VALUES(?,?,?,?)',(self.s.id('outbox'),eid,canonical(payload),'LOCAL_ONLY_PENDING'))
            lid=None
            if amount_micros is not None:
                lid=self.s.id('ledger');self.s.db.execute('INSERT INTO ledger VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,0)',
                    (lid,eid,app,account,source_name,economic_key,revision,amount_micros,currency,economic_kind,economic_at,t,now,avail,correction_of,semantic))
            self.s.bump_graph() # conservative all-bundle invalidation on source changes
            self.audit.append('event_accepted',dict(event_ref=eid,ledger_ref=lid,type=event_type,source_ref=source_ref))
        return dict(status='ACCEPTED',event_ref=eid,ledger_ref=lid)
    def coverage(self,app,*,start_at,end_at,status,available_at=None,source_ref='synth:observation'):
        self.s.entity(app);self.policy.require([app],PURPOSE);source(source_ref)
        start=timestamp(start_at);end=timestamp(end_at)
        if start>end or end>self.s.clock.now or status not in ['COMPLETE','MISSING','EXITED']:raise Rejected('INVALID_COVERAGE')
        avail=self.s.clock.now if available_at is None else timestamp(available_at)
        if avail<self.s.clock.now:raise Rejected('BACKDATED_LOCAL_AVAILABILITY')
        with self.s.db:
            cid=self.s.id('coverage');self.s.db.execute('INSERT INTO coverage VALUES(?,?,?,?,?,?,?,?)',(cid,app,start,end,status,self.s.clock.now,avail,source_ref))
            self.s.bump_graph();self.audit.append('coverage_recorded',dict(coverage_ref=cid,status=status,app_ref=app))
        return cid
    def visible_ledger(self,as_of):
        t=timestamp(as_of)
        if t>self.s.clock.now:raise Rejected('FUTURE_AS_OF')
        # Select the newest economically revised value that was actually known then.
        rows=self.s.db.execute('''SELECT l.* FROM ledger l WHERE deleted=0 AND occurred_at<=? AND observed_at<=? AND available_at<=?
         AND revision=(SELECT MAX(x.revision) FROM ledger x WHERE x.app_ref=l.app_ref AND x.source=l.source AND x.economic_key=l.economic_key
           AND x.deleted=0 AND x.occurred_at<=? AND x.observed_at<=? AND x.available_at<=?) ORDER BY id''',(t,t,t,t,t,t)).fetchall()
        return [dict(x) for x in rows]

class GraphFeatureService:
    def __init__(self,s,policy,graph,events,audit):self.s=s;self.policy=policy;self.graph=graph;self.events=events;self.audit=audit
    @staticmethod
    def admit_backend(capabilities):
        required=['created_timestamp_filter_supported','created_means_consumer_available','exclude_null_created','explicit_relationship_known_at','consent_epoch_gate']
        missing=[k for k in required if capabilities.get(k) is not True]
        return dict(status='STOP' if missing else 'ADAPTER_CONTRACT_ELIGIBLE',missing=missing,
            scope='CAPABILITY_CONTRACT_ONLY;NOT_A_FEAST_RUNTIME_TEST')
    def compute(self,subject,*,as_of=None,since_at=0,purpose=PURPOSE):
        t=self.s.clock.now if as_of is None else timestamp(as_of);since=timestamp(since_at)
        if since>t or t>self.s.clock.now:raise Rejected('FEATURE_TIME_INVALID')
        target=self.s.entity(subject)
        if target['created_at']>t:raise Rejected('ENTITY_NOT_KNOWN_AS_OF')
        self.policy.require([subject],purpose,as_of=t)
        edges=self.graph.active(t,purpose);apps=[];relations=[];entities={subject};incomplete=[]
        if target['entity_type']=='app_instance':apps=[subject]
        elif target['entity_type']=='account':
            selected=[e for e in edges if e['kind']=='logged_in_as' and e['dst']==subject]
            apps=sorted({e['src'] for e in selected});relations.extend(selected)
        elif target['entity_type']=='device':
            devices=set(self.graph.component(subject,t,purpose))
            selected=[e for e in edges if e['kind']=='installed_on' and e['dst'] in devices]
            apps=sorted({e['src'] for e in selected});relations.extend(selected)
            relations.extend(e for e in edges if e['kind']=='same_device' and e['src'] in devices and e['dst'] in devices)
            entities|=devices
        else:incomplete.append('NO_SUPPORTED_PERSON_OR_HOUSEHOLD_RELATION')
        accepted=[]
        for app in apps:
            installed=[e for e in edges if e['kind']=='installed_on' and e['src']==app]
            if len(installed)!=1:
                incomplete.append('MISSING_OR_AMBIGUOUS_INSTALL_RELATION');continue
            participants=[app,installed[0]['dst']]
            if not all(self.policy.allowed(e,purpose,as_of=t) for e in participants):
                incomplete.append('SOURCE_CONSENT_EXCLUDED');continue
            accepted.append(app);entities.update(participants);relations.extend(installed)
        if not accepted:incomplete.append('NO_ELIGIBLE_APP_OBSERVATION')
        totals={};ledger=[]
        for row in self.events.visible_ledger(t):
            if row['app_ref'] not in accepted or row['economic_at']<since:continue
            if target['entity_type']=='account':
                if row['account_ref']!=subject:continue
                # Authentication must cover the original economic event, not just now.
                if not any(e['kind']=='logged_in_as' and e['src']==row['app_ref'] and e['dst']==subject and
                    e['valid_from']<=row['economic_at'] and (e['valid_to'] is None or row['economic_at']<e['valid_to']) for e in relations):continue
            totals[row['currency']]=totals.get(row['currency'],0)+row['amount_micros'];ledger.append(row)
        coverage_refs=[];coverage_status=[]
        for app in accepted:
            c=self.s.db.execute('''SELECT * FROM coverage WHERE app_ref=? AND observed_at<=? AND available_at<=?
                ORDER BY observed_at DESC,id DESC LIMIT 1''',(app,t,t)).fetchone()
            if c is None:coverage_status.append('NOT_OBSERVED')
            else:
                coverage_refs.append(c['id']);coverage_status.append(c['status'] if c['start_at']<=since and c['end_at']>=t else 'MISSING')
        complete=bool(accepted) and not incomplete and all(x=='COMPLETE' for x in coverage_status)
        currency=next(iter(totals)) if len(totals)==1 else (None if totals else 'USD')
        observed=sum(totals.values()) if len(totals)<=1 else None
        if len(totals)>1:observation='MIXED_CURRENCY';complete=False
        elif complete:observation='KNOWN_ZERO' if observed==0 else 'OBSERVED_COMPLETE'
        elif 'EXITED' in coverage_status:observation='EXITED_OBSERVATION'
        elif 'MISSING' in coverage_status:observation='MISSING_OBSERVATION'
        else:observation='NOT_FULLY_OBSERVED'
        values=dict(observed_revenue_micros=observed,revenue_micros=observed if complete else None,
            observed_ledger_count=len(ledger),app_instance_count=len(accepted),currency=currency,
            revenue_by_currency_micros=totals,observation_status=observation,person_inferred=False)
        lineage=dict(entity_refs=sorted(entities),edge_revisions=sorted({(e['id'],e['revision']) for e in relations}),
            event_refs=[r['event_ref'] for r in ledger],ledger_refs=[r['id'] for r in ledger],coverage_refs=coverage_refs,
            incomplete_reasons=sorted(set(incomplete)),feature_group='observed-economic-history-v1',environment=ENV)
        with self.s.db:
            bid=self.s.id('bundle');self.s.db.execute('INSERT INTO feature_bundles VALUES(?,?,?,?,?,?,?,?,?,?,?,?)',
                (bid,subject,purpose,t,since,self.s.clock.now,self.s.clock.now,self.s.graph_version,self.s.epoch,canonical(lineage),canonical(values),'ACTIVE'))
            self.audit.append('feature_materialized',dict(bundle_ref=bid,subject_ref=subject,as_of=t,materialized_at=self.s.clock.now,
                available_at=self.s.clock.now,graph_version=self.s.graph_version,policy_epoch=self.s.epoch))
        return dict(bundle_ref=bid,as_of=t,consumer_available_at=self.s.clock.now,values=values,lineage=lineage,
                    graph_version=self.s.graph_version,policy_epoch=self.s.epoch)
    def read(self,bundle_ref,*,purpose=PURPOSE):
        row=self.s.db.execute('SELECT * FROM feature_bundles WHERE id=?',(bundle_ref,)).fetchone()
        if row is None:raise Rejected('UNKNOWN_BUNDLE')
        if row['status']!='ACTIVE' or row['values_json'] is None:raise Rejected('BUNDLE_INVALIDATED_OR_DELETED')
        if row['purpose']!=purpose:raise Rejected('BUNDLE_PURPOSE_MISMATCH')
        if row['graph_version']!=self.s.graph_version or row['policy_epoch']!=self.s.epoch:raise Rejected('STALE_GRAPH_OR_POLICY_EPOCH')
        if row['available_at']>self.s.clock.now:raise Rejected('BUNDLE_NOT_YET_AVAILABLE')
        lineage=json.loads(row['lineage_json']);self.policy.require(lineage['entity_refs'],purpose,as_of=row['as_of'])
        current={(e['id'],e['revision']) for e in self.graph.active(purpose=purpose)}
        if not all(tuple(e) in current for e in lineage['edge_revisions']):raise Rejected('RELATION_REVOKED_OR_EXPIRED')
        with self.s.db:
            read=self.s.id('read');self.audit.append('feature_read',dict(feature_read_ref=read,bundle_ref=bundle_ref,read_at=self.s.clock.now,purpose=purpose))
        return dict(feature_read_ref=read,bundle_ref=bundle_ref,values=json.loads(row['values_json']),read_at=self.s.clock.now,lineage=lineage)
    def consume_local(self,bundle_ref,*,product='synthetic-mvp',model='local-feature-consumer',model_version='1',decision_at=None,use='active'):
        decision_time=self.s.clock.now if decision_at is None else timestamp(decision_at)
        if decision_time!=self.s.clock.now:raise Rejected('BACKDATED_OR_FUTURE_DECISION_FORBIDDEN')
        if not all(isinstance(x,str) and x for x in [product,model,model_version]) or use not in ['active','shadow','unused']:raise Rejected('CONSUMER_CONTRACT_INVALID')
        value=self.read(bundle_ref);row=self.s.db.execute('SELECT * FROM feature_bundles WHERE id=?',(bundle_ref,)).fetchone()
        with self.s.db:
            rid=self.s.id('resolution');rec=self.s.id('receipt');inf=self.s.id('inference');dec=self.s.id('decision');opp=self.s.id('opportunity')
            # Actually read the local feature value; this consumer is a checksum probe,
            # NOT a trained LTV model, conversion score, ad decision or bid controller.
            checksum=digest(value['values'])
            self.audit.append('local_consumer_read',dict(inference_ref=inf,feature_read_ref=value['feature_read_ref'],bundle_ref=bundle_ref,
                model=model,model_version=model_version,decision_ref=dec,opportunity_ref=opp,use=use,consumed_checksum=checksum))
        ev=dict(environment=ENV,policy_valid=True,
            provenance=dict(source_authenticated=True,independently_reviewed=True,quotation_permitted=True,coverage_complete=True,
                            meaning='SEEDED_LOCAL_FIXTURE_ATTESTATIONS_ONLY'),
            resolution=dict(ref=rid,status='existing_entity_asserted',grain=self.s.entity(row['subject_ref'])['entity_type'],component_version='independent-local-v1',purpose=PURPOSE,available_at=row['available_at']),
            receiver=dict(ref=rec,resolution_ref=rid,product=product,received_at=row['available_at'],available_at=row['available_at'],purpose=PURPOSE),
            read=dict(ref=value['feature_read_ref'],receiver_ref=rec,bundle_ref=bundle_ref,product=product,model=model,model_version=model_version,
                feature_group='observed-economic-history-v1',graph_version=row['graph_version'],inference_ref=inf,
                nonempty_refs=[k for k,v in value['values'].items() if v is not None],read_at=value['read_at'],purpose=PURPOSE,default_fallback=False),
            decision=dict(ref=dec,read_ref=value['feature_read_ref'],inference_ref=inf,model_version=model_version,opportunity_ref=opp,decision_at=decision_time,use=use,purpose=PURPOSE),
            consumed_checksum=checksum,consumer_kind='CHECKSUM_PROBE_NOT_LTV_MODEL')
        return ev

class IdentitySystem:
    """Local single-writer facade; SQLite state + non-restored privacy authority."""
    def __init__(self,directory,*,clock=None,fixture_key=b'public-synthetic-test-key-not-production'):
        self.clock=clock or ManualClock();self.store=Store(directory,self.clock)
        self.audit=ProvenanceAuditLog(self.store)
        if not self.audit.verify():self.store.close();raise Rejected('AUDIT_INTEGRITY_FAILURE')
        self.namespaces=IdentityNamespaceRegistry(self.store,self.audit)
        self.policy=ConsentAndDeletionManager(self.store,self.audit)
        self.graph=ConfidenceAwareRelationshipGraph(self.store,self.policy,self.audit)
        self.resolver=DeterministicIdentityResolver(self.store,self.namespaces,self.policy,self.graph,self.audit,fixture_key)
        self.events=TemporalEventLinker(self.store,self.policy,self.graph,self.audit)
        self.features=GraphFeatureService(self.store,self.policy,self.graph,self.events,self.audit)
        self.policy.reconcile()
    def backup_state(self,path):
        path=Path(path)
        if path.resolve() in [(self.store.directory/'state.sqlite').resolve(),(self.store.directory/'privacy.sqlite').resolve()]:raise Rejected('BACKUP_TARGET_IS_LIVE_DATABASE')
        with sqlite3.connect(str(path)) as dst:self.store.db.backup(dst)
        return str(path)
    def restore_state(self,path):
        """Restore data only; durable privacy.sqlite must never roll back with it."""
        path=Path(path)
        with sqlite3.connect('file:'+path.resolve().as_posix()+'?mode=ro',uri=True) as backup:
            env=backup.execute("SELECT value FROM meta WHERE key='environment'").fetchone()
            if not env or env[0]!=ENV:raise Rejected('BACKUP_ENVIRONMENT_INVALID')
            self.store.db.commit();backup.backup(self.store.db)
        if not self.audit.verify():raise Rejected('BACKUP_AUDIT_INTEGRITY_FAILURE')
        self.policy.reconcile()
        # Every cached value must be invalidated even if backup predates a non-deletion revocation.
        with self.store.db:self.store.bump_graph();self.audit.append('state_restored',dict(privacy_authority_restored=False))
    def training_snapshot(self,entities,*,trained_model=False):
        for e in entities:self.store.entity(e)
        with self.store.db:
            sid=self.store.id('training');self.store.db.execute('INSERT INTO training_snapshots VALUES(?,?,?,?)',(sid,canonical(sorted(set(entities))),int(trained_model),'ACTIVE'))
            self.audit.append('synthetic_training_lineage_registered',dict(snapshot_ref=sid,trained_model_claim=bool(trained_model),actual_training_executed=False))
        return sid
    @staticmethod
    def ltv_admission(metadata):
        required=['real_game_data','lawful_use','stable_scope','complete_install_denominator','mature_revenue_labels','observation_missingness_known','temporal_holdout','feature_available_times','comparison_authorized']
        missing=[k for k in required if metadata.get(k) is not True]
        if metadata.get('synthetic',True):missing.append('REAL_DATA_NOT_SYNTHETIC')
        return dict(status='STOP' if missing else 'REVIEW_REQUIRED_NOT_AUTO_TRAIN',missing=missing,model_training_executed=False,D='UNKNOWN')
    def close(self):self.store.close()
