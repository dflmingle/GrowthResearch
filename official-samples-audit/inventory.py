"""Hash selected existing packages; inspect POM and license entries only."""
from pathlib import Path
import base64,csv,datetime,hashlib,json,xml.etree.ElementTree as ET,zipfile

R=Path(__file__).resolve().parent.parent
D=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):
    if p.exists():
        assert json.loads(p.read_text(encoding='utf-8-sig'))==x,p
        return
    p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def table(p,rs):
    assert rs and not p.exists()
    with p.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rs[0]));w.writeheader();w.writerows(rs)

selected=[
 'ThirdPartySDKs/AppLovin/MAX','ThirdPartySDKs/Unity/LevelPlay','ThirdPartySDKs/Unity/Dependency-mediation-sdk',
 'ThirdPartySDKs/Unity/Ads','ThirdPartySDKs/AppLovin/Adapter-unityads-adapter','ThirdPartySDKs/AppLovin/Adapter-ironsource-adapter',
 'ThirdPartySDKs/AppLovin/Adapter-google-adapter','ThirdPartySDKs/Adjust/Android','ThirdPartySDKs/AppsFlyer/Android',
 'ThirdPartySDKs/Google/AppSet','ThirdPartySDKs/Google/AdsIdentifier']
prov_paths=[]
for root in selected:prov_paths+=sorted((R/root).glob('*/provenance.json'))
prov_paths += [R/n for n in ['cross-sdk/packages/services.analytics/6.3.0/provenance.json',
 'cross-sdk/packages/purchasing/5.4.0/provenance.json','cross-sdk/packages/purchasing/5.5.1/provenance.json',
 'identity-graph/sdk/authentication/3.9.0/provenance.json','cross-sdk/packages/singular/12.17.0/provenance.json']]
allfetch=[]
for p in sorted(D.glob('FETCH_*.json')):
    if p.name!='FETCH_MANIFEST.json':allfetch+=json.loads(p.read_text(encoding='utf-8'))
fetch={x['id']:x for x in allfetch}
save(D/'FETCH_MANIFEST.json',allfetch)

# Decode license documents only; do not download or inspect SDK implementation files.
decoded=[]
for key in ['al-android-license','al-ios-license','lp-unity-license','lp-android-license','google-adapter-license']:
    f=fetch[key]
    if f.get('status')!=200:continue
    x=json.loads((R/f['path']).read_text(encoding='utf-8'))
    b=base64.b64decode(x['content'])
    dest=D/'sources'/(key+'.decoded.txt')
    if dest.exists():assert dest.read_bytes()==b
    else:dest.write_bytes(b)
    decoded.append(dict(id=key,path=dest.relative_to(R).as_posix(),sha256=sha(dest),
      original_api=f['url'],html_url=x.get('html_url'),immutable_license_blob=x.get('git_url'),
      git_blob_sha=x.get('sha'),spdx=x.get('license',{}).get('spdx_id'),
      applies_to='Repository license snapshot;not automatic historical/bundled core permission'))
save(D/'DECODED_LICENSES.json',decoded)

def resolve(path,prov):
    path=Path(path)
    for p in [R/path,R/'ThirdPartySDKs'/path,prov.parent/path.name]:
        if p.is_file():return p
    raise FileNotFoundError(str(path))

