"""Metadata minimization and verification. No model training or identity matching."""
from pathlib import Path
from bs4 import BeautifulSoup
import json,hashlib,re
ROOT=Path(r'D:\GrowthResearch');RAW=ROOT/'public-evidence/raw'
records=[]
for p in RAW.glob('*.json'):
    if p.name.endswith('.metadata.json'):continue
    try:
        o=json.loads(p.read_text(encoding='utf-8'))
        if isinstance(o,dict) and 'id' in o and 'url' in o:records.append(o)
    except (ValueError,UnicodeError):pass

for slug in ['car','meow','rotate','jewel']:
    for kind in ['play','appbrain']:
        ident=slug+'-'+kind;rec=next(r for r in records if r['id']==ident)
        raw=RAW/(ident+'.raw');txt=RAW/(ident+'.txt')
        soup=BeautifulSoup(raw.read_text(encoding='utf-8'),'html.parser')
        if kind=='play':
            ld=[]
            for tag in soup.select('script[type="application/ld+json"]'):
                o=json.loads(tag.string or tag.text)
                ld.append({k:v for k,v in o.items() if k in ['@type','name','url','operatingSystem','applicationCategory','author','offers','contentRating']})
            lines=txt.read_text(encoding='utf-8').splitlines()
            cut=next((i for i,line in enumerate(lines) if line=='Ratings and reviews'),min(100,len(lines)))
            retained=lines[:cut]
            meta={'jsonld':ld,'public_listing_excerpt':retained,'omitted':'review text, reviewer display names, public user references and embedded scripts not needed for this audit'}
        else:
            lines=txt.read_text(encoding='utf-8').splitlines();ranges=[]
            # Public product/metric sections only. Never retain the comments blocks.
            start=None
            for i,line in enumerate(lines):
                if line.startswith('Comments on '):start=i
                if start is not None and (line.startswith('Google Play Rating history') or line.startswith('Google Play Rankings for ')):
                    ranges.append((start,i));start=None
            if start is not None:ranges.append((start,len(lines)))
            keep=[(i+1,line) for i,line in enumerate(lines) if not any(a<=i<b for a,b in ranges)]
            retained=[f'{num}: {line}' for num,line in keep]
            canonical=soup.find('link',rel='canonical')
            meta={'canonical':canonical.get('href') if canonical else None,'source_line_numbered_product_and_metrics':retained,'omitted':'comments/review blocks; no reviewer names retained'}
        out=RAW/(ident+'.metadata.json');out.write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8')
        txt.write_text('\n'.join(retained)+'\n',encoding='utf-8')
        rec.update(response_sha256=rec.pop('sha256'),response_bytes=rec.pop('bytes'),raw_body_retained=False,
            path=out.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(out.read_bytes()).hexdigest(),bytes=out.stat().st_size,
            minimization='Product and aggregate metrics only; comments/reviewers excluded. Response hash recorded but unneeded full HTML not retained.',
            text_sha256=hashlib.sha256(txt.read_bytes()).hexdigest())
        (RAW/(ident+'.json')).write_text(json.dumps(rec,ensure_ascii=False,indent=2),encoding='utf-8')
        raw.unlink()  # Only newly fetched disposable HTML in this round; original 00-64 untouched.

# Remove broad snippets that could accidentally include public reviewer text.
p=ROOT/'public-evidence/IDENTITY_EXTRACTS.json'
o=json.loads(p.read_text(encoding='utf-8'))
for row in o:
    row['excerpts']=[x for x in row['excerpts'] if 'Google Play Rankings for' not in x['text']]
p.write_text(json.dumps(o,ensure_ascii=False,indent=2),encoding='utf-8')

for rec in records:
    if rec.get('path') and (ROOT/rec['path']).is_file():
        if hashlib.sha256((ROOT/rec['path']).read_bytes()).hexdigest()!=rec['sha256']:raise ValueError('hash mismatch '+rec['id'])
(ROOT/'public-evidence/ALL_FETCHES.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
print('PASS: saved product/aggregate metadata, discarded unnecessary review HTML; verified',len(records),'public fetch records')
