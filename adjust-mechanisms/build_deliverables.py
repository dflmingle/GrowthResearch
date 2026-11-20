"""Generate bounded Adjust source-review artifacts. No SDK execution or network.
Uses manually selected call chains and line locators, not whole-program analysis.
"""
from pathlib import Path
import csv, hashlib, json, re
from datetime import datetime, timezone
import analyze_sources as locator

R = Path(__file__).resolve().parent.parent
D = Path(__file__).resolve().parent
VERSIONS = ['5.5.0', '5.7.0', '5.8.1']
FILES = json.loads((D/'EXTRACTED_FILES.json').read_text(encoding='utf-8'))
SAMPLES = json.loads((D/'SAMPLES.json').read_text(encoding='utf-8'))
SYMBOLS = json.loads((D/'SYMBOL_INDEX.json').read_text(encoding='utf-8'))
NOW = datetime.now(timezone.utc).isoformat()
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p, value): p.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
def write(name, value): (D/name).write_text(value.strip()+'\n', encoding='utf-8')
def csvout(name, rows):
    with (D/name).open('w', encoding='utf-8-sig', newline='') as f:
        w=csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

refs=[]; ref_keys={}
def ref(version, file, method):
    if version != '5.8.1' and file == 'DeviceInfo.java' and method == 'readAndroidId':
        method = 'reloadNonPlayIds'
    key=(version,file,method)
    if key in ref_keys: return ref_keys[key]
    entry='com/adjust/sdk/'+file
    filedata=next(x for x in FILES if x['version']==version and x['entry']==entry)
    text=(R/filedata['path']).read_text(encoding='utf-8-sig')
    found=[x for x in SYMBOLS if x['version']==version and x['entry']==entry and x['method']==method]
    if method == '<field_declarations>':
        spans=[(1,min(128,len(text.splitlines())))]; kind='Explicit declaration range; field evidence, not a method'
    elif found:
        # Overloads are all included: a call path must not depend on which overload the regex found first.
        spans=[(x['start_line'],x['end_line']) for x in found]
        kind='Lexical locator; reviewed call-chain; not AST/whole-program proof'
    else:
        clean=locator.mask(text)
        pattern=r'(?m)^    (?:public|protected|private) [^\n;={}]*?\b'+re.escape(method)+r'\s*\([^;{}]*?\)\s*(?:throws\s+[^;{}]+)?\s*\{'
        m=re.search(pattern,clean)
        if not m: raise ValueError(('Missing method',key))
        op=clean.index('{',m.start(),m.end()); end=op+1; depth=1
        while depth:
            depth+=(clean[end]=='{')-(clean[end]=='}'); end+=1
        spans=[(text[:m.start()].count('\n')+1,text[:end].count('\n')+1)]
        kind='Supplemental generic-return declaration locator; reviewed range; not AST'
    lines=text.splitlines()
    rid=f'AMS{len(refs)+1:04d}'
    excerpts=[dict(start_line=a,end_line=b,text='\n'.join(lines[a-1:b])) for a,b in spans]
    rec=dict(id=rid,**filedata,class_name=entry.removesuffix('.java').replace('/','.'),method=method,
             spans=excerpts,locator=kind,level='CLIENT_STATIC_ONLY',SDK_executed=False,
             server_received_proven=False,production_model_consumption_proven=False)
    refs.append(rec);ref_keys[key]=rid
    return rid

findings=[]
def add(fid,title,proven,inp,process,out,chain,unknown,design,methods,versions=VERSIONS):
    evidence={}
    for v in versions:
        selected=methods(v) if callable(methods) else methods
        evidence[v]=[ref(v,f,m) for f,m in selected]
    findings.append(dict(id=fid,title=title,proven_client_mechanism=proven,input=inp,processing=process,output=out,
       call_chain=chain,server_unknown=unknown,reference_design=design,evidence_by_version=evidence,
       evidence_level='客户端静态代码；未运行SDK、未证明实际发送/接收/入模'))

add('AM01','本地UUID属于应用私有SDK状态',
 'ActivityState构造时生成随机UUID；读取/写入应用私有文件，反序列化缺失UUID时补建。不是每次会话重新生成。',
 'Context、已存ActivityState或缺失状态','读取状态；新建时Util.createUuid；MODE_PRIVATE持久化','activityState.uuid；请求键android_uuid',
 'readActivityStateI → Util.readObject → ActivityState/readObject；writeActivityStateI → Util.writeObject',
 '卸载/备份恢复的OS效果、服务端安装身份和旧新UUID合并/解绑均未证实。',
 '独立命名installation_instance；租户/应用命名空间；数据清除建立新epoch，不能称自然人ID。',
 [('ActivityState.java','ActivityState'),('ActivityState.java','readObject'),('Util.java','createUuid'),('Util.java','readObject'),('Util.java','writeObject'),('ActivityHandler.java','readActivityStateI'),('ActivityHandler.java','writeActivityStateI')])
add('AM02','Google广告ID读取及重读并非身份图谱',
 '默认非read-once；重读链根据版本执行儿童/配置门控、服务读取和反射后备；5.8.1读取前清空相关字段。未见该链比较旧新GAID并同步轮换UUID、adid及队列。',
 'AdjustConfig、OS广告服务可返回的值','reloadPlayIds(旧)/reloadGoogleAdId(新)；有限重试/反射读取','gps_adid、tracking_enabled、读取来源/尝试次数或空值',
 'getEventParameters/getSessionParameters → DeviceInfo.reload* → 服务/Reflection',
 'OS重置后服务端是否重连旧身份、忘记历史或实际跨App使用UNKNOWN；不能依赖客户端字段清空推断服务器删除。',
 '外部标识用可撤销时间区间和namespace存储；不以重置ID恢复追踪。',
 lambda v:[('DeviceInfo.java','reloadGoogleAdId' if v=='5.8.1' else 'reloadPlayIds'),('AdjustConfig.java','AdjustConfig'),('AdjustConfig.java','enableDeviceIdsReadingOnce'),('PackageBuilder.java','getEventParameters')])
add('AM03','Android ID是条件回退且作用域由OS决定',
 'AndroidIdUtil调用Settings.Secure.ANDROID_ID；事件构造在未加入Google/Fire广告ID时走AndroidID回退；不是无条件同时读取所有ID。',
 'OS Secure设置、配置/儿童门控','readAndroidId缓存；PackageBuilder检查已加入的广告ID键','条件性的android_id',
 'getEventParameters → contains* → DeviceInfo.readAndroidId → AndroidIdUtil.getAndroidId',
 '客户端不能决定该系统标识跨签名/用户/版本的作用域；不证明跨App或跨设备匹配成功。',
 '注册OS/签名/用户作用域，未知作用域禁止自动合并；空值不是新用户。',
 [('AndroidIdUtil.java','getAndroidId'),('DeviceInfo.java','readAndroidId'),('PackageBuilder.java','getEventParameters')])
