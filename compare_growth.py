from pathlib import Path
import json, re, hashlib, gc, sys, zipfile
from loguru import logger
from androguard.core.dex import DEX
logger.remove()
R=Path(__file__).resolve().parent
sys.stdout.reconfigure(encoding='utf-8')
def scan(slug):
    result={}; origins={}; versions=[]
    apk=next(p for p in (R/slug/'static/splits').glob('*.apk') if 'classes.dex' in zipfile.ZipFile(p).namelist())
    z=zipfile.ZipFile(apk)
    for entry in sorted(n for n in z.namelist() if re.fullmatch(r'classes\d*\.dex',n)):
        p=Path(entry)
        d=DEX(z.read(entry))
        for s in d.get_strings():
            if re.fullmatch(r'(?:\w*SDK\w*[ /_-])?(?:\d{1,2}\.){2}\d{1,3}(?:[-\w.]*)?',s) or re.search(r'AppFlyer_V\d',s):
                versions.append({'dex':p.name,'value':s})
        for c in d.get_classes():
            n=c.get_name()
            if not (n.startswith(('Lcom/unity3d/player/SDKKeybehaviors','Lta/','Lva/','Lg8/','Lcom/hurelax/datareport/')) or n in ['Lcom/unity3d/player/App;','Lcom/unity3d/player/SDKManager;','Ln0/k;']):continue
            origins[n]=p.name
            for m in c.get_methods():
                if not m.get_code():continue
                body='\n'.join(i.get_name()+' '+i.get_output() for i in m.get_code().get_bc().get_instructions())
                key=n+'->'+m.get_name()+m.get_descriptor()
                result[key]=hashlib.sha256(body.encode()).hexdigest()
        print(slug,p.name,len(result),flush=True)
        del d;gc.collect()
    (R/slug/'static/growth-method-hashes.json').write_text(json.dumps({'methods':result,'origins':origins,'version_candidates':versions},indent=2),encoding='utf-8')
    return result,origins
if __name__=='__main__':
    a,_=scan('rotate-rings-1.2.2');b,origins=scan('rotate-rings')
    out={'method':'SHA256 of decoded opcode + resolved operands, class/method/descriptor keyed; no debug information; differences are candidates, not semantic proof',
         'same':[n for n in a if a[n]==b.get(n)],'changed':[n for n in a if n in b and a[n]!=b[n]],'removed':[n for n in a if n not in b],'added':[n for n in b if n not in a]}
    (R/'rotate-rings/history-method-comparison.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print('RESULT',{k:len(out[k]) for k in ['same','changed','removed','added']},flush=True)
    print('ORIGINS',{k:v for k,v in origins.items() if k in ['Lcom/unity3d/player/App;','Lcom/unity3d/player/SDKManager;']})
