from fetch_public import fetch,R
import concurrent.futures,json,re,urllib.parse
u={
 'unity-content-map':'https://unity.com/content/sitemap.xml',
 'unity-legal-map':'https://unity.com/legal/sitemap.xml',
 'unity-support-runtime':'https://support.unity.com/hc/en-us/search?query='+urllib.parse.quote('runtime data sharing'),
 'unity-doc-full':'https://docs.unity.com/llms-full.txt',
 'unity-manual-data':'https://docs.unity3d.com/6000.3/Documentation/Manual/UnityAnalytics.html',
 'unity-runtime-privacy':'https://unity.com/legal/runtime-data-sharing',
 'unity-engine-data':'https://unity.com/legal/engine-data-sharing',
 'unity-runtime-blog-keynote':'https://unity.com/blog/highlights-from-unite-2025-keynote',
 'unity-2026-keynote':'https://unity.com/blog/unite-seoul-keynote-2026-recap',
 'unity-ir-2025-rss':'https://investors.unity.com/rss/pressrelease.aspx?Year=2025',
 'unity-ir-2026-all':'https://investors.unity.com/rss/pressrelease.aspx?Year=2026',
}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:rows=list(ex.map(lambda x:fetch(*x),u.items()))
(R/'fetches-runtime-discovery.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
for x in rows:print(x['id'],x.get('status'),x.get('title'),flush=True)
