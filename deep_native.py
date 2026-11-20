from pathlib import Path
import io,json,re,subprocess,hashlib,sys,collections
from elftools.elf.elffile import ELFFile
from capstone import Cs,CS_ARCH_ARM64,CS_MODE_ARM
R=Path(__file__).resolve().parent;O=R/'jewel-coloring/deep';O.mkdir(exist_ok=True)
p=R/'jewel-coloring/static/native-inputs/lib/arm64-v8a/libMyGame.so';raw=p.read_bytes();elf=ELFFile(io.BytesIO(raw));sha=hashlib.sha256(raw).hexdigest()
segs=[(s['p_vaddr'],s['p_offset'],s['p_filesz']) for s in elf.iter_segments() if s['p_type']=='PT_LOAD']
def data(a,n):
 for v,o,z in segs:
  if v<=a<v+z:return raw[o+a-v:o+a-v+min(n,z-a+v)]
 return b''
syms=[s for s in elf.get_section_by_name('.dynsym').iter_symbols() if s.name and s['st_value']]
names=subprocess.check_output(['C:/msys64/mingw64/bin/c++filt.exe'],input=('\n'.join(s.name for s in syms)+'\n').encode()).decode().splitlines()
byaddr={s['st_value']:n for s,n in zip(syms,names)};byname={s.name:n for s,n in zip(syms,names)}
plt=elf.get_section_by_name('.plt');rel=elf.get_section_by_name('.rela.plt');dyn=elf.get_section_by_name('.dynsym')
for i,x in enumerate(rel.iter_relocations()):
 s=dyn.get_symbol(x['r_info_sym']);byaddr[plt['sh_addr']+32+i*16]=byname.get(s.name,s.name)
interesting=re.compile(r'AdWorth|ad::event::|AdSource|BulldogPlatform::.*(Config|User|Device|Id|ID|Uuid|UUID|Adjust|Revenue|Facebook|Tiktok)|redAnalytics::|DataSync|ConfigUtils|ConfigManager|Analytics.*(User|Id)|CrossPromotion|Identity|Audience|BulldogSdk::|gtuser2::|UserGroup|HotUpdate|cocos2d::FileUtils::|FileUtilsAndroid::|AccountController::|RedUser|BigFile::|readFile|decrypt|Decrypt|DeviceIdUtils::')
functions=[(s,n) for s,n in zip(syms,names) if s['st_info']['type']=='STT_FUNC' and s['st_size'] and not n.startswith(('std::','non-virtual thunk'))]
(O/'all-functions.json').write_text(json.dumps([{'name':n,'rva':hex(s['st_value']),'size':s['st_size']} for s,n in functions],indent=2),encoding='utf-8')
selected=[(s,n) for s,n in functions if interesting.search(n)];idx=[{'name':n,'rva':hex(s['st_value']),'size':s['st_size'],'mangled':s.name} for s,n in selected]
(O/'symbol-index.json').write_text(json.dumps(idx,indent=2),encoding='utf-8')
selected_names={n for _,n in selected};dec=Cs(CS_ARCH_ARM64,CS_MODE_ARM);records=[];callers=[];out=O/'asm';out.mkdir(exist_ok=True)
for count,(s,name) in enumerate(functions):
 va=s['st_value'];selected_here=name in selected_names;calls=[];lines=[f'// Original SHA256 {sha}',f'// {name} RVA={va:#x} size={s["st_size"]}'] if selected_here else None
 # Cheap AArch64 BL/B immediates before full disassembly, retaining original PC and resolved target.
 b=data(va,s['st_size'])
 for j in range(0,len(b)-3,4):
  w=int.from_bytes(b[j:j+4],'little')
  if w&0x7c000000!=0x14000000:continue
  imm=w&0x3ffffff;imm=imm-(1<<26) if imm&(1<<25) else imm;target=va+j+imm*4;callee=byaddr.get(target)
  if callee:
   c={'pc':hex(va+j),'target':hex(target),'callee':callee};calls.append(c)
   if callee in selected_names:callers.append({'caller':name,'caller_rva':hex(va),**c})
 if selected_here:
  for a,z,mn,op in dec.disasm_lite(b,va):
   note=''
   if mn in ['bl','b'] and op.startswith('#'):note=byaddr.get(int(op[1:],0),'')
   lines.append(f'{a:08x}: {mn:10s} {op}'+(' // '+note if note else ''))
  fn=re.sub('[^A-Za-z0-9_.-]','_',name)[:110]+f'-{va:x}.asm';(out/fn).write_text('\n'.join(lines),encoding='utf-8');records.append({'name':name,'rva':hex(va),'size':s['st_size'],'file':'asm/'+fn,'calls':calls})
(O/'method-index.json').write_text(json.dumps(records,indent=2),encoding='utf-8');(O/'direct-callers.json').write_text(json.dumps(callers,indent=2),encoding='utf-8')
print('native symbols',len(idx),'all functions scanned',len(functions),'target incoming calls',len(callers),flush=True)
