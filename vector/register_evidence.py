"""Append this study's evidence; preserve all existing evidence IDs and hashes."""
from pathlib import Path
import json,hashlib,datetime
R=Path(__file__).resolve().parent
ROOT=R.parent
public=json.loads((R/'PUBLIC_SOURCE_INDEX.json').read_text(encoding='utf-8'))
code=json.loads((R/'CODE_EVIDENCE.json').read_text(encoding='utf-8'))
groups=[
 ('VG01','Unity 2025—2026 已实现季度财报与分类口径','官方公开证实；不把 Strategic Grow 或公司收入当 Vector/广告主 ROAS。', ['unity-ir-2025-q1','unity-ir-2025-q2','unity-ir-2025-q3','unity-q4-2025-final','unity-ir-2026-q1','unity-ir-2026-q2','unity-ir-2026-q3'],['vector/FINANCIAL_COMPARISON.csv']),
 ('VG02','AppLovin 同期广告/持续经营收入','官方公开证实；排除 2025Q1 Apps 收入，保留后续终止经营重列背景。',['app-ir-2025-q1','app-ir-2025-q2','app-ir-2025-q3','app-ir-2025-q4','app-ir-2026-q1','app-ir-2026-q2','app-ir-2026-q3'],[]),
 ('VG03','Vector 产品、D28 发布和学习门槛','官方公开证实；beta、内部测试与厂商案例有限定，未证明战胜 Axon。',['unity-vector-correct','d28-blog','d7-d28-iap','doc-intro-to-roas-campaigns','doc-roas-campaign-best-practices','vector-link-unico-studio','vector-link-zephyrmobile','vector-link-voodoo','unity-2026-keynote'],[]),
 ('VG04','Unity 与 MMP 事件/广告收入共享及独立 S2S 协议','官方公开证实；partner/Game ID/授权和映射不等于目标游戏启用；没有访问事件端点。',['doc-integrate-adjust-with-unity','doc-integrate-appsflyer-with-unity','unity-ads-partner','af-unity-partner','doc-send-postbacks','doc-postback-request'],[]),
 ('VG05','Unity Ads 4.17/4.18.1 与 LevelPlay 9.3/9.4/9.5 选定代码','SDK代码证实；请求/竞价/广告事件/队列/隐私与ILRD，不声称恢复 Vector 服务端。',[],['vector/SDK_AUDIT.json','vector/CODE_EVIDENCE.json']+[c['path'] for c in code if not c.get('error') and not c['id'].startswith('runtime_')]),
 ('VG06','Developer Data Runtime 框架、官方 6000.3 Consent 参考绑定','官方公开证实、SDK代码证实；收集/用途/consent 分离；不能证明四款 Runtime 到 Vector 生产链。',['ddf-doc-md','ddf-data-collection-settings','ddf-data-usage-settings','ddf-end-user-consent','ddf-your-data-in-action','ddf-what-is-developer-data','ddf-how-the-framework-works','ddf-getting-started','ddf-external-data-integration','developer-data-terms','developer-data-legacy','doc-configure-diagnostics-editor','unity-runtime-cs-release','unity-runtime-cs-release-state','unity-ddf-consent-api','unity-runtime-blog-keynote'],[]),
 ('VG07','Unity Exchange 公开竞价与美加 RampID 接入','官方公开证实；商业身份互通能力，不证明四款或 Vector 使用，更不证明全部库存被 Vector 购买。',['doc-get-started','exchange-rampid','exchange-tools'],[]),
 ('VG08','可复算的 IAA ROAS 离线模型与校验','合成经济场景及计算校验；不是实测投放或任一平台精度。',[],['vector/model/inputs.json','vector/model/roas_model.py','vector/model/verify_model.py','vector/model/plot_model.py','vector/model/MODEL_VALIDATION.json']+[p.relative_to(ROOT).as_posix() for p in sorted((R/'model/output').iterdir()) if p.is_file()]),
]
manifest_path=ROOT/'EVIDENCE_MANIFEST.json'
manifest=json.loads(manifest_path.read_text(encoding='utf-8'))
assert not any(e['id'].startswith('VG') for e in manifest['entries']), 'Already registered; do not overwrite'
sections=['\n<!-- VECTOR_AXON_STUDY_2026_11_18 -->\n']
for eid,title,notes,ids,rels in groups:
 sources=[]
 for sid in ids:
  row=public[sid]
  for suffix in ['.html','.txt']:
   p=R/(sid+suffix)
   if p.exists():
    sources.append({'path':p.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'url':row['url'],'final_url':row.get('final_url'),'fetched_utc':row['utc'],'http_status':row['status'],'kind':'raw public response' if suffix=='.html' else 'derived text'})
 for rel in dict.fromkeys(rels):
  p=ROOT/rel;assert p.is_file(),rel
  sources.append({'path':rel,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
 if eid=='VG05':
  for rel in ['Unity/Ads/4.17.0','Unity/Ads/4.18.1','Unity/LevelPlay/9.3.0','Unity/Dependency-mediation-sdk/9.4.0','Unity/LevelPlay/9.5.0']:
   for name in ['classes.jar','provenance.json']:
    p=ROOT/'ThirdPartySDKs'/rel/name
    assert p.is_file(),p
    sources.append({'path':p.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
 manifest['entries'].append({'id':eid,'title':title,'notes':notes,'sources':sources})
 sections+=['<a id="'+eid.lower()+'"></a>\n','## '+eid+' · '+title+'\n',notes+'\n']
 for sid in ids:
  row=public[sid];sections.append('- ['+sid+' 公开原文]('+row['url']+')；[本地原始响应](vector/'+sid+'.html)')
 for rel in dict.fromkeys(rels):sections.append('- ['+rel+']('+rel+')')
 sections.append('\n完整来源、抓取时间和 SHA256 见 EVIDENCE_MANIFEST.json 的 '+eid+'。\n')
manifest['utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
with (ROOT/'EVIDENCE_INDEX.md').open('a',encoding='utf-8') as f:f.write('\n'.join(sections)+'\n')
print('appended',len(groups),'groups;',sum(len(e['sources']) for e in manifest['entries'] if e['id'].startswith('VG')),'new source hashes')
