"""Independent evidence-only checker. Does not import service or inspect private state."""
import argparse
from .io import read,write,verify,digest
from .safety import install

def result(status,reason,**extra):
    return dict(status=status,reason=reason,identified_claims=[],not_identified=['natural_person','household','training_origin_H0_vs_H3','Axon_Vector_model_consumption','independent_value_gain'],**extra)

def _audit(packet):
    if set(packet)-{'view','records','observations','capabilities'}:return result('INVALID_EVIDENCE','UNEXPECTED_PACKET_FIELDS')
    # External outputs alone have no trusted provenance.No route guessing from score/creative.
    if packet.get('view')!='complete_local_audit':return result('UNIDENTIFIABLE','OUTPUT_OR_REDACTED_VIEW_INSUFFICIENT')
    rows=packet.get('records',[])
    if not rows or not verify(rows):return result('INVALID_EVIDENCE','HASH_CHAIN_OR_SEQUENCE_INVALID')
    if rows[0]['kind']!='run_open' or rows[-1]['kind']!='run_closed' or not rows[-1]['data'].get('complete'):
        return result('UNIDENTIFIABLE','INCOMPLETE_RUN')
    if any(b['time']<a['time'] for a,b in zip(rows,rows[1:])):return result('INVALID_EVIDENCE','TIME_REVERSAL')
    if rows[0]['data'].get('environment')!='offline-mock':return result('UNIDENTIFIABLE','NO_REAL_PLATFORM_ATTESTATION')
    if any(x['kind']=='command_failed' for x in rows):return result('INVALID_EVIDENCE','FAILED_COMMAND_PRESENT')
    seq={x['seq']:x for x in rows};events={x['seq']:x for x in rows if x['kind']=='event_received'}
    permissions=[x for x in rows if x['kind']=='permission_changed']
    def permitted(app,device,at,before):
        p=[x for x in permissions if x['seq']<before and x['data']['app']==app and x['data']['device']==device and x['data']['effective_at']<=at]
        return bool(p and max(p,key=lambda x:(x['data']['effective_at'],x['data']['version']))['data']['allow'])
    def active_epoch(device,before):
        resets=[x for x in rows if x['seq']<before and x['kind']=='scope_reset' and x['data']['device']==device]
        return resets[-1]['data']['epoch'] if resets else 0
    for e in events.values():
        d=e['data']
        if not (0<=d['event_time']<=d['received_at']==e['time']<=d['available_at']):return result('INVALID_EVIDENCE','EVENT_TIME_INVALID')
        if not permitted('source-app',d['device'],d['event_time'],e['seq']) or not permitted('source-app',d['device'],e['time'],e['seq']):return result('INVALID_EVIDENCE','UNAUTHORIZED_COLLECTION')
        if d['epoch']!=active_epoch(d['device'],e['seq']):return result('INVALID_EVIDENCE','STALE_COLLECTED_SCOPE')
    requests={x['data']['request_id']:x for x in rows if x['kind']=='request_received'}
    if len(requests)!=rows[-1]['data']['requests']:return result('INVALID_EVIDENCE','REQUEST_COUNT_MISMATCH')
    details=[];routes=set();supported=[]
    for rid,req in requests.items():
        q=req['data'];device=q['device'];t=q['prediction_time']
        gates=[x for x in rows if x['kind']=='use_gate' and x['data']['request_id']==rid]
        decisions=[x for x in rows if x['kind']=='decision' and x['data']['request_id']==rid]
        closes=[x for x in rows if x['kind']=='request_closed' and x['data']['request_id']==rid]
        if len(gates)!=1 or len(decisions)!=1 or len(closes)!=1 or not closes[0]['data'].get('feature_log_complete'):
            return result('UNIDENTIFIABLE','REQUEST_PROVENANCE_INCOMPLETE')
        gate,decision,close=gates[0],decisions[0],closes[0]
        expected=permitted('source-app',device,t,gate['seq']) and permitted('target-app',device,t,gate['seq'])
        if gate['data']['allow']!=expected:return result('INVALID_EVIDENCE','GATE_MISMATCH')
        if not(req['seq']<gate['seq']<decision['seq']<close['seq']) or req['time']!=t or decision['time']!=t:return result('INVALID_EVIDENCE','DECISION_ORDER_INVALID')
        if q['epoch']!=active_epoch(device,req['seq']):return result('INVALID_EVIDENCE','STALE_REQUEST_SCOPE')
        lookups=[x for x in rows if x['kind']=='lookup_attempt' and x['data']['request_id']==rid]
        histories=[x for x in rows if x['kind']=='history_read' and x['data']['request_id']==rid]
        features=[x for x in rows if x['kind']=='feature_read' and x['data']['request_id']==rid]
        if not expected and (lookups or histories or features):return result('INVALID_EVIDENCE','DENIED_PURPOSE_USED_HISTORY')
        if set(decision['data']['feature_receipts'])!={x['seq'] for x in features}:return result('UNIDENTIFIABLE','FEATURE_DECISION_LINK_MISSING')
        if histories and not features:return result('UNIDENTIFIABLE','READ_WITHOUT_CONSUMPTION_TRACE')
        if close['data']['decision_receipt']!=decision['seq'] or decision['data']['request_receipt']!=req['seq'] or decision['data']['gate_receipt']!=gate['seq']:return result('INVALID_EVIDENCE','DECISION_RECEIPT_MISMATCH')
        families=set()
        for f in features:
            d=f['data'];p=seq.get(d.get('provenance'))
            if not d.get('actual_read') or not d.get('nonnull') or not p:return result('UNIDENTIFIABLE','NO_ACTUAL_NON_NULL_READ')
            if d['model_version']!=decision['data']['model_version'] or d['materialized_at']>t:return result('INVALID_EVIDENCE','MODEL_OR_AVAILABILITY_MISMATCH')
            if not (gate['seq']<f['seq']<decision['seq'] and p['seq']<f['seq']):return result('INVALID_EVIDENCE','READ_ORDER_INVALID')
            family=d['family'];families.add(family)
            if family=='cross-app-device-history':
                if p['kind']!='history_read' or p['data']['request_id']!=rid or p['data']['device']!=device or p['data']['scope']!='same-device':return result('INVALID_EVIDENCE','SAME_DEVICE_ROUTE_INVALID')
                if not lookups or any(x['seq']>=p['seq'] for x in lookups):return result('UNIDENTIFIABLE','LOOKUP_PROVENANCE_MISSING')
            elif family=='current-context':
                if p['kind']!='context_bridge' or p['data']['device']!=device:return result('INVALID_EVIDENCE','CONTEXT_BRIDGE_INVALID')
                if q['context'].get('bridge_receipt')!=p['seq'] or q['context'].get('source_category')!=d['value']:return result('INVALID_EVIDENCE','REQUEST_BRIDGE_MISMATCH')
            else:return result('UNIDENTIFIABLE','UNKNOWN_FEATURE_FAMILY')
            e=events.get(p['data'].get('event_receipt'))
            if not e:return result('UNIDENTIFIABLE','SOURCE_RECEIPT_MISSING')
            ed=e['data']
            if ed['device']!=device or ed['source_app']!='source-app' or ed['epoch']!=active_epoch(device,f['seq']) or ed['purpose']!=q['purpose']:return result('INVALID_EVIDENCE','SOURCE_SCOPE_MISMATCH')
            if ed['available_at']>p['time'] or p['time']>t or ed['epoch']!=active_epoch(device,p['seq']):return result('INVALID_EVIDENCE','PROVENANCE_TIME_OR_SCOPE_INVALID')
            if not permitted('source-app',device,p['time'],p['seq']) or not permitted('target-app',device,p['time'],p['seq']):return result('INVALID_EVIDENCE','UNAUTHORIZED_PROVENANCE_READ')
            if ed['available_at']>t or ed['received_at']>t or ed['event_time']>t or ed['category']!=d['value']:return result('INVALID_EVIDENCE','FUTURE_OR_WRONG_HISTORY')
        if 'source_category' in q['context'] and expected and 'current-context' not in families:return result('UNIDENTIFIABLE','UNEXPLAINED_CONTEXT_CHANNEL')
        if families=={'cross-app-device-history'}:route='SAME_DEVICE_HISTORY_READ';supported.append('local_same_device_source_history_consumed')
        elif families=={'current-context'}:route='CONTEXT_LEAKAGE';supported.append('local_source_to_current_context_bridge')
        elif families:route='MULTIPLE_CHANNELS'
        elif not expected:route='GATE_BLOCKED'
        else:route='NO_INDIVIDUAL_HISTORY_READ_OBSERVED'
        routes.add(route);details.append(dict(request_id=rid,route=route,decision_seq=decision['seq'],feature_families=sorted(families),response=decision['data']['response']))
    out=result('IDENTIFIED_LOCAL_CHAIN','COMPLETE_INSTRUMENTED_LOCAL_TRACE',scope='local_fixture_run_only',routes=sorted(routes),requests=details)
    out['identified_claims']=sorted(set(supported));out['complete_local_no_read']=not bool(supported)
    out['caveat']='Local producer instrumentation is trusted for this fixture;hash chains are not signatures and do not prove production truth. No architecture-wide absence or value gain inferred.'
    return out

