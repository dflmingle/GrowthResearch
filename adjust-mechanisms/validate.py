"""Offline static provenance, quote, diff and preservation checks. Not SDK tests."""
from pathlib import Path
from urllib.parse import unquote,urlsplit
import csv,difflib,hashlib,json,re,zipfile
from datetime import datetime,timezone
R=Path(__file__).resolve().parent.parent;D=Path(__file__).resolve().parent
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
checks=[]
def check(name,ok):checks.append(dict(check=name,passed=bool(ok)))
history=load(D/'HISTORY_BEFORE.json');numbered={p:s for p,s in history.items() if p[:2].isdigit()}
check('153 numbered reports preserved',len(numbered)==153)
for p,h in numbered.items():check('history:'+p,(R/p).is_file() and sha(R/p)==h)
for p in ['EVIDENCE_INDEX.md','prediction-system/EVIDENCE_GRAPH.json']:
    snap=D/('EVIDENCE_INDEX.before.md' if p.endswith('.md') else 'EVIDENCE_GRAPH.before.json')
    check('frozen baseline:'+p,sha(snap)==history[p])
for x in load(R/'engineering76/ARTIFACT_MANIFEST.json'):
    if x['path'] in ['EVIDENCE_INDEX.md','prediction-system/EVIDENCE_GRAPH.json']:continue
    check('76 unchanged:'+x['path'],(R/x['path']).is_file() and sha(R/x['path'])==x['sha256'])
for x in load(R/'official-samples-audit/ARTIFACT_MANIFEST.json'):
    if x['path'] in ['EVIDENCE_INDEX.md','prediction-system/EVIDENCE_GRAPH.json']:continue
    check('prior audit unchanged:'+x['path'],(R/x['path']).is_file() and sha(R/x['path'])==x['sha256'])
samples=load(D/'SAMPLES.json');files=load(D/'EXTRACTED_FILES.json')
check('only three approved source JARs',[s['sample_id'] for s in samples]==['OSM034','OSM036','OSM038'])
for s in samples:
    check('archive hash:'+s['sample_id'],sha(R/s['path'])==s['sha256']==s['recorded_sha256'])
    check('provenance hash:'+s['sample_id'],sha(R/s['provenance'])==s['provenance_sha256'])
    with zipfile.ZipFile(R/s['path']) as z:
        for f in [f for f in files if f['sample_id']==s['sample_id']]:
            check('member bytes:'+f['path'],z.read(f['entry'])==(R/f['path']).read_bytes())
    license_path=D/'sources'/s['version']/'LICENSE'
    license_text=license_path.read_text(encoding='utf-8')
    check('MIT notice:'+s['version'],'Permission is hereby granted' in license_text and 'copyright' in license_text.lower())
check('111 extracted entries',len(files)==111)
for f in files:
    check('extracted hash:'+f['path'],sha(R/f['path'])==f['sha256'])
    check('archive reference:'+f['path'],any(s['path']==f['archive'] and s['sha256']==f['archive_sha256'] for s in samples))
refs=load(D/'CODE_EVIDENCE.json');refmap={x['id']:x for x in refs}
check('unique reference ids',len(refs)==len(refmap))
for x in refs:
    check('code ref file hash:'+x['id'],sha(R/x['path'])==x['sha256'])
    lines=(R/x['path']).read_text(encoding='utf-8-sig').splitlines()
    for a in x['spans']:
        check('exact quote/lines:'+x['id']+':'+str(a['start_line']),
          a['text']=='\n'.join(lines[a['start_line']-1:a['end_line']]))
        check('method token:'+x['id'],x['method']=='<field_declarations>' or bool(re.search(r'\b'+re.escape(x['method'])+r'\s*\(',a['text'])))
    check('no production upgrade:'+x['id'],not x['SDK_executed'] and not x['server_received_proven'] and not x['production_model_consumption_proven'])
findings=load(D/'FINDINGS.json')
check('22 findings',len(findings)==22)
check('61 version findings',sum(len(x['evidence_by_version']) for x in findings)==61)
used=set()
for f in findings:
    check('finding populated:'+f['id'],all(f[k] for k in ['input','processing','output','call_chain','server_unknown','reference_design','proven_client_mechanism']))
    for v,ids in f['evidence_by_version'].items():
        check('finding refs:'+f['id']+':'+v,all(i in refmap and refmap[i]['version']==v for i in ids));used.update(ids)
