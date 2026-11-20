"""Publish selected research and original official SDK releases; never alter source."""
from pathlib import Path
import argparse
import csv
import hashlib
import json
import re
import shutil
import tarfile
import zipfile

ROOTS = {
    "auction", "axon", "client-growth", "core-insights", "cross-sdk",
    "identity-graph", "ltv", "model-architecture", "nongame",
    "prediction-system", "prediction-validation", "public-evidence",
    "public-experiments", "public-research", "ThirdPartySDKs", "vector",
}
NESTED = {
    "auction": {"model"}, "ltv": {"model"}, "vector": {"model"},
    "model-architecture": {"round61-63", "round62", "final64"},
    "public-evidence": {"round66"},
    "public-experiments": {"round66", "round67", "audit"},
    "prediction-validation": {"data_contracts", "experiments", "results", "src", "tests"},
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def selected(rel):
    parts = rel.parts
    name = rel.name.lower()
    if rel.suffix.lower() not in {".md", ".json", ".csv", ".py", ".java", ".txt"}:
        return False
    if any(p in {"__pycache__", "diagnostic-reconstruction"} for p in parts):
        return False
    if re.search(r"(?:\.before|\.after|before\d|after\d|history[_.]|claim_matrix\.before)", name):
        return False
    if name.endswith(("-links.json", "-scripts.json", ".links.json", ".meta.json")):
        return False
    if len(parts) == 1:
        return rel.suffix.lower() != ".txt"
    if parts[0] not in ROOTS:
        return False
    if len(parts) > 2 and parts[1] not in NESTED.get(parts[0], set()):
        return False
    if rel.suffix.lower() == ".txt":
        return name == "requirements.txt" or name.endswith("_license.txt")
    if parts[:2] == ("public-experiments", "audit"):
        return name in {
            "asset_verification.json", "data_dictionary.md", "game_code_data_gap.json",
            "game_framework_license.txt", "kuai_data_license.txt",
            "obd_sample_verification.json", "readme.md",
        }
    return True


def write_csv(path, rows, fields):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def export(source, destination):
    assert source.resolve() != destination.resolve(), "Separate export checkout required"
    assert (destination / ".git").is_dir(), "Clone the destination repository first"
    rows, sdkrows, seen = [], [], set()
    actual_paths = {
        p.relative_to(source).as_posix().casefold(): p.relative_to(source)
        for p in source.rglob("*") if p.is_file()
    }

    def copy(rel, kind):
        rel = actual_paths[Path(rel).as_posix().casefold()]
        key = rel.as_posix()
        if key in seen:
            return rel
        assert ".." not in rel.parts and not rel.is_absolute()
        src, dst = source / rel, destination / rel
        before = sha(src)
        dst.parent.mkdir(parents=True, exist_ok=True)
        if dst.exists():
            assert sha(dst) == before, "Refuse to overwrite changed publication file: " + key
        else:
            shutil.copy2(src, dst)
        assert sha(dst) == before == sha(src)
        rows.append(dict(path=key, sha256=before, bytes=src.stat().st_size, kind=kind))
        seen.add(key)
        return rel

    candidates = sorted(p for p in source.rglob("*") if p.is_file() and selected(p.relative_to(source)))
    for p in candidates:
        copy(p.relative_to(source), "research_source_or_aggregate_result")

    # A release is published only with a verified original hash and source URL.
    catalog = json.loads((source / "ThirdPartySDKs/CATALOG.json").read_text(encoding="utf-8-sig"))
    for item in catalog:
        for artifact in item.get("artifacts", []):
            rel = Path("ThirdPartySDKs") / artifact["path"].replace("\\", "/")
            if rel.suffix.lower() not in {".aar", ".jar", ".pom", ".zip", ".tgz"}:
                continue
            if not (source / rel).is_file():
                continue
            expected = artifact.get("sha256")
            url = artifact.get("url")
            assert expected and url and url.startswith("https://"), rel
            assert sha(source / rel) == expected, rel
            rel = copy(rel, "official_sdk_release")
            sdkrows.append(dict(
                path=rel.as_posix(), vendor=item.get("vendor", ""),
                sdk=item.get("sdk", ""), version=item.get("version", ""),
                sha256=expected, bytes=(source / rel).stat().st_size,
                source_url=url,
                licenses=json.dumps(item.get("licenses", []), ensure_ascii=False),
                last_modified=artifact.get("http_last_modified") or "",
                provenance_file="ThirdPartySDKs/CATALOG.json",
            ))

    # Unity Services and Singular live outside the original SDK vendor tree.
    metadata = {}

    def walk(obj):
        if isinstance(obj, dict):
            if isinstance(obj.get("sha256"), str) and isinstance(obj.get("url"), str):
                metadata[obj["sha256"]] = obj
            for value in obj.values():
                walk(value)
        elif isinstance(obj, list):
            for value in obj:
                walk(value)

    for p in candidates:
        if p.suffix == ".json":
            try:
                walk(json.loads(p.read_text(encoding="utf-8-sig")))
            except (ValueError, UnicodeError):
                pass
    for root in ["cross-sdk", "core-insights", "identity-graph"]:
        for p in (source / root).rglob("*"):
            if not p.is_file() or p.suffix not in {".tgz", ".aar", ".pom"} or "extracted" in p.parts:
                continue
            digest = sha(p)
            meta = metadata.get(digest)
            assert meta and meta["url"].startswith("https://"), "No verified origin: " + str(p)
            rel = p.relative_to(source)
            copy(rel, "official_sdk_release")
            sdkrows.append(dict(
                path=rel.as_posix(), vendor="Unity" if p.suffix == ".tgz" else "Singular",
                sdk=meta.get("sdk", p.parent.parent.name), version=meta.get("version", p.parent.name),
                sha256=digest, bytes=p.stat().st_size, source_url=meta["url"],
                licenses=meta.get("license", "See embedded license and upstream terms"),
                last_modified=meta.get("registry_time", "") or "",
                provenance_file="core-insights/PACKAGE_PROVENANCE.json or cross-sdk/ACQUISITION.json",
            ))
            # Preserve package notices separately for browsing without unpacking.
            if p.suffix == ".tgz":
                for notice in p.parent.rglob("*"):
                    if notice.is_file() and notice.name.lower() in {
                        "license", "license.md", "license.txt", "third party notices.md",
                        "third-party notices.md", "third party notices.txt",
                    }:
                        copy(notice.relative_to(source), "upstream_license_notice")

    # Archives remain untouched: no repacking, no decompiled game distributions.
    for row in sdkrows:
        p = destination / row["path"]
        if p.suffix in {".aar", ".jar", ".zip"}:
            with zipfile.ZipFile(p) as z:
                assert z.testzip() is None, row["path"]
        elif p.suffix == ".tgz":
            with tarfile.open(p, "r:gz") as t:
                assert t.getmembers()
    sdkrows = list({r["path"]: r for r in sdkrows}.values())
    write_csv(destination / "publication/ORIGINAL_FILE_MANIFEST.csv", rows,
              ["path", "sha256", "bytes", "kind"])
    write_csv(destination / "publication/SDK_ARTIFACTS.csv", sdkrows,
              ["path", "vendor", "sdk", "version", "sha256", "bytes",
               "source_url", "licenses", "last_modified", "provenance_file"])
    print(json.dumps(dict(
        copied_files=len(rows), copied_bytes=sum(r["bytes"] for r in rows),
        sdk_files=len(sdkrows), sdk_bytes=sum(r["bytes"] for r in sdkrows),
        reports=sum(bool(re.match(r"\d\d_.*\.md$", r["path"])) for r in rows),
    ), indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--destination", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    export(args.source, args.destination)
