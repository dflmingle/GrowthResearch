"""Small deterministic accounting fixture, NOT a predictive population generator."""
from datetime import datetime, timedelta, timezone
from copy import deepcopy

START=datetime(2026,1,1,tzinfo=timezone.utc)
def ts(hours=0):return (START+timedelta(hours=hours)).isoformat().replace('+00:00','Z')

def fixture():
    manifest=dict(dataset_id='SYNTHETIC_ACCOUNTING_FIXTURE',provenance='synthetic',
        authorization=dict(owner='Local synthetic research author',authorization_reference='SYNTHETIC_ONLY_NO_OPERATOR_DATA',
            approved_purposes=['ltv_research','install_probability_research','cross_app_feature_research','conditional_auction_simulation'],
            valid_from=ts(-1000),valid_until=ts(20000),app_scopes=['SYNTHETIC_GAME'],cross_app_history_allowed=True,
            no_direct_identifiers=True,export_join_scope='dataset_only',source_data_synthetic=True),
        snapshot_at=ts(24*40),label_as_of=ts(24*35),arrival_grace_hours=72,
        iaa_complete_through_at=ts(24*32),iap_complete_through_at=ts(24*32),install_population_complete=True,
        revenue_basis='publisher_net_iaa_and_verified_net_iap',accepted_iaa_precision=['exact'],
        label_precision_scope='exact_callback_revenue',refund_policy='restate_original_purchase_window_as_of_snapshot',
        horizon_definition='elapsed_utc_half_open_7x24_28x24_hours',currency='USD',experiment_id='SYNTHETIC_SMOKE_V1',
        join_contracts=[dict(join_contract_id='SYNTHETIC_JOIN',owner_reference='SIMULATED_OWNER_CONTRACT_NOT_REAL_AUTHORIZATION',
            allowed_purpose='cross_app_feature_research',valid_from=ts(-1000),valid_until=ts(10000),
            scope='owner_authorized_aggregate',raw_ids_exported=False)])
    installs=[];opps=[];features=[];revenues=[]
    for j in range(3):
        key=f'SYNTHETIC_ROW_{j}';opp=f'SYNTHETIC_OPPORTUNITY_{j}';offset=24*j
        installs.append(dict(sample_key=key,app_scope='SYNTHETIC_GAME',install_at=ts(offset),available_at=ts(offset+1),received_at=ts(offset+.5),
            country=['US','GB','JP'][j],platform='android',game_version='SYNTHETIC_V1',ad_policy_version='SYNTHETIC_POLICY_A',opportunity_key=opp))
        opps.append(dict(opportunity_key=opp,bid_at=ts(offset-1),served=True,outcome_complete=True,installed=True,
            outcome_available_at=ts(offset+2),cost_usd='0.05',logged_action_probability=None,logging_policy_id='SYNTHETIC_NONRANDOM_POLICY',randomized_exploration=False))
        for group,name in [('context','device_tier'),('history_ads','past_ad_interactions_7d'),('cross_app_history','owner_cross_app_past_revenue_28d')]:
            features.append(dict(entity_type='opportunity',entity_key=opp,feature_name=name,feature_group=group,value=float(j+1),
                event_at=ts(offset-48),source_max_available_at=ts(offset-47),computed_at=ts(offset-46),available_at=ts(offset-45),received_at=ts(offset-47.5),
                window_start_at=ts(offset-7*24),window_end_at=ts(offset-48),privacy_allowed=True,
                scope='owner_authorized_aggregate' if group=='cross_app_history' else 'single_app',join_contract_id='SYNTHETIC_JOIN' if group=='cross_app_history' else None))
        for group,name in [('d0_behavior','d0_active_minutes'),('d0_revenue','d0_iaa_usd'),('proxy','adworth_style_proxy')]:
            features.append(dict(entity_type='install',entity_key=key,feature_name=name,feature_group=group,value=(.1 if j<2 else 0.) if group=='d0_revenue' else float(j+1),
                event_at=ts(offset+23),source_max_available_at=ts(offset+24),computed_at=ts(offset+24),available_at=ts(offset+24),received_at=ts(offset+23.5),
                window_start_at=ts(offset),window_end_at=ts(offset+24),privacy_allowed=True,scope='single_app',join_contract_id=None))
        context=deepcopy(next(f for f in features if f['entity_key']==opp and f['feature_group']=='context'))
        context.update(entity_type='install',entity_key=key)
        features.append(context)
        def revenue(suffix,hours,amount,kind='iaa',stage='impression',canonical=None,original=None,basis=None):
            return dict(record_key=key+'_'+suffix,sample_key=key,canonical_economic_key=key+'_'+(canonical or suffix),
                kind=kind,stage=stage,recognition_at=ts(offset+hours),event_at=ts(offset+hours),available_at=ts(offset+hours+1),received_at=ts(offset+hours+.5),
                amount=amount,currency='USD',precision='exact',amount_basis=basis or ('publisher_net_iaa' if kind=='iaa' else 'verified_net_iap'),
                purchase_verified=kind=='iap',source_system='SYNTHETIC_MEDIATION' if kind=='iaa' else 'SYNTHETIC_STORE',original_purchase_key=original)
        # Exact half-open boundary cases: +24h excluded from D0; +7d excluded
        # from D7; +28d excluded from D28. The zero-revenue installer is retained.
        if j<2:
            first=revenue('ad0',1,'0.10');revenues.append(first)
            duplicate=deepcopy(first);duplicate['record_key']+='_SDK_COPY';duplicate['source_system']='SYNTHETIC_MMP_COPY';revenues.append(duplicate)
            revenues += [revenue('ad1',24,'0.20'),revenue('ad7',7*24,'0.30'),revenue('ad27',27*24,'0.40'),revenue('ad28',28*24,'1000.00')]
            purchase=revenue('paid',2,'4.00','iap','paid',canonical='transaction');revenues.append(purchase)
            fulfilled=deepcopy(purchase);fulfilled.update(record_key=key+'_fulfilled',stage='fulfilled',event_at=ts(offset+3),received_at=ts(offset+3.5),available_at=ts(offset+4));revenues.append(fulfilled)
            refund=revenue('refund',2,'-1.00','iap','refund',original=key+'_transaction')
            refund.update(event_at=ts(offset+10*24),received_at=ts(offset+10*24+.5),available_at=ts(offset+10*24+1));revenues.append(refund)
            revenues.append(revenue('proxy',2,'9999.00',basis='proxy_value'))
    opps.append(dict(opportunity_key='SYNTHETIC_NONINSTALL',bid_at=ts(12),served=True,outcome_complete=True,installed=False,
        outcome_available_at=ts(24*8),cost_usd='0.05',logged_action_probability=None,logging_policy_id='SYNTHETIC_NONRANDOM_POLICY',randomized_exploration=False))
    return dict(manifest=manifest,installs=installs,opportunities=opps,features=features,revenues=revenues,fx_rates=[])
