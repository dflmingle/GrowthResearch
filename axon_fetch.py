from pathlib import Path
import requests,concurrent.futures,json,datetime,sys,re
from bs4 import BeautifulSoup
R=Path(__file__).resolve().parent/'axon';R.mkdir(exist_ok=True);sys.stdout.reconfigure(encoding='utf-8')
URLS={
 'support-applovin-ua':'https://support.applovin.com/en/ua/',
 'support-axon-growth':'https://support.axon.ai/en/growth/',
 'adjust-integration':'https://support.applovin.com/en/ua/attribution/adjust/',
 'appsflyer-integration':'https://support.applovin.com/en/ua/attribution/appsflyer/',
 'applovin-axon':'https://www.applovin.com/axon/',
 'axon-home':'https://www.axon.ai/',
 'applovin-privacy':'https://legal.applovin.com/privacy/',
 'applovin-sitemap':'https://www.applovin.com/sitemap_index.xml',
 'axon-sitemap':'https://www.axon.ai/sitemap.xml',
 'applovin-success':'https://www.applovin.com/success-stories/',
 'appsflyer-applovin':'https://support.appsflyer.com/hc/en-us/articles/207032066-AppLovin-integration-configuration',
 'adjust-applovin':'https://help.adjust.com/en/partner-setup/applovin',
}
def fetch(k,u):
 x={'id':k,'url':u,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  a=requests.get(u,timeout=(10,30));x.update(status=a.status_code,final_url=a.url,bytes=len(a.content),type=a.headers.get('Content-Type'));(R/(k+'.html')).write_bytes(a.content)
  s=BeautifulSoup(a.content,'html.parser');x['title']=s.title.get_text(' ',strip=True) if s.title else None
  links=[{'text':t.get_text(' ',strip=True)[:180],'href':t['href']} for t in s.find_all('a',href=True)]
  (R/(k+'-links.json')).write_text(json.dumps(links,ensure_ascii=False,indent=2),encoding='utf-8')
  [n.decompose() for n in s(['script','style','nav','footer'])];(R/(k+'.txt')).write_text(s.get_text('\n',strip=True),encoding='utf-8')
 except Exception as e:x['error']=str(e)
 return x
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:out=list(ex.map(lambda p:fetch(*p),URLS.items()))
 (R/'fetches-initial.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
 for x in out:print(x['id'],x.get('status'),x.get('title'),x.get('final_url'),flush=True)
