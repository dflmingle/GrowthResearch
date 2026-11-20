from pathlib import Path
import json,re,zipfile,gc,hashlib,sys,collections
from androguard.core.dex import DEX
from loguru import logger
logger.remove();R=Path(__file__).resolve().parent;sys.stdout.reconfigure(encoding='utf-8')
out=R/'identity-deep';out.mkdir(exist_ok=True)
api=re.compile(r'(?i)(->(?:setCustomerUserId|setCustomerIdAndLogSession|setExternalDeviceId|setExternalDeviceID|setUserId|setUserID|setUserIdentifier|setAccountId|setAccountID|setAccount|setIdentity|setLoginId|setLoginID|setUserData|setEmail|setPhoneNumber|identify|login|bind|linkWithCredential|getAppsFlyerUID|getAdid|getAdvertisingIdInfo|getAdvertisingId|setAdvertisingId|setCustomUserId|trackCrossPromoteImpression|trackAndOpenStore|registerCustomAudience|joinCustomAudience|fetchAndJoinCustomAudience|registerTrigger|setDeviceId|setDeviceID)\(|CustomerUserId|external_device_id|cross.?promotion|cross.?app|identity.?graph|idgraph|liveramp|tapad|zeotap|id5-api|lotame|audienceproject|unifiedid|uid2|neustar|publink|shared.?userid)')
classes_re=re.compile(r'UUIDManager|DeviceId|UserId|Identity|Account|AuthManager|LoginManager|FirebaseAuth|CrossPromotion|Audience|AdSource|AdWorth')
rows=[];class_origins={};vendor_hits=[]
for slug in ['car-race','meowdoku','rotate-rings','jewel-coloring']:
 base=Path('C:/Users/89trillion/game/car-race/source/splits') if slug=='car-race' else R/slug/'static/splits'
 apk=next(p for p in base.glob('*.apk') if 'classes.dex' in zipfile.ZipFile(p).namelist());z=zipfile.ZipFile(apk);cls=[]
 for entry in sorted(n for n in z.namelist() if re.fullmatch(r'classes\d*\.dex',n)):
  d=DEX(z.read(entry))
  for c in d.get_classes():
   n=c.get_name()
   if classes_re.search(n):cls.append({'class':n,'dex':entry})
   for m in c.get_methods():
    code=m.get_code()
    if not code:continue
    matches=[];lines=[];off=0
    for i in code.get_bc().get_instructions():
     s=i.get_name()+' '+i.get_output()
     if api.search(s):matches.append(f'{off:04x}: '+s)
     # Restrict exported literal values, never export credential assignments.
     if i.get_name().startswith('const-string') and not api.search(s):s='const-string [literal omitted]'
     lines.append(f'{off:04x}: '+s);off+=i.get_length()
    if not matches:continue
    key=n+'->'+m.get_name()+m.get_descriptor();dest=out/slug/entry/(re.sub('[^A-Za-z0-9_.-]','_',n+'__'+m.get_name())[:96]+'-'+hashlib.sha256(key.encode()).hexdigest()[:10]+'.txt');dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text('\n'.join(lines),encoding='utf-8');rows.append({'slug':slug,'dex':entry,'class':n,'method':m.get_name(),'descriptor':m.get_descriptor(),'file':str(dest.relative_to(R)).replace('\\','/'),'matches':matches})
  for s in d.get_strings():
   if re.search(r'(?i)(liveramp|tapad|zeotap|id5-api|lotame|identity.?graph|uid2|neustar|audienceproject|pubprovided|pub.?link)',s) and len(s)<220:vendor_hits.append({'slug':slug,'dex':entry,'value':s})
  print(slug,entry,'API callers',sum(x['slug']==slug for x in rows),flush=True);del d;gc.collect()
 class_origins[slug]=cls
 (out/'api-callers.json').write_text(json.dumps(rows,indent=2),encoding='utf-8');(out/'class-origins.json').write_text(json.dumps(class_origins,indent=2),encoding='utf-8');(out/'vendor-literal-candidates.json').write_text(json.dumps(vendor_hits,indent=2),encoding='utf-8')
