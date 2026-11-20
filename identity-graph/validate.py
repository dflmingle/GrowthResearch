"""Check identity research citations and static-source integrity, offline only."""
from pathlib import Path
import json,hashlib,re,urllib.parse,tarfile

R=Path(__file__).resolve().parent.parent
G=R/'identity-graph'
reports=[next(R.glob(f'{n}_*.md')) for n in range(31,35)]
errors=[];links=0
for p in reports:
    s=p.read_text(encoding='utf-8')
    assert '\ufffd' not in s,p
    for label,target in re.findall(r'\[([^\]]*)\]\(([^)]+)\)',s):
        if target.startswith(('https://','http://','mailto:')):continue
        links+=1
        file,_,anchor=urllib.parse.unquote(target).partition('#')
        dest=p.parent/file if file else p
        if not dest.is_file():errors.append(f'missing citation: {p.name}: {target}');continue
        if anchor and file=='EVIDENCE_INDEX.md':
            if f'id="{anchor}"' not in dest.read_text(encoding='utf-8'):
                errors.append(f'missing index anchor: {p.name}: {anchor}')

m=json.loads((R/'EVIDENCE_MANIFEST.json').read_text(encoding='utf-8'))
groups=[x for x in m['entries'] if re.fullmatch(r'IG\d\d',x.get('id',''))]
assert len(groups)==12
hashed=0
for e in groups:
    for s in e['sources']:
        p=R/s['path']
        if not p.is_file():errors.append('missing source '+s['path']);continue
        actual=hashlib.sha256(p.read_bytes()).hexdigest();hashed+=1
        if actual!=s['sha256']:errors.append('hash mismatch '+s['path'])

sdk=json.loads((G/'SDK_IDENTITY_AUDIT.json').read_text())
for s in sdk:
    p=R/s['jar']
    if hashlib.sha256(p.read_bytes()).hexdigest()!=s['sha256']:errors.append('SDK input changed '+str(p))

auth=G/'sdk/authentication/3.9.0'
prov=json.loads((auth/'provenance.json').read_text())
archive=next(auth.glob('*.tgz'))
assert hashlib.sha256(archive.read_bytes()).hexdigest()==prov['sha256']
assert hashlib.sha1(archive.read_bytes()).hexdigest()==prov['registry_shasum']
excerpts=json.loads((G/'IDENTITY_CODE_EXCERPTS.json').read_text())
with tarfile.open(archive,'r:gz') as tar:
    checked=0
    for x in excerpts:
        key='identity-graph/sdk/authentication/3.9.0/extracted/'
        if x['path'].startswith(key):
            path=x['path'][len(key):]
            if tar.extractfile(path).read()!=(R/x['path']).read_bytes():errors.append('UPM extracted content differs '+path)
            checked+=1

pixel=json.loads((G/'PIXEL_IDENTITY_EXCERPTS.json').read_text())
raw=(R/'nongame/pixel-source.raw').read_text(encoding='utf-8')
for x in pixel:
    if x.get('found') is False:errors.append('unresolved static snippet '+x['id']);continue
    offset=x['character_offset']
    if raw[offset:offset+len(x['original'])]!=x['original']:errors.append('pixel offset mismatch '+x['id'])

result=dict(status='PASS' if not errors else 'FAIL',reports=[dict(path=p.name,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in reports],
            local_links_checked=links,evidence_groups=len(groups),source_hashes_checked=hashed,
            official_sdk_inputs_rechecked=len(sdk),authentication_archive_sha256=prov['sha256'],
            authentication_archive_registry_sha1_matches=True,auth_source_excerpts_compared_to_archive=checked,
            pixel_original_offsets_checked=len(pixel),errors=errors,
            scope='Offline artifact checks only. Does not prove server matches, event delivery, target app activation or model use.')
(G/'VALIDATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
raise SystemExit(1 if errors else 0)
