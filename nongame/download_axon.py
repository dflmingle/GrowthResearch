from pathlib import Path
import requests,json,hashlib,zipfile,datetime,subprocess
R=Path(__file__).resolve().parent
dest=R/'sdk/axon/1.3.4';dest.mkdir(parents=True,exist_ok=True)
u='https://repo.maven.apache.org/maven2/com/applovin/axon-sdk/1.3.4/axon-sdk-1.3.4.aar'
p=dest/'axon-sdk-1.3.4.aar'
assert not p.exists(), 'do not redownload existing SDK'
a=requests.get(u,timeout=(8,25),stream=True);a.raise_for_status()
n=0
with p.open('wb') as f:
 for b in a.iter_content(65536):
  n+=len(b)
  if n>20_000_000:raise ValueError('size cap')
  f.write(b)
with zipfile.ZipFile(p) as z:
 (dest/'archive-index.json').write_text(json.dumps(z.namelist(),indent=2),encoding='utf-8')
 (dest/'classes.jar').write_bytes(z.read('classes.jar'))
with zipfile.ZipFile(dest/'classes.jar') as z:
 classes=[x[:-6].replace('/','.') for x in z.namelist() if x.endswith('.class')]
 (dest/'classes.json').write_text(json.dumps(classes,indent=2),encoding='utf-8')
selected=[x for x in classes if x.startswith('com.applovin.sdk.') and '$' not in x]
for cls in selected:
 out=subprocess.run(['javap','-classpath',str(dest/'classes.jar'),'-public',cls],capture_output=True,timeout=15)
 (dest/(cls.split('.')[-1]+'.javap.txt')).write_bytes(out.stdout+out.stderr)
(dest/'provenance.json').write_text(json.dumps({'url':u,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':a.status_code,'bytes':n,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'version':'1.3.4','license':'AppLovin Corporation SDK EULA per official POM; public availability is not redistribution permission','scope':'official standalone Axon artifact; not matched to any non-game sample version; static only','classes_jar_sha256':hashlib.sha256((dest/'classes.jar').read_bytes()).hexdigest()},indent=2),encoding='utf-8')
print('Downloaded official Axon 1.3.4',n,'bytes;',len(classes),'classes;',len(selected),'public API classes inspected')
