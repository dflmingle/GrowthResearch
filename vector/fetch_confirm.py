from fetch_public import fetch,R
import concurrent.futures,json,urllib.parse
u={
 'ddf-doc':'https://docs.unity.com/en-us/cloud/developer-data-framework',
 'ddf-doc-md':'https://docs.unity.com/en-us/cloud/developer-data-framework.md',
 'cloud-index':'https://docs.unity.com/en-us/cloud/llms.txt',
 'runtime-consent-manual':'https://docs.unity3d.com/6000.3/Documentation/Manual/UnityConsent.html',
 'unity-finance-feed':'https://investors.unity.com/feed/PressRelease.svc/GetPressReleaseList?'+urllib.parse.urlencode({'pageSize':100,'pageNumber':0,'year':2026,'bodyType':2,'pressReleaseDateFilter':3,'includeTags':'true'}),
 'unity-financial-feed':'https://investors.unity.com/feed/FinancialReport.svc/GetFinancialReportList?'+urllib.parse.urlencode({'pageSize':100,'pageNumber':0,'year':2025,'includeTags':'true'}),
 'unity-ads-sunset':'https://docs.unity.com/en-us/grow/levelplay/platform/ironsource-ads-retirement.md',
}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:rows=list(ex.map(lambda x:fetch(*x),u.items()))
(R/'fetches-confirm.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
for x in rows:print(x['id'],x.get('status'),x.get('title'),flush=True)
