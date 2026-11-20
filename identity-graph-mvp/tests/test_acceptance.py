import copy,functools,json,sqlite3,unittest
from pathlib import Path
from identity_mvp.fixtures import SyntheticWorld
from identity_mvp.system import PURPOSE,Rejected,ProvenanceAuditLog,GraphFeatureService

CONFIG={'seed':760078,'output':Path('results/manual')}
def serial(value):
    if isinstance(value,Path):return str(value)
    return json.loads(json.dumps(value,ensure_ascii=False,default=str))
class RecordedTest(unittest.TestCase):
    case_id='BASE'
    def setUp(self):
        self.case_id=self._testMethodName.split('_')[1]
        self.folder=CONFIG['output']/'cases'/self.case_id;self.folder.mkdir(parents=True,exist_ok=False)
        self.checks=[];self.calls=[];self.world=SyntheticWorld(self.folder/'database',CONFIG['seed']);self.s=self.world.system
        self.audit_records=[]
        for obj in [self.world,self.s,self.s.clock,self.s.namespaces,self.s.resolver,self.s.graph,self.s.policy,self.s.events,self.s.features]:
            for name in dir(type(obj)):
                if name.startswith('_') or name in ['close','manifest','case','records','verify','deleted','allowed','require','active','component']:continue
                method=getattr(obj,name,None)
                if not callable(method):continue
                def wrap(method,name,owner):
                    @functools.wraps(method)
                    def traced(*a,**kw):
                        entry=dict(component=owner,operation=name,at=self.s.clock.now,args=serial(a),kwargs=serial(kw));self.calls.append(entry)
                        try:
                            result=method(*a,**kw);entry['returned']=serial(result);return result
                        except Exception as exc:
                            entry['raised']=dict(type=type(exc).__name__,message=str(exc));raise
                    return traced
                setattr(obj,name,wrap(method,name,type(obj).__name__))
    def tearDown(self):
        self.audit_records=self.s.audit.records();self.fixture_manifest=self.world.manifest();self.world.close()
    def eq(self,label,actual,expected):
        self.checks.append(dict(assertion=label,input_refs='operation trace',expected=serial(expected),actual=serial(actual),passed=actual==expected))
        self.assertEqual(actual,expected,label)
    def rejects(self,label,call,reason):
        try:call()
        except Rejected as exc:actual=str(exc)
        else:actual='NOT_REJECTED'
        self.eq(label,actual,reason)
    def base(self):return self.world.pair()
    def amount(self,subject,as_of=None):return self.s.features.compute(subject,as_of=as_of,since_at=self.world.start)['values']['observed_revenue_micros']
    def evidence(self):
        _,app,account=self.base();self.world.revenue(app,12_000_000,account=account)
        bundle=self.s.features.compute(account,since_at=self.world.start)
        return self.s.features.consume_local(bundle['bundle_ref'])

