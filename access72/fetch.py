from pathlib import Path
import requests,json,datetime,hashlib,sys,concurrent.futures,ipaddress
from urllib.parse import urlsplit,urljoin
from bs4 import BeautifulSoup
D=Path(__file__).resolve().parent
def public_url(u):
    p=urlsplit(u)
    if p.scheme not in ['http','https'] or not p.hostname:return False
    if p.hostname.lower() in ['localhost','localhost.localdomain']:return False
    try:return ipaddress.ip_address(p.hostname).is_global
    except ValueError:return True
def fetch(x):
    key,url=x;out=dict(id=key,url=url,acquired_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),redirects=[])
    try:
        u=url
        for _ in range(5):
            assert public_url(u),'Non-public redirect blocked'
            r=requests.get(u,timeout=28,allow_redirects=False,headers={'User-Agent':'PublicResearchAudit/1.0'})
            if r.is_redirect:
                new=urljoin(u,r.headers['Location']);out['redirects'].append(dict(status=r.status_code,source=u,target=new));u=new;continue
            break
        else:raise RuntimeError('Redirect limit')
        p=D/'sources'/(key+'.raw');assert not p.exists(),'Do not overwrite response'
        p.write_bytes(r.content);out.update(status=r.status_code,final_url=u,path=p.relative_to(D.parent).as_posix(),sha256=hashlib.sha256(r.content).hexdigest(),bytes=len(r.content),content_type=r.headers.get('Content-Type'))
        if 'html' in r.headers.get('Content-Type',''):
            s=BeautifulSoup(r.content,'html.parser');out['links']=[dict(text=a.get_text(' ',strip=True),url=urljoin(u,a['href'])) for a in s.select('a[href]')]
            main=s.select_one('article') or s.select_one('main') or s
            for z in main(['script','style']):z.decompose()
            txt=main.get_text('\n',strip=True)
        else:txt=r.text
        t=p.with_suffix('.txt');t.write_text(txt,encoding='utf-8');out.update(text_path=t.relative_to(D.parent).as_posix(),text_sha256=hashlib.sha256(t.read_bytes()).hexdigest(),preview=txt[:550])
    except Exception as e:out['error']=str(e)
    return out
if __name__=='__main__':
    p=D/sys.argv[1];xs=json.loads(p.read_text(encoding='utf-8-sig'))
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:out=list(ex.map(fetch,xs))
    dest=D/('FETCH_'+p.stem+'.json');assert not dest.exists();dest.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
    for x in out:print(json.dumps({k:v for k,v in x.items() if k!='links'},ensure_ascii=False)[:1450])
