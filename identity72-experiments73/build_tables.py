from pathlib import Path
import json,csv,hashlib
R=Path(__file__).resolve().parent.parent;D=R/'identity72-experiments73'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')
fields=[]
def field(name,kind,producer,reader,destination,life,scope,privacy,join,refs,grade):
    fields.append(dict(field=name,kind=kind,producer=producer,reader=reader,upload_and_destination=destination,lifecycle_reset=life,cross_app_scope=scope,privacy_conditions=privacy,association_contract=join,evidence_ids=refs,evidence_stages=grade,actual_upload_observed=False,production_match_proven=False,value_model_consumption_proven=False))
field('GAID/AAID/IDFA','设备广告标识','OS广告标识服务','获准SDK；MAX与Unity代码各自读取','MAX逻辑device payload/Unity privacy payload；实际上传未观测','可由用户/OS删除或重置；IDFA受ATT及可用值限制','同设备可为允许的SDK提供共同广告键；非永久/跨设备个人ID','OS政策、用户选择、同意、隐私门控；不能绕过禁用',['同请求共同出现支持可join候选；不证明服务端匹配成功'],['IG72C01','IG72C04','IG72C27','CGS10'],['E1','E2'])
field('Android ID','平台上下文标识','Android scoped system identity','部分MMP；本轮不重新分析所有vendor','Adjust已核验条件fallback请求字段；非所有SDK必采','受设备用户、签名/应用作用域、重置等平台规则','不能当所有发行商共享的全球设备键','平台权限/政策和SDK配置','字段存在不证明跨网络映射',['L71D01'],['E3'])
field('IDFV','vendor级设备标识','Apple OS','对应vendor app/获准SDK','CAPI可接受、Unity相关字段可选；非Android SDK实测','vendor app卸载/重装等平台条件影响','同vendor同设备，不等于同人其他设备','平台及用途授权；不能代替跨vendor广告同意','不得与Unity engine installation ID强行等同',['IG72S06'],['E3'])
field('App Set ID','开发者集合标识','Google Play services','MAX/Axon；Unity条件字段','MAX app_set_id+scope等请求上下文；Unity privacy payload','13个月未访问、最后app卸载等；具体scope依安装来源','可同开发者集合/同设备；不是跨所有App','使用政策和SDK配置；非用于绕过广告ID限制','SDK返回scope与ID一起解释',['IG72C02','IG72C03','IG72C09','IG72C27','IG72S01'],['E1','E2','E3'])
field('Installation ID / Engine Installation ID','安装身份','Unity Core提供者/Engine桥接','UGS Analytics/IAP消费者','Analytics标准字段及Insights身份打包','本地持久化/重装/提供者原生实现边界见53号','接口同名不证明跨App相等','项目/服务初始化、同意与允许列表','相同provider与存储需逐条证实；不等于PlayerId',['C53S05','C53S12','C53S18','C53S19'],['E1','E2'])
field('Firebase FID','安装身份','Firebase Installations','Unity可选反射/SDK消费者','隐私允许时可能进入Unity相关请求/IAP身份包','安装/应用实例及删除API影响','项目/安装作用域；不是Analytics App Instance ID','同意、SDK依赖、允许列表','仅明确赋值桥；不按Firebase名称合并',['XS01','CGS10'],['E1','E2'])
field('Firebase Analytics App Instance ID','分析实例','Firebase Analytics','Analytics和明确集成消费者','分析事件/部分IAP桥接；实际后台未知','重置analytics/实例条件；非FID同义词','应用实例；账户跨设备须另设user_id','分析同意；不得用户重识别','FirebaseApp options.ApplicationId是项目上下文，不是本字段',['XS41','IG72S13'],['E1','E3'])
field('Customer/Publisher User ID','业务指定账号或本地键','开发者业务代码','MAX、MMP或分析SDK setter','MAX用户上下文；MMP额外/用户字段；配置门控','账号生命周期/本地GUID/注销依调用者','只有同namespace合法稳定账号才可能跨设备；本地GUID不够','开发者声明、同意、项目/伙伴配置','四游戏已证的局部同源键不等于全平台账号',['IG72C08','L71D01','L71C01'],['E1','E2','E3'])
field('External User ID','业务身份','游戏/UnityEngine可选原生userId','Core→Analytics/IAP','Analytics优先外部userID；IAP独立打包','原生桥接或内存fallback；解绑/重置由调用者','无默认跨App契约','SDK初始化、同意/allowlist','不等于UGS PlayerId或广告ID',['C53S05','XS06','XS19'],['E1','E2'])
field('UGS Player ID','项目玩家身份','认证服务token.subject','Auth PlayerId组件及消费者','认证上下文；Analytics/IAP可读取','登录/退出clearCredentials/profile切换影响','项目级PlayerId；跨项目需外部账号/组织契约','登录授权及服务配置','token Subject明确赋值；非Engine ID',['IG72C28','C53S16','C53S17'],['E1','E2'])
field('UPA组织级账户ID / Login ID','账户身份','Unity Player Accounts认证服务','OAuth client/UGS登录链接消费者','OAuth token claims→link/login→UGS项目玩家','账户、外部身份link/unlink、注销/删除','官方组织跨游戏/设备契约；非全发行商广告身份','用户登录、组织/项目配置、账号隐私和删除流程','账户图谱E4；未证UPA→RampID或Vector',['IG72C10','IG72C11','IG72C12','IG72C13','IG72C14','IG72S02','IG72S03'],['E1','E2','E3','E4'])
field('Hashed email / hashed phone','伪名化联系方式','业务输入→规范化/hash；Pixel可条件收集','MAX/Axon UserData、Pixel/CAPI','request user_data/事件payload；CAPI官方接收字段','账户/联系方式可变；hash不具自动删除语义','可作为确定性候选；namespace/算法/服务匹配需契约','真实授权、hash规范；哈希不等于匿名','SDK归一化不是已建跨设备图谱',['IG72C06','IG72C20','IG72P04','IG72P05','IG72P06','IG72S06'],['E1','E2','E3'])
field('IP/IPv6','网络环境','网络连接/业务CAPI入参或传输层可见','接收服务器；部分协议字段','CAPI允许client_ip；网络传输IP不需SDK显式读取','随网络/VPN/NAT改变；可能多人共享','不是设备或个人唯一键；家庭推断需额外证据','合法处理目的及共享范围','IP相同只能环境相似，不证明确定性匹配',['IG72S06','L71D01'],['E3'])
for name in ['Device model','OS version','Language','Timezone','Network type','App version','Carrier/MCC/MNC']:
 field(name,'环境/上下文','OS/应用/网络API','广告SDK/MMP选择字段','已有device/app payload与MMP context；逐vendor实际发送未知','随系统/应用/网络变化','非唯一；组合可能增加可识别性但不证明fingerprint模型','SDK配置、最小化和隐私条件','共同出现不等于服务器概率匹配已运行',['IG72C04','IG72C05','L71D01','L71C09'],['E1','E2','E3'])
