from pathlib import Path
import json,subprocess,sys,zipfile
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'ThirdPartySDKs'))
from embedded_scan import dexes
R=Path(__file__).resolve().parent/'deep';ROOT=R.parents[1];JAR=Path('C:/Users/89trillion/game/tower-forge/tools/jadx-headless-mcp-0.7.1-all.jar')
tasks=[('car-race','classes10.dex',r'^com\.metica\.(?:unity_bridge\.UnityBridge|MeticaSdk|MeticaInitConfig|internal\..*(?:User|Config|Init).*)$',25),('car-race','classes8.dex',r'^com\.metica\.ads\.internal\.adapter\.applovin\.ApplovinInitializer.*$',10),('meowdoku','classes5.dex',r'^com\.meevii\.adsdk\.(?:AdInitParameter.*|common\.(?:AdUuid|SharedProxy))$',12),('meowdoku','classes4.dex',r'^com\.learnings\.usertag\.data\.MediaSourceData$',2)]
rows=[]
for slug,dn,pat,n in tasks:
 dest=R/'bridges'/slug/dn;dest.mkdir(parents=True,exist_ok=True);inp=dest/'input.dex'
 for apk,name,data in dexes(slug):
  if name==dn:inp.write_bytes(data);break
 with (dest/'jadx.log').open('wb') as f:x=subprocess.run(['java','-Xmx750m','-cp',str(JAR)+';'+str(ROOT),'SelectJadx',str(inp),str(dest/'java'),pat,str(n)],stdout=f,stderr=subprocess.STDOUT,timeout=150)
 rows.append({'slug':slug,'dex':dn,'pattern':pat,'exit':x.returncode});print(slug,dn,x.returncode,flush=True)
(R/'bridge-decompilation.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
