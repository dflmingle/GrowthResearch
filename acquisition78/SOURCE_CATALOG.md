# 78号输入与规范来源目录

本轮没有新增外部材料或生产证据。12份已有输入全文在本地读取并哈希；这里只建立取证规范。既有官方披露的证明边界不变。

| 原始文件 | SHA256 | 既有证据编号 |
|---|---|---|
| [74_身份图谱生产证据.md](../74_身份图谱生产证据.md) | `7648073cd4dd67e62e58187e19a86d653e3d0b3e5011f311667e9a8732fecdc1` | 历史报告/矩阵；路径为原件定位 |
| [74_身份特征进入价值模型的证据.md](../74_身份特征进入价值模型的证据.md) | `c86e5c9100c6eda34b366f433f49d4ff63bf617ac7fa62f2745ddd30a4e05620` | 历史报告/矩阵；路径为原件定位 |
| [74_研究边界与停止条件.md](../74_研究边界与停止条件.md) | `96016fc995dcf74e1648466b4fe00e6a928882547e3125ae89bf44c18cba75b0` | 历史报告/矩阵；路径为原件定位 |
| [75_黑盒可识别性矩阵.csv](../75_黑盒可识别性矩阵.csv) | `78ee31b309162d8b4511998a95b23f104a61895dbd956cb9496649911508114f` | BB75S02 |
| [76_身份图谱证据链工程验证.md](../76_身份图谱证据链工程验证.md) | `cc8e6343d8c2d30cdccf5eebcc0d9d0d63f3ee91a7fb465e9c1dbb4bec70e3c8` | 历史报告/矩阵；路径为原件定位 |
| [engineering76/mock76/auditor.py](../engineering76/mock76/auditor.py) | `280acfc8094cc5afedecf7386a6af36cdada46c5c722dfcf6e9503ea42ca3f15` | EN76S04 |
| [engineering76/mock76/io.py](../engineering76/mock76/io.py) | `7c4e75c2a43e2ca5bdd09724a35fcc6f30af371e9d19bfdc6c8e9b3f0277d705` | 历史报告/矩阵；路径为原件定位 |
| [engineering76/mock76/safety.py](../engineering76/mock76/safety.py) | `047b6e6aac5970bf8b6bda96be4245b580c535376d09df573106fec22d6facac` | EN76S05 |
| [engineering76/README.md](../engineering76/README.md) | `f128dc960da5216ad757a8e39a4895c65f2f5287279ca3c70b17a3dede797a34` | 历史报告/矩阵；路径为原件定位 |
| [77_生产身份图谱工程证据矩阵.csv](../77_生产身份图谱工程证据矩阵.csv) | `595d7a0de3a3fe13da05e0f46811d7f4adebce65d4249ee3f8cb35fe4c1f0367` | 历史报告/矩阵；路径为原件定位 |
| [77_最终判断与停止条件.md](../77_最终判断与停止条件.md) | `80ca4ebfddad6efca94a6925348d8dfa1c5ba4adcb5ca3228da9d714e6f23f70` | 历史报告/矩阵；路径为原件定位 |
| [77_关键证据缺口与竞争解释.md](../77_关键证据缺口与竞争解释.md) | `a05eb79c52e3f82dd8d1ec9d34000eeda07472a7ee02869e71f93822cc75b21b` | 历史报告/矩阵；路径为原件定位 |

## 76号审计器精确定位

| 文件 | 行 | 原文 |
|---|---|---|
| engineering76/mock76/auditor.py | 9 | `def _audit(packet):` |
| engineering76/mock76/auditor.py | 12 | `if packet.get('view')!='complete_local_audit':return result('UNIDENTIFIABLE','OUTPUT_OR_REDACTED_VIEW_INSUFFICIENT')` |
| engineering76/mock76/auditor.py | 14 | `if not rows or not verify(rows):return result('INVALID_EVIDENCE','HASH_CHAIN_OR_SEQUENCE_INVALID')` |
| engineering76/mock76/auditor.py | 18 | `if rows[0]['data'].get('environment')!='offline-mock':return result('UNIDENTIFIABLE','NO_REAL_PLATFORM_ATTESTATION')` |
| engineering76/mock76/auditor.py | 52 | `if set(decision['data']['feature_receipts'])!={x['seq'] for x in features}:return result('UNIDENTIFIABLE','FEATURE_DECISION_LINK_MISSING')` |
| engineering76/mock76/auditor.py | 58 | `if not d.get('actual_read') or not d.get('nonnull') or not p:return result('UNIDENTIFIABLE','NO_ACTUAL_NON_NULL_READ')` |
| engineering76/mock76/auditor.py | 59 | `if d['model_version']!=decision['data']['model_version'] or d['materialized_at']>t:return result('INVALID_EVIDENCE','MODEL_OR_AVAILABILITY_MISMATCH')` |
| engineering76/mock76/auditor.py | 70 | `if not e:return result('UNIDENTIFIABLE','SOURCE_RECEIPT_MISSING')` |
| engineering76/mock76/auditor.py | 74 | `if not permitted('source-app',device,p['time'],p['seq']) or not permitted('target-app',device,p['time'],p['seq']):return result('INVALID_EVIDENCE','UNAUTHORIZED_PROVENANCE_READ')` |
| engineering76/mock76/auditor.py | 92 | `def assess_observable(packet):` |
| engineering76/mock76/auditor.py | 111 | `def hypothesis_verdict(hypothesis,observation_verdict):` |

以上代码位置支持“76号只能证明本地fixture”的方法边界，不支持真实平台图谱存在。78号拟议来源真实性、授权、跨系统产品/模型及生命周期检查尚未实现为生产适配器。

保全：00—77共148份编号文件；76/77旧manifest覆盖的1217项文件与两个共享索引/主图的冻结基线分别验证。共享文件按要求追加，不拿新哈希与旧版本混比。
新增主图来源EC78S01—05均为研究者设计文件，URL为空、生产标记为false。不能把规范或文档校验PASS升级为C_graph或D。
