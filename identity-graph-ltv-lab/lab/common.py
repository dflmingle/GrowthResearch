from pathlib import Path
import csv,hashlib,json,sys,random
ROOT=Path(__file__).resolve().parent.parent
MVP=ROOT.parent/'identity-graph-mvp'
# Prevent creation/modification of __pycache__ in the read-only reused MVP tree.
sys.dont_write_bytecode=True
sys.path.insert(0,str(MVP))
from identity_mvp.system import PURPOSE,Rejected,ENV,IdentitySystem,ManualClock
from identity_mvp.fixtures import SyntheticWorld
DAY=86400
BASE=1767225600
def load(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def save(p,x):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def csvsave(p,rows):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
    if not rows:return
    with p.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def to_time(clock,t):
    if t<clock.now:raise ValueError('Synthetic clock rewind forbidden')
    clock.advance(t-clock.now)
def performance_mode(world):
    # Only LAB-owned databases. This is not a durability/backup experiment.
    for c in [world.system.store.db,world.system.store.control]:
        c.execute('PRAGMA journal_mode=MEMORY');c.execute('PRAGMA synchronous=OFF')
class LabWorld(SyntheticWorld):
    """Only configures the reused fixture's initial clock/storage; no identity rules."""
    def __init__(self,directory,seed,start):
        self.seed=seed;self.rng=random.Random(seed);self.key=hashlib.sha256(f'public-fixture-{seed}'.encode()).digest()
        self.system=IdentitySystem(directory,clock=ManualClock(start),fixture_key=self.key)
        self.entities={};self.counter=0;self.start=start;performance_mode(self)
def guard_feature(observed_at,available_at,predicted_at):
    if any(type(x) is not int for x in [observed_at,available_at,predicted_at]):return 'INVALID_TIME'
    return 'ALLOW' if observed_at<=predicted_at and available_at<=predicted_at else 'FUTURE_INFORMATION_BLOCKED'
