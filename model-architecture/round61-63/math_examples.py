"""Independent arithmetic examples, NOT Axon/Vector model or performance tests."""
from pathlib import Path
from fractions import Fraction as Q
import json

O=Path(__file__).resolve().parent
def moments(prob,amount):
    p=Q(prob);a=Q(amount);mean=p*a;variance=p*a*a-mean*mean
    return dict(mean=float(mean),variance=float(variance))

def example_cpm(p,mu,tau):return Q(1000)*Q(p)*Q(mu)/Q(tau)

def run():
    a=moments('0.10','8');b=moments('0.01','80')
    assert a==dict(mean=0.8,variance=5.76)
    assert b==dict(mean=0.8,variance=63.36)
    assert example_cpm('0.02','0.8','1.2')==Q(40,3)
    assert example_cpm('0.02','1','1.2')==Q(50,3)
    assert example_cpm('0.02','0.8','1.5')==Q(32,3)
    base=Q('0.54')-Q('0.60');quality=Q('0.66')-Q('0.60');cost=Q('0.54')-Q('0.48')
    assert (base,quality,cost)==(Q('-0.06'),Q('0.06'),Q('0.06'))
    return dict(scope='Independent constructed arithmetic ONLY; no real data, vendor models, auctions or production requests',
      equal_mean_different_tails=dict(A=a,B=b),cpm_examples={
       'p.02_mu.8_tau1.2':float(Q(40,3)),'p.02_mu1_tau1.2':float(Q(50,3)),'p.02_mu.8_tau1.5':float(Q(32,3))},
      contribution_examples=dict(baseline=float(base),quality_case=float(quality),cost_case=float(cost)),
      checks='PASS',vendor_algorithm_claim=False,empirical_performance_claim=False)

if __name__=='__main__':
    result=run();(O/'MATH_EXAMPLES.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))
