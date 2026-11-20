from pathlib import Path
import json,zipfile,hashlib,subprocess,re,sys,datetime,io,struct
sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path(__file__).resolve().parent
SDK=Path('C:/Users/89trillion/AppData/Local/Android/Sdk/build-tools/35.0.1')
PATTERNS={'adjust':'Lcom/adjust/','appsflyer':'Lcom/appsflyer/','branch':'Lio/branch/','tiktok':'Lcom/tiktok/','firebase':'Lcom/google/firebase/','metica':'Lcom/metica/','appmetrica':'Lio/appmetrica/','max':'Lcom/applovin/','ironsource':'Lcom/ironsource/','unityads':'Lcom/unity3d/ads/','admob':'Lcom/google/android/gms/ads/','meta':'Lcom/facebook/','referrer':'Lcom/android/installreferrer/','oakever':'Lcom/oakever/','easybrain':'Lcom/easybrain/','yandex':'Lcom/yandex/','umeng':'Lcom/umeng/'}
def sha(b):return hashlib.sha256(b).hexdigest()
def run(cmd):
 r=subprocess.run(cmd,capture_output=True);return {'exit':r.returncode,'output':(r.stdout+r.stderr).decode('utf-8',errors='replace')}
def inventory(slug,source=None):
 p=ROOT/slug;out=p/'static';out.mkdir(parents=True,exist_ok=True)
 if source is None:
  acq=json.loads((p/'samples/acquisition.json').read_text(encoding='utf-8'));source=p/'samples'/acq['file']
 source=Path(source);raw=source.read_bytes();identity={'sample':str(source),'sha256':sha(raw),'bytes':len(raw),'audited_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()};manifest=None
 with zipfile.ZipFile(io.BytesIO(raw)) as z:
  if 'manifest.json' in z.namelist():manifest=json.loads(z.read('manifest.json'));identity['xapk_manifest']=manifest
  apk_names=[n for n in z.namelist() if n.endswith('.apk')]
  if not apk_names:apk_names=['@self']
  splits=[];abis=set();unity_versions=set();native=[];asset_names=[]
  for n in apk_names:
   data=raw if n=='@self' else z.read(n);fn=source.name if n=='@self' else Path(n).name
   split=out/'splits'/fn;split.parent.mkdir(exist_ok=True);split.write_bytes(data)
   record={'file':fn,'sha256':sha(data),'bytes':len(data)}
   with zipfile.ZipFile(io.BytesIO(data)) as apk:
    names=apk.namelist();asset_names+=names
    record['dex']=[n for n in names if re.match(r'classes\d*\.dex$',n)]
    record['libraries']=[n for n in names if n.startswith('lib/') and n.endswith('.so')]
    abis.update(n.split('/')[1] for n in record['libraries']);native+=record['libraries']
    if 'AndroidManifest.xml' in names and ('config.' not in fn):
     for tool,args,name in [('aapt.exe',['dump','badging'],'badging.txt'),('aapt.exe',['dump','xmltree'],'AndroidManifest.txt')]:
      extra=['AndroidManifest.xml'] if 'xmltree' in args else []
      res=run([str(SDK/tool),*args,str(split),*extra]);(out/name).write_text(res['output'],encoding='utf-8')
      if name=='badging.txt':
       match=re.search(r"package: name='([^']+)' versionCode='([^']+)' versionName='([^']+)'",res['output'])
       if match:identity.update(package=match[1],versionCode=match[2],versionName=match[3])
     res=run([str(SDK/'apksigner.bat'),'verify','--print-certs',str(split)]);(out/'signature.txt').write_text(res['output'],encoding='utf-8');identity['signature_verification_exit']=res['exit'];identity['certificate_sha256']=re.findall(r'^Signer #\d+ certificate SHA-256 digest: (\w+)',res['output'],re.M);identity['source_stamp_certificate_sha256']=re.findall(r'^Source Stamp Signer certificate SHA-256 digest: (\w+)',res['output'],re.M)
    # Index ZIP metadata and SDK versions. Do not extract/read production credential files.
    props={}
    for entry in names:
     if entry.endswith('.properties') and not entry.startswith('assets/') and apk.getinfo(entry).file_size<10000:props[entry]=apk.read(entry).decode('utf-8',errors='replace')
     if entry in ['assets/bin/Data/globalgamemanagers','assets/bin/Data/data.unity3d']:
      b=apk.read(entry)[:250000];unity_versions.update(s.decode() for s in re.findall(rb'\b(?:20\d\d|6000)\.\d+\.\d+[abfp]\d+\b',b))
    record['sdk_properties']=props
    for entry in names:
     if entry.startswith('assets/') and any(key in entry.lower() for key in ['metadata','globalgamemanagers','data.unity3d','settings.json','jsb','project.manifest']):
      if 'metadata' in entry or entry.endswith(('globalgamemanagers','data.unity3d','.jsc')):
       dest=out/'native-inputs'/entry;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(apk.read(entry))
    for entry in record['libraries']:
     if entry.endswith(('libil2cpp.so','libunity.so','libcocos2djs.so','libgame.so','libapp.so')):
      dest=out/'native-inputs'/entry;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(apk.read(entry))
   splits.append(record)
  identity.update(abis=sorted(abis),unity_versions=sorted(unity_versions),splits=splits,native_libraries=sorted(set(native)),asset_paths=sorted(set(asset_names)))
  identity['engine']='Unity IL2CPP' if any('libil2cpp.so' in n for n in native) else 'Unity (backend not yet identified)' if any('libunity.so' in n for n in native) else 'Cocos candidate' if any('cocos' in n for n in native) else 'Flutter' if any('libflutter.so' in n for n in native) else 'Java/Kotlin or other; inspect DEX/assets'
 (out/'sample-identity.json').write_text(json.dumps(identity,ensure_ascii=False,indent=2),encoding='utf-8')
 print(slug,identity.get('package'),identity.get('versionName'),identity['engine'],identity['abis'],identity['unity_versions'],flush=True)
if __name__=='__main__':
 for slug in sys.argv[1:]:
  try:inventory(slug)
  except Exception as ex:print(slug,'ERROR',repr(ex),flush=True)
