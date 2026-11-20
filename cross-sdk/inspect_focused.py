from pathlib import Path
import json,re,difflib,subprocess
ROOT=Path(__file__).resolve().parent.parent;R=ROOT/'cross-sdk'
def section(path,start,end):
 print('\n###',path)
 print('\n'.join(f'{i+1}: {s}' for i,s in enumerate((ROOT/path).read_text(encoding='utf-8').splitlines()) if start<=i+1<=end))
if __name__=='__main__':
 section('cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/Insights/PurchaseEventEmitter.cs',190,259)
 section('ThirdPartySDKs/Google/FirebaseRemoteConfig/24.0.1/sources/com/google/firebase/remoteconfig/internal/ConfigFetchHandler.java',285,355)
 old=ROOT/'axon/deep/sdk/13.6.4/java/com/applovin/impl/sdk/EventServiceImpl.java'
 if not old.exists():
  matches=list((ROOT/'axon').glob('**/13.6.4/**/EventServiceImpl.java'));print('event source',matches[:3])
 else:print('event source',old)
 for p in (ROOT/'ThirdPartySDKs/AppLovin/MAX/13.6.4').rglob('EventServiceImpl.java'):print('event source',p)
 print('sources roots',list((ROOT/'identity-graph/sdk').glob('*/*provenance*')))
