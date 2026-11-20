import copy,json,tempfile,unittest,os,shutil
from pathlib import Path
from mock76.service import Service
from mock76.io import Ledger,write,read,digest
from mock76.app_source import emit
from mock76.app_target import request
from mock76.auditor import audit,assess_observable

def rechain(rows):
    prev='0'*64
    for i,r in enumerate(rows,1):
        r.update(seq=i,prev=prev);r.pop('hash',None);r['hash']=digest(r);prev=r['hash']
    return rows

class EngineCase(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name);self.s=Service(self.root)
        self.s.apply(dict(operation='init',route='D1',seed=760031))
        for app in ['source-app','target-app']:self.s.apply(dict(operation='permit',time=0,app=app,device='mock-device-A',allow=True))
    def tearDown(self):
        if os.environ.get('MOCK76_UNIT_LOG_ROOT'):
            destination=Path(os.environ['MOCK76_UNIT_LOG_ROOT'])/self._testMethodName
            destination.parent.mkdir(parents=True,exist_ok=True)
            shutil.copytree(self.root,destination)
        self.tmp.cleanup()
    def event(self,**kw):
        e=dict(event_id='mock-event-1',device='mock-device-A',installation='mock-install-S',event_time=10,available_at=20,category=1,purpose='mock-research',epoch=0);e.update(kw);return emit(e)['event']
    def collect(self,**kw):return self.s.apply(dict(operation='collect',time=12,event=self.event(**kw)))
    def q(self,**kw):
        q=dict(request_id='mock-request-1',device='mock-device-A',installation='mock-install-T',prediction_time=30,epoch=0,purpose='mock-research',context=dict(country='MOCK',model='mock-device',placement='mock-slot'));q.update(kw);return request(q)['request']
    def predict(self,**kw):
        q=self.q(**kw);return self.s.apply(dict(operation='predict',time=q['prediction_time'],request=q))
    def packet(self):
        self.s.apply(dict(operation='close',time=self.s.s['clock']+1));return dict(view='complete_local_audit',records=self.s.log.records())
    def test_available_history_same_device(self):
        self.collect();self.predict();v=audit(self.packet());self.assertEqual(v['routes'],['SAME_DEVICE_HISTORY_READ'])
    def test_future_available_not_read(self):
        self.collect(available_at=80);self.predict();v=audit(self.packet());self.assertEqual(v['routes'],['NO_INDIVIDUAL_HISTORY_READ_OBSERVED'])
    def test_boundary_available_at_equal_prediction(self):
        self.collect(available_at=30);self.predict();self.assertIn('SAME_DEVICE_HISTORY_READ',audit(self.packet())['routes'])
    def test_future_event_rejected(self):
        x=self.collect(event_time=40,available_at=50);self.assertEqual(x['status'],'INVALID_TIME');self.assertFalse(self.s.s['events'])
    def test_available_before_receipt_rejected(self):self.assertEqual(self.collect(available_at=11)['status'],'INVALID_TIME')
    def test_collect_permission_denied(self):
        self.s.apply(dict(operation='permit',time=1,app='source-app',device='mock-device-A',allow=False));self.assertEqual(self.collect()['status'],'DENIED')
    def test_revoked_no_lookup(self):
        self.collect();self.s.apply(dict(operation='permit',time=21,app='source-app',device='mock-device-A',allow=False));self.predict();p=self.packet()
        self.assertFalse(any(x['kind']=='lookup_attempt' for x in p['records']));self.assertEqual(audit(p)['routes'],['GATE_BLOCKED'])
    def test_target_denied_no_lookup(self):
        self.collect();self.s.apply(dict(operation='permit',time=21,app='target-app',device='mock-device-A',allow=False));self.predict()
        self.assertFalse(any(x['kind']=='lookup_attempt' for x in self.s.log.records()))
    def test_scheduled_permission_effective_boundary(self):
        self.collect();self.s.apply(dict(operation='permit',time=13,app='source-app',device='mock-device-A',allow=False,effective_at=30));self.predict()
        self.assertEqual(audit(self.packet())['routes'],['GATE_BLOCKED'])
    def test_scheduled_changes_order_by_effective_time(self):
        self.collect();self.s.apply(dict(operation='permit',time=13,app='source-app',device='mock-device-A',allow=False,effective_at=30))
        self.s.apply(dict(operation='permit',time=14,app='source-app',device='mock-device-A',allow=True,effective_at=20));self.predict()
        self.assertEqual(audit(self.packet())['routes'],['GATE_BLOCKED'])
    def test_reset_purges_no_relink(self):
        self.collect();self.s.apply(dict(operation='reset',time=21,device='mock-device-A'));self.predict(epoch=1)
        self.assertFalse(self.s.s['events']);self.assertEqual(audit(self.packet())['routes'],['NO_INDIVIDUAL_HISTORY_READ_OBSERVED'])
    def test_stale_event_after_reset(self):
        self.s.apply(dict(operation='reset',time=1,device='mock-device-A'));self.assertEqual(self.collect()['status'],'STALE_EPOCH')
    def test_duplicate_mock_event_not_recounted(self):
        self.collect();self.assertEqual(self.s.apply(dict(operation='collect',time=13,event=self.event()))['status'],'DUPLICATE');self.assertEqual(len(self.s.s['events']),1)
    def test_other_device_cannot_read(self):
        self.collect();self.s.apply(dict(operation='permit',time=13,app='target-app',device='mock-device-B',allow=True));self.predict(device='mock-device-B')
        self.assertNotIn('local_same_device_source_history_consumed',audit(self.packet())['identified_claims'])
    def test_time_reversal(self):
        self.collect()
        with self.assertRaises(ValueError):self.s.apply(dict(operation='permit',time=1,app='target-app',device='mock-device-A',allow=True))
    def test_retroactive_permission_forbidden(self):
        self.collect()
        with self.assertRaises(ValueError):self.s.apply(dict(operation='permit',time=20,effective_at=1,app='target-app',device='mock-device-A',allow=True))
    def test_request_id_reuse(self):
        self.collect();self.predict()
        with self.assertRaises(ValueError):self.predict()
    def test_foreign_purpose(self):
        with self.assertRaises(ValueError):self.event(purpose='ads-personalization')
    def test_unknown_identifier_or_extra_fields(self):
        with self.assertRaises(ValueError):self.event(device='real-id-123')
        with self.assertRaises(ValueError):self.event(email='person@example.org')
    def test_request_context_injection(self):
        with self.assertRaises(ValueError):self.q(context=dict(country='US',model='phone',placement='production'))
    def test_missing_provenance_not_inferred(self):
        self.collect();self.predict();p=self.packet()
        for r in p['records']:
            if r['kind']=='feature_read':r['data']['provenance']=99999
        rechain(p['records']);self.assertEqual(audit(p)['status'],'UNIDENTIFIABLE')
    def test_no_actual_read_is_not_consumption(self):
        self.collect();self.predict();p=self.packet()
        for r in p['records']:
            if r['kind']=='feature_read':r['data']['actual_read']=False
        rechain(p['records']);self.assertEqual(audit(p)['status'],'UNIDENTIFIABLE')
    def test_future_feature_detected_even_with_valid_chain(self):
        self.collect();self.predict();p=self.packet()
        for r in p['records']:
            if r['kind']=='event_received':r['data']['available_at']=999
        rechain(p['records']);self.assertEqual(audit(p)['status'],'INVALID_EVIDENCE')
    def test_scope_forgery_detected(self):
        self.collect();self.predict();p=self.packet()
        for r in p['records']:
            if r['kind']=='history_read':r['data']['device']='mock-device-B'
        rechain(p['records']);self.assertEqual(audit(p)['status'],'INVALID_EVIDENCE')
    def test_tampered_chain(self):
        self.collect();self.predict();p=self.packet();p['records'][0]['data']['seed']=999
        self.assertEqual(audit(p)['status'],'INVALID_EVIDENCE')
    def test_truncated_run_unknown(self):
        self.collect();self.predict();p=self.packet();p['records'].pop()
        self.assertEqual(audit(p)['status'],'UNIDENTIFIABLE')
    def test_external_view_unknown(self):
        self.assertEqual(audit(dict(view='external_only',observations=[dict(score=.8)]))['status'],'UNIDENTIFIABLE')
    def test_hidden_truth_field_not_accepted(self):
        self.assertEqual(audit(dict(view='external_only',route='D1'))['status'],'INVALID_EVIDENCE')
    def test_no_read_does_not_identify_training_origin(self):
        self.s.s['route']='D0';self.s.flush();self.collect();self.predict();v=audit(self.packet())
        self.assertIn('training_origin_H0_vs_H3',v['not_identified'])
    def test_derived_return_never_existing_entity_match(self):
        v=assess_observable(dict(observation_level='match',match=dict(scope_attested=True,namespace='mock-provider',entity_granularity='person',result_type='derived')))
        self.assertNotIn('provider_maintained_status',v['claims'])
    def test_maintained_not_natural_person_truth(self):
        v=assess_observable(dict(observation_level='match',match=dict(scope_attested=True,namespace='mock-provider',entity_granularity='person',result_type='maintained',matchConfidence='8')))
        self.assertEqual(v['claims'],['provider_maintained_status']);self.assertIn('not independent person truth',v['limit'])
    def test_no_true_label_no_gain(self):
        self.assertEqual(assess_observable(dict(observation_level='increment'))['status'],'STOP_REAL_LABELS_NOT_AVAILABLE')
    def test_malformed_trace_fails_closed(self):
        self.assertEqual(audit(dict(view='complete_local_audit',records=[dict(bad=True)]))['status'],'INVALID_EVIDENCE')
    def test_revoked_bridge_dropped_before_target_log(self):
        self.collect();b=self.s.apply(dict(operation='bridge',time=20,device='mock-device-A'))
        self.s.apply(dict(operation='permit',time=21,app='source-app',device='mock-device-A',allow=False))
        q=self.q();q['context'].update(source_category=b['category'],bridge_receipt=b['bridge_receipt'])
        self.s.apply(dict(operation='predict',time=30,request=q));p=self.packet()
        req=next(x for x in p['records'] if x['kind']=='request_received')
        self.assertNotIn('source_category',req['data']['context']);self.assertEqual(audit(p)['routes'],['GATE_BLOCKED'])
    def test_expired_target_bridge_rejected(self):
        self.collect();b=self.s.apply(dict(operation='bridge',time=20,device='mock-device-A'))
        with self.assertRaises(ValueError):request(self.q(),b)
    def test_late_received_event_available_boundary(self):
        out=self.s.apply(dict(operation='collect',time=25,event=self.event(available_at=30)))
        self.assertEqual(out['status'],'RECEIVED');self.predict();self.assertEqual(audit(self.packet())['routes'],['SAME_DEVICE_HISTORY_READ'])
    def test_permission_granted_after_event_does_not_backdate(self):
        self.s.apply(dict(operation='permit',time=1,app='source-app',device='mock-device-A',allow=False))
        self.s.apply(dict(operation='permit',time=11,app='source-app',device='mock-device-A',allow=True))
        self.assertEqual(self.collect()['status'],'DENIED')
    def test_cross_install_source_provenance_retained(self):
        self.collect();self.predict(installation='mock-install-T2')
        v=audit(self.packet());self.assertEqual(v['routes'],['SAME_DEVICE_HISTORY_READ'])
        self.assertNotIn('natural_person',v['identified_claims'])
    def test_gate_blocks_even_when_event_cached(self):
        self.collect();self.predict()
        self.s.apply(dict(operation='permit',time=31,app='target-app',device='mock-device-A',allow=False))
        self.predict(request_id='mock-request-2',prediction_time=32)
        rows=self.s.log.records()
        self.assertFalse(any(x['kind']=='lookup_attempt' and x['data']['request_id']=='mock-request-2' for x in rows))
    def test_unknown_training_mapping_not_recovered(self):
        from mock76.auditor import hypothesis_verdict
        self.assertEqual(hypothesis_verdict('H3_shared',dict(claims=['local_same_device_source_history_consumed'])),'NOT_IDENTIFIED_AT_REQUESTED_HYPOTHESIS_LEVEL')

if __name__=='__main__':unittest.main()
