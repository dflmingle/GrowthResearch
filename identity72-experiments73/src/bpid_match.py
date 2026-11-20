"""BPID synthetic-profile matching baselines. Never links to a real external person."""
from pathlib import Path
import json,zipfile,hashlib,re,unicodedata,time
from difflib import SequenceMatcher
import numpy as np
import pandas as pd
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score,recall_score,f1_score,roc_auc_score,average_precision_score

R=Path(__file__).resolve().parents[1];OUT=R/'results';FIELDS=['fullname','email','phone','addr','dob']
def canon(v):
    if isinstance(v,list):return sorted(set(canon(x) for x in v if canon(x)))
    return re.sub(r'\s+',' ',unicodedata.normalize('NFKC',str(v)).strip().lower())
def hprofile(p):return hashlib.sha256(json.dumps({k:canon(p[k]) for k in FIELDS},sort_keys=True).encode()).hexdigest()
class UF:
    def __init__(self):self.p={}
    def find(self,x):
        self.p.setdefault(x,x)
        if self.p[x]!=x:self.p[x]=self.find(self.p[x])
        return self.p[x]
    def union(self,a,b):
        a=self.find(a);b=self.find(b)
        if a!=b:self.p[b]=a
def vals(v):return v if isinstance(v,list) else ([v] if v else [])
def feature(a,b):
    out=[]
    for k in FIELDS:
        aa=vals(canon(a[k]));bb=vals(canon(b[k]));present=bool(aa and bb)
        exact=int(bool(set(aa)&set(bb)))
        seq=max((SequenceMatcher(None,x,y,autojunk=False).ratio() for x in aa for y in bb),default=0)
        jac=max((len(set(x.split())&set(y.split()))/max(1,len(set(x.split())|set(y.split()))) for x in aa for y in bb),default=0)
        out += [exact,seq,jac,int(not aa),int(not bb),int(present)]
    return out
def array(pairs):return np.asarray([feature(x['profile1'],x['profile2']) for x in pairs],dtype=float)
def threshold(y,s):
    cand=np.unique(np.r_[0,np.linspace(0,1,101),s,1.000001])
    return max(cand,key=lambda t:(f1_score(y,s>=t,zero_division=0),t))
def metrics(y,s,t):
    p=s>=t;tp=int(np.sum(p&(y==1)));fp=int(np.sum(p&(y==0)));tn=int(np.sum((~p)&(y==0)))
    return dict(precision=float(precision_score(y,p,zero_division=0)),recall=float(recall_score(y,p,zero_division=0)),f1=float(f1_score(y,p,zero_division=0)),roc_auc=float(roc_auc_score(y,s)),pr_auc=float(average_precision_score(y,s)),false_merge_rate=float(fp/(tp+fp)) if tp+fp else None,false_positive_rate=float(fp/(fp+tn)) if fp+tn else None,tp=tp,fp=fp,tn=tn,predicted_merges=int(p.sum()))
def mutate(pairs,missing,noise,seed):
    rng=np.random.default_rng(seed);xs=json.loads(json.dumps(pairs))
    for x in xs:
      for side in ['profile1','profile2']:
       for key in FIELDS:
        v=x[side][key]
        if rng.random()<missing:x[side][key]=[] if isinstance(v,list) else '';continue
        def change(s):
            chars=list(str(s))
            for i,c in enumerate(chars):
                if c.isalnum() and rng.random()<noise:chars[i]='x' if c!='x' else 'y'
            return ''.join(chars)
        x[side][key]=[change(q) for q in v] if isinstance(v,list) else change(v)
    return xs
def bootstrap_f1(y,p,groups,seed):
    ids=np.unique(groups);indices=[np.where(groups==g)[0] for g in ids];rng=np.random.default_rng(seed);v=[]
    for _ in range(200):
        ix=np.concatenate([indices[i] for i in rng.integers(0,len(ids),len(ids))]);v.append(f1_score(y[ix],p[ix],zero_division=0))
    return [float(x) for x in np.quantile(v,[.025,.975])]
