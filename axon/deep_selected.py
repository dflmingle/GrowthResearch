from pathlib import Path
import json,re,subprocess,sys
R=Path(__file__).resolve().parent/'deep';ROOT=R.parents[1];JAR=Path('C:/Users/89trillion/game/tower-forge/tools/jadx-headless-mcp-0.7.1-all.jar')
sys.stdout.reconfigure(encoding='utf-8');rows=[]
for v,mgr,conf in [('13.2.0','y6','l4'),('13.6.2','p7','z4'),('13.6.3','s7','c5'),('13.6.4','t7','c5')]:
 a=json.loads((R/'versions'/v/'constant-pool-refs.json').read_text(encoding='utf-8'))
 classes=[x['class'].replace('/','.') for x in a]
 classes+=['com.applovin.impl.'+mgr,'com.applovin.impl.'+conf,'com.applovin.impl.sdk.SessionTracker']
 # Resolve core scheduler and collector return types from previously decompiled core class.
 core=R/'versions'/v/'java/com/applovin/impl/sdk'/('j.java' if v=='13.2.0' else 'l.java')
 s=core.read_text(encoding='utf-8')
 for typ,method in re.findall(r'public (com\.applovin[\w.$]+) (\w+)\(\)',s):
  if method in (['j0','y','p0','X'] if v=='13.2.0' else ['s0','B','h0','z0','y0']):classes.append(typ)
 pat='^(?:'+'|'.join(re.escape(x) for x in dict.fromkeys(classes))+')$';dest=R/'versions'/v/'selected';dest.mkdir(exist_ok=True)
 with (dest/'jadx.log').open('wb') as f:a=subprocess.run(['java','-Xmx750m','-cp',str(JAR)+';'+str(ROOT),'SelectJadx',str(ROOT/'ThirdPartySDKs/AppLovin/MAX'/v/'classes.jar'),str(dest),pat,'50'],stdout=f,stderr=subprocess.STDOUT,timeout=180)
 rows.append({'version':v,'classes':classes,'exit':a.returncode});print(v,a.returncode,flush=True)
(R/'selected-decompilation.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