entries=[];versions=[];license_extracts=[];provenance_hashes={};unavailable=[]
for prov in prov_paths:
    data=json.loads(prov.read_text(encoding='utf-8-sig'))
    rel=prov.relative_to(R).as_posix();provenance_hashes[rel]=sha(prov)
    version=data.get('version',prov.parent.name)
    sdk=(data.get('vendor','')+'/'+data.get('sdk',prov.parent.parent.name)).strip('/')
    pomlicenses=[]
    for pom in prov.parent.glob('*.pom'):
        ns={'m':'http://maven.apache.org/POM/4.0.0'}
        tree=ET.fromstring(pom.read_text(encoding='utf-8-sig'))
        pomlicenses.extend({e.tag.split('}')[-1]:e.text for e in lic} for lic in tree.findall('./m:licenses/m:license',ns))
        provenance_hashes[pom.relative_to(R).as_posix()]=sha(pom)
    package_licenses=list(prov.parent.glob('extracted/package/LICENSE.md'))
    for p in package_licenses:provenance_hashes[p.relative_to(R).as_posix()]=sha(p)
    artifacts=data.get('artifacts',[])
    if not artifacts:
        if data.get('url'):
            name=data['url'].rsplit('/',1)[-1]
            candidates=list(prov.parent.glob('*.tgz'))+list(prov.parent.glob('*.aar'))+list(prov.parent.glob('*.jar'))
            actual=next((p for p in candidates if p.name==name),candidates[0] if len(candidates)==1 else None)
            assert actual is not None,(rel,name)
            artifacts=[dict(path=actual.relative_to(R).as_posix(),url=data['url'],sha256=data.get('sha256'),http_last_modified=None)]
    version_record=dict(sdk=sdk,version=version,provenance=rel,provenance_sha256=sha(prov),
       declared_licenses=pomlicenses or data.get('licenses') or data.get('license'),
       package_license_files=[p.relative_to(R).as_posix() for p in package_licenses],
       registry_time=data.get('registry_time'),dependencies=data.get('dependencies',[]))
    versions.append(version_record)
    for artifact in artifacts:
        if artifact.get('status',200)!=200:
            unavailable.append(dict(provenance=rel,version=version,artifact=artifact,status='NOT_ACQUIRED_HTTP_FAILURE'))
            continue
        p=resolve(artifact['path'],prov)
        provenance_hashes[p.relative_to(R).as_posix()]=sha(p)
        if artifact.get('sha256'):assert sha(p)==artifact['sha256'],p
        if p.suffix not in ['.aar','.jar','.tgz','.unitypackage','.zip']:continue
        kind='sources.jar' if p.name.endswith('-sources.jar') else p.suffix[1:]
        is_adjust='ThirdPartySDKs/Adjust/Android/' in p.relative_to(R).as_posix()
        if is_adjust and kind=='sources.jar':gate='GO_SOURCE_REVIEW_ONLY_NEXT_PHASE'
        elif is_adjust:gate='LIMITED_MIT_SOURCE_PREFERRED_NO_BINARY_WORK_THIS_ROUND'
        elif any(t in p.relative_to(R).as_posix() for t in ['Unity/LevelPlay','Unity/Dependency-mediation-sdk','Unity/Ads','services.analytics','purchasing','authentication']):gate='STOP_SCOPE_OR_REVERSE_PERMISSION_UNRESOLVED'
        elif '/AppLovin/' in '/'+p.relative_to(R).as_posix():gate='UNKNOWN_EULA_SCOPE_NO_NEW_ANALYSIS'
        else:gate='UNKNOWN_LICENSE_SCOPE_NO_NEW_ANALYSIS'
        pub=data.get('registry_time') or 'UNKNOWN'
        lic=';'.join(str(x.get('name',''))+' '+str(x.get('url','')) for x in pomlicenses)
        if not lic:lic='Package LICENSE -> Unity Terms;scope review required' if package_licenses else 'UNKNOWN;see provenance'
        entries.append(dict(sample_id=f'OSM{len(entries)+1:03}',sdk=sdk,version=version,format=kind,
          path=p.relative_to(R).as_posix(),bytes=p.stat().st_size,sha256=sha(p),recorded_sha256=artifact.get('sha256') or data.get('sha256'),
          official_download_url=artifact.get('url') or data.get('url'),provenance=rel,provenance_sha256=sha(prov),
          publication_date=pub,publication_date_type='Official UPM registry timestamp' if data.get('registry_time') else 'UNKNOWN;HTTP Last-Modified is separate',
          http_last_modified=artifact.get('http_last_modified') or artifact.get('last_modified'),license_declaration=lic,
          permission_gate=gate,new_functional_analysis='NOT_STARTED',production_model_consumption='UNKNOWN',
          limitations='Public artifact and source.jar naming do not establish permission,complete implementation or production use'))
        # Read only license/notice entries. Do not read classes.dex,class files or implementation sources.
        if p.suffix in ['.aar','.jar'] and zipfile.is_zipfile(p):
            with zipfile.ZipFile(p) as z:
                for item in z.infolist():
                    name=Path(item.filename).name.lower()
                    if name not in ['license','license.txt','license.md','notice','notice.txt']:continue
                    if item.file_size>150_000:continue
                    b=z.read(item)
                    dest=D/'sources'/('embedded-'+hashlib.sha256((p.as_posix()+item.filename).encode()).hexdigest()[:14]+'.txt')
                    if dest.exists():assert dest.read_bytes()==b
                    else:dest.write_bytes(b)
                    license_extracts.append(dict(archive=p.relative_to(R).as_posix(),archive_sha256=sha(p),entry=item.filename,
                       path=dest.relative_to(R).as_posix(),sha256=sha(dest),scope='License/notice metadata only;not implementation analysis'))

table(D/'ACQUIRED_SAMPLE_CATALOG.csv',entries)
save(D/'VERSION_PROVENANCE.json',versions)
save(D/'REUSED_ARTIFACT_HASHES.json',provenance_hashes)
save(D/'EMBEDDED_LICENSES.json',license_extracts)
save(D/'UNAVAILABLE_ARTIFACTS.json',unavailable)
save(D/'SUMMARY_COUNTS.json',dict(acquired_artifacts=len(entries),versions=len(versions),
   permission_gates={g:sum(x['permission_gate']==g for x in entries) for g in sorted({x['permission_gate'] for x in entries})},
   formats={k:sum(x['format']==k for x in entries) for k in sorted({x['format'] for x in entries})},
   public_metadata_gets=len(allfetch),new_SDK_bundles_downloaded=0,new_functional_static_analyses=0,embedded_license_documents=len(license_extracts)))
print(json.dumps(json.loads((D/'SUMMARY_COUNTS.json').read_text(encoding='utf-8')),ensure_ascii=False))
