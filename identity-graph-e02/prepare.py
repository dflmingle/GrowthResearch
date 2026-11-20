"""Freeze the existing E01 baseline plus all E01 artifacts before E02 tests."""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import json,hashlib,datetime
ROOT=Path(__file__).resolve().parent
PARENT=ROOT.parent
def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()
def save(path,value):path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def main():
    if (ROOT/'PRESERVATION_BASELINE.json').exists():raise SystemExit('Refusing to replace preservation baseline')
    baseline=json.loads((PARENT/'identity-graph-e01/PRESERVATION_BASELINE.json').read_text(encoding='utf-8'))
    for name in ['identity-graph-e01','identity-graph-mvp','identity-graph-ltv-lab','axon-vector-mechanism-gap']:
        for path in (PARENT/name).rglob('*'):
            if path.is_file():baseline.setdefault(path.relative_to(PARENT).as_posix(),sha(path))
    missing=[p for p,h in baseline.items() if not (PARENT/p).is_file() or sha(PARENT/p)!=h]
    if missing:raise SystemExit('Prior integrity mismatch: '+repr(missing))
    save(ROOT/'PRESERVATION_BASELINE.json',baseline)
    paths=['identity-graph-mvp/identity_mvp/system.py','identity-graph-mvp/identity_mvp/fixtures.py',
        'identity-graph-mvp/identity_mvp/schema.sql','identity-graph-mvp/identity_mvp/control_schema.sql',
        'identity-graph-e01/adapter.py','identity-graph-e01/common.py','identity-graph-e01/README.md',
        'axon-vector-mechanism-gap/03_下一轮最小实验方案.md']
    save(ROOT/'REUSED_SOURCES.json',[dict(path=p,sha256=sha(PARENT/p)) for p in paths])
    save(ROOT/'PROTOCOL.json',dict(scope='E02_ONLY_LOCAL_SYNTHETIC',seed=780241,
        frozen_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        states=['QUEUED','CLAIMED','REVALIDATING','CANCELLED','LOCAL_ACK','RETRY_PENDING'],
        source='Original MVP outbox; immutable event and economic lineage refs',
        permission='Original policy+graph+E01 reread at claim/retry/pre-handoff; current read-only original checks under dual DB locks at memory acceptance',
        boundary='Single trusted thread, ManualClock, no callback/yield in critical section, exact built-in memory sink; memory insertion linearization only',
        unsupported='ATOMIC_HANDOFF_UNPROVEN for external/durable/restart/multiprocess claims or unestablished boundary',
        mutations=['enqueue_only','stale_retry_epoch','check_then_revoke_commit'],
        no_E03=True,no_training=True,no_network=True,no_sdk=True,no_real_data=True,
        C_graph_Axon='UNKNOWN',C_graph_Vector='UNKNOWN',D='UNKNOWN',production_forensics='STOP'))
    save(ROOT/'PROTOCOL_SHA256.json',dict(sha256=sha(ROOT/'PROTOCOL.json')))
    print(dict(protected_files=len(baseline),seed=780241,scope='E02_ONLY'))
if __name__=='__main__':main()