class AcceptanceSuite(RecordedTest):
    def test_V01_namespace_isolation(self):
        a=self.world.entity('a','device',token='syn:same',issuer='synthetic:issuer-a')
        b=self.world.entity('b','device',token='syn:same',issuer='synthetic:issuer-b')
        self.eq('same bare value is not same scoped identity',self.s.namespaces.compare(a,b),'DIFFERENT_NAMESPACE')
        self.eq('separate records',a==b,False)
        unknown=self.s.namespaces.register(tenant='synthetic-tenant',issuer='synthetic:unknown',app='a',sector='a',entity_type='device',scope='UNKNOWN')
        self.rejects('unknown scope abstains',lambda:self.s.namespaces.create(unknown,'syn:unknown'),'UNKNOWN_SCOPE')
    def test_V02_pairwise_sector(self):
        a=self.world.entity('a','account',sector='sector-a',token='syn:same')
        b=self.world.entity('b','account',sector='sector-b',token='syn:same')
        na=self.s.store.entity(a)['namespace_id'];nb=self.s.store.entity(b)['namespace_id']
        self.eq('different sectors cannot implicitly map',self.s.namespaces.mapping_allowed(na,nb),False)
        self.s.namespaces.authorize_mapping(na,nb,evidence='synth:explicit-sector-mapping')
        self.eq('explicit scoped permission recorded',self.s.namespaces.mapping_allowed(na,nb),True)
        self.eq('permission is not proof of same subject',self.s.namespaces.compare(a,b),'DIFFERENT_NAMESPACE')
        same=self.world.entity('same-a','account',sector='sector-a',token='syn:same')
        self.eq('same namespace exact key reused',a,same)
        self.eq('no person records generated',self.s.store.db.execute("SELECT count(*) FROM entities WHERE entity_type='person'").fetchone()[0],0)
    def test_V03_authentication_and_replay(self):
        d=self.world.entity('d','device');app=self.world.install('i',d);a=self.world.entity('a','account')
        assertion,signature=self.world.assertion(a,app,d)
        self.eq('valid local fixture authenticates account relation',self.s.resolver.login(assertion,signature)['status'],'ACCOUNT_RELATION_ESTABLISHED')
        self.rejects('nonce replay refused',lambda:self.s.resolver.login(assertion,signature),'AUTH_REPLAY')
        self.rejects('wrong signed audience refused',lambda:self.world.login(a,app,d,audience='other-app'),'AUTH_ISSUER_OR_AUDIENCE')
        self.rejects('expired local assertion refused',lambda:self.world.login(a,app,d,expires_at=self.s.clock.now),'AUTH_TIME_INVALID')
        self.rejects('invalid signature refused',lambda:self.s.resolver.login(assertion,'invalid'),'BAD_FIXTURE_SIGNATURE')
        self.eq('only one account relation',len([e for e in self.s.graph.active() if e['kind']=='logged_in_as']),1)
    def test_V04_account_multidevice_and_shared_device(self):
        d1,i1,a=self.base();d2=self.world.entity('device-b','device');i2=self.world.install('app-b',d2,app='synthetic-app-b');b=self.world.entity('account-b','account')
        self.world.login(a,i2,d2);self.world.login(b,i1,d1)
        self.world.revenue(i1,100,account=a);self.world.revenue(i2,200,account=a);self.world.revenue(i1,700,account=b)
        self.eq('single account spans its two devices',self.amount(a),300)
        self.eq('shared device does not mix account B with A',self.amount(b),700)
        self.eq('no person identity inferred',self.s.features.compute(a)['values']['person_inferred'],False)
        self.eq('account nodes never union',self.s.graph.component(a),[a])
    def test_V05_uncalibrated_candidate(self):
        a=self.world.entity('a','device');b=self.world.entity('b','device')
        edge=self.s.graph.add(a,b,'candidate_same_entity',source_ref='synth:probability-candidate',confidence=.9999)
        self.eq('high score remains candidate',edge['status'],'CANDIDATE')
        self.eq('no automatic transitive or irreversible merge',self.s.graph.component(a),[a])
        row=self.s.store.db.execute('SELECT quality_kind FROM edge_revisions WHERE id=?',(edge['edge_ref'],)).fetchone()
        self.eq('uncalibrated score labeled',row[0],'uncalibrated_score')
    def test_V06_bridge_conflict(self):
        a,b,c=[self.world.entity(x,'device') for x in ['a','b','c']]
        self.s.graph.add(a,c,'cannot_link',source_ref='synth:cannot-link')
        self.s.graph.add(a,b,'same_device',source_ref='synth:local-truth')
        edge=self.s.graph.add(b,c,'same_device',source_ref='synth:bad-bridge')
        self.eq('bridge violating cannot-link quarantined',edge['status'],'CONFLICT')
        self.eq('A/B component excludes C',self.s.graph.component(a),sorted([a,b]))
    def test_V07_revocation_split_and_feature_invalidation(self):
        a,b,c=[self.world.entity(x,'device') for x in ['a','b','c']]
        self.s.graph.add(a,b,'same_device',source_ref='synth:local-truth')
        bridge=self.s.graph.add(b,c,'same_device',source_ref='synth:local-truth')
        app=self.world.install('app-c',c);self.world.revenue(app,900)
        bundle=self.s.features.compute(a);self.eq('fixture connected relation serves C history',bundle['values']['observed_revenue_micros'],900)
        self.s.clock.advance();self.s.graph.revoke(bridge['edge_ref'],reason='synth:incorrect-relation')
        self.eq('graph split after wrong edge revoke',self.s.graph.component(a),sorted([a,b]))
        self.eq('C becomes separate',self.s.graph.component(c),[c])
        self.rejects('old derived bundle blocked',lambda:self.s.features.read(bundle['bundle_ref']),'BUNDLE_INVALIDATED_OR_DELETED')
        self.eq('new history does not leak across revoked bridge',self.amount(a),0)
    def test_V08_relationship_known_time(self):
        a=self.world.entity('a','device');b=self.world.entity('b','device');app=self.world.install('b-app',b);self.world.revenue(app,1700)
        old=self.s.clock.now;self.s.clock.advance(5)
        self.s.graph.add(a,b,'same_device',source_ref='synth:late-discovery',valid_from=old)
        self.eq('backfilled validity cannot leak knowledge into old decision',self.amount(a,old),0)
        self.eq('later query can use newly known relation',self.amount(a),1700)
    def test_V09_event_idempotence(self):
        _,app,account=self.base()
        kw=dict(account=account,event_id='synth:event-one',economic_key='synth:order-one')
        self.world.revenue(app,1100,**kw)
        self.eq('event retry deduplicated',self.world.revenue(app,1100,**kw)['status'],'DUPLICATE_EVENT')
        self.rejects('same event ID with different payload is conflict',lambda:self.world.revenue(app,1200,**kw),'IDEMPOTENCY_PAYLOAD_CONFLICT')
        self.world.revenue(app,1100,account=account,event_id='synth:event-two',economic_key='synth:order-two')
        self.eq('two genuine business events survive',self.amount(account),2200)
        self.eq('exactly two local economic entries',len(self.s.events.visible_ledger(self.s.clock.now)),2)
    def test_V10_economic_exhibition_not_load(self):
        _,app,account=self.base()
        for n in range(3):self.s.events.ingest(app=app,source_name='synth:ads',event_id=f'synth:load-{n}',event_type='load',occurred_at=self.s.clock.now,
            opportunity_ref='synth:opportunity-1',candidate_ref=f'synth:candidate-{n}')
        self.world.revenue(app,300,account=account,event_id='synth:ilrd-1',economic_key='synth:impression-1',economic_kind='IAA',impression_ref='synth:impression-1')
        duplicate=self.world.revenue(app,300,account=account,event_id='synth:ilrd-adapter-duplicate',economic_key='synth:impression-1',economic_kind='IAA',impression_ref='synth:impression-1')
        self.eq('duplicate economic callback suppressed',duplicate['status'],'DUPLICATE_LEDGER')
        self.eq('loads/candidates do not become money',self.amount(account),300)
        self.eq('one economic impression entry',len(self.s.events.visible_ledger(self.s.clock.now)),1)
    def test_V11_late_revenue_and_refund(self):
        _,app,account=self.base()
        first=self.world.revenue(app,10000,account=account,economic_key='synth:order-original');old=self.s.clock.now
        self.s.clock.advance(10)
        self.world.revenue(app,4000,account=account,occurred_at=old+1)
        self.world.revenue(app,7000,account=account,economic_key='synth:order-original',revision=2,correction_of=first['ledger_ref'])
        self.eq('late amount and refund not available at old prediction',self.amount(account,old),10000)
        self.eq('new query uses revised net total not both revisions',self.amount(account),11000)
        replay=self.s.features.compute(account,as_of=old)
        self.eq('historical replay is materialized now',replay['consumer_available_at'],self.s.clock.now)
        self.rejects('cannot fabricate old active decision',lambda:self.s.features.consume_local(replay['bundle_ref'],decision_at=old),'BACKDATED_OR_FUTURE_DECISION_FORBIDDEN')
    def test_V12_zero_vs_missing_vs_exit(self):
        d=self.world.entity('d','device');apps=[self.world.install(n,d) for n in ['zero','missing','exit']]
        for a,state in zip(apps,['COMPLETE','MISSING','EXITED']):self.s.events.coverage(a,start_at=self.world.start,end_at=self.s.clock.now,status=state)
        values=[self.s.features.compute(a,since_at=self.world.start)['values'] for a in apps]
        self.eq('only completely observed no-purchase is zero',[v['revenue_micros'] for v in values],[0,None,None])
        self.eq('missingness distinctions preserved',[v['observation_status'] for v in values],['KNOWN_ZERO','MISSING_OBSERVATION','EXITED_OBSERVATION'])
    def test_V13_backend_admission(self):
        good=dict(created_timestamp_filter_supported=True,created_means_consumer_available=True,exclude_null_created=True,explicit_relationship_known_at=True,consent_epoch_gate=True)
        self.eq('explicit local adapter capability contract eligible',self.s.features.admit_backend(good)['status'],'ADAPTER_CONTRACT_ELIGIBLE')
        for key in good:
            bad=dict(good);bad[key]=False
            self.eq('missing backend guarantee '+key,self.s.features.admit_backend(bad)['status'],'STOP')
        self.eq('not a Feast runtime claim',self.s.features.admit_backend(good)['scope'],'CAPABILITY_CONTRACT_ONLY;NOT_A_FEAST_RUNTIME_TEST')
    def test_V14_revoked_consent_blocks_cache(self):
        _,app,account=self.base();self.world.revenue(app,100,account=account);bundle=self.s.features.compute(account)
        self.s.clock.advance();self.s.policy.set(account,PURPOSE,False)
        self.rejects('old cache denied after revoke',lambda:self.s.features.read(bundle['bundle_ref']),'BUNDLE_INVALIDATED_OR_DELETED')
        self.rejects('new feature query denied',lambda:self.s.features.compute(account),'CONSENT_DENIED_OR_UNKNOWN')
        self.eq('old values removed from persistent cache',self.s.store.db.execute('SELECT values_json FROM feature_bundles WHERE id=?',(bundle['bundle_ref'],)).fetchone()[0],None)
    def test_V15_deletion_propagation_and_pending_sink(self):
        _,app,account=self.base();self.world.revenue(app,900,account=account);self.s.features.compute(account)
        case=self.s.policy.delete(app,extra_sinks=['synthetic:offline-export'])
        self.eq('unconfirmed downstream sink prevents completion',case['state'],'ACK_PENDING')
        self.eq('pending sink explicit',case['pending_sinks'],['synthetic:offline-export'])
        self.eq('local token purged',self.s.store.db.execute('SELECT token FROM entities WHERE id=?',(app,)).fetchone()[0],None)
        self.eq('local economic source deleted',len(self.s.events.visible_ledger(self.s.clock.now)),0)
        self.eq('no sensitive event payload left',self.s.store.db.execute('SELECT count(*) FROM events WHERE app_ref=? AND payload_json IS NOT NULL',(app,)).fetchone()[0],0)
        self.eq('outbox payload purged',self.s.store.db.execute('SELECT count(*) FROM outbox WHERE payload_json IS NOT NULL').fetchone()[0],0)
        self.eq('derived values purged',self.s.store.db.execute('SELECT count(*) FROM feature_bundles WHERE values_json IS NOT NULL').fetchone()[0],0)
        complete=self.s.policy.acknowledge(case['id'],'synthetic:offline-export',source_ref='synth:export-deletion-fixture-ack')
        self.eq('bounded declared sink scope complete',complete['state'],'COMPLETE_FOR_DECLARED_SCOPE')
        self.eq('audit preserved without identity tokens',self.s.audit.verify(),True)
    def test_V16_backup_restore_cannot_resurrect(self):
        _,app,account=self.base();token=self.s.store.entity(app)['token'];namespace=self.s.store.entity(app)['namespace_id']
        self.world.revenue(app,900,account=account);self.s.features.compute(account)
        path=self.folder/'before-deletion.sqlite';self.s.backup_state(path)
        case=self.s.policy.delete(app);self.s.restore_state(path)
        self.eq('restored entity remains deleted',self.s.store.db.execute('SELECT deleted FROM entities WHERE id=?',(app,)).fetchone()[0],1)
        self.eq('restored revenue stays purged',len(self.s.events.visible_ledger(self.s.clock.now)),0)
        self.rejects('deleted key replay cannot create new identity',lambda:self.s.namespaces.create(namespace,token),'DELETED_KEY_REPLAY')
        self.eq('durable delete control not rolled back',self.s.policy.case(case['id'])['state'],'COMPLETE_FOR_DECLARED_SCOPE')
    def test_V17_training_influence_unknown(self):
        _,app,account=self.base();snap=self.s.training_snapshot([account,app],trained_model=True)
        case=self.s.policy.delete(account)
        self.eq('source snapshot blocked',self.s.store.db.execute('SELECT status FROM training_snapshots WHERE id=?',(snap,)).fetchone()[0],'BLOCKED_DELETED_SOURCE')
        self.eq('no fake model unlearning confirmation',case['training_disposition'],'MODEL_ERASURE_UNKNOWN')
        self.eq('scope not declared wholly erased',case['state'],'EXCEPTION_OR_UNKNOWN')
    def test_V18_incomplete_consumption_chain(self):
        good=self.evidence();self.eq('local complete trace checks only local consistency',self.s.audit.assess_chain(good)['status'],'LOCAL_CHAIN_VERIFIED')
        absent=copy.deepcopy(good);del absent['receiver']
        self.eq('materialization without receiver insufficient',self.s.audit.assess_chain(absent)['status'],'NOT_IDENTIFIABLE')
        fallback=copy.deepcopy(good);fallback['read']['default_fallback']=True
        self.eq('default values not graph consumption',self.s.audit.assess_chain(fallback)['reason'],'NO_NONEMPTY_MODEL_INPUT')
        empty=copy.deepcopy(good);empty['read']['nonempty_refs']=[]
        self.eq('empty read not graph consumption',self.s.audit.assess_chain(empty)['status'],'NOT_IDENTIFIABLE')
        derived=copy.deepcopy(good);derived['resolution']['status']='new_derived_key'
        self.eq('derived ID is not existing-entity match',self.s.audit.assess_chain(derived)['reason'],'NON_MATCH_OR_DERIVED_ID')
    def test_V19_product_separation(self):
        good=self.evidence()
        for receiver,consumer in [('Unity Exchange','Vector'),('Adjust','Axon')]:
            mismatch=copy.deepcopy(good);mismatch['receiver']['product']=receiver;mismatch['read']['product']=consumer
            self.eq(receiver+' receipt does not prove '+consumer,self.s.audit.assess_chain(mismatch)['reason'],'PRODUCT_MISMATCH')
        production=copy.deepcopy(good);production['environment']='PRODUCTION'
        self.eq('local verifier cannot authorize production claim',self.s.audit.assess_chain(production)['status'],'NOT_IDENTIFIABLE')
    def test_V20_authenticity_and_quotation(self):
        good=self.evidence()
        for key in ['source_authenticated','independently_reviewed','quotation_permitted','coverage_complete']:
            weakened=copy.deepcopy(good);weakened['provenance'][key]=False
            self.eq('same checksum insufficient without '+key,self.s.audit.assess_chain(weakened)['status'],'UNTRUSTED')
        result=self.s.audit.assess_chain(good)
        self.eq('vendor claims remain UNKNOWN',[result['C_graph_Axon'],result['C_graph_Vector'],result['D']],['UNKNOWN']*3)

