from pathlib import Path
import io,json,re,subprocess,hashlib
from elftools.elf.elffile import ELFFile
from capstone import Cs,CS_ARCH_ARM64,CS_MODE_ARM
ROOT=Path(__file__).resolve().parent/'jewel-coloring/static'
p=ROOT/'native-inputs/lib/arm64-v8a/libMyGame.so';raw=p.read_bytes();elf=ELFFile(io.BytesIO(raw))
segs=[(s['p_vaddr'],s['p_offset'],s['p_filesz']) for s in elf.iter_segments() if s['p_type']=='PT_LOAD']
def data(addr,n=256):
 for va,off,size in segs:
  if va<=addr<va+size:return raw[off+addr-va:off+addr-va+min(n,size-(addr-va))]
 return b''
def string(addr):
 b=data(addr,350).split(b'\0')[0]
 if 3<=len(b)<300 and all(32<=c<127 for c in b):return b.decode()
 return None
syms=[s for s in elf.get_section_by_name('.dynsym').iter_symbols() if s.name and s['st_value']]
names=[s.name for s in syms];demangled=subprocess.check_output(['C:/msys64/mingw64/bin/c++filt.exe'],input=('\n'.join(names)+'\n').encode()).decode().splitlines()
byaddr={s['st_value']:n for s,n in zip(syms,demangled)}
byname={s.name:n for s,n in zip(syms,demangled)}
plt=elf.get_section_by_name('.plt');rel=elf.get_section_by_name('.rela.plt');dyn=elf.get_section_by_name('.dynsym')
if plt and rel:
 for i,r in enumerate(rel.iter_relocations()):
  s=dyn.get_symbol(r['r_info_sym']);name=s.name
  byaddr[plt['sh_addr']+32+i*16]=byname.get(name,name)
selected=[]
for s,n in zip(syms,demangled):
 if s['st_info']['type']!='STT_FUNC' or not s['st_size'] or s['st_size']>60000:continue
 if not re.search(r'(ad::event::(AdWorthEvent|AWEC|AWESend)|ad::AdWorth|adsource::AdSourceUtils|BulldogPlatform::.*(Worth|Adjust|Revenue|Facebook|Tiktok)|RedAnalytics|GRT|XGBoost|Predict.*Worth)',n):continue
 if n.startswith(('std::','non-virtual thunk','vtable','typeinfo')):continue
 selected.append((s,n))
dec=Cs(CS_ARCH_ARM64,CS_MODE_ARM);dec.detail=True;out=ROOT/'native-evidence';out.mkdir(exist_ok=True);records=[];allcalls=[]
for s,name in selected:
 va=s['st_value'];regs={};lits=set();calls=[];lines=[f'// Original ARM64 libMyGame.so SHA256={hashlib.sha256(raw).hexdigest()}',f'// {name} RVA={va:#x} size={s["st_size"]}']
 for ins in dec.disasm(data(va,s['st_size']),va):
  op=ins.op_str;parts=op.split(', ');note=[]
  if ins.mnemonic=='adrp':
   try:regs[parts[0]]=int(parts[1].lstrip('#'),0)
   except:pass
  elif ins.mnemonic=='adr':
   try:regs[parts[0]]=int(parts[1].lstrip('#'),0)
   except:pass
  elif ins.mnemonic=='add' and len(parts)==3:
   try:regs[parts[0]]=regs[parts[1]]+int(parts[2].lstrip('#'),0)
   except:regs.pop(parts[0],None)
  elif ins.mnemonic=='ldr' and len(parts)>1:
   m=re.match(r'(\w+), \[(\w+)(?:, #(0x[0-9a-f]+|\d+))?\]$',op)
   if m and m[2] in regs:
    b=data(regs[m[2]]+int(m[3] or '0',0),8)
    if len(b)==8:regs[m[1]]=int.from_bytes(b,'little')
    else:regs.pop(parts[0],None)
   else:regs.pop(parts[0],None)
  elif ins.mnemonic=='mov' and len(parts)==2:
   if parts[1] in regs:regs[parts[0]]=regs[parts[1]]
   else:regs.pop(parts[0],None)
  else:
   try:
    for regid in ins.regs_access()[1]:regs.pop(ins.reg_name(regid),None)
   except Exception:pass
  for reg in list(regs):
   st=string(regs[reg])
   if st and reg in parts[:1] and not st.startswith(('_Z','Java_')):lits.add(st);note.append(reg+' STRING '+json.dumps(st))
  if ins.mnemonic in ['bl','b'] and op.startswith('#'):
   addr=int(op[1:],0);callee=byaddr.get(addr)
   if callee:calls.append({'pc':hex(ins.address),'target':hex(addr),'callee':callee});note.append(callee)
  lines.append(f'{ins.address:08x}: {ins.mnemonic:10s} {op}'+(' // '+' | '.join(note) if note else ''))
  if ins.mnemonic in ['bl','blr']:
   for i in range(19):regs.pop('x'+str(i),None)
 filename=re.sub('[^A-Za-z0-9_.-]','_',name)[:105]+f'-{va:x}.asm';(out/filename).write_text('\n'.join(lines),encoding='utf-8');records.append({'name':name,'rva':hex(va),'size':s['st_size'],'file':'native-evidence/'+filename,'strings':sorted(lits),'calls':calls})
(ROOT/'native-method-evidence.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
print('Exported native growth functions',len(records))
