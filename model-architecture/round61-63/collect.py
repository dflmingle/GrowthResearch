"""Public-document retrieval only, bounded and cached; no advertising API calls."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import datetime,hashlib,json,requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
R=Path(__file__).resolve().parents[2];O=Path(__file__).resolve().parent
(O/'public').mkdir(parents=True,exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
baseline=O/'HISTORY.before.json'
if not baseline.exists():
    paths=list(R.glob('[0-6][0-9]_*.md'))
    paths += [p for p in (R/'model-architecture').rglob('*') if p.is_file() and 'round61-63' not in str(p) and '__pycache__' not in str(p)]
    paths += [p for p in (R/'prediction-validation').rglob('*') if p.is_file() and '__pycache__' not in str(p)]
    save(baseline,[dict(path=p.relative_to(R).as_posix(),sha256=sha(p)) for p in paths])
for a,b in [('prediction-system/EVIDENCE_GRAPH.json','EVIDENCE_GRAPH.before.json'),('EVIDENCE_INDEX.md','EVIDENCE_INDEX.before.md'),('EVIDENCE_MANIFEST.json','EVIDENCE_MANIFEST.before.json'),('model-architecture/CLAIM_MATRIX.csv','CLAIM_MATRIX.before.csv')]:
    if not (O/b).exists():(O/b).write_bytes((R/a).read_bytes())

TARGETS={
 'u-roas-setup':'https://docs.unity.com/en-us/grow/acquire/campaigns/roas/return-on-ad-spend-campaigns.md',
 'u-post-install':'https://docs.unity.com/en-us/grow/acquire/partner-integration/post-install-event-data.md',
 'u-integration-best':'https://docs.unity.com/en-us/grow/acquire/partner-integration/integration-best-practices.md',
 'u-budgets-nav':'https://docs.unity.com/en-us/grow/acquire/budgets.md',
 'u-bids-nav':'https://docs.unity.com/en-us/grow/acquire/bids.md',
 'u-campaigns-nav':'https://docs.unity.com/en-us/grow/acquire/campaigns.md',
 'u-acquire-nav':'https://docs.unity.com/en-us/grow/acquire.md',
 'al-mmp-start':'https://support.applovin.com/en/growth/promoting-your-apps/track-and-optimize/set-up-mmp-tracking',
 'al-scale':'https://support.applovin.com/en/growth/promoting-your-apps/manage-campaigns/scale-your-campaign',
 'al-website-dedup':'https://support.applovin.com/en/growth/promoting-your-websites/track-and-optimize/deduplicating-events',
}
def fetch(item):
    ident,url=item;base=O/'public'/ident;meta=base.with_suffix('.meta.json')
    if meta.exists():return json.loads(meta.read_text('utf-8'))
    row=dict(id=ident,url=url,acquired_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),method='public documentation GET; no login or production ad/event endpoint')
    try:
        a=requests.get(url,timeout=(8,24),headers={'User-Agent':'Mozilla/5.0'})
        raw=base.with_suffix('.raw');raw.write_bytes(a.content)
        soup=BeautifulSoup(a.content,'html.parser')
        links=[dict(text=t.get_text(' ',strip=True)[:160],url=urljoin(a.url,t['href'])) for t in soup.find_all('a',href=True)]
        if 'text/markdown' in a.headers.get('Content-Type','') or a.text.startswith('---\n') or a.text.startswith('# '):
            text=a.text
            import re
            links += [dict(text=x,url=urljoin(a.url,y)) for x,y in re.findall(r'\[([^\]]+)\]\(([^)]+)\)',text)]
        else:
            for t in soup(['script','style','svg','noscript']):t.decompose()
            text=soup.get_text('\n',strip=True)
        p=base.with_suffix('.txt');p.write_text(text,encoding='utf-8')
        save(base.with_suffix('.links.json'),links)
        row.update(status=a.status_code,final_url=a.url,raw_path=raw.relative_to(R).as_posix(),raw_sha256=sha(raw),
          text_path=p.relative_to(R).as_posix(),sha256=sha(p),bytes=len(a.content),content_type=a.headers.get('Content-Type'))
    except requests.RequestException as e:row['error']=type(e).__name__+': '+str(e)[:160]
    save(meta,row);return row
if __name__=='__main__':
    import sys
    targets=json.loads(Path(sys.argv[1]).read_text('utf-8')) if len(sys.argv)>1 else list(TARGETS.items())
    with ThreadPoolExecutor(max_workers=4) as ex:rows=list(ex.map(fetch,targets))
    save(O/('FETCHES_'+datetime.datetime.now(datetime.timezone.utc).strftime('%H%M%S')+'.json'),rows)
    print(json.dumps([dict(id=x['id'],status=x.get('status'),error=x.get('error'),bytes=x.get('bytes')) for x in rows],indent=2))
