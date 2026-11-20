"""Bounded excerpts from existing public snapshots; no SDK or JS execution."""
from pathlib import Path
import json,re,hashlib
ROOT=Path(__file__).resolve().parent.parent;R=ROOT/'ltv'
specs=[
 ('AXON_INPUTS','nongame/applovin-axon-about.txt',r'What data does Axon AI use',20),
 ('AXON_PREDICTION','nongame/applovin-axon-about.txt',r'How does Axon AI work',12),
 ('AXON_COMBINATION','nongame/applovin-policy-direct.txt',r'collected automatically across mobile apps',12),
 ('AXON_TRUE_PURCHASE','axon/doc-in-app-purchase-revenue-sharing.txt',r'Please only send revenue',16),
 ('MAX_ILRD','axon/max-ilrd.txt',r'Impression-level user revenue API',24),
 ('MAX_PRECISION','axon/max-ilrd.txt',r'This precision takes',15),
 ('VECTOR_GAME_DNA','vector/unity-vector-correct.txt',r'Vector AI goes beyond',12),
 ('VECTOR_POSTBACK','vector/unity-vector-correct.txt',r'Send attributed',8),
 ('VECTOR_IAP_LINK','vector/unity-2026-keynote.txt',r'purchase data collected',5),
 ('UNITY_VALUE_BIDS','vector/doc-intro-to-roas-campaigns.txt',r'With a ROAS campaign',8),
 ('UNITY_WINDOWS','vector/doc-intro-to-roas-campaigns.txt',r'After you select your optimization',18),
 ('UNITY_MATURITY','vector/doc-intro-to-roas-campaigns.txt',r'### Data cohorts and maturity',15),
 ('UNITY_LEARNING','vector/doc-intro-to-roas-campaigns.txt',r'#### Learning phase thresholds',23),
 ('UNITY_POSTBACK_EVENTS','vector/doc-send-postbacks.txt',r'Ad revenue event flag',14),
 ('MMP_CONFIG','axon/doc-appsflyer.txt',r'In-app event postbacks window',45),
 ('DDF_PRIVACY','vector/ddf-end-user-consent.txt',r'ads_intent',15),
]
out=[]
for key,path,pattern,after in specs:
 p=ROOT/path
 if not p.exists():out.append(dict(id=key,path=path,status='missing_source'));continue
 lines=p.read_text(encoding='utf-8').splitlines();hits=[i for i,s in enumerate(lines) if re.search(pattern,s,re.I)]
 if not hits:out.append(dict(id=key,path=path,status='pattern_not_found'));continue
 i=hits[0];start=max(0,i-2);end=min(len(lines),i+after)
 out.append(dict(id=key,path=path,status='excerpted',sha256=hashlib.sha256(p.read_bytes()).hexdigest(),
  start_line=start+1,end_line=end,text='\n'.join(f'{j+1}: {s}' for j,s in enumerate(lines) if start<=j<end)))
(R/'SOURCE_EXCERPTS.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print('excerpts',sum(x['status']=='excerpted' for x in out),'of',len(out))
for x in out:
 if x['status']!='excerpted':print(x)
