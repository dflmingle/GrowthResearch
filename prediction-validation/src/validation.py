"""Offline contract, as-of feature and economic-ledger checks; no model training.

Passing this module is NOT a legal authorization decision or causal identification.
Real datasets must undergo an independent owner/authorization/security review.
"""
from pathlib import Path
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from collections import Counter, defaultdict
import json, math
from jsonschema import Draft202012Validator, FormatChecker

BASE=Path(__file__).resolve().parents[1]
SCHEMA=json.loads((BASE/'data_contracts/bundle.schema.json').read_text('utf-8'))
FEATURE_REGISTRY=json.loads((BASE/'data_contracts/feature_registry.json').read_text('utf-8'))
GROUPS={r['feature_name']:r['feature_group'] for r in FEATURE_REGISTRY}
MODEL_GROUPS={
    'M0':{'context'},'M1':{'context','history_ads'},'M2':{'context','history_ads','cross_app_history'},
    'M3':{'context','d0_behavior'},'M4':{'context','d0_behavior','d0_revenue'},
    'M5':{'context','d0_behavior','d0_revenue','proxy'},
}

def moment(v):
    t=datetime.fromisoformat(v.replace('Z','+00:00'))
    if t.utcoffset()!=timedelta(0):raise ValueError('UTC timestamps with explicit offset required')
    return t

def schema_errors(bundle):
    # Never include offending field values or identifiers in diagnostics.
    return [dict(code='SCHEMA',path='/'.join(map(str,e.absolute_path)),rule=e.validator)
        for e in Draft202012Validator(SCHEMA,format_checker=FormatChecker()).iter_errors(bundle)]

def feature_eligibility(feature, cutoff, model):
    reasons=[]
    if feature['feature_group'] not in MODEL_GROUPS[model]:reasons.append('GROUP_NOT_IN_MODEL')
    if not feature['privacy_allowed']:reasons.append('PRIVACY_GATE')
    # Four clocks: the source must already exist, aggregation must be finished,
    # and the serving-side feature must already have become available.
    if any(moment(feature[k])>cutoff for k in ['event_at','source_max_available_at','computed_at','available_at','window_end_at']):
        reasons.append('AFTER_PREDICTION_TIME')
    if moment(feature['window_start_at'])>moment(feature['window_end_at']):reasons.append('INVALID_WINDOW')
    return not reasons,reasons

def canonicalize(bundle):
    """Canonical economic keys must be assigned by owner before export.

    No value/amount-based fuzzy matching. Paid and fulfilled are two reports of
    one economic transaction; their price/currency must agree before combining.
    """
    m=bundle['manifest']; groups=defaultdict(list); excluded=Counter(); errors=[]
    for r in bundle['revenues']:
        if moment(r['available_at'])>moment(m['label_as_of']) or moment(r['received_at'])>moment(m['label_as_of']):
            excluded['arrived_after_label_snapshot']+=1;continue
        if r['amount_basis'] in ('catalog_metadata','proxy_value','predicted_value'):
            excluded['non_revenue_value']+=1;continue
        if r['kind']=='iaa' and (r['stage']!='impression' or r['amount_basis']!='publisher_net_iaa'):
            errors.append('IAA_SEMANTICS');continue
        if r['kind']=='iaa' and r['precision'] not in m['accepted_iaa_precision']:
            errors.append('IAA_PRECISION_NOT_ACCEPTED');continue
        if r['kind']=='iap' and (r['stage'] not in ('paid','fulfilled','refund') or not r['purchase_verified'] or r['amount_basis']!='verified_net_iap'):
            errors.append('IAP_NOT_VERIFIED_NET_REVENUE');continue
        if r['stage']=='refund':
            if Decimal(r['amount'])>=0 or not r['original_purchase_key']:errors.append('REFUND_LINK_OR_SIGN');continue
        elif Decimal(r['amount'])<0:errors.append('NEGATIVE_NON_REFUND');continue
        groups[(r['kind'],r['canonical_economic_key'])].append(r)
    ledger=[]; duplicates=0
    for key, rs in groups.items():
        fingerprints={(r['sample_key'],r['amount'],r['currency'],r['recognition_at'],
            'refund' if r['stage']=='refund' else 'revenue',r['original_purchase_key'],r['amount_basis'],r['precision']) for r in rs}
        if len(fingerprints)!=1:errors.append('CANONICAL_KEY_CONFLICT');continue
        if len({r['event_at'] for r in rs if r['stage']=='impression'})>1:errors.append('IMPRESSION_TIME_CONFLICT');continue
        chosen=next((r for r in rs if r['stage']=='paid'),rs[0])
        duplicates+=len(rs)-1
        ledger.append(chosen)
    purchases={(r['sample_key'],r['canonical_economic_key']):r for r in ledger if r['kind']=='iap' and r['stage']!='refund'}
    for r in ledger:
        if r['stage']=='refund':
            orig=purchases.get((r['sample_key'],r['original_purchase_key']))
            if orig is None:errors.append('REFUND_WITHOUT_PURCHASE')
            elif r['recognition_at']!=orig['recognition_at'] or r['currency']!=orig['currency']:
                errors.append('REFUND_RESTATEMENT_MISMATCH')
    return ledger,dict(excluded),duplicates,errors

