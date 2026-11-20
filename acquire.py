from pathlib import Path
import requests, json, hashlib, datetime, concurrent.futures, sys, re, zipfile
from bs4 import BeautifulSoup
sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path(__file__).resolve().parent
TARGETS={'car-race':'com.dino.race.master','meowdoku':'com.oakever.meowdoku','rotate-rings':'com.nebula.rotaterings','amaze-go':'com.oakever.arrows','jewel-coloring':'color.number.paint.pixle.art.sort.jigsaw'}
HEADERS={'User-Agent':'Mozilla/5.0'}
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def page(slug,package):
 p=ROOT/slug/'public';p.mkdir(parents=True,exist_ok=True)
 url=f'https://play.google.com/store/apps/details?id={package}&hl=en&gl=US';out={'package':package,'accessed_utc':now(),'url':url}
 try:
  r=requests.get(url,headers=HEADERS,timeout=30);out.update(status=r.status_code,final_url=r.url)
  (p/'google-play.html').write_bytes(r.content)
  soup=BeautifulSoup(r.text,'html.parser');text=soup.get_text('\n',strip=True);(p/'google-play.txt').write_text(text,encoding='utf-8')
  out['title']=soup.title.get_text() if soup.title else None
  out['structured_data']=[json.loads(s.string) for s in soup.find_all('script',type='application/ld+json') if s.string]
  out['links']=[{'label':a.get_text(' ',strip=True),'url':a.get('href')} for a in soup.find_all('a') if a.get('href') and (a.get('href').startswith('mailto:') or any(t in a.get_text(' ',strip=True) for t in ['Website','Privacy','developer']))]
  print(slug,'PLAY',r.status_code,out['title'],flush=True)
 except Exception as ex:out['error']=str(ex)
 (p/'identity.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
 return out
def download(slug,package):
 p=ROOT/slug/'samples';p.mkdir(parents=True,exist_ok=True);url=f'https://d.apkpure.net/b/XAPK/{package}?version=latest';out={'package':package,'requested_utc':now(),'url':url}
 try:
  r=requests.get(url,headers=HEADERS,timeout=(20,60),stream=True);out.update(status=r.status_code,final_url=r.url,content_type=r.headers.get('Content-Type'),content_length=r.headers.get('Content-Length'))
  if r.status_code!=200:
   out['response_excerpt']=r.raw.read(1500).decode('utf-8',errors='replace');return out
  declared=int(r.headers.get('Content-Length') or 0)
  if declared>1024**3:out['error']='Size exceeds 1GiB research cap';return out
  f=p/'latest.package';h=hashlib.sha256();size=0
  with f.open('wb') as dst:
   for block in r.iter_content(1024*1024):
    size+=len(block)
    if size>1024**3:raise RuntimeError('Stream exceeds 1GiB research cap')
    h.update(block);dst.write(block)
  out.update(bytes=size,sha256=h.hexdigest(),completed_utc=now(),zip=zipfile.is_zipfile(f))
  if zipfile.is_zipfile(f):
   with zipfile.ZipFile(f) as z:
    names=z.namelist();out['entries']=names
    if 'manifest.json' in names:
     out['manifest']=json.loads(z.read('manifest.json'));(p/'xapk-manifest.json').write_text(json.dumps(out['manifest'],ensure_ascii=False,indent=2),encoding='utf-8')
    suffix='.xapk' if any(x.endswith('.apk') for x in names) else '.apk'
   dest=f.with_suffix(suffix);f.rename(dest);out['file']=dest.name
  else:out['error']='Response is not an APK/XAPK ZIP archive'
  print(slug,'DOWNLOAD',out.get('bytes'),out.get('file'),out.get('error'),flush=True)
 except Exception as ex:out['error']=str(ex);print(slug,'DOWNLOAD ERROR',str(ex),flush=True)
 finally:(p/'acquisition.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
 return out
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:list(pool.map(lambda kv:page(*kv),TARGETS.items()))
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:list(pool.map(lambda kv:download(*kv),[(s,p) for s,p in TARGETS.items() if s!='car-race']))
