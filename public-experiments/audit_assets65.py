from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
from datetime import datetime,timezone
import requests,json,hashlib,zipfile,tarfile,io,csv

ROOT=Path(r'D:\GrowthResearch');OUT=ROOT/'public-experiments'/'audit';OUT.mkdir(parents=True,exist_ok=True)
def download(ident,url,cap):
    p=OUT/(ident+'.download')
    record={'id':ident,'url':url,'observed_utc':datetime.now(timezone.utc).isoformat(),'byte_cap':cap,'real_identity_reconstruction':False}
    try:
        if p.exists():data=p.read_bytes();record.update(status=200,cached=True)
        else:
            with requests.get(url,stream=True,timeout=(12,35)) as r:
                record.update(status=r.status_code,final_url=r.url,content_type=r.headers.get('Content-Type'),declared_length=r.headers.get('Content-Length'))
                if r.status_code!=200:return record
                chunks=[];size=0
                for chunk in r.iter_content(256*1024):
                    size+=len(chunk)
                    if size>cap:raise ValueError('bounded download cap exceeded; stopped')
                    chunks.append(chunk)
                data=b''.join(chunks)
            p.write_bytes(data)
        record.update(path=p.relative_to(ROOT).as_posix(),bytes=len(data),sha256=hashlib.sha256(data).hexdigest())
        if ident=='retail352':
            z=zipfile.ZipFile(io.BytesIO(data));record['archive_entries']=z.namelist()
            import pandas as pd
            frame=pd.read_excel(z.open('Online Retail.xlsx'),engine='openpyxl')
            record['structural_audit']={'rows':len(frame),'columns':list(frame.columns),'dtypes':{k:str(v) for k,v in frame.dtypes.items()},'missing_counts':{k:int(v) for k,v in frame.isna().sum().items()},'min_event_time':str(frame.InvoiceDate.min()),'max_event_time':str(frame.InvoiceDate.max()),'complete_row_duplicates':int(frame.duplicated().sum()),'nonpositive_unit_price_rows':int((frame.UnitPrice<=0).sum()),'nonpositive_quantity_rows':int((frame.Quantity<=0).sum()),'customer_keys_are_source_scoped_not_cross_app_identity':True,'no_row_values_exported':True}
        elif ident=='kuairand-pure':
            entries=[];headers={};licenses={}
            with tarfile.open(fileobj=io.BytesIO(data),mode='r:gz') as tar:
                for m in tar:
                    entries.append({'name':m.name,'bytes':m.size})
                    if m.isfile() and m.name.endswith('.csv'):
                        headers[m.name]=tar.extractfile(m).readline().decode('utf-8-sig',errors='replace').strip()
                    if m.isfile() and any(n in m.name.lower() for n in ['license','readme']):
                        licenses[m.name]=tar.extractfile(m).read(25000).decode('utf-8',errors='replace')
            record.update(archive_entries=entries,csv_headers=headers,archive_license_readme=licenses,no_person_level_values_exported=True)
        elif ident=='zenodo-game-model':
            z=zipfile.ZipFile(io.BytesIO(data));record['archive_entries']=z.namelist()
            record['data_or_license_docs']={name:z.read(name).decode('utf-8',errors='replace')[:16000] for name in z.namelist() if any(k in name.lower() for k in ['readme','license']) and not name.endswith('/')}
    except Exception as e:record['error']=type(e).__name__+': '+str(e)
    return record

if __name__=='__main__':
    jobs=[('retail352','https://archive.ics.uci.edu/static/public/352/online+retail.zip',30_000_000),('kuairand-pure','https://zenodo.org/api/records/10439422/files/KuaiRand-Pure.tar.gz/content',55_000_000),('zenodo-game-model','https://zenodo.org/api/records/24211987/files/code_R1_v1.zip/content',400_000)]
    results=[]
    with ThreadPoolExecutor(max_workers=3) as pool:
        for f in as_completed([pool.submit(download,*job) for job in jobs]):
            x=f.result();results.append(x);print(json.dumps({k:x.get(k) for k in ['id','status','bytes','error']},ensure_ascii=True),flush=True)
    (OUT/'ASSET_VERIFICATION.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