add('AM04','App Set ID是外部服务标识，不是本地跨设备解析',
 'Reflection调用AppSet客户端、等待任务并取getId；未保存getScope。DeviceInfo门控后保存并进入google_app_set_id。',
 'Google AppSet服务、AdjustConfig','getAppSetIdInfo → getId；SDK未实现其签发/重置规则','google_app_set_id或空',
 'DeviceInfo构造 → Reflection.getAppSetId → PackageBuilder',
 '仅凭getId不能给样本判定developer/device scope；也不能确认重置历史、跨设备或自然人关系。',
 '作用域证据需单独记录；同开发者可共享不等于任意App全局身份。',
 [('Reflection.java','getAppSetId'),('DeviceInfo.java','DeviceInfo'),('PackageBuilder.java','getEventParameters')])
add('AM05','Facebook aid读取依赖外部Provider与签名校验',
 '校验Facebook应用签名后查询AttributionIdProvider的aid，失败返回null。5.7新增显式FB读取开关；5.5没有该显式开关不等于无任何前置约束。',
 '已安装官方Facebook应用及其可访问Provider','包签名校验、ContentResolver查询、游标与异常处理','fbAttributionId → fb_id或空',
 'DeviceInfo构造 → getFacebookAttributionId → getEventParameters',
 'Provider实际返回率、身份粒度、平台匹配或跨设备关系不能由客户端查询代码证明。',
 '外部来源标识记来源/验证条件/读取权限；不将provider标识升级为person。',
 [('DeviceInfo.java','DeviceInfo'),('DeviceInfo.java','getFacebookAttributionId'),('PackageBuilder.java','getEventParameters')])
add('AM06','external_device_id只证明标识传输入口',
 'setExternalDeviceId保存调用方字符串，session/event参数可携带；首会话延迟期间可更新。无该字符串的账号认证或跨设备关系解析代码证明。',
 '开发者提供的字符串','配置赋值；受控首会话延迟修改；构包','external_device_id',
 'AdjustConfig.setExternalDeviceId / FirstSessionDelayManager → PackageBuilder',
 '账户真实性、跨App命名空间、服务器身份合并及partner共享UNKNOWN。',
 '只有经过自有认证的账号才建立account-device边，记录auth证明；同值不得无条件跨租户合并。',
 [('AdjustConfig.java','setExternalDeviceId'),('FirstSessionDelayManager.java','setExternalDeviceIdInDelayI'),('PackageBuilder.java','getSessionParameters'),('PackageBuilder.java','getEventParameters')])
add('AM07','安装和会话以本地状态及计数连续表达',
 '首状态会话计数为1；间隔触发新session/subsession；默认会话间隔30分钟、子会话1秒，Factory可覆盖。resetSessionAttributes不轮换UUID/adid。',
 '活动时间、lastActivity、ActivityState','processSessionI比较间隔；trackNewSessionI计数；buildSessionPackage','/session及session_count、subsession_count等',
 'startFirstSessionI / processSessionI → trackNewSessionI → transferSessionPackageI → PackageBuilder',
 '首次session并不证明服务端最终认定新安装；不能拿计数当全局安装唯一键。',
 '安装、会话和广告机会用不同ID；会话保留显式起止及发生时间。',
 [('ActivityHandler.java','startFirstSessionI'),('ActivityHandler.java','processSessionI'),('ActivityHandler.java','trackNewSessionI'),('ActivityState.java','resetSessionAttributes'),('AdjustFactory.java','getSessionInterval'),('AdjustFactory.java','getSubsessionInterval'),('PackageBuilder.java','getSessionParameters')])
add('AM08','事件token是类型，seq是该类型的本地序号',
 '事件门控后递增eventCount和EventMetadata的eventToken计数，序列化event_token/seq/session_count及android_uuid。',
 '有效AdjustEvent、当前状态、eventToken','trackEventI → incrementSequenceForEvent → buildEventPackage','/event参数及本地EventMetadata',
 'trackEventI → EventMetadata.incrementSequenceForEvent → PackageBuilder.getEventParameters → PackageHandler',
 '不是服务器全局唯一经济事件ID；不能仅用token或seq关联所有App、订单和广告展示。',
 '单独生成事件实例ID；保留event_type、local_seq和installation引用，避免混用。',
 [('ActivityHandler.java','trackEventI'),('EventMetadata.java','incrementSequenceForEvent'),('PackageBuilder.java','getEventParameters'),('ActivityHandler.java','writeEventMetadataI')])
add('AM09','去重是有限本地字符串窗口',
 'deduplicationId非空才查本地orderIds列表；默认容量10、可配置0关闭；列表不含eventToken维度，容量淘汰后重复值可再通过。setOrderId不会自动等价setDeduplicationId。',
 'event.deduplicationId；state列表；容量配置','contains → 拒绝，或入列后再构包/持久化','本地接受或忽略事件',
 'AdjustEvent setters → trackEventI → shouldProcessEventI → ActivityState.eventDeduplicationIdExists/addDeduplicationId',
 '不证明服务端收入去重、订单真实性、跨设备去重或exactly-once；状态/队列分写可能产生崩溃窗口。',
 '采用租户+业务事件实例ID幂等账本和原子outbox；不要把有限缓存当唯一账本。',
 [('AdjustEvent.java','setOrderId'),('AdjustEvent.java','setDeduplicationId'),('ActivityHandler.java','shouldProcessEventI'),('ActivityState.java','addDeduplicationId'),('ActivityState.java','eventDeduplicationIdExists'),('ActivityState.java','ActivityState'),('ActivityState.java','readObject'),('ActivityState.java','<field_declarations>')])
add('AM10','主包队列落盘但没有跨状态原子事务证明',
 'PackageHandler以列表FIFO保存ActivityPackage、app-private序列化；主队列单发送门控，ActivityState/EventMetadata另外写文件。',
 '构造好的ActivityPackage与应用Context','addI追加并写队列；sendFirstI取队首；paused/isSending门控','本地队列及准备提交的包',
 'addPackage → scheduler → addI/writePackageQueueI → sendFirstI → sender',
 '落盘不等于远端提交；独立文件写入不提供exactly-once或事务性崩溃恢复保证。',
 '显式outbox事务、唯一事件键、服务端幂等确认；持久化错误必须可审计。',
 [('PackageHandler.java','addI'),('PackageHandler.java','sendFirstI'),('PackageHandler.java','readPackageQueueI'),('PackageHandler.java','writePackageQueueI'),('ActivityHandler.java','trackEventI'),('Util.java','writeObject')])