def fx_value(r,bundle):
    if r['currency']=='USD':return Decimal(r['amount'])
    date=moment(r['recognition_at']).date().isoformat()
    rates=[f for f in bundle['fx_rates'] if f['currency']==r['currency'] and f['rate_date']==date
        and moment(f['available_at'])<=moment(bundle['manifest']['label_as_of'])]
    if len(rates)!=1 or Decimal(rates[0]['usd_per_unit'])<=0:raise ValueError('MISSING_OR_AMBIGUOUS_FX')
    return Decimal(r['amount'])*Decimal(rates[0]['usd_per_unit'])

def validate(bundle):
    errors=schema_errors(bundle)
    if errors:return dict(passed=False,errors=errors,real_training_allowed=False)
    m=bundle['manifest']; auth=m['authorization']
    err=[]
    for table in ['installs','opportunities','features','revenues','fx_rates']:
        for r in bundle[table]:
            for k,v in r.items():
                if k.endswith('_at') and v is not None:
                    try:moment(v)
                    except (ValueError,TypeError):err.append('TIMESTAMP_NOT_UTC')
    times=[m[k] for k in ['snapshot_at','label_as_of','iaa_complete_through_at','iap_complete_through_at']]
    times += [auth['valid_from'],auth['valid_until']]
    times += [j[k] for j in m['join_contracts'] for k in ['valid_from','valid_until']]
    for v in times:
        try:moment(v)
        except (ValueError,TypeError):err.append('TIMESTAMP_NOT_UTC')
    if err:return dict(passed=False,errors=sorted(set(err)),real_training_allowed=False)
    asof=moment(m['label_as_of']); snap=moment(m['snapshot_at'])
    if asof>snap:err.append('LABEL_SNAPSHOT_AFTER_EXPORT')
    if not auth['no_direct_identifiers']:err.append('IDENTIFIER_POLICY')
    if m['provenance']=='synthetic' and not auth['source_data_synthetic']:err.append('SYNTHETIC_PROVENANCE_MISMATCH')
    if m['provenance']=='real_authorized' and auth['source_data_synthetic']:err.append('REAL_PROVENANCE_MISMATCH')
    if not moment(auth['valid_from'])<=snap<=moment(auth['valid_until']):err.append('AUTHORIZATION_TIME_SCOPE')
    if 'ltv_research' not in auth['approved_purposes']:err.append('LTV_PURPOSE_NOT_ALLOWED')
    if not m['install_population_complete']:err.append('INSTALL_DENOMINATOR_INCOMPLETE')
    if not m['accepted_iaa_precision']:err.append('NO_IAA_PRECISION_POLICY')
    if m['label_precision_scope']=='exact_callback_revenue' and set(m['accepted_iaa_precision'])!={'exact'}:
        err.append('EXACT_LABEL_MIXED_PRECISION')
    inst={r['sample_key']:r for r in bundle['installs']}; opp={r['opportunity_key']:r for r in bundle['opportunities']}
    if len(inst)!=len(bundle['installs']):err.append('DUPLICATE_INSTALL_KEY')
    if not inst:err.append('EMPTY_INSTALL_POPULATION')
    if len(opp)!=len(bundle['opportunities']):err.append('DUPLICATE_OPPORTUNITY_KEY')
    if len({r['record_key'] for r in bundle['revenues']})!=len(bundle['revenues']):err.append('DUPLICATE_REPORT_KEY')
    if len({(f['entity_type'],f['entity_key'],f['feature_name']) for f in bundle['features']})!=len(bundle['features']):err.append('DUPLICATE_FEATURE_SNAPSHOT')
    for table in ['revenues','features','installs']:
        for r in bundle[table]:
            for k,v in r.items():
                if k.endswith('_at'):
                    try:moment(v)
                    except (ValueError,TypeError):err.append('TIMESTAMP_NOT_UTC')
    # Schema and UTC checks must pass before arithmetic.
    if 'TIMESTAMP_NOT_UTC' in err:return dict(passed=False,errors=sorted(set(err)),real_training_allowed=False)
    for i in inst.values():
        t=moment(i['install_at']); end=t+timedelta(days=28)
        if i['app_scope'] not in auth['app_scopes']:err.append('APP_OUTSIDE_AUTHORIZATION')
        if not t<=moment(i['received_at'])<=moment(i['available_at'])<=snap:err.append('INSTALL_TIME_ORDER')
        if asof<end+timedelta(hours=m['arrival_grace_hours']):err.append('IMMATURE_D28')
        if any(moment(m[k])<end for k in ['iaa_complete_through_at','iap_complete_through_at']):err.append('REVENUE_WATERMARK_INCOMPLETE')
        if i['opportunity_key'] is not None:
            o=opp.get(i['opportunity_key'])
            if not o or o['installed'] is not True or not o['served'] or moment(o['bid_at'])>t:err.append('INSTALL_OPPORTUNITY_LINK')
    used_opportunities=[i['opportunity_key'] for i in inst.values() if i['opportunity_key'] is not None]
    if len(set(used_opportunities))!=len(used_opportunities):err.append('MULTIPLE_INSTALLS_PER_OPPORTUNITY')
    for o in opp.values():
        if not o['served'] and o['installed'] is not None:err.append('UNSERVED_COUNTERFACTUAL_OUTCOME')
        if o['outcome_complete'] and (o['outcome_available_at'] is None or o['installed'] is None):err.append('INCOMPLETE_INSTALL_LABEL')
        if o['outcome_available_at'] and moment(o['outcome_available_at'])>asof:err.append('INSTALL_OUTCOME_NOT_MATURE')
        if o['cost_usd'] is not None and Decimal(o['cost_usd'])<0:err.append('NEGATIVE_COST')
        if o['outcome_available_at'] and moment(o['outcome_available_at'])<moment(o['bid_at']):err.append('OUTCOME_BEFORE_BID')
    joins={j['join_contract_id']:j for j in m['join_contracts']}
    for f in bundle['features']:
        if not math.isfinite(f['value']):err.append('NONFINITE_FEATURE')
        if GROUPS.get(f['feature_name'])!=f['feature_group']:err.append('UNREGISTERED_FEATURE_OR_GROUP')
        if f['entity_key'] not in (inst if f['entity_type']=='install' else opp):err.append('ORPHAN_FEATURE')
        if not moment(f['event_at'])<=moment(f['received_at'])<=moment(f['source_max_available_at'])<=moment(f['computed_at'])<=moment(f['available_at']):
            err.append('FEATURE_TIME_ORDER')
        if moment(f['window_start_at'])>moment(f['window_end_at']) or moment(f['window_end_at'])>moment(f['computed_at']):err.append('FEATURE_WINDOW_ORDER')
        if f['feature_group']=='cross_app_history':
            j=joins.get(f['join_contract_id'])
            if not (auth['cross_app_history_allowed'] and 'cross_app_feature_research' in auth['approved_purposes']
                and f['scope']=='owner_authorized_aggregate' and j and not j['raw_ids_exported']
                and moment(j['valid_from'])<=moment(f['available_at'])<=moment(j['valid_until'])):
                err.append('CROSS_APP_JOIN_NOT_AUTHORIZED')
        elif f['scope']!='single_app' or f['join_contract_id'] is not None:err.append('FEATURE_SCOPE_MISMATCH')
    for r in bundle['revenues']:
        if r['sample_key'] not in inst:err.append('ORPHAN_REVENUE');continue
        if not moment(r['event_at'])<=moment(r['received_at'])<=moment(r['available_at']):err.append('REVENUE_TIME_ORDER')
        if moment(r['recognition_at'])>moment(r['event_at']):err.append('RECOGNITION_AFTER_EVENT')
        if moment(r['recognition_at'])<moment(inst[r['sample_key']]['install_at']):err.append('REVENUE_BEFORE_INSTALL')
    ledger,excluded,duplicates,ledger_errors=canonicalize(bundle);err.extend(ledger_errors)
    for r in ledger:
        try:fx_value(r,bundle)
        except ValueError as e:err.append(str(e))
    # Report only aggregate errors; never log raw identity or user feature values.
    return dict(passed=not err,errors=sorted(set(err)),counts=dict(installs=len(inst),opportunities=len(opp),
        revenue_reports=len(bundle['revenues']),canonical_revenue_events=len(ledger),duplicate_economic_reports=duplicates),
        excluded=excluded,provenance=m['provenance'],
        real_training_allowed=False,real_gate_reason='No real training entry point: separate owner-reviewed authorization, maturity and leakage audit required',
        install_probability_scope='observed served opportunities only; unserved outcomes must be unknown' if opp else 'not identifiable: installers only',
        causal_roas_identified=False)

