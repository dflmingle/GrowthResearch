from pathlib import Path
import json,sys,re,concurrent.futures,urllib.parse
from axon_fetch import fetch,R
sys.stdout.reconfigure(encoding='utf-8')
base='https://support.applovin.com';u={}
a=json.loads((R/'support-applovin-ua-links.json').read_text(encoding='utf-8'))
for x in a:
 if re.search(r'/promoting-your-apps/(track-and-optimize|welcome-to-applovin/top-creative|troubleshooting/in-app-purchase)',x['href']):u['doc-'+x['href'].rstrip('/').split('/')[-1]]=base+x['href']
u.update({
 'gaming-product':'https://www.applovin.com/en/gaming',
 'appsflyer-partner-search':'https://support.appsflyer.com/hc/en-us/search?query=AppLovin',
 'applovin-blog-search':'https://www.applovin.com/en/blog?search=Oakever',
 'ddg-oakever':'https://www.google.com/search?gbv=1&q=%22Oakever%22+%22AppLovin%22',
 'bing-ikame':'https://www.bing.com/search?q=%22iKame%22+%22AppLovin%22',
 'bing-meow':'https://www.bing.com/search?q=%22Meowdoku%22+%22AppLovin%22',
 'bing-car':'https://www.bing.com/search?q=%22com.dino.race.master%22+%22AppLovin%22',
 'bing-rotate':'https://www.bing.com/search?q=%22com.nebula.rotaterings%22+%22AppLovin%22',
 'bing-jewel':'https://www.bing.com/search?q=%22color.number.paint.pixle.art.sort.jigsaw%22+%22AppLovin%22',
 'bing-amaze':'https://www.bing.com/search?q=%22com.oakever.arrows%22+%22AppLovin%22',
 'bing-zego':'https://www.bing.com/search?q=%22Zego%22+%22AppDiscovery%22',
 'appsflyer-appLovin-correct':'https://support.appsflyer.com/hc/en-us/articles/360001441657-AppLovin-integration-configuration',
})
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as e:o=list(e.map(lambda p:fetch(*p),u.items()))
(R/'fetches-discovery.json').write_text(json.dumps(o,ensure_ascii=False,indent=2),encoding='utf-8')
for x in o:print(x['id'],x.get('status'),x.get('title'),flush=True)
