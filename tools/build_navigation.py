"""Build report and SDK navigation from the curated files, without source edits."""
from pathlib import Path
from collections import defaultdict
import csv
import re

ROOT = Path(__file__).resolve().parents[1]
reports = sorted(p for p in ROOT.glob("*.md") if re.match(r"\d\d_", p.name))
lines = [
    "# 研究报告目录", "",
    "完整保留历史文件名与编号。同号不同专题分别列出；后续核验优先于旧版假设。", "",
    "| 编号 | 报告 |", "|---|---|",
]
for p in reports:
    lines.append(f"| {p.name[:2]} | [{p.stem[3:]}]({p.name}) |")
lines += ["", "证据入口：[索引](EVIDENCE_INDEX.md)、[主图](prediction-system/EVIDENCE_GRAPH.json)。",
          "最新实验：[实验索引](public-experiments/EXPERIMENT_INDEX.md)。"]
(ROOT / "REPORTS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

with (ROOT / "publication/SDK_ARTIFACTS.csv").open(encoding="utf-8", newline="") as f:
    sdks = list(csv.DictReader(f))
groups = defaultdict(lambda: {"versions": set(), "count": 0, "path": None})
for row in sdks:
    g = groups[(row["vendor"], row["sdk"])]
    g["versions"].add(row["version"])
    g["count"] += 1
    g["path"] = (Path("..") / Path(row["path"]).parent.parent).as_posix()
lines = [
    "# 已入库的第三方SDK", "",
    "本目录及跨SDK目录包含实际官方原包，不只是清单。",
    "所有发行文件在[SDK_ARTIFACTS.csv](../publication/SDK_ARTIFACTS.csv)逐项记录路径、SHA256、来源和许可。", "",
    "| 厂商 | SDK | 版本 | 文件数 |", "|---|---|---|---:|",
]
for (vendor, name), g in sorted(groups.items()):
    lines.append(f"| {vendor} | [{name}]({g['path']}) | {', '.join(sorted(g['versions']))} | {g['count']} |")
lines += [
    "",
    "包括AAR、JAR、POM及Unity TGZ。sources JAR不一定包含完整实现，部分SDK采用POM聚合/轻量包装；原件存在不代表完整依赖闭包。",
    "",
    "保留原归档，不上传重复反编译副本。许可证以各包、POM与[第三方声明](../THIRD_PARTY_NOTICES.md)为准；未为闭源SDK重新授予开源许可。",
]
for number in ["14", "47", "53"]:
    report = next(p for p in reports if p.name.startswith(number + "_"))
    lines.append(f"- [{report.stem}](../{report.name})")
(ROOT / "ThirdPartySDKs/README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"Navigation built: {len(reports)} reports, {len(groups)} SDK families, {len(sdks)} artifacts")
