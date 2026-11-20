from pathlib import Path
import subprocess,json,zipfile,re,sys
R=Path(__file__).resolve().parent/'deep';ROOT=R.parents[1];R.mkdir(exist_ok=True)
JAR=Path('C:/Users/89trillion/game/tower-forge/tools/jadx-headless-mcp-0.7.1-all.jar')
sys.stdout.reconfigure(encoding='utf-8')
rows=[]
for v in ['13.2.0','13.6.2','13.6.3','13.6.4']:
 p=ROOT/'ThirdPartySDKs/AppLovin/MAX'/v/'classes.jar';out=R/'versions'/v;out.mkdir(parents=True,exist_ok=True)
 pat=r'^com\.applovin\.(?:sdk\.(?:AppLovinSdk|AppLovinSdkSettings|AppLovinUserData)|impl\.sdk\.(?:EventServiceImpl|j|k|l|m)|impl\.sdk\.network\.(?:b|c|d|e|PostbackServiceImpl)|impl\.(?:c5|l4|r7|t1))$'
 # Python regex is passed verbatim; JAVA expects a single backslash before a dot.
 pat=pat.replace('\\\\','\\')
 with (out/'jadx.log').open('wb') as f:x=subprocess.run(['java','-Xmx750m','-cp',str(JAR)+';'+str(ROOT),'SelectJadx',str(p),str(out/'java'),pat,'30'],stdout=f,stderr=subprocess.STDOUT,timeout=180)
 rows.append({'version':v,'input':str(p.relative_to(ROOT)).replace('\\','/'),'pattern':pat,'exit':x.returncode});print(v,x.returncode,flush=True)
(R/'version-decompilation.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
