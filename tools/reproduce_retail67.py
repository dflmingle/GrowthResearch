"""Reproduce fixed retail67 in a fresh external sandbox, without downloads."""
from pathlib import Path
import argparse
import csv
import hashlib
import json
import shutil
import subprocess
import sys

REPO = Path(__file__).resolve().parents[1]
EXPECTED = "f5385cbb54bbebf7196389109c6b0621faab0c304e3702548165e71c84aede8b"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--run-dir", type=Path, required=True)
    args = parser.parse_args()
    data, run = args.data.resolve(), args.run_dir.resolve()
    if not data.is_file() or hashlib.sha256(data.read_bytes()).hexdigest() != EXPECTED:
        parser.error("Original UCI ZIP SHA256 does not match the registered source")
    if run.exists() or run == REPO or REPO in run.parents:
        parser.error("Use a nonexistent directory outside this repository")
    run.mkdir(parents=True)
    with (REPO / "publication/ORIGINAL_FILE_MANIFEST.csv").open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    for row in rows:
        rel = Path(row["path"])
        needed = (
            (len(rel.parts) == 1 and rel.name[:2].isdigit() and int(rel.name[:2]) <= 67)
            or rel.as_posix().startswith("public-experiments/round66/")
            or rel.as_posix() in {
                "EVIDENCE_INDEX.md", "prediction-system/EVIDENCE_GRAPH.json",
                "public-experiments/audit/ASSET_VERIFICATION.json",
            }
        )
        if needed:
            dst = run / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(REPO / rel, dst)
    raw = run / "public-experiments/audit/retail352.download"
    raw.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(data, raw)
    original = REPO / "public-experiments/round67/run67.py"
    script = run / "public-experiments/round67/run67.py"
    script.parent.mkdir(parents=True, exist_ok=True)
    source = original.read_text(encoding="utf-8")
    old = "ROOT=Path(r'D:\\GrowthResearch')"
    if source.count(old) != 1:
        raise RuntimeError("Unexpected historical script structure")
    script.write_text(source.replace(old, "ROOT=Path(__file__).resolve().parents[2]"), encoding="utf-8")
    (run / "PORTABLE_RUN_NOTICE.json").write_text(json.dumps({
        "original_script_sha256": hashlib.sha256(original.read_bytes()).hexdigest(),
        "portable_script_sha256": hashlib.sha256(script.read_bytes()).hexdigest(),
        "only_script_change": "ROOT derives from sandbox script path",
        "archived_outputs_overwritten": False,
        "purpose": "Known fixed experiment reproduction, not a new independent test",
    }, indent=2) + "\n", encoding="utf-8")
    subprocess.run([sys.executable, "-X", "utf8", str(script)], cwd=run, check=True)


if __name__ == "__main__":
    main()
