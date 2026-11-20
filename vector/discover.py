from fetch_public import fetch,R
import concurrent.futures,json
u={
 'unity-vector-correct':'https://unity.com/products/unity-ads/vector',
 'unity-blog-map':'https://unity.com/blog/sitemap.xml',
 'unity-news-map':'https://unity.com/news/sitemap.xml',
 'q4-api-js':'https://widgets.q4app.com/widgets/q4.api.1.13.5.min.js',
 'unity-ir-rss':'https://investors.unity.com/rss/pressrelease.aspx',
 'applovin-ir-rss':'https://investors.applovin.com/rss/pressrelease.aspx',
 'unity-docs-index':'https://docs.unity.com/llms.txt',
 'unity-ir-2025-q1':'https://investors.unity.com/news/news-details/2025/Unity-Reports-First-Quarter-2025-Financial-Results/default.aspx',
 'unity-ir-2025-q2':'https://investors.unity.com/news/news-details/2025/Unity-Reports-Second-Quarter-2025-Financial-Results/default.aspx',
 'unity-ir-2025-q3':'https://investors.unity.com/news/news-details/2025/Unity-Reports-Third-Quarter-2025-Financial-Results/default.aspx',
 'unity-ir-2025-q4':'https://investors.unity.com/news/news-details/2026/Unity-Reports-Fourth-Quarter-and-Full-Year-2025-Financial-Results/default.aspx',
 'unity-ir-2026-q1':'https://investors.unity.com/news/news-details/2026/Unity-Reports-First-Quarter-2026-Financial-Results/default.aspx',
 'unity-ir-2026-q2':'https://investors.unity.com/news/news-details/2026/Unity-Reports-Second-Quarter-2026-Financial-Results/default.aspx',
 'unity-ir-2026-q3':'https://investors.unity.com/news/news-details/2026/Unity-Reports-Third-Quarter-2026-Financial-Results/default.aspx',
 'app-ir-2026-q1':'https://investors.applovin.com/news/news-details/2026/AppLovin-Announces-First-Quarter-2026-Financial-Results/default.aspx',
 'app-ir-2026-q2':'https://investors.applovin.com/news/news-details/2026/AppLovin-Announces-Second-Quarter-2026-Financial-Results/default.aspx',
 'app-ir-2026-q3':'https://investors.applovin.com/news/news-details/2026/AppLovin-Announces-Third-Quarter-2026-Financial-Results/default.aspx',
}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:rows=list(ex.map(lambda x:fetch(*x),u.items()))
(R/'fetches-discovery.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
for x in rows:print(x['id'],x.get('status'),x.get('title'),flush=True)
