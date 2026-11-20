from pathlib import Path
import sys,json,gc,re,subprocess
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'ThirdPartySDKs'))
from embedded_scan import dexes
from androguard.core.dex import DEX
R=Path(__file__).resolve().parent/'deep';ROOT=R.parents[1];JAR=Path('C:/Users/89trillion/game/tower-forge/tools/jadx-headless-mcp-0.7.1-all.jar')
sys.stdout.reconfigure(encoding='utf-8');rows=[]
targets={'Lcom/metica/MeticaSdk;','Lcom/metica/MeticaInitConfig;','Lcom/metica/MeticaSdk$initialize$2;','Lcom/metica/ads/internal/MeticaAdsImpl;'}
for apk,dn,data in dexes('car-race'):
 if b'com/metica' not in data:continue
 d=DEX(data);found=[c.get_name() for c in d.get_classes() if c.get_name() in targets]
 if found:
  out=R/'metica-car'/dn;out.mkdir(parents=True,exist_ok=True);p=out/'input.dex';p.write_bytes(data);pat='^(?:'+'|'.join(re.escape(x[1:-1].replace('/','.')) for x in found)+')$'
  with (out/'jadx.log').open('wb') as f:z=subprocess.run(['java','-Xmx750m','-cp',str(JAR)+';'+str(ROOT),'SelectJadx',str(p),str(out/'java'),pat,'10'],stdout=f,stderr=subprocess.STDOUT,timeout=150)
  rows.append({'dex':dn,'classes':found,'exit':z.returncode});print(dn,found,z.returncode,flush=True)
 del d,data;gc.collect()
(R/'metica-car-index.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
