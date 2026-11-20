from pathlib import Path
import json,subprocess,re,sys
R=Path(__file__).resolve().parent/'deep';ROOT=R.parents[1];JAR=Path('C:/Users/89trillion/game/tower-forge/tools/jadx-headless-mcp-0.7.1-all.jar')
sys.stdout.reconfigure(encoding='utf-8');rows=[]
for row in json.loads((R/'network-candidates.json').read_text(encoding='utf-8')):
 v=row['version'];classes=[x['class'] for x in row['candidates'] if not x['class'].endswith(('q7','t7','u7','z6'))]
 classes+=['com.applovin.impl.sdk.network.b$a','com.applovin.impl.sdk.network.d$b']
 pat='^(?:'+'|'.join(re.escape(x) for x in classes)+')$';out=R/'versions'/v/'network';out.mkdir(exist_ok=True)
 with (out/'jadx.log').open('wb') as f:p=subprocess.run(['java','-Xmx750m','-cp',str(JAR)+';'+str(ROOT),'SelectJadx',str(ROOT/'ThirdPartySDKs/AppLovin/MAX'/v/'classes.jar'),str(out),pat,'20'],stdout=f,stderr=subprocess.STDOUT,timeout=180)
 print(v,p.returncode,flush=True);rows.append({'version':v,'classes':classes,'exit':p.returncode})
(R/'network-decompilation.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
