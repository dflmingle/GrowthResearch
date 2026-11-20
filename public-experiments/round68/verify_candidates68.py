"""Inspect only legally public release metadata and limited relevant artifacts."""
from concurrent.futures import ThreadPoolExecutor
import importlib.util
import json
from collect68 import OUT, fetch

TARGETS = {
    "kg-jewelry-files": "https://www.kaggle.com/api/v1/datasets/list/mkechinov/ecommerce-purchase-history-from-jewelry-store",
    "kg-cosmetics-files": "https://www.kaggle.com/api/v1/datasets/list/mkechinov/ecommerce-events-history-in-cosmetics-shop",
    "kg-multicategory-files": "https://www.kaggle.com/api/v1/datasets/list/mkechinov/ecommerce-behavior-data-from-multi-category-store",
    "kg-vibrent-files": "https://www.kaggle.com/api/v1/datasets/list/kaborg15/vibrent-clothes-rental-dataset",
    "kg-gamelytics-files": "https://www.kaggle.com/api/v1/datasets/list/debs2x/gamelytics-mobile-analytics-challenge",
    "kg-iap-files": "https://www.kaggle.com/api/v1/datasets/list/pratyushpuri/mobile-game-in-app-purchases-dataset-2025",
    "journey-download-code": "https://raw.githubusercontent.com/bradleyboehmke/completejourney/master/R/utils.R",
    "journey-transactions-manual": "https://raw.githubusercontent.com/bradleyboehmke/completejourney/master/man/transactions_sample.Rd",
    "rees46-datasets": "https://rees46.com/en/datasets",
    "rees46-original-cdp": "https://rees46.com/en/open-cdp",
}
with ThreadPoolExecutor(max_workers=4) as pool:
    rows = list(pool.map(fetch, TARGETS.items()))
(OUT / "FETCH_LEDGER_VERIFY.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
for row in rows:
    print(json.dumps({k: row.get(k) for k in ["id", "status", "bytes", "error"]}))
for path in sorted((OUT / "sources").glob("kg-*-files.json")):
    obj = json.loads(path.read_text(encoding="utf-8"))
    print("\nFILES", path.stem, json.dumps(obj, ensure_ascii=False)[:13000])
print("R_READERS", {name: importlib.util.find_spec(name) is not None for name in ["pyreadr", "rdata"]})
