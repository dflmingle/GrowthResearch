from roas_model import *
import tempfile,copy
cfg=json.loads((R/'inputs.json').read_text(encoding='utf-8'));x=run(cfg);checks=[]
def check(name,value):
 if not value:raise AssertionError(name)
 checks.append(name)
a,b=x['arms'];check('matched inputs yield identical outcomes',a['cumulative_ltv']==b['cumulative_ltv'] and a['roas_d28']==b['roas_d28'])
check('D0 is unconditional installed-user revenue',a['ltv_d0']==cfg['net_ad_revenue_per_active_day_usd'])
check('ROAS and profit reconcile',abs(a['cohort_revenue_d28_usd']-a['spend_usd']-a['cohort_profit_d28_usd'])<1e-8)
c=copy.deepcopy(cfg);c['arms'][0]['cpi_usd']=100;check('no false payback beyond observed horizon',run(c)['arms'][0]['cohort_payback_day'] is None)
check('marginal differs from blended',x['supply_segments'][-1]['marginal_roas_d28']<x['supply_segments'][-1]['average_roas_d28'])
check('zero prediction bias at tROAS ceiling',x['prediction_bias_sensitivity'][1]['realized_roas_if_price_equals_ceiling']==cfg['target_roas'])
with tempfile.TemporaryDirectory(dir=R) as td:
 p=Path(td)/'actual.csv';write_rows(p,[{'arm':arm['name'],'day':d,'net_ad_revenue_per_install_usd':.01} for arm in cfg['arms'] for d in range(29)]);obs=observed_curves(p,28);check('actual CSV overrides simulated retention',abs(run(cfg,obs)['arms'][0]['ltv_d28']-.29)<1e-9)
 write_rows(p,[{'arm':'Unity_Vector','day':0,'net_ad_revenue_per_install_usd':.01}])
 try:observed_curves(p,28);raise AssertionError('accepted immature data')
 except ValueError:checks.append('reject immature or missing daily cohorts')
(R/'MODEL_VALIDATION.json').write_text(json.dumps({'status':'PASS','checks':checks,'scope':'offline calculation and data validation; no platform performance proof'},indent=2),encoding='utf-8');print('PASS',len(checks))
