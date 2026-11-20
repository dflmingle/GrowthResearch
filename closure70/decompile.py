from pathlib import Path
import subprocess,json,hashlib
R=Path(__file__).resolve().parent.parent;D=R/'closure70'
jar=Path('C:/Users/89trillion/game/tower-forge/tools/jadx-headless-mcp-0.7.1-all.jar')
specs=[('unity-4181','ThirdPartySDKs/Unity/Ads/4.18.1/classes.jar',r'^com\.unity3d\.ads\.core\.domain\.(LegacyLoadUseCase|LegacyShowUseCase|AndroidLoad|AndroidGetAdPlayerConfigRequest|AndroidHandleGatewayAdResponse|AndroidShow|events\.GetOperativeEventApi|exposure\.CommonAdViewerExposedFunctionsKt)$',9),('adapter-417','ThirdPartySDKs/AppLovin/Adapter-unityads-adapter/4.17.0.0/classes.jar',r'^com\.applovin\.mediation\.adapters\.UnityAdsMediationAdapter$',1)]
rows=[]
for name,path,pattern,maxn in specs:
    out=D/'java'/name;out.mkdir(parents=True,exist_ok=True)
    with (D/(name+'.decompile.log')).open('wb') as f:
        p=subprocess.run(['java','-Xmx650m','-cp',str(jar)+';'+str(R),'SelectJadx',str(R/path),str(out),pattern,str(maxn)],stdout=f,stderr=subprocess.STDOUT,cwd=R,timeout=170)
    rows.append(dict(name=name,input=path,input_sha256=hashlib.sha256((R/path).read_bytes()).hexdigest(),pattern=pattern,exit=p.returncode,output=out.relative_to(R).as_posix(),log=(D/(name+'.decompile.log')).relative_to(R).as_posix()))
    print(name,p.returncode,len(list(out.rglob('*.java'))),flush=True)
(D/'DECOMPILE.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
