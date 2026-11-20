"""Freeze pre78 evidence and read the explicitly requested inputs. Offline only."""
from pathlib import Path
import csv, datetime, hashlib, json, shutil

R=Path(__file__).resolve().parent.parent
D=Path(__file__).resolve().parent
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):
    assert not p.exists(),p
    p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

assert not (D/'HISTORY_BEFORE.json').exists(),'Never replace the frozen pre78 baseline'
h={p.name:sha(p) for p in R.iterdir() if p.is_file() and p.name[:2].isdigit() and int(p.name[:2])<=77}
for path in ['EVIDENCE_INDEX.md','prediction-system/EVIDENCE_GRAPH.json']:
    h[path]=sha(R/path)
save(D/'HISTORY_BEFORE.json',h)
shutil.copyfile(R/'EVIDENCE_INDEX.md',D/'EVIDENCE_INDEX.before.md')
shutil.copyfile(R/'prediction-system/EVIDENCE_GRAPH.json',D/'EVIDENCE_GRAPH.before.json')
inputs=[R/n for n in [
 '74_身份图谱生产证据.md','74_身份特征进入价值模型的证据.md','74_研究边界与停止条件.md',
 '75_黑盒可识别性矩阵.csv','76_身份图谱证据链工程验证.md',
 'engineering76/mock76/auditor.py','engineering76/mock76/io.py','engineering76/mock76/safety.py','engineering76/README.md',
 '77_生产身份图谱工程证据矩阵.csv','77_最终判断与停止条件.md','77_关键证据缺口与竞争解释.md']]
g=json.loads((D/'EVIDENCE_GRAPH.before.json').read_text(encoding='utf-8'))
catalog=[]
for p in inputs:
    content=p.read_text(encoding='utf-8-sig')
    rel=p.relative_to(R).as_posix()
    ids=[s['id'] for s in g['sources'] if s['path']==rel]
    catalog.append(dict(path=rel,sha256=sha(p),lines=len(content.splitlines()),existing_source_ids=ids,
      read_utc=datetime.datetime.now(datetime.timezone.utc).isoformat()))
save(D/'INPUT_CATALOG.json',catalog)
# Freeze all artifacts previously included in the 76/77 manifests, avoiding SDK traversal.
legacy={}
for n in ['engineering76/ARTIFACT_MANIFEST.json','production77/ARTIFACT_MANIFEST.json']:
    legacy[n]=sha(R/n)
    for x in json.loads((R/n).read_text(encoding='utf-8-sig')):
        if x['path'] not in ['EVIDENCE_INDEX.md','prediction-system/EVIDENCE_GRAPH.json']:
            legacy[x['path']]=sha(R/x['path'])
save(D/'LEGACY_ARTIFACTS_BEFORE.json',legacy)
print(json.dumps(dict(numbered=len(h)-2,read_inputs=len(catalog),preserved_76_77_artifacts=len(legacy))))
