# 文档核验说明

首次核验发现README指向核验器自己的VALIDATION.json，而该文件要到检查结束才写出，导致首次运行报一条自引用缺失。该失败原件保留在[attempt-001](validation-runs/attempt-001.json)。

修复仅限新目录核验工具：在检查前生成IN_PROGRESS状态的结果文件，完成后才写PASS/FAIL，并保存前次结果。没有改动数据资格、历史代码、历史结果或预期门槛。该工具不读取真实数据记录、不训练、不检查真实关系是否准确。

正式结果见[VALIDATION.json](VALIDATION.json)。PASS只表示当前文档/引用/历史哈希完整，不代表任何来源获得真实数据准入或C_graph/D升级。
