from pathlib import Path
import subprocess,zipfile,json,re,sys
ROOT=Path(__file__).resolve().parent
REPO=Path('C:/Users/89trillion/game')
JAR=REPO/'tower-forge/tools/jadx-headless-mcp-0.7.1-all.jar'
def run(slug,pattern,limit=120):
 out=ROOT/slug/'static';audit=json.loads((out/'dex-audit.json').read_text(encoding='utf-8'));match=re.compile(pattern);dexes=set()
 for m in audit['business_calls']+audit['sdk_method_candidates']:
  name=m['class'][1:-1].replace('/','.')
  if match.search(name):dexes.add((m.get('apk'),m['dex']))
 # SDK records omit apk; base APK is the one with classes*.dex.
 base=next(p for p in (out/'splits').glob('*.apk') if zipfile.ZipFile(p).namelist().count('classes.dex'))
 for _,entry in sorted(dexes,key=lambda x:x[1]):
  p=out/'dex-inputs'/entry;p.parent.mkdir(exist_ok=True)
  with zipfile.ZipFile(base) as z:p.write_bytes(z.read(entry))
  dest=out/'java'/entry
  cmd=['java','-Xmx1100m','-cp',str(JAR)+';'+str(ROOT),'SelectJadx',str(p),str(dest),pattern,str(limit)]
  log=out/(entry+'.jadx.log')
  with log.open('wb') as f:r=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT,cwd=ROOT)
  print(slug,entry,'exit',r.returncode,flush=True)
if __name__=='__main__':run(sys.argv[1],sys.argv[2],int(sys.argv[3]) if len(sys.argv)>3 else 120)
