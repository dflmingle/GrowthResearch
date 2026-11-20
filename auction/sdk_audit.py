from pathlib import Path
import zipfile,json,hashlib,re,subprocess
R=Path(__file__).resolve().parent;ROOT=R.parent
JADX='C:/Users/89trillion/game/tower-forge/tools/jadx-headless-mcp-0.7.1-all.jar'
tasks=[('MAX-13.6.4',ROOT/'ThirdPartySDKs/AppLovin/MAX/13.6.4/classes.jar',[
 'com.applovin.impl.a6','com.applovin.impl.a6$a','com.applovin.impl.c3','com.applovin.impl.g3',
 'com.applovin.impl.h2','com.applovin.impl.l6','com.applovin.impl.u5','com.applovin.impl.v3',
 'com.applovin.impl.mediation.MediationServiceImpl','com.applovin.impl.mediation.MaxAdWaterfallInfoImpl',
 'com.applovin.impl.mediation.MaxAdapterParametersImpl']),
 ('LevelPlay-9.4.0',ROOT/'ThirdPartySDKs/Unity/Dependency-mediation-sdk/9.4.0/classes.jar',[])]
records=[]
for name,jar,selected in tasks:
 dest=R/'sdk'/name;dest.mkdir(parents=True,exist_ok=True)
 terms=['auctionTimeout','auctionResponse','auction_request','auctionId','bidderToken','biddingData','auctionData','https://auction','Auction failed','auctionTrials','load_timeout','bid_response']
 hits=[]
 with zipfile.ZipFile(jar) as z:
  for n in z.namelist():
   if not n.endswith('.class'):continue
   b=z.read(n);found=[t for t in terms if t.encode() in b]
   if found:hits.append(dict(cls=n[:-6].replace('/','.'),terms=found))
 if not selected:
  selected=[x['cls'] for x in sorted(hits,key=lambda x:len(x['terms']),reverse=True)[:14]]
 regex='^(?:'+'|'.join(re.escape(s) for s in selected)+')$'
 with (dest/'jadx.log').open('wb') as f:
  run=subprocess.run(['java','-Xmx650m','-cp',JADX+';'+str(ROOT),'SelectJadx',str(jar),str(dest/'java'),regex,'35'],stdout=f,stderr=subprocess.STDOUT,timeout=180)
 records.append(dict(sdk=name,jar=jar.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(jar.read_bytes()).hexdigest(),
                     classes=selected,hits=hits,exit=run.returncode))
 print(name,'classes',len(selected),'exit',run.returncode,flush=True)
(R/'SDK_AUDIT.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
