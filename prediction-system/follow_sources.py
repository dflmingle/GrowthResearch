from pathlib import Path
import importlib.util,json,re
from urllib.parse import urlencode
from bs4 import BeautifulSoup
R=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('discovery',R/'search_sources.py')
d=importlib.util.module_from_spec(spec);spec.loader.exec_module(d)

if __name__=='__main__':
 jobs=json.loads((R/'applovin-public-jobs.raw').read_text(encoding='utf-8'))['jobs']
 selected=[]
 for j in jobs:
  if re.search('learn|scientist|research|data|infrastructure',j['title'],re.I):
   name='applovin-job-'+str(j['id'])+'.txt'
   content=BeautifulSoup(j.get('content',''),'html.parser').get_text('\n',strip=True)
   (R/name).write_text(j['title']+'\n'+j['absolute_url']+'\nupdated_at='+j.get('updated_at','unknown')+'\n'+content,encoding='utf-8')
   selected.append(dict(id=j['id'],title=j['title'],url=j['absolute_url'],updated_at=j.get('updated_at'),path='prediction-system/'+name))
 (R/'JOB_INDEX.json').write_text(json.dumps(selected,ensure_ascii=False,indent=2),encoding='utf-8')
 urls={k.replace('search-','bing-'):'https://www.bing.com/search?'+urlencode({'q':q,'format':'rss'}) for k,q in d.queries.items()}
 urls.update({'unity-careers':'https://unity.com/careers','applovin-blog-index':'https://www.applovin.com/blog/',
  'unity-public-jobs-alternate':'https://boards-api.greenhouse.io/v1/boards/unity/jobs?content=true',
  'patents-applovin-results':'https://patents.google.com/xhr/query?'+urlencode({'url':'assignee=AppLovin&q=(advertising prediction)','exp':''}),
  'patents-unity-results':'https://patents.google.com/xhr/query?'+urlencode({'url':'assignee=Unity Technologies&q=(user value prediction)','exp':''})})
 d.base.batch('followup',urls)
