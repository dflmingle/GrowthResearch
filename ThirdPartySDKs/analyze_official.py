from pathlib import Path
import json,zipfile,re,subprocess,sys,hashlib
R=Path(__file__).resolve().parent;ROOT=R.parent
sys.stdout.reconfigure(encoding='utf-8')
jar=Path('C:/Users/89trillion/game/tower-forge/tools/jadx-headless-mcp-0.7.1-all.jar')
PATTERNS={
 'AppLovin/MAX':r'^com\.applovin\.(?:sdk\.(?:AppLovinSdk|AppLovinSdkSettings|AppLovinEventService|AppLovinEventTypes|AppLovinEventParameters|AppLovinPrivacySettings)|impl\.sdk\.(?:EventServiceImpl|network\.(?:PostbackServiceImpl|a|b|c))|mediation\.(?:MaxAd|MaxAdRevenueListener|MaxAdWaterfallInfo|MaxNetworkResponseInfo))$',
 'AppsFlyer/Android':r'^com\.appsflyer\.(?:AppsFlyerLib|AppsFlyerProperties|AFAdRevenueData|MediationNetwork|AppsFlyerConversionListener|internal\.AFg1rSDK)$',
 'InMobi/Android':r'^com\.inmobi\.(?:sdk\.InMobiSdk|unifiedId\.(?:InMobiUnifiedIdService|InMobiUnifiedIdInterface))$',
 'Meta/FacebookCore':r'^com\.facebook\.appevents\.(?:AppEventsLogger|InternalAppEventsLogger|UserDataStore|AppEventQueue|AppEventStore|AppEventUtility)$',
 'Moloco/Android':r'^com\.moloco\.sdk\.publisher\.(?:Moloco|MolocoInitParams|MolocoAdError|MolocoAdRevenue)$',
 'Google/InstallReferrer':r'^com\.android\.installreferrer\.api\.(?:InstallReferrerClient|InstallReferrerClientImpl|ReferrerDetails)$',
}
rows=[]
for src in R.glob('*/*/*/*-sources.jar'):
 dest=src.parent/'sources';dest.mkdir(exist_ok=True);n=0
 with zipfile.ZipFile(src) as z:
  for name in z.namelist():
   if not name.endswith(('.java','.kt','.md','.txt','.xml')):continue
   p=(dest/name).resolve()
   if not p.is_relative_to(dest.resolve()):raise ValueError('unsafe archive path')
   p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(z.read(name));n+=1
 rows.append({'archive':str(src.relative_to(R)),'files_extracted':n})
for path,pat in PATTERNS.items():
 roots=list((R/path).glob('*/classes.jar'))
 for classes in roots:
  if path=='AppLovin/MAX' and classes.parent.name not in ['13.2.0','13.6.4']:continue
  if path=='Meta/FacebookCore' and classes.parent.name!='18.0.3':continue
  out=classes.parent/'decompiled';out.mkdir(exist_ok=True)
  cmd=['java','-Xmx750m','-cp',str(jar)+';'+str(ROOT),'SelectJadx',str(classes),str(out),pat,'40']
  with (classes.parent/'jadx.log').open('wb') as f:p=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT,cwd=ROOT,timeout=150)
  print(path,classes.parent.name,p.returncode,flush=True)
  rows.append({'jar':str(classes.relative_to(R)),'decompiled':str(out.relative_to(R)),'exit_code':p.returncode,'pattern':pat})
(R/'ANALYSIS_MANIFEST.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
