from pathlib import Path
import importlib.util, json, subprocess, requests, datetime
R=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('collect',R/'collect.py');m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
rows=[]
rows.append(m.decompile(('max-dispatch','AppLovin/MAX/13.6.4',r'^com\.applovin\.impl\.mediation\.MediationServiceImpl$',2)))
cp=m.ROOT/'ThirdPartySDKs/AppLovin/MAX/13.6.4/classes.jar'
for cls in ['com.applovin.impl.g5$c','com.applovin.impl.g5$b']:
 p=R/(cls.rsplit('.',1)[1]+'.javap.txt')
 a=subprocess.run(['javap','-c','-p','-classpath',str(cp),cls],capture_output=True,timeout=30)
 p.write_bytes(a.stdout);rows.append(dict(class_name=cls,path=p.relative_to(m.ROOT).as_posix(),exit_code=a.returncode,sha256=m.sha(p),classes_jar_sha256=m.sha(cp)))
m.save(R/'DECOMPILE_FINAL.json',rows)
# One bounded retry on a public doc, then continue with cached evidence if unavailable.
record=m.fetch(('unity-post-install-data','https://docs.unity.com/en-us/grow/acquire/partner-integration/post-install-event-data.md'))
m.save(R/'PUBLIC_FETCH_RETRY.json',[record])
print('Views',[x.get('name',x.get('class_name')) for x in rows]);print('Doc',record.get('status',record.get('error')))
