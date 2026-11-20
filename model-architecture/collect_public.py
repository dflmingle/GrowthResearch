"""Public architecture research only. No ad production API or SDK execution."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlencode, urljoin, urlsplit, parse_qs
import datetime, hashlib, json, re
import requests
from bs4 import BeautifulSoup

R=Path(__file__).resolve().parent.parent
O=R/'model-architecture'; (O/'public').mkdir(parents=True,exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
if not (O/'HISTORY.before60.json').exists():
    paths=list(R.glob('[0-5][0-9]_*.md'))+[R/'prediction-system/EVIDENCE_GRAPH.json',R/'EVIDENCE_INDEX.md',R/'EVIDENCE_MANIFEST.json']
    paths += [p for p in (R/'prediction-validation').rglob('*') if p.is_file() and '__pycache__' not in str(p)]
    dump(O/'HISTORY.before60.json',[dict(path=p.relative_to(R).as_posix(),sha256=sha(p)) for p in paths])
for old,new in [('prediction-system/EVIDENCE_GRAPH.json','EVIDENCE_GRAPH.before60.json'),('EVIDENCE_INDEX.md','EVIDENCE_INDEX.before60.md'),('EVIDENCE_MANIFEST.json','EVIDENCE_MANIFEST.before60.json')]:
    if not (O/new).exists():(O/new).write_bytes((R/old).read_bytes())

QUERIES={
 'axon-production':'site:applovin.com Axon "model" "training" architecture',
 'axon-representations':'AppLovin Axon embeddings multi-task learning engineering talk',
 'axon-engineering':'AppLovin Axon technical interview real time inference deep learning architecture',
 'vector-models':'site:unity.com Vector "model" "training" architecture',
 'vector-conference':'Unity Ads Vector machine learning GDC talk transfer learning',
 'vector-research':'Unity Ads lifetime value prediction multi task learning paper',
 'axon-patent':'AppLovin patent lifetime value machine learning prediction',
 'unity-patent':'Unity Technologies patent lifetime value advertisement prediction',
 'axon-whitepaper':'site:applovin.com Axon reinforcement learning prediction cold start',
 'vector-embeddings':'site:unity.com Vector embeddings foundation model player',
 'unity-d28':'site:unity.com "Day 28" "predict"',
 'axon-architecture':'site:axon.ai "model" "data"',
}

def fetch(item):
    ident,url=item
    base=O/'public'/ident
    if base.with_suffix('.meta.json').exists():return json.loads(base.with_suffix('.meta.json').read_text('utf-8'))
    row=dict(id=ident,url=url,acquired_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),method='public GET only; no authentication or access-control bypass')
    try:
        a=requests.get(url,timeout=(7,22),headers={'User-Agent':'Mozilla/5.0'})
        raw=base.with_suffix('.raw');raw.write_bytes(a.content)
        soup=BeautifulSoup(a.content,'html.parser')
        links=[]
        for tag in soup.find_all('a',href=True):
            href=urljoin(a.url,tag['href'])
            if href.startswith('http'):links.append(dict(text=tag.get_text(' ',strip=True)[:180],url=href))
        for tag in soup(['script','style','noscript','svg']):tag.decompose()
        text=soup.get_text('\n',strip=True)
        txt=base.with_suffix('.txt');txt.write_text(text,encoding='utf-8')
        # RSS result links are elements rather than anchors.
        if '<rss' in a.text[:500]:
            import xml.etree.ElementTree as ET
            links=[dict(text=it.findtext('title',''),url=it.findtext('link',''),description=it.findtext('description','')) for it in ET.fromstring(a.content).findall('.//item')]
        dump(base.with_suffix('.links.json'),links)
        row.update(status=a.status_code,final_url=a.url,bytes=len(a.content),raw_path=raw.relative_to(R).as_posix(),sha256=sha(raw),
          text_path=txt.relative_to(R).as_posix(),text_sha256=sha(txt),title=(soup.title.get_text(' ',strip=True) if soup.title else ''),links=len(links))
    except Exception as e:row['error']=type(e).__name__+': '+str(e)[:180]
    dump(base.with_suffix('.meta.json'),row)
    return row

if __name__=='__main__':
    import sys
    if len(sys.argv)>1 and sys.argv[1]=='direct':
        targets=json.loads((O/'DIRECT_TARGETS.json').read_text('utf-8'))
    else:
        targets=[(name,'https://www.google.com/search?'+urlencode({'q':q})) for name,q in QUERIES.items()]
    with ThreadPoolExecutor(max_workers=4) as pool:
        result=list(pool.map(fetch,targets))
    dump(O/('DIRECT_FETCHES.json' if len(sys.argv)>1 else 'SEARCH_FETCHES.json'),result)
    print(json.dumps([dict(id=x['id'],status=x.get('status'),error=x.get('error'),bytes=x.get('bytes'),links=x.get('links')) for x in result],indent=2))
