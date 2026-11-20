"""Bounded primary-source follow-up for cold-start hypotheses only."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin
import datetime,hashlib,json,requests,re
from bs4 import BeautifulSoup
R=Path(__file__).resolve().parents[2];O=Path(__file__).resolve().parent
(O/'public').mkdir(parents=True,exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

if not (O/'HISTORY.before.json').exists():
    paths=list(R.glob('[0-6][0-9]_*.md'))
    paths += [p for p in (R/'model-architecture').rglob('*') if p.is_file() and 'round62' not in str(p) and '__pycache__' not in str(p)]
    paths += [p for p in (R/'prediction-validation').rglob('*') if p.is_file() and '__pycache__' not in str(p)]
    save(O/'HISTORY.before.json',[dict(path=p.relative_to(R).as_posix(),sha256=sha(p)) for p in paths])
for a,b in [('prediction-system/EVIDENCE_GRAPH.json','EVIDENCE_GRAPH.before.json'),('EVIDENCE_INDEX.md','EVIDENCE_INDEX.before.md'),
            ('EVIDENCE_MANIFEST.json','EVIDENCE_MANIFEST.before.json'),('model-architecture/CLAIM_MATRIX.csv','CLAIM_MATRIX.before.csv')]:
    if not (O/b).exists():(O/b).write_bytes((R/a).read_bytes())

targets=[
 ('unity-march-linked','https://unity.com/blog/uads-march-updates'),
 ('unity-vector-product','https://unity.com/products/unity-ads/vector'),
 ('unity-acquire-attribution','https://docs.unity.com/en-us/grow/acquire/partner-integration/attribution/introduction.md'),
 ('axon-data-boundary','https://legal.applovin.com/about-applovins-axon-ai/'),
]
def fetch(item):
    ident,url=item;base=O/'public'/ident;meta=base.with_suffix('.meta.json')
    if meta.exists():return json.loads(meta.read_text('utf-8'))
    row=dict(id=ident,url=url,acquired_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),method='public documentation GET, no identifiers or production ad requests')
    try:
        a=requests.get(url,timeout=(8,24),headers={'User-Agent':'Mozilla/5.0'})
        raw=base.with_suffix('.raw');raw.write_bytes(a.content)
        soup=BeautifulSoup(a.content,'html.parser')
        links=[dict(text=t.get_text(' ',strip=True)[:180],url=urljoin(a.url,t['href'])) for t in soup.find_all('a',href=True)]
        jld=[]
        for s in soup.find_all('script',type='application/ld+json'):
            try:jld.append(json.loads(s.get_text()))
            except json.JSONDecodeError:pass
        if 'text/markdown' in a.headers.get('Content-Type','') or a.text.startswith('---\n'):
            text=a.text;links += [dict(text=x,url=urljoin(a.url,y)) for x,y in re.findall(r'\[([^\]]+)\]\(([^)]+)\)',text)]
        else:
            for s in soup(['script','style','svg','noscript']):s.decompose()
            text=soup.get_text('\n',strip=True)
        p=base.with_suffix('.txt');p.write_text(text,encoding='utf-8');save(base.with_suffix('.links.json'),links)
        row.update(status=a.status_code,final_url=a.url,bytes=len(a.content),raw_path=raw.relative_to(R).as_posix(),raw_sha256=sha(raw),
          text_path=p.relative_to(R).as_posix(),sha256=sha(p),structured_data=jld)
    except requests.RequestException as e:row['error']=type(e).__name__+': '+str(e)[:180]
    save(meta,row);return row

if __name__=='__main__':
    with ThreadPoolExecutor(max_workers=4) as ex:rows=list(ex.map(fetch,targets))
    save(O/'FETCHES.json',rows)
    print(json.dumps([dict(id=x['id'],status=x.get('status'),error=x.get('error'),bytes=x.get('bytes')) for x in rows],indent=2))