field('Device fingerprint','推断性派生标识','若平台存在需服务端算法/契约','未知','未恢复完整生产指纹构造或图谱输出','未知','不能仅凭多个设备字段声称生成了指纹','不得绕过重置、同意或反跟踪','将上下文与概率匹配候选区分',['IG72C04','CGS51'],[])
field('Advertising token / HeaderBiddingToken','广告信号封包','Unity Token builder','适配器/mediation/网关','opaque token作为竞价信号','缓存TTL/生成时刻/格式配置','广告请求上下文，不是跨设备用户主键','SDK隐私门控/配置','不能把未解码token当特征清单',['CGS01','CGS02'],['E1','E2'])
field('MAX request/event/waterfall ID','广告生命周期','响应event_id→T()/waterfall/下一请求','MAX对象/遥测/条件收入广播','基础广播id可被overlay覆盖；S2S另有EVENT_ID','响应/广告位历史/事件各自生命周期','候选可共享；不是经济账本或个人身份','配置/订阅/账户启用','需要映射契约才能跨出口join',['L71C01','L71C02'],['E1','E2'])
field('biddingAdId/objectId/impressionOpportunityId','加载实例','适配器load UUID→Unity选项','Unity load/show/repository/operative','请求/config/事件对象明确复制','广告实例内稳定；本地重复检查非全局持久唯一约束','不跨设备；晚于原HB信号','SDK初始化及同意，广告对象存在','没有与原TokenID相等契约',['L71C15','L71C16','L71C21'],['E1','E2'])
field('trackingToken','服务器opaque广告上下文','gateway响应；viewer可更新','AdObject与operative构造','事件构造复制当前值；持久化重试原bytes','可刷新；旧token服务器语义未知','不是长期自然人键','隐私门控、合法广告上下文','机会ID+事件快照可关联，不证明经济收入标签',['L71C15','L71C16','L71C18','L71C19'],['E1','E2'])
field('operative eventId / Session ID / Event UUID','事件或会话','SDK生成','事件构造/队列/接收方','各自事件/会话字段','每事件或会话；不可互换','不是用户ID','事件用途/采集条件','事件去重不等于身份合并',['L71C16','C53S19'],['E1','E2'])
field('Attribution ID / AppsFlyer ID / click ID','归因实例/广告点击','MMP或广告点击链','MMP/获准伙伴postback','按来源范围发送；all-source对其他来源归因脱敏','重装/归因窗口/点击生命周期','归因scope；非永久跨App账户','伙伴映射/同意/共享开关','MMP已接收/训练须独立证明',['L72S08','L71D01','L72S05','L72S06'],['E3'])
field('Pixel _axwrt / _axeid / _axart','网站访客与点击标记','Pixel cookie/local备份/URL解析','同源Pixel、授权CAPI','事件payload及cookie-match代码；未实际发送','cookie域/过期/浏览器限制；_axwrt约一年参数非保证','同源访客/点击串联；不自动跨域','商家部署、用户同意、远程配置','autoEmailCapture需精确true；服务器匹配未知',['IG72P01','IG72P02','IG72P03','IG72P07','IG72P08','IG72P09','IG72P10'],['E1','E2','E3'])
field('RampID','第三方广告身份','LiveRamp受许可身份解析/翻译','支持的Exchange/DSP伙伴','Unity官方美加库存受众激活；具体请求字段未证','受服务协议/伙伴命名空间与隐私删除控制','产品具跨渠道身份能力；每请求映射成功未知','双方支持/合约/同意和地域限制','UPA→RampID、RampID→Vector训练未知',['IG72S04','IG72S05'],['E3','E4'])
field('UID2','第三方确定性广告身份','UID2受许可邮件/电话等输入→广告token体系','UID2参与者/支持广告伙伴','公开确定性广告身份framework；两厂商具体集成未证','token刷新/退出/隐私机制按服务契约','开放namespace；不是默认所有SDK共享','参与者授权/用户选择/适用政策','不能将UID2产品存在等同Axon/Vector部署',['IG72S09'],['E3','E4'])
save(D/'IDENTIFIER_INVENTORY.json',fields)
with (D/'IDENTIFIER_INVENTORY.csv').open('w',encoding='utf-8-sig',newline='') as h:
 out=[{k:(';'.join(v) if isinstance(v,list) else v) for k,v in x.items()} for x in fields];w=csv.DictWriter(h,fieldnames=list(out[0]));w.writeheader();w.writerows(out)
