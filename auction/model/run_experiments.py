"""Deterministic local synthetic data only; matched opportunities for all arms."""
from pathlib import Path
from dataclasses import asdict
from decimal import Decimal
import json,random,csv
from auction_model import Auction,Offer,PROFILES,D,value_bid,request_fixture,response_fixture

R=Path(__file__).resolve().parent;O=R/'output';O.mkdir(exist_ok=True)
def dump(name,x):
 (O/name).write_text(json.dumps(x,ensure_ascii=False,indent=2,default=str),encoding='utf-8')

for p in PROFILES:
 dump('request-'+p+'.json',request_fixture(p))
 dump('response-'+p+'.json',response_fixture(Offer('synthetic-DSP',D('12')),p))
rng=random.Random(351940)
opps=[]
for i in range(10000):
 p=rng.uniform(.015,.075);ltv=rng.uniform(.4,2.2)
 opps.append(dict(id='synthetic-'+str(i),p=p,ltv=ltv,install_draw=rng.random(),
                  rival_cpm=rng.uniform(4,100),rival_latency=rng.choice([80,150,260,550]),
                  load_ok=rng.random()>.04,render=rng.random()>.08))
rows=[];sample=[]
for profile in PROFILES:
 for factor in [0.6,1.0,1.4]:
  auction=Auction(PROFILES[profile]);budgets={'advertiser':D('20'),'competitor':D('1000')}
  spend=D('0');installs=0;wins=0;truth=D('0');timeouts=0;budget_rejects=0
  for i,x in enumerate(opps):
   bid=value_bid(x['p'],x['ltv']*factor,target_roas=D('1'),shade=D('.8')).quantize(D('.001'))
   offers=[Offer('advertiser',bid,request_id=x['id'],load_ok=x['load_ok'],render=x['render']),
           Offer('competitor',D(str(x['rival_cpm'])).quantize(D('.001')),latency_ms=x['rival_latency'],request_id=x['id'])]
   result=auction.run(offers,floor=D('3'),request_id=x['id'],budgets=budgets)
   timeouts+=int(result.rejected.get('competitor')=='timeout')
   budget_rejects+=int(result.rejected.get('advertiser')=='budget_limit')
   if result.selected=='advertiser' and result.rendered:
    wins+=1;spend+=result.billed_usd
    if x['install_draw']<x['p']:
     installs+=1;truth+=D(str(x['ltv']))
   if i<12 and factor==1.0:sample.append(dict(profile=profile,opportunity=x,bid=str(bid),result=asdict(result)))
  d0=truth*D('.15');d7=truth*D('.55');d28=truth
  rows.append(dict(profile=profile,configured_tmax_ms=PROFILES[profile].tmax_ms,ltv_prediction_multiplier=factor,
   opportunities=len(opps),rendered_wins=wins,installs=installs,spend_usd=float(spend),
   CPI_usd=float(spend/installs) if installs else None,
   D0_revenue_usd=float(d0),D7_revenue_usd=float(d7),D28_revenue_usd=float(d28),
   D0_ROAS=float(d0/spend) if spend else None,D7_ROAS=float(d7/spend) if spend else None,D28_ROAS=float(d28/spend) if spend else None,
   competitor_timeout_count=timeouts,advertiser_budget_rejects=budget_rejects))
dump('results.json',dict(seed=351940,synthetic=True,platform_model_recovered=False,
 limits=['200ms Unity fixture is configurable; difference is protocol/fixture effect, not AI superiority.',
         'Same pInstall, true LTV, random draws and competitors across arms; sample variance remains.',
         'Revenue maturity schedule D0=15%, D7=55%, D28=100% is synthetic, not vendor/game data.',
         'Only one winning candidate per opportunity; real failover and mediation logic are not reproduced.'],arms=rows))
dump('sample_traces.json',sample)
with (O/'arms.csv').open('w',newline='',encoding='utf-8-sig') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

# Control: eliminate configured tmax difference; do not attribute fixture differences to AI quality.
control=Auction(PROFILES['unity']);cb={'advertiser':D('20'),'competitor':D('1000')}
cs=D('0');cw=0;ci=0;cr=D('0')
for x in opps:
 offers=[Offer('advertiser',value_bid(x['p'],x['ltv'],shade=D('.8')).quantize(D('.001')),
               request_id=x['id'],load_ok=x['load_ok'],render=x['render']),
         Offer('competitor',D(str(x['rival_cpm'])).quantize(D('.001')),latency_ms=x['rival_latency'],request_id=x['id'])]
 result=control.run(offers,floor=D('3'),request_id=x['id'],budgets=cb,tmax_ms=500)
 if result.selected=='advertiser' and result.rendered:
  cw+=1;cs+=result.billed_usd
  if x['install_draw']<x['p']:ci+=1;cr+=D(str(x['ltv']))
baseline=next(x for x in rows if x['profile']=='applovin' and x['ltv_prediction_multiplier']==1.0)
equal=(cw==baseline['rendered_wins'] and ci==baseline['installs'] and float(cs)==baseline['spend_usd'] and float(cr)==baseline['D28_revenue_usd'])
assert equal
dump('matched_tmax_control.json',dict(synthetic=True,profiles=['applovin','unity'],tmax_ms=500,
   multiplier=1.0,economics_identical=equal,rendered_wins=cw,installs=ci,spend_usd=str(cs),D28_revenue_usd=str(cr),
   meaning='Same value predictions and opportunities yield identical economics after eliminating tmax; NOT production equivalence proof.'))

# Controlled feedback illustration: analyst-defined EMA, not either proprietary training loop.
old=D('.8');observed=D('1.6');new=old*D('.5')+observed*D('.5')
dump('feedback.json',dict(method='Illustrative EMA with synthetic mature cohort revenue; NOT Axon/Vector learning',
 p_install='.02',prior_predicted_ltv=str(old),synthetic_observed_ltv=str(observed),updated_ltv=str(new),
 cpm_before=str(value_bid('.02',old)),cpm_after=str(value_bid('.02',new)),
 restriction='No individual/user data. Do not substitute predicted values for actual revenue postbacks.'))

# Simple illustrative waterfall merging: declared CPM is a ranking estimate, not an actual DSP bid.
dump('waterfall_example.json',dict(scope='Teaching assumption, NOT complete MAX/LevelPlay scheduler',
 candidates=[dict(source='waterfall-instance',ranking_cpm=20,kind='estimated',load='fail'),
             dict(source='real-time-bid',ranking_cpm=15,kind='bid',load='success')],
 result='Try estimated 20 first; failover to actual 15. Estimate is not a guaranteed payable offer.'))
print(json.dumps(rows,indent=2));print('feedback',old,'->',new)
