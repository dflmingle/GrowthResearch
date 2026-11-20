from pathlib import Path
import hashlib,json,shutil

R=Path(__file__).resolve().parent.parent;D=R/'engineering76'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert not (D/'HISTORY_BEFORE.json').exists(),'Baseline exists;do not replace'
h={p.name:sha(p) for p in R.iterdir() if p.is_file() and p.name[:2].isdigit() and int(p.name[:2])<=75}
for rel in ['EVIDENCE_INDEX.md','prediction-system/EVIDENCE_GRAPH.json']:h[rel]=sha(R/rel)
save(D/'HISTORY_BEFORE.json',h)
shutil.copyfile(R/'EVIDENCE_INDEX.md',D/'EVIDENCE_INDEX.before.md')
shutil.copyfile(R/'prediction-system/EVIDENCE_GRAPH.json',D/'EVIDENCE_GRAPH.before.json')
g=json.loads((D/'EVIDENCE_GRAPH.before.json').read_text('utf-8'))
ids=['BB75S01','BB75S02','BB75S11','BB75S12','BB75S13','BB75S14','BB75S15','BB75S16','IV74S01','IV74S02','IV74S04','IV74S05','IV74S09','IG72S05','MA60S17']
reuse=[next(x for x in g['sources'] if x['id']==sid) for sid in ids]
for x in reuse:assert sha(R/x['path'])==x['sha256']
save(D/'REUSED_EVIDENCE.json',reuse)
print(json.dumps(dict(historical_files=len(h)-2,reused=len(reuse))))
