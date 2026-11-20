"""Local metadata-only inventory. No row data, network, model or SDK access."""
from pathlib import Path
import csv,hashlib,json,datetime

ROOT=Path(__file__).resolve().parent
PARENT=ROOT.parent
def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()
def load(path):return json.loads(path.read_text(encoding='utf-8-sig'))
def save(path,obj):path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

SOURCES=[
 'identity-graph-ltv-lab/REAL_DATA_ADMISSION.md',
 'identity-graph-ltv-lab/PREREGISTRATION.json',
 'identity-graph-ltv-lab/EXPERIMENT_SUMMARY.md',
 'identity-graph-mvp/DATABASE_CONTRACTS.md',
 'identity-graph-mvp/LTV_FEATURE_ADMISSION.md',
 '68_DATASET_CATALOG.csv','68_DATASET_LICENSE_AUDIT.md',
 '69_实验准入最终判断.md','public-experiments/round69/ADMISSION_EIGHT_GATES.csv',
 '69_Uken数据获取与准入审计.md','69_Unity交易数据来源审计.md','69_MAG游戏经营数据审计.md',
 'game-industry69/DATASET_ADMISSION.csv','game-industry69/SOURCE_CATALOG.md',
 '70_真实游戏数据新增来源审计.md','71_Uken数据授权最终申请包.md',
 '72_真实游戏数据获取进展.md','access72/ACCESS_ROUTES.json',
 '73_数据许可及质量审计.md','identity72-experiments73/DATASET_ADMISSION.json',
 '77_最终判断与停止条件.md','77_生产身份图谱工程证据矩阵.csv',
 '78_身份图谱最小生产证据契约.md','78_证据验收与升级规则.md',
 '78_Axon证据获取路径.md','78_Vector证据获取路径.md','78_最小行动方案与停止条件.md',
 'server-identity-reference/AXON_VECTOR_GAP_MATRIX.csv',
 'server-identity-reference/与Axon_Vector已证证据的差距矩阵.md',
 'acquisition78/ADAPTER_SPEC.json'
]

