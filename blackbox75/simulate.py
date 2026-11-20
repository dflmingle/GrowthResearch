"""Offline identifiability/design counterexamples;no vendor or real user data."""
from pathlib import Path
import datetime,hashlib,json,math,time
import numpy as np
import pandas as pd
from scipy.special import expit
from scipy.stats import norm,t as tdist

D=Path(__file__).resolve().parent
C=json.loads((D/'CONFIG.json').read_text('utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def paired_t(d):
 n=len(d);est=float(np.mean(d));se=float(np.std(d,ddof=1)/np.sqrt(n))
 if se==0:return est,1. if est==0 else 0.,est,est
 cut=float(tdist.ppf(.975,n-1))*se
 return est,float(2*tdist.sf(abs(est/se),n-1)),est-cut,est+cut

def randomization_p(d,rng):
 signs=rng.choice([-1.,1.],size=(C['permutation_draws'],len(d)))
 null=np.abs((signs*d[None,:]).mean(axis=1));observed=abs(float(d.mean()))
 return float((1+np.sum(null>=observed-1e-14))/(len(null)+1))

def render(rng,logits,cap=False,low_stock=False):
 # Independent opportunities within a device conditional on its latent score;
 # caps create additional dependence. No external ad requests exist.
 n=len(logits);o=C['opportunities_per_cell']
 prob=expit(logits[:,None]+rng.normal(0,C['auction_logit_sd'],size=(n,o)))
 fill=rng.random((n,o))<(0.28 if low_stock else .92)
 eligible=rng.random((n,o))<(.18 if low_stock else 1.)
 target=(rng.random((n,o))<prob)&fill&eligible
 if cap:target&=np.cumsum(target,axis=1)<=C['frequency_cap_per_cell']
 # category 0 denotes no fill;1 target;2 another category.
 observed=np.where(~fill,0,np.where(target,1,2))
 return target,fill,observed

S1=[
 dict(name='H0_randomized',mechanism='H0',beta=0.),
 dict(name='H3_frozen_randomized',mechanism='H3',beta=0.),
 dict(name='H1_randomized',mechanism='H1',beta=C['history_logit_coefficient']),
 dict(name='H1_false_route20',mechanism='H1',beta=C['history_logit_coefficient'],false_route=.2),
 dict(name='H1_privacy_gate_off',mechanism='H1',beta=0.,gate_off=True),
 dict(name='H1_time_relation_reversed',mechanism='H1',beta=-C['history_logit_coefficient']),
 dict(name='H1_low_target_inventory',mechanism='H1',beta=C['history_logit_coefficient'],low_stock=True),
 dict(name='H1_frequency_cap',mechanism='H1',beta=C['history_logit_coefficient'],cap=True),
 dict(name='H0_sequential_inventory_confound',mechanism='H0',beta=0.,inventory_confound=True),
 dict(name='H0_inventory_block_repaired',mechanism='H0',beta=0.),
 dict(name='H0_prior_frequency_confound',mechanism='H0',beta=0.,prior_frequency_confound=True),
 dict(name='H0_prior_frequency_balanced',mechanism='H0',beta=0.),
]
S2=[
 dict(name='H0_account_main_effect_only',mechanism='H0',beta=0.),
 dict(name='H1_no_cross_device',mechanism='H1',beta=0.),
 dict(name='H3_frozen_no_transfer',mechanism='H3',beta=0.),
 dict(name='H2_account_history_transfer',mechanism='H2_account',beta=C['history_logit_coefficient']),
 dict(name='H2_false_route20',mechanism='H2_account',beta=C['history_logit_coefficient'],false_route=.2),
 dict(name='H2_privacy_gate_off',mechanism='H2_account',beta=0.,gate_off=True),
 dict(name='H3_target_context_leak',mechanism='H3_no_identity_history_store',beta=C['history_logit_coefficient'],exclusion_violation=True),
]

def main():
 out=D/'results';assert not out.exists(),'Never overwrite experiment outputs'
 out.mkdir();(out/'TRUTH').mkdir();(out/'OBSERVATIONS').mkdir()
 start=time.time();rng=np.random.default_rng(C['seed']);rows=[];samples=[];truth=[]
 n=C['independent_blocks'];o=C['opportunities_per_cell']
 for spec in S1:
  for rep in range(C['replicates']):
   history=rng.integers(0,2,size=(n,2)) # overwritten by one randomized arm per block
   treated_slot=rng.integers(0,2,size=n);history[:]=0;history[np.arange(n),treated_slot]=1
   market=rng.normal(0,C['shared_inventory_logit_sd'],n)
   dev=rng.normal(0,C['device_logit_sd'],size=(n,2))
   routed=history.copy();mask=rng.random((n,2))<spec.get('false_route',0)
   routed[mask]=rng.integers(0,2,size=int(mask.sum()))
   logits=-.8+market[:,None]+dev+spec['beta']*routed
   if spec.get('inventory_confound'):logits+=1.0*history
   if spec.get('prior_frequency_confound'):logits-=1.0*history
   target,fill,obs=render(rng,logits.ravel(),cap=spec.get('cap',False),low_stock=spec.get('low_stock',False))
   means=target.mean(axis=1).reshape(n,2);d=means[np.arange(n),treated_slot]-means[np.arange(n),1-treated_slot]
   estimate,pt,lo,hi=paired_t(d);pr=randomization_p(d,rng)
   tr=target.reshape(n,2,o)[np.arange(n),treated_slot].ravel()
   co=target.reshape(n,2,o)[np.arange(n),1-treated_slot].ravel()
   pooled=(tr.sum()+co.sum())/(len(tr)+len(co));se=np.sqrt(pooled*(1-pooled)*(1/len(tr)+1/len(co)))
   naive=float(2*norm.sf(abs(estimate/se))) if se else 1.
   rows.append(dict(module='S1',scenario=spec['name'],mechanism_truth=spec['mechanism'],replicate=rep,
    true_history_coefficient=spec['beta'],null_history_channel=spec['beta']==0,
    valid_design=not(spec.get('inventory_confound',False) or spec.get('prior_frequency_confound',False)),
    estimate=estimate,p_value=pr,p_kind='block_sign_flip_199',ci_low=lo,ci_high=hi,ci_kind='block_t_approximation',
    naive_opportunity_p=naive,account_main_effect_p=None,fill_fraction=float(fill.mean()),independent_blocks=n,observations=2*n*o))
   if rep==C['samples_saved_replicate']:
    for b in range(n):
     truth.append(dict(module='S1',scenario=spec['name'],block=b,history_slot0=int(history[b,0]),history_slot1=int(history[b,1]),route_slot0=int(routed[b,0]),route_slot1=int(routed[b,1]),beta=spec['beta'],mechanism=spec['mechanism']))
     for slot in range(2):
      for j in range(o):samples.append(dict(module='S1',scenario=spec['name'],block=b,cell=slot,opportunity=j,assigned_history=int(history[b,slot]),assigned_account_link=None,category=int(obs.reshape(n,2,o)[b,slot,j]),filled=bool(fill.reshape(n,2,o)[b,slot,j])))
 for spec in S2:
  for rep in range(C['replicates']):
   # Four independent target units in each block,randomized physical ordering.
   history=np.tile([0,1,0,1],(n,1));link=np.tile([0,0,1,1],(n,1))
   perm=np.array([rng.permutation(4) for _ in range(n)])
   h=np.take_along_axis(history,perm,axis=1);l=np.take_along_axis(link,perm,axis=1)
   routed=h.copy();mask=rng.random((n,4))<spec.get('false_route',0);routed[mask]=rng.integers(0,2,size=int(mask.sum()))
   market=rng.normal(0,C['shared_inventory_logit_sd'],n)
   dev=rng.normal(0,C['device_logit_sd'],size=(n,4))
   logits=-.8+market[:,None]+dev+.35*l+spec['beta']*routed*l
   target,fill,obs=render(rng,logits.ravel());means=target.mean(axis=1).reshape(n,4)
   # Gather canonical (h0l0,h1l0,h0l1,h1l1),irrespective of randomized slots.
   y=np.take_along_axis(means,np.argsort(perm,axis=1),axis=1)
   d=(y[:,3]-y[:,2])-(y[:,1]-y[:,0]);estimate,p,lo,hi=paired_t(d)
   main=.5*((y[:,2]+y[:,3])-(y[:,0]+y[:,1]));_,pm,_,_=paired_t(main)
   rows.append(dict(module='S2',scenario=spec['name'],mechanism_truth=spec['mechanism'],replicate=rep,
    true_history_coefficient=spec['beta'],null_history_channel=spec['beta']==0,
    valid_design=not spec.get('exclusion_violation',False),estimate=estimate,p_value=p,p_kind='block_interaction_t_approximation',
    ci_low=lo,ci_high=hi,ci_kind='block_t_approximation',naive_opportunity_p=None,account_main_effect_p=pm,
    fill_fraction=float(fill.mean()),independent_blocks=n,observations=4*n*o))
   if rep==C['samples_saved_replicate']:
    for b in range(n):
     truth.append(dict(module='S2',scenario=spec['name'],block=b,beta=spec['beta'],mechanism=spec['mechanism'],exclusion_violation=spec.get('exclusion_violation',False)))
     for slot in range(4):
      for j in range(o):samples.append(dict(module='S2',scenario=spec['name'],block=b,cell=slot,opportunity=j,assigned_history=int(h[b,slot]),assigned_account_link=int(l[b,slot]),category=int(obs.reshape(n,4,o)[b,slot,j]),filled=bool(fill.reshape(n,4,o)[b,slot,j])))
 df=pd.DataFrame(rows);df['rejected']=df.p_value<=C['alpha'];df.to_csv(out/'REPLICATE_RESULTS.csv',index=False,encoding='utf-8-sig')
 pd.DataFrame(samples).to_csv(out/'OBSERVATIONS/replicate0_all.csv',index=False,encoding='utf-8-sig')
 pd.DataFrame(truth).to_csv(out/'TRUTH/replicate0_generator.csv',index=False,encoding='utf-8-sig')
 def wilson(k,n):
  z=norm.ppf(.975);p=k/n;den=1+z*z/n;center=(p+z*z/(2*n))/den;half=z*np.sqrt(p*(1-p)/n+z*z/(4*n*n))/den
  return float(center-half),float(center+half)
 summary=[]
 for (module,scenario),q in df.groupby(['module','scenario'],sort=False):
  k=int(q.rejected.sum());lo,hi=wilson(k,len(q));main=q.account_main_effect_p.dropna()
  summary.append(dict(module=module,scenario=scenario,data_type='SYNTHETIC_DESIGN_VALIDATION_ONLY',replicates=len(q),
   mechanism_truth=q.mechanism_truth.iloc[0],null_history_channel=bool(q.null_history_channel.iloc[0]),valid_design=bool(q.valid_design.iloc[0]),
   mean_estimate=float(q.estimate.mean()),reject_count=k,reject_rate=k/len(q),reject_rate_mc_ci_low=lo,reject_rate_mc_ci_high=hi,
   non_reject_rate=1-k/len(q),naive_iid_reject_rate=float((q.naive_opportunity_p.dropna()<=C['alpha']).mean()) if q.naive_opportunity_p.notna().any() else None,
   account_main_effect_reject_rate=float((main<=C['alpha']).mean()) if len(main) else None,
   mean_fill_fraction=float(q.fill_fraction.mean()),independent_blocks=n,opportunities_per_cell=o))
 pd.DataFrame(summary).to_csv(out/'DESIGN_SUMMARY.csv',index=False,encoding='utf-8-sig')
 # Exact observational equivalence: a constructive counterexample,not a failed test.
 eq=[];eq_truth=[];nr=512;rr=np.random.default_rng(C['seed']+9000)
 x=rr.normal(size=nr);h=rr.integers(0,2,nr);link=rr.integers(0,2,nr)
 for name,latent,truth_a,truth_b in [
  ('H0_vs_H3_same_frozen_mapping',-.8+.4*x,'target/context parameters','cross-game learned parameters;identical mapping'),
  ('H1_vs_H3_unobserved_context_mediator',-.8+.4*x+.65*h,'online individual cross-app route','no history lookup;current cohort/context encodes intervention'),
  ('H2_history_vs_account_audience',-.8+.4*x+.65*h*link,'cross-device history feature read','account audience eligibility rule;not value model')]:
  probability=expit(latent);u=rr.random(nr);fill=rr.random(nr)<.92
  # The same observable probability function makes all listed observations identical.
  a=np.where(~fill,0,np.where(u<probability,1,2));b=np.where(~fill,0,np.where(u<probability,1,2))
  for i in range(nr):eq.append(dict(pair=name,observation=i,world_A_category=int(a[i]),world_B_category=int(b[i]),
    world_A_advertiser=int(a[i]),world_B_advertiser=int(b[i]),world_A_filled=bool(fill[i]),world_B_filled=bool(fill[i])))
  eq_truth.append(dict(pair=name,truth_A=truth_a,truth_B=truth_b,identical_observations=bool(np.array_equal(a,b)),
    discriminator='source-training provenance' if 'frozen' in name else 'causal exclusion/context-path audit' if 'mediator' in name else 'recipient feature-group consumption and audience/selector audit'))
 pd.DataFrame(eq).to_csv(out/'OBSERVATIONS/EQUIVALENT_WORLDS.csv',index=False,encoding='utf-8-sig')
 save(out/'TRUTH/EQUIVALENT_WORLDS.json',eq_truth)
 base=np.column_stack([x,.4-x,-.6+.1*x]);scaled=7*base+3
 save(out/'VALUE_SCALE_COUNTEREXAMPLE.json',dict(rows=nr,scores_A='unscaled synthetic ranking scores',scores_B='7*A+3',
  identical_winner=bool(np.array_equal(np.argmax(base,axis=1),np.argmax(scaled,axis=1))),
  absolute_value_scale_identifiable=False,qualifier='No observed bid/score or controller;not a vendor formula or revenue label'))
 save(out/'RUN.json',dict(completed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),seconds=time.time()-start,
  seed=C['seed'],protocol_sha256=sha(D/'PREREGISTRATION.md'),config_sha256=sha(D/'CONFIG.json'),code_sha256=sha(Path(__file__)),
  replicates_rows=len(df),summary_rows=len(summary),raw_observation_rows=len(samples),synthetic_truth_rows=len(truth),
  equivalence_rows=len(eq),real_external_observations=0,real_identity_queries=0,real_training=False,
  intervals='Within-replicate block t CIs;rejection-rate Wilson Monte Carlo CIs;neither estimates real platform effects'))
 print(json.dumps(dict(status='DONE_SYNTHETIC_ONLY',replicate_rows=len(df),summary_rows=len(summary),seconds=time.time()-start),indent=2))

if __name__=='__main__':main()
