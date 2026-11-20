from axon_fetch import fetch,R
import concurrent.futures,json
URLS={
 'gaming-apps':'https://www.applovin.com/en/gaming-apps',
 'game-inventory':'https://www.applovin.com/en/game-inventory',
 'af-campaign':'https://support.appsflyer.com/hc/en-us/articles/208335613-AppLovin-campaign-configuration',
 'af-max-revenue':'https://support.appsflyer.com/hc/en-us/articles/360004707378-Applovin-MAX-ad-revenue-configuration',
 'blog-data-boundary':'https://www.applovin.com/en/blog/catch-bad-ads-not-data',
 'search-ddg-oakever':'https://html.duckduckgo.com/html/?q=%22Oakever%22+%22AppLovin%22',
 'search-ddg-car':'https://html.duckduckgo.com/html/?q=%22Car+Race%22+%22AppLovin%22',
 'search-ddg-jewel':'https://html.duckduckgo.com/html/?q=%22Jewel+Coloring%22+%22AppLovin%22',
 'search-ddg-rotate':'https://html.duckduckgo.com/html/?q=%22Rotate+Rings%22+%22AppLovin%22',
 'search-ddg-meow':'https://html.duckduckgo.com/html/?q=%22Meowdoku%22+%22AppLovin%22',
 'search-ddg-amaze':'https://html.duckduckgo.com/html/?q=%22com.oakever.arrows%22+%22AppLovin%22',
 'sdk-applovin-doc':'https://support.applovin.com/en/max/android/overview/advanced-settings/',
}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as e:o=list(e.map(lambda p:fetch(*p),URLS.items()))
(R/'fetches-focused.json').write_text(json.dumps(o,ensure_ascii=False,indent=2),encoding='utf-8')
for x in o:print(x['id'],x.get('status'),x.get('title'),flush=True)