add('AM11','HTTP结果、是否重试和业务成功不同',
 'sender把success定义为JSON存在、无retryIn且HTTP200；willRetry主要取决于JSON缺失或retryIn存在。主队列!willRetry即推进队首，不能称成功收款/入库。',
 '连接结果/HTTP码/JSON/retry_in','tryToGetResponse → onResponseDataCallback；退避上限和随机抖动','success、willRetry、退避/出队/回调',
 'ActivityPackageSender.tryToGetResponse → PackageHandler.onResponseDataCallback → sendNextI/重试',
 '不证明服务器写入、伙伴收到、模型读取；HTTP错误+有效JSON且无retry_in也可能不重试。',
 '运输确认、业务入账确认及特征消费确认分层；指数退避与幂等配合。',
 [('network/ActivityPackageSender.java','tryToGetResponse'),('PackageHandler.java','onResponseDataCallback'),('PackageHandler.java','sendNextI'),('Util.java','getWaitingTime')])
add('AM12','序列化保存事件上下文，发送另有时间',
 '构包写created_at等参数，发送构造POST表单并编码；发送前可加入sent_at/排队重试字段。客户端创建和发送时刻不是服务器可用时间。',
 'ActivityPackage.parameters、构包时间、发送时间','map → form-urlencoded POST；ActivityPackage对象持久化','静态可见的请求构造规则',
 'PackageBuilder.getEventParameters → ActivityPackage → generatePOSTBodyString/injectParametersToPOSTStringBuilder',
 '真实payload、到达/available_at、远端可用时间和训练时点UNKNOWN。',
 '事件发生/采集/送达/available_at分别记录；推断前必须校验available_at≤decision_at。',
 [('PackageBuilder.java','getEventParameters'),('ActivityPackage.java','writeObject'),('PackageHandler.java','sendFirstI'),('network/ActivityPackageSender.java','configConnectionForPOST'),('network/ActivityPackageSender.java','generatePOSTBodyString'),('network/ActivityPackageSender.java','injectParametersToPOSTStringBuilder')])
add('AM13','referrer/deeplink是归因输入，不是本地归因算法',
 'PackageFactory把referrer或deeplink构造成/sdk_click；按已保存的referrer详情抑制重复。SdkClickHandler独立内存队列/重试，不等同主落盘FIFO。',
 '安装referrer、来源API、click/install时间戳、deeplink','sendInstallReferrerI比较详情 → SDKclick包 → 单独队列 → 返回详情保存','/sdk_click参数与本地referrer状态',
 'sendInstallReferrerI → PackageFactory.buildInstallReferrerSdkClickPackage → SdkClickHandler → checkForInstallReferrerInfo',
 '没有本地归因胜者选择/跨设备图谱算法证明。非重试分支复制referrer详情，不应单凭注释称服务端成功归因。',
 '原始触点和归因结果分存；重复触点抑制不替代经济事件去重。',
 [('ActivityHandler.java','sendInstallReferrerI'),('PackageFactory.java','buildInstallReferrerSdkClickPackage'),('PackageFactory.java','buildDeeplinkSdkClickPackage'),('SdkClickHandler.java','sendSdkClickI'),('SdkClickHandler.java','sendNextSdkClickI'),('ActivityHandler.java','checkForInstallReferrerInfo'),('Util.java','isEqualReferrerDetails')])
add('AM14','Adjust adid与归因结果来自服务器响应',
 'parseResponse读取adid、attribution、tracking_state及调度字段；客户端更新adid/归因缓存并触发回调。session success时标记installTracked。',
 '响应JSON','parseResponse → session/event/sdkclick/attribution回调 → 更新状态','本地adid、归因结果及应用回调',
 'ActivityPackageSender.parseResponse → launchSessionResponseTasksI → updateAdidI/updateAttributionI；AttributionHandler.checkAttributionI',
 'adid签发范围、同人/设备匹配、归因算法、graph entity及模型消费全为服务端UNKNOWN。adid不等于gps_adid。',
 '远端返回标识保留issuer/product/时间；归因是一条有来源的结果边，不是本地同人事实。',
 [('network/ActivityPackageSender.java','parseResponse'),('ActivityHandler.java','updateAdidI'),('ActivityHandler.java','updateAttributionI'),('ActivityHandler.java','launchSessionResponseTasksI'),('AttributionHandler.java','checkAttributionI')])
add('AM15','GDPR请求与opt-out响应是不同阶段',
 'gdprForgetMe先缓存意图；本地handler标记forgotten并把GDPR包加入主队列。gotOptOutResponseI明确flush主队列并disable；GDPR方法本身未flush主队列，也未清空UUID/adid。',
 '开发者GDPR调用或服务器opted_out响应','缓存 → 状态持久化/排队；或optout → flush+disable','本地门控及待发送删除请求',
 'AdjustInstance.gdprForgetMe → ActivityHandler.gdprForgetMeI；sender.parseResponse → gotOptOutResponseI',
 '不证明所有队列即时取消、所有派生/伙伴缓存删除或服务器删除完成；普通配置禁读不等于撤回已排队字段。',
 '删除独立高优先级控制通道、撤销epoch、队列清理、派生特征清理和接收方确认。',
 [('AdjustInstance.java','gdprForgetMe'),('ActivityHandler.java','gdprForgetMeI'),('ActivityHandler.java','gotOptOutResponseI'),('ActivityHandler.java','trackEventI'),('network/ActivityPackageSender.java','parseResponse')])
add('AM16','disable/offline不等于身份删除',
 'setEnabledI持久化启停并拒绝重新启用已forgotten状态；offline调整发送门控。它们不构成本地身份删除契约；离线时可继续积累事件包。',
 'enabled/offline状态','设置状态、暂停/恢复handlers；事件enabled/GDPR校验','暂停或恢复发送与事件接纳',
 'setEnabledI/setOfflineModeI → updateHandlersStatusAndSendI；trackEventI',
 '不能由暂停推断清库、撤销伙伴接收或新旧ID断开。',
 '区分collection_allowed、transmission_allowed、purpose_allowed和delete_required。',
 [('ActivityHandler.java','setEnabledI'),('ActivityHandler.java','setOfflineModeI'),('ActivityHandler.java','trackEventI')])
add('AM17','measurement consent与TPS是专门设置事件',
 'measurement consent/TPS按状态门控后构包；不自动证明所有ID读取被关闭或伙伴已执行。5.7新增TPS返回结果、缓存和设置回调。',
 '开发者consent/TPS设置','canTrack* → 构包 → 主队列','measurement_consent/third_party_sharing事件',
 'trackMeasurementConsentI/trackThirdPartySharingI → PackageBuilder → PackageHandler',
 '远端用途落实、伙伴设置同步和撤销历史数据UNKNOWN；真实用户授权不能由布尔配置替代。',
 '用途授权做版本化状态机；读取/发送/特征服务同一epoch校验。',
 [('ActivityHandler.java','trackMeasurementConsentI'),('ActivityHandler.java','trackThirdPartySharingI'),('PackageBuilder.java','buildMeasurementConsentPackage'),('PackageBuilder.java','buildThirdPartySharingPackage')])
