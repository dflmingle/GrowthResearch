import requests,json,hashlib,concurrent.futures
from pathlib import Path
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parent
def get(item):
    key,url=item
    try:
        r=requests.get(url,timeout=35,headers={'User-Agent':'ResearchEvidenceAudit/1.0'})
        ext='.pdf' if r.content[:4]==b'%PDF' else ('.docx' if r.content[:2]==b'PK' else '.html')
        p=ROOT/'sources'/(key+ext)
        p.write_bytes(r.content)
        rec={'id':key,'url':url,'final_url':r.url,'status':r.status_code,'path':str(p.relative_to(ROOT.parent)),'sha256':hashlib.sha256(r.content).hexdigest(),'bytes':len(r.content)}
        if 'json' in r.headers.get('Content-Type',''):
            j=r.json()
            works=j.get('results',[j])
            rec['works']=[{'title':w.get('title'),'doi':w.get('doi'),'authors':[a['author']['display_name'] for a in w.get('authorships',[])],'locations':w.get('locations',[])} for w in works]
        elif p.suffix=='.html':
            soup=BeautifulSoup(r.content,'html.parser')
            for s in soup(['script','style']):s.decompose()
            t=soup.get_text('\n',strip=True)
            p.with_suffix('.txt').write_text(t,encoding='utf-8')
            rec['text_preview']=t[:8000]
            rec['links']=[{'text':a.get_text(' ',strip=True),'url':a.get('href')} for a in soup.select('a[href]') if any(x in (a.get_text(' ',strip=True)+' '+a.get('href','')).lower() for x in ['uken','data','monet','mag inter','pdf','doi'])][:70]
        return rec
    except Exception as e:return {'id':key,'url':url,'error':str(e)}
if __name__=='__main__':
    import sys
    if sys.argv[1]=='first':
        tasks=[('unity-paper-openalex','https://api.openalex.org/works/https://doi.org/10.1145/3582927'),('drachen-data','https://andersdrachen.com/data/'),('mag-crossref','https://api.openalex.org/works?search=%22MAG%20Interactive%22&per-page=12'),('uken-search','https://www.google.com/search?q=%22Uken%22+%22300%2C000%22+data'),('mag-search','https://www.google.com/search?q=%22MAG+Interactive%22+%22rewarded%22+research+data')]
    else:tasks=json.loads((ROOT/sys.argv[1]).read_text(encoding='utf-8'))
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:out=list(ex.map(get,tasks))
    dest=ROOT/('FETCH_'+Path(sys.argv[1]).stem+'.json')
    dest.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
    for x in out:
        small={k:v for k,v in x.items() if k not in ['text_preview','links','works']}
        small['preview']=x.get('text_preview','')[:500]
        small['titles']=[w.get('title') for w in x.get('works',[])]
        print(json.dumps(small,ensure_ascii=False))
