"""Independent post-run consistency and preservation audit. Does not train."""
import sys
sys.dont_write_bytecode=True
import csv,collections,datetime
from lab.common import ROOT,load,sha,save,DAY
import numpy as np
from lab.model import matrix,scale_fit,metrics

def read(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))

def main():
    checks=[]
    def check(name,expected,actual):
        checks.append(dict(name=name,expected=expected,actual=actual,passed=expected==actual))
    base=load(ROOT/'PRESERVATION_BASELINE.json');changed=[]
    for path,h in base.items():
        p=ROOT.parent/path
        if not p.is_file() or sha(p)!=h:changed.append(path)
    check('all_prior_files_unchanged',[],changed)
    run=ROOT/(ROOT/'LATEST_RUN.txt').read_text().strip();manifest=load(run/'RUN_MANIFEST.json')
    for path,h in manifest['code_hashes'].items():check('executed_source:'+path,h,sha(ROOT/path))
    check('frozen_protocol',load(ROOT/'PREREGISTRATION_HASH.json')['sha256'],sha(ROOT/'PREREGISTRATION.json'))
    check('run_protocol',manifest['protocol_sha256'],sha(ROOT/'PREREGISTRATION.json'))
    check('dependency_license',load(ROOT/'dependencies/AUDIT.json')['source_sha256'],sha(ROOT/'dependencies/NUMPY_LICENSE.txt'))
    summary=load(run/'SUMMARY.json');check('run_completed','PASS',summary['status'])
    check('all_engine_probes_pass',True,all(p['passed'] for p in load(run/'ENGINE_PROBES.json')))
    check('all_graph_missing_controls',True,all(p['passed'] and p['actual_max_abs_prediction_difference']<=1e-8 for p in load(run/'CONTROL_EQUIVALENCE.json')))
    audits=read(run/'TIME_PERMISSION_AUDIT.csv');check('actual_queries',3600,len(audits))
    for row in audits:
        for key in ['early_observed_at','early_available_at','feature_actual_available_at','graph_relation_max_observed','graph_relation_max_available','event_max_observed','event_max_available']:
            if row[key]:check('time:'+row['sample_id']+':'+key,True,int(row[key])<=int(row['prediction_at']))
    installations=0;ledger_checks=0;graph_checks=0
    for path in sorted((run/'data').glob('*/*/GENERATED_INSTALLS_WITH_TRUTH.json')):
        folder=path.parent;rows=load(path);features=load(folder/'FEATURE_ROWS.json');byevent=collections.defaultdict(list)
        for event in load(folder/'CASHFLOW_LEDGER.json'):byevent[event['sample_id']].append(event)
        check('feature_order:'+str(folder.relative_to(run)),[r['sample_id'] for r in rows],[r['sample_id'] for r in features])
        groups=[{r['owner_unit'] for r in rows if r['split']==stage} for stage in ['train','validation','test']]
        check('owner_disjoint:'+str(folder.relative_to(run)),True,all(not groups[a]&groups[b] for a,b in [(0,1),(0,2),(1,2)]))
        for row,f in zip(rows,features):
            installations+=1
            for h in [1,7,30]:
                cash=[e for e in byevent[row['sample_id']] if row['install_at']<=e['occurred_at']<row['install_at']+h*DAY]
                check('cash_label:'+row['sample_id']+':'+str(h),True,abs(row[f'label_D{h}']-sum(e['amount_micros'] for e in cash)/1e6)<1e-9)
                check('label_available:'+row['sample_id']+':'+str(h),True,all(e['available_at']<=row[f'mature_D{h}'] for e in cash));ledger_checks+=1
            if f['graph_available']:
                import math
                expected=math.log1p((row['history_gross_micros']-row['history_refund_micros'])/1e6)
                check('mvp_feature_amount:'+row['sample_id'],True,abs(expected-f['graph_log_history'])<1e-10);graph_checks+=1
            if row['shared_device']:check('shared_device_rejected:'+row['sample_id'],'SHARED_DEVICE_ACCOUNT_AMBIGUITY',f['graph_gate_reason'])
        check('maturity_gates:'+str(folder.relative_to(run)),True,all(x['status']=='GO_SYNTHETIC_ONLY' for x in load(folder/'LABEL_MATURITY.json')))
        check('future_injection:'+str(folder.relative_to(run)),'FUTURE_INFORMATION_BLOCKED',load(folder/'BLOCKED_FUTURE_FEATURE.json')['decision'])
        check('immature_rejection:'+str(folder.relative_to(run)),'STOP',load(folder/'IMMATURE_LABEL_REJECTION.json')['status'])
    selection=load(run/'MODEL_SELECTION_AND_PARAMETERS.json');ids={}
    for row in selection:
        key=(row['world'],row['seed'],row['horizon']);value=[row[x] for x in ['same_train_ids','same_validation_ids','same_test_ids']]
        if key in ids:check('same_ids:'+str(key)+row['variant'],ids[key],value)
        else:ids[key]=value
        check('equal_trials:'+str(key)+row['variant'],4,len(row['trials']))
        check('trial_budget:'+str(key)+row['variant'],True,all(t['train_rows']==180 and t['validation_rows']==90 for t in row['trials']))
    pred=read(run/'PREDICTIONS.csv');labels={}
    for row in pred:
        key=(row['world'],row['seed'],row['horizon'],row['sample_id']);v=float(row['label'])
        if key in labels and labels[key]!=v:check('same_label:'+str(key),labels[key],v)
        labels[key]=v
    check('unique_test_labels',2700,len(labels));check('prediction_rows',32400,len(pred))
    # Reconstruct every stored forecast from the recorded fitted parameters,
    # without refitting or reading a test label for model selection.
    pred_by=collections.defaultdict(list)
    for row in pred:pred_by[(row['world'],int(row['seed']),int(row['horizon']),row['variant'])].append(row)
    cached={}
    for row in selection:
        dataset=(row['world'],row['seed']);key=(*dataset,row['horizon'],row['variant'])
        if dataset not in cached:
            folder=run/'data'/row['world']/str(row['seed'])
            cached[dataset]=(load(folder/'FEATURE_ROWS.json'),load(folder/'COUNTERFACTUAL_GRAPH_INPUTS.json'))
        feature_rows,inputs=cached[dataset];variant=row['variant'];m=variant if variant in ['M0','M1'] else 'M2'
        ablation=inputs.get(variant);x=matrix(feature_rows,m,
            graph_values=ablation['value'] if ablation else None,graph_available=ablation['available'] if ablation else None)
        tr=[i for i,r in enumerate(feature_rows) if r['split']=='train'];te=[i for i,r in enumerate(feature_rows) if r['split']=='test']
        actual_state=scale_fit(x[tr]);state=row['fit_state']
        for saved,calculated in [('medians','median'),('means','mean'),('stds','std')]:
            check('train_only:'+str(key)+saved,True,bool(np.allclose(state[saved],actual_state[calculated],rtol=0,atol=1e-12)))
        filled=np.where(np.isfinite(x),x,np.asarray(state['medians']))
        a=np.c_[np.ones(len(x)),(filled-np.asarray(state['means']))/np.asarray(state['stds'])]
        forecast=np.maximum(0,np.exp(np.clip(a@np.asarray(state['beta']),-40,40))*state['smearing']-1)[te]
        observed=np.asarray([float(r['prediction']) for r in pred_by[key]])
        check('reconstructed_forecast:'+str(key),True,bool(np.allclose(forecast,observed,rtol=1e-12,atol=1e-9)))
    for row in read(run/'MODEL_METRICS.csv'):
        key=(row['world'],int(row['seed']),int(row['horizon']),row['variant']);pp=pred_by[key]
        actual=metrics(np.asarray([float(x['label']) for x in pp]),np.asarray([float(x['prediction']) for x in pp]))
        for name,value in actual.items():
            check('recomputed_metric:'+str(key)+name,True,(row[name]=='' if value is None else abs(float(row[name])-value)<1e-9))
    unit=load(ROOT/'results/unit-tests/SUMMARY.json');check('unit_test_status','PASS',unit['status'])
    for path,h in unit['sources'].items():check('unit_test_source:'+path,h,sha(ROOT/path))
    check('counterexamples',10,len(load(run/'TEN_COUNTEREXAMPLES.json')))
    failures=[c for c in checks if not c['passed']]
    save(ROOT/'DELIVERY_VERIFICATION.json',dict(status='FAIL' if failures else 'PASS',run=run.relative_to(ROOT).as_posix(),
        verified_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),prior_files_checked=len(base),installations=installations,
        cashflow_label_checks=ledger_checks,actual_graph_amount_checks=graph_checks,checks=len(checks),failures=failures,checks_detail=checks))
    print(dict(status='FAIL' if failures else 'PASS',prior_files=len(base),checks=len(checks),failures=len(failures)))
    if failures:raise SystemExit(1)

if __name__=='__main__':main()
