# 本地交付保全记录（不包含于合作方审核ZIP）

本目录只用于内部来源、哈希和交付核验。合作方审核包partner-review-kit.zip使用严格白名单，仅20份问卷/Schema/边界/判定/方案/待确认问题与总览文件；不会包含本目录、研究历史、代码、基线或个人记录。

SOURCE_REUSE.json复用上轮六项材料和状态；PRESERVATION_BASELINE.json保护既有研究/MVP/lab/76程序及上轮审计。只对旧文件流式SHA256，不解析真实身份/交易行。

VALIDATION.json的PASS仅验证本轮文档、模板、ZIP与历史哈希一致，绝不授权访问、训练或证明生产事实。PARTNER_KIT_MANIFEST.json列出审核包逐文件哈希，ARTIFACT_MANIFEST.json覆盖新目录交付。

核验/重打包命令：

```powershell
Set-Location D:\GrowthResearch\two-app-partner-readiness
C:\Users\89trillion\anaconda3\python.exe -X utf8 verify_package.py
```

首次生成脚本build_templates.py拒绝覆盖基线及原始模板，不应重跑。核验脚本不导入MVP、SDK或第三方依赖，不联网，不训练。任何未来实际处理必须另有明确授权和执行任务。

保持C_graph.Axon=UNKNOWN、C_graph.Vector=UNKNOWN、D=UNKNOWN，原生产取证STOP。
