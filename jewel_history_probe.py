from pathlib import Path
import requests,json,datetime,hashlib,zipfile
R=Path(__file__).resolve().parent/'jewel-coloring/deep/history';R.mkdir(parents=True,exist_ok=True);rows=[]
for code in [23,22]:
 u=f'https://d.apkpure.net/b/XAPK/color.number.paint.pixle.art.sort.jigsaw?version={code}'
 x={'url':u,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'requested_version_code':code}
 try:
  with requests.get(u,stream=True,timeout=(12,35)) as a:
   x.update(status=a.status_code,final_url=a.url,content_type=a.headers.get('Content-Type'))
   if a.status_code!=200 or 'html' in x['content_type'].lower():rows.append(x);continue
   p=R/f'version-code-{code}.xapk';h=hashlib.sha256();size=0
   with p.open('wb') as f:
    for b in a.iter_content(1024*1024):
     size+=len(b)
     if size>650*1024*1024:raise ValueError('size bound exceeded')
     f.write(b);h.update(b)
   x.update(file=p.name,bytes=size,sha256=h.hexdigest(),zip=zipfile.is_zipfile(p))
   if x['zip']:
    z=zipfile.ZipFile(p)
    if 'manifest.json' in z.namelist():
     m=json.loads(z.read('manifest.json'));x['identity']={k:m.get(k) for k in ['package_name','version_name','version_code']}
  rows.append(x)
  if x.get('zip'):break
 except Exception as e:x['error']=str(e);rows.append(x)
(R/'attempts.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
for x in rows:print(x.get('status'),x.get('identity'),x.get('bytes'),flush=True)
