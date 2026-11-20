from fetch_public import fetch,R
import concurrent.futures,json,re
u={
 'd28-blog':'https://unity.com/blog/d28-roas',
 'd7-d28-iap':'https://unity.com/blog/d7-vs-d28-iap-roas-campaigns',
 'exchange-rampid':'https://unity.com/blog/unity-exchange-rampid-addressable-buying-mobile-gaming',
 'exchange-tools':'https://unity.com/blog/ironsource-expands-its-ad-exchange-with-powerful-new-tools',
 'mattel-case':'https://unity.com/blog/mattel163-phase-10-vector-roas',
 'playrix-case':'https://unity.com/blog/playrix-township-roas-optimization-vector',
 'grow-doc-index':'https://docs.unity.com/en-us/grow/llms.txt',
 'ads-doc-index':'https://docs.unity.com/en-us/ads-android/llms.txt',
 'acquire-doc-index':'https://docs.unity.com/en-us/acquire/llms.txt',
 'runtime-doc-index':'https://docs.unity.com/en-us/runtime-data-sharing/llms.txt',
 'unity-ir-2025-q4-fixed':'https://investors.unity.com/news/news-details/2026/Unity-Reports-Fourth-Quarter-and-Full-Year-2025-Financial-Results-and-Provides-2026-Guidance/default.aspx',
 'app-ir-2025-q1':'https://investors.applovin.com/news/news-details/2025/AppLovin-Announces-First-Quarter-2025-Financial-Results/default.aspx',
 'app-ir-2025-q2':'https://investors.applovin.com/news/news-details/2025/AppLovin-Announces-Second-Quarter-2025-Financial-Results/default.aspx',
 'app-ir-2025-q3':'https://investors.applovin.com/news/news-details/2025/AppLovin-Announces-Third-Quarter-2025-Financial-Results/default.aspx',
 'app-ir-2025-q4':'https://investors.applovin.com/news/news-details/2026/AppLovin-Announces-Fourth-Quarter-and-Full-Year-2025-Financial-Results/default.aspx',
}
for x in json.loads((R/'unity-vector-correct-links.json').read_text(encoding='utf-8')):
 if 'case' in x['href'] or 'resources' in x['href']:u['vector-link-'+x['href'].rstrip('/').split('/')[-1]]=x['href'] if x['href'].startswith('http') else 'https://unity.com'+x['href']
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:rows=list(ex.map(lambda x:fetch(*x),u.items()))
(R/'fetches-detail.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
for x in rows:print(x['id'],x.get('status'),x.get('title'),flush=True)
