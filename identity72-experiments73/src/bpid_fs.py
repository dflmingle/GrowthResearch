from pathlib import Path
import zipfile,json,time,hashlib
import numpy as np
import pandas as pd
from bpid_match import array,threshold,metrics,mutate,bootstrap_f1,UF,hprofile
R=Path(__file__).resolve().parents[1];O=R/'results'
def states(x):
    x=x.reshape(len(x),5,6);s=np.where(x[:,:,1]<.5,1,np.where(x[:,:,1]<.8,2,3))
    s=np.where(x[:,:,0]>0,4,s);return np.where(x[:,:,5]==0,0,s).astype(int)
def main():
    assert not (O/'B_FS_RESULTS.csv').exists()
    with zipfile.ZipFile(R/'sources/BPID.zip') as z:xs=[json.loads(s) for s in z.read('data_release/matching_dataset.jsonl').decode().splitlines()]
    y=np.array([x['match']=='True' for x in xs],dtype=int);split=np.load(O/'B_SPLIT_INDICES.npz');tr=split['train'];va=split['validation'];te=split['test']
    x=array(xs);train=states(x[tr]);probs=np.zeros((2,5,5))
    for cl in [0,1]:
        for f in range(5):
            count=np.bincount(train[y[tr]==cl,f],minlength=5)+1;probs[cl,f]=count/count.sum()
    prior=(y[tr].sum()+1)/(len(tr)+2)
    def score(xx):
        st=states(xx);logit=np.full(len(xx),np.log(prior/(1-prior)))
        for f in range(5):logit+=np.log(probs[1,f,st[:,f]]/probs[0,f,st[:,f]])
        return 1/(1+np.exp(-np.clip(logit,-40,40)))
    t=threshold(y[va],score(x[va]));uf=UF();left=[hprofile(z['profile1']) for z in xs];right=[hprofile(z['profile2']) for z in xs]
    for a,b in zip(left,right):uf.union(a,b)
    groups=np.array([uf.find(v) for v in left]);rows=[]
    for missing,noise in [(0,0),(.1,0),(.3,0),(.5,0),(0,.05),(0,.1),(0,.2)]:
        xx=x[te] if missing==0 and noise==0 else array(mutate([xs[i] for i in te],missing,noise,7302));s=score(xx);lo,hi=bootstrap_f1(y[te],s>=t,groups[te],7303)
        rows.append(dict(experiment='B',data_type='BPID_SYNTHETIC_HUMAN_ANNOTATED',model='fellegi_sunter_independent',extra_missing_probability=missing,character_corruption_probability=noise,threshold=float(t),test_n=len(te),f1_ci_low=lo,f1_ci_high=hi,**metrics(y[te],s,t)))
    pd.DataFrame(rows).to_csv(O/'B_FS_RESULTS.csv',index=False,encoding='utf-8-sig')
    (O/'B_FS_RUN.json').write_text(json.dumps(dict(amendment_sha256=hashlib.sha256((R/'PROTOCOL_AMENDMENT_FS.md').read_bytes()).hexdigest(),prior=prior,threshold=float(t),conditional_probs=probs.tolist(),test_tuning=False),indent=2),encoding='utf-8');print('FS PASS',len(rows))
if __name__=='__main__':main()
