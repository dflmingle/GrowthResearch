"""Package completed static review; does not call the SDK or any network."""
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parent.parent;D=Path(__file__).resolve().parent
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
v=load(D/'VALIDATION.json');assert v['status']=='PASS'
status=load(D/'STATUS.json')
out=['# 来源目录与复核范围',
 '原始JAR未改；源码副本按归档成员字节核对，MIT LICENSE保留在每个版本目录。正式发布日期未确认，不能以HTTP Last-Modified替代。完整逐方法证据见CODE_EVIDENCE.json，附源码SHA及调用方法/行号；没有SDK执行证据。',
 '| 样本 | 版本 | 原始下载URL | 本地归档 | SHA256 |','|---|---|---|---|---|']
for s in load(D/'SAMPLES.json'):
    out.append(f"| {s['sample_id']} | {s['version']} | {s['official_download_url']} | {s['path']} | `{s['sha256']}` |")
out.extend(['\n## 本轮新增公开法律响应','只有以下5次GET，没有新SDK下载或广告/身份服务请求。所有URL、时间及重定向见license-review/FETCH_MANIFEST.json。',
 '| ID | 原始URL | HTTP | SHA256 |','|---|---|---|---|'])
for s in load(D/'license-review/FETCH_MANIFEST.json'):
    out.append(f"| {s['id']} | {s['url']} | {s['status']} | `{s['sha256']}` |")
out.extend(['\n## 复用证据',
 '[首轮许可与版本证据](../official-samples-audit/LICENSE_EVIDENCE.json)、[版本元数据](../official-samples-audit/VERSION_PROVENANCE.json)、[47样本目录](../official-samples-audit/ACQUIRED_SAMPLE_CATALOG.csv)。没有改写首轮报告或旧结论。',
 '本轮代码辅助器只做读取、定位、文本差分、哈希和文档写入；初始词法定位有泛型返回方法盲区，补定位已经显式写入CODE_EVIDENCE。不能用本工具证明完整调用图或无其他服务端机制。'])
(D/'SOURCE_CATALOG.md').write_text('\n\n'.join(out)+'\n',encoding='utf-8')
report=f'''# Adjust源码机制验证完成报告

限定的三份MIT源码静态分析完成：111个选定Java条目，22项发现、61行逐版本证据、{status['code_evidence_records']}条方法/字段范围引用，76个文件配对中24项变化或新增。

已交付[机制图](Adjust身份与归因机制图.md)、[差分](三版本源码差分.md)、[生命周期](身份标识生命周期表.md)、[已证实/未知清单](已证实机制与服务端未知清单.md)、[自主Resolver最小设计](自主IdentityResolver最小设计建议.md)、[授权与测试条件](下一阶段授权和测试条件.md)。另有[具体版本许可复核](license-review/版本许可复核.md)、[来源目录](SOURCE_CATALOG.md)、[代码行与哈希](CODE_LOCATIONS.md)和完整JSON/CSV原件。

关键结论：本地UUID是应用私有SDK状态；OS广告ID、AppSet、AndroidID和外部字符串不能自动升级为自然人图谱。安装/会话/事件通过上下文参数关联；event token/seq不是经济事件全局唯一ID。去重是默认10条的本地窗口，队列推进不等于远端业务成功。GDPR请求、optout响应、暂停与本地teardown不是同一个删除阶段。

5.7.0加入类白名单反序列化、FB显式控制和TPS结果链；5.8.1增加细分标识禁读、修正retryCount恢复键及retryIn分支。未发现可在这些选定客户端链中证明的跨设备账号解析或服务端图谱算法；这不排除未知服务端能力。

静态核验：**{v['passed']}/{v['check_count']} PASS**。覆盖归档/成员/源码哈希、方法原文与行号、差分重算、引用和许可响应、00—78的153份编号文件、76产物与首轮审计保全、主图旧对象及索引前缀。PASS不代表SDK行为、OS权限/重置、网络交付、服务器删除或生产模型测试通过。

初次核验曾因输出文件VALIDATION.json尚未创建而出现1项自引用链接失败；已修正检查器的首次运行依赖，重新核验通过，未调整机制结论或降低证据门槛。

没有启动SDK、没有新SDK下载、没有生产请求/身份查询，没有真实身份或预测收益数字；仅5次公开法律响应。MAX/LevelPlay与适配器许可继续HOLD，未做其功能分析。未修改76、不创建79；主索引和证据图仅追加本轮有界研究，旧对象保持。

**C_graph.Axon=UNKNOWN；C_graph.Vector=UNKNOWN；D=UNKNOWN；原生产取证STOP。** 下一步优先取得OS作用域契约及权利方的匿名去重/删除/接收schema，或另行授权纯本地自主实现测试；不得用Adjust传输入口替代Axon/Vector消费证据。
'''
(D/'完成报告.md').write_text(report,encoding='utf-8')
manifest=[]
for p in sorted(D.rglob('*')):
    if not p.is_file() or '__pycache__' in p.parts or p.name=='ARTIFACT_MANIFEST.json':continue
    manifest.append(dict(path=p.relative_to(R).as_posix(),bytes=p.stat().st_size,sha256=sha(p)))
(D/'ARTIFACT_MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(packaged_files=len(manifest),verification=v['status'],checks=v['check_count']),ensure_ascii=False))
