from pathlib import Path
import json,hashlib,datetime,csv,re
R=Path(__file__).resolve().parent.parent;D=R/'identity72-experiments73'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')
now=datetime.datetime.now(datetime.timezone.utc).isoformat();fetch=[]
for p in sorted(D.glob('FETCH_*.json')):
    if p.name!='FETCH_MANIFEST.json':fetch+=read(p)
save(D/'FETCH_MANIFEST.json',fetch)
matrix=read(R/'cross-sdk/SDK_MATRIX.json');audit=read(R/'identity-graph/SDK_IDENTITY_AUDIT.json')
code=[]
for i,x in enumerate(read(R/'identity-graph/IDENTITY_CODE_EXCERPTS.json'),1):
    p=R/x['path'];assert sha(p)==x['sha256'];ls=p.read_text(encoding='utf-8').splitlines()
    expected='\n'.join(f'{j+1}: {s}' for j,s in enumerate(ls) if x['start_line']<=j+1<=x['end_line']);assert expected==x['text'],x['id']
    tag=x['id'];sdk,version=('AppLovin/MAX','13.6.4') if tag.startswith('MAX-') else (('AppLovin/Axon','1.3.4') if tag.startswith('AXON-') else (('Unity/Ads','4.18.1' if '4.18.1' in x['path'] else '4.17.0') if tag.startswith('UNITY-') else ('Unity Authentication/Player Accounts','3.9.0 package')))
    jars=[dict(path=a['jar'],sha256=a['sha256']) for a in audit if ('max' in a['sdk'] and tag.startswith('MAX-')) or ('axon' in a['sdk'] and tag.startswith('AXON-'))]
    pkgs=[a for m in matrix if m['sdk']==sdk and m['version']==version for a in m.get('artifacts',[]) if a['path'].endswith('.aar')]
    for z in jars+pkgs:assert sha(R/z['path'])==z['sha256']
    code.append(dict(id=f'IG72C{i:02}',legacy_id=tag,path=x['path'],sha256=x['sha256'],start_line=x['start_line'],end_line=x['end_line'],excerpt=x['text'],sdk=sdk,version=version,class_or_method=tag,original_packages=pkgs,original_jars=jars,evidence_stages=['E1'] if tag in ['MAX-GAID','MAX-AppSet-start','MAX-AppSet-result','MAX-cuid-manager','AXON-appset-result','UNITY-ads-analytics-source','UNITY-ads-identity-repository','UNITY-ads-idfi-auid','UGS-identity-model','UPA-id-claims'] else ['E1','E2'] if tag not in ['MAX-user-normalization','AXON-user-normalization','UGS-PlayerId-token'] else ['E1'],proof_scope='Read/normalization/model or request-construction fragment;not actual upload/match/training',privacy_conditions='OS identifier scope,SDK flags,authenticated account/provider consent,project config and applicable privacy authorization;field-specific report adds limits',production_match_proven=False,prediction_model_consumption_proven=False,reviewed_utc=now))
save(D/'CODE_EVIDENCE.json',code)
for x in code:
    if x['legacy_id'] in ['MAX-structured-device','UPA-id-claims','UGS-token-scope','UGS-unity-id','UGS-network-endpoints','UGS-identity-model']:
        x['evidence_stages']=['E1']
        x['proof_scope']='Identity model/field declarations or endpoint definitions only;not standalone upload proof'
save(D/'CODE_EVIDENCE.json',code)
pixel=[]
for i,x in enumerate(read(R/'identity-graph/PIXEL_IDENTITY_EXCERPTS.json'),1):
    p=R/x['source'];assert sha(p)==x['source_sha256'];s=p.read_text(encoding='utf-8');a=x['character_offset'];assert s[a:a+len(x['original'])]==x['original'],x['id']
    pixel.append(dict(id=f'IG72P{i:02}',legacy_id=x['id'],path=x['source'],sha256=x['source_sha256'],offset_start=a,excerpt=x['original'],annotation=x.get('annotation'),version='public Pixel snapshot,version not asserted',evidence_stages=['E1','E2'] if x['id'] in ['payload','cookie-match'] else ['E1'],scope=x['limitation'],privacy_conditions='Merchant config and user consent;auto-email requires explicit flag;no script execution',production_match_proven=False,prediction_model_consumption_proven=False))
