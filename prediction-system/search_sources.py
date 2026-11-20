"""Bounded public-document discovery; no SDK execution or production ad traffic."""
from pathlib import Path
import importlib.util,json
from urllib.parse import urlencode

R=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('public_collect',R.parent/'identity-graph/collect.py')
base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base);base.R=R
queries={
 'search-axon-engineering':'AppLovin Axon engineering LTV prediction embeddings feature store',
 'search-axon-research':'AppLovin Axon multi-task learning delayed feedback patent inventors',
 'search-vector-engineering':'Unity Vector machine learning embeddings real time inference',
 'search-vector-data':'site:unity.com Vector first party gameplay data prediction',
 'search-axon-features':'site:applovin.com Axon model training identity user revenue',
 'search-vector-research':'Unity Ads Vector research multi task learning delayed feedback',
 'search-axon-incrementality':'site:applovin.com incrementality Axon experiment',
 'search-vector-case':'site:unity.com Vector ROAS D28 test methodology',
}
if __name__=='__main__':
 urls={k:'https://www.google.com/search?'+urlencode({'q':q}) for k,q in queries.items()}
 urls.update({
  'applovin-public-jobs':'https://boards-api.greenhouse.io/v1/boards/applovin/jobs?content=true',
  'unity-public-jobs':'https://boards-api.greenhouse.io/v1/boards/unity3d/jobs?content=true',
  'patents-applovin':'https://patents.google.com/?q=(machine+learning+advertising)&assignee=AppLovin',
  'patents-unity':'https://patents.google.com/?q=(user+value+prediction)&assignee=Unity+Technologies',
 })
 base.batch('discovery',urls)