catalog=[]
def sdk(name,versions,status,cap,refs,level,limits):catalog.append(dict(sdk=name,versions=versions,analysis_status=status,identity_capability=cap,evidence_ids=refs,evidence_stages=level,limits=limits,production_matching=False,axon_vector_consumption=False))
sdk('MAX/Axon','MAX13.6.4;Axon1.3.4','已核验所选完整调用链','设备ID/AppSet/CUID/user_data归一化和请求字段',['IG72C01','IG72C04','IG72C06','IG72C08','IG72C20'],['E1','E2'],'没有完整生产图谱/匹配服务输出')
sdk('Unity Ads/Vector','4.17.0/4.18.1','已核验所选调用链','广告/分析标识和隐私构造、机会事件',['IG72C21','IG72C22','IG72C23','IG72C24','IG72C25','IG72C26','IG72C27'],['E1','E2'],'Vector是服务端产品，不是独立客户端启用证据')
sdk('LevelPlay/ironSource','9.3.0/9.4.0/9.5.0归档','复用已有mediation分析；本轮未恢复新图谱','用户/广告收入接口不自动成为跨设备join',['L71D01'],[],'版本存在不是身份图谱证据；无新的逐字段合并契约')
sdk('AppsFlyer','6.14.2/6.17.5','复用官方字段/业务链','安装作用域ID、CUID/收入和伙伴转发',['L72S08','L72S05','L72S06'],['E3'],'安装/归因和伙伴sharing不等于跨游戏个人图谱')
sdk('Adjust','5.5.0/5.7.0/5.8.1','复用所选源码和伙伴契约','允许设备字段/partner参数/收入',['L71D01','L71C09'],['E1','E2','E3'],'SDK包构造不等于匹配/训练')
sdk('Singular','12.17.0','复用setter核验','开发者显式用户ID',['XS39'],['E1'],'未证目标业务调用或跨SDK共享')
sdk('Firebase Analytics/Installations','Analytics22.1.2;Installations19.0.0等归档','FID/AII区别及官方跨App user ID契约','可选开发者稳定user_id支持BigQuery同人跨App/设备分析',['IG72S13','XS41'],['E3','E4'],'不自动回填历史/不许PII；不等于向Axon/Vector共享')
sdk('Unity Core/Auth/Analytics/IAP','Core1.19.0;Auth3.9.0;Analytics6.3.0;IAP5.5.1','提供者、消费者与账号链接已核验','项目玩家/组织外部账号；IAP身份共包',['C53S12','C53S16','XS11','IG72S02','IG72S03'],['E1','E2','E3','E4'],'E4是账号服务，不是广告图谱/训练列')
sdk('Meta Audience Network','6.21.0/6.22.0;FacebookCore18.0.3','已有归档/选定跨SDK提供者证据','Adjust官方签名校验的Facebook attribution provider',['XS34'],['E1'],'非Facebook登录账号；FAN完整图谱未恢复')
sdk('Google Mobile Ads','25.1.0/25.2.0/25.4.0等','已有归档/适配器链','竞价placement_req_id及广告上下文',['CGS26'],['E1','E2'],'广告请求关联非跨设备人图；不将所有Google数据视为共享')
for name,versions in [('Mintegral','16.9.91'),('Liftoff/Vungle','7.6.3/7.7.1/7.7.6'),('Pangle','7.8.5.2/8.1.0.3/8.1.0.5'),('Chartboost','归档目录存在，但本轮未确认独立可用AAR/接口')]:
 sdk(name,versions,'归档核验；本轮未找到可补核心断点的身份合并链','UNKNOWN',[],[],'不能从适配器/同名设备字段声称图谱；不宣称已逐类完成逆向')
