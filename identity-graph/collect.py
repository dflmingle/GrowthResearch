from pathlib import Path
import requests,json,datetime,hashlib,concurrent.futures,sys
from bs4 import BeautifulSoup
R=Path(__file__).resolve().parent
sys.stdout.reconfigure(encoding='utf-8')
def fetch(k,u):
 row={'id':k,'url':u,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'method':'public GET; no SDK/JS execution; no personal identifier or credentials'}
 try:
  a=requests.get(u,timeout=(8,24));row.update(status=a.status_code,final_url=a.url,bytes=len(a.content),sha256=hashlib.sha256(a.content).hexdigest())
  (R/(k+'.raw')).write_bytes(a.content)
  s=BeautifulSoup(a.content,'html.parser');row['title']=s.title.get_text(' ',strip=True) if s.title else None
  links=[{'text':n.get_text(' ',strip=True)[:140],'href':n['href']} for n in s.find_all('a',href=True)]
  (R/(k+'-links.json')).write_text(json.dumps(links,ensure_ascii=False,indent=2),encoding='utf-8')
  [n.decompose() for n in s(['script','style','nav','footer'])]
  (R/(k+'.txt')).write_text(s.get_text('\n',strip=True),encoding='utf-8')
 except Exception as e:row['error']=str(e)
 return row
def batch(name,urls):
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:rows=list(pool.map(lambda x:fetch(*x),urls.items()))
 (R/('fetches-'+name+'.json')).write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
 for x in rows:print(x['id'],x.get('status'),x.get('title') or x.get('error',''),flush=True)
 return rows
if __name__=='__main__':batch('initial',{
 'unity-player-accounts':'https://docs.unity.com/ugs/en-us/manual/authentication/manual/unity-player-accounts',
 'unity-player-id':'https://docs.unity.com/ugs/en-us/manual/authentication/manual/player-id',
 'unity-organization-id':'https://docs.unity.com/ugs/en-us/manual/authentication/manual/organization-id',
 'unity-auth-overview':'https://docs.unity.com/ugs/en-us/manual/authentication/manual/overview',
 'unity-accounts-custom':'https://docs.unity.com/ugs/en-us/manual/authentication/manual/platform-signin-unity-player',
 'unity-anonymous':'https://docs.unity.com/ugs/en-us/manual/authentication/manual/use-anon-sign-in',
 'unity-auth-package':'https://packages.unity.com/com.unity.services.authentication',
 'unity-upa-package':'https://packages.unity.com/com.unity.services.playeraccounts',
 'unity-github-auth':'https://api.github.com/repos/needle-mirror/com.unity.services.authentication',
 'liveramp-unity':'https://liveramp.com/blog/unity-liveramp-rampid/',
 'liveramp-rampid':'https://docs.liveramp.com/connect/en/rampid.html',
 'liveramp-identity':'https://liveramp.com/our-platform/identity-resolution/',
 'google-appset':'https://developers.google.com/android/guides/app-set-id',
 'google-ads-id':'https://support.google.com/googleplay/android-developer/answer/6048248?hl=en',
 'apple-idfv':'https://developer.apple.com/documentation/uikit/uidevice/identifierforvendor',
 'apple-idfa':'https://developer.apple.com/documentation/adsupport/asidentifiermanager/advertisingidentifier',
 'google-cookie-match':'https://developers.google.com/authorized-buyers/rtb/cookie-guide',
 'applovin-how-ads':'https://legal.applovin.com/how-applovin-shows-you-ads/',
 'unity-exchange-eids':'https://docs.unity.com/en-us/grow/programmatic/unity-exchange/extended-identifiers.md',
})
