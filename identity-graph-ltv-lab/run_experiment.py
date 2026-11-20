"""End-to-end synthetic study. No real identity, advertising or model interfaces."""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import argparse,copy,datetime,hashlib,io,json,platform,socket,contextlib
from unittest.mock import patch
import numpy as np
from lab.common import ROOT,load,save,sha,csvsave,guard_feature
from lab.generator import generate
from lab.extraction import extract
from lab.model import matrix,fit_predict,metrics
from lab.counterexamples import run_engine_probes,maturity_admission

def code_hashes():
    return {p.relative_to(ROOT).as_posix():sha(p) for p in sorted(ROOT.rglob('*.py')) if not any(x in p.parts for x in ['results','__pycache__'])}
def execute(output,protocol,progress):
    probes=run_engine_probes(output)
    allmetrics=[];calibration=[];grouped=[];predictions=[];selections=[];time_audit=[];counter=[];predsets={}
    for world in protocol['worlds']:
        for seed in protocol['seeds']:
            progress(dict(stage='START_WORLD_SEED',world=world,seed=seed))
            generated,flows=generate(seed,world,protocol)
            raw=output/'data'/world/str(seed);save(raw/'GENERATED_INSTALLS_WITH_TRUTH.json',generated);save(raw/'CASHFLOW_LEDGER.json',flows)
            maturity=[maturity_admission(generated,h) for h in [1,7,30]]
            if any(x['status']!='GO_SYNTHETIC_ONLY' for x in maturity):raise RuntimeError('Preregistered split maturity fails')
            save(raw/'LABEL_MATURITY.json',maturity)
            # Engineering feature extraction happens before model training and never
            # supplies future cashflows or z to the imported graph engine.
            rows,audit=extract(generated,seed,world,output,protocol,progress);save(raw/'FEATURE_ROWS.json',rows);time_audit.extend(audit)
            split=[r['split'] for r in rows];test_indices=[i for i,s in enumerate(split) if s=='test'];train_indices=[i for i,s in enumerate(split) if s=='train']
            # Disjoint latent owners: no same account/entity crosses stages.
            owners=[{r['owner_unit'] for r in rows if r['split']==s} for s in ['train','validation','test']]
            if any(owners[a]&owners[b] for a,b in [(0,1),(0,2),(1,2)]):raise RuntimeError('Owner leakage')
            rng=np.random.default_rng(seed+909)
            values=np.asarray([r['graph_log_history'] if r['graph_available'] else np.nan for r in rows],dtype=float)
            available=np.asarray([r['graph_available'] for r in rows],dtype=int)
            perm=values.copy();wrong=values.copy();wrong_guarded=values.copy();wrong_a=available.copy();guard_a=available.copy()
            for stage in ['train','validation','test']:
                idx=np.asarray([i for i,s in enumerate(split) if s==stage]);eligible=idx[available[idx]==1]
                perm[eligible]=values[rng.permutation(eligible)]
                # Controlled 20% false assignment to another known account. This is
                # an explicitly unsafe negative-control bypass, never a legal graph query.
                corrupted=rng.choice(eligible,size=max(1,int(len(eligible)*.2)),replace=False)
                donor=rng.permutation(eligible)
                wrong[corrupted]=values[donor[:len(corrupted)]]
                wrong_guarded[corrupted]=np.nan;guard_a[corrupted]=0
            keep_draw=rng.random(len(rows));cover50=available*(keep_draw<.5);cover20=available*(keep_draw<.2)
            zero=np.zeros(len(rows),dtype=int);missing=np.full(len(rows),np.nan)
            unsafe_shared=values.copy();unsafe_shared_a=available.copy()
            for i,r in enumerate(rows):
                if r['shared_device']:
                    unsafe_shared[i]=np.log1p((r['history_gross_micros']-r['history_refund_micros']+5000000)/1e6);unsafe_shared_a[i]=1
            variants={
              'M0':('M0',None,None),'M1':('M1',None,None),'M2':('M2',None,None),
              'C1_permuted_graph':('M2',perm,available),'C2_wrong_merge_UNSAFE':('M2',wrong,wrong_a),
              'C2_known_wrong_merge_GUARDED':('M2',wrong_guarded,guard_a),
              'C3_candidates_rejected':('M2',missing,zero),'C4_relation_revoked':('M2',missing,zero),
              'C5_deleted_history':('M2',missing,zero),'C8_coverage50':('M2',values,cover50),'C8_coverage20':('M2',values,cover20),
              'C9_shared_device_UNSAFE':('M2',unsafe_shared,unsafe_shared_a)}
            # Record exact ablation inputs, separate from generator ground truth.
            save(raw/'COUNTERFACTUAL_GRAPH_INPUTS.json',{name:dict(value=[None if not np.isfinite(v) else float(v) for v in (values if vv is None else vv)],
                available=(available if aa is None else aa).tolist(),safety='UNSAFE_DIAGNOSTIC' if 'UNSAFE' in name else 'GUARDED_OR_CONTROL')
                for name,(m,vv,aa) in variants.items() if m=='M2'})
            for horizon in [1,7,30]:
                y=np.asarray([r[f'label_D{horizon}'] for r in rows]);yt=y[test_indices]
                fitted={}
                for variant,(model,gv,ga) in variants.items():
                    x=matrix(rows,model,gv,ga);fit=fit_predict(x,y,split,protocol['fitting']['alpha_grid']);pt=fit['predictions'][test_indices];fitted[variant]=pt
                    coverage=float(np.mean((available if ga is None else ga)[test_indices])) if model=='M2' else 0.
                    met=dict(world=world,seed=seed,horizon=horizon,variant=variant,model=model,graph_coverage=coverage,**metrics(yt,pt));allmetrics.append(met)
                    selections.append(dict(world=world,seed=seed,horizon=horizon,variant=variant,chosen_alpha=fit['chosen_alpha'],trials=fit['trials'],fit_state=fit['fit_state'],
                        same_train_ids=[rows[i]['sample_id'] for i in fit['train_indices']],same_validation_ids=[rows[i]['sample_id'] for i in fit['validation_indices']],
                        same_test_ids=[rows[i]['sample_id'] for i in fit['test_indices']],feature_columns=x.shape[1]))
                    if variant in ['M0','M1','M2']:
                        order=np.argsort(pt,kind='stable')
                        for bin_idx,idx in enumerate(np.array_split(order,5)):
                            calibration.append(dict(world=world,seed=seed,horizon=horizon,model=variant,bin=bin_idx,samples=len(idx),prediction_mean=float(pt[idx].mean()),actual_mean=float(yt[idx].mean())))
                        for group in ['country','shared_device','graph_available']:
                            for key in sorted(set(rows[i][group] for i in test_indices)):
                                mask=np.asarray([rows[i][group]==key for i in test_indices]);gmet=metrics(yt[mask],pt[mask])
                                grouped.append(dict(world=world,seed=seed,horizon=horizon,model=variant,group=group,value=str(key),**gmet))
                    for j,i in enumerate(test_indices):
                        predictions.append(dict(world=world,seed=seed,horizon=horizon,variant=variant,sample_id=rows[i]['sample_id'],owner_unit=rows[i]['owner_unit'],
                            label=float(yt[j]),prediction=float(pt[j]),prediction_at=rows[i]['prediction_at'],label_mature_at=rows[i][f'mature_D{horizon}'],
                            graph_available=int((available if ga is None else ga)[i]) if model=='M2' else 0))
                # These controls must collapse to M1 when every graph column is absent,
                # after train-only imputation; don't silently report absence as a gain.
                for name in ['C3_candidates_rejected','C4_relation_revoked','C5_deleted_history']:
                    delta=float(np.max(np.abs(fitted[name]-fitted['M1'])))
                    if delta>1e-8:raise RuntimeError('All-graph-denied control is not equivalent to M1')
                    counter.append(dict(world=world,seed=seed,horizon=horizon,control=name,expected='Equivalent to M1 with all graph inputs denied',actual_max_abs_prediction_difference=delta,passed=True))
                predsets[(world,seed,horizon)]=(yt,fitted)
            # Explicit future-label feature injection is audited and denied, never
            # concatenated into any design matrix. Include values in the probe evidence.
            injection=dict(sample_id=rows[-1]['sample_id'],attempted_feature='future_D30_label',attempted_value=rows[-1]['label_D30'],
                observed_at=rows[-1]['mature_D30'],available_at=rows[-1]['mature_D30'],prediction_at=rows[-1]['prediction_at'])
            injection['decision']=guard_feature(injection['observed_at'],injection['available_at'],injection['prediction_at'])
            if injection['decision']!='FUTURE_INFORMATION_BLOCKED':raise RuntimeError('Leakage injection not blocked')
            save(raw/'BLOCKED_FUTURE_FEATURE.json',injection)
            immature=copy.deepcopy(rows)
            for r in immature:
                if r['split']=='train':r['mature_D30']=min(x['prediction_at'] for x in rows if x['split']=='validation')+1
            stopped=maturity_admission(immature,30)
            if stopped['status']!='STOP':raise RuntimeError('Immature training labels not stopped')
            save(raw/'IMMATURE_LABEL_REJECTION.json',stopped)
            progress(dict(stage='COMPLETED_MODELS',world=world,seed=seed,horizons=3,variants=len(variants)))
    intervals=[];rng=np.random.default_rng(170078)
    for world in protocol['worlds']:
        for horizon in [1,7,30]:
            for metric in ['MAE','RMSE']:
                empirical=[];samples=[]
                for seed in protocol['seeds']:
                    y,f=predsets[(world,seed,horizon)];empirical.append(metrics(y,f['M2'])[metric]-metrics(y,f['M1'])[metric])
                for b in range(protocol['uncertainty']['hierarchical_paired_bootstrap_repeats']):
                    values=[]
                    for seed in rng.choice(protocol['seeds'],len(protocol['seeds']),replace=True):
                        y,f=predsets[(world,int(seed),horizon)];idx=rng.integers(0,len(y),len(y));values.append(metrics(y[idx],f['M2'][idx])[metric]-metrics(y[idx],f['M1'][idx])[metric])
                    samples.append(float(np.mean(values)))
                intervals.append(dict(world=world,horizon=horizon,metric=metric,contrast='M2_minus_M1',mean_delta=float(np.mean(empirical)),
                    seed_std=float(np.std(empirical,ddof=1)),ci95_low=float(np.quantile(samples,.025)),ci95_high=float(np.quantile(samples,.975)),
                    seeds=len(protocol['seeds']),repeats=500,interpretation='Conditional synthetic generator interval; not real LTV or vendor effect'))
    csvsave(output/'MODEL_METRICS.csv',allmetrics);csvsave(output/'PREDICTIONS.csv',predictions);csvsave(output/'CALIBRATION.csv',calibration)
    csvsave(output/'GROUPED_ERRORS.csv',grouped);csvsave(output/'TIME_PERMISSION_AUDIT.csv',time_audit);csvsave(output/'PAIRED_INTERVALS.csv',intervals)
    save(output/'MODEL_SELECTION_AND_PARAMETERS.json',selections);save(output/'CONTROL_EQUIVALENCE.json',counter)
    summary=dict(status='PASS',engineering_probes_passed=sum(x['passed'] for x in probes),engineering_probes_total=len(probes),
      synthetic_worlds=2,seeds=5,installations=3600,horizons=[1,7,30],model_rows=len(allmetrics),prediction_rows=len(predictions),
      actual_feature_queries=len(time_audit),training_scope='SYNTHETIC_ONLY',no_fabricated_real_gain=True,
      C_graph_Axon='UNKNOWN',C_graph_Vector='UNKNOWN',D='UNKNOWN',production_forensics='STOP')
    save(output/'SUMMARY.json',summary);return summary

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();output=Path(args.output)
    if not output.is_absolute():output=ROOT/output
    if output.exists():raise SystemExit('Refusing to overwrite existing experiment '+str(output))
    output.mkdir(parents=True);protocol=load(ROOT/'PREREGISTRATION.json')
    if sha(ROOT/'PREREGISTRATION.json')!=load(ROOT/'PREREGISTRATION_HASH.json')['sha256']:raise SystemExit('Protocol changed')
    save(output/'RUN_MANIFEST.json',dict(started_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),python=sys.version,platform=platform.platform(),numpy=np.__version__,
        protocol_sha256=sha(ROOT/'PREREGISTRATION.json'),code_hashes=code_hashes(),seeds=protocol['seeds'],network='ALL socket/DNS/connection attempts blocked'))
    log=output/'RUN_LOG.jsonl'
    def progress(row):
        with log.open('a',encoding='utf-8') as f:f.write(json.dumps(row,ensure_ascii=False)+'\n')
        print(json.dumps(row),flush=True)
    def denied(*a,**kw):raise RuntimeError('NETWORK_DISABLED_SYNTHETIC_LAB')
    try:
        with patch('socket.socket',side_effect=denied),patch('socket.create_connection',side_effect=denied),patch('socket.getaddrinfo',side_effect=denied):
            summary=execute(output,protocol,progress)
    except BaseException as exc:
        import traceback
        save(output/'FAILURE.json',dict(type=type(exc).__name__,message=str(exc),traceback=traceback.format_exc()));raise
    (ROOT/'LATEST_RUN.txt').write_text(output.relative_to(ROOT).as_posix()+'\n',encoding='utf-8')
    print(json.dumps(summary,ensure_ascii=False))
if __name__=='__main__':main()
