"""Read-only DEX xrefs for AppLovin direct events and identity sinks. No SDK execution."""
from pathlib import Path
import sys,json,re,hashlib,gc
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'ThirdPartySDKs'))
from embedded_scan import dexes,redact
from androguard.core.dex import DEX
R=Path(__file__).resolve().parent/'deep';R.mkdir(exist_ok=True)
sys.stdout.reconfigure(encoding='utf-8')
event=re.compile(r'Lcom/applovin/(?:sdk/AppLovinEventService|impl/sdk/EventServiceImpl);->|Lcom/applovin/.*->(?:getEventService|trackEvent|trackEventSynchronously|maybeTrackAppOpenEvent)|Lcom/metica/.*->trackEvent|Lcom/applovin/mediation/MaxAdRevenueListener;->')
identity=re.compile(r'Lcom/applovin/.*->(?:setUserIdentifier|getUserIdentifier|setUserData|getUserData)|Lcom/applovin/sdk/AppLovinUserData;|Lcom/metica/.*->(?:setUserId|getUserId)|Lcom/meevii/adsdk/common/AdUuid;->|Lcom/learnings/.*->getUUID')
literal=re.compile(r'"(?:axon_events|dedupe_id|visitInfo|send_user_data|cuid|rewarded_ad_opportunity|ad_view|ad_clicked|level_complete|tutorial_complete)"')
selected={'Lcom/applovin/impl/sdk/EventServiceImpl;','Lcom/applovin/sdk/AppLovinSdkSettings;','Lcom/applovin/sdk/AppLovinSdk;','Lcom/applovin/sdk/AppLovinUserData;'}
def main(slug):
 out=R/'games'/slug;out.mkdir(parents=True,exist_ok=True);calls=[];defs=[];inv=[]
 for apk,dn,data in dexes(slug):
  d=DEX(data);inv.append({'apk':apk,'dex':dn,'sha256':hashlib.sha256(data).hexdigest(),'class_count':len(list(d.get_classes()))})
  for c in d.get_classes():
   cn=c.get_name()
   for m in c.get_methods():
    if not m.get_code():continue
    hits=[];body=[];off=0
    for ins in m.get_code().get_bc().get_instructions():
     s=ins.get_name()+' '+ins.get_output();body.append(f'{off:04x}: '+redact(s))
     types=[]
     if event.search(s):types.append('event')
     if identity.search(s):types.append('identity')
     if literal.search(s):types.append('literal')
     if types:hits.append({'offset':off,'kinds':types,'instruction':redact(s)})
     off+=ins.get_length()
    keep=bool(hits) or cn in selected
    if not keep:continue
    label=re.sub(r'[^\w.-]','_',cn+'__'+m.get_name())[:125]+'-'+hashlib.sha256(m.get_descriptor().encode()).hexdigest()[:10]
    p=out/'raw'/dn/(label+'.txt');p.parent.mkdir(parents=True,exist_ok=True);p.write_text('\n'.join(body),encoding='utf-8')
    row={'apk':apk,'dex':dn,'class':cn,'method':m.get_name(),'descriptor':m.get_descriptor(),'file':str(p.relative_to(R)).replace('\\','/'),'hits':hits}
    defs.append(row)
    if hits:calls.append(row)
  print(slug,dn,'matches',len(calls),flush=True);del d,data;gc.collect()
 obj={'slug':slug,'scope':'all classes*.dex in APK splits; all namespaces scanned; native, reflection and server dispatch require separate evidence','dex_inventory':inv,'methods':defs,'callsite_count':len(calls)}
 (out/'calls.json').write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')
if __name__=='__main__':
 for s in sys.argv[1:] or ['car-race','meowdoku','rotate-rings','jewel-coloring']:main(s)
