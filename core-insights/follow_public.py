from pathlib import Path
import json,importlib.util,concurrent.futures
R=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('acq',R/'acquire.py');a=importlib.util.module_from_spec(sp);sp.loader.exec_module(a)
if __name__=='__main__':
 tree=json.loads((R/'unity-runtime-tree.raw').read_text(encoding='utf-8'));commit=tree['sha']
 paths=['Modules/Identifiers/Identifiers.bindings.cs','Modules/Insights/EngineDiagnostics.bindings.cs','Modules/InsightsEditor/EngineDiagnosticsSettings.bindings.cs','Modules/InsightsEditor/RequiresInsightsAttribute.cs']
 urls={p.split('/')[-1].replace('.cs',''):'https://raw.githubusercontent.com/Unity-Technologies/UnityCsReference/'+commit+'/'+p for p in paths}
 urls.update({'unity-6000-7-branch':'https://api.github.com/repos/Unity-Technologies/UnityCsReference/branches/6000.7','unity-6000-6-branch':'https://api.github.com/repos/Unity-Technologies/UnityCsReference/branches/6000.6',
 'iap-privacy-package':'https://docs.unity3d.com/Packages/com.unity.purchasing@5.5/manual/UnityIAPPrivacy.html',
 'identifiers-api-correct':'https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Identifiers.Identifiers.html'})
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:list(ex.map(lambda x:a.get(*x),urls.items()))
 (R/'RUNTIME_PUBLIC_PROVENANCE.json').write_text(json.dumps(dict(tree_sha=commit,scope='pinned public UnityCsReference master snapshot, not target-game engine version',paths=paths,fetches=a.log),ensure_ascii=False,indent=2),encoding='utf-8')
 print([(x['id'],x.get('status')) for x in a.log])