def main():
    assert not (OUT/'B_RESULTS.csv').exists(),'Do not overwrite results'
    start=time.time();arch=R/'sources/BPID.zip'
    with zipfile.ZipFile(arch) as z:xs=[json.loads(s) for s in z.read('data_release/matching_dataset.jsonl').decode().splitlines()]
    y=np.array([{'True':1,'False':0}[x['match']] for x in xs]);left=[hprofile(x['profile1']) for x in xs];right=[hprofile(x['profile2']) for x in xs]
    uf=UF()
    for a,b in zip(left,right):uf.union(a,b)
    groups=np.array([uf.find(x) for x in left]);unique=np.unique(groups);rng=np.random.default_rng(7301);order=rng.permutation(unique)
    n=len(order);trainset=set(order[:int(.6*n)]);valset=set(order[int(.6*n):int(.8*n)]);testset=set(order[int(.8*n):]);splits=[np.where(np.isin(groups,list(s)))[0] for s in [trainset,valset,testset]]
    tr,va,te=splits;assert all(len(np.unique(y[ix]))==2 for ix in splits)
    endpoints=[set(left[i] for i in ix)|set(right[i] for i in ix) for ix in splits]
    assert all(not endpoints[i]&endpoints[j] for i in range(3) for j in range(i+1,3))
    audit=dict(rows=len(xs),positive=int(y.sum()),negative=int((1-y).sum()),synthetic=True,licence='Apache-2.0 per official Zenodo metadata',groups=len(unique),largest_component_pairs=int(max(np.sum(groups==v) for v in unique)),unique_endpoint_profiles=len(set(left+right)),exact_duplicate_pair_rows=len(xs)-len(set(zip(left,right))),split_rows=[len(i) for i in splits],split_positives=[int(y[i].sum()) for i in splits],shared_endpoint_leakage=0,unobserved_latent_profile_relatedness='UNKNOWN:no hidden entity lineage;canonical exact endpoint groups isolated',missing_field_fraction={k:float(np.mean([not bool(x[s][k]) for x in xs for s in ['profile1','profile2']])) for k in FIELDS},source_zip_sha256=hashlib.sha256(arch.read_bytes()).hexdigest())
    (OUT/'B_DATA_AUDIT.json').write_text(json.dumps(audit,indent=2),encoding='utf-8')
    np.savez_compressed(OUT/'B_SPLIT_INDICES.npz',train=tr,validation=va,test=te)
    x=array(xs);lr=make_pipeline(StandardScaler(),LogisticRegression(C=1,max_iter=1000,random_state=7301));rf=RandomForestClassifier(n_estimators=200,max_depth=8,min_samples_leaf=10,random_state=7301,n_jobs=2)
    lr.fit(x[tr],y[tr]);rf.fit(x[tr],y[tr])
    def scores(xx):
        shape=xx.reshape(len(xx),5,6);present=shape[:,:,5];count=present.sum(axis=1)
        exact=((shape[:,:,0]*present).sum(axis=1)==count)&(count>=2)
        sim=(shape[:,:,1]*present).sum(axis=1)/np.maximum(count,1)
        return dict(exact=exact.astype(float),similarity_score=sim,logistic=lr.predict_proba(xx)[:,1],random_forest=rf.predict_proba(xx)[:,1])
    val=scores(x[va]);thresholds={k:(.5 if k=='exact' else float(threshold(y[va],v))) for k,v in val.items()};thresholds['graph_closure']=thresholds['random_forest']
    rows=[]
    for missing,noise in [(0,0),(.1,0),(.3,0),(.5,0),(0,.05),(0,.1),(0,.2)]:
        xx=x[te] if missing==0 and noise==0 else array(mutate([xs[i] for i in te],missing,noise,7302))
        sc=scores(xx);gr=UF()
        for j,i in enumerate(te):
            if sc['random_forest'][j]>=thresholds['random_forest']:gr.union(left[i],right[i])
        closure=np.array([float(gr.find(left[i])==gr.find(right[i])) for i in te]);sc['graph_closure']=closure
        for name,s in sc.items():
            t=.5 if name=='graph_closure' else thresholds[name];met=metrics(y[te],s,t)
            lo,hi=bootstrap_f1(y[te],s>=t,groups[te],7303)
            rows.append(dict(experiment='B',data_type='BPID_SYNTHETIC_HUMAN_ANNOTATED',model=name,extra_missing_probability=missing,character_corruption_probability=noise,threshold=t,test_n=len(te),f1_ci_low=lo,f1_ci_high=hi,**met))
    pd.DataFrame(rows).to_csv(OUT/'B_RESULTS.csv',index=False,encoding='utf-8-sig')
    (OUT/'B_RUN.json').write_text(json.dumps(dict(protocol_sha256=hashlib.sha256((R/'PREREGISTRATION.md').read_bytes()).hexdigest(),thresholds=thresholds,rows=len(rows),seconds=time.time()-start,models='Fixed preregistered baselines;no test tuning',graph_limit='Transitive closure on provided candidate graph only;unlabeled pairs not evaluated',auc_limit='Graph closure and exact give binary scores,not calibrated probabilities'),indent=2),encoding='utf-8')
    print(json.dumps(dict(status='PASS',rows=len(rows),split=audit['split_rows'],seconds=time.time()-start)))
if __name__=='__main__':main()
