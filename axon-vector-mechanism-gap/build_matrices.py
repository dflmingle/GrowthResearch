"""Build scoped evidence and engineering-gap matrices; no simulation or training."""
from pathlib import Path
import csv,hashlib,json,datetime
ROOT=Path(__file__).resolve().parent
PARENT=ROOT.parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,obj):p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def csvsave(p,rows):
    with p.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def main():
    if (ROOT/'MECHANISM_EVIDENCE.csv').exists():raise SystemExit('Refusing to replace mechanism assessment')
    evidence=[]
    def add(id,vendor,product,mechanism,status,sourceid,url,file,version,location,observed,explanation,alternative,missing,guidance):
        evidence.append(dict(id=id,vendor=vendor,product=product,mechanism=mechanism,status=status,
          source_ids=sourceid,original_url=url,source_file=file,source_sha256=sha(PARENT/file),version_or_time_scope=version,
          location=location,direct_observation=observed,technical_interpretation=explanation,alternative_explanation=alternative,
          missing_evidence=missing,independent_implementation_guidance=guidance,new_vendor_mechanism=False,
          production_graph_consumption='UNKNOWN',D='UNKNOWN'))
    add('MG01','AppLovin','Axon partner postback','身份输入','CONFIRMED','L71D01',
      'https://help.adjust.com/en/partner-setup/applovin','axon/adjust-applovin.txt','cached official partner documentation; version not stated','L165-L249',
      '官方可配置出站字段包含idfa/gps_adid/idfv/android_id及上下文、revenue_usd/is_organic等；并非每次都有',
      '支持有作用域的MMP→伙伴输入契约','仅配置能力，可能未启用或因隐私/来源缺字段',
      '指定Axon接收回执、resolver及模型字段映射','可借鉴typed namespace和可用性；不证明身份匹配')
    add('MG02','AppLovin','Web CAPI/Pixel','第一方网站输入','CONFIRMED','IG72S06;IG72P01-10',
      'https://support.applovin.com/en/growth/promoting-your-websites/api/conversion-api','72_AppLovin身份图谱逆向.md',
      '72 snapshot; underlying public contract referenced','Pixel/CAPI的跨网站与账户链',
      '网站cookie/点击标记与商家user_id、联系方式、交易输入有公开契约/历史审计',
      '可存在第一方转化归属与匹配','同商家转化归属，不必连接手游自然人或跨设备',
      '商家输出→游戏身份解析→Axon指定价值模型的实际链','仅参考来源分区、用途隔离，不复制受限实现')
    add('MG03','AppLovin','MAX13.6.4 / Axon SDK1.3.4','客户端标识能力','CONFIRMED','IG72C01-09/20',
      'local historical evidence; original artifact provenance in 72 catalog','72_AppLovin身份图谱逆向.md',
      'MAX13.6.4;Axon1.3.4;NO_NEW_ANALYSIS','MAX与Axon客户端能证什么',
      '旧报告有OS广告ID/App Set ID/本地GUID与多字段构包；本轮不重扫或新反编译',
      '多标识可能供后端关联','也可只是单设备上下文、计量或频控',
      '具体版本可分析许可、实际接收、跨App/server mapping','仅引用历史有界事实；许可未明确不重新分析核心')
    add('MG04','AppLovin','Axon','关系构建','INFERRED','MG01;MG02;MG03',
      'existing source contracts only','74_身份特征进入价值模型的证据.md','existing scope only','两条尚未闭合的数据链',
      '存在多标识输入，但无可核验解析输出','技术上可建立映射，不是已建立的事实',
      '直接上下文建模、同App历史或聚合/共享参数同样解释公开现象',
      'resolver版本、关系grain/quality、输出及产品接收','只指导可选接口，不指定厂商确定性/概率算法')
    add('MG05','Unity','Player Accounts / Authentication','账号关联','CONFIRMED','IG72S02/03;IG72C10-19/28',
      'https://docs.unity.com/en-us/authentication/unity-player-accounts.md','72_Unity身份图谱逆向.md',
      'Authentication3.9.0 historical audit; org/project contract','账号提供者和显式身份映射',
      '组织级player pool、项目PlayerId、显式link/unlink和冲突契约',
      '账号namespace与认证关系可跨游戏/设备','账号控制关系不是自然人一对一，也不等于广告模型输入',
      'UPA→Ads/Vector接收与特征实际消费','适合账号/设备/安装分粒度、显式冲突拒识的参考')
    add('MG06','Unity','Unity Exchange / LiveRamp','第三方广告身份激活','CONFIRMED','IG72S05;IV74S01-06',
      'https://unity.com/blog/unity-exchange-rampid-addressable-buying-mobile-gaming','72_Unity身份图谱逆向.md',
      '2026-04-02 official Exchange announcement;US/Canada','RampID的真实契约边界',
      'Exchange支持范围化RampID受众激活，依赖接收伙伴支持',
      '身份服务结果可以服务于该库存的需求方激活','Exchange需求方使用，不代表Vector自营价值模型读取',
      '特定输出成功、Exchange→Vector桥和模型读取','可借鉴接收产品/namespace/结果类型分离，不能归属Vector')
    add('MG07','Unity','Player Accounts / Authentication','关系更新','CONFIRMED','IG72S03;IG72C14',
      'https://docs.unity.com/en-us/authentication/identity-management.md','72_Unity身份图谱逆向.md',
      'public identity contract;no new SDK scan','账号提供者和显式身份映射',
      '显式unlink、已链接其他玩家时冲突、凭证/profile生命周期',
      '认证关系需可撤销且不能静默合并','只影响账号服务；广告侧缓存和图谱更新可能不同',
      'Vector图谱TTL、删除水位、重建/拆分生产契约','参考账号关系撤销与命名空间；不证明Vector更新机制')
    add('MG08','Unity','Unity Ads4.17 client','广告机会关联','CONFIRMED','L71C15-21;MA60S25',
      'existing official SDK historical evidence','71_Unity机会ID与事件关联.md',
      'Ads4.17.0;historical audit only','HeaderBiddingToken/trackingToken/operative event sections',
      '机会ID、广告对象、事件快照和重试路径有历史代码证据',
      '广告生命周期可关联','广告对象/机会关系不是跨设备用户关系或经济展示唯一键',
      '服务端token join、Vector值特征、经济唯一键','参考分离请求/展示/事件/经济账本的键')
    for id,vendor,product,mechanism,sourceid,missing in [
      ('MG09','AppLovin','Axon','生产图谱更新','G04/G09;EC78S01','图谱TTL/冲突/撤销/删除/重建的实际版本化契约与执行'),
      ('MG10','Unity','Vector','生产图谱更新','G04/G09;EC78S01','Vector的关系TTL/冲突/撤销/删除水位，不能以UPA替代'),
      ('MG11','AppLovin','Axon','图谱特征服务与消费','G07/G08;77;78','关系输出→feature_group/graph/model版本→非空有效读取'),
      ('MG12','Unity','Vector','图谱特征服务与消费','G05/G07/G08;77;78','UPA/Exchange等输出→Vector实际接收→当时可用特征→模型读取')]:
        add(id,vendor,product,mechanism,'UNKNOWN',sourceid,'NO_NEW_PRIMARY_RECORD',
          'server-identity-reference/AXON_VECTOR_GAP_MATRIX.csv','existing gaps G01-G12','corresponding row',
          '没有本项目可核验的指定模型生产链','不能选择闭源实现','可能无需个人图谱而使用群体/共享参数',
          missing,'可按独立通用机制设计，不可称复制厂商实现')
    add('MG13','AppLovin','Axon/Axon2','价值预测与竞价用途','CONFIRMED','MA60S01/02/04',
      'https://www.applovin.com/en/blog/applovin-business-model','model-architecture/public/al-business.txt',
      '2026-02-02 public article;cached original','L31-L34',
      '官方说明预测未来多日价值分布并用于实时资本分配；非游戏offer解释有特定scope',
      '产品级未来价值/决策用途有官方声明','上下文、同广告主历史、聚合或共享模型都可能实现',
      '目标手游具体任务/输入列、实际inference→active决策trace和独立消融',
      '参考标签窗口/预测输出与控制器分离，不能指定分布族或模型结构')
    add('MG14','Unity','Vector IAP D7/D28','价值预测与动态竞价用途','CONFIRMED','MA60S16/17',
      'https://unity.com/blog/d7-vs-d28-iap-roas-campaigns','model-architecture/public/unity-d7-d28.txt',
      '2026-06-25 article;cached original','L145-L176;L208-L223',
      '官方将D7/D28价值、动态竞价与cross-game patterns/aggregate cohorts连接',
      '产品级预测/出价用途成立；不是具体身份列消费','群体统计/共享参数与合法个人历史无法从文章区分',
      '特定特征组/时点/版本、个人关系结果和实际决策引用','参考同时保留群体/共享参数对照，禁止只靠效果反推图谱')
    add('MG15','AppLovin','Axon ad decision','实时return-goal用途','CONFIRMED','MA60S02/04',
      'https://www.applovin.com/en/blog/introducing-applovin-ads','model-architecture/public/al-introducing.txt',
      '2025-10-01 article;cached original','L27-L50',
      '官方说明实时评估展示并按return goals出价；跨业务增量部分为前瞻声明',
      '模型价值可用于实时决策的产品用途','不需要指定个人图谱；前瞻声明也不证共享已上线',
      '身份特征→指定模型inference→机会active决策原始引用','控制器与特征血缘分离；不自行实现厂商报价公式')
    csvsave(ROOT/'MECHANISM_EVIDENCE.csv',evidence)
    levels=[
      ('L1','身份输入','CONFIRMED','MMP→Axon伙伴可配置ID/上下文字段契约；实际收妥UNKNOWN','MG01/MG02/MG03',
       'UNKNOWN','CONFIRMED仅限邻接Unity Ads/UPA输入契约；Vector逐字段接收UNKNOWN','MG05/MG06/MG08'),
      ('L2','关系解析','UNKNOWN','多ID/商家事件不证明Axon的个人关系解析','MG04',
       'UNKNOWN','UPA账号/Exchange激活可确认，但Vector关系解析UNKNOWN','MG05/MG06'),
      ('L3','图谱更新','UNKNOWN','Axon TTL/冲突/撤销/重建执行未知；客户端隐私开关不替代','MG09',
       'UNKNOWN','UPA unlink不是Vector图谱更新契约','MG07/MG10'),
      ('L4','特征服务','UNKNOWN','无Axon graph output→feature接口/时点/实际读取','MG11',
       'UNKNOWN','无UPA/Exchange→Vector特征服务实际链','MG12'),
      ('L5','价值预测','CONFIRMED','官方多日价值分布用途；具体图谱输入、结构与增益未知','MG13',
       'CONFIRMED','官方D7/D28及cohort用途；具体个人历史输入未知','MG14'),
      ('L6','竞价消费','CONFIRMED','官方实时return-goal出价用途；图谱→单机会active trace未知','MG15',
       'CONFIRMED','官方动态bid及bid-time intelligence用途；图谱→单机会active trace未知','MG14')
    ]
    matrix=[]
    for id,level,a,ac,ar,v,vc,vr in levels:
        matrix.append(dict(level_id=id,level=level,Axon_status=a,Axon_scoped_claim=ac,Axon_evidence=ar,
          Vector_status=v,Vector_scoped_claim=vc,Vector_evidence=vr,
          CONFIRMED_scope='Documented contract/vendor product statement only unless explicitly scoped;not independent production audit',
          C_graph_Axon='UNKNOWN',C_graph_Vector='UNKNOWN',D='UNKNOWN'))
    csvsave(ROOT/'01_Axon_Vector机制差异矩阵.csv',matrix)
    candidates=[
      dict(rank=1,id='C01',mechanism='任务主体一致的账号/设备特征路由',potential_value='直接影响可用历史的粒度与共享设备选择偏差，真实收益未知',
        current_capability='MVP已有account/device/app_instance查询；lab只有device适配且多账号设备全拒绝',gap_type='FEATURE_ADAPTER_AND_EVALUATION',
        source_evidence='MG05/MG07;system.py:462-508;lab/adapter.py:6-29',difficulty='LOW_TO_MEDIUM',
        synthetic_test_feasibility='HIGH:复用现有API，只比较路由与期望账本，不训练',extra_authority='本地合成不需要真实数据；真实账号关联需授权和独立真值',
        evidence_confidence='CONFIRMED_LOCAL_CODE_AND_ADJACENT_ACCOUNT_CONTRACT;NOT_VECTOR',
        recommendation='DESIGN_MINIMUM_E01;NO_IMPLEMENTATION_THIS_ROUND',novelty='本轮具体适配差距，不是新厂商算法'),
      dict(rank=2,id='C02',mechanism='出队/重试时重新检查用途与权限epoch',potential_value='阻止旧身份包越过已撤销用途进入后续特征链；不直接提高预测准确率',
        current_capability='MVP有事务outbox与隐私控制；仅LOCAL_ONLY_PENDING，无dispatch-time状态机',gap_type='ASYNC_LIFECYCLE_ARCHITECTURE',
        source_evidence='Adjust AM15/16/20/22;MG07;system.py:171-183/426-427;schema.sql outbox',difficulty='MEDIUM',
        synthetic_test_feasibility='HIGH:本地假sink+调度器，复用policy.allowed，不开网络',extra_authority='本地合成可验证；真实接收/删除完成仍需权利方证据',
        evidence_confidence='CONFIRMED_ADJUST_STATIC_REFERENCE_AND_LOCAL_GAP;NOT_AXON_VECTOR',
        recommendation='DESIGN_MINIMUM_E02;NO_IMPLEMENTATION_THIS_ROUND',novelty='已有机制的未实现调度边界，不是厂商生产发现'),
      dict(rank=3,id='C03',mechanism='依赖感知且含负依赖的特征失效计划',potential_value='减少无关更新造成的缓存重算；先证明无漏失效再考虑延迟',
        current_capability='MVP所有graph/policy变更全局失效，read也查当前边/权限；安全但保守',gap_type='FEATURE_CACHE_ARCHITECTURE',
        source_evidence='system.py:173-183/462-538;MVP ARCHITECTURE;SIR feature-serving reference',difficulty='MEDIUM_TO_HIGH',
        synthetic_test_feasibility='HIGH_FOR_SHADOW_PLANNER:与强制新算oracle比较，含新边加入/到期无写入',extra_authority='合成规划器不需真实数据；生产性能/多机一致性未授权',
        evidence_confidence='CONFIRMED_LOCAL_GLOBAL_INVALIDATION;PROPOSED_OPTIMIZATION_NOT_VENDOR',
        recommendation='DESIGN_MINIMUM_E03_SHADOW_ONLY;DO_NOT_BYPASS_MVP_READ',novelty='新失效审计问题；并无Axon/Vector采用证明'),
      dict(rank=4,id='C04',mechanism='校准后的概率候选评分与拒识',potential_value='可能改善覆盖/误并权衡，但是否提升价值预测未知',
        current_capability='候选隔离已实现；没有真实评分模型或代表性校准',gap_type='DATA_AND_ALGORITHM',
        source_evidence='MG06;IV74S05;SIR01;lab confidence probes',difficulty='HIGH_WITHOUT_REAL_TRUTH',
        synthetic_test_feasibility='只能验证代码行为，不能估真实准确率；73已做基准，不重复',extra_authority='代表性合法关系真值、用途、独立测试',
        evidence_confidence='THIRD_PARTY_GENERIC_ONLY;AXON_VECTOR_UNKNOWN',
        recommendation='HOLD_NO_NEW_MODULE_NO_NEW_STATISTICAL_EXPERIMENT',novelty='既有未解决方向，非本轮新机制')
    ]
    csvsave(ROOT/'02_最值得复制的机制清单.csv',candidates)
    sources=[]
    for row in evidence:
        sources.append(dict(evidence_id=row['id'],original_url=row['original_url'],version=row['version_or_time_scope'],
          file=row['source_file'],sha256=row['source_sha256'],location=row['location'],new_vendor_mechanism=False))
    save(ROOT/'EVIDENCE_SOURCE_LINKS.json',sources)
    notes=json.loads((ROOT/'RELEASE_NOTES_REVIEW.json').read_text(encoding='utf-8'))
    for n in notes:
        n['novelty']='NO_NEW_IDENTITY_MECHANISM_OR_MODEL_MAPPING_IN_REVIEWED_NOTE'
        n['manual_review']='Read complete body, not only keyword hits; no SDK/core source fetched'
    save(ROOT/'RELEASE_NOTES_REVIEW.json',notes)
    save(ROOT/'STATUS.json',dict(status='DESIGN_AND_BOUNDED_PUBLIC_METADATA_REVIEW_COMPLETE',
       protected_files=json.loads((ROOT/'SCOPE.json').read_text())['protected_files'],
       new_public_metadata_responses=2,release_notes_reviewed=len(notes),new_vendor_mechanisms=0,new_C_graph_evidence=0,
       mechanism_evidence_rows=len(evidence),comparison_layers=len(matrix),ranked_candidates=len(candidates),
       minimum_experiments_designed=3,experiments_executed=0,models_trained=0,
       C_graph_Axon='UNKNOWN',C_graph_Vector='UNKNOWN',D='UNKNOWN',production_forensics='STOP',
       no_questionnaires=True,no_contacts=True,no_personal_data=True,no_new_sdk_functional_analysis=True))
    print(json.dumps(dict(evidence=len(evidence),layers=len(matrix),candidates=len(candidates),new_vendor_mechanisms=0)))

if __name__=='__main__':main()
