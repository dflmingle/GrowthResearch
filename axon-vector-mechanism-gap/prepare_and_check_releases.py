"""Bounded official release-note check, no SDK, auth or production endpoints."""
from pathlib import Path
import hashlib,json,datetime,re,urllib.request,urllib.error,urllib.parse

ROOT=Path(__file__).resolve().parent
PARENT=ROOT.parent
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def save(p,obj):
    p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

SOURCES=[
 'EVIDENCE_INDEX.md','EVIDENCE_MANIFEST.json',
 '72_AppLovin身份图谱逆向.md','72_Unity身份图谱逆向.md',
 '74_身份图谱生产证据.md','74_身份特征进入价值模型的证据.md','74_研究边界与停止条件.md',
 '71_Axon训练数据字段证据.md','71_Vector训练数据字段证据.md',
 '77_生产身份图谱工程证据矩阵.csv','77_最终判断与停止条件.md',
 '78_身份图谱最小生产证据契约.md','78_证据验收与升级规则.md',
 'official-samples-audit/ACQUIRED_SAMPLE_CATALOG.csv','official-samples-audit/SOURCE_CATALOG.md',
 'official-samples-audit/下一轮授权与测试条件.md',
 'adjust-mechanisms/已证实机制与服务端未知清单.md','adjust-mechanisms/三版本源码差分.md',
 'adjust-mechanisms/CODE_EVIDENCE.json','adjust-mechanisms/SAMPLES.json',
 'server-identity-reference/AXON_VECTOR_GAP_MATRIX.csv',
 'server-identity-reference/REFERENCE_CONTRACTS.json','server-identity-reference/SOURCE_CATALOG.md',
 'identity-graph-mvp/ARCHITECTURE.md','identity-graph-mvp/FAILURES_AND_RISKS.md',
 'identity-graph-mvp/identity_mvp/system.py','identity-graph-mvp/identity_mvp/schema.sql',
 'identity-graph-ltv-lab/lab/adapter.py','identity-graph-ltv-lab/lab/counterexamples.py',
 'identity-graph-ltv-lab/EXPERIMENT_SUMMARY.md',
 'identity72-experiments73/SOURCE_CATALOG.md','identity-value74/SOURCE_CATALOG.md',
 'lineage71/SOURCE_CATALOG.md','model-architecture/SOURCE_CATALOG.md'
]

