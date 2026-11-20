from pathlib import Path
import datetime,hashlib,json,shutil

R=Path(__file__).resolve().parent.parent;D=R/'blackbox75';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert not (D/'HISTORY_BEFORE.json').exists(),'Never replace an existing baseline'
h={p.name:sha(p) for p in R.iterdir() if p.is_file() and p.name[:2].isdigit() and int(p.name[:2])<=74}
for rel in ['EVIDENCE_INDEX.md','prediction-system/EVIDENCE_GRAPH.json']:h[rel]=sha(R/rel)
save(D/'HISTORY_BEFORE.json',h)
shutil.copyfile(R/'EVIDENCE_INDEX.md',D/'EVIDENCE_INDEX.before.md')
shutil.copyfile(R/'prediction-system/EVIDENCE_GRAPH.json',D/'EVIDENCE_GRAPH.before.json')
g=json.loads((D/'EVIDENCE_GRAPH.before.json').read_text('utf-8'))
ids=['IG72S01','IG72S02','IG72S03','IG72S05','IG72C04','IG72C05','IG72C14','IG72C25','IG72C27','CGS51','MA60S17',
     'IV74S01','IV74S02','IV74S03','IV74S04','IV74S05','IV74S07','IV74S08','IV74S09','IV74S10','IV74S12','IV74S13','IV74S14',
     'EX73R04','EX73R06','EX73R07','EX73R08','EX73R09','IV74R01','IV74R02','IV74R03']
sources=[next(x for x in g['sources'] if x['id']==sid) for sid in ids]
for x in sources:assert sha(R/x['path'])==x['sha256'],x['id']
save(D/'REUSED_EVIDENCE.json',sources)
reports=[]
for p in sorted(R.iterdir()):
 if p.suffix!='.md' or not p.name.startswith(('72_','73_','74_')):continue
 text=p.read_text('utf-8');reports.append(dict(path=p.name,sha256=sha(p),characters=len(text)))
 # Only bounded opening sections;source originals remain readable and unchanged.
 print(p.name,':',text[:650].replace('\n',' '))
save(D/'READING_LOG.json',dict(read_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),reports=reports,
  focus='72 identities,73 synthetic and licence boundaries,74 production/feature/use/design/stopping conclusions'))
save(D/'RUN_SCOPE.json',dict(external_requests=0,SDK_scans=0,downloads=0,real_personal_data_read=0,identity_queries=0,
 production_ad_requests=0,real_ad_campaigns=0,real_devices_modified=0,real_accounts_linked=0,
 real_model_training=0,synthetic_only=True,synthetic_trial_is_not_vendor_architecture=True))
print(json.dumps(dict(historical_numbered_files=len(h)-2,reused_sources=len(sources),reports_read=len(reports))))
