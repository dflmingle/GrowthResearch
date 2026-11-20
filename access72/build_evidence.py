from pathlib import Path
import json,hashlib,datetime
R=Path(__file__).resolve().parent.parent;D=R/'access72'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')
now=datetime.datetime.now(datetime.timezone.utc).isoformat();fetch=[]
for p in sorted(D.glob('FETCH_*.json')):
    if p.name!='FETCH_MANIFEST.json':fetch+=read(p)
save(D/'FETCH_MANIFEST.json',fetch)
specs=[
('L72S01','af-revenue-roi360',5,62,'2026-11-19 09:45 as displayed,timezone unspecified','Integration granularity,SDK freshness/device accuracy and hybrid replacement;not per-impression exactly-once'),
('L72S02','af-revenue-roi360',171,215,'2026-11-19 09:45 as displayed,timezone unspecified','Cross-reference dedup checkbox scope/exceptions;aggregate eRPA is allocated value,not observed individual impression income'),
('L72S03','af-revenue-roi360',419,460,'2026-11-19 09:45 as displayed,timezone unspecified','Impression input can become device-level export;conversion context copied into attributed revenue reports;not physical training columns'),
('L72S04','af-revenue-roi360',573,681,'2026-11-19 09:45 as displayed,timezone unspecified','Integration start boundary,report freshness and revisions;raw export/Pull API not revised like dashboards/Data Locker'),
('L72S05','af-share-revenue',1,78,'2026-09-15 11:11 as displayed,timezone unspecified','Daily UA signals vs realtime SDK postbacks;ROI360 Advanced and partner permissions;other-source attribution redacted'),
('L72S06','af-share-revenue',93,189,'2026-09-15 11:11 as displayed,timezone unspecified','af_ad_revenue explicitly mapped to Unity ad_revenue;select-all excludes it;mediation source list not receiver list'),
('L72S07','af-share-revenue',191,457,'2026-09-15 11:11 as displayed,timezone unspecified','Receiver table lists Unity Ads for both channels;AppLovin/Axon absent from this table snapshot,not proof universally unsupported'),
('L72S08','af-raw-dictionary',743,769,'2026-11-18 13:51 as displayed,timezone unspecified','AppsFlyer install-scoped attribution identity semantics;not person-level cross-game identity'),
('L72S09','af-raw-dictionary',1413,1458,'2026-11-18 13:51 as displayed,timezone unspecified','Event time depends on source/report;device/original time is not information available_at'),
('L72S10','af-ltv-activity',23,49,'2025-12-18 00:01 as displayed,timezone unspecified','Install-cohort LTV vs event-date activity;raw activity is not mature D28 cohort by itself'),
('L72S11','adjust-sdk-revenue',39,67,'not stated;2026-11-20 snapshot','SDK/API overlap and account-level API pulls;Ad Revenue Sources filter applies to reporting,partner sharing and conversion mapping;not economic ID dedup guarantee')]
docs=[]
for sid,key,a,b,date,claim in specs:
    f=next(x for x in fetch if x['id']==key);assert f['status']==200
    p=R/f['text_path'];ss=p.read_text(encoding='utf-8').splitlines();assert b<=len(ss),(sid,b,len(ss))
    docs.append(dict(id=sid,url=f['url'],final_url=f['final_url'],path=f['path'],sha256=f['sha256'],text_path=f['text_path'],text_sha256=f['text_sha256'],start_line=a,end_line=b,excerpt='\n'.join(f'{i+1}: {s}' for i,s in enumerate(ss) if a<=i+1<=b),claim=claim,source_date=date,acquired_utc=f['acquired_utc'],evidence_level='官方公开契约',authorization_scope='Public document read/citation;not transaction-data licence or account access',production_received_observed=False,physical_training_consumption_proven=False))
