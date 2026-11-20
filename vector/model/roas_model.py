"""Offline cohort economics. No network, SDK, advertising endpoint, or personal ID."""
from pathlib import Path
import argparse,json,csv,math
R=Path(__file__).resolve().parent
def active_curve(anchors,horizon):
 a=sorted((int(k),float(v)) for k,v in anchors.items());out=[]
 if a[0][0]!=0 or a[-1][0]<horizon:raise ValueError('anchors must cover day 0 through horizon')
 for d in range(horizon+1):
  for (lo,p),(hi,q) in zip(a,a[1:]):
   if lo<=d<=hi:out.append(p+(q-p)*(d-lo)/(hi-lo));break
 if any(x<0 or x>1 for x in out):raise ValueError('active-day probability outside [0,1]')
 return out
def observed_curves(path,horizon):
 curves={}
 with Path(path).open(encoding='utf-8-sig',newline='') as f:
  for row in csv.DictReader(f):
   arm=row['arm'];d=int(row['day']);value=float(row['net_ad_revenue_per_install_usd'])
   if not 0<=d<=horizon or value<0:raise ValueError('invalid observed row')
   if d in curves.setdefault(arm,{}):raise ValueError('duplicate arm/day')
   curves[arm][d]=value
 for arm,ds in curves.items():
  if set(ds)!=set(range(horizon+1)):raise ValueError('mature daily data required for all days; never fill immature data with zero: '+arm)
 return curves
def arm_result(arm,daily,budget):
 cpi=float(arm['cpi_usd'])
 if cpi<=0:raise ValueError('CPI must be positive')
 installed=budget/cpi;cum=[];total=0
 for value in daily:total+=value;cum.append(total)
 payback=next((d for d,x in enumerate(cum) if x>=cpi),None)
 return {'arm':arm['name'],'cpi_usd':cpi,'expected_installs':installed,'spend_usd':budget,'daily_net_ad_revenue_per_install':daily,'cumulative_ltv':cum,'ltv_d0':cum[0],'ltv_d7':cum[7],'ltv_d28':cum[28],'roas_d0':cum[0]/cpi,'roas_d7':cum[7]/cpi,'roas_d28':cum[28]/cpi,'cohort_revenue_d28_usd':cum[28]*installed,'cohort_profit_d28_usd':budget*(cum[28]/cpi-1),'cohort_payback_day':payback,'payback_censored':payback is None}
def supply_curve(segments,base_ltv):
 out=[];spend=0;n=0;rev=0
 for s in segments:
  k=float(s['installs']);c=float(s['cpi_usd']);ltv=base_ltv*float(s['ltv_multiplier'])
  if k<=0 or c<=0:raise ValueError('supply segment must have positive volume and CPI')
  spend+=k*c;n+=k;rev+=k*ltv
  out.append({'incremental_installs':k,'marginal_cpi_usd':c,'marginal_ltv_d28_usd':ltv,'marginal_roas_d28':ltv/c,'cumulative_installs':n,'cumulative_spend_usd':spend,'cumulative_revenue_usd':rev,'average_cpi_usd':spend/n,'average_roas_d28':rev/spend,'cumulative_profit_usd':rev-spend})
 return out
def run(cfg,observed=None):
 h=cfg['horizon_day']
 if h!=28:raise ValueError('this report uses mature D0/D7/D28; horizon must be 28')
 p=active_curve(cfg['active_day_probability_anchors'],h);base=[x*cfg['net_ad_revenue_per_active_day_usd'] for x in p]
 arms=[]
 for a in cfg['arms']:
  daily=[observed[a['name']][d] for d in range(h+1)] if observed is not None else [v*a['quality_multiplier'] for v in base]
  x=arm_result(a,daily,cfg['cohort_budget_usd']);x['data_origin']='user supplied mature aggregate CSV' if observed is not None else 'SYNTHETIC, no platform advantage assumed';arms.append(x)
 bias=[];ltv=sum(base);target=cfg['target_roas']
 for b in cfg['prediction_bias_scenarios']:
  ceiling=ltv*(1+b)/target
  if ceiling<=0:raise ValueError('prediction multiplier must be positive')
  bias.append({'assumed_relative_bias':b,'assumed_actual_ltv':ltv,'predicted_ltv':ltv*(1+b),'illustrative_cpi_ceiling':ceiling,'realized_roas_if_price_equals_ceiling':target/(1+b),'profit_per_install_if_price_equals_ceiling':ltv-ceiling,'limitation':'a value-to-price sensitivity identity, not an auction simulation or measured platform calibration'})
 learn=[]
 for a in cfg['arms']:
  speed=cfg['daily_budget_usd']/a['cpi_usd'];payer=cfg['payer_probability_d7'];lag=cfg['report_lag_days']
  for kind,window,n,pay,mature in [('IAA',0,1000,0,0),('IAA',7,1000,0,7),('IAA',28,1000,0,7),('IAP',7,0,75,7),('IAP',28,0,75,7),('Hybrid',7,1000,35,7),('Hybrid',28,1000,35,7)]:
   need=max(n,pay/payer if pay else 0);days=math.ceil(need/speed)
   learn.append({'arm':a['name'],'unity_documented_threshold_scenario_only':True,'type':kind,'window':window,'expected_acquisition_days_to_threshold':days,'conservative_maturity_plus_reporting_days':days+mature+lag,'assumptions':'constant CPI, fixed eligible payer rate, positive matured IAA; no guarantee of platform learning; not Axon threshold'})
 return {'scope':cfg['label'],'input':cfg,'arms':arms,'supply_segments':supply_curve(cfg['supply_segments'],ltv),'prediction_bias_sensitivity':bias,'learning_planning':learn,'definitions':{'day0':'install calendar day; days0..7 and0..28 inclusive','ltv':'net ad revenue per originally installed user, not per survivor','active_probability':'unconditional probability of activity on that day; may include returners, not survival','payback':'cohort cumulative revenue >= CPI, not cash settlement or portfolio cash-flow payback','installs':'expected fractional count for analytical budget comparison','no_head_to_head_claim':True}}
def write_rows(p,rows):
 with p.open('w',encoding='utf-8-sig',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def export(result,out):
 out.mkdir(parents=True,exist_ok=True);(out/'results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
 write_rows(out/'arms.csv',[{k:v for k,v in a.items() if not isinstance(v,list)} for a in result['arms']]);write_rows(out/'scaling.csv',result['supply_segments']);write_rows(out/'prediction_bias.csv',result['prediction_bias_sensitivity']);write_rows(out/'learning.csv',result['learning_planning'])
 write_rows(out/'daily_actual_template.csv',[{'arm':a['arm'],'day':d,'net_ad_revenue_per_install_usd':v,'label':'SYNTHETIC template replace with mature measured cohort revenue'} for a in result['arms'] for d,v in enumerate(a['daily_net_ad_revenue_per_install'])])
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--input',default=str(R/'inputs.json'));p.add_argument('--actual-daily-csv');p.add_argument('--output',default=str(R/'output'));a=p.parse_args();cfg=json.loads(Path(a.input).read_text(encoding='utf-8'));obs=observed_curves(a.actual_daily_csv,28) if a.actual_daily_csv else None;result=run(cfg,obs);export(result,Path(a.output));print(json.dumps([{k:a[k] for k in ['arm','ltv_d0','ltv_d7','ltv_d28','roas_d28','cohort_payback_day']} for a in result['arms']],indent=2))
