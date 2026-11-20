from pathlib import Path
import json,re,zipfile,hashlib,subprocess,sys
R=Path(__file__).resolve().parent;ROOT=R.parent;sys.stdout.reconfigure(encoding='utf-8')
JAR=Path('C:/Users/89trillion/game/tower-forge/tools/jadx-headless-mcp-0.7.1-all.jar')
tasks=[('Unity/Ads/4.17.0',r'^com\.unity3d\.(?:ads\.UnityAds|ads\.core\.domain\.(?:AndroidGetAdRequest|CommonGetHeaderBiddingToken|GetUniversalRequestForPayLoad)|ads\.core\.data\.repository\.AndroidSessionRepository|ads\.core\.domain\.events\.GetOperativeEventRequest|services\.core\.device\.reader\.DeviceInfoReaderWithPrivacy)$'),
 ('Unity/Ads/4.18.1',r'^com\.unity3d\.(?:ads\.UnityAds|ads\.core\.domain\.(?:AndroidGetAdRequest|CommonGetHeaderBiddingToken|GetUniversalRequestForPayLoad)|ads\.core\.data\.repository\.AndroidSessionRepository|ads\.core\.domain\.events\.GetOperativeEventRequest|services\.core\.device\.reader\.DeviceInfoReaderWithPrivacy)$'),
 ('Unity/LevelPlay/9.3.0',r'^(?:com\.unity3d\.mediation\.(?:LevelPlay|LevelPlayInitRequest|LevelPlayAdInfo|LevelPlayImpressionData)|com\.ironsource\.mediationsdk\.(?:IronSource|ImpressionData))$'),
 ('Unity/Dependency-mediation-sdk/9.4.0',r'^(?:com\.unity3d\.mediation\.(?:LevelPlay|LevelPlayInitRequest|LevelPlayAdInfo)|com\.ironsource\.mediationsdk\.(?:IronSource|ImpressionData))$'),
 ('Unity/LevelPlay/9.5.0',r'^(?:com\.unity3d\.mediation\.(?:LevelPlay|LevelPlayInitRequest|LevelPlayAdInfo)|com\.ironsource\.mediationsdk\.(?:IronSource|ImpressionData))$')]
results=[]
for rel,pat in tasks:
 jar=ROOT/'ThirdPartySDKs'/rel/'classes.jar';dest=R/'sdk'/rel;dest.mkdir(parents=True,exist_ok=True);scan=[]
 with zipfile.ZipFile(jar) as z:
  for n in z.namelist():
   if not n.endswith('.class'):continue
   b=z.read(n);hits=[s for s in ['Vector','vector','Day28','RuntimeData','runtimeData','collectSignals','ad_revenue','privacy','UnityServices'] if s.encode() in b]
   if hits:scan.append({'class':n[:-6].replace('/','.'),'literals':hits})
 with (dest/'jadx.log').open('wb') as f:x=subprocess.run(['java','-Xmx750m','-cp',str(JAR)+';'+str(ROOT),'SelectJadx',str(jar),str(dest/'java'),pat,'18'],stdout=f,stderr=subprocess.STDOUT,timeout=180)
 rows={'sdk':rel,'classes_jar_sha256':hashlib.sha256(jar.read_bytes()).hexdigest(),'literal_candidates':scan,'decompile_exit':x.returncode};(dest/'scan.json').write_text(json.dumps(rows,indent=2),encoding='utf-8');results.append(rows);print(rel,x.returncode,len(scan),flush=True)
(R/'SDK_AUDIT.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
