"""Text-only provenance/symbol locators/diffs for three approved MIT source JARs.
Not a Java compiler, SDK runner, or behavioral test.
"""
from pathlib import Path
import difflib,hashlib,json,re

R=Path(__file__).resolve().parent.parent
D=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def mask(text):
    # Preserve positions/newlines while ignoring braces in comments and literals.
    pattern=r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\''
    return re.sub(pattern,lambda m:''.join('\n' if c=='\n' else ' ' for c in m.group()),text)

records= json.loads((D/'EXTRACTED_FILES.json').read_text(encoding='utf-8'))
symbols=[]
declaration=re.compile(r'(?m)^    (?:(?:public|private|protected|static|final|synchronized|native|abstract)\s+)*(?:<[^\n]+?>\s+)?(?:[\w.<>,?\[\]]+\s+)?(?P<name>\w+)\s*\([^;{}]*?\)\s*(?:throws\s+[^{};]+)?\s*\{')
for f in records:
    p=R/f['path'];assert sha(p)==f['sha256']
    text=p.read_text(encoding='utf-8-sig');clean=mask(text)
    for m in declaration.finditer(clean):
        start=m.start();op=clean.index('{',m.start(),m.end());depth=1;end=op+1
        while depth and end<len(clean):
            depth+=(clean[end]=='{')-(clean[end]=='}');end+=1
        assert depth==0,(p,m['name'])
        symbols.append(dict(sample_id=f['sample_id'],version=f['version'],archive=f['archive'],archive_sha256=f['archive_sha256'],
          entry=f['entry'],path=f['path'],sha256=f['sha256'],class_name=f['entry'].removesuffix('.java').replace('/','.'),
          method=m['name'],start_line=text[:start].count('\n')+1,end_line=text[:end].count('\n')+1,
          normalized_method_sha256=hashlib.sha256(text[start:end].encode('utf-8')).hexdigest(),
          locator_kind='Lexical Java method locator;manually reviewed call chains,not full AST/type resolution'))
save(D/'SYMBOL_INDEX.json',symbols)

diffs=[];(D/'diffs-final').mkdir(exist_ok=True)
for a,b in [('5.5.0','5.7.0'),('5.7.0','5.8.1')]:
    aa={x['entry']:x for x in records if x['version']==a};bb={x['entry']:x for x in records if x['version']==b}
    for entry in sorted(set(aa)|set(bb)):
        at=(R/aa[entry]['path']).read_text(encoding='utf-8-sig').splitlines(keepends=True) if entry in aa else []
        bt=(R/bb[entry]['path']).read_text(encoding='utf-8-sig').splitlines(keepends=True) if entry in bb else []
        delta=list(difflib.unified_diff(at,bt,fromfile=a+'/'+entry,tofile=b+'/'+entry))
        dest=None;digest=None
        if delta:
            p=D/'diffs-final'/(a+'_'+b+'_'+entry.replace('/','_')+'.diff')
            p.write_text(''.join(delta),encoding='utf-8');dest=p.relative_to(R).as_posix();digest=sha(p)
        diffs.append(dict(from_version=a,to_version=b,entry=entry,status='UNCHANGED' if not delta else ('ADDED' if not at else 'REMOVED' if not bt else 'CHANGED'),
          from_path=aa.get(entry,{}).get('path'),to_path=bb.get(entry,{}).get('path'),from_sha256=aa.get(entry,{}).get('sha256'),
          to_sha256=bb.get(entry,{}).get('sha256'),diff_path=dest,diff_sha256=digest,
          comparison_scope='Selected allowed sources only;normalized newlines,no SDK-wide equivalence claim'))
save(D/'DIFF_INDEX.final.json',diffs)
print(json.dumps(dict(selected_files=len(records),located_methods=len(symbols),diffs=len([d for d in diffs if d['status']!='UNCHANGED'])),ensure_ascii=False))
