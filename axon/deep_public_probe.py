from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from axon_fetch import fetch,R
import json,concurrent.futures,urllib.parse
urls={
 'deep-official-blog-search':'https://www.applovin.com/en/blog/search?q=Oakever',
 'deep-yahoo-meow':'https://search.yahoo.com/search?p='+urllib.parse.quote('"Meowdoku" "AppLovin"'),
 'deep-yahoo-rotate':'https://search.yahoo.com/search?p='+urllib.parse.quote('"Rotate Rings" "AppLovin"'),
 'deep-yahoo-car':'https://search.yahoo.com/search?p='+urllib.parse.quote('"com.dino.race.master" "AppLovin"'),
 'deep-yahoo-jewel':'https://search.yahoo.com/search?p='+urllib.parse.quote('"Jewel Coloring" "AppLovin"'),
}
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:out=list(ex.map(lambda x:fetch(*x),urls.items()))
(R/'deep/public-probe.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
for x in out:print(x['id'],x.get('status'),x.get('title'),flush=True)
