from collect_sdk import acquire,R
import json,concurrent.futures
M='https://repo.maven.apache.org/maven2'
specs=[('AppLovin','MAX','com.applovin','applovin-sdk',v,M,'core') for v in ['13.2.0','13.6.2','13.6.3','13.6.4']]
specs += [('Adjust','Android','com.adjust.sdk','adjust-android',v,M,'core') for v in ['5.5.0','5.7.0']]
specs += [('Meta','FacebookCore','com.facebook.android','facebook-core','18.0.3',M,'core')]
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:out=list(ex.map(acquire,specs))
(R/'MATCHED_MANIFEST.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
