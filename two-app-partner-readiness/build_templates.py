"""Generate blank partner metadata forms and synthetic field examples only."""
from pathlib import Path
import csv,hashlib,json,datetime

ROOT=Path(__file__).resolve().parent
PARENT=ROOT.parent
AUDIT=PARENT/'identity-graph-real-data-audit'
def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()
def load(path):return json.loads(path.read_text(encoding='utf-8-sig'))
def save(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def csvsave(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def main():
    baseline_file=ROOT/'internal/PRESERVATION_BASELINE.json'
    if baseline_file.exists():raise SystemExit('Refusing to replace frozen baseline/templates')
    baseline=load(AUDIT/'PRESERVATION_BASELINE.json')
    for folder in [AUDIT,PARENT/'identity-graph-ltv-lab',PARENT/'identity-graph-mvp']:
        for path in folder.rglob('*'):
            if path.is_file():baseline.setdefault(path.relative_to(PARENT).as_posix(),sha(path))
    changed=[p for p,h in baseline.items() if not (PARENT/p).is_file() or sha(PARENT/p)!=h]
    if changed:raise SystemExit('Prior evidence mismatch: '+str(changed))
    save(baseline_file,baseline)
    sources=[
      '01_真实数据来源及授权可行性矩阵.csv','02_最小真实实验数据契约.md',
      '03_真实M0_M1_M2预注册方案.md','04_数据准入和STOP检查器设计.md',
      '05_Axon_Vector关键证据缺口及突破条件.md','06_下一步GO_HOLD_STOP决策.md',
      'PREREGISTRATION_MANIFEST.json','CURRENT_READINESS.json'
    ]
    save(ROOT/'internal/SOURCE_REUSE.json',[dict(path=(AUDIT/name).relative_to(PARENT).as_posix(),sha256=sha(AUDIT/name),
        use='EXISTING_CONTRACT_AND_GATE_REUSE_ONLY') for name in sources])
    rows=[]
    def field(group,name,type_,meaning,constraint,example):
        rows.append(dict(field_name=group+'.'+name,type=type_,semantics=meaning,constraints=constraint,synthetic_example=str(example)))
    def f(g,n,t,m,c,e):field(g,n,t,m,c,e)
    utc='2035-01-01T00:00:00Z'
    f('P0','package_ref','string','本次审核包引用','只用本包随机别名；不填客户或账号标识','syn:review:001')
    f('P0','controller_and_authority_refs','array<string>','两App控制权、保管人与授权链证明引用','双方/多方权利分别签认；只交文件索引不交用户清单','["syn:authority:A","syn:authority:B"]')
    f('P0','applicant_role_and_purpose_ref','string','申请主体、真实用途和商业属性文件','不默认学术或非商业资格','syn:purpose:UNCONFIRMED')
    f('P0','scope_apps_regions_people','object','App别名、地区、人员/角色范围','所有参与源/目标、处理方均须被涵盖','{"apps":["syn:app:A","syn:app:B"],"region":"syn:region","role":"syn:reviewer"}')
    f('P0','legal_basis_and_link_use_ref','string|null','跨App/跨设备关系的合法依据与允许用途','空值阻断图谱实验；匿名化本身不替代合法依据','syn:basis:NOT_APPROVED')
    f('P0','permissions','object<bool>','查验、解析、训练、扰动、导出、公开引用许可分别列出','不以一项许可代替全部；未批均false','{"inspect":false,"link":false,"train":false,"perturb":false,"export":false,"quote":false}')
    f('P0','permission_valid_from_to','object<utc|null>','授权用途生效半开区间','历史和当前用途分别核验；禁止事后补同意回填','{"from":null,"to":null}')
    f('P0','controlled_environment_ref','string|null','合作方受控环境及审批责任','不填写登录凭证/服务器密钥','syn:environment:PROPOSED_ONLY')
    f('P0','retention_deletion_review_ref','string|null','留存、撤销删除和逐sink责任文件','未签认不启动处理；包含训练产物','syn:lifecycle:UNCONFIRMED')
    f('P0','approval_status','enum','有权审核人的批准状态','UNKNOWN/PENDING/APPROVED/DENIED；模板不等于授权','UNKNOWN')
    f('P1','tenant_issuer_namespace_version','object','实体命名空间发行者、范围与版本','不能凭相同字符串跨命名空间合并','{"tenant":"syn:tenant","issuer":"syn:issuer","namespace":"syn:ns","version":"syn:v1"}')
    f('P1','app_alias_and_version','object','App业务别名和版本','App A/B须是独立产品范围；不交商业密钥','{"app":"syn:app:A","version":"syn:v1"}')
    f('P1','entity_grain','enum','实体粒度','ACCOUNT/DEVICE/APP_INSTANCE/PERSON/HOUSEHOLD各自分离；人级须另证','ACCOUNT')
    f('P1','entity_ref','string','源内随机实体引用','只能留合作方环境；不可逆联系信息；默认不导出','syn:account:001')
    f('P1','install_ref','string','App安装实例引用','(app,namespace,install_ref,epoch)唯一；重装另实例','syn:install:001')
    f('P1','install_at','utc','安装发生时间','需证明真实安装而非首次可见事件；UTC和误差另列',utc)
    f('P1','first_seen_at','utc','首次被观察到的时间','不替代安装时间或进入观察边界',utc)
    f('P1','reset_epoch','int64','设备/安装标识重置代次','非负；不绕过合法重置恢复关联',0)
    f('P1','reinstall_dedup_definition_ref','string','重装、重复安装及分母口径','规则在标签和测试预览前冻结','syn:install-rule:UNCONFIRMED')
    f('P2','edge_ref_revision','object','关系主键与修订','修订不可静默覆盖；候选不自动激活','{"ref":"syn:edge:001","revision":1}')
    f('P2','typed_endpoints','object','关系两端实体引用和粒度/namespace','禁止账号直接提升person或跨类型闭包','{"src":{"ref":"syn:account:001","grain":"ACCOUNT","ns":"syn:ns:A"},"dst":{"ref":"syn:device:001","grain":"DEVICE","ns":"syn:ns:B"}}')
    f('P2','source_target_apps','array<string>','跨App关系两端产品','独立App的合法使用范围须有权利人证明','["syn:app:A","syn:app:B"]')
    f('P2','relation_kind','string','账号登录、同设备、家庭等具体关系语义','类型受端点约束；不是自然人事实','syn:authenticated_account_device')
    f('P2','method_source_component_version','object','认证/解析依据、来源及组件版本','不能仅因字段存在就认定服务端匹配','{"evidence":"syn:assertion:001","component":"syn:resolver","version":"syn:v1"}')
    f('P2','purpose_scope_ref','string','该边允许用途与App/地区范围','引用P0，不能先读后mask','syn:purpose:NOT_APPROVED')
    f('P2','quality_kind_score_calibration','object','质量类型、分数及校准版本','未校准score不当概率；候选隔离','{"kind":"uncalibrated_score","score":0.5,"calibration":null}')
    f('P2','valid_from_to','object<utc|null>','业务有效时间','半开区间；valid_from不替代当时已知时间','{"from":"2035-01-01T00:00:00Z","to":null}')
    for name,meaning in [('observed_at','关系首次被系统观察'),('received_at','关系到达该系统'),('available_at','关系实际可供模型使用')]:
        f('P2',name,'utc',meaning,'分别提供；不晚于实际预测且附时钟误差',utc)
    f('P2','revoked_expired_deleted_effective','object<utc|null>','撤销/到期/删除禁止使用生效时点','null需说明未发生还是未知；未知不当未撤销','{"revoked":null,"expired":null,"deleted":null,"knowledge":"UNKNOWN"}')
    f('P2','status','enum','边状态','ACTIVE/CANDIDATE/CONFLICT/REVOKED；候选不得传递合并','CANDIDATE')
    f('P3','event_key_source_revision','object','行为来源内幂等主键','同键不同payload冲突拒绝；仅合作方内引用','{"event":"syn:event:001","source":"syn:app:A","revision":1}')
    f('P3','app_instance_ref','string','事件所属安装实例','引用P1；不能拿请求ID冒充安装键','syn:install:001')
    f('P3','event_type','string','行为类型定义','使用冻结字段字典；无内容文本或个人画像','syn:session_start')
    for name,meaning in [('occurred_at','行为实际发生'),('source_received_at','源系统接收'),('source_available_at','源系统实际可用')]:
        f('P3',name,'utc',meaning,'三时点独立记录；不能以导出时间倒填',utc)
    f('P3','revision_and_arrival_watermark_ref','string','迟到/修订及到账水位说明','可信原件或上界，缺失不猜测','syn:watermark:UNVERIFIED')
    f('P3','account_ref','string|null','合法账号归属，若适用','可缺；不能由共享设备自动赋账号','syn:account:001')
    f('P4','economic_key_source_app_revision','object','经济事实幂等键','与请求/机会/回调ID分离；修订不重复累加','{"key":"syn:cashflow:001","source":"syn:ledger","app":"syn:app:B","revision":1}')
    f('P4','event_and_install_refs','object','经济事件到目标安装的可核验归属','需独立映射依据；重装和历史退款口径冻结','{"event":"syn:event:001","install":"syn:install:001","basis":"syn:allocation-rule"}')
    f('P4','cashflow_kind','enum','IAP/IAA/REFUND/ADJUSTMENT','只含授权且真实采集类型；没有IAA不能填0','REFUND')
    for name,meaning in [('cashflow_at','经济现金流发生'),('received_at','账本事实到达'),('available_at','账本事实可用')]:
        f('P4',name,'utc',meaning,'按发生时间定标签，不按到达时间挪窗口',utc)
    f('P4','signed_amount_micros','int64','有符号实际金额，百万分之一货币单位','退款允许负；禁止强制裁0；金额非预测值或广告标价',-300000)
    f('P4','currency','string','金额ISO4217币种','缺币种不可合并；混币需冻结汇率规则','USD')
    f('P4','precision_gross_net_tax_definition_ref','string','真实金额、估算精度、税费及净额口径','估算ILRD需单列；不可冒充结算净收入','syn:money-definition:UNVERIFIED')
    f('P4','correction_and_refund_refs','object','技术修订链及退款原交易','修订替换同事实，退款另现金流；不能混用','{"corrects_revision":null,"refunds_transaction":"syn:purchase:001"}')
    f('P4','dedup_and_install_allocation_ref','string','多回调去重和安装归属证明','按真实经济事实，不以广告请求ID当账本主键','syn:dedup-rule:UNVERIFIED')
    f('P4','finality_watermark_ref','string','该金额窗口及修订完成的证书引用','仅有截止日期不等于成熟','syn:finality:UNVERIFIED')
    f('P5','roster_and_observation_unit_ref','string','完整安装名册及观察单位定义','不是仅付费者或成功匹配样本；不对外提交名册','syn:roster:INTERNAL_ONLY')
    f('P5','observation_start_end','object<utc>','入样/退出观察边界','不以首末交易代替','{"start":"2035-01-01T00:00:00Z","end":"2035-01-02T00:00:00Z"}')
    f('P5','coverage_intervals','array<object>','完整、缺采、退出区间及原因','COMPLETE需证据；无事件不自动零','[{"status":"MISSING","from":"2035-01-01T00:00:00Z","to":"2035-01-02T00:00:00Z","reason":"syn:unknown-gap"}]')
    f('P5','source_receiver_watermarks','object','各行为/收入源和接收系统的成熟水位','所有声明收入源均覆盖；缺源不填0','{"source_ref":"syn:source","certificate":"syn:watermark:UNVERIFIED"}')
    f('P5','arrival_lag_certificate','object','最大迟到/修订界及证明','现有协议要求L≤7天；未知或更长不得缩窗口凑数','{"max_days":null,"certificate":"syn:lag:UNVERIFIED"}')
    f('P5','denominator_reconciliation_ref','string','安装数/事件/经济账本及零值对账','需包含未匹配/零收入与退出，不导出个体','syn:reconciliation:UNVERIFIED')
    f('P5','label_definition_version','string','remaining/install标签及退款定义版本','两个窗口分开；现金流时间与修订规则固定','syn:label-v1-PROPOSED')
    f('P5','D1_D7_D30_maturity','object','三个窗口成熟证书及实际时点','未知保持UNKNOWN；未来时点示例不证真实成熟','{"D1":"UNKNOWN","D7":"UNKNOWN","D30":"UNKNOWN","certificate":"syn:maturity:UNVERIFIED"}')
    f('P6','bundle_feature_schema_version','object','时间点特征快照、组和schema版本','实际快照不可事后倒填','{"bundle":"syn:bundle:001","group":"syn:history","version":"syn:v1"}')
    f('P6','entity_app_scope','object','特征实体及源目标App粒度','设备/账号/人区分；只留合作方内','{"grain":"ACCOUNT","entity":"syn:account:001","apps":["syn:app:A","syn:app:B"]}')
    f('P6','graph_mapping_version','string','生成特征依赖的关系版本','须在预测时已存在且合法','syn:graph:001')
    f('P6','event_edge_lineage_refs','object','源事件和边修订引用','只指合法且当时可用来源；不导出明细血缘','{"events":["syn:event:001"],"edges":["syn:edge:001@1"]}')
    for name,meaning in [('source_max_observed_at','依赖最大观察时刻'),('source_max_available_at','依赖最大可用时刻'),('materialized_at','实际特征物化'),('consumer_available_at','模型消费系统实际可用'),('as_of','预测截止')]:
        f('P6',name,'utc',meaning,'逐依赖因果审计；未来可用不得入模',utc)
    f('P6','policy_epoch_gate_missing_reason','object','权限代次、门控和缺失原因','缺失不填真实0；授权未知则不读','{"epoch":0,"gate":"DENY","missing_reason":"syn:permission_unknown"}')
    f('P6','retention_invalid_after','object','特征保留期和禁止使用时点','撤销/删除后旧缓存及snapshot同样受限','{"retention_policy":"syn:policy:UNCONFIRMED","invalid_after":null}')
    f('P7','purpose_legal_basis_policy_version','object','生命周期的用途和合法依据版本','历史采集及当前训练都需覆盖','{"purpose":"syn:purpose","basis":"syn:basis:UNCONFIRMED","version":"syn:v1"}')
    f('P7','permission_effective_intervals','array<object>','同意或其他合法基础的生效/观察区间','不能只给当前同意boolean；后补不回填','[{"state":"UNKNOWN","effective_from":null,"effective_to":null,"observed_at":"2035-01-01T00:00:00Z"}]')
    f('P7','revocation_deletion_request_effective','object','请求与禁止继续使用生效时间','请求、法定/合同生效、传播完成分别记录','{"requested_at":null,"use_prohibited_at":null,"knowledge":"UNKNOWN"}')
    f('P7','reset_expiry_epoch','object','身份重置/到期/代次','不绕过退出、重置重新关联','{"reset_at":null,"expires_at":null,"epoch":0}')
    f('P7','sink_acknowledgements','array<object>','图/特征/缓存/快照/训练产物逐sink验收','未确认要明示；删除服务在线状态不等于模型遗忘','[{"sink":"syn:training-snapshot","status":"UNCONFIRMED","confirmed_at":null}]')
    f('P7','retention_exception_and_responsibility_ref','string','保留期限、例外、备份到期及执行/验收责任','不允许无限保留；责任人角色需签认','syn:retention-responsibility:UNCONFIRMED')
    f('P8','truth_unit_grain','enum','独立真值的pair/cluster实体粒度','不以模型分数或未来收入自证；不默认自然人','ACCOUNT_PAIR')
    f('P8','truth_and_annotation_ref','string','正负关系标注与独立依据','仅权利方内部；不给本方真实配对记录','syn:gold:INTERNAL_ONLY_UNVERIFIED')
    f('P8','sampling_frame_weights','object','抽样框、纳入概率和权重','需覆盖拒识、未匹配、共享设备和负例','{"frame":"syn:frame","inclusion_probability":null,"weight":null}')
    f('P8','annotation_time_uncertainty','object','标注时刻、不确定性和冲突','不强制模糊样本变确定真值','{"at":"2035-01-01T00:00:00Z","status":"UNKNOWN"}')
    f('P8','isolation_calibration_threshold_ref','string','关系质量训练/验证/测试隔离及阈值版本','先冻结质量阈值，再解封价值测试；不拿测试调阈值','syn:quality-plan:UNCONFIRMED')
    f('P8','independent_review_ref','string','独立复核与利益关系声明','供应方score不足；不能只挑成功匹配','syn:review:UNCONFIRMED')
    f('P9','source_original_location_ref','string','原件受控位置与获取责任','只交文档索引；不交后台URL/token/凭证','syn:original:CONTROLLED_ONLY')
    f('P9','original_sha256','string','原件一致性承诺','64小写hex；全零仅示例不证真实/完整','0'*64)
    f('P9','signer_authority_review_ref','string','出具权限、原件见证和独立审核依据','签名不等于事实都真，需说明查验路径','syn:attestation:UNVERIFIED')
    f('P9','transformation_missing_coverage_manifest','object','转换清单、缺字段/缺日志范围和记录覆盖','不拿选中成功记录推总体覆盖','{"transform":"syn:transform","missing":"syn:unknown-fields","coverage":"UNKNOWN"}')
    f('P9','environment_versions_clock_error_ref','string','环境、版本生效和跨系统时钟误差','生产/测试/回放分开；误差不明不扩大容差','syn:environment-clock:UNVERIFIED')
    f('P9','independent_reviewer_scope_ref','string','审核人角色、利益关系、实际见到和未见内容','不要求暴露私人联系方式；授权后内部实名签认','syn:reviewer-role:UNCONFIRMED')
    f('P9','inspection_export_quotation_permissions','object<bool>','查验/导出/引用分离','未经批准不能公开或通过匿名化绕过限制','{"inspect":false,"export":false,"quote":false}')
    csvsave(ROOT/'02_最小Schema审核模板.csv',rows)
    for group in [f'P{i}' for i in range(10)]:csvsave(ROOT/'schema'/f'{group}_字段审核模板.csv',[r for r in rows if r['field_name'].startswith(group+'.')])
    gate_specs=[
      ('RA00','权利与目的','Q1/Q2','P0','两App权利链、跨App用途、训练/输出授权','缺明确授权即STOP'),
      ('RA01','来源与真实性','Q1/Q6','P9','原件与签认权限、独立查验路径','未知则HOLD；原件矛盾STOP'),
      ('RA02','实体作用域','Q3','P1/P2','命名空间、设备/账号/安装/重装，禁止粒度升级','未明HOLD；跨人错误作用域STOP'),
      ('RA03','真实净收入语义','Q5','P4','真实金额、币种、精度、退款、修订与去重','未知则HOLD；代理/重复计费STOP'),
      ('RA04','全安装与覆盖','Q4','P1/P5','全名册、观察入退样、零与缺失、缺采对账','未知HOLD；缺失冒充零STOP'),
      ('RA05','可用时间因果','Q4','P2/P3/P6','源发生/接收/可用、物化、预测、时钟误差','未明HOLD；未来泄漏STOP'),
      ('RA06','合法关系与质量','Q2/Q3','P0/P2/P8','合法依据、认证真值、代表性抽样、阈值冻结','无合法关系依据即STOP；质量未证HOLD'),
      ('RA07','撤销删除保留','Q6','P7','当前/历史权限、逐sink、缓存/快照/模型责任','未知HOLD；失效后使用STOP'),
      ('RA08','成熟收入标签','Q5','P4/P5','D1/D7/D30现金流窗、水位和迟到/修订证明','无成熟标签即STOP'),
      ('RA09','时间和实体隔离','Q3/Q4','P1/P2/P5/P8','绝对时窗、审计簇隔离、独立测试保管','未知HOLD；跨阶段泄漏STOP'),
      ('RA10','预注册功效公平','Q4/Q5/Q6','P0/P5/P6/P8','冻结参数、样本功效、同样本/标签/预算','未知HOLD；测试调参或不公平STOP'),
      ('RA11','审计与聚合输出','Q6','P9','负结果、样本流图、聚合门槛、导出/引用审批','未知HOLD；无权输出STOP')
    ]
    gates=[]
    for id,title,q,p,requirements,rule in gate_specs:
        gates.append(dict(gate_id=id,gate_name=title,question_refs=q,package_refs=p,minimum_evidence=requirements,
          partner_answer='UNANSWERED',evidence_document_alias='PENDING_NO_RECORDS',applicable_scope='UNCONFIRMED',
          reviewer_role='UNASSIGNED',verification_status='UNKNOWN',gate_decision='STOP' if id in ['RA00','RA06','RA08'] else 'HOLD',
          missing_or_conflict='尚未收到合作方答复/核验，不代表存在违规',remediation_owner_role='PARTNER_TO_CONFIRM',
          review_due_or_expiry='UNSET',reviewer_signoff_ref='NONE',decision_rule=rule))
    csvsave(ROOT/'04_真实实验准入判定表.csv',gates)
    save(ROOT/'04_准入结论填写模板.json',dict(schema='partner-metadata-review-1.0',status='UNFILLED_TEMPLATE',
      partner_submission_received=False,review_scope='METADATA_ONLY_NO_REAL_RECORDS',partner_alias=None,
      allowed_operations=['REVIEW_BLANK_DOCUMENTS_AND_SYNTHETIC_FIELD_EXAMPLES'],
      forbidden_operations=['REAL_RECORD_IMPORT','IDENTITY_LOOKUP','REAL_TRAINING','PRODUCTION_ADS','UNAPPROVED_EXPORT'],
      source_target_app_aliases=None,entity_scope=None,income_scope=None,
      explicit_authority_verified=False,legal_relationship_basis_verified=False,mature_labels_verified=False,
      all_RA00_RA11_verified=False,overall_experiment_decision='STOP',authorization_preparation='GO_LOCAL_ONLY',
      partner_response_state='HOLD',missing_authority=['controller chain','processing purposes','cross-App use'],
      missing_data_proofs=['timestamps and coverage','net revenue and maturity','relationship truth','lifecycle'],
      gate_evidence_refs={},not_applicable_signed_reasons={},partner_approver_role_and_signoff=None,
      research_method_reviewer_signoff=None,privacy_security_reviewer_signoff=None,
      reviewer_decision_utc=None,approved_scope_and_expiry=None,
      next_action='NO_SEND_NO_DATA_REQUEST;WAIT_FOR_EXPLICITLY_AUTHORIZED_NEXT_TASK',
      C_graph_Axon='UNKNOWN',C_graph_Vector='UNKNOWN',D='UNKNOWN',production_forensics='STOP'))
    save(ROOT/'internal/BUILD_SUMMARY.json',dict(created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
      schema_rows=len(rows),schema_columns=['field_name','type','semantics','constraints','synthetic_example'],
      packages=[f'P{i}' for i in range(10)],gates=12,protected_files=len(baseline),
      synthetic_examples_only=True,real_records_read=0,external_contacts=0,applications_sent=0,real_models_trained=0,
      C_graph_Axon='UNKNOWN',C_graph_Vector='UNKNOWN',D='UNKNOWN',production_forensics='STOP'))
    print(json.dumps(dict(schema_fields=len(rows),packages=10,gates=12,protected_files=len(baseline),actual_admission='STOP')))

if __name__=='__main__':main()