add('AM18','本地清理入口不是生产删除保证',
 'AdjustFactory.teardown(context)可调用ActivityHandler.deleteState和PackageHandler.deleteState清本地状态/队列；不能等价公开用户删除API及服务器删除完成。',
 'Factory teardown传入的Context','删除指定本地文件/偏好并释放Factory引用','本地测试/生命周期清理能力',
 'AdjustFactory.teardown → ActivityHandler.deleteState + PackageHandler.deleteState',
 '其他进程缓存、系统ID、服务端归因历史、伙伴和训练数据删除UNKNOWN。',
 '身份生命周期与测试清理分开；生产删除需要全接收方确认及可审计的范围。',
 [('AdjustFactory.java','teardown'),('ActivityHandler.java','deleteState'),('PackageHandler.java','deleteState')])
add('AM19','5.7起本地反序列化加入类白名单',
 'Util.readObject从ObjectInputStream改成ObjectInputFilterStream；resolveClass拒绝未列入类。只证明限定的本地反序列化约束。',
 '应用私有序列化文件','allowed-class检查，未知类抛InvalidClassException','反序列化对象或失败',
 'Util.readObject → ObjectInputFilterStream.resolveClass',
 '不是数据加密、完整性签名或全安全证明；未执行损坏文件或兼容性测试。',
 '新实现优先schema校验与显式版本迁移；避免不受控对象反序列化。',
 [('Util.java','readObject'),('ObjectInputFilterStream.java','resolveClass')],['5.7.0','5.8.1'])
add('AM20','5.8.1细分ID禁读且保持wire身份语义',
 'Google/Android/Fire/plugin分别有禁读开关及总禁读方法；儿童模式另门控。playAdId重命名googleAdId但wire键gps_adid不变。',
 '配置开关、COPPA/Kids状态','禁读各入口；reload时依据开关','新读取可被禁止；并非全局撤销已缓存/排队标识',
 'AdjustConfig.disable* → Util.is*ReadingEnabled → DeviceInfo/PackageBuilder',
 '不能确认远程接收或删除；运行时修改配置能否覆盖所有历史缓存需专门测试。',
 '最小必要读取、用途门控、构包/发送再次校验；禁读与删除分离。',
 [('AdjustConfig.java','disableDeviceIdsReading'),('AdjustConfig.java','disableGoogleAdIdReading'),('Util.java','isGoogleAdIdReadingEnabled'),('Util.java','isAndroidIdReadingEnabled'),('Util.java','isAppSetIdReadingEnabled'),('DeviceInfo.java','reloadOtherDeviceInfoParams')],['5.8.1'])
add('AM21','重试恢复字段和retryIn分支发生修正',
 '5.8.1 readObject读取retryCount而非errorCount，与serialPersistentFields一致；主队列只有retryIn>0才直接按该值调度，否则走退避。',
 '旧队列序列化字段、响应retryIn','本地恢复键修正和分支选择','恢复的retryCount/重试等待',
 'ActivityPackage.readObject → PackageHandler.onResponseDataCallback',
 '静态修正不等于测得更高交付率；历史文件兼容/实际部署效果未运行验证。',
 '版本化迁移并保留恢复测试；等待语义与业务确认分离。',
 [('ActivityPackage.java','readObject'),('ActivityPackage.java','<field_declarations>'),('PackageHandler.java','onResponseDataCallback')],['5.7.0','5.8.1'])
add('AM22','远程设置返回不证明模型特征消费',
 '5.7起有TPS结果保存/回调和控制参数处理；构包可携带control_params。这是配置/状态传输，不是身份图谱特征读取证据。',
 '服务器JSON、TPS设置结果、control参数','parse/缓存/回调；参数再次构包','客户端可读取的远程控制状态',
 'parseResponse → ActivityHandler.updateThirdPartySharingSettingsI → prefs/listener；PackageBuilder',
 '远端规则版本含义、partner实际接收和Axon/Vector读取UNKNOWN。',
 '控制面与特征数据面分离；记录规则版本与实际消费审计，不凭开关推断上线。',
 [('network/ActivityPackageSender.java','parseResponse'),('ActivityHandler.java','updateThirdPartySharingSettingsI'),('PackageBuilder.java','getEventParameters')],['5.7.0','5.8.1'])

save(D/'CODE_EVIDENCE.json',refs)
save(D/'FINDINGS.json',findings)
flat=[]
for x in findings:
    for v,ids in x['evidence_by_version'].items():
        s=next(z for z in SAMPLES if z['version']==v)
        flat.append(dict(finding_id=x['id'],title=x['title'],sample_id=s['sample_id'],version=v,archive=s['path'],archive_sha256=s['sha256'],
          evidence_ids=';'.join(ids),input=x['input'],processing=x['processing'],output=x['output'],call_chain=x['call_chain'],
          proven_client_mechanism=x['proven_client_mechanism'],server_unknown=x['server_unknown'],reference_design=x['reference_design'],evidence_level=x['evidence_level']))
csvout('FINDINGS.csv',flat)

header='''# Adjust限定源码机制验证

本轮仅静态分析OSM034/036/038三份MIT源码，未启动SDK，未发送生产请求，未读取真实第三方身份；未修改76号程序，未创建79号生产取证任务。**C_graph.Axon=UNKNOWN，C_graph.Vector=UNKNOWN，D=UNKNOWN；原生产取证STOP。** Adjust机制不归属于Axon/Vector。

方法：选取111个Java文件条目，逐链阅读并进行文本差分。2486个初始方法定位只是词法辅助，不是完整AST/调用图；Map等泛型返回方法另补定位，精确摘录见CODE_EVIDENCE.json。全部结论限于所列版本、路径和分支；未执行OS权限、网络、崩溃恢复或服务器验证。
'''
sample_table='\n| 样本 | 版本 | 原始归档SHA256 |\n|---|---|---|\n'+'\n'.join(f"| {s['sample_id']} | {s['version']} | `{s['sha256']}` |" for s in SAMPLES)
write('README.md',header+sample_table+'''

## 交付导航

1. [Adjust身份与归因机制图](Adjust身份与归因机制图.md)
2. [三版本源码差分](三版本源码差分.md)
3. [身份标识生命周期表](身份标识生命周期表.md)
4. [已证实机制与服务端未知清单](已证实机制与服务端未知清单.md)
5. [自主Identity Resolver最小设计建议](自主IdentityResolver最小设计建议.md)
6. [下一阶段授权和测试条件](下一阶段授权和测试条件.md)

附：[版本许可复核](license-review/版本许可复核.md)、[逐版本发现矩阵](FINDINGS.csv)、[完整原文/行号/哈希](CODE_EVIDENCE.json)、[可读代码定位](CODE_LOCATIONS.md)、[最终diff索引](DIFF_INDEX.final.json)、[静态保全验证](VALIDATION.json)。旧diffs/为开发中间产物，正式差分只引用diffs-final及DIFF_INDEX.final.json。

运行复核：`python -X utf8 adjust-mechanisms/validate.py`。这只验证静态证据和历史保全，不加载Java、不连接SDK服务器。build_deliverables.py会重建本轮报告；index_and_validate.py仅追加本轮索引/证据图，不改旧对象。

SAMPLES.json保留盘点时的permission_gate/new_functional_analysis原始值；当前范围见STATUS.json，不能将旧快照当成本轮未开展。归档的HTTP Last-Modified不等于正式发布日期，正式发布日期仍UNKNOWN。
''')

