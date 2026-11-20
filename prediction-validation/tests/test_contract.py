"""Accounting/leakage failure tests use only in-memory synthetic rows."""
import copy, unittest
from datetime import timedelta
from decimal import Decimal
from src.synthetic_fixture import fixture, ts
from src.validation import validate, build_labels, feature_eligibility, moment

class ContractTests(unittest.TestCase):
    def setUp(self):self.b=fixture()
    def rejected(self,code):
        errors=validate(self.b)['errors']
        self.assertIn(code,[x['code'] if isinstance(x,dict) else x for x in errors])
    def test_valid_synthetic_bundle(self):self.assertTrue(validate(self.b)['passed'])
    def test_half_open_windows_and_no_duplicate_income(self):
        labels,q=build_labels(self.b);x=labels[0]
        self.assertEqual(Decimal(x['d0_total_usd']),Decimal('3.10'))
        self.assertEqual(Decimal(x['d7_total_usd']),Decimal('3.30'))
        self.assertEqual(Decimal(x['d28_total_usd']),Decimal('4.00'))
        self.assertEqual(Decimal(x['d1_d28_remaining_usd']),Decimal('0.90'))
        self.assertEqual(q['counts']['duplicate_economic_reports'],4)
    def test_zero_revenue_installer_retained(self):self.assertEqual(Decimal(build_labels(self.b)[0][2]['d28_total_usd']),0)
    def test_proxy_never_added(self):self.assertEqual(validate(self.b)['excluded']['non_revenue_value'],2)
    def test_paid_fulfilled_conflict_rejected(self):
        next(r for r in self.b['revenues'] if r['stage']=='fulfilled')['amount']='5.00';self.rejected('CANONICAL_KEY_CONFLICT')
    def test_unknown_refund_rejected(self):
        next(r for r in self.b['revenues'] if r['stage']=='refund')['original_purchase_key']='SYNTHETIC_MISSING';self.rejected('REFUND_WITHOUT_PURCHASE')
    def test_positive_refund_rejected(self):
        next(r for r in self.b['revenues'] if r['stage']=='refund')['amount']='1.00';self.rejected('REFUND_LINK_OR_SIGN')
    def test_unverified_iap_rejected(self):
        next(r for r in self.b['revenues'] if r['kind']=='iap')['purchase_verified']=False;self.rejected('IAP_NOT_VERIFIED_NET_REVENUE')
    def test_missing_fx_rejected(self):
        self.b['revenues'][0]['currency']='EUR';self.b['revenues'][1]['currency']='EUR';self.rejected('MISSING_OR_AMBIGUOUS_FX')
    def test_fx_applies_once(self):
        for r in self.b['revenues'][:2]:r['currency']='EUR'
        self.b['fx_rates']=[dict(currency='EUR',rate_date='2026-01-01',usd_per_unit='2.0',available_at=ts(48),source_reference='SYNTHETIC_FX')]
        self.assertEqual(Decimal(build_labels(self.b)[0][0]['d0_total_usd']),Decimal('3.20'))
    def test_estimated_cannot_be_called_exact(self):
        self.b['manifest']['accepted_iaa_precision'].append('estimated');self.rejected('EXACT_LABEL_MIXED_PRECISION')
    def test_no_population_denominator(self):self.b['manifest']['install_population_complete']=False;self.rejected('INSTALL_DENOMINATOR_INCOMPLETE')
    def test_immature_cohort(self):self.b['manifest']['label_as_of']=ts(28*24);self.rejected('IMMATURE_D28')
    def test_missing_watermark(self):self.b['manifest']['iaa_complete_through_at']=ts(27*24);self.rejected('REVENUE_WATERMARK_INCOMPLETE')
    def test_late_arrival_not_silently_in_snapshot(self):
        for r in self.b['revenues'][:2]:r['available_at']=ts(36*24);r['received_at']=ts(36*24-.5)
        self.assertEqual(validate(self.b)['excluded']['arrived_after_label_snapshot'],2)
        self.assertEqual(Decimal(build_labels(self.b)[0][0]['d0_total_usd']),Decimal('3.00'))
    def test_future_feature_is_ineligible(self):
        f=self.b['features'][0];f['available_at']=ts(1)
        self.assertIn('AFTER_PREDICTION_TIME',feature_eligibility(f,moment(ts(-1)),'M0')[1])
    def test_source_arrived_after_bid_is_ineligible(self):
        f=self.b['features'][0];f['source_max_available_at']=ts(1)
        self.assertFalse(feature_eligibility(f,moment(ts(-1)),'M0')[0])
    def test_postinstall_features_never_in_m0_m2(self):
        f=next(f for f in self.b['features'] if f['feature_group']=='d0_revenue')
        self.assertIn('GROUP_NOT_IN_MODEL',feature_eligibility(f,moment(ts(-1)),'M2')[1])
    def test_privacy_denied_removed(self):
        f=self.b['features'][0];f['privacy_allowed']=False
        self.assertIn('PRIVACY_GATE',feature_eligibility(f,moment(ts(-1)),'M0')[1])
    def test_unapproved_cross_app_join(self):
        self.b['manifest']['authorization']['cross_app_history_allowed']=False;self.rejected('CROSS_APP_JOIN_NOT_AUTHORIZED')
    def test_unregistered_feature_blocks(self):self.b['features'][0]['feature_name']='d28_target';self.rejected('UNREGISTERED_FEATURE_OR_GROUP')
    def test_raw_identifier_column_rejected(self):self.b['installs'][0]['gaid']='SYNTHETIC_FORBIDDEN_COLUMN';self.rejected('SCHEMA')
    def test_export_outside_owner_scope(self):self.b['installs'][0]['app_scope']='SYNTHETIC_OTHER_OWNER';self.rejected('APP_OUTSIDE_AUTHORIZATION')
    def test_expired_authorization(self):self.b['manifest']['authorization']['valid_until']=ts(10);self.rejected('AUTHORIZATION_TIME_SCOPE')
    def test_authorization_assertion_does_not_enable_real_training(self):
        self.b['manifest']['provenance']='real_authorized';self.b['manifest']['authorization']['source_data_synthetic']=False
        self.assertFalse(validate(self.b)['real_training_allowed'])
    def test_installers_only_not_probability_sample(self):
        self.b['opportunities']=[];self.b['features']=[f for f in self.b['features'] if f['entity_type']=='install']
        for i in self.b['installs']:i['opportunity_key']=None
        self.assertEqual(validate(self.b)['install_probability_scope'],'not identifiable: installers only')
    def test_unserved_outcome_not_observed(self):self.b['opportunities'][0]['served']=False;self.rejected('UNSERVED_COUNTERFACTUAL_OUTCOME')
    def test_nonfinite_features_rejected(self):
        self.b['features'][0]['value']=float('nan');self.rejected('NONFINITE_FEATURE')
    def test_non_utc_manifest_rejected(self):
        self.b['manifest']['label_as_of']='2026-02-05T08:00:00+08:00';self.rejected('TIMESTAMP_NOT_UTC')
    def test_duplicate_feature_snapshot_rejected(self):
        self.b['features'].append(copy.deepcopy(self.b['features'][0]));self.rejected('DUPLICATE_FEATURE_SNAPSHOT')
    def test_disallowed_iaa_precision_rejected(self):
        self.b['revenues'][0]['precision']='estimated';self.rejected('IAA_PRECISION_NOT_ACCEPTED')

if __name__=='__main__':unittest.main()
