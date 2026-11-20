"""Public metadata and official documentation audit. No logins or production events."""
from pathlib import Path
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor
import hashlib, json, re, requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
OUT.mkdir(parents=True, exist_ok=True)
(OUT / "sources").mkdir(exist_ok=True)
TARGETS = {
    "kg-game-revenue": "https://www.kaggle.com/api/v1/datasets/list?search=mobile%20game%20revenue&page=1",
    "kg-inapp": "https://www.kaggle.com/api/v1/datasets/list?search=in%20app%20purchase&page=1",
    "kg-ad-revenue": "https://www.kaggle.com/api/v1/datasets/list?search=ad%20impression%20revenue&page=1",
    "kg-subscription": "https://www.kaggle.com/api/v1/datasets/list?search=subscription%20transactions&page=1",
    "kg-multistore": "https://www.kaggle.com/api/v1/datasets/list?search=multi%20store%20transactions&page=1",
    "kg-tafeng": "https://www.kaggle.com/api/v1/datasets/list?search=ta%20feng&page=1",
    "google-game": "https://developers.google.com/analytics/bigquery/app-gaming-demo-dataset",
    "google-retail": "https://developers.google.com/analytics/bigquery/web-ecommerce-demo-dataset",
    "google-ga360": "https://support.google.com/analytics/answer/7586738?hl=en",
    "journey-description": "https://raw.githubusercontent.com/bradleyboehmke/completejourney/master/DESCRIPTION",
    "journey-readme": "https://raw.githubusercontent.com/bradleyboehmke/completejourney/master/README.md",
    "journey-license": "https://raw.githubusercontent.com/bradleyboehmke/completejourney/master/LICENSE.md",
    "journey-load": "https://raw.githubusercontent.com/bradleyboehmke/completejourney/master/R/get_transactions.R",
    "journey-tree": "https://api.github.com/repos/bradleyboehmke/completejourney/git/trees/master?recursive=1",
    "zenodo-game-search": "https://zenodo.org/api/records?q=%22game%22%20%22revenue%22&size=10",
}


def fetch(item):
    ident, url = item
    record = {"id": ident, "url": url, "observed_utc": datetime.now(timezone.utc).isoformat(),
              "authorization": "Unauthenticated public metadata/document GET only"}
    try:
        response = requests.get(url, timeout=35)
        record.update(status=response.status_code, final_url=response.url,
                      content_type=response.headers.get("Content-Type"), bytes=len(response.content))
        # Save metadata/documents, not raw user-level records or tracking identifiers.
        extension = ".json" if "json" in response.headers.get("Content-Type", "") else ".txt"
        if extension == ".json":
            try:
                parsed = response.json()
                body = json.dumps(parsed, ensure_ascii=False, indent=2).encode("utf-8")
            except ValueError:
                body = response.content
        else:
            soup = BeautifulSoup(response.content, "html.parser")
            for tag in soup(["script", "style", "nav", "footer"]):
                tag.decompose()
            body = soup.get_text("\n", strip=True).encode("utf-8") if "<html" in response.text[:3000].lower() else response.content
        path = OUT / "sources" / (ident + extension)
        path.write_bytes(body)
        record.update(path=path.relative_to(ROOT).as_posix(), sha256=hashlib.sha256(body).hexdigest(),
                      original_response_sha256=hashlib.sha256(response.content).hexdigest(),
                      transformation="JSON pretty print or visible document text; tracking scripts excluded")
    except requests.RequestException as exc:
        record["error"] = type(exc).__name__
    return record


if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(fetch, TARGETS.items()))
    (OUT / "FETCH_LEDGER_INITIAL.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for row in results:
        print(json.dumps({k: row.get(k) for k in ["id", "status", "bytes", "error"]}))
    for path in sorted((OUT / "sources").glob("kg-*.json")):
        try:
            entries = json.loads(path.read_text(encoding="utf-8"))
            for entry in entries[:9]:
                print(json.dumps({"search": path.stem, "ref": entry.get("ref"),
                                  "title": entry.get("title"), "license": entry.get("licenseName"),
                                  "bytes": entry.get("totalBytes"),
                                  "description": entry.get("subtitle", "")}, ensure_ascii=False))
        except (ValueError, TypeError):
            pass
