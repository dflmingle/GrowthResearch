from pathlib import Path
import json,re,struct,io
from collections import defaultdict
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from elftools.elf.elffile import ELFFile
ROOT=Path('C:/Users/89trillion/game/car-race')
OUT=Path('D:/GrowthResearch/axon/deep/native-car');OUT.mkdir(parents=True,exist_ok=True)
types=json.loads(Path('D:/GrowthResearch/car-race/reused-evidence/monetization-20261117/method-index.json').read_text(encoding='utf-8'))
meta=(ROOT/'source/extracted/assets/bin/Data/Managed/Metadata/global-metadata.dat').read_bytes()
version=struct.unpack_from('<I',meta,4)[0]
if version>=38:
 lo,ls,lc,do,ds,dc=struct.unpack_from('<6I',meta,8)
 offsets=struct.unpack_from('<'+str(lc)+'I',meta,lo)
 assert ls==lc*4 and len(offsets)==dc+1 and offsets[-1]==ds
 literals=[meta[do+a:do+b].decode('utf-8',errors='replace') for a,b in zip(offsets,offsets[1:])]
else:
 lo,ls,do,ds=struct.unpack_from('<4I',meta,8)
 literals=[meta[do+off:do+off+n].decode('utf-8',errors='replace') for n,off in struct.iter_unpack('<II',meta[lo:lo+ls])]
raw=(ROOT/'source/extracted/lib/armeabi-v7a/libil2cpp.so').read_bytes()
def literal(v):
 if v is not None and v>>29==5 and v&1 and ((v&0x1fffffff)>>1)<len(literals):return literals[(v&0x1fffffff)>>1]
 return None
segments=[(s['p_vaddr'],s['p_offset'],s['p_filesz']) for s in ELFFile(io.BytesIO(raw)).iter_segments() if s['p_type']=='PT_LOAD']
def u32(addr):
 for va,off,size in segments:
  if va<=addr<va+size-3:return struct.unpack_from('<I',raw,off+addr-va)[0]
 return None
def literal(v):
 if v is not None and v>>29==5 and v&1 and ((v&0x1fffffff)>>1)<len(literals): return literals[(v&0x1fffffff)>>1]
def resolve(v):
 for depth in range(3):
  s=literal(v)
  if s is not None:return s
  if v is None:break
  v=u32(v)
 return None
byaddr=defaultdict(list)
allmethods=[]
for t in types:
 for m in t['methods']:
  label=f"{t['assembly']}::{t['namespace']}.{t['name']}.{m['name']}"
  byaddr[int(m['RVA'],16)&~1].append(label)
  allmethods.append((t,m,label))
def wanted(t):
 return t['assembly']=='Metica.SDK' and t['name'] in ['MeticaSdk','MeticaInitConfig','AndroidDelegate','AndroidNativeBridgeImpl','AndroidUnityBridge','AndroidInitConfigJson'] or t['assembly']=='Zego' and t['name']=='ZegoUserUID' or t['assembly']=='AdjustSdk.Scripts' and t['name']=='AdjustAndroid'

dec=Cs(CS_ARCH_ARM,CS_MODE_ARM)
def branch_target(addr):
 seen=set()
 while addr not in seen and addr not in byaddr:
  seen.add(addr)
  word=u32(addr)
  if word is None or word & 0xff000000 != 0xea000000:break
  delta=(word&0xffffff)<<2
  if delta & 0x2000000:delta-=0x4000000
  addr=(addr+8+delta)&0xffffffff
 return addr
