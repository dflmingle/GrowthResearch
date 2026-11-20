from collect_sdk import acquire,R
import requests,json,datetime,hashlib,zipfile,sys
rows=[]
for v in ['1.6.1','1.7.1']:
 rows.append(acquire(('TikTok','Business','com.github.tiktok','tiktok-business-android-sdk',v,'https://jitpack.io','core')))
 u=f'https://codeload.github.com/tiktok/tiktok-business-android-sdk/zip/refs/tags/{v}';x={'vendor':'TikTok','sdk':'Business','version':v,'url':u,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  a=requests.get(u,timeout=(10,40));x['status']=a.status_code
  if a.ok and a.content.startswith(b'PK'):
   p=R/'TikTok/Business'/v/('github-source-'+v+'.zip');p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(a.content);x.update(path=str(p.relative_to(R)),sha256=hashlib.sha256(a.content).hexdigest())
   with zipfile.ZipFile(p) as z:
    prefix=z.namelist()[0];dest=p.parent/'github-source';dest.mkdir(exist_ok=True)
    for n in z.namelist():
     if not n.endswith(('.java','.kt','.gradle','.md','.properties','LICENSE')):continue
     q=(dest/n[len(prefix):]).resolve()
     if not q.is_relative_to(dest.resolve()):raise ValueError('unsafe source archive path')
     q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(z.read(n))
 except Exception as e:x['error']=str(e)
 rows.append(x);print('tiktok source',v,x.get('status'),flush=True)
urls={
 'metica-android':'https://docs.metica.com/api/android-sdk.md',
 'metica-index':'https://docs.metica.com/llms.txt',
 'metica-sitemap-pages':'https://docs.metica.com/sitemap-pages.xml',
}
for k,u in urls.items():
 x={'id':k,'url':u,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  a=requests.get(u,timeout=(10,30));p=R/'Discovery'/(k+'.txt');p.write_bytes(a.content);x.update(status=a.status_code,path=str(p.relative_to(R)),sha256=hashlib.sha256(a.content).hexdigest())
 except Exception as e:x['error']=str(e)
 rows.append(x);print(k,x.get('status'),flush=True)
(R/'DISCOVERED_MANIFEST.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
