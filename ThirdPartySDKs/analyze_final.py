from pathlib import Path
import subprocess,zipfile,json,re,sys
R=Path(__file__).resolve().parent;ROOT=R.parent
sys.stdout.reconfigure(encoding='utf-8');JAR=Path('C:/Users/89trillion/game/tower-forge/tools/jadx-headless-mcp-0.7.1-all.jar')
tasks=[
 ('AppsFlyer/Android/6.17.5',r'^com\.appsflyer\.internal\.(?:AFa1ySDK|AFc1vSDK|AFe1bSDK|AFf1hSDK|AFf1rSDK)$'),
 ('AppsFlyer/Android/6.14.2',r'^com\.appsflyer\.internal\.(?:AFb1iSDK|AFf1mSDK|AFg1sSDK)$'),
 ('Metica/Android/2.5.4',r'^com\.metica\.(?:MeticaSdk|MeticaInitConfig|BuildConfig|ads\.internal\.adapter\.applovin\.(?:ApplovinInitializer|ApplovinFunctions)|ads\.mediation\.MeticaApplovinFunctions)$'),
]
rows=[]
for rel,pat in tasks:
 p=R/rel;out=p/'final-java';out.mkdir(exist_ok=True)
 with (p/'final-jadx.log').open('wb') as f:x=subprocess.run(['java','-Xmx750m','-cp',str(JAR)+';'+str(ROOT),'SelectJadx',str(p/'classes.jar'),str(out),pat,'15'],stdout=f,stderr=subprocess.STDOUT,timeout=180)
 rows.append({'root':rel,'pattern':pat,'exit':x.returncode});print(rel,x.returncode,flush=True)
for src in R.glob('*/*/*/*-sources.jar'):
 dest=src.parent/'sources'
 if dest.exists():continue
 dest.mkdir(exist_ok=True)
 with zipfile.ZipFile(src) as z:
  for n in z.namelist():
   if not n.endswith(('.java','.kt','.txt','.md')):continue
   p=(dest/n).resolve()
   if not p.is_relative_to(dest.resolve()):raise ValueError('unsafe source archive')
   p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(z.read(n))
(R/'FINAL_ANALYSIS.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
