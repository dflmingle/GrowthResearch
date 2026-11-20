"""Read-only imports; all new writes belong to E02 run directories."""
import sys
sys.dont_write_bytecode = True
from pathlib import Path
import hashlib, json, csv
ROOT = Path(__file__).resolve().parent
PARENT = ROOT.parent
sys.path.insert(0, str(PARENT/'identity-graph-e01'))
from adapter import TaskAwareAdapter
from identity_mvp.fixtures import SyntheticWorld
from identity_mvp.system import PURPOSE, ENV, Rejected, ManualClock, canonical, digest
# E01's common module prepends its own dependency paths. Restore E02 precedence
# so our independent fixtures module cannot accidentally resolve to E01's file.
sys.path.insert(0, str(ROOT))
SEED = 780241

def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()

def save(path, value):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')

def load(path):return json.loads(Path(path).read_text(encoding='utf-8-sig'))

def csvsave(path, rows):
    with Path(path).open('w',encoding='utf-8-sig',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)

def preservation():
    baseline=load(ROOT/'PRESERVATION_BASELINE.json')
    return dict(checked=len(baseline),mismatches=[p for p,h in baseline.items() if not (PARENT/p).is_file() or sha(PARENT/p)!=h])