loc=['# 代码定位与样本血缘','每个编号对应完整方法摘录（JSON）及原始归档哈希。路径是源码副本，已按JAR成员字节核验；MIT LICENSE随各版本保留。']
for x in refs:
    spans='、'.join(f"L{z['start_line']}–{z['end_line']}" for z in x['spans'])
    link=x['path'].removeprefix('adjust-mechanisms/')
    loc.extend([f"\n## {x['id']} · {x['sample_id']} / {x['version']}",f"`{x['class_name']}#{x['method']}`；{spans}；[源码]({link}#L{x['spans'][0]['start_line']})。",
        f"归档：`{x['archive']}`；SHA256 `{x['archive_sha256']}`。源码SHA256 `{x['sha256']}`。"])
write('CODE_LOCATIONS.md','\n\n'.join(loc))

details=[header+sample_table,'\n## 22项发现及证明边界\n']
for x in findings:
    citations=[]
    for v,ids in x['evidence_by_version'].items(): citations.append(v+'：'+', '.join(f'[{i}](CODE_LOCATIONS.md#{i.lower()}--{next(z for z in SAMPLES if z["version"]==v)["sample_id"].lower()}--{v.replace(".","")})' for i in ids))
    # Stable plain IDs plus central location file avoids dependence on Markdown anchor normalization.
    citations=[v+'：'+', '.join(ids) for v,ids in x['evidence_by_version'].items()]
    details.extend([f"\n### {x['id']} {x['title']}\n",x['proven_client_mechanism'],
      f"输入：{x['input']}。处理：{x['processing']}。输出：{x['output']}。",
      f"调用链：`{x['call_chain']}`。",f"服务端未知：{x['server_unknown']}",f"独立设计参考：{x['reference_design']}",
      '代码证据（[定位与完整哈希](CODE_LOCATIONS.md)，[原文](CODE_EVIDENCE.json)）：'+'；'.join(citations)+'。'])
details.append('''
## 客户端无法证明的清单

归因胜者选择、adid签发范围、OS标识和账号的服务端合并、旧新标识重连、跨设备/跨人/家庭实体、partner实际接收、服务器删除确认、训练标签、特征物化、Axon/Vector模型读取和独立收益均UNKNOWN。

本轮没有认证账户的跨设备关系解析算法证据；external_device_id只是输入字符串。这个有界结论不排除SDK之外的服务端能力。可见同一OS标识接口、同一设备或相同字段值，不足以证明个人级跨App图谱。静态请求构造也不是实际发送/接收。
''')
write('已证实机制与服务端未知清单.md','\n\n'.join(details))

write('Adjust身份与归因机制图.md',header+'''

## 调用链

```mermaid
flowchart TD
  A[应用私有状态文件] --> B[ActivityState UUID/计数/去重记录]
  O[OS广告ID/Android ID/AppSet/外部Provider] --> G[版本与儿童/读取门控]
  G --> C[DeviceInfo 缓存与读取]
  X[开发者 external_device_id/事件/收入声明] --> P[PackageBuilder 参数快照]
  B --> P
  C --> P
  P --> Q[PackageHandler 主队列与独立落盘]
  R[referrer/deeplink] --> K[PackageFactory sdk_click]
  K --> S[SdkClickHandler 独立队列]
  Q --> N[Sender POST构造/重试规则]
  S --> N
  N -. 未执行网络 .-> U[Adjust服务器 实际接收未知]
  U -. 响应契约 不是生产观测 .-> J[parseResponse adid/attribution/optout]
  J --> B
  J --> L[归因/跟踪回调]
  U -. 未证实的伙伴发送 .-> V[广告平台实际接收 UNKNOWN]
  V -. 未证实 .-> M[Axon/Vector模型消费 UNKNOWN]
```

图中实线只代表选定源码中可追踪的调用/数据关系，不代表运行成功。未实施广告机会ID→经济展示→收入→模型的生产闭环。

| 关系 | 已证实客户端机制 | 不应推断 | 证据 |
|---|---|---|---|
| 本地实例→事件 | android_uuid+应用token/包名+session计数+seq入参 | UUID是自然人/跨App通用ID | AM01/07/08/12 |
| OS标识→参数 | 门控读取、空值省略/回退、构包 | 同值=同人，或服务器实际匹配 | AM02–05/20 |
| 账号字符串→请求 | external_device_id传输 | 已认证账户、跨设备合并 | AM06 |
| referrer→归因返回 | sdk_click输入、响应缓存/回调 | 客户端算出归因或同人实体 | AM13/14 |
| 事件→去重/队列 | 有限本地去重，独立文件FIFO | 全局经济事件唯一性、exactly-once | AM09–11 |
| 收入字段→服务器/伙伴 | 事件参数支持声明金额等 | 真实成交、伙伴收妥、模型训练 | AM08/12及其服务端未知项 |
| 删除意图→本地门控 | forgotten状态、GDPR包、optout flush/disable | 服务器/伙伴历史删除完成 | AM15–18 |

逐路径、类/方法/行号和三版本哈希见[22项发现](已证实机制与服务端未知清单.md)及[CODE_EVIDENCE.json](CODE_EVIDENCE.json)。

## 同设备跨应用问题的回答

独立应用可能读取同一外部OS/服务标识，是否同值受OS、用户、签名、开发者/分发作用域、权限和重置规则影响；这里没有执行两App读取，也没有完整外部作用域契约。因此只能证明“有读取和携带外部标识的客户端入口”。本地android_uuid来自应用私有SDK状态，不是SDK自行创建的跨App共享标识。

AppSet路径只取getId不取getScope，不能用这一字符串判定样本的developer/device scope。AndroidID由Secure设置提供，SDK不实现OS的版本/签名/用户作用域规则。Google广告ID是广告标识而非跨设备自然人凭据。FB aid依赖外部Provider和官方签名校验，不是Adjust自建身份解析服务。
''')

