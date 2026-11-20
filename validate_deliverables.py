from pathlib import Path
import re,json,hashlib,datetime,collections
R=Path(__file__).resolve().parent
reports=sorted(R.glob('*.md'));issues=[];links=0
for p in reports:
 t=p.read_text(encoding='utf-8')
 if '\ufffd' in t:issues.append({'file':p.name,'issue':'replacement character'})
 for label,target in re.findall(r'\[([^\]]*)\]\(([^)]+)\)',t):
  if target.startswith(('https://','http://','mailto:')):continue
  dest,_,anchor=target.partition('#');f=p.parent/dest if dest else p
  if not f.exists():issues.append({'file':p.name,'target':target,'issue':'missing target'})
  elif anchor and f.suffix=='.md' and f'id="{anchor}"' not in f.read_text(encoding='utf-8'):issues.append({'file':p.name,'target':target,'issue':'missing explicit anchor'})
  links+=1
manifest=json.loads((R/'EVIDENCE_MANIFEST.json').read_text(encoding='utf-8'));n=0
for e in manifest['entries']:
 for s in e['sources']:
  if 'sha256' not in s:continue
  p=R/s['path'];n+=1
  if hashlib.sha256(p.read_bytes()).hexdigest()!=s['sha256']:issues.append({'id':e['id'],'source':s['path'],'issue':'hash mismatch'})
catalog=json.loads((R/'SAMPLE_CATALOG.json').read_text(encoding='utf-8'))
if not all(x.get('hash_matches',True) for x in catalog):issues.append({'issue':'sample hash mismatch'})
gm=json.loads((R/'meowdoku/static/godot-script-map.json').read_text(encoding='utf-8'));dupes=[n for n,c in collections.Counter(x['decompiled_file'] for x in gm).items() if c>1]
if dupes:issues.append({'issue':'GDScript flattened name collision','names':dupes})
v={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'report_count':len(reports),'relative_links_checked':links,'referenced_artifact_hashes_checked':n,'sample_archive_checks':[(x['slug'],x.get('hash_matches','MISSING')) for x in catalog],'godot_script_mappings':len(gm),'issues':issues,'status':'PASS' if not issues else 'FAIL','scope':'artifact/link/hash integrity only; not runtime SDK delivery or advertising-performance validation'}
(R/'DELIVERABLE_VALIDATION.json').write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(v,ensure_ascii=True,indent=2))
raise SystemExit(bool(issues))
