from pathlib import Path
import json,re,zipfile,gc,sys
from loguru import logger
from androguard.core.dex import DEX
logger.remove();R=Path(__file__).resolve().parent;sys.stdout.reconfigure(encoding='utf-8')
targets={
 'Lcom/adjust/sdk/PackageHandler;':r'^(addPackage|sendFirstPackage|sendNextPackage|closeFirstPackage|readPackageQueue|writePackageQueue|sendFirstI|addI|sendNextI|closeFirstI)',
 'Lcom/adjust/sdk/DeviceInfo;':r'^(<init>|getSdkVersion)',
 'Lcom/tiktok/appevents/TTAppEventLogger;':r'(?i)flush|queue|persist|send|retry',
 'Lcom/tiktok/appevents/TTRequestBuilder;':r'(?i)build|post|send|retry',
 'Lcom/tiktok/appevents/TTAppEventStorage;':r'(?i)save|persist|read|add|clear',
 'Lcom/learnings/unikit/module/ModuleManager;':r'(?i)initModules',
 'Lcom/learnings/grt/LearningsGRT;':r'^init$',
 'Lcom/unity3d/player/f2;':r'^run$',
 'Lcom/unity3d/player/App$4;':r'(?i)conversion',
}
rows=[]
for slug in ['meowdoku','rotate-rings','jewel-coloring']:
 out=R/slug/'static';apk=next(a for a in (out/'splits').glob('*.apk') if 'classes.dex' in zipfile.ZipFile(a).namelist());z=zipfile.ZipFile(apk)
 for dex in sorted(x for x in z.namelist() if re.fullmatch(r'classes\d*\.dex',x)):
  d=DEX(z.read(dex))
  for c in d.get_classes():
   n=c.get_name()
   if n not in targets:continue
   for m in c.get_methods():
    if not m.get_code() or not re.search(targets[n],m.get_name()):continue
    body=[];off=0
    for ins in m.get_code().get_bc().get_instructions():
     t=ins.get_name()+' '+ins.get_output()
     if re.search(r'(?i)(appsecret|devkey|sdkkey|access_token)',t):t='[credential-related instruction omitted]'
     body.append(f'{off:04x}: {t}');off+=ins.get_length()
    if len(body)>1800:continue
    p=out/'sdk-internals'/dex/(re.sub('[^a-zA-Z0-9_.-]','_',n+'__'+m.get_name())+'.txt');p.parent.mkdir(parents=True,exist_ok=True);p.write_text('\n'.join(body),encoding='utf-8')
    rows.append({'slug':slug,'dex':dex,'class':n,'method':m.get_name(),'descriptor':m.get_descriptor(),'file':str(p.relative_to(R)).replace('\\','/')})
  del d;gc.collect()
 print('done',slug,flush=True)
(R/'SDK_INTERNALS_INDEX.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
