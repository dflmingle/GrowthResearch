# 合成实验汇总（非Axon/Vector表现）

各指标为3个seed的均值；完整seed范围与配对变化在summary.json。召回以实际出价分数pInstall×预测LTV排名，评价对象为全部留出集已安装样本。install_only的条件LTV是常数，其条件LTV排名仅为行序打破平局，不具识别意义；不将该指标用于模型优势比较。

| 分布 | 模型/场景 | 出价分数Top10%召回 | 价值预测/实际 | 分箱校准误差 | 实现D28 ROAS | 预算利用 |
|---|---|---:|---:|---:|---:|---:|
| diffuse | behavior_removed | 32.50% | 1.025 | 12.37% | 8.809 | 100.00% |
| diffuse | context_behavior | 33.62% | 0.990 | 8.76% | 10.043 | 99.19% |
| diffuse | context_behavior_identity | 43.16% | 1.003 | 8.21% | 10.335 | 99.51% |
| diffuse | context_identity | 34.13% | 1.007 | 10.21% | 9.383 | 98.97% |
| diffuse | context_ltv | 15.07% | 0.996 | 14.09% | 8.704 | 99.47% |
| diffuse | identity_removed | 34.38% | 1.020 | 10.03% | 9.552 | 100.00% |
| diffuse | install_only | 12.56% | 0.993 | 6.97% | 8.553 | 99.37% |
| diffuse | privacy_limited | 24.97% | 1.022 | 8.85% | 8.387 | 100.00% |
| diffuse | wrong_links_30pct | 40.53% | 0.985 | 12.60% | 10.133 | 98.63% |
| heavy_tail | behavior_removed | 41.64% | 1.084 | 22.45% | 16.849 | 100.00% |
| heavy_tail | context_behavior | 21.18% | 0.956 | 29.03% | 17.926 | 97.72% |
| heavy_tail | context_behavior_identity | 42.17% | 0.940 | 17.96% | 20.750 | 98.62% |
| heavy_tail | context_identity | 40.65% | 0.927 | 20.57% | 18.720 | 98.15% |
| heavy_tail | context_ltv | 10.80% | 0.953 | 39.64% | 14.948 | 98.19% |
| heavy_tail | identity_removed | 22.55% | 0.927 | 24.82% | 16.379 | 100.00% |
| heavy_tail | install_only | 11.14% | 0.943 | 16.80% | 15.148 | 98.15% |
| heavy_tail | privacy_limited | 20.32% | 0.973 | 28.70% | 12.935 | 100.00% |
| heavy_tail | wrong_links_30pct | 34.97% | 0.906 | 24.78% | 19.872 | 98.41% |
| identity_null | behavior_removed | 13.51% | 1.032 | 13.23% | 6.198 | 100.00% |
| identity_null | context_behavior | 36.28% | 0.991 | 4.96% | 8.036 | 100.00% |
| identity_null | context_behavior_identity | 37.16% | 0.992 | 5.30% | 8.032 | 99.83% |
| identity_null | context_identity | 13.38% | 1.003 | 11.94% | 6.940 | 100.00% |
| identity_null | context_ltv | 14.25% | 1.005 | 10.39% | 6.920 | 100.00% |
| identity_null | identity_removed | 37.17% | 0.994 | 4.82% | 7.964 | 100.00% |
| identity_null | install_only | 10.49% | 0.998 | 5.53% | 6.899 | 100.00% |
| identity_null | privacy_limited | 21.72% | 1.005 | 8.05% | 6.656 | 100.00% |
| identity_null | wrong_links_30pct | 36.91% | 0.992 | 5.65% | 8.039 | 99.89% |
