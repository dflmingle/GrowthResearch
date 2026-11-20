from fetch_public import fetch,R
import concurrent.futures,json,re
u={}
for line in (R/'ddf-doc-md.txt').read_text(encoding='utf-8').splitlines():
 m=re.search(r'\]\((/cloud/[^)]+)\)',line)
 if m:u['ddf-'+m[1].split('/')[-1].replace('.md','')]='https://docs.unity.com/en-us'+m[1]
x=json.loads((R/'unity-finance-feed.html').read_text(encoding='utf-8'))
for item in x['GetPressReleaseListResult']:
 if re.search('Fourth|Full.Year',item['Headline'],re.I):u['unity-q4-2025-resolved']='https://investors.unity.com'+item['LinkToDetailPage']
x=json.loads((R/'unity-financial-feed.html').read_text(encoding='utf-8'))
pdfs=[]
for item in x['GetFinancialReportListResult']:
 if item.get('ReportSubType')=='Fourth Quarter':
  pdfs=item.get('Documents',[])
  for doc in pdfs:
   if doc['DocumentCategory']=='news' and doc.get('DocumentPath'):u['unity-q4-2025-pdf']=doc['DocumentPath']
(R/'q4-financial-documents.json').write_text(json.dumps(pdfs,indent=2),encoding='utf-8')
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:rows=list(ex.map(lambda x:fetch(*x),u.items()))
(R/'fetches-resolved.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
for x in rows:print(x['id'],x.get('status'),x.get('title'),flush=True)