save(D/'PIXEL_EVIDENCE.json',pixel)
docspec=[
('IG72S01','identity-graph/google-appset-guide.raw','identity-graph/google-appset-guide.txt','https://developer.android.com/identity/app-set-id',['E3'],'Google App Set ID scope/reset and permitted usage;not global personal identity'),
('IG72S02','identity-graph/unity-upa-doc-md.raw','identity-graph/unity-upa-doc-md.txt','https://docs.unity.com/en-us/authentication/unity-player-accounts.md',['E3','E4'],'Explicit org-scoped account persistence across games/devices;not Vector consumption'),
('IG72S03','identity-graph/unity-identity-management.raw','identity-graph/unity-identity-management.txt','https://docs.unity.com/en-us/authentication/identity-management.md',['E3','E4'],'Link/unlink external identities,conflict constraints;not automatic unconsented merge'),
('IG72S04','identity-graph/liveramp-rampid-product.raw','identity-graph/liveramp-rampid-product.txt','https://liveramp.com/our-platform/rampid',['E3','E4'],'Commercial identity resolution/activation product;not measured Unity match rate'),
('IG72S05','vector/exchange-rampid.raw','vector/exchange-rampid.txt','https://unity.com/blog/unity-exchange-rampid-addressable-buying-mobile-gaming',['E3','E4'],'US/Canada Exchange RampID activation requires receiving partner support;not confirmed Vector input'),
('IG72S06','nongame/doc-capi.raw','nongame/doc-capi.txt','https://support.applovin.com/en/growth/promoting-your-websites/api/conversion-api',['E3'],'Merchant customer/click/contact/transaction inputs,not observed game cross-business join'),
('IG72S07','nongame/applovin-policy.raw','nongame/applovin-policy.txt','https://www.applovin.com/privacy/',['E3'],'Privacy scope is not a particular production identity mapping'),
('IG72S08','nongame/wurl-home.raw','nongame/wurl-home.txt','https://www.wurl.com/',['E3'],'CTV advertising/content business;not evidence of personal game training join')]
docs=[]
for sid,path,txt,url,stages,claim in docspec:
    p=R/path;t=R/txt
    if not p.exists():p=t
    ls=t.read_text(encoding='utf-8').splitlines()
    terms=['rampid','identity','cross','user_id','email','privacy','delete','cookie','identifier','address','consent','app set']
    indices=[i for i,s in enumerate(ls) if any(k in s.lower() for k in terms)];a=max(1,indices[0] if indices else 1);b=min(len(ls),a+90)
    docs.append(dict(id=sid,path=p.relative_to(R).as_posix(),sha256=sha(p),url=url,text_path=txt,text_sha256=sha(t),start_line=a,end_line=b,excerpt='\n'.join(f'{i+1}: {s}' for i,s in enumerate(ls) if a<=i+1<=b),claim=claim,evidence_stages=stages,source_date='2026-04-02' if sid=='IG72S05' else 'previous verified official snapshot;not new publication',reviewed_utc=now,privacy_conditions='Subject to provider contracts,scope,consent and local privacy controls',production_match_proven=False,prediction_model_consumption_proven=False))
for key,sid,stages in [('uid2-overview','IG72S09',['E3','E4']),('mixpanel-identify','IG72S10',['E3','E4']),('amplitude-identify','IG72S11',['E3','E4']),('branch-identity','IG72S12',['E3','E4']),('firebase-user-id','IG72S13',['E3','E4']),('criteo','EX73S01',[]),('bpid','EX73S02',[]),('bpid-amazon','EX73S03',[]),('talkingdata','EX73S04',[]),('talkingdata-rules','EX73S05',[])]:
    x=next(z for z in fetch if z['id']==key);assert x['status']==200
    ls=(R/x['text_path']).read_text(encoding='utf-8').splitlines();a=2264 if key=='branch-identity' else 1;b=min(len(ls),a+110)
    docs.append(dict(id=sid,path=x['path'],sha256=x['sha256'],url=x['url'],text_path=x['text_path'],text_sha256=x['text_sha256'],start_line=a,end_line=b,excerpt='\n'.join(f'{i+1}: {s}' for i,s in enumerate(ls) if a<=i+1<=b),claim={'talkingdata':'HTML shell only;no accepted competition rules/files','talkingdata-rules':'Rules shell only;not licence to train','bpid':'Official synthetic matching dataset Apache2.0 metadata','bpid-amazon':'Original publisher confirms synthetic profiles not real individuals','criteo':'Real sampled displayed impressions,30-day conversion label;noncommercial restricted;no training'}.get(key,'Explicit analytics/identity service contract;not proof of Axon/Vector integration'),evidence_stages=stages,source_date='2026-11-20 collection;page-specific dates retained in raw',privacy_conditions='Public docs;no API execution or real identity matching;dataset licence separately audited',production_match_proven=False,prediction_model_consumption_proven=False,acquired_utc=x['acquired_utc']))
