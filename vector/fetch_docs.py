from fetch_public import fetch,R
import concurrent.futures,re,json,xml.etree.ElementTree as ET
u={
 'runtime-manual':'https://docs.unity3d.com/6000.3/Documentation/Manual/ent-unity-data.html',
 'unity-data-sharing':'https://unity.com/legal/engine-improve-data',
 'unity-ir-q4-alternate':'https://investors.unity.com/news/news-details/2026/Unity-Reports-Fourth-Quarter-2025-Financial-Results/default.aspx',
 'unity-terms':'https://unity.com/legal/editor-terms-of-service/software',
 'runtime-search':'https://www.google.com/search?q=site%3Aunity.com+%22Runtime%22+%22data+sharing%22+Vector',
}
s=(R/'grow-doc-index.txt').read_text(encoding='utf-8')
for title,url in re.findall(r'\[([^\]]+)\]\((https://[^)]+)\)',s):
 if any(t in url for t in ['roas/intro','roas/roas-campaign-best','roas/return-on','integrate-adjust-with-unity','integrate-appsflyer-with-unity','advanced-ad-metrics','custom/postback-request','custom/send-postbacks','bids/revenue-bids','programmatic/unity-exchange/get-started','user-level-revenue']):u['doc-'+url.rstrip('/').split('/')[-1].replace('.md','')]=url
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:rows=list(ex.map(lambda x:fetch(*x),u.items()))
(R/'fetches-docs.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
for x in rows:print(x['id'],x.get('status'),x.get('title'),flush=True)
