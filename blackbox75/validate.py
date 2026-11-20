from pathlib import Path
import csv,datetime,hashlib,json,re,ast
import numpy as np
import pandas as pd
from scipy.stats import norm,t as tdist

R=Path(__file__).resolve().parent.parent;D=R/'blackbox75';V=D/'VALIDATION.json';checks=[]
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def check(name,condition,detail=''):
 checks.append(dict(name=name,pass_check=bool(condition),detail=detail))
 if not condition:raise AssertionError(name+': '+str(detail))

def main():
 save(V,dict(status='RUNNING',started_utc=datetime.datetime.now(datetime.timezone.utc).isoformat()))
 history=read(D/'HISTORY_BEFORE.json');old=read(D/'EVIDENCE_GRAPH.before.json');g=read(R/'prediction-system/EVIDENCE_GRAPH.json')
 for rel,digest in history.items():
  if rel not in ['EVIDENCE_INDEX.md','prediction-system/EVIDENCE_GRAPH.json']:check('Historical numbered bytes: '+rel,sha(R/rel)==digest)
 check('134 historical numbered files',len(history)-2==134)
 check('Index baseline hash',sha(D/'EVIDENCE_INDEX.before.md')==history['EVIDENCE_INDEX.md'])
 check('Graph baseline hash',sha(D/'EVIDENCE_GRAPH.before.json')==history['prediction-system/EVIDENCE_GRAPH.json'])
 check('Index append only',(R/'EVIDENCE_INDEX.md').read_bytes().startswith((D/'EVIDENCE_INDEX.before.md').read_bytes()))
 for k,v in old.items():check('Graph old section preserved: '+k,g[k][:len(v)]==v if k in ['nodes','edges','sources'] else g[k]==v)
 # Check all prior round74 artifacts as well as numbered reports;do not rerun old validation or update its hashes.
 for x in read(R/'identity-value74/ARTIFACT_MANIFEST.json'):
  if x['path'] not in ['EVIDENCE_INDEX.md','prediction-system/EVIDENCE_GRAPH.json']:check('Prior74 artifact unchanged: '+x['path'],sha(R/x['path'])==x['sha256'])
 for k in ['nodes','edges','sources']:check('Graph unique IDs: '+k,len(g[k])==len({x['id'] for x in g[k]}))
 nn=g['nodes'][len(old['nodes']):];ne=g['edges'][len(old['edges']):];ns=g['sources'][len(old['sources']):]
 check('Expected new graph counts',(len(nn),len(ne),len(ns))==(18,21,16))
 ni={x['id'] for x in g['nodes']};si={x['id'] for x in g['sources']}
 check('Graph new refs valid',all(x['source'] in ni and x['target'] in ni and set(x['source_ids'])<=si for x in ne))
 check('No new E5/E6',all(not set(x['evidence_stages'])&{'E5','E6'} for x in ns+ne))
 check('No new real match/use/lift claim',all(x['production_match_proven'] is False and x['prediction_model_consumption_proven'] is False and x['independent_real_identity_lift_proven'] is False for x in ns+ne))
 for x in ns+read(D/'REUSED_EVIDENCE.json'):check('Evidence source SHA: '+x['id'],sha(R/x['path'])==x['sha256'])
 scope=read(D/'RUN_SCOPE.json')
 check('No external/real execution declared',all(v==0 for k,v in scope.items() if isinstance(v,int) and not isinstance(v,bool)))
 # Semantic/static guard:study scripts use no external clients or subprocess operations.
 for name in ['simulate.py','admission.py','build_matrix.py','write_sim_report.py','update_graph.py']:
  tree=ast.parse((D/name).read_text('utf-8'));imports=[]
  for node in ast.walk(tree):
   if isinstance(node,ast.Import):imports += [z.name for z in node.names]
   elif isinstance(node,ast.ImportFrom):imports.append(node.module or '')
  check('Offline import scope: '+name,not any(x.split('.')[0] in ['requests','http','urllib','socket','subprocess','selenium','playwright'] for x in imports))
 config=read(D/'CONFIG.json');run=read(D/'results/RUN.json')
 check('Protocol/config/code frozen in run',run['protocol_sha256']==sha(D/'PREREGISTRATION.md') and run['config_sha256']==sha(D/'CONFIG.json') and run['code_sha256']==sha(D/'simulate.py'))
 for p in [D/'PREREGISTRATION.md',D/'CONFIG.json',D/'simulate.py']:
  check('Frozen before result mtime: '+p.name,p.stat().st_mtime<=(D/'results/RUN.json').stat().st_mtime)
 check('Declared synthetic no revenue/training',config['data_type']=='SYNTHETIC_DESIGN_VALIDATION_ONLY' and config['label_or_revenue_prediction'] is False and run['real_training'] is False and run['real_external_observations']==0)
 df=pd.read_csv(D/'results/REPLICATE_RESULTS.csv');summary=pd.read_csv(D/'results/DESIGN_SUMMARY.csv')
 check('5700 rows and19x300 repeats',len(df)==5700 and len(summary)==19 and df.groupby(['module','scenario']).size().eq(300).all())
 check('Replicate IDs complete',all(sorted(q.replicate)==list(range(300)) for _,q in df.groupby(['module','scenario'])))
 check('Module scenario counts',summary.groupby('module').size().to_dict()=={'S1':12,'S2':7})
 check('P/CI values finite and bounded',np.isfinite(df[['estimate','p_value','ci_low','ci_high','fill_fraction']].to_numpy()).all() and df.p_value.between(0,1).all() and df.fill_fraction.between(0,1).all() and (df.ci_low<=df.estimate).all() and (df.ci_high>=df.estimate).all())
 check('Independent-block opportunity denominators',(df.independent_blocks==80).all() and (df.loc[df.module=='S1','observations']==3840).all() and (df.loc[df.module=='S2','observations']==7680).all())
 check('Recorded rejection decisions',np.array_equal(df.rejected.to_numpy(),(df.p_value<=.05).to_numpy()))
 for _,s in summary.iterrows():
  q=df[(df.module==s.module)&(df.scenario==s.scenario)];k=int(q.rejected.sum());n=len(q);p=k/n;z=norm.ppf(.975);den=1+z*z/n
  center=(p+z*z/(2*n))/den;half=z*np.sqrt(p*(1-p)/n+z*z/(4*n*n))/den
  check('Summary arithmetic: '+s.scenario,k==s.reject_count and abs(q.estimate.mean()-s.mean_estimate)<1e-12 and abs(p-s.reject_rate)<1e-12 and abs(center-half-s.reject_rate_mc_ci_low)<1e-12 and abs(center+half-s.reject_rate_mc_ci_high)<1e-12)
 check('Synthetic false-positive comparison truth',summary.set_index('scenario').loc['H0_randomized','reject_rate']==.04 and summary.set_index('scenario').loc['H0_randomized','naive_iid_reject_rate']==.21)
 check('Confounded scenarios explicitly invalid',not summary.loc[summary.scenario.isin(['H0_sequential_inventory_confound','H0_prior_frequency_confound','H3_target_context_leak']),'valid_design'].any())
 check('No arbitrary significance target required',True,'Validation checks arithmetic and declared truth;does not require null FPR exactly .05 or positive effects to pass')
 obs=pd.read_csv(D/'results/OBSERVATIONS/replicate0_all.csv');truth=pd.read_csv(D/'results/TRUTH/replicate0_generator.csv')
 check('Raw saved replicate0 only exact rows',len(obs)==99840 and len(truth)==1520 and run['raw_observation_rows']==len(obs))
 check('Observation schema separates truth',not any(c in obs.columns for c in ['mechanism','beta','maintained','true_person_id','real_user_id']) and set(obs.category.unique())<={0,1,2})
 check('Raw outcome fill consistency',((obs.category==0)==(~obs.filled)).all())
 obs['target']=(obs.category==1).astype(int)
 for (module,scenario),q in obs.groupby(['module','scenario']):
  estimate_record=df[(df.module==module)&(df.scenario==scenario)&(df.replicate==0)].iloc[0]
  if module=='S1':
   block=q.groupby(['block','assigned_history']).target.mean().unstack();d=block[1]-block[0]
  else:
   block=q.groupby(['block','assigned_history','assigned_account_link']).target.mean().unstack(['assigned_history','assigned_account_link'])
   d=(block[(1,1.)]-block[(0,1.)])-(block[(1,0.)]-block[(0,0.)])
  se=d.std(ddof=1)/np.sqrt(len(d));delta=d.mean();cut=tdist.ppf(.975,len(d)-1)*se
  check('Raw replicate0 independently reproduces effect/CI: '+scenario,abs(delta-estimate_record.estimate)<1e-12 and abs(delta-cut-estimate_record.ci_low)<1e-12 and abs(delta+cut-estimate_record.ci_high)<1e-12)
  if module=='S2':check('S2 interaction t p from raw: '+scenario,abs(2*tdist.sf(abs(delta/se),len(d)-1)-estimate_record.p_value)<1e-12)
  else:
   observed_p=estimate_record.p_value
   check('S1 permutation p grid: '+scenario,abs(observed_p*200-round(observed_p*200))<1e-9)
 eq=pd.read_csv(D/'results/OBSERVATIONS/EQUIVALENT_WORLDS.csv');eqt=read(D/'results/TRUTH/EQUIVALENT_WORLDS.json')
 check('Three exact observational equivalences',len(eq)==1536 and eq.groupby('pair').size().eq(512).all() and all(x['identical_observations'] for x in eqt))
 for a,b in [('world_A_category','world_B_category'),('world_A_advertiser','world_B_advertiser'),('world_A_filled','world_B_filled')]:check('Row-identical external fields: '+a,np.array_equal(eq[a],eq[b]))
 scale=read(D/'results/VALUE_SCALE_COUNTEREXAMPLE.json');check('Winner does not identify value scale',scale['identical_winner'] and not scale['absolute_value_scale_identifiable'])
 with next(R.glob('75_*.csv')).open(encoding='utf-8-sig',newline='') as f:matrix=list(csv.DictReader(f))
 check('Matrix56 and JSON consistency',len(matrix)==56 and matrix==read(D/'IDENTIFIABILITY_MATRIX.json'))
 check('Seven hypotheses x eight observables',len({x['hypothesis'] for x in matrix})==7 and len({x['observation_id'] for x in matrix})==8 and len({(x['hypothesis'],x['observation_id']) for x in matrix})==56)
 check('Matrix all assumptions/unknowns explicit',all(x['identifying_assumptions'] and x['additional_evidence_required'] and x['identifiability'] for x in matrix))
 for x in matrix:check('Matrix reused source refs: '+x['row_id'],set(x['evidence_ids'].split(';'))<=si)
 admission=read(D/'ADMISSION_AND_INTERPRETATION_CHECKS.json')
 check('12 local fixtures no actual L2',admission['status']=='PASS' and len(admission['checks'])==12 and admission['current_L2_permission'] is False and admission['external_execution'] is False)
 readiness=read(D/'EXPERIMENT_READINESS.json')
 check('Real platforms still STOP',readiness['current_external_authorization'] is False and readiness['current_real_ad_execution'] is False and readiness['L1']['external_platform_experiment']=='STOP' and readiness['L2']['status'].startswith('STOP') and readiness['real_value_experiment'].startswith('STOP'))
 files=sorted(R.glob('75_*'));check('Eight requested deliverables',len(files)==8 and sum(p.suffix=='.md' for p in files)==7 and sum(p.suffix=='.csv' for p in files)==1)
 # Verify new links only;historical index copied into this folder is not a new report.
 for p in files+[p for p in D.glob('*.md') if not p.name.endswith('.before.md')]:
  if p.suffix!='.md':continue
  txt=p.read_text('utf-8');check('No decode replacement: '+p.name,'\ufffd' not in txt)
  for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',txt):
   target=target.strip('<>').split('#')[0]
   if not target or re.match(r'https?://|mailto:',target):continue
   check('New doc local link: '+p.name+' -> '+target,(p.parent/target).exists())
 paths=files+[R/'EVIDENCE_INDEX.md',R/'prediction-system/EVIDENCE_GRAPH.json']+[p for p in D.rglob('*') if p.is_file() and p not in [V,D/'ARTIFACT_MANIFEST.json']]
 manifest=[dict(path=p.relative_to(R).as_posix(),bytes=p.stat().st_size,sha256=sha(p),modified_utc=datetime.datetime.fromtimestamp(p.stat().st_mtime,datetime.timezone.utc).isoformat()) for p in sorted(set(paths))]
 save(D/'ARTIFACT_MANIFEST.json',manifest)
 result=dict(status='PASS',completed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),checks_passed=len(checks),checks=checks,
  historical_numbered_files_unchanged=len(history)-2,deliverables=len(files),matrix_rows=56,synthetic_replicate_rows=len(df),synthetic_scenarios=len(summary),exact_equivalence_pairs=len(eqt),
  graph_counts={k:len(g[k]) for k in ['nodes','edges','sources']},external_requests=0,real_identity_queries=False,real_platform_effect_estimated=False,
  C_graph='UNKNOWN',D_independent_real_value_gain='UNKNOWN',artifact_manifest_sha256=sha(D/'ARTIFACT_MANIFEST.json'),
  limitations=['Arithmetic/hash/link integrity does not prove identification assumptions in reality','No real L1/L2 performed','Only synthetic scenario0 raw opportunities saved;all repeated statistics and seeds retained','Run scope is code/artifact audit,not independent packet capture','Public/vendor production conclusions not upgraded'])
 save(V,result);print(json.dumps({k:result[k] for k in ['status','checks_passed','historical_numbered_files_unchanged','deliverables','matrix_rows','synthetic_replicate_rows','graph_counts']},indent=2))
if __name__=='__main__':
 try:main()
 except Exception as e:save(V,dict(status='FAIL',error=repr(e),checks=checks));raise
