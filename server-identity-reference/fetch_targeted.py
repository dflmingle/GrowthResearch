"""Narrow primary-document follow-up after pin/license inspection; public GET only."""
from research import D,R,load,batch
pins={p['component']:p for p in load(D/'COMPONENT_PINS.json')}
paths={
 'splink':[
  ('theory','docs/topic_guides/theory/fellegi_sunter.md'),
  ('deterministic','docs/topic_guides/theory/probabilistic_vs_deterministic.md'),
  ('cluster-doc','docs/api_docs/clustering.md'),
  ('cluster-api','docs/api_docs/linker_clustering.md'),
  ('cluster-code','splink/internals/clustering.py'),
  ('version','pyproject.toml')],
 'dedupe':[
  ('how','docs/how-it-works/How-it-works.rst'),
  ('matching','docs/how-it-works/Matching-records.rst'),
  ('grouping','docs/how-it-works/Grouping-duplicates.rst'),
  ('threshold','docs/how-it-works/Choosing-a-good-threshold.rst'),
  ('cluster-code','dedupe/clustering.py'),
  ('version','pyproject.toml')],
 'recordlinkage':[
  ('classifiers','docs/ref-classifiers.rst'),
  ('datasets','docs/ref-datasets.rst'),
  ('evaluation','docs/ref-evaluation.rst'),
  ('version','pyproject.toml')],
 'feast':[
  ('point-time','docs/getting-started/concepts/point-in-time-joins.md'),
  ('entity','docs/getting-started/concepts/entity.md'),
  ('retrieval','docs/getting-started/concepts/feature-retrieval.md'),
  ('online','docs/reference/online-stores/README.md'),
  ('version','pyproject.toml')]
}
items=[]
for k,ls in paths.items():
 p=pins[k];base='https://raw.githubusercontent.com/'+p['repository']+'/'+p['commit']+'/'
 for label,path in ls:items.append((k+'-'+label,base+path,'Pinned official algorithm/feature documentation or licensed reference source; not vendor architecture'))
items.extend([
 ('oidc-core','https://openid.net/specs/openid-connect-core-1_0.html','Official protocol specification; documentary citation only'),
 ('w3c-prov','https://www.w3.org/TR/prov-dm/','Official provenance specification; documentary citation only')])
batch(items)