sdk('Branch','公开Android API文档；本轮未下载二进制','官方setIdentity/logout契约','开发者非PII别名可跨平台/重装持久归因',['IG72S12'],['E3','E4'],'未证与两平台的图谱共享')
sdk('Amplitude','公开文档；本轮未下载二进制','官方device/user/Amplitude ID合并','登录后的账号关联、同组织项目作用域',['IG72S11'],['E3','E4'],'稳定userID由客户指定；不是全球广告图谱')
sdk('Mixpanel','Simplified ID Merge API文档；未下载SDK','官方显式merge契约','$device_id+$user_id同事件→identity cluster；logout reset',['IG72S10'],['E3','E4'],'共享设备未reset会误合并；两平台集成未知')
sdk('LiveRamp/RampID','官方产品+Unity2026-04-02公告','第三方身份激活契约','跨渠道身份/受众激活',['IG72S04','IG72S05'],['E3','E4'],'Unity具体输入/返回映射和Vector消费未证')
sdk('UID2','公开namespace/确定性服务文档','官方服务契约','广告身份framework',['IG72S09'],['E3','E4'],'未证两平台部署；不构造真实身份查询')
save(D/'SDK_CAPABILITY_MATRIX.json',catalog)
inventory=['# 72号：设备标识与身份标识完整清单','', '2026-11-20。此处“完整”指覆盖本任务要求的类别；**不声称恢复了所有SDK或服务器内部字段**。复用103个AAR和67个sources.jar归档哈希，没有重复下载SDK。没有采集真实标识、解码真实token或发送生产请求。','', 'E1读取能力、E2上传构造代码、E3接收/用途文档、E4身份服务关联契约、E5实际匹配、E6入预测模型。以下E1—E4可独立存在，不自动连成六层。没有E5/E6。','', '| 字段 | 来源/读取方 | 上传目的地与观测边界 | 生命周期/作用域 | 同意/授权 | 关联程度/证据 |','|---|---|---|---|---|---|']
for x in fields:
 join='；'.join(x['association_contract']) if isinstance(x['association_contract'],list) else x['association_contract']
 inventory.append(f"| {x['field']} | {x['producer']}；{x['reader']} | {x['upload_and_destination']} | {x['lifecycle_reset']}；{x['cross_app_scope']} | {x['privacy_conditions']} | {join}；{','.join(x['evidence_stages']) or 'UNKNOWN'}；{','.join(x['evidence_ids'])} |")
