from pathlib import Path
import requests,json,datetime,hashlib,concurrent.futures,sys
from bs4 import BeautifulSoup
R=Path(__file__).resolve().parent;R.mkdir(exist_ok=True);sys.stdout.reconfigure(encoding='utf-8')
URLS={
 'unity-ir-releases':'https://investors.unity.com/news/default.aspx',
 'unity-ir-financials':'https://investors.unity.com/financials/quarterly-results/default.aspx',
 'applovin-ir-financials':'https://investors.applovin.com/financials/quarterly-results/default.aspx',
 'applovin-ir-releases':'https://investors.applovin.com/news/default.aspx',
 'unity-vector':'https://unity.com/products/unity-vector',
 'unity-ads':'https://unity.com/products/unity-ads',
 'unity-blog-sitemap':'https://unity.com/sitemap.xml',
 'unity-runtime-doc':'https://docs.unity.com/grow/ads/privacy/runtime-data-sharing',
 'unity-roas-doc':'https://docs.unity.com/grow/acquire/roas-campaigns',
 'unity-exchange':'https://unity.com/products/unity-exchange',
 'unity-privacy':'https://unity.com/legal/game-player-and-app-user-privacy-policy',
}
def fetch(k,u):
 row={'id':k,'url':u,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  a=requests.get(u,timeout=(10,30));row.update(status=a.status_code,final_url=a.url,bytes=len(a.content),sha256=hashlib.sha256(a.content).hexdigest())
  (R/(k+'.html')).write_bytes(a.content);s=BeautifulSoup(a.content,'html.parser');row['title']=s.title.get_text(' ',strip=True) if s.title else None
  links=[{'text':n.get_text(' ',strip=True)[:200],'href':n['href']} for n in s.find_all('a',href=True)];(R/(k+'-links.json')).write_text(json.dumps(links,ensure_ascii=False,indent=2),encoding='utf-8')
  [n.decompose() for n in s(['script','style','nav','footer'])];(R/(k+'.txt')).write_text(s.get_text('\n',strip=True),encoding='utf-8')
 except Exception as e:row['error']=str(e)
 return row
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:rows=list(ex.map(lambda a:fetch(*a),URLS.items()))
 (R/'fetches-initial.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
 for r in rows:print(r['id'],r.get('status'),r.get('title'),flush=True)
