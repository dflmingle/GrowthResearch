from pathlib import Path
import json,hashlib,datetime
R=Path(__file__).resolve().parent/'deep';ROOT=R.parents[1]
mf=ROOT/'EVIDENCE_MANIFEST.json';manifest=json.loads(mf.read_text(encoding='utf-8'));entries=[]
def rel(p):return str(p.relative_to(ROOT)).replace('\\','/')
def files(pat):return [rel(p) for p in R.glob(pat) if p.is_file()]
def add(id,title,refs,notes):
 out=[]
 for s in dict.fromkeys(refs):
  p=ROOT/s
  if not p.is_file():raise FileNotFoundError(p)
  out.append({'path':s,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
 entries.append({'id':id,'title':title,'notes':notes,'sources':out})
add('XD01','四包全DEX AppLovin事件/身份调用交叉引用',files('games/*/calls.json')+files('games/*/raw/**/*.txt')+['axon/deep_calls.py','axon/deep_summarize.py','axon/deep/game-scan-summary.json','axon/deep/event-callsite-catalog.json','axon/deep/event-callsite-catalog.csv','axon/deep/identity-callsite-catalog.json'],
 '15/8/14/12个DEX，所有命名空间；62条候选事件invoke含重载与SDK自动路径，不是62个业务事件。Car generic桥可见，其他三款未建立SDK外显式事件调用；native/反射/服务端另论。')
add('XD02','Car原生/Unity桥入口与trackEvent字面量归属',files('native-car/*')+files('native-car/native/*.asm')+files('bridges/car-race/**/*.java')+['axon/deep_native_car.py','axon/deep_bridges.py','car-race/reused-evidence/monetization-20261117/method-index.json'],
 'Car两个generic bridge存在但具体游戏触发未证；原生metadata trackEvent字面量可在AdjustAndroid.TrackEvent RVA0xDE7BF0定位，不作为MAX直发证据。ARM来自原包同哈希SO/metadata；未使用托管stub证明实现。')
add('XD03','四个匹配MAX版本事件协议与SDK自动调用方',files('versions/*/java/com/applovin/impl/sdk/EventServiceImpl.java')+files('versions/*/selected/com/applovin/impl/sdk/SessionTracker.java')+files('versions/*/selected/com/applovin/impl/sdk/AppLovinExceptionHandler.java')+files('versions/*/java/com/applovin/sdk/AppLovinSdk.java')+files('versions/*/selected/com/applovin/impl/*.java')+files('versions/*/constant-pool-refs.json')+files('versions/*/javap/*.txt')+['axon/deep/protocol-matrix.json','axon/deep/numbered-excerpts.json','axon/deep_versions.py','axon/jar_refs.py','axon/deep_selected.py'],
 '13.6.2/13.6.3/13.6.4有v1/app与相同默认42名表；13.2同类无。SDK自动landing默认旧路由。callsite与反编译受原始JVM/DEX佐证，不推断生产生效配置和初次发布日期。')
add('XD04','MAX持久postback队列到网络任务与回调',files('versions/*/java/com/applovin/impl/sdk/network/*.java')+files('versions/*/network/**/*.java')+files('games/*/sinks/**/*.txt')+files('games/*/sinks.json')+['axon/deep_network.py','axon/deep_sinks.py','axon/deep/network-candidates.json','axon/deep/network-decompilation.json'],
 'PersistentPostbackManager network.b、network.c磁盘pb队列、PostbackServiceImpl、TaskDispatchPostback/网络类及成功失败回调均保留；客户端postback不是MMP partner postback。没有成功发送运行观测。')
add('XD05','MAX用户ID管理器到cuid与请求/事件逻辑字段',files('versions/*/java/com/applovin/sdk/AppLovinSdkSettings.java')+files('versions/*/selected/com/applovin/impl/y6.java')+files('versions/*/selected/com/applovin/impl/p7.java')+files('versions/*/selected/com/applovin/impl/s7.java')+files('versions/*/selected/com/applovin/impl/t7.java')+files('versions/*/selected/com/applovin/impl/sdk/k.java')+files('versions/*/selected/com/applovin/impl/sdk/m.java')+files('versions/*/final/com/applovin/impl/n4.java')+files('versions/*/final/com/applovin/impl/b5.java')+files('versions/*/final/com/applovin/impl/e5.java')+['axon/deep/type-resolution.json'],
 'setUserIdentifier预attach缓存/attach转交；pui默认持久化com.applovin.sdk.user_id，qq3默认传cuid；旧事件扁平map、新事件/广告请求app_info。逻辑字段不等于已观察线上字节。')
add('XD06','三款实际用户ID上游与Meow AF/MAX同源补证',files('bridges/meowdoku/**/*.java')+files('metica-car/**/*.java')+['axon/deep/metica-car-index.json','axon/deep/bridge-decompilation.json','axon/deep_metica.py','ThirdPartySDKs/BUSINESS_TRACES.json']+[rel(p) for p in (ROOT/'ThirdPartySDKs/Embedded/meowdoku/business-trace').rglob('*') if p.is_file() and ('AdInitParameter' in p.name or 'AdUuid___' in p.name)]+['ThirdPartySDKs/Embedded/rotate-rings/bridge-java/classes3.dex/w6/e.java','car-race/reused-evidence/monetization-20261117/native/Zego.Advertisement.Metica__Zego.Advertisement.Metica.AdMeticaDefault.get_NextUserId-32d967c.asm','car-race/reused-evidence/monetization-20261117/native/Zego.Advertisement.Metica__Zego.Advertisement.Metica.AdMeticaDefault.Init-32da628.asm'],
 'Meow builder从AnalyzeManager UUID设AdUuid，与既有AF CUID同源；Rotate distinctId→MAX；Car本地GUID/测试覆盖→initConfig→Metica preservedID→MAX。静态条件链，不读取实际ID，不推跨应用。')
add('XD07','配置更新、13.6.4独立user_data与字段条件',files('versions/*/final/**/*.java')+files('versions/13.6.4/java/com/applovin/impl/sdk/l.java')+files('versions/13.6.4/java/com/applovin/sdk/AppLovinUserData.java')+['ThirdPartySDKs/AppLovin/MAX/13.6.4/focused/com/applovin/impl/r7.java','axon/deep_finish_code.py'],
 'SettingsManager按注册key读取JSON/缓存生效值；默认不等于生产。user_data独立对象，send_user_data默认true但需非空有效输入；setUserIdentifier不创建该对象；13.6.4广告请求也可消费。')
pub=['axon/deep/public-probe.json','axon/deep_public_probe.py']
for key in ['deep-official-blog-search','deep-yahoo-meow','deep-yahoo-rotate','deep-yahoo-car','deep-yahoo-jewel']:
 pub += ['axon/'+key+ext for ext in ['.html','.txt','-links.json'] if (ROOT/('axon/'+key+ext)).exists()]
add('XD08','新增公开投放记录调查与静态证据校验',pub+['axon/deep/VALIDATION.json','axon/deep_validate.py'],
 '官方博客搜索仅壳；Yahoo准确目标查询500；仍未取得产品×AppLovin付费投放记录。VALIDATION核对原始DEX协议字段、原始SO/metadata与archive一致，不证明生产送达。')
ids={x['id'] for x in entries};manifest['entries']=[x for x in manifest['entries'] if x['id'] not in ids]+entries;manifest['axon_deep_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();mf.write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
p=ROOT/'EVIDENCE_INDEX.md';s=p.read_text(encoding='utf-8');mark='<!-- AXON_DEEP_20261118 -->';s=s.split(mark)[0].rstrip()+'\n\n'+mark+'\n\n## Axon事件与用户ID深度专项\n\n新增20/21/22；SDK自动直发、游戏显式业务、默认事件表和网络成功分别判断。MMP partner回传独立。本轮新证据补齐Meow AdUuid来源、Car本地GUID链及13.6.2/13.6.3协议，未取得生产事件接收或实际投放记录。\n\n'
for e in entries:
 s+=f'<a id="{e["id"].lower()}"></a>\n## {e["id"]} · {e["title"]}\n\n{e["notes"]}\n\n'
 refs=e['sources'];chosen=[x for x in refs if x['path'].endswith('.json')][:8]+[x for x in refs if x['path'].endswith('.java')][:4]
 if not chosen:chosen=refs[:8]
 for x in dict((x['path'],x) for x in chosen).values():s+=f'- [{x["path"]}]({x["path"]})\n'
 s+=f'\n完整原始位置与SHA256见EVIDENCE_MANIFEST.json的{e["id"]}（{len(refs)}份材料）。\n\n'
p.write_text(s,encoding='utf-8');print('new groups',len(entries),'hashed sources',sum(len(x['sources']) for x in entries))
