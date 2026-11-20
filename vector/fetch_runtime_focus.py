from fetch_public import fetch,R
import concurrent.futures,json
u={
 'runtime-manual-main':'https://docs.unity3d.com/Manual/UnityRuntimeDataSharing.html',
 'runtime-manual-alt':'https://docs.unity3d.com/6000.3/Documentation/Manual/UnityDataPrivacy.html',
 'unitycs-tree':'https://api.github.com/repos/Unity-Technologies/UnityCsReference/git/trees/master?recursive=1',
 'unitycs-release-tree':'https://api.github.com/repos/Unity-Technologies/UnityCsReference/git/trees/6000.3?recursive=1',
 'data-checklist':'https://unity.com/resources/unity-vector-data-health-checklist',
 'unity-2025-10k':'https://investors.unity.com/news/news-details/2026/Unity-Announces-Fourth-Quarter-and-Full-Year-2025-Financial-Results/default.aspx',
 'unity-financial-widget':'https://investors.unity.com/js/module/widgets/dist/latest/evergreen.q4Api.min.js',
 'unity-ir-events':'https://investors.unity.com/events-presentations/default.aspx',
 'unity-pdf-2025q4':'https://s205.q4cdn.com/200788659/files/doc_financials/2025/q4/Unity-Q4-2025-Shareholder-Letter.pdf',
 'unity-retire-search':'https://support.unity.com/hc/en-us/search?query=ironSource+Ads+retirement',
}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:rows=list(ex.map(lambda x:fetch(*x),u.items()))
(R/'fetches-runtime-focus.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
for x in rows:print(x['id'],x.get('status'),x.get('title'),flush=True)
