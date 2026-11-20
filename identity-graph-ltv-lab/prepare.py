"""Freeze protocol and prior evidence before simulation/training. No network."""
from pathlib import Path
import hashlib,importlib.metadata,json
from datetime import datetime,timezone
R=Path(__file__).resolve().parent;P=R.parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
if (R/'PREREGISTRATION.json').exists():raise SystemExit('Protocol exists; refusing to replace it')
baseline=json.loads((P/'identity-graph-mvp/RESEARCH_BASELINE.json').read_text(encoding='utf-8'))
for p in (P/'identity-graph-mvp').rglob('*'):
    if p.is_file():baseline[p.relative_to(P).as_posix()]=sha(p)
save(R/'PRESERVATION_BASELINE.json',baseline)
(R/'dependencies').mkdir(exist_ok=True)
d=importlib.metadata.distribution('numpy')
license_path=next(d.locate_file(f) for f in d.files if str(f).endswith('LICENSE.txt') and '.dist-info/' in str(f))
(R/'dependencies/NUMPY_LICENSE.txt').write_bytes(license_path.read_bytes())
save(R/'dependencies/AUDIT.json',dict(numpy_version=d.version,license='BSD-3-Clause root license; bundled notices retained',
    source_license_path=str(license_path),source_sha256=sha(license_path),local_license='dependencies/NUMPY_LICENSE.txt',
    newly_installed_packages=[],network_requests=0,usage='Existing local NumPy only; no package redistribution'))
protocol=dict(schema='synthetic-ltv-lab-1.0',frozen_utc=datetime.now(timezone.utc).isoformat(),status='PREREGISTERED_BEFORE_SIMULATION',
  seeds=[20261,20262,20263,20264,20265],samples_per_world_seed=360,shard_size=24,
  worlds=['history_informative','no_graph_information'],
  split_sizes=dict(train=180,validation=90,test=90),install_days=dict(train=[0,13],validation=[60,66],test=[120,126]),
  prediction_offset_hours=6,label_horizons_days=[1,7,30],label_arrival_buffer_days=2,
  label_definition='Net cashflows occurring in [install,install+horizon); refunds dated inside window subtract; no purchase occurs before prediction in this generator',
  feature_cutoff='observed/available/relationship-known time <= prediction; current permission and quality gate; no row dropping for graph missingness',
  observation='Full synthetic cashflow ledger by construction; zeros are observed zero only inside this finite synthetic universe',
  models=dict(M0=['country_one_hot','platform','context_score'],M1=['M0','log1p_early_sessions','early_engagement'],
     M2=['M1','log1p_graph_observed_revenue','graph_available']),
  graph_query='Reuse identity-graph-mvp GraphFeatureService.compute/read on DEVICE; do not infer natural person; ambiguous multi-account device rejected by task-specific eligibility gate',
  generator=dict(history_latent='z~Normal(0,1), independent of context and early-intent w',
    informative_log_rate='0.9*z + 0.5*context_score + 0.65*early_engagement -0.4',
    null_log_rate='0.5*context_score + 0.65*early_engagement -0.4; history coefficient exactly zero',
    history_amount='round(1e6*max(0,80*exp(0.95*z +0.2*noise))) with synthetic refund revision',
    shared_device_rate=0.10,purchase_days=[0.5,2,6,14,29],refund_delay_days=4,refund_fraction=0.30,
    future_cashflow_noise='independent of feature creation; same seed structure in both worlds'),
  fitting=dict(algorithm='standardized ridge on log1p(net revenue); back-transform with train-only residual smearing; clip predictions >=0',
    alpha_grid=[0.1,1.0,10.0,100.0],selection='validation MAE per horizon/model; no test tuning',
    equal_samples=True,equal_labels=True,equal_splits=True,equal_hyperparameter_trials=4,
    preprocessing='train-only median imputation and standardization; graph unavailable encoded missing plus availability bit'),
  counterfactuals=['within-split graph permutation','wrong merge guarded and explicitly unsafe diagnostic',
     'candidate confidence 0.2/0.6/0.99 stays quarantined','relationship revocation','deletion invalidation',
     'future-label feature injection rejected','immature-label experiment STOP','coverage 50% and20%',
     'shared-device ambiguity','no-graph-information world'],
  uncertainty=dict(hierarchical_paired_bootstrap_repeats=500,unit='independent synthetic installation/account, then seed',
    report='all seeds, paired M2-M1 MAE/RMSE deltas, 95% intervals; no realistic effect interpretation',
    primary='D30 paired MAE delta M2-minus-M1 in informative and null worlds',multiple_comparison_policy='Other outcomes descriptive; no production significance claims'),
  metrics=['MAE','RMSE','median_absolute_error','total_prediction_ratio','Recall@10%','Top10%value_capture','graph_coverage','grouped_error','calibration_bins'],
  restrictions=dict(real_data=False,production_requests=False,SDK_execution=False,identity_service_calls=False,
    mutate_MVP=False,C_graph_Axon='UNKNOWN',C_graph_Vector='UNKNOWN',D='UNKNOWN',production_forensics='STOP'))
save(R/'PREREGISTRATION.json',protocol)
save(R/'PREREGISTRATION_HASH.json',dict(sha256=sha(R/'PREREGISTRATION.json'),frozen_utc=protocol['frozen_utc']))
print(json.dumps(dict(frozen_files=len(baseline),seeds=5,rows_per_world_seed=360,dependency=d.version)))
