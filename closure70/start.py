from pathlib import Path
import json,hashlib,shutil
R=Path(__file__).resolve().parent.parent;D=R/'closure70'
(D/'sources').mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
paths=[p for p in R.iterdir() if p.is_file() and p.name[:2].isdigit() and int(p.name[:2])<=69]+[R/'EVIDENCE_INDEX.md',R/'prediction-system/EVIDENCE_GRAPH.json']
assert not (D/'HISTORY_BEFORE.json').exists(),'Round70 already initialized;do not reset baseline'
(D/'HISTORY_BEFORE.json').write_text(json.dumps({p.relative_to(R).as_posix():sha(p) for p in paths},ensure_ascii=False,indent=2),encoding='utf-8')
for src,name in [(R/'EVIDENCE_INDEX.md','EVIDENCE_INDEX.before.md'),(R/'prediction-system/EVIDENCE_GRAPH.json','EVIDENCE_GRAPH.before.json')]:shutil.copyfile(src,D/name)
print('saved',len(paths),'historical hashes')
