from pathlib import Path
import json,requests,tarfile,hashlib,datetime
R=Path(__file__).resolve().parent
m=json.loads((R/'unity-auth-package.raw').read_text(encoding='utf-8'))
ver='3.9.0';row=m['versions'][ver];u=row['dist']['tarball'];d=R/'sdk/authentication'/ver;d.mkdir(parents=True,exist_ok=True)
p=d/'authentication-3.9.0.tgz'
assert not p.exists(),'Do not redownload'
a=requests.get(u,timeout=(8,25));a.raise_for_status();assert len(a.content)<12_000_000
p.write_bytes(a.content)
sha1=hashlib.sha1(p.read_bytes()).hexdigest()
assert sha1==row['dist']['shasum'],'registry integrity'
with tarfile.open(p) as t:
 members=t.getmembers();safe=[]
 for z in members:
  if not z.isfile():continue
  out=d/'extracted'/z.name
  assert out.resolve().is_relative_to((d/'extracted').resolve())
  if out.suffix.lower() in ['.cs','.md','.json','.txt','.asmdef']:
   out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(t.extractfile(z).read())
 (d/'archive-index.json').write_text(json.dumps([z.name for z in members],indent=2),encoding='utf-8')
(d/'provenance.json').write_text(json.dumps({'url':u,'version':ver,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'registry_sha1_matches':True,'registry_shasum':row['dist']['shasum'],'license':row.get('license'),'scope':'official Unity UPM public package source; static only; not any game version match'},indent=2),encoding='utf-8')
print('Official Authentication',ver,len(a.content),'bytes, registry SHA1 verified')