f=next(x for x in fetch if x['id']=='yokozuna-public-bundle');excerpt=read(D/'YOKOZUNA_CONTACT_EXCERPT.json')
assert (R/f['path']).read_text(encoding='utf-8')[excerpt['offset_start']:excerpt['offset_end']]==excerpt['excerpt']
docs.append(dict(id='L72S12',url=f['url'],path=f['path'],sha256=f['sha256'],acquired_utc=f['acquired_utc'],source_date='not stated;2026-11-20 snapshot',offset_start=excerpt['offset_start'],offset_end=excerpt['offset_end'],excerpt=excerpt['excerpt'],claim='Public contact component names info@yokozunadata.com;paper authors affiliated to same company;not confirmed current Age-of-Ishtaria custodian or licence channel',evidence_level='官方公开联系入口',authorization_scope='Public marketing component only;no sign-in,data or private API requested',production_received_observed=False,physical_training_consumption_proven=False))
save(D/'SOURCE_EVIDENCE.json',docs)
g=read(D/'EVIDENCE_GRAPH.before.json')
ids=['CL70S01','CL70S02','CL70S04','CL70S05','GI69S_uken_participant','GI69S_uken_code','GI69S_unity_paper','GI69S_unity_code','GI69S_unity_osf','GI69S_ageishtaria','CGS42','CGS49','CGS50','CGS51','MA60S17','L71C01','L71C02','L71C07','L71C08','L71C09','L71C10','L71C11','L71C12','L71C13','L71C15','L71C16','L71C18','L71C19','L71C21','L71D01','L71S01','L71S02','L71S03','L71S07','L71S08']
reuse=[]
for sid in ids:
    x=next(x for x in g['sources'] if x['id']==sid);assert sha(R/x['path'])==x['sha256'],sid;reuse.append(x)
save(D/'REUSED_EVIDENCE.json',reuse)
routes=[dict(id='U72_UKEN',contact='support@uken.com',source_ids=['CL70S04','CL70S05'],role='Current company routing only',custodian_2015_confirmed=False,data_access_permitted=False,sent=False),dict(id='U72_SFU',contact='statmgr@sfu.ca',source_ids=['CL70S01','CL70S02'],role='Current department archive/custodian routing only',custodian_2015_confirmed=False,data_access_permitted=False,sent=False),dict(id='U72_AGE',contact='info@yokozunadata.com',source_ids=['L72S12','GI69S_ageishtaria'],role='Newly verified public company contact;historical research affiliation,not proved rights-holder',custodian_2015_confirmed=False,data_access_permitted=False,sent=False),dict(id='U72_UNITY',contact='No verified open application channel for the original dataset',source_ids=['GI69S_unity_paper'],role='Original paper explicitly says authors cannot share or facilitate access',custodian_2015_confirmed=False,data_access_permitted=False,sent=False)]
save(D/'ACCESS_ROUTES.json',routes)
cat=['# 72号一手材料与搜索边界','',f'核验UTC：{now}。没有扫描SDK；仅读取官网公开文档和主页引用的公开JS联系组件。','', '| ID | 原始URL | 时间 | 原始位置 | SHA256 | 支持及限制 |','|---|---|---|---|---|---|']
for x in docs:
    loc=(x.get('text_path','')+':'+str(x.get('start_line',''))) if 'start_line' in x else x['path']+'@'+str(x['offset_start'])
    cat.append(f"| {x['id']} | {x['url']} | {x['source_date']} | {loc} | `{x['sha256']}` | {x['claim']} |")
cat+=['','同一原件的多个片段不算多项独立突破。SOURCE_EVIDENCE.json保存精确摘录和文本哈希；REUSED_EVIDENCE.json仅复用已核验对象。所有取得材料均为公开契约/模式说明，**不是运营方授权的实收日志、后台导出或模型训练表**。','', '搜索边界：Uken沿71号官方路由与未发送申请包；Age仅原论文、现行公司公开联系组件；Unity原论文/OSF明确不共享，未重复下载补充文件。原raw-data-export文档路径404不作有效接口证据，未继续猜测路径。','', 'MMP仅官方收入集成、共享渠道、去重适用范围、时间与cohort字典。没有访问报表、Data Locker、生产归因/竞价端点或广告账户。官方示例报表链接不等于许可明确的真实游戏数据，本轮未下载示例行。','', 'public bundle中的contact组件只用于核验业务邮箱；未执行其中应用代码、登录或访问数据路由。随机字符串中的NDA匹配不是协议证据，已排除。SFU/Uken当前职能与历史论文机构不能证明2015现行数据保管权。']
(D/'SOURCE_CATALOG.md').write_text('\n'.join(cat)+'\n',encoding='utf-8')
print(json.dumps(dict(new_records=len(docs),reused=len(reuse),fetches=len(fetch),emails_sent=0,new_datasets=0),indent=2))
