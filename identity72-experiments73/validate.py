"""Validate current artifacts, immutable history and experiment accounting;no fitting."""
from pathlib import Path
import datetime, hashlib, json, re, zipfile, unicodedata
import numpy as np
import pandas as pd

R = Path(__file__).resolve().parent.parent
D = R / 'identity72-experiments73'
V = D / 'VALIDATION.json'
checks = []

def read(p):
    return json.loads(p.read_text(encoding='utf-8-sig'))

def sha(p, algorithm='sha256'):
    h = hashlib.new(algorithm)
    with p.open('rb') as f:
        for b in iter(lambda: f.read(1024*1024), b''):
            h.update(b)
    return h.hexdigest()

def save(p, x):
    p.write_text(json.dumps(x, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

def check(name, condition, detail=''):
    checks.append(dict(name=name, pass_check=bool(condition), detail=detail))
    if not condition:
        raise AssertionError(name + ': ' + str(detail))

def main():
    save(V,dict(status='RUNNING',started_utc=datetime.datetime.now(datetime.timezone.utc).isoformat()))
    history=read(D/'HISTORY_BEFORE.json')
    old=read(D/'EVIDENCE_GRAPH.before.json')
    g=read(R/'prediction-system/EVIDENCE_GRAPH.json')
    for rel,digest in history.items():
        if rel not in ['EVIDENCE_INDEX.md','prediction-system/EVIDENCE_GRAPH.json']:
            check('Historical file unchanged: '+rel,sha(R/rel)==digest)
    check('Old graph snapshot matches baseline hash',sha(D/'EVIDENCE_GRAPH.before.json')==history['prediction-system/EVIDENCE_GRAPH.json'])
    check('Old index snapshot matches baseline hash',sha(D/'EVIDENCE_INDEX.before.md')==history['EVIDENCE_INDEX.md'])
    check('Index only appended',(R/'EVIDENCE_INDEX.md').read_bytes().startswith((D/'EVIDENCE_INDEX.before.md').read_bytes()))
    for k,v in old.items():
        check('Graph original section preserved: '+k, g[k][:len(v)]==v if k in ['nodes','edges','sources'] else g[k]==v)
    for k in ['nodes','edges','sources']:
        check(k+' IDs unique',len({x['id'] for x in g[k]})==len(g[k]))
    nn=g['nodes'][len(old['nodes']):];ne=g['edges'][len(old['edges']):];ns=g['sources'][len(old['sources']):]
    nids={x['id'] for x in g['nodes']};sids={x['id'] for x in g['sources']}
    check('New edge references valid',all(x['source'] in nids and x['target'] in nids and set(x['source_ids'])<=sids for x in ne))
    check('New evidence has no E5/E6',all(not set(x.get('identity_evidence_stages',x.get('evidence_stages',[])))&{'E5','E6'} for x in ne+ns))
    check('No production identity match/model claim',all(x.get('production_match_proven') is False and x.get('prediction_model_consumption_proven') is False for x in ne+ns))
    ident=read(R/'72_跨应用身份关联证据图.json')
    ins={x['id'] for x in ident['sources']};inn={x['id'] for x in ident['nodes']}
    check('Identity graph self-contained',all(x['source'] in inn and x['target'] in inn and set(x['source_ids'])<=ins for x in ident['edges']))
    check('Identity graph contains no real identity values',all(x['contains_real_identity_values'] is False for x in ident['nodes']))
    check('Standalone/main identity edges agree',ident['edges']==[x for x in ne if x['id'].startswith('IG72')])
    for x in ns+read(D/'REUSED_EVIDENCE.json'):
        check('Source SHA256: '+x['id'],sha(R/x['path'])==x['sha256'])
        if 'text_path' in x:
            check('Source text SHA256: '+x['id'],sha(R/x['text_path'])==x['text_sha256'])
    for x in read(D/'CODE_EVIDENCE.json')+read(D/'SOURCE_EVIDENCE.json'):
        p=R/x.get('text_path',x['path']);ls=p.read_text('utf-8').splitlines()
        expected='\n'.join(f'{i+1}: {s}' for i,s in enumerate(ls) if x['start_line']<=i+1<=x['end_line'])
        check('Exact line excerpt: '+x['id'],expected==x['excerpt'])
        for pkg in x.get('original_packages',[])+x.get('original_jars',[]):
            check('Original SDK archive: '+x['id']+' '+pkg['path'],sha(R/pkg['path'])==pkg['sha256'])
    for x in read(D/'PIXEL_EVIDENCE.json'):
        s=(R/x['path']).read_text('utf-8');a=x['offset_start']
        check('Pixel exact offset: '+x['id'],s[a:a+len(x['excerpt'])]==x['excerpt'])
    arcs=read(D/'ARCHIVE_INVENTORY.json')
    check('Reused SDK archive counts',sum(x['type']=='AAR' for x in arcs)==103 and sum(x['type']=='sources.jar' for x in arcs)==67)
    check('All reused archive hashes unchanged',all(sha(R/x['path'])==x['sha256'] for x in arcs))
    for x in read(D/'FETCH_MANIFEST.json'):
        if x.get('status')==200:
            check('Public fetch original/text: '+x['id'],sha(R/x['path'])==x['sha256'] and sha(R/x['text_path'])==x['text_sha256'])
    audit=read(D/'BPID_ARCHIVE_AUDIT.json');zp=R/audit['path']
    check('BPID complete size/SHA256/MD5',zp.stat().st_size==58115842 and sha(zp)==audit['sha256'] and sha(zp,'md5')==audit['md5']==audit['published_checksum'].split(':')[1])
    with zipfile.ZipFile(zp) as z:
        check('BPID ZIP CRC',z.testzip() is None)
        rows=[json.loads(s) for s in z.read('data_release/matching_dataset.jsonl').decode('utf-8').splitlines()]
    check('BPID actual pairs and labels',len(rows)==10000 and set(x['match'] for x in rows)=={'True','False'} and sum(x['match']=='True' for x in rows)==4333)
    # Independently reconstruct canonical endpoint intersections, without displaying profiles.
    def canonical(x):
        def norm(v):
            if isinstance(v,list):return sorted(set(norm(t) for t in v if norm(t)))
            return re.sub(r'\s+',' ',unicodedata.normalize('NFKC',str(v)).strip().lower())
        p={k:norm(x[k]) for k in ['fullname','email','phone','addr','dob']}
        return hashlib.sha256(json.dumps(p,sort_keys=True).encode()).hexdigest()
    endpoints=[(canonical(x['profile1']),canonical(x['profile2'])) for x in rows]
    split=np.load(D/'results/B_SPLIT_INDICES.npz')
    idx=[split[k] for k in ['train','validation','test']]
    check('B split sizes and complete disjoint coverage',[len(x) for x in idx]==[6000,2000,2000] and len(set(np.concatenate(idx)))==10000)
    sets=[{p for i in xx for p in endpoints[i]} for xx in idx]
    check('No exact endpoint leakage',not (sets[0]&sets[1] or sets[0]&sets[2] or sets[1]&sets[2]))
    check('B 20000 isolated canonical endpoints',len(set(p for q in endpoints for p in q))==20000)
    b=pd.concat([pd.read_csv(D/'results/B_RESULTS.csv'),pd.read_csv(D/'results/B_FS_RESULTS.csv')],ignore_index=True)
    check('B 42 synthetic metric rows',len(b)==42 and (b['test_n']==2000).all() and (b['data_type']=='BPID_SYNTHETIC_HUMAN_ANNOTATED').all())
    probcols=['precision','recall','f1','roc_auc','pr_auc','false_positive_rate','f1_ci_low','f1_ci_high']
    check('B metric ranges finite',np.isfinite(b[probcols].to_numpy()).all() and ((b[probcols]>=0)&(b[probcols]<=1)).all().all())
    check('B false merge definition',np.allclose(b['false_merge_rate'],b['fp']/b['predicted_merges'].replace(0,np.nan),equal_nan=True))
    nz=b.predicted_merges>0
    den=b.precision+b.recall
    calc_f1=np.divide(2*b.precision*b.recall,den,out=np.zeros(len(b)),where=den.to_numpy()!=0)
    check('B precision and F1',np.allclose(b.loc[nz,'precision'],1-b.loc[nz,'false_merge_rate']) and (b.loc[~nz,'precision']==0).all() and np.allclose(b['f1'],calc_f1))
    check('B counts and FPR',((b.tp+b.fp)==b.predicted_merges).all() and np.allclose(b.false_positive_rate,b.fp/(b.fp+b.tn)))
    rf=b[b.model=='random_forest'].sort_values(['extra_missing_probability','character_corruption_probability'])
    graph=b[b.model=='graph_closure'].sort_values(['extra_missing_probability','character_corruption_probability'])
    check('B graph/rf same pair decisions counts',np.array_equal(rf[['tp','fp','tn']].to_numpy(),graph[['tp','fp','tn']].to_numpy()))
    check('B thresholds fixed across stress',all(a.threshold.nunique()==1 for _,a in b.groupby('model')))
    check('B no protocol overwrite',sha(D/'PREREGISTRATION.md')==read(D/'results/B_RUN.json')['protocol_sha256'])
    check('B FS amendment frozen',sha(D/'PROTOCOL_AMENDMENT_FS.md')==read(D/'results/B_FS_RUN.json')['amendment_sha256'] and read(D/'results/B_FS_RUN.json')['test_tuning'] is False)
    t=pd.read_csv(D/'results/D_RESULTS.csv');agg=pd.read_csv(D/'results/D_AGGREGATE.csv');dc=read(D/'results/D_CHECKS.json')
    check('D all 360 rows and 120 aggregates',len(t)==360 and len(agg)==120 and (t.data_type=='SYNTHETIC_ONLY').all() and (t.test_n==3000).all())
    keys=['scenario','history_per_app_device','target_train_n','seed']
    check('D all 36 groups ten models',len(t.groupby(keys))==36 and (t.groupby(keys).size()==10).all())
    metrics=['mae','rmse','median_ae','recall_at_10','top10_amount_capture','total_bias','mae_delta_vs_A','mae_delta_vs_C','mae_delta_vs_A_ci_low','mae_delta_vs_A_ci_high']
    check('D all metrics finite',np.isfinite(t[metrics].to_numpy()).all())
    check('D metric bounds',(t[['mae','rmse','median_ae']]>=0).all().all() and (t.rmse>=t.mae).all() and ((t.recall_at_10>=0)&(t.recall_at_10<=1)).all() and ((t.top10_amount_capture>=0)&(t.top10_amount_capture<=1)).all())
    c=t[t.model=='C'].set_index(keys).sort_index();d0=t[t.model=='D_00'].set_index(keys).sort_index()
    check('D zero-error/oracle metric identity',np.array_equal(c[metrics].to_numpy(),d0[metrics].to_numpy()))
    check('D runtime assertions exact injected errors',dc['status']=='PASS' and len(dc['checks'])==180 and all(x['actual_wrong']==x['expected_wrong'] for x in dc['checks']) and all(x['zero_equals_oracle'] is True for x in dc['checks'] if x['rate']==0))
    check('D protocol/config frozen',dc['protocol_sha256']==sha(D/'PREREGISTRATION.md') and dc['config_sha256']==sha(D/'results/D_CONFIG.json'))
    primary=t[(t.history_per_app_device==8)&(t.target_train_n==2000)&(t.model=='C')]
    check('D individual conditional CI signs',len(primary[primary.scenario=='individual_signal'])==3 and (primary[primary.scenario=='individual_signal'].mae_delta_vs_A_ci_high<0).all())
    check('D reverse-history conditional CI signs',len(primary[primary.scenario=='source_shift'])==3 and (primary[primary.scenario=='source_shift'].mae_delta_vs_A_ci_low>0).all())
    for _,q in t.groupby(keys):
        a=q[q.model=='A'].iloc[0];cc=q[q.model=='C'].iloc[0]
        check('D paired delta accounting: '+str(tuple(a[k] for k in keys)),np.allclose(q.mae_delta_vs_A,q.mae-a.mae) and np.allclose(q.mae_delta_vs_C,q.mae-cc.mae) and q.zero_fraction.nunique()==1)
    means=t.groupby(['scenario','history_per_app_device','target_train_n','model']).mae.mean()
    observed=agg.set_index(['scenario','history_per_app_device','target_train_n','model']).mae_mean
    check('D aggregate reproduces all means',np.allclose(means.sort_index(),observed.sort_index()))
    summary=pd.read_csv(next(R.glob('73_*.csv')))
    check('Summary 404 rows and independent A/C STOP',len(summary)==404 and summary.groupby('experiment').size().to_dict()=={'A':1,'B':42,'C':1,'D':360})
    stops=summary[summary.experiment.isin(['A','C'])]
    check('STOP rows contain no fabricated metrics',stops[['mae','rmse','f1','roc_auc']].isna().all().all())
    delivery=sorted(p for p in R.glob('72_*') if p.is_file() and p.name not in history)+sorted(R.glob('73_*'))
    check('All 16 requested deliverables',len(delivery)==16)
    for p in delivery+[D/'README.md',D/'SOURCE_CATALOG.md']:
        if p.suffix!='.md':continue
        targets=re.findall(r'\[[^\]]*\]\(([^)]+)\)',p.read_text('utf-8'))
        for target in targets:
            target=target.strip('<>').split('#')[0]
            if not target or re.match(r'https?://|mailto:',target):continue
            check('Local report link: '+p.name+' -> '+target,(p.parent/target).exists())
    manifests=read(D/'RUN_MANIFEST.json')
    check('Declared prohibited runtime actions absent',all(manifests[k]==0 for k in ['new_sdk_downloads','sdk_runtime_tests','production_requests','real_identity_collection','real_cross_dataset_joins']), 'Artifact/log audit and declared run scope;not an independent packet capture')
    for proto,res in [('PREREGISTRATION.md','results/B_RESULTS.csv'),('PREREGISTRATION.md','results/D_RESULTS.csv'),('PROTOCOL_AMENDMENT_FS.md','results/B_FS_RESULTS.csv')]:
        check('Protocol before result: '+res,(D/proto).stat().st_mtime<=(D/res).stat().st_mtime)
    paths=delivery+[R/'EVIDENCE_INDEX.md',R/'prediction-system/EVIDENCE_GRAPH.json']
    paths+=list((D/'src').glob('*.py'))+list((D/'results').glob('*'))
    paths+=list(D.glob('*.py'))+[D/'PREREGISTRATION.md',D/'PROTOCOL_AMENDMENT_FS.md',D/'CODE_EVIDENCE.json',D/'SOURCE_EVIDENCE.json',D/'PIXEL_EVIDENCE.json',D/'README.md']
    manifest=[dict(path=p.relative_to(R).as_posix(),bytes=p.stat().st_size,sha256=sha(p),modified_utc=datetime.datetime.fromtimestamp(p.stat().st_mtime,datetime.timezone.utc).isoformat()) for p in sorted(set(paths)) if p.is_file()]
    save(D/'ARTIFACT_MANIFEST.json',manifest)
    result=dict(status='PASS',completed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),checks_passed=len(checks),checks=checks,
        immutable_historical_files=len(history)-2,new_deliverables=len(delivery),graph_counts={k:len(g[k]) for k in ['nodes','edges','sources']},
        limitations=['No model retraining in this validation','Synthetic benchmark only;no E5/E6','Endpoint split cannot exclude undisclosed latent family relation','No real device cross-dataset joins','Artifact/log audit is not independent network monitoring'],
        artifact_manifest_sha256=sha(D/'ARTIFACT_MANIFEST.json'))
    save(V,result)
    print(json.dumps({k:result[k] for k in ['status','checks_passed','immutable_historical_files','new_deliverables','graph_counts']},indent=2))

if __name__=='__main__':
    try:
        main()
    except Exception as e:
        save(V,dict(status='FAIL',error=repr(e),checks=checks))
        raise