diffs=json.loads((D/'DIFF_INDEX.final.json').read_text(encoding='utf-8'))
changed=[x for x in diffs if x['status']!='UNCHANGED']
dt='\n| 版本 | 文件 | 类型 | 完整diff |\n|---|---|---|---|\n'+'\n'.join(f"| {x['from_version']}→{x['to_version']} | {x['entry']} | {x['status']} | [diff]({x['diff_path'].removeprefix('adjust-mechanisms/')}) |" for x in changed)
write('三版本源码差分.md',header+sample_table+'''

## 差分结论

范围为所选111个条目，按版本配对共76个文件比较，24个有变化/新增（不是整个SDK的变更数）。新增仅指本轮比较集合的对应版本缺失；未据此断言发布历史首次出现。原始SHA和diff SHA见DIFF_INDEX.final.json；统一diff规范化换行，原始成员哈希保留。

| 机制 | 5.5.0→5.7.0 | 5.7.0→5.8.1 | 证据/限制 |
|---|---|---|---|
| 本地UUID/去重/事件seq | 相关选定文件未变 | 相关选定文件未变 | ActivityState/EventMetadata/AdjustEvent；外围变化不代表系统行为完全相同 |
| FB标识读取 | 增加显式disableFbIdReading与canReadFbId | 整理为isFbIdReadingEnabled | AM05/20；5.5签名Provider等前提仍在 |
| Google等设备标识 | 仍reloadPlayIds | rename google；新增Google/Android/Fire/plugin及总禁读 | AM02/20；wire gps_adid未变，非新身份类型 |
| TPS与远程控制 | 结果/设置回调、缓存、control参数链 | 延续 | AM17/22；不能推断实际partner执行或模型 |
| 本地反序列化 | 增加ObjectInputFilterStream类白名单 | 延续 | AM19；非加密/完整安全证明 |
| 重试调度 | 未见该条件变化 | retryIn非空且正才直接等待 | AM11/21；否则退避，非业务成功保证 |
| 队列计数恢复 | 读取errorCount | 改读retryCount，与持久字段相符 | AM21；未运行跨版本恢复 |
| 连接读取/编码 | 无此轮重点变化 | null stream处理、资源关闭和ENCODING整理 | sender diff；未测实际网络收益 |
| 设备环境 | 新增系统应用/更新系统应用信息 | 延续并有其他外围调整 | DeviceInfo diff；不是同人匹配 |
| 跨设备身份图谱 | 未取得该解析算法证据 | 未取得该解析算法证据 | 有界静态结论，服务端UNKNOWN |

## 配对差分目录
'''+dt+'''

Constants及外围referrer/preinstall变化一并保存在diff中，不升级成身份解析结论。初始词法定位2486项并非方法总数；泛型返回方法的补定位包含于CODE_EVIDENCE，不能用方法数比较功能强弱。程序只比较源码文本，没有调用SDK和编译网络依赖。
''')

life=[
 ('android_uuid','AM01','ActivityState / Util.createUuid','应用私有SDK状态（非物理设备/个人）','新建/缺失字段时生成；会话重置不轮换','状态文件清除可重建；卸载/备份由OS决定','构包可携带；真实接收UNKNOWN','不得跨应用按本地UUID合并'),
 ('gps_adid','AM02','OS广告服务/Reflection','OS广告标识；非跨设备账号','默认重读；read-once当前对象可缓存','OS重置由外部服务提供新值；未见自动清历史链','读取门控、儿童限制；不是删除回执','存namespace/有效时间，不恢复已退出标识'),
 ('android_id','AM03','Settings.Secure','OS版本/用户/签名范围；本轮未核实完整外部契约','条件回退；单次读取缓存','重置/作用域由OS；客户端不签发','无Google/Fire参数时才回退且需门控','不可当全局设备主键'),
 ('google_app_set_id','AM04','Google AppSet服务','scope由外部返回；本路径未读取getScope','DeviceInfo初始化门控读取','外部签发/重置规则未在客户端实现','儿童/开关门控；缓存不是接收证据','缺scope禁止任意App等值合并'),
 ('fb_id','AM05','Facebook官方签名Provider aid','外部Provider作用域UNKNOWN','构造读取，失败空值','本客户端不定义其重置/实体范围','5.7新增显式开关；Provider前提仍必要','外部标识只建有来源候选边'),
 ('external_device_id','AM06','开发者输入','开发者自定义；不自带认证/全局命名空间','配置或首会话延迟更新','变更没有账户解绑完整契约','客户端构包；partner/图谱用途UNKNOWN','验证账号所有权、租户与用途后才建边'),
 ('adid','AM14','服务器响应JSON','Adjust服务端定义；本轮无实体范围契约','非空变化后写本地ActivityState','重签发/旧新ID合并由服务端UNKNOWN','响应解析不是观测到实际下发','必须保留issuer与响应来源；不等于GAID'),
 ('event_token / seq','AM08','事件配置 / EventMetadata','事件类型 / 本地每类型序号','每接受事件递增；独立文件持久化','本地metadata清除重建','构包带seq，不提供全局唯一事件契约','分离事件类型与事件实例ID'),
 ('deduplication_id / order_id','AM09','开发者输入','前者本地共享列表；后者订单声明','前者默认仅保留10个，可设0；两setter独立','淘汰/本地丢失允许重复；非服务器去重','没有跨系统经济事件唯一契约','业务幂等账本按租户/事件实例，保留退款'),
 ('session_count / subsession_count','AM07','ActivityState','当前SDK状态内计数','默认30min/1s间隔更新，可覆盖','新会话不重置实例UUID/adid','非session UUID或新安装证据','会话与安装实例分层'),
 ('referrer详情','AM13','安装referrer提供者','来源API+触点详情','本地详情比较抑制重复；成功/重试分支需区分','服务端归因/多触点规则UNKNOWN','sdk_click独立队列；不是主队列持久化保证','保留原始触点及返回结果的独立血缘'),
 ('forgotten / enabled / offline','AM15/16','开发者调用 / 响应 / 内部状态','本地控制面','忘记、禁用、离线各自门控；非同义','optout flush主队列；GDPR本身排队；本地teardown另列','不证明服务器/伙伴/特征删除','授权epoch与删除传播覆盖所有派生缓存'),
]
lifecsv=[dict(identifier=x[0],finding=x[1],issuer=x[2],scope=x[3],creation_and_cache=x[4],reset_and_lifetime=x[5],privacy_and_unknown=x[6],reference_design=x[7]) for x in life]
csvout('IDENTITY_LIFECYCLE.csv',lifecsv)
table='\n| 标识 | 生成者/作用域 | 生命周期与重置 | 权限/限制 | 代码证据 |\n|---|---|---|---|---|\n'+'\n'.join(f'| {x[0]} | {x[2]}；{x[3]} | {x[4]}；{x[5]} | {x[6]} | {x[1]} |' for x in life)
write('身份标识生命周期表.md',header+'''

完整列及独立设计参考见[IDENTITY_LIFECYCLE.csv](IDENTITY_LIFECYCLE.csv)，逐版本归档和源码方法/行号见[FINDINGS.csv](FINDINGS.csv)及[CODE_LOCATIONS.md](CODE_LOCATIONS.md)。表中OS作用域不由SDK保证；未运行任何真实设备实验。
'''+table+'''

### 重置的关键边界

5.8.1 reloadGoogleAdId先将相关字段清空再读取；所谓previousGoogleAdId局部值是在清空及可选Samsung读取之后取值，不能描述为“持久保存上一次OS广告ID以恢复追踪”。默认非read-once，但配置read-once或其他缓存可改变何时重读。没有在这条调用链找到旧新OS广告ID比较后自动轮换UUID/adid/清全队列的逻辑；服务器如何处理历史仍UNKNOWN。

读取开关主要控制读取入口；构造时已缓存的AppSet/FB及已排队包不因此获得全局追溯撤回保证。measurement consent/TPS上传不等于本地统一的全部身份禁读或远端删除完成。此处是控制范围分析，不是未经运行验证的隐私违规结论。
''')

