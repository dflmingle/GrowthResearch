from pathlib import Path
import csv,datetime,hashlib,json,re

R=Path(__file__).resolve().parent.parent;D=R/'identity-value74';V=D/'VALIDATION.json';checks=[]
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def check(name,condition,detail=''):
 checks.append(dict(name=name,pass_check=bool(condition),detail=detail))
 if not condition:raise AssertionError(name+': '+str(detail))
def main():
 save(V,dict(status='RUNNING',started_utc=datetime.datetime.now(datetime.timezone.utc).isoformat()))
 h=read(D/'HISTORY_BEFORE.json');old=read(D/'EVIDENCE_GRAPH.before.json');g=read(R/'prediction-system/EVIDENCE_GRAPH.json')
 for rel,digest in h.items():
  if rel not in ['EVIDENCE_INDEX.md','prediction-system/EVIDENCE_GRAPH.json']:check('Historical bytes unchanged: '+rel,sha(R/rel)==digest)
 for x in read(R/'identity72-experiments73/ARTIFACT_MANIFEST.json'):
  if x['path'] not in ['EVIDENCE_INDEX.md','prediction-system/EVIDENCE_GRAPH.json']:
   check('Prior 72/73 artifact unchanged: '+x['path'],sha(R/x['path'])==x['sha256'])
 check('Frozen graph baseline hash',sha(D/'EVIDENCE_GRAPH.before.json')==h['prediction-system/EVIDENCE_GRAPH.json'])
 check('Frozen index baseline hash',sha(D/'EVIDENCE_INDEX.before.md')==h['EVIDENCE_INDEX.md'])
 check('Index append only',(R/'EVIDENCE_INDEX.md').read_bytes().startswith((D/'EVIDENCE_INDEX.before.md').read_bytes()))
 for k,v in old.items():check('Old graph section preserved: '+k,g[k][:len(v)]==v if k in ['nodes','edges','sources'] else g[k]==v)
 for k in ['nodes','edges','sources']:check('All graph IDs unique: '+k,len({x['id'] for x in g[k]})==len(g[k]))
 nn=g['nodes'][len(old['nodes']):];ne=g['edges'][len(old['edges']):];ns=g['sources'][len(old['sources']):]
 check('Only expected new objects',(len(nn),len(ne),len(ns))==(16,19,17))
 ni={x['id'] for x in g['nodes']};si={x['id'] for x in g['sources']}
 check('New graph references valid',all(e['source'] in ni and e['target'] in ni and set(e['source_ids'])<=si for e in ne))
 check('No new E5/E6',all(not set(x.get('evidence_stages',[]))&{'E5','E6'} for x in ne+ns))
 check('No new actual graph-use or independent-lift assertion',all(x['production_match_proven'] is False and x['prediction_model_consumption_proven'] is False and x['independent_identity_lift_proven'] is False for x in ne+ns))
 for x in ns+read(D/'REUSED_EVIDENCE.json'):check('Source file hash: '+x['id'],sha(R/x['path'])==x['sha256'])
 sources=read(D/'SOURCE_EVIDENCE.json');check('14 primary excerpt records',len(sources)==14)
 for x in sources:
  check('Source text hash: '+x['id'],sha(R/x['text_path'])==x['text_sha256'])
  ls=(R/x['text_path']).read_text('utf-8').splitlines();excerpt='\n'.join(f'{i+1}: {s}' for i,s in enumerate(ls) if x['start_line']<=i+1<=x['end_line'])
  check('Exact substantive excerpt: '+x['id'],excerpt==x['excerpt'] and len(excerpt)>100)
 fetch=read(D/'FETCH_MANIFEST.json');coverage=read(D/'SEARCH_COVERAGE.json')
 check('30 public retrieval records',len(fetch)==30 and coverage['requests']==30 and coverage['search_pages']==8)
 for f in fetch:
  if 'path' in f:check('Public response unchanged: '+f['id'],sha(R/f['path'])==f['sha256'] and sha(R/f['text_path'])==f['text_sha256'])
 check('No search/shell promoted to proof',all(not x['claim_proof_used'] for x in coverage['assessments'] if x['id'].startswith('search-') or x['id'] in ['lr-api','lr-resolution','lr-privacy-guide','al-audiences','lr-sidecar','wurl-behavior','wurl-mobile']))
 matrix_path=next(R.glob('74_*.csv'))
 with matrix_path.open(encoding='utf-8-sig',newline='') as f:matrix=list(csv.DictReader(f))
 check('18 claims equal JSON matrix',len(matrix)==18 and matrix==read(D/'CLAIMS.json'))
 refs={x['id']:x for x in sources+read(D/'REUSED_EVIDENCE.json')}
 for x in matrix:
  ids=x['source_ids'].split(';')
  check('Matrix source/hash references: '+x['claim_id'],all(s in refs for s in ids) and x['source_sha256']==';'.join(refs[s]['sha256'] for s in ids))
  check('No actual receiver asserted: '+x['claim_id'],x['B_actual_target_receipt']=='UNKNOWN')
 vendor=[x for x in matrix if x['company'] in ['AppLovin','Unity']]
 check('Target C_graph/D retained unknown',all(x['C_resolved_identity_model_use']=='UNKNOWN' and x['D_identity_only_incremental_gain']=='UNKNOWN' for x in vendor))
 check('Official C_id evidence not erased',any(x['company']=='AppLovin' and x['C_identifier_category_use']=='OFFICIAL_AXON_FACTORS' for x in vendor))
 readiness=read(D/'EXPERIMENT_READINESS.json')
 check('All five real experiments STOP with no result',len(readiness['models'])==5 and all(x['status']=='STOP_REAL_DATA_NOT_ADMITTED' and x['result'] is None for x in readiness['models']))
 check('Primary M4-M3 same effective samples',readiness['primary_contrast']=='M4-M3' and readiness['M3_M4_effective_supervised_samples_fixed'] is True and readiness['all_five_effective_source_data_equal'] is False)
 check('No real training or ROAS',readiness['real_training_performed'] is False and readiness['real_ROAS_allowed'] is False)
 check('Protocol SHA frozen with readiness',sha(R/readiness['protocol_path'])==readiness['protocol_sha256'])
 check('Declared runtime boundaries',all(v==0 for k,v in read(D/'RUN_SCOPE.json').items() if isinstance(v,int)),'Script/artifact scope audit;not independent network capture')
 files=sorted(R.glob('74_*'));check('Five requested deliverables',len(files)==5 and sum(p.suffix=='.md' for p in files)==4 and sum(p.suffix=='.csv' for p in files)==1)
 # Link verification is scoped to new docs;old reports intentionally remain immutable.
 for p in files+[p for p in D.glob('*.md') if not p.name.endswith('.before.md')]:
  if p.suffix!='.md':continue
  txt=p.read_text('utf-8');check('No replacement decoding characters: '+p.name,'\ufffd' not in txt)
  for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',txt):
   target=target.strip('<>').split('#')[0]
   if not target or re.match(r'https?://|mailto:',target):continue
   check('Local link: '+p.name+' -> '+target,(p.parent/target).exists())
 check('Semantic correction recorded',(D/'CORRECTIONS.md').exists() and 'IG72S07' in (D/'CORRECTIONS.md').read_text('utf-8'))
 check('Literal existing-vs-derived caveat retained','derived' in sources[0]['excerpt'] and 'maintained' in sources[0]['excerpt'])
 proto=(R/readiness['protocol_path']).read_text('utf-8')
 check('Protocol includes source-sample caveat and identity controls',all(t in proto for t in ['M4-shuffled','M4-thinned','M1-more-data','available_at','M4减M3','有效秩']))
 paths=files+[R/'EVIDENCE_INDEX.md',R/'prediction-system/EVIDENCE_GRAPH.json']+[p for p in D.rglob('*') if p.is_file() and p not in [V,D/'ARTIFACT_MANIFEST.json']]
 manifest=[dict(path=p.relative_to(R).as_posix(),bytes=p.stat().st_size,sha256=sha(p),modified_utc=datetime.datetime.fromtimestamp(p.stat().st_mtime,datetime.timezone.utc).isoformat()) for p in sorted(set(paths))]
 save(D/'ARTIFACT_MANIFEST.json',manifest)
 result=dict(status='PASS',completed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),checks_passed=len(checks),checks=checks,
  historical_numbered_files_unchanged=len(h)-2,new_deliverables=len(files),new_primary_excerpt_records=len(sources),matrix_rows=len(matrix),
  graph_counts={k:len(g[k]) for k in ['nodes','edges','sources']},
  real_model_training=False,production_identity_queries=False,C_graph='UNKNOWN',D_identity_only_lift='UNKNOWN',
  artifact_manifest_sha256=sha(D/'ARTIFACT_MANIFEST.json'),
  limitations=['Hashes/link tests do not prove semantic claims by themselves','Public contracts not authorized production receipts','Search coverage limited,not proof no other papers exist','No new real experiment or vendor effect estimate'])
 save(V,result);print(json.dumps({k:result[k] for k in ['status','checks_passed','historical_numbered_files_unchanged','new_deliverables','graph_counts']},indent=2))
if __name__=='__main__':
 try:main()
 except Exception as e:
  save(V,dict(status='FAIL',error=repr(e),checks=checks));raise
