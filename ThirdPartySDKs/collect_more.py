from collect_sdk import acquire,R
import json,concurrent.futures,requests,datetime,hashlib,zipfile,re
G='https://dl.google.com/dl/android/maven2';M='https://repo.maven.apache.org/maven2'
specs=[
 ('Unity','LevelPlay','com.unity3d.ads-mediation','mediation-sdk','9.3.0',M,'core'),
 ('Unity','LevelPlay','com.unity3d.ads-mediation','mediation-sdk','9.5.0',M,'core'),
 ('Google','FirebaseRemoteConfig','com.google.firebase','firebase-config',None,G,'core'),
 ('Google','FirebaseCommon','com.google.firebase','firebase-common',None,G,'core'),
 ('Google','MeasurementAPI','com.google.android.gms','play-services-measurement-api','22.4.0',G,'core'),
 ('Google','MeasurementSDK','com.google.android.gms','play-services-measurement-sdk','22.4.0',G,'core'),
 ('Google','MeasurementImpl','com.google.android.gms','play-services-measurement-impl','22.4.0',G,'core'),
 ('Google','MeasurementBase','com.google.android.gms','play-services-measurement-base','22.4.0',G,'core'),
 ('Google','MeasurementSDKAPI','com.google.android.gms','play-services-measurement-sdk-api','22.4.0',G,'core'),
 ('Google','MobileAdsLite','com.google.android.gms','play-services-ads-lite','25.1.0',G,'core'),
 ('Google','MobileAdsBase','com.google.android.gms','play-services-ads-base','25.1.0',G,'core'),
 ('Google','AdsIdentifier','com.google.android.gms','play-services-ads-identifier','17.1.0',G,'core'),
 ('Google','AppSet','com.google.android.gms','play-services-appset','16.0.0',G,'core'),
 ('Mintegral','Android','com.mbridge.msdk.oversea','mbridge_android_sdk','16.9.91','https://dl-maven-android.mintegral.com/repository/mbridge_android_sdk_oversea','core'),
 ('Pangle','Android','com.pangle.global','pag-sdk','7.8.5.2','https://artifact.bytedance.com/repository/pangle','core'),
 ('Pangle','Android','com.pangle.global','pag-sdk','8.1.0.3','https://artifact.bytedance.com/repository/pangle','core'),
]
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:out=list(ex.map(acquire,specs))
(R/'ADDITIONAL_MANIFEST.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
urls={
 'tiktok-readme':'https://raw.githubusercontent.com/tiktok/tiktok-business-android-sdk/main/README.md',
 'tiktok-readme-master':'https://raw.githubusercontent.com/tiktok/tiktok-business-android-sdk/master/README.md',
 'tiktok-release-161':'https://api.github.com/repos/tiktok/tiktok-business-android-sdk/releases/tags/v1.6.1',
 'tiktok-release-171':'https://api.github.com/repos/tiktok/tiktok-business-android-sdk/releases/tags/v1.7.1',
 'adjust-release':'https://api.github.com/repos/adjust/android_sdk/releases/tags/v5.8.1',
 'metica-readme':'https://raw.githubusercontent.com/Metica/metica-sdk-android/main/README.md',
 'metica-docs':'https://docs.metica.com/',
 'learnings-github':'https://api.github.com/orgs/Learnings/repos?per_page=100',
 'applovin-adapters-license':'https://raw.githubusercontent.com/AppLovin/AppLovin-MAX-SDK-Android/master/LICENSE',
 'firebase-github-config':'https://raw.githubusercontent.com/firebase/firebase-android-sdk/master/firebase-config/src/main/java/com/google/firebase/remoteconfig/FirebaseRemoteConfig.java',
}
p=R/'Discovery';p.mkdir(exist_ok=True);rows=[]
for k,u in urls.items():
 x={'id':k,'url':u,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  z=requests.get(u,timeout=(10,35));x.update(status=z.status_code,final_url=z.url)
  f=p/(k+('.json' if 'api.github' in u else '.txt'));f.write_bytes(z.content);x['path']=str(f.relative_to(R));x['sha256']=hashlib.sha256(z.content).hexdigest()
 except Exception as e:x['error']=str(e)
 rows.append(x);print(k,x.get('status'),flush=True)
(R/'DISCOVERY_MANIFEST.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
