"""Parse constant-pool references from already acquired official jars, then javap selected classes."""
from pathlib import Path
import struct,zipfile,json,subprocess,re,sys
R=Path(__file__).resolve().parent/'deep';ROOT=R.parents[1]
sys.stdout.reconfigure(encoding='utf-8')
def refs(b):
 pos=8
 def u1():
  nonlocal pos
  v=b[pos];pos+=1;return v
 def u2():
  nonlocal pos
  v=struct.unpack_from('>H',b,pos)[0];pos+=2;return v
 n=u2();cp=[None]*n;i=1
 while i<n:
  t=u1()
  if t==1:
   l=u2();cp[i]=(t,b[pos:pos+l].decode('utf-8',errors='replace'));pos+=l
  elif t in [7,8,16,19,20]:cp[i]=(t,u2())
  elif t in [9,10,11,12,17,18]:cp[i]=(t,u2(),u2())
  elif t in [3,4]:cp[i]=(t,);pos+=4
  elif t in [5,6]:cp[i]=(t,);pos+=8;i+=1
  elif t==15:cp[i]=(t,u1(),u2())
  else:raise ValueError(t)
  i+=1
 members=[]
 for i,v in enumerate(cp):
  if v and v[0] in [9,10,11]:
   cn=cp[cp[v[1]][1]][1];nt=cp[v[2]];members.append({'pool_index':i,'kind':'field' if v[0]==9 else 'method','owner':cn,'name':cp[nt[1]][1],'descriptor':cp[nt[2]][1]})
 return members
rows=[]
for v,mgr in [('13.2.0','y6'),('13.6.2','p7'),('13.6.3','s7'),('13.6.4','t7')]:
 jar=ROOT/'ThirdPartySDKs/AppLovin/MAX'/v/'classes.jar';dest=R/'versions'/v/'javap';dest.mkdir(exist_ok=True);allrefs=[];select=set()
 with zipfile.ZipFile(jar) as z:
  for n in z.namelist():
   if not n.endswith('.class'):continue
   rs=refs(z.read(n));cn=n[:-6]
   hit=[x for x in rs if x['owner'] in ['com/applovin/impl/sdk/EventServiceImpl','com/applovin/sdk/AppLovinEventService','com/applovin/impl/'+mgr,'com/applovin/sdk/AppLovinUserData'] or x['name'] in ['setUserIdentifier','getUserIdentifier','setUserData']]
   if hit:allrefs.append({'class':cn,'references':hit});select.add(cn)
 for cn in sorted(select):
  p=dest/(cn.replace('/','.')+'.txt')
  a=subprocess.run(['javap','-p','-c','-s','-classpath',str(jar),cn.replace('/','.')],capture_output=True,encoding='utf-8',errors='replace');p.write_text(a.stdout,encoding='utf-8')
 (R/'versions'/v/'constant-pool-refs.json').write_text(json.dumps(allrefs,indent=2),encoding='utf-8');rows.append({'version':v,'selected_classes':len(select),'manager':mgr});print(v,len(select),flush=True)
(R/'jar-reference-index.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
