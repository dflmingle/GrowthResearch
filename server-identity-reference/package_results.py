"""Package the completed documentary design without running any algorithm tests."""
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parent.parent;D=Path(__file__).resolve().parent
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
v=load(D/'VALIDATION.json');assert v['status']=='PASS'
s=load(D/'STATUS.json')
summary=f'''# 服务端身份解析参考架构研究完成说明

已完成[六项交付](README.md)：技术路线、开源许可、参考架构、关系生命周期规则、图谱/LTV接口和Axon/Vector证据差距。

新增核验4个固定提交的开源项目（Splink MIT、dedupe MIT、RecordLinkage BSD-3-Clause、Feast Apache-2.0），19项逐行原文证据，42份公开文档/源码/法律/论文GET响应。许可只覆盖相应文件/项目范围，依赖和示例数据不自动放行；论文PDF仅本地阅读，不据此取得再分发或数据使用授权。

自主设计含7组件、8条技术路线、14条关系/冲突/撤销/删除规则、20项尚未执行的验收设计。所有字段是拟议契约，不是平台真实schema；没有原型或统计效果数字。关键取舍是typed实体、显式命名空间、认证账号不升级自然人、概率候选不硬闭包、双时态和consumer_available_at、撤销epoch与派生特征清理，以及接收/消费/active决策分层。

公开证据仍不能连通“身份解析输出→指定Axon/Vector实际接收→指定价值模型非空读取”。第三方组件能力、Unity账号或Exchange、Adjust传输入口不能拼成该生产链。12行差距矩阵逐项说明所缺原件；没有新增可升级厂商证据，也没有新的合格真实跨设备/游戏收入测试数据。

**静态保全核验{v['passed']}/{v['check_count']} PASS**：原件/摘要哈希、引用行号、许可/commit元数据、设计表和链接一致性，历史153份编号文件、76产物、官方样本与Adjust审计原件保持。索引和主图仅追加本轮研究：8节点/8边/31来源，旧308/362/678对象及旧元数据不改。

这些检查不是匹配准确率、延迟、删除传播、LTV增益或生产行为验证。未启动SDK/解析器/特征服务/模型，未提交身份、访问真实第三方个人记录或请求生产广告/身份接口。76号程序不改不重跑，不创建79号。

**C_graph.Axon=UNKNOWN；C_graph.Vector=UNKNOWN；D=UNKNOWN；原生产取证STOP。** 下一步自主工程可另行验证本地契约；厂商取证只能等待权利方可复核的匿名接收/模型读取/决策trace或明确授权沙箱，不能以参考实现代替生产证明。

复核命令：`python -X utf8 server-identity-reference/validate.py`。执行范围是文档与保全检查。extract_paper.py只用于本地重现纸面文本抽取，未运行任何论文算法。
'''
(D/'完成说明.md').write_text(summary,encoding='utf-8')
rows=[]
for p in sorted(D.rglob('*')):
    if not p.is_file() or '__pycache__' in p.parts or p.name=='ARTIFACT_MANIFEST.json':continue
    rows.append(dict(path=p.relative_to(R).as_posix(),bytes=p.stat().st_size,sha256=sha(p),
                     redistribution='NOT_CLEARED_PAPER_READING_COPY' if p.name.startswith('bayesian-paper-pdf') or p.name=='PAPER_PAGES.json' else 'SEE_SOURCE_SPECIFIC_LICENSE'))
(D/'ARTIFACT_MANIFEST.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(packaged_files=len(rows),validation=v['status'],static_checks=v['check_count'],production_forensics=s['production_forensics'])))
