"""Public official metadata/legal GET only. Not an SDK/network client."""
from pathlib import Path
from urllib.parse import urlsplit,urljoin
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
import requests,json,hashlib,datetime,sys

D=Path(__file__).resolve().parent
ALLOWED={'www.applovin.com','applovin.com','unity.com','unity3d.com','www.unity.com','api.github.com','raw.githubusercontent.com','developers.is.com','docs.unity.com'}
def get(item):
    key,url=item
    out=dict(id=key,url=url,acquired_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),redirects=[])
    try:
        current=url
        for _ in range(6):
            p=urlsplit(current)
            assert p.scheme=='https' and p.hostname in ALLOWED,'Outside official metadata/legal allowlist'
            response=requests.get(current,timeout=28,allow_redirects=False,headers={'User-Agent':'OfficialSampleLicenseAudit/1.0'})
            if response.is_redirect:
                dest=urljoin(current,response.headers['Location'])
                out['redirects'].append(dict(source=current,target=dest,status=response.status_code));current=dest
                continue
            break
        else:raise ValueError('Redirect limit')
        assert len(response.content)<=8_000_000,'Oversize metadata/legal response'
        raw=D/'sources'/(key+'.raw');assert not raw.exists(),'Refuse duplicate fetch overwrite'
        raw.write_bytes(response.content)
        out.update(status=response.status_code,final_url=current,path=raw.relative_to(D.parent).as_posix(),
          sha256=hashlib.sha256(response.content).hexdigest(),bytes=len(response.content),content_type=response.headers.get('Content-Type'))
        if 'html' in response.headers.get('Content-Type',''):
            soup=BeautifulSoup(response.content,'html.parser')
            out['links']=[dict(text=a.get_text(' ',strip=True),url=urljoin(current,a['href'])) for a in soup.select('a[href]')]
            for node in soup(['script','style']):node.decompose()
            text=soup.get_text('\n',strip=True)
        else:text=response.content.decode('utf-8-sig')
        readable=raw.with_suffix('.txt');readable.write_text(text,encoding='utf-8')
        out.update(text_path=readable.relative_to(D.parent).as_posix(),text_sha256=hashlib.sha256(readable.read_bytes()).hexdigest(),preview=text[:300])
    except Exception as exc:out['error']=str(exc)
    return out
if __name__=='__main__':
    batch=D/sys.argv[1]
    with ThreadPoolExecutor(max_workers=3) as executor:results=list(executor.map(get,json.loads(batch.read_text(encoding='utf-8-sig'))))
    dest=D/('FETCH_'+batch.stem+'.json');assert not dest.exists()
    dest.write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for x in results:print(json.dumps({k:v for k,v in x.items() if k not in ['links','preview']},ensure_ascii=False)[:800])
