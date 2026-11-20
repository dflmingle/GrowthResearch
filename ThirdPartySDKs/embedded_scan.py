from pathlib import Path
import json,zipfile,sys,re,gc,hashlib,io
from loguru import logger
logger.remove()
from androguard.core.dex import DEX
R=Path(__file__).resolve().parent;ROOT=R.parent
sys.stdout.reconfigure(encoding='utf-8')
TARGETS={
 'Lcom/applovin/sdk/AppLovinSdk;':r'(?i)getVersion|<clinit>',
 'Lcom/applovin/sdk/AppLovinEventService;':r'.*',
 'Lcom/applovin/sdk/AppLovinSdkSettings;':r'(?i)setUserIdentifier|setExtraParameter|setMuted',
 'Lcom/applovin/impl/sdk/EventServiceImpl;':r'(?i)track|user',
 'Lcom/applovin/mediation/MaxAd;':r'.*',
 'Lcom/applovin/mediation/MaxAdRevenueListener;':r'.*',
 'Lcom/adjust/sdk/Constants;':r'.*',
 'Lcom/adjust/sdk/AdjustConfig;':r'(?i)setExternalDeviceId|setFbAppId|setDefaultTracker',
 'Lcom/adjust/sdk/Adjust;':r'(?i)trackEvent|trackAdRevenue|addGlobalPartner|addSessionPartner|setExternalDeviceId',
 'Lcom/adjust/sdk/ActivityHandler;':r'(?i)trackAdRevenueI|trackEventI|isValidAttribution',
 'Lcom/adjust/sdk/PackageBuilder;':r'(?i)buildAdRevenuePackage|buildEventPackage|buildSessionPackage|addDeviceInfo|buildAttributionPackage',
 'Lcom/appsflyer/AppsFlyerLib;':r'(?i)logAdRevenue|logEvent|setCustomerUserId|setPartnerData',
 'Lcom/appsflyer/AppsFlyerProperties;':r'^$',
}
PREFIX=('Lcom/applovin/','Lcom/adjust/','Lcom/appsflyer/','Lcom/google/','Lcom/facebook/','Lcom/ironsource/','Lcom/unity3d/ads/','Lcom/tiktok/','Lcom/bytedance/','Lcom/mbridge/','Lcom/inmobi/','Lcom/vungle/','Lcom/moloco/','Lcom/safedk/','Landroid','Lkotlin','Ljava')
api=re.compile(r'Lcom/applovin/.*->(?:trackEvent|trackCheckout|trackPurchase|setUserIdentifier)|Lcom/appsflyer/.*->setPartnerData')
partner=re.compile(r'(?i)applovin_int|appdiscovery|\baxon\b|applovin.{0,25}(?:campaign|postback|media_source)|(?:campaign|media_source).{0,25}applovin')
ver=re.compile(r'^(?:android\d+\.\d+\.\d+|(?:unity|android)\d+\.\d+\.\d+.*|!SDK-VERSION-STRING!.*|AppsFlyer_\d+\.\d+\.\d+)$')
def redact(s):
 if re.search(r'(?i)(api.?key|app.?secret|dev.?key|sdk.?key|password|access.?token)',s):return '[credential-related instruction omitted]'
 return s[:1000]
def dexes(slug):
 if slug=='car-race':
  p=Path('C:/Users/89trillion/game/car-race/source/CarRace-1.348.2.xapk')
  with zipfile.ZipFile(p) as outer:
   for n in outer.namelist():
    if n.endswith('.apk'):
     with zipfile.ZipFile(io.BytesIO(outer.read(n))) as z:
      for e in z.namelist():
       if re.fullmatch(r'classes\d*\.dex',e):yield n,e,z.read(e)
 else:
  for p in (ROOT/slug/'static/splits').glob('*.apk'):
   with zipfile.ZipFile(p) as z:
    for e in z.namelist():
     if re.fullmatch(r'classes\d*\.dex',e):yield p.name,e,z.read(e)
def main(slug):
 out=R/'Embedded'/slug;out.mkdir(parents=True,exist_ok=True)
 rows=[];fields=[];calls=[];strings=[];inventory=[]
 for apk,name,data in dexes(slug):
  if b'com/applovin' not in data and b'com/adjust' not in data and b'com/appsflyer' not in data:continue
  d=DEX(data);inventory.append({'apk':apk,'dex':name,'sha256':hashlib.sha256(data).hexdigest()})
  for s in d.get_strings():
   if ver.search(s) or partner.search(s):strings.append({'dex':name,'value':redact(s)})
  for c in d.get_classes():
   cn=c.get_name()
   if cn in TARGETS:
    for f in c.get_fields():
     if not re.search(r'(?i)VERSION|CLIENT_SDK|SDK_NAME',f.get_name()):continue
     iv=f.get_init_value()
     if iv:
      try:v=iv.get_value();fields.append({'dex':name,'class':cn,'field':f.get_name(),'value':v.decode(errors='replace') if isinstance(v,bytes) else v})
      except Exception:pass
    for m in c.get_methods():
     if not re.search(TARGETS[cn],m.get_name()):continue
     row={'dex':name,'class':cn,'method':m.get_name(),'descriptor':m.get_descriptor()}
     if m.get_code():
      body=[];offset=0
      for ins in m.get_code().get_bc().get_instructions():
       body.append(f'{offset:04x}: '+redact(ins.get_name()+' '+ins.get_output()));offset+=ins.get_length()
      label=re.sub(r'[^\w.-]','_',cn+'__'+m.get_name())[:135]+'-'+hashlib.sha256(m.get_descriptor().encode()).hexdigest()[:10]
      p=out/name/(label+'.txt');p.parent.mkdir(exist_ok=True);p.write_text('\n'.join(body),encoding='utf-8');row['file']=str(p.relative_to(R)).replace('\\','/')
     rows.append(row)
   elif not cn.startswith(PREFIX):
    for m in c.get_methods():
     if not m.get_code():continue
     hit=[]
     for ins in m.get_code().get_bc().get_instructions():
      txt=ins.get_name()+' '+ins.get_output()
      if api.search(txt) or partner.search(txt):hit.append(redact(txt))
     if hit:calls.append({'dex':name,'class':cn,'method':m.get_name(),'descriptor':m.get_descriptor(),'matches':hit})
  print(slug,name,'selected',len(rows),'calls',len(calls),flush=True)
  del d,data;gc.collect()
 obj={'slug':slug,'inventory':inventory,'version_fields':fields,'version_or_partner_strings':strings,'selected_methods':rows,'appLovin_acquisition_candidate_calls':calls,'scope':'APK main DEX definitions and non-vendor acquisition API callers; not proof of backend configuration; no live execution'}
 (out/'audit.json').write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')
if __name__=='__main__':
 for s in sys.argv[1:] or ['car-race','meowdoku','rotate-rings','jewel-coloring']:main(s)
