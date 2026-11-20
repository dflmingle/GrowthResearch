"""Offline integrity checks for the curated publication; no SDK execution."""
from pathlib import Path
from datetime import datetime, timezone
import ast
import csv
import hashlib
import json
import re
import sys
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    errors = []
    files = sorted(p for p in ROOT.rglob("*") if p.is_file() and
                   ".git" not in p.relative_to(ROOT).parts and
                   "__pycache__" not in p.relative_to(ROOT).parts)
    with (ROOT / "publication/ORIGINAL_FILE_MANIFEST.csv").open(encoding="utf-8", newline="") as f:
        original = list(csv.DictReader(f))
    with (ROOT / "publication/SDK_ARTIFACTS.csv").open(encoding="utf-8", newline="") as f:
        sdks = list(csv.DictReader(f))
    for row in original:
        p = ROOT / row["path"]
        if not p.is_file() or sha(p) != row["sha256"]:
            errors.append("Copied original changed: " + row["path"])
    for row in sdks:
        p = ROOT / row["path"]
        if not p.is_file() or sha(p) != row["sha256"] or not row["source_url"].startswith("https://"):
            errors.append("SDK integrity/origin failed: " + row["path"])
    graph = json.loads((ROOT / "prediction-system/EVIDENCE_GRAPH.json").read_text(encoding="utf-8-sig"))
    for key in ["nodes", "edges", "sources"]:
        ids = [x["id"] for x in graph[key]]
        if len(ids) != len(set(ids)):
            errors.append("Duplicate graph IDs: " + key)
    patterns = {
        "private_key": r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
        "github_token": r"\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{50,})\b",
        "google_api_key": r"\bAIza[0-9A-Za-z_-]{30,}\b",
        "aws_access_key": r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b",
        "jwt": r"\beyJ[A-Za-z0-9_-]{12,}\.[A-Za-z0-9_-]{12,}\.[A-Za-z0-9_-]{12,}\b",
        "url_credentials": r"https?://[^/\s:@]+:[^/\s@]+@",
    }
    forbidden = {".apk", ".xapk", ".apks", ".aab", ".dex", ".so", ".exe", ".dll",
                 ".xlsx", ".xls", ".download", ".parquet", ".pem", ".p12", ".pfx", ".keystore"}
    counts = dict(python=0, json=0, csv=0)
    alternate_log_encodings = []
    gaps = []
    for p in files:
        rel = p.relative_to(ROOT).as_posix()
        if p.suffix.lower() in forbidden or p.name.startswith(".env"):
            errors.append("Excluded material in publication: " + rel)
        if p.stat().st_size >= 100_000_000:
            errors.append("GitHub file size limit: " + rel)
        if p.suffix not in {".md", ".py", ".json", ".csv", ".java", ".txt", ".sql", ".diff", ".log", ".jsonl"}:
            continue
        try:
            content = p.read_text(encoding="utf-8-sig")
        except UnicodeError:
            # PowerShell historical stdout is UTF-16 with an explicit BOM.
            # Preserve original bytes/hashes; do not silently replace characters.
            if p.suffix == ".log" and p.read_bytes()[:2] in {b"\xff\xfe", b"\xfe\xff"}:
                try:
                    content = p.read_text(encoding="utf-16")
                    alternate_log_encodings.append(dict(path=rel, encoding="utf-16-bom", sha256=sha(p)))
                except UnicodeError:
                    errors.append("Invalid UTF-16 log: " + rel)
                    continue
            else:
                errors.append("Invalid text encoding: " + rel)
                continue
        for kind, pattern in patterns.items():
            if re.search(pattern, content):
                errors.append("Credential pattern " + kind + " in " + rel)
        try:
            if p.suffix == ".py":
                ast.parse(content, filename=rel)
                counts["python"] += 1
            elif p.suffix == ".json":
                json.loads(content)
                counts["json"] += 1
            elif p.suffix == ".csv":
                list(csv.reader(content.splitlines()))
                counts["csv"] += 1
        except (SyntaxError, ValueError, csv.Error) as e:
            errors.append("Invalid file " + rel + ": " + str(e))
        if p.suffix == ".md":
            for target in re.findall(r"\]\(([^)]+)\)", content):
                target = target.strip("<>").split("#")[0]
                if not target or target.startswith(("http:", "https:", "mailto:", "app:")):
                    continue
                target = unquote(target)
                absolute = bool(re.match(r"[A-Za-z]:[/\\]", target)) or target.startswith("/")
                status = "machine_absolute_path" if absolute else "not_in_publication"
                if absolute or not (p.parent / target).exists():
                    gaps.append(dict(document=rel, target=target, status=status))
                    if rel in {"README.md", "REPORTS.md", "REPRODUCING.md",
                               "THIRD_PARTY_NOTICES.md", "ThirdPartySDKs/README.md"}:
                        errors.append("Broken navigation link in " + rel + ": " + target)
    gapfile = ROOT / "publication/LOCAL_REFERENCE_GAPS.csv"
    with gapfile.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["document", "target", "status"], lineterminator="\n")
        writer.writeheader()
        writer.writerows(gaps)
    reports = sorted(p for p in ROOT.glob("*.md") if re.match(r"\d\d_", p.name))
    current_scope = ROOT / "publication/CURRENT_SCOPE.json"
    expected_reports = json.loads(current_scope.read_text(encoding="utf-8"))["numbered_reports"] if current_scope.exists() else 71
    if len(reports) != expected_reports:
        errors.append("Numbered report count differs from frozen publication scope")
    original_report_paths = [x["path"] for x in original if re.match(r"(?:[0-5][0-9]|6[0-7])_.*\.md$", x["path"])]
    if len(original_report_paths) != 71:
        errors.append("Original 00-67 report inventory changed")
    result = dict(
        status="PASS" if not errors else "FAIL",
        checked_utc=datetime.now(timezone.utc).isoformat(),
        numbered_reports=len(reports), original_files_verified=len(original),
        sdk_release_files_verified=len(sdks), sdk_bytes=sum(int(x["bytes"]) for x in sdks),
        parsed_files=counts, historical_local_reference_gaps=len(gaps),
        production_requests=0, sdk_execution=False, raw_datasets_included=False,
        source_workspace_modified=False, errors=errors,
        alternate_log_encodings=alternate_log_encodings,
        scope="Publication integrity and navigation, not independent production/model validation",
    )
    (ROOT / "publication/VALIDATION.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