def build_labels(bundle):
    result=validate(bundle)
    if not result['passed']:raise ValueError('DATA_QUALITY_GATE_FAILED: '+str(result['errors']))
    ledger,_,_,_=canonicalize(bundle);by=defaultdict(list)
    for r in ledger:by[r['sample_key']].append(r)
    labels=[]
    for i in bundle['installs']:
        start=moment(i['install_at']);record={'sample_key':i['sample_key'],'provenance':bundle['manifest']['provenance']}
        for days in [1,7,28]:
            horizon='d0' if days==1 else f'd{days}'
            for kind in ['iaa','iap']:
                amount=sum((fx_value(r,bundle) for r in by[i['sample_key']] if r['kind']==kind and start<=moment(r['recognition_at'])<start+timedelta(days=days)),Decimal(0))
                record[f'{horizon}_{kind}_usd']=str(amount)
            record[f'{horizon}_total_usd']=str(Decimal(record[f'{horizon}_iaa_usd'])+Decimal(record[f'{horizon}_iap_usd']))
        record['d1_d28_remaining_usd']=str(Decimal(record['d28_total_usd'])-Decimal(record['d0_total_usd']))
        labels.append(record)
    return labels,result

def feature_audit(bundle):
    """Coverage only; not training, not inference or feature efficacy evidence."""
    if not validate(bundle)['passed']:raise ValueError('DATA_QUALITY_GATE_FAILED')
    installs={i['sample_key']:i for i in bundle['installs']};opps={o['opportunity_key']:o for o in bundle['opportunities']}
    summary={m:Counter() for m in MODEL_GROUPS}
    for f in bundle['features']:
        for model in MODEL_GROUPS:
            if model in ('M0','M1','M2'):
                if f['entity_type']!='opportunity':continue
                cutoff=moment(opps[f['entity_key']]['bid_at'])
            else:
                if f['entity_type']!='install':continue
                cutoff=moment(installs[f['entity_key']]['install_at'])+timedelta(days=1)
            eligible,reasons=feature_eligibility(f,cutoff,model)
            summary[model]['eligible' if eligible else 'excluded']+=1
            summary[model].update(reasons)
    return {k:dict(v) for k,v in summary.items()}
