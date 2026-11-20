from axon_fetch import fetch,R
import concurrent.futures,json,urllib.parse,re,html
urls={
 'brave-oakever':'https://search.brave.com/search?q='+urllib.parse.quote('"Oakever" "AppLovin"'),
 'brave-targets':'https://search.brave.com/search?q='+urllib.parse.quote('"AppLovin" "Meowdoku" OR "Jewel Coloring" OR "Rotate Rings"'),
 'sensortower-car':'https://app.sensortower.com/overview/com.dino.race.master?country=US',
 'appmagic-car':'https://appmagic.rocks/google-play/car-race/com.dino.race.master',
 'max-ilrd':'https://support.applovin.com/en/max/android/overview/advanced-settings#impression-level-user-revenue-api',
 'metica-android-doc':'https://docs.metica.com/api/android-sdk',
}
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:out=list(ex.map(lambda x:fetch(*x),urls.items()))
(R/'fetches-final.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
s=html.unescape(urllib.parse.unquote((R/'game-inventory.html').read_text(encoding='utf-8')))
assets=sorted(set(re.findall(r'https://storage\.googleapis\.com/applovin_assets_us/libraries/clients/gaming-studios/[^\s"&<>\\]+',s)))
(R/'inventory-asset-observations.json').write_text(json.dumps({'source':'https://www.applovin.com/en/game-inventory','observations':assets,'scope':'publisher supply/inventory page assets, not target acquisition campaign records'},indent=2),encoding='utf-8')
for x in out:print(x['id'],x.get('status'),x.get('title'),flush=True)
