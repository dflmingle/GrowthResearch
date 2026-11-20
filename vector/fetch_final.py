from fetch_public import fetch,R
import concurrent.futures,json,re,urllib.parse
u={
 'unity-financial-2026-feed':'https://investors.unity.com/feed/FinancialReport.svc/GetFinancialReportList?'+urllib.parse.urlencode({'pageSize':100,'pageNumber':0,'year':2026,'includeTags':'true'}),
 'unity-runtime-cs-release':'https://raw.githubusercontent.com/Unity-Technologies/UnityCsReference/6000.3/Modules/UnityConsent/EndUserConsent.bindings.cs',
 'unity-runtime-cs-release-state':'https://raw.githubusercontent.com/Unity-Technologies/UnityCsReference/6000.3/Modules/UnityConsent/ConsentState.bindings.cs',
 'unity-unified-ads':'https://docs.unity.com/en-us/grow/levelplay/platform/unity-ads-network.md',
 'unity-retire-hc-search':'https://support.unity.com/hc/en-us/search?query=%22April+30%22+%222026%22',
 'unity-ddf-consent-api':'https://docs.unity3d.com/6000.3/Documentation/ScriptReference/UnityConsent.EndUserConsent.SetConsentState.html',
 'unity-ads-partner':'https://help.adjust.com/en/partner-setup/unity-ads',
 'af-unity-partner':'https://support.appsflyer.com/hc/en-us/articles/208005086-Unity-Ads-campaign-configuration',
}
# Follow documented exact links for post-install schemas and SDK data policies.
for n in ['doc-intro-to-roas-campaigns','doc-integrate-adjust-with-unity','ddf-end-user-consent','ddf-built-for-unity-6','ddf-data-collection-settings','ddf-data-usage-settings']:
 s=(R/(n+'.html')).read_text(encoding='utf-8')
 for path in re.findall(r'\]\((/[^)]+)\)',s):
  if any(t in path for t in ['post-install-event-data','configure-diagnostics-editor','configure-diagnostics-dashboard']):u['doc-'+path.split('/')[-1].replace('.md','')]='https://docs.unity.com/en-us'+path
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:rows=list(ex.map(lambda x:fetch(*x),u.items()))
(R/'fetches-final.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
for x in rows:print(x['id'],x.get('status'),x.get('title'),flush=True)
