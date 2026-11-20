from pathlib import Path
import zipfile,json,re,subprocess,hashlib,sys
R=Path(__file__).resolve().parent;ROOT=R.parent
sys.stdout.reconfigure(encoding='utf-8')
JADX='C:/Users/89trillion/game/tower-forge/tools/jadx-headless-mcp-0.7.1-all.jar'
tasks=[('max-13.6.4',ROOT/'ThirdPartySDKs/AppLovin/MAX/13.6.4/classes.jar'),('axon-1.3.4',ROOT/'nongame/sdk/axon/1.3.4/classes.jar')]
summary=[]
for name,jar in tasks:
 dest=R/'sdk'/name;dest.mkdir(parents=True,exist_ok=True);hits=[]
 with zipfile.ZipFile(jar) as z:
  for n in z.namelist():
   if not n.endswith('.class'):continue
   b=z.read(n);terms=[x for x in ['AppSetIdInfo','AppSet','AdvertisingIdClient','collectGoogleAdvertisingInfo','idfv_scope','AppLovinUserData','AxonUserData','send_user_data','client_ip_address'] if x.encode() in b]
   if terms:hits.append({'class':n[:-6].replace('/','.'),'terms':terms})
 # Include collector/consumers explicitly, but keep this bounded and one Java process at a time.
 chosen={h['class'] for h in hits}
 if name.startswith('max'):chosen.update(['com.applovin.impl.v','com.applovin.impl.sdk.m','com.applovin.impl.r7','com.applovin.impl.t7','com.applovin.impl.sdk.EventServiceImpl','com.applovin.impl.sdk.k'])
 else:chosen.update(['com.applovin.sdk.Axon','com.applovin.sdk.AxonPrivacySettings','com.applovin.sdk.AxonUserData'])
 regex='^(?:'+'|'.join(re.escape(x) for x in sorted(chosen))+')$'
 with (dest/'jadx.log').open('wb') as f:
  run=subprocess.run(['java','-Xmx650m','-cp',JADX+';'+str(ROOT),'SelectJadx',str(jar),str(dest/'java'),regex,'80'],stdout=f,stderr=subprocess.STDOUT,timeout=180)
 record={'sdk':name,'jar':jar.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(jar.read_bytes()).hexdigest(),'exit':run.returncode,'selected_classes':sorted(chosen),'literal_hits':hits}
 summary.append(record);print(name,'exit',run.returncode,'selected',len(chosen),flush=True)
(R/'SDK_IDENTITY_AUDIT.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
