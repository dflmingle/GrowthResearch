"""Follow promising candidates to public dataset cards and original field definitions."""
import json
from concurrent.futures import ThreadPoolExecutor
from collect68 import OUT, fetch

TARGETS = {
    "kg-iap-card": "https://www.kaggle.com/api/v1/datasets/view/pratyushpuri/mobile-game-in-app-purchases-dataset-2025",
    "kg-gamelytics-card": "https://www.kaggle.com/api/v1/datasets/view/debs2x/gamelytics-mobile-analytics-challenge",
    "kg-cosmetics-card": "https://www.kaggle.com/api/v1/datasets/view/mkechinov/ecommerce-events-history-in-cosmetics-shop",
    "kg-multicategory-card": "https://www.kaggle.com/api/v1/datasets/view/mkechinov/ecommerce-behavior-data-from-multi-category-store",
    "kg-jewelry-card": "https://www.kaggle.com/api/v1/datasets/view/mkechinov/ecommerce-purchase-history-from-jewelry-store",
    "kg-olist-card": "https://www.kaggle.com/api/v1/datasets/view/olistbr/brazilian-ecommerce",
    "kg-tafeng-card": "https://www.kaggle.com/api/v1/datasets/view/chiranjivdas09/ta-feng-grocery-dataset",
    "kg-vibrent-card": "https://www.kaggle.com/api/v1/datasets/view/kaborg15/vibrent-clothes-rental-dataset",
    "kg-tiktok-card": "https://www.kaggle.com/api/v1/datasets/view/datascikhan/tiktok-shop-viral-sales-and-cac-attribution",
    "kg-googleplay-card": "https://www.kaggle.com/api/v1/datasets/view/lava18/google-play-store-apps",
    "kkbox-competition": "https://www.kaggle.com/competitions/kkbox-churn-prediction-challenge/data",
    "kkbox-rules": "https://www.kaggle.com/competitions/kkbox-churn-prediction-challenge/rules",
    "journey-fields": "https://raw.githubusercontent.com/bradleyboehmke/completejourney/master/R/transactions.R",
    "journey-download": "https://raw.githubusercontent.com/bradleyboehmke/completejourney/master/R/download_data.R",
    "journey-original": "https://www.8451.com/area51/",
    "google-gaming-queries": "https://developers.google.com/analytics/bigquery/basic-queries",
    "google-export-schema": "https://support.google.com/analytics/answer/7029846?hl=en",
    "criteo-search-data": "https://ailab.criteo.com/criteo-sponsored-search-conversion-log-dataset/",
}
with ThreadPoolExecutor(max_workers=4) as pool:
    rows = list(pool.map(fetch, TARGETS.items()))
(OUT / "FETCH_LEDGER_FOLLOWUP.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
for row in rows:
    print(json.dumps({k: row.get(k) for k in ["id", "status", "bytes", "error"]}))
for p in sorted((OUT / "sources").glob("kg-*-card.json")):
    obj = json.loads(p.read_text(encoding="utf-8"))
    print("\nCARD", p.stem)
    print(json.dumps({k: obj.get(k) for k in ["title", "licenseName", "licenses", "description", "subtitle", "totalBytes", "files"]}, ensure_ascii=False)[:12500])