class RegressionSuite(RecordedTest):
    def test_R01_late_cannot_link(self):
        a,b,c=[self.world.entity(x,'device') for x in ['a','b','c']]
        self.s.graph.add(a,b,'same_device',source_ref='synth:truth');self.s.graph.add(b,c,'same_device',source_ref='synth:truth')
        self.s.graph.add(a,c,'cannot_link',source_ref='synth:late-cannot-link')
        self.eq('new constraint invalidates old connected component',self.s.graph.component(a),[a])
    def test_R02_identifier_reset(self):
        d,app,account=self.base();self.world.revenue(app,400,account=account);bundle=self.s.features.compute(d)
        reset=self.s.graph.reset_device(d)
        new=self.world.entity('new-ad-id','device');newapp=self.world.install('new-install',new)
        self.eq('reset does not recover old identity',reset['restored_old_identity'],False)
        self.eq('new identifier has no old money',self.amount(new),0)
        self.rejects('reset invalidates old feature cache',lambda:self.s.features.read(bundle['bundle_ref']),'BUNDLE_INVALIDATED_OR_DELETED')
        self.eq('old device no longer collected',self.s.policy.allowed(d,PURPOSE),False)
    def test_R03_multiapp_same_device(self):
        d,app,a=self.base();b=self.world.install('app-b',d,app='synthetic-app-b');self.world.revenue(app,100,account=a);self.world.revenue(b,250)
        self.eq('same device authorized multiapp view',self.amount(d),350)
        self.eq('same account does not inherit untagged other-app revenue',self.amount(a),100)
        self.eq('device and person remain different grains',self.s.store.entity(d)['entity_type'],'device')
    def test_R04_wrong_entity_grain(self):
        d,app,a=self.base();p=self.world.entity('person','person')
        self.rejects('cannot promote account to person via same_device edge',lambda:self.s.graph.add(a,p,'same_device',source_ref='synth:bad-grain'),'RELATION_GRAIN_MISMATCH')
        self.eq('person remains unlinked',self.amount(p),0)
    def test_R05_economic_conflicts(self):
        _,app,a=self.base();self.world.revenue(app,100,account=a,economic_key='synth:impression')
        self.rejects('same economic revision cannot change amount',lambda:self.world.revenue(app,200,account=a,economic_key='synth:impression'),'ECONOMIC_REVISION_CONFLICT')
        self.rejects('no orphan revision',lambda:self.world.revenue(app,200,account=a,revision=3,correction_of='ledger_missing'),'CORRECTION_CHAIN_REQUIRED')
        self.eq('failed mutations do not add economic entries',len(self.s.events.visible_ledger(self.s.clock.now)),1)
    def test_R06_invalid_times_and_future_availability(self):
        _,app,a=self.base()
        self.rejects('float timestamp refused',lambda:self.world.revenue(app,100,account=a,occurred_at=1.5),'INVALID_UTC_SECOND')
        self.rejects('future event refused',lambda:self.world.revenue(app,100,account=a,occurred_at=self.s.clock.now+1),'EVENT_TIME_INVALID')
        self.world.revenue(app,100,account=a,available_at=self.s.clock.now+10)
        self.eq('future-available economic row not leaked',self.amount(a),0)
        self.s.clock.advance(10);self.eq('becomes visible only at declared availability',self.amount(a),100)
    def test_R07_restore_nonce_and_id_safety(self):
        d,app,a=self.base();before=int(self.s.store.control.execute("SELECT value FROM control_meta WHERE key='id_counter'").fetchone()[0])
        path=self.folder/'state.sqlite.backup';self.s.backup_state(path)
        new=self.world.entity('deleted-later','device');self.s.policy.delete(new);self.s.restore_state(path)
        another=self.world.entity('new-after-restore','device')
        self.eq('identity IDs never reused after state rollback',new==another,False)
        self.eq('deleted subject authority survives rollback',self.s.policy.deleted(new),True)
    def test_R08_mixed_currency(self):
        _,app,a=self.base();self.world.revenue(app,100,account=a,currency='USD');self.world.revenue(app,200,account=a,currency='EUR')
        v=self.s.features.compute(a)['values']
        self.eq('no implicit currency conversion',v['observed_revenue_micros'],None)
        self.eq('currencies retained',v['revenue_by_currency_micros'],{'USD':100,'EUR':200})
    def test_R09_audit_tampering_detected(self):
        self.base();self.eq('untampered chain valid',self.s.audit.verify(),True)
        with self.s.store.db:self.s.store.db.execute("UPDATE audit_log SET kind='tampered' WHERE seq=1")
        self.eq('tampering invalidates chain',self.s.audit.verify(),False)
    def test_R10_evidence_temporal_and_model_mismatch(self):
        ev=self.evidence();ev['read']['read_at']+=10
        self.eq('feature unavailable before decision',self.s.audit.assess_chain(ev)['reason'],'TEMPORAL_LEAKAGE')
        ev=self.evidence();ev['decision']['model_version']='different'
        self.eq('cross-version decision refused',self.s.audit.assess_chain(ev)['reason'],'MODEL_INFERENCE_MISMATCH')
        ev=self.evidence();ev['invalid_after']=ev['read']['read_at']
        self.eq('revoked read refused',self.s.audit.assess_chain(ev)['reason'],'REVOKED_OR_EXPIRED')
    def test_R11_scope_of_deletion(self):
        _,app,a=self.base();other=self.world.entity('other-account','account');self.world.login(other,app,self.world.entities['device-a'])
        self.world.revenue(app,100,account=a);self.world.revenue(app,200,account=other)
        self.s.policy.delete(a)
        self.eq('deleting account A does not erase distinct account B business event',self.amount(other),200)
        self.eq('only A-owned economic row erased',len(self.s.events.visible_ledger(self.s.clock.now)),1)
    def test_R12_training_admission(self):
        metadata=dict(synthetic=True,real_game_data=False,lawful_use=True)
        self.eq('synthetic tests cannot authorize real LTV claim',self.s.ltv_admission(metadata)['status'],'STOP')
        self.eq('no model trained by admission',self.s.ltv_admission(metadata)['model_training_executed'],False)
    def test_R13_replay_authority_survives_backup(self):
        d,app,a=self.base();path=self.folder/'before-new-nonce.sqlite';self.s.backup_state(path)
        assertion,signature=self.world.assertion(a,app,d);self.s.resolver.login(assertion,signature)
        self.s.restore_state(path)
        self.rejects('restoring data cannot reset used nonce',lambda:self.s.resolver.login(assertion,signature),'AUTH_REPLAY')
    def test_R14_device_erasure_cascades_without_account_overreach(self):
        d1,app1,a=self.base();d2=self.world.entity('d2','device');app2=self.world.install('app2',d2);self.world.login(a,app2,d2)
        self.world.revenue(app1,100,account=a);self.world.revenue(app2,200,account=a)
        self.s.policy.delete(d1)
        self.eq('device-owned app instance erased',self.s.store.db.execute('SELECT deleted FROM entities WHERE id=?',(app1,)).fetchone()[0],1)
        self.eq('only deleted device contribution removed',self.amount(a),200)
        self.eq('separate device account remains valid',self.s.policy.allowed(a,PURPOSE),True)
        self.eq('erased installation control authority exists',self.s.policy.deleted(app1),True)
    def test_R15_no_unauthenticated_account_edge(self):
        d=self.world.entity('d','device');app=self.world.install('app',d);a=self.world.entity('a','account')
        self.rejects('raw identifier does not authenticate account',lambda:self.s.graph.add(app,a,'logged_in_as',source_ref='synth:claimed-login'),'AUTH_RECEIPT_REQUIRED')
    def test_R16_malformed_evidence_fails_closed(self):
        for bad in [None,[],{'environment':'LOCAL_SYNTHETIC_ONLY','provenance':[]}]:
            self.eq('malformed evidence never crashes or verifies',self.s.audit.assess_chain(bad)['status'],'NOT_IDENTIFIABLE')
        ev=self.evidence();ev['receiver']['purpose']={}
        self.eq('non-scalar purpose rejected',self.s.audit.assess_chain(ev)['status'],'NOT_IDENTIFIABLE')
    def test_R17_edge_expiry_invalidates_cached_use(self):
        d,app,a=self.base()
        e=self.s.graph.add(self.world.entity('device-alias','device'),d,'same_device',source_ref='synth:expiring-relation',valid_to=self.s.clock.now+10)
        alias=self.s.store.db.execute('SELECT src FROM edge_revisions WHERE id=?',(e['edge_ref'],)).fetchone()[0]
        self.world.revenue(app,100,account=a);bundle=self.s.features.compute(alias)
        self.s.clock.advance(10)
        self.rejects('expired edge cannot be consumed from unchanged cache',lambda:self.s.features.read(bundle['bundle_ref']),'RELATION_REVOKED_OR_EXPIRED')
    def test_R18_network_guard_is_active(self):
        import socket
        try:socket.socket()
        except RuntimeError as exc:actual=str(exc)
        else:actual='NETWORK_WAS_NOT_BLOCKED'
        self.eq('runner really blocks socket creation',actual,'NETWORK_DISABLED_FOR_LOCAL_SYNTHETIC_TESTS')
    def test_R19_event_outbox_atomicity(self):
        _,app,a=self.base()
        sql="CREATE TRIGGER synthetic_fail BEFORE INSERT ON outbox BEGIN SELECT RAISE(ABORT,'synthetic-injected-failure'); END"
        self.calls.append(dict(component='SyntheticFaultInjection',operation='sqlite-trigger',input=sql))
        with self.s.store.db:self.s.store.db.execute(sql)
        try:self.world.revenue(app,123,account=a,event_id='synth:atomic-event',economic_key='synth:atomic-order')
        except sqlite3.IntegrityError as exc:actual=str(exc)
        else:actual='FAILURE_NOT_INJECTED'
        self.eq('real SQLite transaction failure triggered',actual,'synthetic-injected-failure')
        for table in ['events','ledger','outbox']:
            self.eq(table+' rolled back on failed outbox insert',self.s.store.db.execute('SELECT count(*) FROM '+table).fetchone()[0],0)
        with self.s.store.db:self.s.store.db.execute('DROP TRIGGER synthetic_fail')
        self.world.revenue(app,123,account=a,event_id='synth:atomic-event',economic_key='synth:atomic-order')
        self.eq('retry after rollback accepts exactly one economic event',self.amount(a),123)
    def test_R20_scheduled_revoke_without_new_writes(self):
        _,app,a=self.base();self.world.revenue(app,100,account=a)
        self.s.policy.set(a,PURPOSE,False,effective_at=self.s.clock.now+5)
        bundle=self.s.features.compute(a)
        self.eq('grant valid before scheduled revoke',self.s.policy.allowed(a,PURPOSE),True)
        self.s.clock.advance(5)
        self.rejects('time gate denies unchanged cache when revoke becomes effective',lambda:self.s.features.read(bundle['bundle_ref']),'CONSENT_DENIED_OR_UNKNOWN')
