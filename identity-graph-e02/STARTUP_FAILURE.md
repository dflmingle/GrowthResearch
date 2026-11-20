# 启动阶段失败记录

首次执行 `python -X utf8 run.py` 在测试开始前退出：

```text
ImportError: cannot import name 'Fixture' from 'fixtures'
(D:\GrowthResearch\identity-graph-e01\fixtures.py)
```

原因：只读导入 E01 adapter 时其 common 模块会把依赖路径放到 sys.path 前部，后续裸 fixtures 导入误指向 E01。修复只发生在 E02 的 e02_common.py：导入完成后恢复 E02 路径优先级。没有执行任何验收用例，不能将本次启动记为 PASS；没有修改 E01。