save(D/'SOURCE_EVIDENCE.json',docs)
g=read(D/'EVIDENCE_GRAPH.before.json');ids=['XS01','XS06','XS11','XS18','XS19','XS20','XS34','XS39','XS41','C53S05','C53S12','C53S15','C53S16','C53S17','C53S18','C53S19','C53S24','C53S27','C53S52','CGS01','CGS02','CGS10','CGS26','CGS42','CGS49','CGS50','CGS51','MA60S17','L71D01','L71C01','L71C02','L71C15','L71C16','L71C18','L71C19','L72S05','L72S06','L72S07','L72S08']
reuse=[]
for sid in ids:
    x=next(z for z in g['sources'] if z['id']==sid);assert sha(R/x['path'])==x['sha256'];reuse.append(x)
save(D/'REUSED_EVIDENCE.json',reuse)
archives=[]
for p in sorted((R/'ThirdPartySDKs').rglob('*')):
    if p.is_file() and (p.suffix=='.aar' or p.name.endswith('sources.jar')):
        archives.append(dict(path=p.relative_to(R).as_posix(),bytes=p.stat().st_size,sha256=sha(p),type='AAR' if p.suffix=='.aar' else 'sources.jar',status='Reused unchanged;not claim every SDK fully reversed'))
save(D/'ARCHIVE_INVENTORY.json',archives)
save(D/'RUN_MANIFEST.json',dict(reviewed_utc=now,original_aar_count=sum(x['type']=='AAR' for x in archives),original_source_jar_count=sum(x['type']=='sources.jar' for x in archives),new_sdk_downloads=0,sdk_runtime_tests=0,production_requests=0,real_identity_collection=0,real_cross_dataset_joins=0,BPID_is_synthetic=True,TalkingData_training=False,Criteo_training=False))
cat=['# 72身份审计＋73实验：来源目录','',f'UTC:{now}。与此前72数据访问专题并存，全部历史报告保留。','', '## 静态调用链','', '| ID | 组件版本 | 原始位置 | 能证层级 |','|---|---|---|---|']
for x in code:cat.append(f"| {x['id']} / {x['legacy_id']} | {x['sdk']} {x['version']} | {x['path']}:{x['start_line']} | {','.join(x['evidence_stages'])}，生产匹配/入模未证 |")
cat+=['','## 官方契约与数据发布者','', '| ID | URL | SHA256 | 等级/边界 |','|---|---|---|---|']
for x in docs:cat.append(f"| {x['id']} | {x['url']} | `{x['sha256']}` | {','.join(x['evidence_stages']) or '数据准入证据，非平台身份等级'}；{x['claim']} |")
cat+=['','全部精确摘录和源文件哈希见CODE_EVIDENCE、PIXEL_EVIDENCE、SOURCE_EVIDENCE；原始AAR/JAR哈希见ARCHIVE_INVENTORY，原分析JAR哈希见代码对象。既有图对象复用见REUSED_EVIDENCE；不将E1/E2提升为E5/E6。','', 'BPID完整ZIP58,115,842字节，发布MD5及ZIP CRC核验见BPID_ARCHIVE_AUDIT。论文与原作者明确synthetic，只有匹配数据有人工标签；1M blocking记录无实体簇真值。本地未输出档案值，未关联外部身份。','', 'TalkingData只取得Kaggle网页壳，未登录、未接受竞赛规则，未下载镜像。Criteo CC BY-NC-SA4.0用途资格未确认，仅读字段/许可，未下载原始行、未训练。三份数据从不互相join。','', 'PREREGISTRATION在实验前保存；结果B/D是两种不同的合成实验，不是实际设备图谱、LTV或ROAS。所有结果文件和脚本哈希将在验证清单留存。']
(D/'SOURCE_CATALOG.md').write_text('\n'.join(cat)+'\n',encoding='utf-8')
print(json.dumps(dict(code=len(code),pixel=len(pixel),docs=len(docs),reused=len(reuse),aar=sum(x['type']=='AAR' for x in archives),sources=sum(x['type']=='sources.jar' for x in archives)),indent=2))
