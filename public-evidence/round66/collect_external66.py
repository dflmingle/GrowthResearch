"""Bounded public-history follow-up: no access bypass, no production advertising calls."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
from datetime import datetime,timezone
import requests,json,hashlib,re
from bs4 import BeautifulSoup
ROOT=Path(r'D:\GrowthResearch');OUT=ROOT/'public-evidence/round66';(OUT/'sources').mkdir(parents=True,exist_ok=True)
targets=[
 ('rotate-cdx','https://web.archive.org/cdx/search/cdx?url=www.appbrain.com/app/rotate-rings/com.nebula.rotaterings&output=json&filter=statuscode:200&filter=mimetype:text/html&collapse=timestamp:6&from=2026&to=2026&limit=12'),
 ('meow-cdx','https://web.archive.org/cdx/search/cdx?url=www.appbrain.com/app/meowdoku-brain-puzzle-games/com.oakever.meowdoku&output=json&filter=statuscode:200&filter=mimetype:text/html&collapse=timestamp:6&from=2026&to=2026&limit=12'),
 ('rotate-apkpure-history','https://apkpure.com/rotate-rings/com.nebula.rotaterings/versions'),
 ('meow-apkpure-history','https://apkpure.com/meowdoku-brain-puzzle-games/com.oakever.meowdoku/versions'),
 ('rotate-appbrain','https://www.appbrain.com/app/rotate-rings/com.nebula.rotaterings'),
 ('meow-appbrain','https://www.appbrain.com/app/meowdoku-brain-puzzle-games/com.oakever.meowdoku'),
 ('rotate-appmagic','https://appmagic.rocks/google-play/rotate-rings/com.nebula.rotaterings'),
 ('meow-appmagic','https://appmagic.rocks/google-play/meowdoku-brain-puzzle-games/com.oakever.meowdoku'),
 ('rotate-developer','https://www.hurelax.com/'),
 ('meow-developer','https://oakevergames.com/'),
]
def fetch(item):
 ident,url=item;meta=OUT/'sources'/(ident+'.json')
 if meta.exists():return json.loads(meta.read_text(encoding='utf-8'))
 rec=dict(id='EXT66-'+ident,url=url,observed_utc=datetime.now(timezone.utc).isoformat(),access='Public GET, no login, provided cookies, retries or bypass')
 try:
  with requests.get(url,headers={'User-Agent':'GrowthResearch-public-history-audit/66'},stream=True,timeout=(10,18)) as r:
   chunks=[];size=0
   for b in r.iter_content(65536):
    size+=len(b)
    if size>4_000_000:raise ValueError('bounded response cap exceeded')
    chunks.append(b)
   data=b''.join(chunks)
   rec.update(status=r.status_code,final_url=r.url,response_bytes=len(data),response_sha256=hashlib.sha256(data).hexdigest())
   r.encoding='utf-8';txt=data.decode('utf-8',errors='replace')
   if 'appbrain' in ident:
    soup=BeautifulSoup(txt,'html.parser');canonical=soup.find('link',rel='canonical')
    # Only current aggregate metrics, history access links, version changelog and chart code.
    selectors=['script[type="application/ld+json"]']
    scripts=[]
    for s in soup.find_all('script'):
     st=s.get_text()
     if any(k in st.lower() for k in ['highcharts','chartdata','chart_data','installschart','rankchart']):scripts.append(st[:30000])
    links=[{'text':a.get_text(' ',strip=True)[:120],'url':a.get('href')} for a in soup.find_all('a',href=True) if any(k in a.get('href','').lower() for k in ['history','changelog','ranking'])]
    for tag in soup(['script','style','noscript']):tag.decompose()
    lines=soup.get_text('\n',strip=True).splitlines();out=[];skip=False
    for line in lines:
     if line.startswith('Comments on ') or line in ['User feedback','Ratings and reviews on Google Play']:skip=True
     if skip and (line.startswith('Google Play Rating history') or line.startswith('Google Play Rankings for ') or line=='Store listing'):skip=False
     if not skip:out.append(line)
    payload={'canonical':canonical.get('href') if canonical else None,'product_aggregate_and_history_excerpt':out,'public_history_links':links,'public_chart_script_matches':scripts,'response_full_html_retained':False,'omitted':'comments/reviewers and irrelevant full HTML'}
    p=OUT/'sources'/(ident+'.metadata.json');p.write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8')
    text='\n'.join(out)
   else:
    p=OUT/'sources'/(ident+'.response');p.write_bytes(data)
    soup=BeautifulSoup(txt,'html.parser')
    for tag in soup(['script','style','noscript']):tag.decompose()
    text=soup.get_text('\n',strip=True) if '<html' in txt[:1000].lower() else txt
   t=OUT/'sources'/(ident+'.txt');t.write_text(text,encoding='utf-8')
   rec.update(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),text_path=t.relative_to(ROOT).as_posix(),text_sha256=hashlib.sha256(t.read_bytes()).hexdigest())
 except Exception as e:rec['error']=type(e).__name__+': '+str(e)
 meta.write_text(json.dumps(rec,ensure_ascii=False,indent=2),encoding='utf-8');return rec
if __name__=='__main__':
 rows=[]
 with ThreadPoolExecutor(max_workers=5) as pool:
  for f in as_completed([pool.submit(fetch,t) for t in targets]):
   x=f.result();rows.append(x);print(json.dumps({k:x.get(k) for k in ['id','status','response_bytes','error']},ensure_ascii=True),flush=True)
 (OUT/'FETCH_LEDGER.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
