"""Offline CLI: python -m identity_mvp demo --output demo/run-001."""
from pathlib import Path
import argparse,json,socket
from unittest.mock import patch
from .fixtures import SyntheticWorld
from generate_synthetic_data import generate
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def main():
    ap=argparse.ArgumentParser();ap.add_argument('command',choices=['demo']);ap.add_argument('--seed',type=int,default=760078);ap.add_argument('--output',required=True);args=ap.parse_args()
    directory=Path(args.output)
    if directory.exists():raise SystemExit('Refusing to overwrite '+str(directory))
    directory.mkdir(parents=True);data=generate(args.seed);save(directory/'INPUT.json',data)
    world=SyntheticWorld(directory/'database',args.seed);s=world.system
    def no_network(*a,**k):raise RuntimeError('NETWORK_DISABLED_FOR_LOCAL_SYNTHETIC_DEMO')
    try:
        with patch('socket.socket',side_effect=no_network),patch('socket.create_connection',side_effect=no_network),patch('socket.getaddrinfo',side_effect=no_network):
            ids={n['label']:world.entity(n['label'],n['entity_type'],app=n['app'],token=n['token']) for n in data['nodes']}
            for inst in data['installations']:ids[inst['label']]=world.install(inst['label'],ids[inst['device']],app=inst['app'])
            for login in data['logins']:world.login(ids[login['account']],ids[login['installation']],ids[login['device']])
            for event in data['events']:world.revenue(ids[event['installation']],event['amount_micros'],account=ids[event['account']],economic_kind=event['economic_kind'])
            for inst in data['installations']:s.events.coverage(ids[inst['label']],start_at=world.start,end_at=s.clock.now,status='COMPLETE')
            a=s.features.compute(ids['account-a'],since_at=world.start);b=s.features.compute(ids['account-b'],since_at=world.start)
            person=s.features.compute(ids['person-isolated'],since_at=world.start)
            evidence=s.features.consume_local(a['bundle_ref']);verdict=s.audit.assess_chain(evidence)
            save(directory/'FEATURES.json',dict(account_a=a,account_b=b,person_isolated=person))
            save(directory/'CONSUMER_EVIDENCE.json',dict(evidence=evidence,local_verdict=verdict))
            save(directory/'AUDIT_LOG.json',s.audit.records())
            expected=data['synthetic_truth'];passed=a['values']['observed_revenue_micros']==expected['account_a_observed_revenue_micros'] and b['values']['observed_revenue_micros']==expected['account_b_observed_revenue_micros'] and not person['values']['person_inferred'] and s.audit.verify()
            result=dict(status='PASS' if passed else 'FAIL',seed=args.seed,account_a_observed_revenue_micros=a['values']['observed_revenue_micros'],
                account_b_observed_revenue_micros=b['values']['observed_revenue_micros'],person_inferred=False,scope='SYNTHETIC_LOCAL_DEMONSTRATION_NOT_LTV_EFFECT',
                C_graph_Axon='UNKNOWN',C_graph_Vector='UNKNOWN',D='UNKNOWN',production_forensics='STOP')
            save(directory/'SUMMARY.json',result);print(json.dumps(result));return 0 if passed else 1
    finally:world.close()
if __name__=='__main__':raise SystemExit(main())