evidence=[]; allcalls=defaultdict(list)
native_dir=OUT/'native';native_dir.mkdir(exist_ok=True)
for t,m,label in allmethods:
 if not wanted(t):continue
 if t['name']=='AdjustAndroid' and m['name']!='TrackEvent':continue
 start=int(m['Offset'],16)&~1; va=int(m['RVA'],16)&~1; length=int(m['Length'],16)
 if length>100000:continue
 regs={};strings=set();calls=[];lines=[f'// Original ARMv7 {label} RVA={va:#x} bytes={length}', '// String annotations: symbolic PC-relative loads into original encoded metadata slots; no generated IL implementation.']
 for ins in dec.disasm(raw[start:start+length],va):
  op=ins.op_str;mn=ins.mnemonic;note=[];parts=op.split(', ')
  if mn in ('bl','b','blx') and op.startswith('#'):
   target=int(op[1:],0);resolved=branch_target(target);labels=byaddr.get(resolved,[])
   if labels:
    calls.append({'pc':hex(ins.address),'target':hex(target),'resolved_target':hex(resolved),'methods':labels});note+=labels
    allcalls[hex(resolved)].append({'caller':label,'pc':hex(ins.address)})
  if mn=='movw':regs[parts[0]]=int(parts[1].lstrip('#'),0)
  elif mn=='movt':regs[parts[0]]=(regs.get(parts[0],0)&65535)|(int(parts[1].lstrip('#'),0)<<16)
  elif mn=='mov' and len(parts)==2:
   if parts[1].startswith('#'):regs[parts[0]]=int(parts[1][1:],0)&0xffffffff
   elif parts[1] in regs:regs[parts[0]]=regs[parts[1]]
   else:regs.pop(parts[0],None)
  elif mn=='add' and len(parts)==3:
   a=ins.address+8 if parts[1]=='pc' else regs.get(parts[1]);b=ins.address+8 if parts[2]=='pc' else (int(parts[2][1:],0) if parts[2].startswith('#') else regs.get(parts[2]))
   if a is not None and b is not None:regs[parts[0]]=(a+b)&0xffffffff
   else:regs.pop(parts[0],None)
  elif mn=='ldr':
   regmat=re.match(r'(\w+), \[(\w+), (\w+)\]$',op)
   if regmat:
    dst,base,ofs=regmat.groups();baseval=ins.address+8 if base=='pc' else regs.get(base)
    val=u32((baseval+regs[ofs])&0xffffffff) if baseval is not None and ofs in regs else None
    if val is not None:
     regs[dst]=val;s=resolve(val)
     if s is not None and (len(s)>100 or re.search(r'(?i)secret|api.?key|sdk.?key|password',s)):s='[credential-related or long literal omitted]'
     if s is not None and base=='pc':strings.add(s);note.append('STRING '+json.dumps(s,ensure_ascii=False))
    else:regs.pop(dst,None)
   mat=re.match(r'(\w+), \[(\w+)(?:, #(-?0x[0-9a-f]+|-?\d+))?\]$',op)
   if mat:
    dst,base,ofs=mat.groups();baseval=ins.address+8 if base=='pc' else regs.get(base)
    val=u32((baseval+int(ofs or '0',0))&0xffffffff) if baseval is not None else None
    if val is not None:
     regs[dst]=val
    else:regs.pop(dst,None)
  elif mn.startswith('bl'):
   pass
  elif parts and parts[0] in regs and mn not in ('cmp','tst','str','strb','strh','push','vstr'):
   regs.pop(parts[0],None)
  lines.append(f'{ins.address:08x}: {mn:10s} {op}'+(' // '+' | '.join(note) if note else ''))
  if mn in ('bl','blx'):
   for reg in ['r0','r1','r2','r3','ip']:regs.pop(reg,None)
 filename=re.sub(r'[^A-Za-z0-9_.-]','_',label)+f'-{va:x}.asm'
 (native_dir/filename).write_text('\n'.join(lines),encoding='utf-8')
 evidence.append({'method':label,'rva':hex(va),'length':length,'file':'native/'+filename,'strings':sorted(strings),'calls':calls})
(OUT/'method-evidence.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2),encoding='utf-8')
(OUT/'callers.json').write_text(json.dumps(allcalls,ensure_ascii=False,indent=2),encoding='utf-8')

print('native exported',len(evidence),flush=True)
