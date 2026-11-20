"""Generate reproducible fake identifiers and a local demonstration scenario."""
from pathlib import Path
import argparse,json,random
def generate(seed=760078):
    rng=random.Random(seed)
    nodes=[dict(label=name,entity_type=kind,app=app,token=f'syn:{name}:{rng.getrandbits(64):016x}')
        for name,kind,app in [('device-a','device','synthetic-app-a'),('device-b','device','synthetic-app-a'),
          ('account-a','account','first-party-account'),('account-b','account','first-party-account'),('person-isolated','person','synthetic-app-a')]]
    return dict(environment='LOCAL_SYNTHETIC_ONLY',seed=seed,currency='USD',money_unit='integer-micros',nodes=nodes,
        installations=[dict(label='app-a-on-a',device='device-a',app='synthetic-app-a'),dict(label='app-b-on-b',device='device-b',app='synthetic-app-b')],
        logins=[dict(account='account-a',installation='app-a-on-a',device='device-a'),dict(account='account-a',installation='app-b-on-b',device='device-b'),
                dict(account='account-b',installation='app-a-on-a',device='device-a')],
        events=[dict(installation='app-a-on-a',account='account-a',amount_micros=1200000,economic_kind='IAP'),
                dict(installation='app-b-on-b',account='account-a',amount_micros=250000,economic_kind='IAA'),
                dict(installation='app-a-on-a',account='account-b',amount_micros=9000000,economic_kind='IAP')],
        synthetic_truth=dict(account_a_observed_revenue_micros=1450000,account_b_observed_revenue_micros=9000000,
            person_account_relationship='UNSPECIFIED_AND_NOT_INFERRED'),
        caveat='Entirely fabricated event amounts/identities; NOT LTV data or a real-world effect')
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--seed',type=int,default=760078);p.add_argument('--output',required=True);args=p.parse_args()
    out=Path(args.output)
    if out.exists():raise SystemExit('Refusing to overwrite '+str(out))
    out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(generate(args.seed),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(str(out.resolve()))
