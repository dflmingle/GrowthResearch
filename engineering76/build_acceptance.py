"""Compile each original row to explicit fixtures/claims;no new experiments."""
from pathlib import Path
import csv,json,hashlib

D=Path(__file__).resolve().parent;R=D.parent
def compile_cases():
    source=R/'75_黑盒可识别性矩阵.csv'
    with source.open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
    # Hand-reviewed observation contracts,not taken from runtime auditor output.
    contracts={
      'O1_creative':('creative','UNIDENTIFIABLE'),
      'O2_frequency':('frequency','UNIDENTIFIABLE'),
      'O3_advertiser_category':('advertiser_category','UNIDENTIFIABLE'),
      'O4_audience':('audience','BOUNDED_AUDIENCE_STATE'),
      'O5_match':('match','BOUNDED_PROVIDER_STATUS'),
      'O6_feature':('feature','BOUNDED_LOCAL_CHAIN'),
      'O7_score':('score','BOUNDED_LOCAL_CHAIN'),
      'O8_increment':('increment','STOP_REAL_LABELS_NOT_AVAILABLE')}
    cases=[]
    for row in rows:
        level,status=contracts[row['observation_id']]
        # H2/HH rows remain challenge hypotheses;we only implemented D0/D1/leak.
        # Deliberately do NOT create H2/person/household "positive engine truth".
        fixture='D0' if row['hypothesis'] in ['H0','H3_cohort','H3_shared'] else 'D1'
        required=[]
        if level=='audience':required=['recipient_test_audience_state']
        if level=='match':required=['provider_maintained_status']
        if level in ['feature','score'] and fixture=='D1':required=['local_same_device_source_history_consumed']
        cases.append(dict(case_id=row['row_id'],original_row=row,fixture_route=fixture,observation_level=level,
          expected_status=status,required_claims=required,
          forbidden_claims=['natural_person','household','cross_device_account','Axon_Vector_model_consumption','independent_value_gain','H0_training_origin','H3_training_origin'],
          hypothesis_outcome='LOCAL_SAME_DEVICE_CHAIN_ONLY' if row['hypothesis']=='H1' and level in ['feature','score'] else 'NOT_IDENTIFIED_AT_REQUESTED_HYPOTHESIS_LEVEL',
          scope='ENGINE_FIXTURE_OR_CONTRACT_FIXTURE_ONLY;NO_REAL_H2_PERSON_HOUSEHOLD_ENGINE',
          ablation='Remove audience/match scope or route provenance;must never produce stronger claims'))
    return dict(source_path=source.name,source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),row_count=len(cases),
                explicitly_unimplemented_engine_mechanisms=['cross-device identity','person entity','household entity','real mature-value gain'],cases=cases)

if __name__=='__main__':
    out=D/'acceptance/CASES.json';out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(compile_cases(),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(cases=56,original_rows_preserved=True)))
