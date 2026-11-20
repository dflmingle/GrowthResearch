"""Bounded public release downloads; no authentication or raw-ID reporting."""
from pathlib import Path
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import quote, urlsplit
import hashlib, io, json, requests, struct, zlib
from collect68 import OUT, fetch

RAW = OUT / "raw"
RAW.mkdir(exist_ok=True)


def asset(spec):
    ident, url, limit, prefix_only = spec
    record = dict(id=ident, url=url, observed_utc=datetime.now(timezone.utc).isoformat(),
                  mode="prefix_schema_only" if prefix_only else "bounded_complete_download",
                  byte_limit=limit, credentials_used=False)
    try:
        with requests.get(url, stream=True, timeout=(15, 45)) as response:
            record.update(status=response.status_code, content_type=response.headers.get("Content-Type"),
                          declared_length=response.headers.get("Content-Length"),
                          redirect_host=urlsplit(response.url).hostname)
            if response.status_code != 200:
                return record
            chunks, total, complete = [], 0, True
            for chunk in response.iter_content(65536):
                total += len(chunk)
                if total > limit:
                    complete = False
                    break
                chunks.append(chunk)
            body = b"".join(chunks)
            record.update(bytes_read=len(body), complete=complete,
                          received_bytes_sha256=hashlib.sha256(body).hexdigest())
            if body.lstrip().startswith((b"<", b"{")):
                record["stop"] = "Unexpected HTML/JSON instead of dataset; no bypass"
                return record
            if prefix_only:
                decoded = body
                if body[:4] == b"PK\x03\x04":
                    fields = struct.unpack("<IHHHHHIIIHH", body[:30])
                    method, names, extras = fields[3], fields[-2], fields[-1]
                    start = 30 + names + extras
                    decoded = zlib.decompressobj(-15).decompress(body[start:]) if method == 8 else body[start:]
                    record["archive_member_name"] = body[30:30 + names].decode("utf-8", errors="replace")
                line = decoded.splitlines()[0].decode("utf-8-sig", errors="replace")
                record["header_only"] = line
                record["raw_rows_saved"] = False
                record["complete"] = False
            elif complete:
                path = RAW / (ident + ".download")
                path.write_bytes(body)
                record["path"] = path.relative_to(OUT.parents[1]).as_posix()
            else:
                record["stop"] = "Byte cap reached; full artifact not saved"
    except (requests.RequestException, ValueError, zlib.error, struct.error) as exc:
        record["error"] = type(exc).__name__
    return record


def kaggle_file(ref, name):
    return "https://www.kaggle.com/api/v1/datasets/download/" + ref + "/" + quote(name, safe="")


if __name__ == "__main__":
    extra = fetch(("kg-electronics-card", "https://www.kaggle.com/api/v1/datasets/view/mkechinov/ecommerce-purchase-history-from-electronics-store"))
    (OUT / "FETCH_LEDGER_ELECTRONICS.json").write_text(json.dumps([extra], indent=2) + "\n", encoding="utf-8")
    card = json.loads((OUT / "sources/kg-electronics-card.json").read_text(encoding="utf-8"))
    print(json.dumps({k: card.get(k) for k in ["title", "description", "licenseName", "totalBytes"]}, ensure_ascii=False))
    specs = [
        ("completejourney", "https://raw.githubusercontent.com/bradleyboehmke/completejourney/master/data/transactions.rds", 18_000_000, False),
        ("jewelry", kaggle_file("mkechinov/ecommerce-purchase-history-from-jewelry-store", "jewelry.csv"), 20_000_000, False),
        ("vibrent-orders", kaggle_file("kaborg15/vibrent-clothes-rental-dataset", "additional_tabular_data/original_orders.csv"), 3_000_000, False),
        ("vibrent-plans", kaggle_file("kaborg15/vibrent-clothes-rental-dataset", "additional_tabular_data/subscription_plan.csv"), 100_000, False),
        ("vibrent-spot", kaggle_file("kaborg15/vibrent-clothes-rental-dataset", "additional_tabular_data/spot_rentals.csv"), 2_000_000, False),
        ("cosmetics-prefix", kaggle_file("mkechinov/ecommerce-events-history-in-cosmetics-shop", "2019-Oct.csv"), 262144, True),
    ]
    with ThreadPoolExecutor(max_workers=3) as pool:
        rows = list(pool.map(asset, specs))
    (OUT / "ASSET_ACQUISITION.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for row in rows:
        print(json.dumps(row, ensure_ascii=False))
