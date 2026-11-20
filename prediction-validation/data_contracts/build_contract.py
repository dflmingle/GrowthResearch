"""Write a closed, aggregate/opaque-row-only import contract. No raw identity fields."""
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent
def s(**kw):return dict(type='string',**kw)
def enum(*values):return dict(type='string',enum=list(values))
def dt():return s(format='date-time')
def obj(props,optional=()):return dict(type='object',properties=props,required=[k for k in props if k not in optional],additionalProperties=False)
def arr(item):return dict(type='array',items=item)
def key():return s(minLength=1,maxLength=128)
def nullable(v):return {'anyOf':[v,{'type':'null'}]}
money=s(pattern=r'^-?(0|[1-9][0-9]*)(\.[0-9]{1,12})?$')
bool_={'type':'boolean'}
num={'type':'number'}
unit=enum('single_app','owner_authorized_aggregate')
features=['context','history_ads','cross_app_history','d0_behavior','d0_revenue','proxy']

auth=obj(dict(owner=s(minLength=1),authorization_reference=s(minLength=1),
    approved_purposes=arr(enum('ltv_research','install_probability_research','cross_app_feature_research','conditional_auction_simulation')),
    valid_from=dt(),valid_until=dt(),app_scopes=arr(s(minLength=1)),
    cross_app_history_allowed=bool_,no_direct_identifiers=bool_,export_join_scope=enum('dataset_only'),
    source_data_synthetic=bool_))
manifest=obj(dict(dataset_id=key(),provenance=enum('synthetic','real_authorized'),
    authorization=auth,snapshot_at=dt(),label_as_of=dt(),arrival_grace_hours={'type':'integer','minimum':0,'maximum':720},
    iaa_complete_through_at=dt(),iap_complete_through_at=dt(),install_population_complete=bool_,
    revenue_basis=enum('publisher_net_iaa_and_verified_net_iap'),
    accepted_iaa_precision=arr(enum('exact','estimated','publisher_defined','undefined')),
    label_precision_scope=enum('exact_callback_revenue','estimated_callback_revenue'),
    refund_policy=enum('restate_original_purchase_window_as_of_snapshot'),
    horizon_definition=enum('elapsed_utc_half_open_7x24_28x24_hours'),
    currency=enum('USD'),experiment_id=key(),
    join_contracts=arr(obj(dict(join_contract_id=key(),owner_reference=s(minLength=1),
        allowed_purpose=enum('cross_app_feature_research'),valid_from=dt(),valid_until=dt(),
        scope=enum('owner_authorized_aggregate'),raw_ids_exported=bool_)))))

installs=obj(dict(sample_key=key(),app_scope=key(),install_at=dt(),available_at=dt(),received_at=dt(),
    country=s(pattern='^[A-Z]{2}$'),platform=enum('android','ios'),game_version=key(),ad_policy_version=key(),
    opportunity_key=nullable(key())))
opportunities=obj(dict(opportunity_key=key(),bid_at=dt(),served=bool_,outcome_complete=bool_,
    installed=nullable(bool_),outcome_available_at=nullable(dt()),
    cost_usd=nullable(money),logged_action_probability=nullable({'type':'number','exclusiveMinimum':0,'maximum':1}),
    logging_policy_id=key(),randomized_exploration=bool_))
feature=obj(dict(entity_type=enum('opportunity','install'),entity_key=key(),feature_name=key(),
    feature_group=enum(*features),value=num,event_at=dt(),source_max_available_at=dt(),
    computed_at=dt(),available_at=dt(),received_at=dt(),window_start_at=dt(),window_end_at=dt(),
    privacy_allowed=bool_,scope=unit,join_contract_id=nullable(key())))
revenue=obj(dict(record_key=key(),sample_key=key(),canonical_economic_key=key(),
    kind=enum('iaa','iap'),stage=enum('impression','paid','fulfilled','refund'),
    recognition_at=dt(),event_at=dt(),available_at=dt(),received_at=dt(),
    amount=money,currency=s(pattern='^[A-Z]{3}$'),precision=enum('exact','estimated','publisher_defined','undefined'),
    amount_basis=enum('publisher_net_iaa','verified_net_iap','catalog_metadata','proxy_value','predicted_value'),
    purchase_verified=bool_,source_system=key(),original_purchase_key=nullable(key())))
fx=obj(dict(currency=s(pattern='^[A-Z]{3}$'),rate_date=s(format='date'),usd_per_unit=s(pattern=r'^(0|[1-9][0-9]*)(\.[0-9]{1,12})?$'),
    available_at=dt(),source_reference=s(minLength=1)))
bundle=obj(dict(manifest=manifest,installs=arr(installs),opportunities=arr(opportunities),
    features=arr(feature),revenues=arr(revenue),fx_rates=arr(fx)))
bundle.update({'$schema':'https://json-schema.org/draft/2020-12/schema',
    '$id':'urn:growth-research:prediction-validation:bundle:v1',
    'title':'Independent LTV research export v1; schema validity is not authorization verification'})
(HERE/'bundle.schema.json').write_text(json.dumps(bundle,indent=2)+'\n','utf-8')
print('Closed bundle schema written; no raw GAID/email/IP/user account columns.')
