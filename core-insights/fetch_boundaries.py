"""Fetch pinned public reference bindings/docs, never execute SDKs."""
from pathlib import Path
import json, importlib.util, concurrent.futures

R = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('acq', R / 'acquire.py')
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)
urls = {}
for branch in ('6', '7'):
    d = json.loads((R / f'unity-6000-{branch}-branch.raw').read_text('utf-8'))
    commit = d['commit']['sha']
    for name, path in {
        'Identifiers': 'Modules/Identifiers/Identifiers.bindings.cs',
        'EngineDiagnostics': 'Modules/Insights/EngineDiagnostics.bindings.cs',
        'RequiresInsights': 'Modules/InsightsEditor/RequiresInsightsAttribute.cs',
    }.items():
        urls[f'{name}-6000-{branch}'] = f'https://raw.githubusercontent.com/Unity-Technologies/UnityCsReference/{commit}/{path}'
urls.update({
    'installation-property': 'https://docs.unity.com/en-us/engine/6000.7/script-reference/unityengine/identifiers/identifiers-installationid',
    'userid-property': 'https://docs.unity.com/en-us/engine/6000.7/script-reference/unityengine/identifiers/identifiers-userid',
})
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
    list(ex.map(lambda x: a.get(*x), urls.items()))
(R / 'BOUNDARY_ACQUISITION.json').write_text(json.dumps(a.log, ensure_ascii=False, indent=2), 'utf-8')
print([(x['id'], x.get('status')) for x in a.log])