def main():
    if (ROOT/'PRESERVATION_BASELINE.json').exists():raise SystemExit('Refusing to replace historical freeze')
    # Only hashes of historical files are streamed; no record formats parsed.
    prior=load(PARENT/'identity-graph-ltv-lab/PRESERVATION_BASELINE.json')
    added={}
    for name in ['identity-graph-mvp','identity-graph-ltv-lab','engineering76','server-identity-reference']:
        for path in (PARENT/name).rglob('*'):
            if path.is_file():added[path.relative_to(PARENT).as_posix()]=sha(path)
    for path in PARENT.iterdir():
        if path.is_file() and (path.name.startswith(tuple(f'{i:02d}_' for i in range(79))) or path.name in ['EVIDENCE_INDEX.md','EVIDENCE_GRAPH.json']):
            added.setdefault(path.relative_to(PARENT).as_posix(),sha(path))
    failures=[p for p,h in prior.items() if not (PARENT/p).is_file() or sha(PARENT/p)!=h]
    if failures:raise SystemExit('Historical baseline mismatch; do not replace it: '+str(failures))
    baseline=dict(added);baseline.update(prior)
    save(ROOT/'PRESERVATION_BASELINE.json',baseline)
    save(ROOT/'SOURCE_REUSE_CATALOG.json',[dict(id=f'REUSE{i:02d}',path=name,sha256=sha(PARENT/name),
       evidence_type='EXISTING_LOCAL_REPORT_OR_METADATA',new_external_evidence=False,records_parsed=False) for i,name in enumerate(SOURCES,1)])
    # Matrix consists of reviewed metadata facts and explicitly conditional routes.
    rows=[]
    def add(id,name,kind,owner,url,license,identity,links,times,labels,lifecycle,quality,next_input,route,refs):
        rows.append(dict(source_id=id,name=name,source_kind=kind,rights_holder=owner,original_url=url,
          existing_license_and_purpose=license,device_account_app_scope=identity,authorized_cross_app_or_device_links=links,
          event_received_available_time=times,mature_D1_D7_D30_labels=labels,deletion_revocation_retention=lifecycle,
          coverage_quality_independent_audit=quality,minimum_new_input=next_input,authorization_route_status=route,
          metadata_review='GO_LOCAL_ONLY',real_record_processing='STOP',real_graph_gain_training='STOP',
          C_graph_Axon='UNKNOWN',C_graph_Vector='UNKNOWN',D='UNKNOWN',source_refs=refs,
          external_recheck_this_round=False,personal_records_read_this_round=False))
    add('RD01','第一方发行方两App受控协作（候选方案，非已取得数据）','CONDITIONAL_NOT_A_DATASET',
      '需同时有权授权源App、目标App、认证关系、经济账本的主体；未确认','NONE_VERIFIED',
      '无书面许可；需明确模型训练、跨App用途、受控执行和输出审核','拟用App安装/设备/账号，禁止默认person',
      '未取得；仅可由运营方认证且授权的账号关系，不要求自然人ID',
      '未取得；需要三时点与历史特征快照','未取得；必须含全安装分母、真实退款和水位',
      '未取得；逐sink与训练快照处置待签认','无已确认合作方；完整分母与关系真值均待提供',
      '权利人确认+无个人值的schema/覆盖证明+受控方案书面答复','HOLD_NO_CONFIRMED_PARTNER',
      'identity-graph-ltv-lab/REAL_DATA_ADMISSION.md;78_最小行动方案与停止条件.md')
    add('RD02','Uken SFU2015','REAL_GAME_RESTRICTED','2015现行保管人和授权主体未确认',
      'https://raw.githubusercontent.com/nathanesau-academic/ukencompetition/master/README.md',
      '原参与者明确不能上传；未获本申请主体的许可或NDA','约300k聚合行；设备/安装/账号作用域未核验',
      '无已证跨App/跨设备合法关系','有部分日期描述；逐事件接收/可用时间未核验',
      '缩放金额/窗口/退款/币种未知；不能认定D1/D7/D30成熟金额',
      '留存、退出、删除和用途约束未取得','文件未取得；零值/退出/漏采及独立审计缺失',
      '先确认2015文件是否保留、权属、字典、缩放与单/多游戏关系','HOLD_ROUTING_ONLY_NO_SEND',
      'GI69D01;GI69S_uken_participant;71_Uken数据授权最终申请包.md;access72/ACCESS_ROUTES.json')
    add('RD03','Age of Ishtaria','REAL_GAME_PAPER_NO_RAW','历史研究机构Yokozuna Data；现行转授权未确认',
      'https://arxiv.org/abs/1811.12799',
      '论文公开不授予原始玩家数据使用权','单游戏研究；player key的安装/账号作用域未取文件核验',
      '无已证多App或跨设备关系','论文覆盖2014-09-24至2017-05-01；可用时间未核验',
      '真实IAP研究；本项目无D1/D7/D30成熟标签文件','未知',
      '无完整安装分母/零收入/水位证书，未获数据',
      '由机构路由确认权利人和留存；再审时间、全分母和许可','HOLD_ROUTING_ONLY_NO_SEND',
      'GI69D04;GI69S_ageishtaria;L72S12;72_真实游戏数据获取进展.md')
    add('RD04','Unity Many Faces of Monetisation','REAL_IAP_PRIVATE','Unity；原研究受机构法律协议限制',
      'https://doi.org/10.1145/3582927',
      '原作者不能分享或协助第三方获取；本项目无新协议','2873游戏内局部付费用户键；非全安装',
      '论文明确不同游戏之间不能关联；不能自行恢复',
      '2020-08-01至2022-04-16交易时间；接收/可用时点未公开',
      'IAP按日汇率换USD；仅付费者，无本项目可用成熟全安装标签','未获本项目授权的生命周期契约',
      '真实大规模付费样本；无零收入玩家/IAA；公开R是合成占位',
      '仅Unity新书面受控协议可重启；不能向作者索取受限副本','STOP_NO_VERIFIED_OPEN_APPLICATION',
      'GI69D02;GI69S_unity_paper;69_Unity交易数据来源审计.md;72_真实游戏数据获取进展.md')
    add('RD05','MAG五游戏日级面板线索','UNRESOLVED_PRIMARY_SOURCE','准确论文/数据权利方未定位',
      'https://www.maginteractive.com/',
      '数据许可未确认','仅任务提供日级国家/平台/游戏字段；不是已核验玩家ID',
      '聚合日面板即使取得也不包含已证个人关系','原论文/时期/可用时间未知',
      '奖励广告次数/标价/购买次数不等于收入标签','未知','不能唯一对应原论文和数据包',
      '准确题名/DOI/作者原件；聚合面板不能默认升为个人任务','STOP_NEEDS_PRIMARY_IDENTITY',
      'GI69D03;GI69S_mag_site;69_MAG游戏经营数据审计.md;70_真实游戏数据新增来源审计.md')
    add('RD06','Google Flood-It! BigQuery demo','OBFUSCATED_GAME_DEMO','Google/项目权利人；数据条款需另核',
      'https://developers.google.com/analytics/bigquery/app-gaming-demo-dataset',
      '文档许可不是数据处理许可；未核验本用途','user_pseudo_id文档定义；无实际稳定性核验',
      '单游戏的Android/iOS不是两个App产品或已证跨设备关系',
      '文档114天；actual received_at/available_at与观察水位未核验',
      '混淆/占位金额，不能由event_value_in_usd推为真实IAA/IAP',
      '未知','只有文档；本轮不查询Cloud行数据',
      '权利方确认真实金额、数据许可、全分母和合法关系；否则不适配本任务','STOP_VALUE_AND_LINKS_UNVERIFIED',
      'DS68-01;GI69D06;68_DATASET_CATALOG.csv;game-industry69/DATASET_ADMISSION.csv')
    add('RD07','Gamelytics Mobile Analytics Challenge','GAME_CANDIDATE_UNVERIFIED','Kaggle上传者debs2x；原运营方未核验',
      'https://www.kaggle.com/datasets/debs2x/gamelytics-mobile-analytics-challenge',
      '上传者声明Apache2；真实来源及原权利人授权未证','uid/user_id关系未有原契约',
      '无多游戏/跨设备合法映射','reg/auth有时间；A/B金额缺事件/可用时点',
      '累计revenue未证币种、退款、窗口和真实交易','未知','仅文件目录元数据；real-world-inspired不证真实',
      '原运营方和schema/金额/观察契约；不凭上传者许可直接训练','STOP_ORIGINAL_PROVENANCE',
      'DS68-04;68_DATASET_CATALOG.csv')
    add('RD08','TalkingData Mobile User Demographics','BEHAVIOR_PROXY_UNACQUIRED','TalkingData/Kaggle竞赛',
      'https://www.kaggle.com/competitions/talkingdata-mobile-user-demographics/data',
      '规则正文未取得；不登录代接受或取镜像','设备ID/App关系待实际许可字段核验；非person',
      '设备-App潜在行为关系不构成跨设备同人真值','仅网页壳；时间与可用时点未核验',
      '任务年龄/性别，不是收入标签','未知','无已核验数据压缩包',
      '许可和访问条件实质变化才恢复；即使取得也不直接满足收入任务','STOP_NO_REPEAT_DOWNLOAD',
      '73_数据许可及质量审计.md;identity72-experiments73/DATASET_ADMISSION.json')
    add('RD09','Criteo Attribution Modeling for Bidding','REAL_AD_CONVERSION_NOT_REVENUE','Criteo AI Lab',
      'https://ailab.criteo.com/criteo-attribution-modeling-bidding-dataset/',
      'CC BY-NC-SA4.0；申请主体NC资格未确认','dataset uid，不证明设备/账号/个人跨设备作用域',
      '无已证跨App/跨设备身份真值','30天展示+未来30天转化；不支持任意完整成熟时间外切分',
      'binary conversion，不是金额；cost/cpo为变换成本','匿名化不自动授权本用途；生命周期未知',
      '采样已展示广告；不是安装全分母，未取行数据',
      '仅许可和时间条件变化才恢复代理任务；收入任务仍需新真实金额源','STOP_PROXY_AND_LICENSE',
      '73_数据许可及质量审计.md;identity72-experiments73/DATASET_ADMISSION.json')
    add('RD10','Complete Journey','REAL_RETAIL_LIMITED_LEDGER','84.51°来源；作者R包发行',
      'https://github.com/bradleyboehmke/completejourney',
      'R包声明CC0；不替代身份/完整观察/原账本认证','household_key是家庭，不是自然人/账号；门店与SKU不是独立App',
      '无设备/账号/跨App合法关系','作者重映射日历且人工构造秒；无真实received/available',
      'sales_value非顾客实付；货币/退款及真实日历D1/D7/D30未证',
      '家庭入退样/漏采未知','69号较68号有更新：加工日历/删日；仅受限发布账本可研究',
      '原始时间/观察spell和经济账本；此方向不替代游戏图谱','STOP_FOR_CURRENT_TARGET',
      'DS68-06;69_实验准入最终判断.md;public-experiments/round69/ADMISSION_EIGHT_GATES.csv')
    add('RD11','REES46 Jewelry','REAL_PURCHASE_RELEASE_INCOMPLETE','REES46/原始作者',
      'https://www.kaggle.com/datasets/mkechinov/ecommerce-purchase-history-from-jewelry-store',
      '官方免费使用双署名声明；再分发不默认许可','69已恢复13字段；user_id稳定性/短行版本未知',
      '无跨店/跨设备授权映射；不得和electronics数字键join',
      'event_time有；收到/可用时点及观察完整性未知',
      'price非已证净成交额；币种/退款和成熟窗口不足','未知',
      '5352条键/金额缺失；2589重复；不能凭分布解释原因',
      '权利方短行、键作用域、净额与观察证据；不再泛搜同源副本','STOP_FOR_CURRENT_TARGET',
      'DS68-07;69_实验准入最终判断.md;public-experiments/round69/ADMISSION_EIGHT_GATES.csv')
    add('RD12','REES46 Electronics','REAL_PURCHASE_RELEASE_INCOMPLETE','REES46/原始作者',
      'https://www.kaggle.com/datasets/mkechinov/ecommerce-purchase-history-from-electronics-store',
      '免费使用双署名声明；不推定跨域身份使用权','user_id缺失78.58%；稳定和重置未知',
      '无跨店/设备授权关系','1970异常及2020版本范围；收到/可用时点未知',
      'price缺失/货币/付款/退款未证，不能形成完整成熟收入','未知',
      '675重复及异常原因未解释；删除异常不能制造完整集',
      '原业务生成日志/字段语义/观察分母；不自行修复成GO','STOP_FOR_CURRENT_TARGET',
      'DS68-08;69_实验准入最终判断.md;public-experiments/round69/ADMISSION_EIGHT_GATES.csv')
    add('RD13','BPID Identity Deduplication','SYNTHETIC_IDENTITY_BENCHMARK','AWS/Amazon Science',
      'https://zenodo.org/records/13932202','Apache2.0元数据；仅合成匹配基准',
      '合成档案对；不能与任何真实用户连接','仅合成真值/人工标对；没有真实玩家关系',
      '无纵向事件时间','无真实金额/安装标签','不涉及本任务真实身份生命周期',
      '73已执行合成基准；完整ZIP哈希可复核，但不证真实增益',
      '不能通过新增授权把合成样本变真；本轮不重复实验','STOP_NOT_REAL_DATA',
      '73_数据许可及质量审计.md;identity72-experiments73/DATASET_ADMISSION.json')
    add('RD14','Criteo Sponsored Search Conversion Log','REAL_ATTRIBUTED_SALES_NOT_PLAYER_LTV','Criteo AI Lab',
      'https://ailab.criteo.com/criteo-sponsored-search-conversion-log-dataset/',
      'CC BY-NC-SA4.0；用途资格未确认','user_id/partner_id文档，持续性与作用域未文件核验',
      'partner_id不是合法个人跨产品关系真值','文档90天采样点击和转化延迟；available未知',
      'SalesAmountInEuro是归因广告主销售额；非玩家完整IAP/IAA',
      '未知','点击选择偏差，无完整安装/用户消费分母；未取行数据',
      '只可能另立归因销售额代理研究，不适配当前身份图谱收入问题','STOP_FOR_CURRENT_TARGET',
      'DS68-05;68_DATASET_CATALOG.csv')
    with (ROOT/'01_真实数据来源及授权可行性矩阵.csv').open('w',encoding='utf-8-sig',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    save(ROOT/'CURRENT_READINESS.json',dict(as_of_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
      scope='LOCAL_EXISTING_EVIDENCE_REVIEW_ONLY',reviewed_entries=len(rows),conditional_non_dataset_routes=1,
      qualifying_real_graph_gain_datasets=0,real_training='STOP',authorization_preparation='GO_LOCAL_ONLY',
      external_contact='HOLD_NO_SEND_INSTRUCTION_OR_COMPLETE_APPLICANT',new_production_evidence=0,
      C_graph_Axon='UNKNOWN',C_graph_Vector='UNKNOWN',D='UNKNOWN',production_forensics='STOP',
      source_revalidation='NO_NEW_SEARCH_OR_EXTERNAL_CHECK',evidence_strength='EXISTING_REPORTS_AND_METADATA',
      no_real_records_read=True,no_real_model_training=True,no_external_requests=True,
      preserved_files=len(baseline)))
    print(json.dumps(dict(status='METADATA_DESIGN_ONLY',entries=len(rows),protected_files=len(baseline),qualified=0)))

if __name__=='__main__':main()
