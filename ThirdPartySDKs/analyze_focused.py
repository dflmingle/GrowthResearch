from pathlib import Path
import subprocess,json
R=Path(__file__).resolve().parent;ROOT=R.parent
JAR=Path('C:/Users/89trillion/game/tower-forge/tools/jadx-headless-mcp-0.7.1-all.jar')
tasks=[
 ('AppLovin/MAX/13.6.4',r'^com\.applovin\.(?:impl\.(?:c5|r7|t1|sdk\.m|sdk\.network\.(?:b|d))|sdk\.AppLovinUserData)$'),
 ('AppLovin/MAX/13.2.0',r'^com\.applovin\.(?:impl\.(?:sdk\.k|l4)|sdk\.AppLovinSdkSettings)$'),
 ('AppsFlyer/Android/6.17.5',r'^com\.appsflyer\.internal\.(?:AFa1tSDK|AFb1tSDK|AFd1kSDK|AFg1rSDK|AFg1cSDK|AFh1ySDK)$'),
]
rows=[]
for rel,pat in tasks:
 p=R/rel;out=p/'focused';out.mkdir(exist_ok=True)
 with (p/'focused-jadx.log').open('wb') as f:x=subprocess.run(['java','-Xmx750m','-cp',str(JAR)+';'+str(ROOT),'SelectJadx',str(p/'classes.jar'),str(out),pat,'15'],stdout=f,stderr=subprocess.STDOUT,timeout=180)
 print(rel,x.returncode,flush=True);rows.append({'root':rel,'pattern':pat,'exit':x.returncode})
(R/'FOCUSED_ANALYSIS.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
