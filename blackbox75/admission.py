"""Local-only permission/design guard. This is not permission to call a service."""
from pathlib import Path
import json

D=Path(__file__).resolve().parent
def admissible(s):
 if s.get('real_personal_identity_query',False):return False,'No real identity queries in round75'
 if s.get('production_ad_request',False):return False,'No production ads/events in round75'
 if s.get('level')=='L0':return s.get('action') in ['read_archived_docs','offline_synthetic'],'L0 has no external experiment'
 if s.get('level')=='L1':
  return bool(s.get('owned_resources') and s.get('mock_only') and not s.get('external_endpoint')),'Owned devices alone do not authorize platform experiments'
 if s.get('level')=='L2':
  return bool(s.get('written_platform_scope') and s.get('test_namespace') and s.get('synthetic_test_subjects') and s.get('privacy_purpose_allowed') and s.get('endpoint_in_scope') and not s.get('external_endpoint')=='production'),'L2 is prospective scoped sandbox only;no such permission held now'
 return False,'Unknown execution scope'

def interpretation(s):
 result=[]
 if s.get('ad_changed'):result.append('response_change_only')
 if s.get('rampid_returned') and not s.get('maintained'):result.append('derived_or_unknown_not_existing_match')
 if s.get('maintained') and s.get('authoritative_match_status'):result.append('provider_existing_match_status_not_independent_person_truth')
 if s.get('same_account'):result.append('account_not_person')
 if s.get('exchange_partner'):result.append('exchange_not_vector_consumption')
 if s.get('feature_consumed') and s.get('authorized_trace') and s.get('source_lineage') and s.get('actual_nonnull_read'):
  result.append('specified_recipient_feature_read_only')
 if s.get('independent_mature_test') and s.get('same_data_capacity_policy') and s.get('authorized_trace') and s.get('heldout_effect_ci'):
  result.append('bounded_independent_prediction_gain_not_causal_UA')
 return result

def main():
 cases=[
  ('L0 offline',dict(level='L0',action='offline_synthetic'),True),
  ('L1 local mock',dict(level='L1',owned_resources=True,mock_only=True),True),
  ('L1 owned but production ad request',dict(level='L1',owned_resources=True,mock_only=False,production_ad_request=True),False),
  ('L1 unapproved identity query',dict(level='L1',owned_resources=True,mock_only=True,real_personal_identity_query=True),False),
  ('L2 no written scope',dict(level='L2',test_namespace=True,synthetic_test_subjects=True,privacy_purpose_allowed=True,endpoint_in_scope=True),False),
  ('L2 hypothetical approved sandbox',dict(level='L2',written_platform_scope=True,test_namespace=True,synthetic_test_subjects=True,privacy_purpose_allowed=True,endpoint_in_scope=True,external_endpoint='explicit_sandbox'),True),
  ('L2 purpose denied',dict(level='L2',written_platform_scope=True,test_namespace=True,synthetic_test_subjects=True,privacy_purpose_allowed=False,endpoint_in_scope=True),False)]
 checks=[]
 for name,s,want in cases:
  got,why=admissible(s);assert got==want,name;checks.append(dict(case=name,input=s,allowed=got,reason=why))
 traps=[
  ('derived return',dict(rampid_returned=True,maintained=False),'derived_or_unknown_not_existing_match'),
  ('ad response',dict(ad_changed=True),'response_change_only'),
  ('same login',dict(same_account=True),'account_not_person'),
  ('Exchange cooperation',dict(exchange_partner=True),'exchange_not_vector_consumption'),
  ('logged feature without nonnull read',dict(feature_consumed=True,authorized_trace=True,source_lineage=True),None)]
 for name,s,want in traps:
  out=interpretation(s);assert (want in out if want else 'specified_recipient_feature_read_only' not in out),name
  checks.append(dict(case=name,input=s,interpretation=out))
 assert not any('prediction_gain' in t for _,s,_ in traps for t in interpretation(s))
 p=D/'ADMISSION_AND_INTERPRETATION_CHECKS.json';assert not p.exists()
 p.write_text(json.dumps(dict(status='PASS',hypothetical_cases_only=True,current_L2_permission=False,external_execution=False,checks=checks),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(dict(status='PASS',cases=len(checks),external_execution=False)))

if __name__=='__main__':main()