write('自主IdentityResolver最小设计建议.md',header+'''

以下是自主参考设计，不复制Adjust实现，不声称厂商采用本架构；本轮只交设计，不开发/运行解析器。

| 模块 | 最小数据与不变量 | 本轮参考 |
|---|---|---|
| Namespace Registry | issuer、tenant、app、entity_type、scope_evidence、版本；未知scope不得全局合并 | AM01–06/14 |
| Identity Resolver | 标识相等只产生候选关系；自有已认证账号可建account-device边，禁止自动升级person/household；不做真实个人概率重识别 | AM02–06 |
| Relationship Store | relation_id、from/to、粒度、evidence、quality_type、valid_from/to、recorded_at、consent_epoch、revoked_at；不破坏性union所有设备 | AM06/15–18 |
| Temporal Event Linker | event_instance_id、event_type、installation、session、occurred_at、received_at、available_at；只链接有证据的事件，不拿请求ID充收入主键 | AM07–14 |
| Consent & Deletion | collection/transmission/purpose分别授权；撤销epoch立即拒读；删除遍历关系、outbox和派生缓存，确认有范围与截止时点 | AM15–18/20 |
| Graph Feature Service | as_of及model/purpose/epoch校验；来源关系、特征materialized_at、available_at；失效/撤销后不得使用旧快照 | AM12/15/20 |
| LTV Feature Consumer | 默认仅空接口；记录非空feature_group、模型版本、decision_trace；真实标签/授权未获准不训练，收益UNKNOWN | AM12/14/22及78号契约 |
| Audit & Provenance | 原件SHA、代码/规则版本、接收/消费独立引用、缺失字段、UNKNOWN判定；mock不升级生产 | AM10–14及76/78原则 |

## 最小模式与解析规则

```text
IdentityKey = (tenant, issuer, namespace_version, entity_type, scoped_value)
Relation = (relation_id, source_key, target_key, relation_type, evidence_id,
            valid_from, valid_to, observed_at, available_at, purpose,
            consent_epoch, revoked_at, quality_type)
Event = (tenant, app, event_instance_id, event_type, install_id, session_id,
         occurred_at, received_at, available_at, consent_epoch, payload_hash)
FeatureRead = (trace_id, model_id, model_version, feature_group, nonempty_count,
               source_relation_ids, graph_version, as_of, read_at, purpose, epoch)
```

标识仅在相同tenant/issuer/namespace和作用域证据成立时比较；设备、安装、账号、人、家庭分别建节点。一个账号可被多人共享，一个人可有多个账号，因此account链接不能自动证明person。仅有模型分数变化时返回不可识别。

时间查询要求occurred_at≤available_at≤决策时刻，关系valid_from/valid_to与撤销时刻同时生效；迟到事件不能倒灌早期决策。数据删除使用tombstone和epoch阻断旧缓存，按来源遍历派生特征，拒绝旧关系重放。

幂等键用(tenant, app, event_instance_id)，事件接受与outbox原子提交；重试具有独立attempt_id，不改变经济事件主键。服务端幂等确认不能由FIFO出队或HTTP200代替。不同事件类型不得复用去重键；订单/退款、广告展示和收入修正分别表达。

## 可复现测试设计（尚未执行）

| 测试 | 自有/合成输入 | 预期 | 反例 |
|---|---|---|---|
| namespace隔离 | 两应用相同字符串但不同issuer/scope | 不合并 | 按裸字符串union必须失败 |
| 账号关系 | 两自有设备经自有账号认证；另一个共享账号 | account-device边，person仍未确定 | 相同账号不能生成已证实person边 |
| 重置 | 撤销旧设备标识epoch，新建测试标识 | 旧关系失效，禁止恢复追踪 | 旧缓存特征读应拒绝 |
| 去重 | 同实例重试、不同类型复用相同业务串、窗口外重放 | 实例幂等且不同业务不误删 | 有限10项缓存不满足持久幂等 |
| 时间 | 迟到收入、晚于决策的特征 | 拒绝早期读 | 仅按occurred_at过滤会泄漏 |
| 删除 | outbox、图边、缓存、特征快照都含待撤销记录 | 每层可核对清理及审计确认 | 只flush队列不算删除完成 |
| UNKNOWN | 删除接收/非空读取/trace任一证据 | 保持不可识别 | 把接口存在当模型消费应拒绝 |

匹配准确率、错误合并/拆分、漂移、查询延迟及撤销传播需合法测试样本和实测；本轮未产生这些数字。对LTV的独立增益需固定样本/容量/时间/预算，聚合学习、共享参数与个人关联分别消融；没有真实授权收入标签不报告收益。
''')

