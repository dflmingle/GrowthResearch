from pathlib import Path
import json,hashlib,requests,datetime,zipfile
R=Path(__file__).resolve().parent
version='12.17.0';dest=R/'packages/singular'/version;dest.mkdir(parents=True,exist_ok=True)
rows=[]
for suffix in ['.pom','.aar','-sources.jar']:
 url=f'https://maven.singular.net/com/singular/sdk/singular_sdk/{version}/singular_sdk-{version}{suffix}'
 p=dest/('singular_sdk-'+version+suffix)
 row=dict(url=url,utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),path=p.relative_to(R.parent).as_posix())
 if p.exists():row.update(reused=True,sha256=hashlib.sha256(p.read_bytes()).hexdigest());rows.append(row);continue
 try:
  a=requests.get(url,timeout=(8,20));row.update(status=a.status_code,last_modified=a.headers.get('Last-Modified'))
  if a.status_code==200:
   p.write_bytes(a.content);row.update(sha256=hashlib.sha256(a.content).hexdigest(),bytes=len(a.content))
   if suffix=='.aar':
    with zipfile.ZipFile(p) as z:(dest/'classes.jar').write_bytes(z.read('classes.jar'))
 except Exception as e:row['error']=str(e)
 rows.append(row)
print([(x.get('status'),x['url']) for x in rows])
(dest/'provenance.json').write_text(json.dumps(dict(sdk='Singular Android',version=version,source='official vendor Maven',artifacts=rows,scope='standalone, no target game integration established'),indent=2),encoding='utf-8')
