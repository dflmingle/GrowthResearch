"""Read-only imports of the existing synthetic MVP and lab adapter."""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import hashlib,json,csv
ROOT=Path(__file__).resolve().parent
PARENT=ROOT.parent
sys.path.insert(0,str(PARENT/'identity-graph-mvp'))
sys.path.insert(0,str(PARENT/'identity-graph-ltv-lab'))
from identity_mvp.system import PURPOSE,ENV,Rejected
from identity_mvp.fixtures import SyntheticWorld
from lab.adapter import GraphAdapter
SEED=780241
def save(path,value):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
def load(path):return json.loads(Path(path).read_text(encoding='utf-8-sig'))
def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()
def csvsave(path,rows):
    with Path(path).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
