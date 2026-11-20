"""Optional reproduction of local paper text extraction; no downloads or data access."""
from pathlib import Path
import json
import pymupdf
D=Path(__file__).resolve().parent
with pymupdf.open(D/'sources/bayesian-paper-pdf.raw') as document:
    pages=[dict(page=i+1,text=page.get_text()) for i,page in enumerate(document)]
(D/'PAPER_PAGES.json').write_text(json.dumps(pages,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(D/'sources/bayesian-paper-pdf.txt').write_text('\n\n'.join('PAGE '+str(p['page'])+'\n'+p['text'] for p in pages)+'\n',encoding='utf-8')
print(json.dumps(dict(pages=len(pages),scope='Local documentary extraction only; not paper replication')))
