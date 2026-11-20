from pathlib import Path
import subprocess,json,hashlib
R=Path(__file__).resolve().parent.parent;D=R/'closure70'
specs=[('max-q','ThirdPartySDKs/AppLovin/MAX/13.6.4/classes.jar','com.applovin.impl.sdk.q'),('max-g6','ThirdPartySDKs/AppLovin/MAX/13.6.4/classes.jar','com.applovin.impl.g6'),('max-o3','ThirdPartySDKs/AppLovin/MAX/13.6.4/classes.jar','com.applovin.impl.o3'),('adapter417','ThirdPartySDKs/AppLovin/Adapter-unityads-adapter/4.17.0.0/classes.jar','com.applovin.mediation.adapters.UnityAdsMediationAdapter')]
out=[]
for key,path,cls in specs:
    f=D/(key+'.javap.txt');assert not f.exists()
    with f.open('wb') as h:r=subprocess.run(['javap','-c','-p','-classpath',str(R/path),cls],stdout=h,stderr=subprocess.STDOUT,timeout=30)
    out.append(dict(id=key,input=path,input_sha256=hashlib.sha256((R/path).read_bytes()).hexdigest(),class_name=cls,path=f.relative_to(R).as_posix(),sha256=hashlib.sha256(f.read_bytes()).hexdigest(),exit=r.returncode))
(D/'BYTECODE_CHECK.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print('saved',len(out),'javap views; exits',[x['exit'] for x in out])
