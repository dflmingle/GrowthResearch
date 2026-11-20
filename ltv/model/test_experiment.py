import unittest
import numpy as np
from experiment import generate,alter_features,inventory_digest,metrics,top_recall,auction_evaluate,ARMS,CONTEXT

class ExperimentalValidity(unittest.TestCase):
 def test_prebid_features_deterministic(self):
  a=generate(500,51,'diffuse');b=generate(500,51,'diffuse')
  np.testing.assert_equal(a['X'],b['X']);self.assertEqual(inventory_digest(a),inventory_digest(b))
 def test_stress_does_not_change_inventory_or_labels(self):
  a=generate(500,51,'heavy_tail');original=a['X'].copy()
  for mode in ['identity_removed','wrong_links_30pct','privacy_limited','behavior_removed']:
   b=alter_features(a,mode,52)
   self.assertEqual(inventory_digest(a),inventory_digest(b));np.testing.assert_equal(a['value'],b['value'])
  np.testing.assert_equal(a['X'],original)
 def test_removed_identity_has_no_values_or_available_flag(self):
  b=alter_features(generate(500,51,'diffuse'),'identity_removed',52)
  self.assertTrue(np.isnan(b['X'][:,7:9]).all());self.assertTrue((b['X'][:,10]==0).all())
 def test_future_label_edits_do_not_change_feature_transforms(self):
  a=generate(500,51,'diffuse');b={**a,'value':a['value']*100,'install':~a['install']}
  np.testing.assert_equal(alter_features(a,'wrong_links_30pct',52)['X'],alter_features(b,'wrong_links_30pct',52)['X'])
 def test_perfect_value_prediction_has_correct_metrics(self):
  a=generate(1000,53,'diffuse');m=metrics(a,a['p'],a['value'])
  self.assertEqual(m['top10_value_recall'],1.0);self.assertAlmostEqual(m['ltv_predicted_to_actual'],1.0)
  self.assertEqual(m['ltv_decile_calibration_error'],0.)
 def test_top10_definition_exact(self):
  y=np.arange(1,101,dtype=float)
  self.assertEqual(top_recall(y,y)[0],1.0);self.assertEqual(top_recall(y,-y)[0],0.)
 def test_same_model_and_inventory_same_economics(self):
  a=generate(500,54,'diffuse')
  x=auction_evaluate(a,a['p'],a['conditional_mean'],1.,budget=5.)
  y=auction_evaluate(a,a['p'],a['conditional_mean'],1.,budget=5.)
  self.assertEqual(x,y);self.assertLessEqual(x['spend_usd'],5.+1e-9)
 def test_install_and_context_ltv_use_same_context(self):
  self.assertEqual(ARMS['install_only'],CONTEXT);self.assertEqual(ARMS['context_ltv'],CONTEXT)
 def test_positive_heavy_tail_outcome(self):
  a=generate(10000,55,'heavy_tail')
  self.assertTrue((a['value']>0).all());self.assertGreater(np.quantile(a['value'],.99),5*np.median(a['value']))

if __name__=='__main__':unittest.main(verbosity=2)
