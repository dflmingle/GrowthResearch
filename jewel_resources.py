from pathlib import Path
import zipfile,zlib,struct,json,hashlib,sys,collections,re
R=Path(__file__).resolve().parent;O=R/'jewel-coloring/deep/resources';O.mkdir(parents=True,exist_ok=True);sys.stdout.reconfigure(encoding='utf-8')
package=b'color.number.paint.pixle.art.sort.jigsaw'
def decode(b):
 # Original BigFile rc4_crypt: KSA j retained; PRGA starts i=0 (not standard RC4).
 s=list(range(256));j=0
 for i in range(256):j=(j+s[i]+package[i%len(package)])&255;s[i],s[j]=s[j],s[i]
 o=bytearray(len(b))
 for k,v in enumerate(b):
  i=k&255;j=(j+s[i])&255;s[i],s[j]=s[j],s[i];o[k]=v^s[(s[i]+s[j])&255]
 try:return zlib.decompress(o)
 except zlib.error:return bytes(o)
def vint(b,p):
 v=0;shift=0
 while True:
  x=b[p];p+=1;v|=(x&127)<<shift
  if not x&128:return v,p
  shift+=7
  if shift>64:raise ValueError('varint')
def fields(b):
 p=0;out=[]
 while p<len(b):
  key,p=vint(b,p);n,t=key>>3,key&7
  if not n:raise ValueError('invalid field')
  if t==0:v,p=vint(b,p)
  elif t==2:z,p=vint(b,p);v=b[p:p+z];p+=z
  elif t==5:v=b[p:p+4];p+=4
  elif t==1:v=b[p:p+8];p+=8
  else:raise ValueError('wire '+str(t))
  out.append((n,t,v))
 return out
z=zipfile.ZipFile(R/'jewel-coloring/static/splits/color.number.paint.pixle.art.sort.jigsaw.apk');b=z.read('assets/bin/Data/mainData')
d=decode(b);f=fields(d)
summary={'original_entry_sha256':hashlib.sha256(b).hexdigest(),'decoded_bytes':len(d),'decoded_sha256':hashlib.sha256(d).hexdigest(),'algorithm_evidence':['BigFile::BigFile(bool) RVA0x206ffa8 stores Android package at +0x58','BigFile::rc4_crypt RVA0x20709d4','BigFile::decryptAndDecompress RVA0x2072000'],'top_fields':dict(collections.Counter(str(n)+':'+str(t) for n,t,v in f))}
print(summary,flush=True)
records=[]
for n,t,v in f:
 if not isinstance(v,bytes):continue
 try:sub=fields(v)
 except:continue
 record={'field':n,'wire_fields':[(i,j,len(x) if isinstance(x,bytes) else x) for i,j,x in sub]}
 texts=[]
 for i,j,x in sub:
  if isinstance(x,bytes) and len(x)<350:
   try:
    st=x.decode('utf-8')
    if st.isprintable():texts.append((i,st))
   except:pass
 record['text_fields']=texts;records.append(record)
(O/'main-data-structure.json').write_text(json.dumps({'summary':summary,'records':records},indent=2),encoding='utf-8')
print('records',len(records),'examples',records[:3],flush=True)
targets=[]
for n,t,v in f:
 if n!=1 or t!=2:continue
 sub=fields(v);name=next((x.decode('utf-8') for i,j,x in sub if i==1 and j==2),None)
 if not name or not re.search(r'ad_worth|adjust_name_token|ad_source|user_group|gtuser|worth_event|^(appConf|appGrps|sdk_event|ad_rule)\.json$',name,re.I):continue
 meta=next((x for i,j,x in sub if i==2 and j==2),b'')
 try:
  mf=fields(meta);m=[]
  for i,j,x in mf:
   if isinstance(x,bytes):
    try:x=x.decode('utf-8')
    except:x=x.hex()
   m.append((i,j,x))
 except:m={'hex':meta.hex()}
 targets.append({'logical_path':name,'metadata':m})
(O/'target-resource-map.json').write_text(json.dumps(targets,ensure_ascii=False,indent=2),encoding='utf-8')
print('TARGETS',targets,flush=True)
def redact(v,key=''):
 if re.search(r'(?i)(secret|sdk.?key|api.?key|dev.?key|app.?key|password|access.?token)',key):return '[credential omitted]'
 if isinstance(v,dict):return {k:redact(x,k) for k,x in v.items()}
 if isinstance(v,list):return [redact(x,key) for x in v]
 return v
decoded=[]
for item in targets:
 path='assets/'+next(x[2] for x in item['metadata'] if x[0]==1)
 for apk in (R/'jewel-coloring/static/splits').glob('*.apk'):
  archive=zipfile.ZipFile(apk)
  if path not in archive.namelist():continue
  enc=archive.read(path);b=decode(enc)
  try:obj=json.loads(b.decode('utf-8'))
  except Exception as e:
   decoded.append({**item,'apk':apk.name,'entry':path,'decoded_bytes':len(b),'parse_error':str(e)});break
  # App configuration may embed SDK credentials: export only scoped research keys.
  if item['logical_path']=='appConf.json':
   def select(v):
    if not isinstance(v,dict):return {}
    result={}
    for k,x in v.items():
     if re.search(r'(?i)(worth|event|group|country|source|device|user|startapp|appType|bulldog|version)',k) and not re.search(r'(?i)secret|token|api|sdkkey|appkey',k):result[k]=redact(x,k)
     elif isinstance(x,dict):
      y=select(x)
      if y:result[k]=y
    return result
   safe=select(obj)
  else:safe=redact(obj)
  dest=O/(Path(item['logical_path']).name+'.redacted.json');dest.write_text(json.dumps(safe,ensure_ascii=False,indent=2),encoding='utf-8')
  decoded.append({**item,'apk':apk.name,'entry':path,'original_sha256':hashlib.sha256(enc).hexdigest(),'decoded_sha256':hashlib.sha256(b).hexdigest(),'decoded_bytes':len(b),'file':dest.name,'root_keys':list(obj) if isinstance(obj,dict) else 'array'})
  print('DECODED',item['logical_path'],len(b),'keys',list(obj)[:15] if isinstance(obj,dict) else len(obj),flush=True);break
(O/'decoded-config-provenance.json').write_text(json.dumps(decoded,ensure_ascii=False,indent=2),encoding='utf-8')
# Do not write full decoded archive or any unrelated credential-bearing config.