write('下一阶段授权和测试条件.md',header+'''

## 当前准入

| 范围 | 状态 | 条件 |
|---|---|---|
| 三份Adjust MIT源码静态分析 | 本轮完成 | 保留MIT声明；只推导所引客户端机制 |
| 自有实现的namespace/时间/幂等单元测试 | 可另立任务；本轮未开发/运行 | 完全本地自有/合成标识，不加载生产SDK |
| SDK真实OS读取与重置/安装实验 | 未执行，需单独测试方案 | 自有设备/应用、隐私授权、OS范围契约、阻断生产端点；不绕过退出 |
| SDK网络/服务端归因、身份或删除验证 | HOLD | 权利方书面测试授权、指定沙箱、用途/字段/版本/保留及引用权；不得生产请求 |
| MAX/LevelPlay核心功能分析 | HOLD | [版本许可复核](license-review/版本许可复核.md)；未满足不扩范围 |
| Axon/Vector实际图谱消费 | UNKNOWN / 生产执行STOP | 78号F01–F10的匿名接收、非空读取、模型与机会trace完整链 |

## 最少仍需取得的材料

1. OS官方作用域与重置契约：Google广告ID、AndroidID、AppSet的当前版本/用户/签名/分发条件。之后才设计两自有测试App比较，不能拿单次字符串相等判同人。
2. Adjust书面说明/授权匿名schema：adid范围、旧新系统ID处理、安装/事件去重键、删除处理/确认以及沙箱边界。客户端代码不能填补这些服务端环节。
3. 如验证伙伴回传，需授权的MMP接收记录、partner mapping、发出/收妥引用及事件唯一键；严禁只据客户端调用声称平台已收到。
4. 如验证C_graph，需指定Axon或Vector产品、模型版本、实际非空特征读取、graph版本/实体粒度、权限/时间门控和决策trace。Unity Exchange或Adjust接收不得替代Vector消费。
5. 如验证D，另需合法真实收入、成熟观察窗口、完整分母与固定预算/容量对照；不能从SDK架构或本地模拟反推独立收益。

## 六个重点问题

同设备跨App：可读取外部系统/服务标识，但作用域与实际同值需要外部契约；本地UUID不提供跨App通用身份（AM01–05）。

重置：Google重读不保证同步清本地UUID/adid/旧队列；read-once与缓存需另测；服务端历史处理UNKNOWN（AM02/15/20）。

安装/会话/事件：共同参数中的实例UUID、app token/包名、session计数及每类型seq；referrer另有sdk_click链。它们不等于全局收入主键（AM07–14）。

跨设备账号：external_device_id传输不含可证明的账号认证、实体合并与冲突处理；选定客户端链未证明跨设备解析（AM06）。

只在服务端：归因算法、adid实体范围、身份图谱、partner实际共享、删除完成及训练消费均UNKNOWN。不得借Adjust能力升级Axon/Vector（AM13–18/22）。

可独立复现：分作用域标识、时间化关系、会话/事件链接、幂等outbox、权限epoch/删除传播与消费审计；先设计的本地测试，禁止借此恢复第三方真实身份（最小设计文档）。

## 停止/恢复

不重复扫描其他SDK或扩大三样本范围。MAX/Unity具体许可未厘清不分析其实现。涉及未授权后台、私人身份、绕过保护、真实广告或身份请求立即STOP。生产取证只等待权利方提供的新许可、匿名原始接收/消费证据或授权测试环境；本轮不发申请、不创建79号。
''')

# Normalize only the new collector's metadata paths. Raw legal artifacts remain untouched.
manifest_path=D/'license-review/FETCH_MANIFEST.json'
legal=json.loads(manifest_path.read_text(encoding='utf-8'))
for x in legal:
    for key in ['path','text_path']:
        if x.get(key) and x[key].startswith('license-review/'):
            x[key]='adjust-mechanisms/'+x[key]
save(manifest_path,legal)
write('license-review/版本许可复核.md','''# MAX、LevelPlay及适配器版本许可复核

本轮仅补取5份公开许可/许可链接响应，**不开展MAX、Unity或适配器功能静态分析**。原始URL/采集时间/状态/重定向/完整SHA256见[FETCH_MANIFEST.json](FETCH_MANIFEST.json)。条款页面可以公开访问，不等于允许任意逆向；当前版本条款也不能追溯替代历史适用合同。

| 版本/组件 | 新增核验 | 许可结论与准入 |
|---|---|---|
| MAX Android 13.2.0 | 官方release_13_2_0 LICENSE.md 200 | 自定义SDK EULA，非MIT；HOLD |
| MAX Android 13.6.4 | 官方release_13_6_4 LICENSE.md 200 | 同上；HOLD |
| MAX Android 13.7.0 | 官方release_13_7_0 LICENSE.md 200 | 同上；HOLD |
| MAX LICENSE链接的/eula/ | 请求落到/en主页，不是可审阅EULA正文 | 不能声称取得适用历史全文；UNKNOWN/HOLD |
| LevelPlay Unity wrapper 9.3.0 | UnityLevelPlay_9.3.0/LICENSE 200 | Service Asset受Unity Advertising Terms；不自动覆盖Android核心9.5 |
| LevelPlay Android核心9.3/9.4/9.5 | 复用首轮相应POM与Unity条款 | 尚无充分逐版本分析许可；HOLD，不下载/反编译 |
| AppLovin Unity Ads适配器4.17.0.0/4.18.1.0 | 复用首轮逐版本POM | AppLovin Mediation Adapter EULA；HOLD |
| AppLovin ironSource适配器9.3.0.0/9.4.0.0/9.5.0.0 | 复用首轮POM | 同上；HOLD |
| AppLovin Google适配器25.1.0.0/25.2.0.0/25.4.0.0 | 复用首轮POM | 同上；不能套Google仓库Apache许可 |
| Google官方适配器开源仓库 | 首轮Apache2线索 | 需固定对应commit/路径/第三方NOTICE，不放行厂商核心 |

MAX三tag许可原文相同，SHA256 `e736ae9fee62d3e70c9325b848aaf1b37351117889fab3472dee84acec0612f8`。只明确“subject to ... SDK EULA”，没有本地反编译授权证明。LevelPlay wrapper许可SHA256 `4aa74c09508382bcf26b4d62928ece88bb268fff609f901aee999e102e8a070e`。

Unity当前Advertising Terms日期2026-06-30与General Terms 2026-11-16为首轮所采当前文本；不能自动选择成旧SDK的适用合同。反向工程限制及法律例外不能由本审计自行认定适用；继续HOLD，等待明确可分析范围/书面授权或充分适用的许可。

原`ThirdPartySDKs/Discovery/applovin-adapters-license.txt`是404正文，不是许可证。复用原件/来源/哈希见[首轮许可证据](../../official-samples-audit/LICENSE_EVIDENCE.json)、[47份样本目录](../../official-samples-audit/ACQUIRED_SAMPLE_CATALOG.csv)、[版本元数据](../../official-samples-audit/VERSION_PROVENANCE.json)。首轮原件未改。

本轮collector最初以adjust-mechanisms为路径基准；现只把新manifest的path/text_path规范为项目根相对路径，原始raw/txt字节未改。HTTP请求仅为上列5份法律响应，不是生产广告、身份或SDK端点。
''')

save(D/'REPORT_PATHS.json',[f'adjust-mechanisms/{p}' for p in ['README.md','Adjust身份与归因机制图.md','三版本源码差分.md','身份标识生命周期表.md','已证实机制与服务端未知清单.md','自主IdentityResolver最小设计建议.md','下一阶段授权和测试条件.md','license-review/版本许可复核.md']])
save(D/'STATUS.json',dict(reviewed_utc=NOW,scope='Three approved MIT Adjust source archives only',
    samples=[s['sample_id'] for s in SAMPLES],selected_source_entries=len(FILES),initial_lexical_method_locations=len(SYMBOLS),
    findings=len(findings),per_version_findings=len(flat),code_evidence_records=len(refs),changed_or_added_selected_pairs=len(changed),
    public_legal_only_GETs=len(legal),new_SDK_downloads=0,SDK_executions=0,production_requests=0,real_identity_accesses=0,
    engineering76_modified=False,C_graph_Axon='UNKNOWN',C_graph_Vector='UNKNOWN',D='UNKNOWN',production_forensics='STOP',
    max_levelplay_functional_analysis='NOT_PERFORMED;LICENSE_HOLD'))
print(json.dumps(dict(findings=len(findings),per_version_findings=len(flat),references=len(refs),reports=8),ensure_ascii=False))
