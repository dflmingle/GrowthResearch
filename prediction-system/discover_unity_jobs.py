"""Read public SSR job listings and public job-detail JSON, without login."""
from pathlib import Path
import json,re,importlib.util
from bs4 import BeautifulSoup
from urllib.parse import urlsplit
R=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('follow',R/'follow_sources.py');f=importlib.util.module_from_spec(s);s.loader.exec_module(f)
if __name__=='__main__':
 raw=(R/'unity-ml-positions.raw').read_text(encoding='utf-8')
 decoder=json.JSONDecoder();chunks=[]
 for script in BeautifulSoup(raw,'html.parser').find_all('script'):
  text=script.string or script.get_text()
  for m in re.finditer(r'self\.__next_f\.push\(',text):
   try:
    a,_=decoder.raw_decode(text,m.end())
    if len(a)>1 and isinstance(a[1],str):chunks.append(a[1])
   except ValueError:pass
 text=''.join(chunks);jobs={}
 for m in re.finditer(r'\{"title":',text):
  try:j,_=decoder.raw_decode(text,m.start())
  except ValueError:continue
  if isinstance(j,dict) and j.get('externalUrl') and re.search('Vector|Ads Modeling|Machine Learning',j['title']):jobs[j['id']]=j
 (R/'UNITY_JOB_INDEX.json').write_text(json.dumps(list(jobs.values()),ensure_ascii=False,indent=2),encoding='utf-8')
 selected=[j for j in jobs.values() if re.search('Vector Bidding Science|Ads Modeling|Staff Backend Engineer, Vector',j['title'])][:3]
 urls={}
 for j in selected:
  print(j['id'],j['title'],j['externalUrl'])
  url=j['externalUrl'];path=urlsplit(url).path.split('/Unity',1)[-1]
  urls['unity-job-'+j['id']]='https://unitytech.wd1.myworkdayjobs.com/wday/cxs/unitytech/Unity'+path
 f.d.base.batch('unity-job-details',urls)