inventory+=['','原始SDK版本、类/方法、行号、源码及原包SHA256见[证据目录](identity72-experiments73/SOURCE_CATALOG.md)、[代码对象](identity72-experiments73/CODE_EVIDENCE.json)。[逐字段机器表](identity72-experiments73/IDENTIFIER_INVENTORY.json)保留全部列。没有真实上传/成功匹配标记。','', '同一device上的公共广告ID相等只能支持同设备关联候选；账户作用域需单独契约。IP/NAT/家庭网络不是个人。哈希联系方式仍可匹配，不是匿名；请求/事件/机会ID不是用户ID。']
(R/'72_设备标识与身份标识完整清单.md').write_text('\n'.join(inventory)+'\n',encoding='utf-8')
report=['# 72号：第三方SDK身份关联能力矩阵','', '2026-11-20。归档实数103 AAR、67源码包已逐哈希记录；不以SDK数量作为新增成果。不重复下载已验证版本，只核验既有调用链及新增官方身份服务契约。','', '| SDK/服务 | 版本/材料 | 当前可证能力 | 等级 | 分析范围及未证 |','|---|---|---|---|---|']
for x in catalog:report.append(f"| {x['sdk']} | {x['versions']} | {x['identity_capability']} | {','.join(x['evidence_stages']) or 'UNKNOWN'}；{','.join(x['evidence_ids'])} | {x['analysis_status']}；{x['limits']} |")
report+=['','新增E4以官方明确链接/合并/身份解析契约为准：Mixpanel、Amplitude、Branch、Firebase的开发者user-ID能力不能转移为Axon/Vector事实；LiveRamp/UID2也不能自动套用两家所有流量。','', 'Mintegral/Vungle/Pangle/Chartboost虽有归档或目录，本轮没有足够证据给它们填完整生产图谱；这是明确分析缺口，不能把UNKNOWN改成没有能力。全部版本存在证据见[ARCHIVE_INVENTORY](identity72-experiments73/ARCHIVE_INVENTORY.json)，能力逐项见[机器矩阵](identity72-experiments73/SDK_CAPABILITY_MATRIX.json)。','', '每项调用链有源路径/哈希，文档有URL/摘录。所有实际生产匹配与Axon/Vector消费均未证。只要没有明确赋值、返回映射或服务契约，就不因字段同名建立跨SDKjoin。']
(R/'72_第三方SDK身份关联能力矩阵.md').write_text('\n'.join(report)+'\n',encoding='utf-8')
print('fields',len(fields),'sdk groups',len(catalog))
