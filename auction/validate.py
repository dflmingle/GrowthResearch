"""Offline deliverable and source-integrity checks; not production platform verification."""
from pathlib import Path
import json,hashlib,re,subprocess,sys,datetime
ROOT=Path(__file__).resolve().parent.parent;R=ROOT/'auction'
errors=[];links=0
reports=[next(ROOT.glob(f'{n}_*.md')) for n in range(35,41)]
for p in reports:
 text=p.read_text(encoding='utf-8')
 if '\ufffd' in text:errors.append('replacement character '+p.name)
 for label,target in re.findall(r'\[([^\]]*)\]\(([^)]+)\)',text):
  if target.startswith(('http:','https:','mailto:')):continue
  file,_,anchor=target.partition('#');f=p.parent/file if file else p;links+=1
  if not f.is_file():errors.append('missing link '+p.name+' '+target)
  elif anchor and file=='EVIDENCE_INDEX.md' and f'id="{anchor}"' not in f.read_text(encoding='utf-8'):
   errors.append('missing anchor '+anchor)
m=json.loads((ROOT/'EVIDENCE_MANIFEST.json').read_text(encoding='utf-8'))
gs=[e for e in m['entries'] if re.fullmatch(r'BP\d\d',e.get('id',''))]
assert len(gs)==11
count=0
for g in gs:
 for s in g['sources']:
  p=ROOT/s['path'];count+=1
  if not p.is_file():errors.append('missing source '+s['path']);continue
  if hashlib.sha256(p.read_bytes()).hexdigest()!=s['sha256']:errors.append('hash mismatch '+s['path'])
for x in json.loads((R/'SDK_AUDIT.json').read_text()):
 if hashlib.sha256((ROOT/x['jar']).read_bytes()).hexdigest()!=x['sha256']:errors.append('SDK changed '+x['sdk'])
for x in json.loads((R/'CODE_EVIDENCE.json').read_text()):
 p=ROOT/x['path'];lines=p.read_text().splitlines()
 if hashlib.sha256(p.read_bytes()).hexdigest()!=x['sha256']:errors.append('excerpt source hash '+x['id'])
 expected='\n'.join(f'{i+1}: {line}' for i,line in enumerate(lines) if x['start_line']<=i+1<=x['end_line'])
 if x['text']!=expected:errors.append('excerpt content '+x['id'])
fields=json.loads((R/'PROTOCOL_FIELDS.json').read_text())
assert len(fields)==444
for x in fields:
 if len(x['cells'])<2:errors.append('bad row '+x['field'])
 if hashlib.sha256((ROOT/x['source']).read_bytes()).hexdigest()!=x['sha256']:errors.append('field source changed '+x['source'])
control=json.loads((R/'model/output/matched_tmax_control.json').read_text());assert control['economics_identical']
econ=json.loads((R/'model/output/results.json').read_text());assert econ['synthetic'] and not econ['platform_model_recovered']
for arm in econ['arms']:
 if not 0<=arm['spend_usd']<=20:errors.append('budget overrun')
 if arm['installs'] and abs(arm['CPI_usd']-arm['spend_usd']/arm['installs'])>1e-9:errors.append('CPI mismatch')
 if abs(arm['D28_ROAS']-arm['D28_revenue_usd']/arm['spend_usd'])>1e-9:errors.append('ROAS mismatch')
 # cumulative maturity, not sum of D0+D7+D28 as three separate revenue streams
 if not arm['D0_revenue_usd']<=arm['D7_revenue_usd']<=arm['D28_revenue_usd']:errors.append('maturity mismatch')
test=subprocess.run([sys.executable,'-X','utf8','-m','unittest','test_auction_model','-v'],cwd=R/'model',capture_output=True,text=True)
(R/'model/TEST_RESULTS.txt').write_text(test.stdout+test.stderr,encoding='utf-8')
if test.returncode:errors.append('model tests failed')
summary=dict(status='PASS' if not errors else 'FAIL',utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
 reports=[dict(path=p.name,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in reports],local_links_checked=links,
 evidence_groups=len(gs),source_hashes_checked=count,protocol_table_rows=len(fields),model_tests=17,
 model_arms=len(econ['arms']),matched_tmax_control=control['economics_identical'],errors=errors,
 scope='Offline citations/source/model checks; not proof of production auction behavior, identity joins or model accuracy.')
(R/'VALIDATION.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False,indent=2))
raise SystemExit(bool(errors))