check('all code records referenced',used==set(refmap))
diffs=load(D/'DIFF_INDEX.final.json');check('76 selected pairs',len(diffs)==76)
check('24 changed pairs',sum(x['status']!='UNCHANGED' for x in diffs)==24)
for x in diffs:
    aa=(R/x['from_path']).read_text(encoding='utf-8-sig').splitlines(keepends=True) if x['from_path'] else []
    bb=(R/x['to_path']).read_text(encoding='utf-8-sig').splitlines(keepends=True) if x['to_path'] else []
    computed=''.join(difflib.unified_diff(aa,bb,fromfile=x['from_version']+'/'+x['entry'],tofile=x['to_version']+'/'+x['entry']))
    check('diff status:'+str(x['from_version'])+x['entry'],bool(computed)==(x['status']!='UNCHANGED'))
    if x['diff_path']:
        check('diff exact:'+x['diff_path'],computed==(R/x['diff_path']).read_text(encoding='utf-8') and sha(R/x['diff_path'])==x['diff_sha256'])
for x in load(D/'license-review/FETCH_MANIFEST.json'):
    check('legal raw:'+x['id'],sha(R/x['path'])==x['sha256'])
    check('legal text:'+x['id'],sha(R/x['text_path'])==x['text_sha256'])
check('5 legal-only responses',len(load(D/'license-review/FETCH_MANIFEST.json'))==5)
old=load(D/'EVIDENCE_GRAPH.before.json');g=load(R/'prediction-system/EVIDENCE_GRAPH.json')
for k,v in old.items():check('old graph preserved:'+k,g[k][:len(v)]==v if k in ['nodes','edges','sources'] else g.get(k)==v)
check('graph additions 5/4/21',[len(g[k])-len(old[k]) for k in ['nodes','edges','sources']]==[5,4,21])
allids={x['id'] for x in g['sources']};nodes={x['id'] for x in g['nodes']}
for k in ['nodes','edges','sources']:check('unique graph ids:'+k,len({x['id'] for x in g[k]})==len(g[k]))
added=load(D/'ADDED_GRAPH_OBJECTS.json')
for s in added['sources']:check('new graph source:'+s['id'],sha(R/s['path'])==s['sha256'])
for e in added['edges']:
    check('edge refs:'+e['id'],e['source'] in nodes and e['target'] in nodes and all(s in allids for s in e['source_ids']))
    check('edge limits:'+e['id'],not any(e[k] for k in ['production_actual_proven','production_match_proven','prediction_model_consumption_proven','independent_real_identity_lift_proven']))
check('index append-only',(R/'EVIDENCE_INDEX.md').read_bytes().startswith((D/'EVIDENCE_INDEX.before.md').read_bytes()))
for rel in load(D/'REPORT_PATHS.json'):
    p=R/rel;check('report exists:'+rel,p.is_file() and p.stat().st_size>300)
    text=p.read_text(encoding='utf-8')
    for raw in re.findall(r'\]\(([^)]+)\)',text):
        target=unquote(raw.split('#')[0])
        if target and not urlsplit(target).scheme:
            resolved=(p.parent/target).resolve()
            # This check produces VALIDATION.json; its output is not a pre-existing input.
            check('report link:'+rel+':'+raw,resolved==(D/'VALIDATION.json').resolve() or resolved.exists())
status=load(D/'STATUS.json')
check('scope preserved',status['C_graph_Axon']==status['C_graph_Vector']==status['D']=='UNKNOWN' and status['production_forensics']=='STOP')
check('no runtime activities',all(status[k]==0 for k in ['new_SDK_downloads','SDK_executions','production_requests','real_identity_accesses']))
check('no79 created',not list(R.glob('79*')))
result=dict(reviewed_utc=datetime.now(timezone.utc).isoformat(),status='PASS' if all(c['passed'] for c in checks) else 'FAIL',
   check_count=len(checks),passed=sum(c['passed'] for c in checks),failed=[c for c in checks if not c['passed']],
   scope='Static hash/quote/diff/link/preservation verification only; no Java execution or production/behavior test',checks=checks)
(D/'VALIDATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:result[k] for k in ['status','check_count','passed','failed']},ensure_ascii=False))
raise SystemExit(0 if result['status']=='PASS' else 1)
