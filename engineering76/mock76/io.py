from pathlib import Path
import hashlib,json,os

def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False)
def digest(x):return hashlib.sha256(canonical(x).encode()).hexdigest()
def read(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def write(p,x):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
    temp=p.with_suffix(p.suffix+'.tmp')
    temp.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    os.replace(temp,p)

class Ledger:
    def __init__(self,path):self.path=Path(path)
    def records(self):
        if not self.path.exists():return []
        return [json.loads(s) for s in self.path.read_text('utf-8').splitlines()]
    def append(self,kind,time,**data):
        rows=self.records();rec=dict(seq=len(rows)+1,prev=rows[-1]['hash'] if rows else '0'*64,kind=kind,time=time,data=data)
        rec['hash']=digest(rec)
        self.path.parent.mkdir(parents=True,exist_ok=True)
        with self.path.open('a',encoding='utf-8',newline='\n') as f:f.write(canonical(rec)+'\n')
        return rec['seq']

def verify(rows):
    previous='0'*64
    for i,r in enumerate(rows,1):
        bare={k:v for k,v in r.items() if k!='hash'}
        if r.get('seq')!=i or r.get('prev')!=previous or r.get('hash')!=digest(bare):return False
        previous=r['hash']
    return True
