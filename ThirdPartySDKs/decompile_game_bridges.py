from pathlib import Path
import zipfile,io,json,subprocess
R=Path(__file__).resolve().parent;ROOT=R.parent
JAR=Path('C:/Users/89trillion/game/tower-forge/tools/jadx-headless-mcp-0.7.1-all.jar')
tasks=[
 ('car-race','classes8.dex',r'^com\.metica\.(?:ads\.internal\.adapter\.applovin\.(?:ApplovinFunctions|ApplovinInitializer|ApplovinAdapter)|sdk\..*BuildConfig).*',35),
 ('meowdoku','classes.dex',r'^com\.learnings\.usertag\.data\.tag\.MediaSourceTag$',3),
 ('meowdoku','classes5.dex',r'^com\.meevii\.adsdk\.mediation\.applovinmax\.MaxInitHelper.*',8),
 ('rotate-rings','classes3.dex',r'^w6\.e$',3),
]
rows=[]
for slug,dex,pat,limit in tasks:
 out=R/'Embedded'/slug/'bridge-java'/dex;inp=out.parent/(dex+'.input');out.mkdir(parents=True,exist_ok=True)
 if slug=='car-race':
  with zipfile.ZipFile('C:/Users/89trillion/game/car-race/source/CarRace-1.348.2.xapk') as o:
   for n in o.namelist():
    if n.endswith('.apk'):
     with zipfile.ZipFile(io.BytesIO(o.read(n))) as z:
      if dex in z.namelist():inp.write_bytes(z.read(dex));break
 else:
  for p in (ROOT/slug/'static/splits').glob('*.apk'):
   with zipfile.ZipFile(p) as z:
    if dex in z.namelist():inp.write_bytes(z.read(dex));break
 # JADX identifies DEX by header, but use .dex suffix for explicit format detection.
 dexfile=inp.with_suffix('.dex');inp.rename(dexfile)
 with (out/'jadx.log').open('wb') as f:
  p=subprocess.run(['java','-Xmx750m','-cp',str(JAR)+';'+str(ROOT),'SelectJadx',str(dexfile),str(out),pat,str(limit)],stdout=f,stderr=subprocess.STDOUT,timeout=150)
 rows.append({'slug':slug,'dex':dex,'pattern':pat,'output':str(out.relative_to(R)).replace('\\','/'),'exit':p.returncode});print(slug,dex,p.returncode,flush=True)
(R/'BRIDGE_ANALYSIS.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