def audit(packet):
    try:return _audit(packet)
    except (KeyError,TypeError,ValueError,IndexError):return result('INVALID_EVIDENCE','MALFORMED_OR_UNSUPPORTED_SCHEMA')

def assess_observable(packet):
    """Matrix adapter uses available evidence,never hypothesis/row ID or route truth."""
    level=packet['observation_level'];base=audit(packet.get('audit_packet',dict(view='external_only')))
    if level in ['creative','frequency','advertiser_category']:
        return dict(status='UNIDENTIFIABLE',claims=[],limit='Response cannot identify history route,person or model benefit')
    if level=='audience':
        a=packet.get('audience',{})
        return dict(status='BOUNDED_AUDIENCE_STATE' if a.get('scope_attested') else 'UNIDENTIFIABLE',claims=['recipient_test_audience_state'] if a.get('scope_attested') else [],limit='Audience is not actual value-feature use')
    if level=='match':
        m=packet.get('match',{})
        if not m.get('scope_attested') or not m.get('namespace') or not m.get('entity_granularity'):return dict(status='UNIDENTIFIABLE',claims=[],limit='No authorized scoped match state')
        typ=m.get('result_type');claims=['provider_maintained_status'] if typ=='maintained' else []
        return dict(status='BOUNDED_PROVIDER_STATUS',claims=claims,result_type=typ,limit='Derived is not existing match;maintained not independent person truth;confidence not probability')
    if level in ['feature','score']:
        if base['status']!='IDENTIFIED_LOCAL_CHAIN':return dict(status='UNIDENTIFIABLE',claims=[],limit='Actual-read lineage missing')
        return dict(status='BOUNDED_LOCAL_CHAIN',claims=base['identified_claims'],limit='Local chain only;no natural person,vendor consumption,training origin or benefit',routes=base['routes'])
    if level=='increment':return dict(status='STOP_REAL_LABELS_NOT_AVAILABLE',claims=[],limit='No real mature values or equal-budget independent effect evidence')
    return dict(status='UNIDENTIFIABLE',claims=[],limit='Unsupported observation')

def hypothesis_verdict(hypothesis,observation_verdict):
    """Hypothesis is the question,not a supplied mechanism truth label."""
    if hypothesis=='H1' and 'local_same_device_source_history_consumed' in observation_verdict.get('claims',[]):
        return 'LOCAL_SAME_DEVICE_CHAIN_ONLY'
    return 'NOT_IDENTIFIED_AT_REQUESTED_HYPOTHESIS_LEVEL'

def main():
    install();p=argparse.ArgumentParser();p.add_argument('--input',required=True);p.add_argument('--output',required=True);p.add_argument('--matrix-view',action='store_true');a=p.parse_args()
    write(a.output,assess_observable(read(a.input)) if a.matrix_view else audit(read(a.input)))
if __name__=='__main__':main()
