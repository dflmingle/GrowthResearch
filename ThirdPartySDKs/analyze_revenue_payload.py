from pathlib import Path
import subprocess,json
R=Path(__file__).resolve().parent;ROOT=R.parent
JAR=Path('C:/Users/89trillion/game/tower-forge/tools/jadx-headless-mcp-0.7.1-all.jar')
rel='AppsFlyer/Android/6.17.5';p=R/rel;out=p/'revenue-java';out.mkdir(exist_ok=True)
with (p/'revenue-jadx.log').open('wb') as f:
 x=subprocess.run(['java','-Xmx750m','-cp',str(JAR)+';'+str(ROOT),'SelectJadx',str(p/'classes.jar'),str(out),r'^com\.appsflyer\.internal\.(?:AFf1tSDK|AFh1lSDK|AFh1qSDK)$','6'],stdout=f,stderr=subprocess.STDOUT,timeout=120)
(R/'REVENUE_PAYLOAD_ANALYSIS.json').write_text(json.dumps({'root':rel,'exit':x.returncode,'output':str(out.relative_to(R))},indent=2),encoding='utf-8')
print('exit',x.returncode)
