from fetch_public import fetch,R
import concurrent.futures,json,re
u={
 'developer-data-terms':'https://unity.com/legal/developer-data-framework-additional-terms',
 'developer-data-legacy':'https://unity.com/legal/developer-data-framework-additional-terms-legacy',
 'unity-support-ddf':'https://support.unity.com/hc/en-us/search?query=Developer+Data+Framework',
 'unity-consent-api':'https://docs.unity3d.com/6000.3/Documentation/ScriptReference/UnityConsent.EndUserConsent.html',
 'unity-consent-cs':'https://raw.githubusercontent.com/Unity-Technologies/UnityCsReference/master/Modules/UnityConsent/EndUserConsent.bindings.cs',
 'unity-consent-state-cs':'https://raw.githubusercontent.com/Unity-Technologies/UnityCsReference/master/Modules/UnityConsent/ConsentState.bindings.cs',
 'unity-consent-status-cs':'https://raw.githubusercontent.com/Unity-Technologies/UnityCsReference/master/Modules/UnityConsent/ConsentStatus.bindings.cs',
 'unity-q4-2025-short':'https://investors.unity.com/news/news-details/2026/Unity-Reports-Fourth-Quarter-and-Full-Year-2025-Financial-Results-2026/default.aspx',
}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:rows=list(ex.map(lambda x:fetch(*x),u.items()))
(R/'fetches-framework.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
for x in rows:print(x['id'],x.get('status'),x.get('title'),flush=True)
