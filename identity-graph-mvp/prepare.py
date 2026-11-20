"""Freeze existing research; all writes are confined to this independent MVP folder."""
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parent.parent;D=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
if (D/'RESEARCH_BASELINE.json').exists():raise SystemExit('Baseline already frozen; refusing to replace it')
paths=load(R/'server-identity-reference/HISTORY_BEFORE.json')
for rel in ['server-identity-reference/ARTIFACT_MANIFEST.json','adjust-mechanisms/ARTIFACT_MANIFEST.json','engineering76/ARTIFACT_MANIFEST.json']:
    for x in load(R/rel):paths[x['path']]=sha(R/x['path'])
    paths[rel]=sha(R/rel)
for rel in ['EVIDENCE_INDEX.md','prediction-system/EVIDENCE_GRAPH.json']:
    paths[rel]=sha(R/rel)
for s in load(R/'prediction-system/EVIDENCE_GRAPH.json')['sources']:
    p=R/s['path']
    if p.is_file():paths[s['path']]=sha(p)
(D/'RESEARCH_BASELINE.json').write_text(json.dumps(paths,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for name in ['ACCEPTANCE_TEST_DESIGN.csv','REFERENCE_CONTRACTS.json','RELATIONSHIP_RULES.csv']:
    p=R/'server-identity-reference'/name
    out=D/'contracts'/name;out.parent.mkdir(exist_ok=True);out.write_bytes(p.read_bytes())
print(json.dumps(dict(frozen_files=len(paths),copied_contracts=3)))
