"""Inventory/license phase only. No source/decompiler/SDK execution."""
from pathlib import Path
import datetime, hashlib, json, shutil

R=Path(__file__).resolve().parent.parent
D=Path(__file__).resolve().parent
(D/'sources').mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):
    assert not p.exists(),p
    p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert not (D/'HISTORY_BEFORE.json').exists()
h={p.name:sha(p) for p in R.iterdir() if p.is_file() and p.name[:2].isdigit() and int(p.name[:2])<=78}
for n in ['EVIDENCE_INDEX.md','prediction-system/EVIDENCE_GRAPH.json']:h[n]=sha(R/n)
save(D/'HISTORY_BEFORE.json',h)
shutil.copyfile(R/'EVIDENCE_INDEX.md',D/'EVIDENCE_INDEX.before.md')
shutil.copyfile(R/'prediction-system/EVIDENCE_GRAPH.json',D/'EVIDENCE_GRAPH.before.json')
save(D/'SCOPE.json',dict(created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
 active_stage='Official sample inventory and license verification;no new functional static analysis',
 original_reference_architecture_goal='Retained but deferred;first-round sample/license gate takes priority',
 allowed=['Read archived provenance/POM/package/license metadata','Hash existing selected artifacts','Read license entries only from archives',
          'Bounded official public license/repository/release metadata GETs','Reuse prior identity findings with original scope'],
 forbidden=['New SDK decompile or identity code scan','Real ad or identity query','Production SDK execution','Third-party personal identifiers',
            'Leaked repo or access-control bypass','Modify engineering76','Automatic reference implementation development'],
 invariants=dict(Axon_C_graph='UNKNOWN',Vector_C_graph='UNKNOWN',D='UNKNOWN',production_forensics='STOP')))
save(D/'first.json',[
 ['al-eula','https://www.applovin.com/eula'],
 ['unity-operate-terms','https://unity.com/legal/one-operate-services-terms-of-service'],
 ['unity-ads-terms','https://unity3d.com/legal/monetization-services-terms-of-service'],
 ['al-android-repo','https://api.github.com/repos/AppLovin/AppLovin-MAX-SDK-Android'],
 ['al-ios-repo','https://api.github.com/repos/AppLovin/AppLovin-MAX-SDK-iOS'],
 ['al-unity-repo','https://api.github.com/repos/AppLovin/AppLovin-MAX-Unity-Plugin'],
 ['lp-unity-repo','https://api.github.com/repos/ironsource-mobile/Unity-sdk'],
 ['lp-android-repo','https://api.github.com/repos/ironsource-mobile/Android-sdk'],
 ['adjust-version-license','https://raw.githubusercontent.com/adjust/android_sdk/v5.8.1/LICENSE']])
print(json.dumps(dict(historical_numbered=len(h)-2,stage='INVENTORY_AND_LICENSE_ONLY')))
