from pathlib import Path
import requests,json,hashlib,datetime,re,sys
from bs4 import BeautifulSoup
R=Path(__file__).resolve().parent;sys.stdout.reconfigure(encoding='utf-8');out=R/'Discovery';out.mkdir(exist_ok=True)
urls={
 'tiktok-tags':'https://api.github.com/repos/tiktok/tiktok-business-android-sdk/tags?per_page=100',
 'tiktok-contents':'https://api.github.com/repos/tiktok/tiktok-business-android-sdk/contents',
 'tiktok-build':'https://raw.githubusercontent.com/tiktok/tiktok-business-android-sdk/master/build.gradle',
 'metica-maven-search':'https://search.maven.org/solrsearch/select?q=metica&rows=30&wt=json',
 'metica-github-org':'https://api.github.com/orgs/Metica/repos?per_page=100',
 'metica-docs-sitemap':'https://docs.metica.com/sitemap.xml',
 'applovin-github-readme':'https://raw.githubusercontent.com/AppLovin/AppLovin-MAX-SDK-Android/master/README.md',
 'adjust-release-550':'https://api.github.com/repos/adjust/android_sdk/releases/tags/v5.5.0',
 'adjust-release-570':'https://api.github.com/repos/adjust/android_sdk/releases/tags/v5.7.0',
}
rows=[]
for k,u in urls.items():
 x={'id':k,'url':u,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  a=requests.get(u,timeout=(10,25));x.update(status=a.status_code,final_url=a.url)
  p=out/(k+('.json' if 'api.github' in u or 'solrsearch' in u else '.txt'));p.write_bytes(a.content);x.update(path=str(p.relative_to(R)),sha256=hashlib.sha256(a.content).hexdigest())
  if k=='metica-docs-sitemap' and a.ok:
   x['sdk_pages']=[v for v in re.findall(r'<loc>(.*?)</loc>',a.text) if re.search('android|sdk|install|unity',v,re.I)]
 except Exception as e:x['error']=str(e)
 rows.append(x);print(k,x.get('status'),flush=True)
(R/'DISCOVERY_ADDITIONAL.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
