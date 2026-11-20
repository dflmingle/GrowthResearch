from pathlib import Path
import zipfile,json,re,sys,collections,gc,hashlib
from loguru import logger
logger.remove()
from androguard.core.dex import DEX
sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path(__file__).resolve().parent
FAMILIES={'Adjust':'Lcom/adjust/','AppsFlyer':'Lcom/appsflyer/','Branch':'Lio/branch/','TikTok':'Lcom/tiktok/','Firebase':'Lcom/google/firebase/','Metica':'Lcom/metica/','AppMetrica':'Lio/appmetrica/','AppLovin_MAX':'Lcom/applovin/','ironSource':'Lcom/ironsource/','UnityAds':'Lcom/unity3d/ads/','AdMob':'Lcom/google/android/gms/ads/','Meta':'Lcom/facebook/','InstallReferrer':'Lcom/android/installreferrer/','ThinkingData':'Lcn/thinkingdata/','GameAnalytics':'Lcom/gameanalytics/','Tenjin':'Lcom/tenjin/','Sensors':'Lcom/sensorsdata/'}
INTEREST=re.compile(r'(?i)attribution|referrer|campaign|media.source|ad.revenue|revenue|roas|\bltv\b|ad_impression|paid_ad|first_reward|value_optimization|tiktok|appsflyer|adjust|taichi|metica|trackevent|logevent|remoteconfig|setrevenue|reportad|purchase|onpaid|firebaseanalytics|facebook.appevents')
NOISE=('Landroid','Lkotlin','Ljava','Lcom/google/','Lcom/applovin/','Lcom/ironsource/','Lcom/adjust/','Lcom/appsflyer/','Lcom/facebook/','Lcom/tiktok/','Lcom/bytedance/','Lcom/unity3d/','Lcom/mbridge/','Lcom/fyber/','Lcom/inmobi/','Lcom/vungle/','Lcom/bigossp/','Lcom/moloco/','Lcom/yandex/','Lio/appmetrica/','Lcom/chartboost/','Lcom/bidmachine/','Lio/bidmachine/','Lcom/amazon/','Lcom/iab/','Lcom/qq/','Lokhttp','Lokio','Lorg/','Lcom/safedk/','Lcom/jingdong/','Lcom/pubmatic/','Lcom/criteo/')
def safe(s):
 # Do not export credential literals. Event tokens are handled separately in native/game evidence.
 if re.search(r'(?i)(api.?key|app.?secret|dev.?key|sdk.?key|password|access.?token)',s):return '[credential-related literal redacted]'
 if len(s)>500:return s[:250]+'...[truncated]'
 return s
def audit(slug):
 out=ROOT/slug/'static';files=list((out/'splits').glob('*.apk'));inventory=[];strings=[];business=[];sdkmethods=[];top=collections.Counter();version=[];allclasses=[]
 for f in files:
  with zipfile.ZipFile(f) as z:
   for entry in z.namelist():
    if not re.match(r'classes\d*\.dex$',entry):continue
    data=z.read(entry);d=DEX(data);counts=collections.Counter();classes=list(d.get_classes());names=[c.get_name() for c in classes];allclasses+=names
    for n in names:
     top['/'.join(n.split('/')[:3])]+=1
     for k,v in FAMILIES.items():
      if n.startswith(v):counts[k]+=1
    inventory.append({'apk':f.name,'dex':entry,'sha256':hashlib.sha256(data).hexdigest(),'classes':len(names),'families':dict(counts)})
    for s in d.get_strings():
     if INTEREST.search(s) and len(s)<800:strings.append({'dex':entry,'value':safe(s)})
    for c in classes:
     n=c.get_name();is_business=not n.startswith(NOISE)
     is_sdk=any(n.startswith(x) for x in ['Lcom/adjust/','Lcom/appsflyer/','Lcom/tiktok/','Lcom/metica/'])
     for m in c.get_methods():
      code=m.get_code()
      if not code:continue
      lines=[];selected=[];offset=0
      try:
       for ins in code.get_bc().get_instructions():
        text=ins.get_name()+' '+ins.get_output();lines.append(f'{offset:04x}: {text}');offset+=ins.get_length()
        if INTEREST.search(text):selected.append(text)
      except Exception:continue
      if selected and is_business:
       # Preserve DEX instruction offsets and method names; redact suspect config literals.
       record={'apk':f.name,'dex':entry,'class':n,'method':m.get_name(),'descriptor':m.get_descriptor(),'matches':[safe(x) for x in selected]}
       business.append(record)
       if len(lines)<450 and len(business)<1200:
        label=n+'__'+m.get_name()+'_'+m.get_descriptor()
        dest=out/'dex-evidence'/entry/(re.sub('[^A-Za-z0-9_.-]','_',label)[:105]+'-'+hashlib.sha256(label.encode()).hexdigest()[:12])
        dest=dest.with_suffix('.smali.txt');dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text('\n'.join(safe(x) for x in lines),encoding='utf-8');record['file']=str(dest.relative_to(out))
      elif selected and is_sdk and re.search(r'(?i)version|trackad|trackevent|initialize|start|revenue|referrer|attribution|queue|retry|cache',m.get_name()):sdkmethods.append({'dex':entry,'class':n,'method':m.get_name(),'matches':[safe(x) for x in selected][:40]})
    print(slug,entry,'classes',len(names),'business matches',len(business),flush=True)
    del d,classes,data;gc.collect()
 result={'dex_inventory':inventory,'class_prefixes':top.most_common(100),'business_calls':business,'sdk_method_candidates':sdkmethods}
 (out/'dex-audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');(out/'dex-interest-strings.json').write_text(json.dumps(strings,ensure_ascii=False,indent=2),encoding='utf-8');(out/'dex-class-index.txt').write_text('\n'.join(allclasses),encoding='utf-8')
 print(slug,'DONE',len(business),flush=True)
if __name__=='__main__':
 for s in sys.argv[1:]:audit(s)
