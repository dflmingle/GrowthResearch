from pathlib import Path
import requests,hashlib,json,datetime,concurrent.futures,sys
from bs4 import BeautifulSoup
D=Path(__file__).resolve().parent
def fetch(spec):
    key,url=spec
    t=datetime.datetime.now(datetime.timezone.utc).isoformat()
    try:
        r=requests.get(url,timeout=35,headers={'User-Agent':'PublicResearchAudit/1.0'})
        suffix='.pdf' if r.content.startswith(b'%PDF') else '.raw'
        p=D/'sources'/(key+suffix)
        if p.exists():raise RuntimeError('Do not overwrite previous response: '+str(p))
        p.write_bytes(r.content)
        x=dict(id=key,url=url,acquired_utc=t,status=r.status_code,final_url=r.url.split('?')[0] if 'X-Amz-' in r.url else r.url,path=p.relative_to(D.parent).as_posix(),sha256=hashlib.sha256(r.content).hexdigest(),bytes=len(r.content),content_type=r.headers.get('Content-Type'))
        if 'json' in r.headers.get('Content-Type',''):
            j=r.json()
            if isinstance(j,dict):
                x['json_keys']=list(j)
                if isinstance(j.get('results'),list):x['titles']=[a.get('title') for a in j['results']]
        elif suffix!='.pdf':
            soup=BeautifulSoup(r.content,'html.parser')
            for a in soup(['script','style']):a.decompose()
            txt=soup.get_text('\n',strip=True)
            p.with_suffix('.txt').write_text(txt,encoding='utf-8')
            x['links']=[dict(text=a.get_text(' ',strip=True),url=a['href']) for a in soup.select('a[href]')]
            x['preview']=txt[:1000]
        return x
    except Exception as e:return dict(id=key,url=url,acquired_utc=t,error=str(e))
if __name__=='__main__':
    specs=json.loads((D/sys.argv[1]).read_text(encoding='utf-8-sig'))
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:out=list(ex.map(fetch,specs))
    dest=D/('FETCH_'+Path(sys.argv[1]).stem+'.json')
    assert not dest.exists()
    dest.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
    for x in out:print(json.dumps({k:v for k,v in x.items() if k not in ['links']},ensure_ascii=False)[:1800])

