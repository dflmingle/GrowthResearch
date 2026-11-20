"""Focused regression tests, including the observed run-001 scheduling failure."""
import sys
sys.dont_write_bytecode=True
import tempfile,unittest,copy
from pathlib import Path
import numpy as np
from lab.common import ROOT,DAY,load,guard_feature
from lab.generator import generate
from lab.extraction import schedule_actions,extract
from lab.model import matrix,fit_predict,scale_fit
from lab.counterexamples import maturity_admission

class LabTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.p=load(ROOT/'PREREGISTRATION.json')
        cls.rows,cls.flows=generate(20261,'history_informative',cls.p)

    def test_overlapping_installations_schedule_without_rewind(self):
        rows=self.rows[:3];actions=schedule_actions(rows)
        self.assertEqual(actions,sorted(actions))
        self.assertLess(rows[1]['install_at'],rows[0]['prediction_at'])
        self.assertEqual(len(actions),6)
        installed=set()
        for _,kind,i in actions:
            if kind==0:installed.add(i)
            else:self.assertIn(i,installed)

    def test_actual_mvp_extraction_overlapping_installations(self):
        with tempfile.TemporaryDirectory() as tmp:
            rows,audit=extract(self.rows[:3],20261,'test',Path(tmp),self.p,lambda row:None)
            self.assertEqual([r['sample_id'] for r in rows],[r['sample_id'] for r in self.rows[:3]])
            self.assertEqual(len(audit),3)
            for r in audit:self.assertLessEqual(r['feature_actual_available_at'],r['prediction_at'])

    def test_generator_fixed_seed(self):
        rows,flows=generate(20261,'history_informative',self.p)
        self.assertEqual(rows,self.rows);self.assertEqual(flows,self.flows)

    def test_cashflow_labels_refunds_and_maturity(self):
        byid={}
        for event in self.flows:byid.setdefault(event['sample_id'],[]).append(event)
        self.assertTrue(any(e['amount_micros']<0 for e in self.flows))
        for row in self.rows:
            events=byid.get(row['sample_id'],[])
            for h in [1,7,30]:
                used=[e for e in events if row['install_at']<=e['occurred_at']<row['install_at']+h*DAY]
                self.assertAlmostEqual(row[f'label_D{h}'],sum(e['amount_micros'] for e in used)/1e6)
                self.assertTrue(all(e['available_at']<=row[f'mature_D{h}'] for e in used))
            self.assertTrue(all(e['occurred_at']>row['prediction_at'] for e in events))

    def test_owner_and_time_isolation(self):
        groups=[{r['owner_unit'] for r in self.rows if r['split']==s} for s in ['train','validation','test']]
        for a,b in [(0,1),(0,2),(1,2)]:self.assertFalse(groups[a]&groups[b])
        for h in [1,7,30]:self.assertEqual(maturity_admission(self.rows,h)['status'],'GO_SYNTHETIC_ONLY')

    def test_immature_label_stops(self):
        rows=copy.deepcopy(self.rows)
        rows[0]['mature_D30']=rows[-1]['prediction_at']
        self.assertEqual(maturity_admission(rows,30)['status'],'STOP')

    def test_future_and_late_features_denied(self):
        self.assertEqual(guard_feature(10,11,10),'FUTURE_INFORMATION_BLOCKED')
        self.assertEqual(guard_feature(11,10,10),'FUTURE_INFORMATION_BLOCKED')
        self.assertEqual(guard_feature(10,10,10),'ALLOW')
        self.assertEqual(guard_feature(10,None,10),'INVALID_TIME')

    def test_scaler_fitted_on_training_only(self):
        state=scale_fit(np.array([[1.,np.nan],[3.,7.]]))
        self.assertEqual(state['median'].tolist(),[2.,7.])
        self.assertEqual(state['mean'].tolist(),[2.,7.])

    def test_test_labels_never_change_fit_or_model_selection(self):
        x=matrix(self.rows,'M1');y=np.array([r['label_D30'] for r in self.rows]);split=[r['split'] for r in self.rows]
        first=fit_predict(x,y,split,[.1,1,10,100]);y[270:]=1e12
        second=fit_predict(x,y,split,[.1,1,10,100])
        self.assertEqual(first['fit_state'],second['fit_state'])
        self.assertEqual(first['trials'],second['trials'])
        np.testing.assert_array_equal(first['predictions'],second['predictions'])

    def test_latent_truth_not_in_feature_matrix(self):
        rows=copy.deepcopy(self.rows)
        for row in rows:row['history_latent']=1e30;row['label_D30']=1e30
        np.testing.assert_array_equal(matrix(rows,'M1'),matrix(self.rows,'M1'))

    def test_null_world_keeps_covariates_but_changes_response_mechanism(self):
        null,_=generate(20261,'no_graph_information',self.p)
        for a,b in zip(self.rows,null):
            for key in ['context_score','early_engagement','history_gross_micros','shared_device','install_at']:
                self.assertEqual(a[key],b[key])
        self.assertTrue(any(a['label_D30']!=b['label_D30'] for a,b in zip(self.rows,null)))

if __name__=='__main__':unittest.main(verbosity=2)
