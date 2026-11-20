from embedded_scan import dexes,R,redact
from pathlib import Path
from androguard.core.dex import DEX
import re,json,gc,sys,hashlib
sys.stdout.reconfigure(encoding='utf-8')
patterns={
 'car-race':re.compile(r'(?i)(?:MeticaApplovinFunctions|ApplovinFunctions).*->trackEvent|ApplovinInitializer.*->initializeSdk|Lcom/metica/.*->(?:getVersion|getSdkVersion)|AppLovinUserData|->setUserData\('),
 'meowdoku':re.compile(r'(?i)AppLovinUserData|->setUserData\(|MediaSourceTag;->(?:APPLOVIN_INT|values|valueOf|getName)|Lcom/meevii/adsdk/common/AdUuid;->'),
 'rotate-rings':re.compile(r'(?i)AppLovinUserData|->setUserData\('),
 'jewel-coloring':re.compile(r'(?i)AppLovinUserData|->setUserData\('),
}
rows=[]
for slug,pat in patterns.items():
 for apk,name,data in dexes(slug):
  if not any(x in data for x in [b'com/applovin',b'com/metica',b'com/meevii',b'MediaSourceTag']):continue
  d=DEX(data)
  for c in d.get_classes():
   n=c.get_name();selected=slug=='meowdoku' and n=='Lcom/meevii/adsdk/common/AdUuid;'
   if not selected and n.startswith(('Lcom/applovin/','Lcom/facebook/','Lcom/google/','Lcom/mbridge/','Lcom/fyber/','Lcom/inmobi/')):continue
   for m in c.get_methods():
    if not m.get_code():continue
    body=[];matches=[];off=0
    for ins in m.get_code().get_bc().get_instructions():
     t=ins.get_name()+' '+ins.get_output();body.append(f'{off:04x}: '+redact(t));off+=ins.get_length()
     if pat.search(t):matches.append(redact(t))
    if not matches and not selected:continue
    p=R/'Embedded'/slug/'business-trace'/name/(re.sub(r'[^\w.-]','_',n+'__'+m.get_name())[:125]+'-'+hashlib.sha256(m.get_descriptor().encode()).hexdigest()[:10]+'.txt');p.parent.mkdir(parents=True,exist_ok=True);p.write_text('\n'.join(body),encoding='utf-8')
    rows.append({'slug':slug,'dex':name,'class':n,'method':m.get_name(),'descriptor':m.get_descriptor(),'matches':matches,'file':str(p.relative_to(R)).replace('\\','/')})
  del d;gc.collect()
 print(slug,'trace complete',flush=True)
(R/'BUSINESS_TRACES.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
