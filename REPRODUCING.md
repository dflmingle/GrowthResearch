# 复现与核验

## 发布包核验

在仓库根目录执行：

~~~sh
python -X utf8 tools/verify_publication.py
~~~

不联网、不加载SDK、不训练模型；检查原件哈希、JSON/CSV、Python语法、报告数量、证据图及发布禁入项。

## 离线边界测试

建议Python 3.11/3.12：

~~~sh
python -m pip install -r requirements-research.txt
python -m unittest discover -s auction/model -p "test_*.py" -v
python -m unittest discover -s ltv/model -p "test_*.py" -v
~~~

进入prediction-validation/后执行：

~~~sh
python -m unittest discover -s tests -v
~~~

这些测试核验合成竞价、隔离与会计/时点门控，不证明厂商效果。不要批量运行采集、生成报告或历史校验脚本：它们可能需要未公开的本地证据，或写入固定历史目录。

## 后续自主身份图谱工程

MVP、LTV lab、E01和E02保留原源码、参数和实际运行结果。各README中的原始命令面向完整研究工作区，裁剪仓库未包含全部缓存、原数据和旧机器路径；缺少时应保留原STOP，不伪造原件、不删除保护检查。

先读[能力总览](identity-graph-capability-review/README.md)，核对正式运行manifest、源码SHA256及失败记录。本次发布核验不重新训练或重跑模型；完整重放须在新工作区合法补齐依赖，不能覆盖原prepare和历史结果。

E01/E02未接入lab，不存在统一端到端验收。E02 ACK仅限同进程内存假sink，不证明外部交付、多进程一致性、持久恢复或真实删除。合成预测不是现实LTV增益、机会估值或ROAS。

## 66/67号零售实验

历史脚本、协议、数据质量、切分、客户隔离、环境及统计区间保留在public-experiments/round66和round67。

原脚本使用历史Windows根目录，不应在归档目录直接运行。请从[UCI官方页面](https://archive.ics.uci.edu/dataset/352/online+retail)自行取得ZIP并遵守CC BY 4.0。预期SHA256：

~~~text
f5385cbb54bbebf7196389109c6b0621faab0c304e3702548165e71c84aede8b
~~~

以67号为例，使用全新且位于仓库外的目录：

~~~sh
python -X utf8 tools/reproduce_retail67.py --data /path/to/online-retail.zip --run-dir /path/to/new-retail67-run
~~~

入口验证数据哈希，复制必要历史参照，仅将新目录中的67号脚本根路径改为相对定位。归档源代码、模型、协议、参数及结果不修改；新脚本记录自己的新哈希，不能冒充历史原运行。新运行只是已知固定实验的复现，不是新的独立测试。

数据时区、到达时间和真实零消费仍未知；0标签仅指源文件内无正向购买记录。零售实验不能证明手游LTV、迁移、安装前排序或广告ROAS。
