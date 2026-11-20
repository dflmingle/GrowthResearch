"""Public research documents only. Reuse game/vendor sources already preserved."""
from pathlib import Path
import importlib.util
R=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('public_research_collect',R.parent/'identity-graph/collect.py')
base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base);base.R=R
if __name__=='__main__':
 base.batch('model-literature',{
  'esmm-paper':'https://arxiv.org/abs/1804.07931',
  'mmoe-paper':'https://research.google/pubs/modeling-task-relationships-in-multi-task-learning-with-multi-gate-mixture-of-experts/',
  'calibration-paper':'https://proceedings.mlr.press/v70/guo17a.html',
  'delayed-feedback-paper':'https://research.google/pubs/modeling-delayed-feedback-in-display-advertising/',
  'conformal-paper':'https://arxiv.org/abs/2107.07511',
 })
