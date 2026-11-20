"""Freeze prior files and E01-only protocol before executing test fixtures."""
from pathlib import Path
import hashlib,json,datetime
ROOT=Path(__file__).resolve().parent
PARENT=ROOT.parent
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def main():
    if (ROOT/'PRESERVATION_BASELINE.json').exists():raise SystemExit('Refusing to replace baseline')
    prior=json.loads((PARENT/'axon-vector-mechanism-gap/PRESERVATION_BASELINE.json').read_text(encoding='utf-8'))
    for name in ['axon-vector-mechanism-gap','identity-graph-mvp','identity-graph-ltv-lab']:
        for p in (PARENT/name).rglob('*'):
            if p.is_file():prior.setdefault(p.relative_to(PARENT).as_posix(),sha(p))
    bad=[p for p,h in prior.items() if not (PARENT/p).is_file() or sha(PARENT/p)!=h]
    if bad:raise SystemExit('Prior mismatch '+str(bad))
    save(ROOT/'PRESERVATION_BASELINE.json',prior)
    inputs=['identity-graph-mvp/identity_mvp/system.py','identity-graph-mvp/identity_mvp/schema.sql',
       'identity-graph-mvp/identity_mvp/control_schema.sql','identity-graph-mvp/identity_mvp/fixtures.py',
       'identity-graph-mvp/DATABASE_CONTRACTS.md','identity-graph-ltv-lab/lab/adapter.py',
       'identity-graph-ltv-lab/lab/common.py','axon-vector-mechanism-gap/03_下一轮最小实验方案.md',
       'axon-vector-mechanism-gap/EXPERIMENT_DESIGNS.json']
    save(ROOT/'REUSED_SOURCES.json',[dict(path=p,sha256=sha(PARENT/p)) for p in inputs])
    save(ROOT/'PROTOCOL.json',dict(scope='E01_LOCAL_SYNTHETIC_ONLY',seed=780241,
       frozen_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
       comparison=['A_existing_device_adapter','B_original_account_API','C_task_aware_adapter'],
       baseline_micros=dict(account_A_source_X=7000000,account_A_target_Y=3000000,account_B_source_X=99000000),
       receipt_semantics='Durable original resolver nonce receipt binds target installation/account/purpose; not raw account ID; assertion TTL is login-time proof, not invented session expiry',
       partition_semantics='Only read original account bundle approved ledger/event/edge/coverage refs by primary key; reconcile totals before partition; no all-ledger fallback',
       target_scope='Target App product namespace, not just target installation; same-product reinstalls stay target history',
       prediction_semantics='Current clock only; no backdated active feature availability',
       no_E02_E03=True,no_model_training=True,no_real_data=True,no_SDK=True,no_network=True,
       C_graph_Axon='UNKNOWN',C_graph_Vector='UNKNOWN',D='UNKNOWN',production_forensics='STOP'))
    save(ROOT/'PROTOCOL_HASH.json',dict(sha256=sha(ROOT/'PROTOCOL.json')))
    print(json.dumps(dict(protected_files=len(prior),seed=780241,scope='E01_ONLY')))
if __name__=='__main__':main()
