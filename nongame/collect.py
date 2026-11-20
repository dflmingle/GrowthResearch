from pathlib import Path
import requests,json,datetime,hashlib,concurrent.futures,sys,re
from bs4 import BeautifulSoup
R=Path(__file__).resolve().parent
sys.stdout.reconfigure(encoding='utf-8')
def fetch(k,u):
 row={'id':k,'url':u,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'method':'public HTTP GET, no script execution, no persistent cookies'}
 try:
  a=requests.get(u,timeout=(8,22),allow_redirects=True)
  row.update(status=a.status_code,final_url=a.url,bytes=len(a.content),sha256=hashlib.sha256(a.content).hexdigest())
  (R/(k+'.raw')).write_bytes(a.content)
  if len(a.content)>12_000_000:raise ValueError('response too large for parsing')
  s=BeautifulSoup(a.content,'html.parser')
  row['title']=s.title.get_text(' ',strip=True) if s.title else None
  links=[{'text':n.get_text(' ',strip=True)[:160],'href':n['href']} for n in s.find_all('a',href=True)]
  scripts=[{'src':n.get('src'),'type':n.get('type'),'inline_mentions':[m.group(0)[:250] for m in re.finditer(r'.{0,65}(?:applovin|axonc?dn|axon\(|unityads|ironsource).{0,90}',n.get_text(),re.I)][:12]} for n in s.find_all('script')]
  (R/(k+'-links.json')).write_text(json.dumps(links,ensure_ascii=False,indent=2),encoding='utf-8')
  (R/(k+'-scripts.json')).write_text(json.dumps(scripts,ensure_ascii=False,indent=2),encoding='utf-8')
  [n.decompose() for n in s(['script','style','nav','footer'])]
  (R/(k+'.txt')).write_text(s.get_text('\n',strip=True),encoding='utf-8')
 except Exception as e:row['error']=str(e)
 return row
def batch(name,urls):
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:rows=list(pool.map(lambda a:fetch(*a),urls.items()))
 (R/('fetches-'+name+'.json')).write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
 for row in rows:print(row['id'],row.get('status'),row.get('title') or row.get('error',''),flush=True)
 return rows
if __name__=='__main__':
 batch('initial',{
 'axon-docs':'https://support.axon.ai/en/growth/promoting-your-websites/track-and-optimize',
 'axon-docs-root':'https://support.axon.ai/llms.txt',
 'axon-case-studies':'https://www.axon.ai/en/success-stories',
 'applovin-policy':'https://www.applovin.com/privacy/',
 'unity-ad-partners':'https://unity.com/legal/advertising-partners',
 'unity-policy':'https://unity.com/legal/game-player-and-app-user-privacy-policy',
 'wurl-privacy':'https://www.wurl.com/privacy-policy/',
 'wurl-home':'https://www.wurl.com/',
 'utility-zedge':'https://www.zedge.net/privacy',
 'utility-weatherbug':'https://www.weatherbug.com/legal/privacy',
 'utility-truecaller':'https://www.truecaller.com/privacy-policy',
 'content-newsbreak':'https://www.newsbreak.com/terms/privacy-policy',
 'content-dailyhunt':'https://m.dailyhunt.in/privacypolicy',
 'content-wattpad':'https://policies.wattpad.com/privacy/',
 'shopping-temu':'https://www.temu.com/privacy-and-cookie-policy.html',
 'shopping-shein':'https://www.shein.com/Privacy-Security-Policy-a-282.html',
 'shopping-aliexpress':'https://terms.alicdn.com/legal-agreement/terms/suit_bu1_aliexpress/suit_bu1_aliexpress202204112216_41097.html',
 'site-ridge':'https://ridge.com/pages/privacy-policy',
 'site-hexclad':'https://hexclad.com/pages/privacy-policy',
 'site-jonesroad':'https://www.jonesroadbeauty.com/pages/privacy-policy',
 })
