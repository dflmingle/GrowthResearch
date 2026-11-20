from pathlib import Path
import requests,json,datetime,concurrent.futures,re
from bs4 import BeautifulSoup
R=Path(__file__).resolve().parent/'public-research/deep';R.mkdir(exist_ok=True)
urls={
 'jewel-history':'https://ws75.aptoide.com/api/7/app/get/package_name=color.number.paint.pixle.art.sort.jigsaw',
 'jewel-versions':'https://ws75.aptoide.com/api/7/app/getVersions/package_name=color.number.paint.pixle.art.sort.jigsaw/limit=10',
 'jewel-policy':'https://sites.google.com/view/brilliantsort-privacypolicy',
 'oakever-policy':'https://oakevergames.com/pp.html',
 'hurelax-policy':'https://www.hurelax.com/privacy-policy',
 'zego-policy':'https://zegostudio.com/privacy-policy.html',
 'adjust-externalid':'https://dev.adjust.com/en/sdk/android/features/external-device-id/',
 'appsflyer-cuid':'https://dev.appsflyer.com/hc/docs/android-sdk-reference-appsflyerlib#setcustomeruserid',
 'firebase-userid':'https://firebase.google.com/docs/analytics/userid',
 'metica-privacy':'https://www.metica.com/privacy-policy',
 'adworth-search':'https://www.google.com/search?q=%22AdWorthEvent%22+%22Bulldog%22',
 'bulldog-search':'https://www.google.com/search?q=%22BulldogSdk%22+game',
 'tatagame-search':'https://www.google.com/search?q=%22tatagame%22+%22Bulldog%22',
}
def get(k,u):
 x={'id':k,'url':u,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  a=requests.get(u,timeout=24);x.update(status=a.status_code,final_url=a.url,bytes=len(a.content));(R/(k+'.html')).write_bytes(a.content)
  try:o=a.json();(R/(k+'.json')).write_text(json.dumps(o,indent=2),encoding='utf-8')
  except:pass
  s=BeautifulSoup(a.text,'html.parser');[n.decompose() for n in s(['script','style'])];t=s.get_text('\n',strip=True);(R/(k+'.txt')).write_text(t,encoding='utf-8');x['title']=s.title.get_text() if s.title else None
 except Exception as e:x['error']=str(e)
 return x
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as e:out=list(e.map(lambda p:get(*p),urls.items()))
(R/'fetches.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
for x in out:print(x['id'],x.get('status'),x.get('title'),flush=True)
