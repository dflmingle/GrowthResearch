from pathlib import Path
import json
from urllib.parse import urlencode
D=Path(__file__).resolve().parent
requests=[
 ('al-infra-job','https://boards-api.greenhouse.io/v1/boards/applovin/jobs/4655740006'),
 ('al-analytics-job','https://boards-api.greenhouse.io/v1/boards/applovin/jobs/4705263006'),
 ('unity-careers','https://unity.com/careers/positions'),
 ('al-patent-assignee','https://patents.google.com/xhr/query?'+urlencode({'url':'assignee=Applovin&num=20','exp':''})),
 ('is-patent-identity','https://patents.google.com/xhr/query?'+urlencode({'url':'q=identity&assignee=ironSource&num=20','exp':''})),
 ('unity-paper-exact','https://api.openalex.org/works?'+urlencode({'search':'"Unity Ads" machine learning','per-page':10})),
 ('al-paper-exact','https://api.openalex.org/works?'+urlencode({'search':'"AppLovin" "representation"','per-page':10}))]
(D/'follow.json').write_text(json.dumps(requests,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
