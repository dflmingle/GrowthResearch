from pathlib import Path
import subprocess,concurrent.futures,json
ROOT=Path(__file__).resolve().parent.parent;R=ROOT/'cross-sdk'
JAR='C:/Users/89trillion/game/tower-forge/tools/jadx-headless-mcp-0.7.1-all.jar'
specs=[
 ('max-unity-417','ThirdPartySDKs/AppLovin/Adapter-unityads-adapter/4.17.0.0/classes.jar',r'UnityAdsMediationAdapter',15),
 ('max-unity-418','ThirdPartySDKs/AppLovin/Adapter-unityads-adapter/4.18.1.0/classes.jar',r'UnityAdsMediationAdapter',15),
 ('max-google-254','ThirdPartySDKs/AppLovin/Adapter-google-adapter/25.4.0.0/classes.jar',r'GoogleMediationAdapter',15),
 ('max-137','ThirdPartySDKs/AppLovin/MAX/13.7.0/classes.jar',r'^com\.applovin\.(sdk\.(AppLovinSdk|AppLovinSdkSettings|AppLovinUserData)|impl\.sdk\.(EventServiceImpl|network\.(b|c|d)))$',20),
 ('metica-254','ThirdPartySDKs/Metica/Android/2.5.4/classes.jar',r'(ApplovinInitializer|MeticaSdk|MeticaInitConfig|Analytics|UserId|Event|RemoteConfig|Revenue)',70),
]
def work(s):
 name,path,pat,n=s;out=R/'java'/name;out.mkdir(parents=True,exist_ok=True)
 with (out/'jadx.log').open('wb') as f:
  p=subprocess.run(['java','-Xmx650m','-cp',JAR+';'+str(ROOT),'SelectJadx',str(ROOT/path),str(out),pat,str(n)],stdout=f,stderr=subprocess.STDOUT,cwd=ROOT,timeout=160)
 print(name,p.returncode,flush=True)
 return dict(name=name,input=path,pattern=pat,returncode=p.returncode,output=out.relative_to(ROOT).as_posix())
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:rows=list(ex.map(work,specs))
 (R/'DECOMPILE.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
