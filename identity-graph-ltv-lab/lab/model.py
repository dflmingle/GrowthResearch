"""Small transparent ridge baseline, equal grid/training rows for M0/M1/M2."""
import numpy as np
def matrix(rows,model,graph_values=None,graph_available=None):
    values=[]
    for i,r in enumerate(rows):
        x=[float(r['country']==j) for j in range(4)]+[r['platform'],r['context_score']]
        if model in ['M1','M2']:x += [np.log1p(r['early_sessions']),r['early_engagement']]
        if model=='M2':
            v=r['graph_log_history'] if graph_values is None else graph_values[i]
            present=r['graph_available'] if graph_available is None else graph_available[i]
            x += [float(v) if v is not None and present else float('nan'),float(present)]
        values.append(x)
    return np.asarray(values,dtype=float)
def scale_fit(x):
    median=[]
    for col in x.T:
        valid=col[np.isfinite(col)];median.append(float(np.median(valid)) if len(valid) else 0.)
    median=np.asarray(median);filled=np.where(np.isfinite(x),x,median);mean=filled.mean(0);std=filled.std(0);std[std<1e-12]=1.
    return dict(median=median,mean=mean,std=std)
def scale(x,state):
    filled=np.where(np.isfinite(x),x,state['median']);return np.c_[np.ones(len(x)),(filled-state['mean'])/state['std']]
def fit_predict(x,y,split,grid):
    train=np.asarray([s=='train' for s in split]);val=np.asarray([s=='validation' for s in split]);test=np.asarray([s=='test' for s in split])
    state=scale_fit(x[train]);a=scale(x,state);target=np.log1p(y[train]);trials=[];best=None
    for alpha in grid:
        penalty=np.eye(a.shape[1])*alpha;penalty[0,0]=0
        beta=np.linalg.solve(a[train].T@a[train]+penalty,a[train].T@target)
        residual=target-a[train]@beta;smearing=float(np.mean(np.exp(residual)))
        pred=np.maximum(0,np.exp(np.clip(a@beta,-40,40))*smearing-1)
        loss=float(np.mean(np.abs(pred[val]-y[val])))
        trials.append(dict(alpha=alpha,validation_MAE=loss,train_rows=int(train.sum()),validation_rows=int(val.sum()),columns=x.shape[1]))
        if best is None or loss<best[0]:best=(loss,alpha,pred,beta,smearing)
    return dict(predictions=best[2],chosen_alpha=best[1],trials=trials,
        fit_state=dict(medians=state['median'].tolist(),means=state['mean'].tolist(),stds=state['std'].tolist(),beta=best[3].tolist(),smearing=best[4]),
        train_indices=np.flatnonzero(train).tolist(),validation_indices=np.flatnonzero(val).tolist(),test_indices=np.flatnonzero(test).tolist())
def metrics(y,p):
    error=p-y;n=len(y);k=max(1,int(np.ceil(n*.1)));top_true=np.argsort(-y,kind='stable')[:k];top_pred=np.argsort(-p,kind='stable')[:k]
    total=float(y.sum())
    return dict(MAE=float(np.abs(error).mean()),RMSE=float(np.sqrt(np.mean(error**2))),median_AE=float(np.median(np.abs(error))),
        mean_prediction=float(p.mean()),mean_actual=float(y.mean()),total_prediction_ratio=float(p.sum()/total) if total else None,
        Recall_at_10pct=float(len(set(top_true)&set(top_pred))/k),Top10pct_value_capture=float(y[top_pred].sum()/total) if total else None,
        observed_zero_fraction=float(np.mean(y==0)),samples=n)
