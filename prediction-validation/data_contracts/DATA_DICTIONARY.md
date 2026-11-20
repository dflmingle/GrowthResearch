# 数据字典：bundle v1

由实际JSON Schema生成；语义、授权和时间规则见[接入规范](README.md)。字段类型不是已有真实样本。

## bundle

| 字段 | 类型 | 必需 |
|---|---|---|
| manifest | object | 是 |
| installs | array of object | 是 |
| opportunities | array of object | 是 |
| features | array of object | 是 |
| revenues | array of object | 是 |
| fx_rates | array of object | 是 |

## bundle.manifest

| 字段 | 类型 | 必需 |
|---|---|---|
| dataset_id | string | 是 |
| provenance | string enum: synthetic, real_authorized | 是 |
| authorization | object | 是 |
| snapshot_at | string (date-time) | 是 |
| label_as_of | string (date-time) | 是 |
| arrival_grace_hours | integer | 是 |
| iaa_complete_through_at | string (date-time) | 是 |
| iap_complete_through_at | string (date-time) | 是 |
| install_population_complete | boolean | 是 |
| revenue_basis | string enum: publisher_net_iaa_and_verified_net_iap | 是 |
| accepted_iaa_precision | array of string enum: exact, estimated, publisher_defined, undefined | 是 |
| label_precision_scope | string enum: exact_callback_revenue, estimated_callback_revenue | 是 |
| refund_policy | string enum: restate_original_purchase_window_as_of_snapshot | 是 |
| horizon_definition | string enum: elapsed_utc_half_open_7x24_28x24_hours | 是 |
| currency | string enum: USD | 是 |
| experiment_id | string | 是 |
| join_contracts | array of object | 是 |

## bundle.manifest.authorization

| 字段 | 类型 | 必需 |
|---|---|---|
| owner | string | 是 |
| authorization_reference | string | 是 |
| approved_purposes | array of string enum: ltv_research, install_probability_research, cross_app_feature_research, conditional_auction_simulation | 是 |
| valid_from | string (date-time) | 是 |
| valid_until | string (date-time) | 是 |
| app_scopes | array of string | 是 |
| cross_app_history_allowed | boolean | 是 |
| no_direct_identifiers | boolean | 是 |
| export_join_scope | string enum: dataset_only | 是 |
| source_data_synthetic | boolean | 是 |

## bundle.manifest.join_contracts

| 字段 | 类型 | 必需 |
|---|---|---|
| join_contract_id | string | 是 |
| owner_reference | string | 是 |
| allowed_purpose | string enum: cross_app_feature_research | 是 |
| valid_from | string (date-time) | 是 |
| valid_until | string (date-time) | 是 |
| scope | string enum: owner_authorized_aggregate | 是 |
| raw_ids_exported | boolean | 是 |

## bundle.installs

| 字段 | 类型 | 必需 |
|---|---|---|
| sample_key | string | 是 |
| app_scope | string | 是 |
| install_at | string (date-time) | 是 |
| available_at | string (date-time) | 是 |
| received_at | string (date-time) | 是 |
| country | string | 是 |
| platform | string enum: android, ios | 是 |
| game_version | string | 是 |
| ad_policy_version | string | 是 |
| opportunity_key | string / null | 是 |

## bundle.opportunities

| 字段 | 类型 | 必需 |
|---|---|---|
| opportunity_key | string | 是 |
| bid_at | string (date-time) | 是 |
| served | boolean | 是 |
| outcome_complete | boolean | 是 |
| installed | boolean / null | 是 |
| outcome_available_at | string (date-time) / null | 是 |
| cost_usd | string / null | 是 |
| logged_action_probability | number / null | 是 |
| logging_policy_id | string | 是 |
| randomized_exploration | boolean | 是 |

## bundle.features

| 字段 | 类型 | 必需 |
|---|---|---|
| entity_type | string enum: opportunity, install | 是 |
| entity_key | string | 是 |
| feature_name | string | 是 |
| feature_group | string enum: context, history_ads, cross_app_history, d0_behavior, d0_revenue, proxy | 是 |
| value | number | 是 |
| event_at | string (date-time) | 是 |
| source_max_available_at | string (date-time) | 是 |
| computed_at | string (date-time) | 是 |
| available_at | string (date-time) | 是 |
| received_at | string (date-time) | 是 |
| window_start_at | string (date-time) | 是 |
| window_end_at | string (date-time) | 是 |
| privacy_allowed | boolean | 是 |
| scope | string enum: single_app, owner_authorized_aggregate | 是 |
| join_contract_id | string / null | 是 |

## bundle.revenues

| 字段 | 类型 | 必需 |
|---|---|---|
| record_key | string | 是 |
| sample_key | string | 是 |
| canonical_economic_key | string | 是 |
| kind | string enum: iaa, iap | 是 |
| stage | string enum: impression, paid, fulfilled, refund | 是 |
| recognition_at | string (date-time) | 是 |
| event_at | string (date-time) | 是 |
| available_at | string (date-time) | 是 |
| received_at | string (date-time) | 是 |
| amount | string | 是 |
| currency | string | 是 |
| precision | string enum: exact, estimated, publisher_defined, undefined | 是 |
| amount_basis | string enum: publisher_net_iaa, verified_net_iap, catalog_metadata, proxy_value, predicted_value | 是 |
| purchase_verified | boolean | 是 |
| source_system | string | 是 |
| original_purchase_key | string / null | 是 |

## bundle.fx_rates

| 字段 | 类型 | 必需 |
|---|---|---|
| currency | string | 是 |
| rate_date | string (date) | 是 |
| usd_per_unit | string | 是 |
| available_at | string (date-time) | 是 |
| source_reference | string | 是 |