def main():
    freeze=ROOT/'PRESERVATION_BASELINE.json'
    if (ROOT/'FETCH_MANIFEST.json').exists():raise SystemExit('Refusing to re-request existing release checks')
    if freeze.exists():baseline=load(freeze)
    else:
        baseline=load(PARENT/'two-app-partner-readiness/internal/PRESERVATION_BASELINE.json')
        for name in ['two-app-partner-readiness','identity-graph-real-data-audit','official-samples-audit','adjust-mechanisms',
                     'server-identity-reference','identity-graph-mvp','identity-graph-ltv-lab']:
            for p in (PARENT/name).rglob('*'):
                if p.is_file():baseline.setdefault(p.relative_to(PARENT).as_posix(),sha(p))
    changed=[p for p,h in baseline.items() if not (PARENT/p).is_file() or sha(PARENT/p)!=h]
    if changed:raise SystemExit('Historical mismatch '+str(changed))
    if not freeze.exists():save(freeze,baseline)
    save(ROOT/'REUSED_SOURCES.json',[dict(id=f'REUSE{i:02d}',path=name,sha256=sha(PARENT/name),new_vendor_evidence=False)
        for i,name in enumerate(SOURCES,1)])
    # The existing research index is text-only; never search user rows or APKs.
    catalogs=[]
    for p in PARENT.rglob('SOURCE_CATALOG.md'):
        if ROOT not in p.parents:catalogs.append(p)
    for directory in ['official-samples-audit','identity72-experiments73','model-architecture','production77']:
        for pattern in ['*FETCH*MANIFEST*.json','*SOURCE*EVIDENCE*.json']:
            catalogs.extend((PARENT/directory).glob(pattern))
    existing='\n'.join(p.read_text(encoding='utf-8-sig',errors='replace') for p in catalogs)
    targets=[
      ('NEW01','AppLovin/AppLovin-MAX-Unity-Plugin','https://api.github.com/repos/AppLovin/AppLovin-MAX-Unity-Plugin/releases?per_page=5'),
      ('NEW02','ironsource-mobile/Unity-sdk','https://api.github.com/repos/ironsource-mobile/Unity-sdk/releases?per_page=5')
    ]
    manifest=[];notes=[]
    for id,repo,url in targets:
        entry=dict(id=id,repo=repo,url=url,purpose='PUBLIC_RELEASE_NOTES_ONLY',sdk_download=False,
          collected_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),publication_date='PER_RELEASE_METADATA',
          license_scope='Read public metadata; no license inferred for SDK or implementation',production_evidence=False)
        if url in existing:
            entry.update(status='SKIP_EXACT_PRIOR_SOURCE',http_status=None);manifest.append(entry);continue
        try:
            request=urllib.request.Request(url,headers={'User-Agent':'GrowthResearch-public-metadata-audit','Accept':'application/vnd.github+json'})
            with urllib.request.urlopen(request,timeout=25) as response:
                if urllib.parse.urlparse(response.geturl()).hostname!='api.github.com':raise RuntimeError('Unexpected redirect host')
                body=response.read(1500001)
                if len(body)>1500000:raise RuntimeError('Metadata exceeds bounded response budget')
                entry.update(status='FETCHED_METADATA_ONLY',http_status=response.status,final_url=response.geturl())
            path=ROOT/'sources'/f'{id}-releases.json';path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(body)
            entry.update(raw_path=path.relative_to(ROOT).as_posix(),sha256=sha(path),bytes=len(body))
            payload=json.loads(body)
            if not isinstance(payload,list):raise RuntimeError('Release list expected')
            for release in payload:
                text=release.get('body') or '';tag=release.get('tag_name')
                hits=[line for line in text.splitlines() if re.search(r'identity|user.?id|consent|privacy|token|revenue|impression|reset|expir|session|custom.?data|cohort',line,re.I)]
                notes.append(dict(source_id=id,repo=repo,tag=tag,published_at=release.get('published_at'),html_url=release.get('html_url'),
                    release_note_text=text,mechanism_lines=hits,tag_previously_mentioned=(str(tag) in existing if tag else False),
                    novelty='UNASSESSED_NOT_A_BREAKTHROUGH',scope='SDK_WRAPPER_RELEASE_NOT_AXON_OR_VECTOR_MODEL'))
        except urllib.error.HTTPError as exc:
            body=exc.read(100000);path=ROOT/'sources'/f'{id}-http-{exc.code}.txt';path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(body)
            entry.update(status='HTTP_ERROR_NO_RETRY_NO_BYPASS',http_status=exc.code,raw_path=path.relative_to(ROOT).as_posix(),sha256=sha(path))
        except Exception as exc:entry.update(status='FAILED_NO_RETRY',error=repr(exc))
        manifest.append(entry)
    save(ROOT/'FETCH_MANIFEST.json',manifest);save(ROOT/'RELEASE_NOTES_REVIEW.json',notes)
    save(ROOT/'SCOPE.json',dict(protected_files=len(baseline),reused_sources=len(SOURCES),official_metadata_targets=2,
      official_requests=sum(e['status']!='SKIP_EXACT_PRIOR_SOURCE' for e in manifest),sdk_scans=0,sdk_runs=0,
      production_requests=0,identity_lookups=0,real_data_access=0,simulations_run=0,
      questionnaires_created=0,external_contacts=0,C_graph_Axon='UNKNOWN',C_graph_Vector='UNKNOWN',D='UNKNOWN',production_forensics='STOP'))
    print(json.dumps(dict(protected=len(baseline),statuses=[(x['id'],x['status']) for x in manifest],releases=len(notes))))
    for r in notes:print(json.dumps({k:r[k] for k in ['source_id','tag','published_at','mechanism_lines']},ensure_ascii=False))

if __name__=='__main__':main()
