from pathlib import Path
import subprocess,re,json,sys
R=Path(__file__).resolve().parent/'deep';ROOT=R.parents[1];JAR=Path('C:/Users/89trillion/game/tower-forge/tools/jadx-headless-mcp-0.7.1-all.jar');sys.stdout.reconfigure(encoding='utf-8')
rows=[]
for v,classes in [
 ('13.2.0',['com.applovin.impl.n4','com.applovin.impl.m4','com.applovin.impl.e5$b']),
 ('13.6.2',['com.applovin.impl.b5','com.applovin.impl.a5','com.applovin.impl.s5$b']),
 ('13.6.3',['com.applovin.impl.e5','com.applovin.impl.d5','com.applovin.impl.v5$b']),
 ('13.6.4',['com.applovin.impl.e5','com.applovin.impl.d5','com.applovin.impl.v5$b','com.applovin.impl.sdk.utils.JsonUtils']),
]:
 out=R/'versions'/v/'final';out.mkdir(exist_ok=True);pat='^(?:'+'|'.join(re.escape(c) for c in classes)+')$'
 with (out/'jadx.log').open('wb') as f:a=subprocess.run(['java','-Xmx750m','-cp',str(JAR)+';'+str(ROOT),'SelectJadx',str(ROOT/'ThirdPartySDKs/AppLovin/MAX'/v/'classes.jar'),str(out),pat,'10'],stdout=f,stderr=subprocess.STDOUT,timeout=150)
 rows.append({'version':v,'classes':classes,'exit':a.returncode});print(v,a.returncode,flush=True)
(R/'final-decompilation.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
