"""Package round68 evidence audit; never train or replace historical evidence."""
from pathlib import Path
from datetime import datetime, timezone
import csv, hashlib, json, re

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
NOW = datetime.now(timezone.utc).isoformat()


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def write(path, text):
    p = ROOT / path
    if p.exists():
        raise RuntimeError("Do not overwrite historical deliverable: " + str(p))
    p.write_text(text.strip() + "\n", encoding="utf-8", newline="\n")


def csvwrite(path, rows):
    p = ROOT / path
    assert not p.exists()
    fields = list(dict.fromkeys(k for row in rows for k in row))
    with p.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def load(name):
    return json.loads((OUT / name).read_text(encoding="utf-8-sig"))


fetches = []
for p in sorted(OUT.glob("FETCH_LEDGER_*.json")):
    fetches.extend(json.loads(p.read_text(encoding="utf-8")))
sources = {row["id"]: row for row in fetches}
assert len(sources) == len(fetches)
assets = load("ASSET_ACQUISITION.json") + load("ASSET_ELECTRONICS.json")
assetmap = {x["id"]: x for x in assets}
journey = load("AUDIT_JOURNEY.json")
jewelry = load("AUDIT_JEWELRY.json")
electronics = load("AUDIT_ELECTRONICS.json")
vibrent = load("AUDIT_VIBRENT.json")


def url(ident):
    return sources[ident]["url"]


catalog = []


def dataset(ident, name, publisher, grade, refs, license_, access, period, money,
            stable_id, zeros, future, transfer, stop, fields, raw=None):
    catalog.append(dict(
        dataset_id="DS68-" + ident, name=name, publisher=publisher, grade=grade,
        official_source_url=url(refs[0]), additional_source_urls="; ".join(url(x) for x in refs[1:]),
        download_url=assetmap[raw]["url"] if raw else "See source card; not a verified full download",
        declared_license=license_, license_evidence="; ".join(refs),
        actual_access=access, time_range=period, amount_semantics=money,
        stable_source_scoped_id=stable_id, complete_zero_population=zeros,
        future_7_28_readiness=future, cross_product_readiness=transfer,
        fields=fields, training_status="STOP", audit_status="LIMITED" if raw else "METADATA_ONLY",
        blocking_reason=stop, raw_artifact_sha256=assetmap[raw].get("received_bytes_sha256", "") if raw else "",
        evidence_paths="; ".join(sources[x].get("path", "") for x in refs),
        local_audit_path={
            "completejourney": "AUDIT_JOURNEY.json", "jewelry": "AUDIT_JEWELRY.json",
            "electronics": "AUDIT_ELECTRONICS.json",
        }.get(raw, ""),
        event_time="Documented or observed as time_range describes",
        available_at="NOT_ESTABLISHED", observation_watermark="NOT_ESTABLISHED",
        privacy="Only source-local pseudonymous grouping; no external matching or ID feature/export",
        is_independent_of_uci_online_retail=True,
    ))


dataset("01", "Google Firebase Flood-It! BigQuery demo", "Google / Flood-It!", "A_CANDIDATE_OBFUSCATED",
        ["google-game", "google-export-schema"],
        "Dataset terms not independently verified; page CC BY4/code Apache is not automatic dataset license",
        "Official docs HTTP200; queries require authorized Cloud project; no event rows retrieved",
        "114 days documented; actual dates/table coverage not queried",
        "IAA/IAP completeness and amount truth UNKNOWN; obfuscated placeholders/internal inconsistency disclosed",
        "user_pseudo_id in official example; actual stability not tested", "UNKNOWN",
        "STOP: no actual mature monetary labels verified", "One game; Android/iOS are platforms, not two products",
        "No verified value rows/license scope/zero denominator; do not infer demo income from generic GA schema",
        "event_date,event_timestamp,user_pseudo_id; generic event_value_in_usd is not certified income")
dataset("02", "Google Play Store Apps", "Lavanya Gupta / scraped Play listing", "D",
        ["kg-googleplay-card"], "CC BY-SA4 declared by uploader",
        "Card HTTP200; no review/customer rows downloaded", "Listing snapshot; no user transaction timeline",
        "Listed app price/installs are not realized user revenue", "NO stable purchasing user key", "NO",
        "STOP", "App rows do not create user-value transfer samples",
        "No longitudinal user-level realized money", "App,Category,Rating,Installs,Price as described by listing")
dataset("03", "Mobile Game In-App Purchases Dataset 2025", "Pratyush Puri / Kaggle", "SYNTHETIC_NOT_A",
        ["kg-iap-card", "kg-iap-files"], "CC0 declared",
        "Card/file metadata HTTP200; intentionally no synthetic row download",
        "2025 snapshot with last-purchase date; not a transaction sequence",
        "InAppPurchaseAmount explicitly synthetic, not actual IAP", "Synthetic UserID only",
        "Synthetic zeros/missingness do not establish real denominator",
        "STOP", "GameGenre is not independently observed game ID",
        "Description explicitly says comprehensive synthetic dataset", "UserID,InAppPurchaseAmount,SpendingSegment,LastPurchaseDate")
dataset("04", "Gamelytics Mobile Analytics Challenge", "debs2x / Kaggle uploader", "A_CANDIDATE_UNVERIFIED",
        ["kg-gamelytics-card", "kg-gamelytics-files"], "Apache2 declared by uploader; original operator provenance unverified",
        "Three real file entries verified; no raw download", "reg_ts/auth_ts; A/B revenue has no event timestamp",
        "Revenue int with no certified currency, horizon or real operator provenance", "uid vs user_id no verified join contract",
        "A/B zero counts described; not tied to mature longitudinal population",
        "STOP: cumulative A/B target not D7/D28 event labels", "No multi-game identifier",
        "Real-world-inspired is not proof of production data; no shared identity/time contract",
        "reg_data(reg_ts,uid),auth_data(auth_ts,uid),ab_test(user_id,revenue,testgroup)")
dataset("05", "Criteo Sponsored Search Conversion Log", "Criteo AI Lab", "C_AD_CONVERSION_NOT_B",
        ["criteo-search-data"], "CC BY-NC-SA4 explicit official terms",
        "Official definitions HTTP200; no download under unresolved commercial-purpose restriction",
        "90 days sampled live click traffic documented",
        "SalesAmountInEuro is attributed advertiser sale, not publisher IAA; -1 denotes no conversion",
        "user_id,partner_id documented only; sampled-history persistence unknown",
        "Click non-conversion present, not complete user purchase/IAA population",
        "STOP: click conversion horizon is not user D7/D28 LTV",
        "partner_id could separate advertisers; no file audit and NC constraint",
        "NC purpose not assumed permitted; click-selection and conversion attribution differ from customer total value",
        "Sale,SalesAmountInEuro,time_delay_for_conversion,click_timestamp,partner_id,user_id")
dataset("06", "Complete Journey full transactions", "84.51 degree data / Brad Boehmke & Steven Mortimer data-package release", "C",
        ["journey-description", "journey-readme", "journey-download-code", "journey-transactions-manual", "journey-original"],
        "Published R data package explicitly CC0; original portal failed connection this audit",
        "FULL_200_12775661_BYTE_RDS_PARSED_1469307_ROWS",
        "Observed 2017-01-01 11:53:26 to 2018-01-01 04:01:20 UTC representation",
        "sales_value: dollars retailer receives per receipt line; not bank-settled net profit",
        "2469 source households; no missing keys; household is not a person",
        "All household purchases at retailer documented; per-household active intervals/outages absent",
        "Time span and real recorded amount support conditional ledger forecasting; strict zero/missing gate unresolved",
        "457 outlets and 68509 SKUs are not independent merchant/apps",
        "STOP strict training until observation spells/completeness and exact amount/zero definitions fixed",
        "household_id,store_id,basket_id,product_id,quantity,sales_value,transaction_timestamp", "completejourney")
dataset("07", "REES46 jewelry purchase history", "REES46 / Open CDP / Mikhail Kechinov", "C_POSITIONAL_SCHEMA_PENDING",
        ["kg-jewelry-card", "kg-jewelry-files", "rees46-datasets"],
        "Card expressly allows free use with dataset+REES46 attribution; metadata says copyright original authors; not CC0",
        "FULL_200_ZIP_CRC_AND_95911_HEADERLESS_ROWS",
        "Observed 2018-12-01 to 2021-12-01; official landing older two-year period conflicts",
        "Purchase records asserted by publisher; c7 price hypothesis unconfirmed schema/currency",
        "c8 candidate key 32233 distinct and 5352 missing; column meaning not yet established",
        "No active-customer/exposure roster; 14 source-wide calendar days without rows unexplained",
        "Time span sufficient in principle; schema/coverage/amount gate STOP",
        "Different store domain than electronics per publisher; ownership independence not verified",
        "Missing header, positional schema and key scope; no absent-vs-zero contract",
        "13 headerless columns; c0 parses timestamp; remaining semantic mapping pending", "jewelry")
dataset("08", "REES46 electronics purchase history", "REES46 / Open CDP / Mikhail Kechinov", "C",
        ["kg-electronics-card", "kg-electronics-files", "rees46-datasets"],
        "Explicit free-use with dual attribution; original-author copyright retained; redistribution terms not assumed",
        "FULL_200_ZIP_CRC_AND_2633521_ROWS",
        "Actual 19631 rows in Jan1970; remaining Jan-Nov2020, versus card Apr-Nov2020",
        "price purchase-line field; no ISO currency, quantity/payment/refund certification",
        "user_id 233834 unique nonmissing keys; 2069352 rows missing (78.5774%)",
        "Incomplete keys and missing coverage cannot certify future zero money",
        "STOP: source dates, absent keys and missing amounts must be resolved",
        "Candidate second merchant; do not match IDs against jewelry/cosmetics",
        "431954 prices missing (16.4021%), 675 duplicates, 121 nonpositive prices; do not silently drop anomalies",
        "event_time,order_id,product_id,category_id,category_code,brand,price,user_id", "electronics")
dataset("09", "REES46 cosmetics behavior events", "REES46 / Open CDP / Mikhail Kechinov", "C_CANDIDATE_PURCHASE_EVENTS",
        ["kg-cosmetics-card", "kg-cosmetics-files", "rees46-datasets"],
        "Explicit free-use with dataset+REES46 attribution; original-author copyright retained",
        "October ZIP HTTP200 prefix only; 262144 compressed bytes, header extracted; no raw rows retained",
        "Oct2019-Feb2020 documented; 5 month file names verified, no full continuity check",
        "price on view/cart is not revenue; only verified completed purchase could become a ledger label",
        "user_id documented permanent; actual long-term stability not tested",
        "Views expose some nonbuyers, not proof of all visitors/active observation",
        "Potential 7/28 windows after full release/schema/coverage audit; STOP now",
        "Candidate distinct store domain, not a confirmed independent game",
        "Prefix/header is not full dataset; conflicting card event_type description; order/refund/dedup semantics missing",
        assetmap["cosmetics-prefix"]["header_only"])
dataset("10", "REES46 multi-category store behavior", "REES46 / Open CDP / Mikhail Kechinov", "C_CANDIDATE_PURCHASE_EVENTS",
        ["kg-multicategory-card", "kg-multicategory-files", "rees46-datasets"],
        "Explicit free-use and dual attribution; not an assumed CC0 release",
        "Kaggle lists Oct/Nov; Dec-Apr official-host links documented, binaries not fetched",
        "Oct2019-Apr2020 documented; only 2 Kaggle files directly listed",
        "purchase price possibly recorded sales; view/cart prices are proxy context, not realized revenue",
        "Permanent user_id documented; no cross-store contract", "UNKNOWN",
        "STOP full months and observation coverage not verified", "Store-level transfer candidate, categories are not products/apps",
        "Huge advertised row count does not establish economic labels or maturity",
        "event_time,event_type,product_id,price,user_id,user_session")
dataset("11", "Vibrent clothes rental", "Karl Audun Kagnes Borgersen et al. / RecSys2024", "C_PRICE_METADATA_D_BEHAVIOR",
        ["kg-vibrent-card", "kg-vibrent-files"], "CC BY4 with paper citation",
        "3 relevant CSVs downloaded and parsed, not 7GB images/embeddings",
        "Original rental starts Mar2016-Apr2021; spot starts Feb2020-Jun2024",
        "58 subscription price plans are offered prices; no per-user charged/paid/refunded amount in obtained tables",
        "5438 distinct customer keys in 12558 original rental rows",
        "No verified billing eligibility or missed-payment observation denominator",
        "STOP future monetary labels; rental behavior only",
        "Original/spot services from same operator not proven two independent products",
        "Plan price times rental month would be fabricated revenue; spot file lacks customer ID",
        "customer.id,outfit.id,rentalPeriod.start/end; plan metadata pricePerMonth.amount/currency")
dataset("12", "KKBox churn competition", "KKBOX / WSDM / Kaggle competition", "C_CANDIDATE_UNVERIFIED_ACCESS",
        ["kkbox-competition", "kkbox-rules"], "Competition rules not readable from public page shell; no license assumed",
        "HTTP200 page shells only; no data/rules access or bypass",
        "Actual file time span not established this audit",
        "No ledger obtained; field names from secondary descriptions not accepted as actual data",
        "UNKNOWN this audit", "UNKNOWN", "STOP", "One service, not multigame",
        "No verified applicable license or public file obtained", "NOT_VERIFIED")
dataset("13", "Olist Brazilian E-Commerce", "Olist official Kaggle publisher", "C_DOCUMENTED_REAL",
        ["kg-olist-card"], "CC BY-NC-SA4",
        "Official real commercial data card HTTP200; no raw download with unresolved NC purpose",
        "2016-2018 per official card", "Item prices/payment records described; no actual file audit",
        "Stable-customer vs per-order key not verified from files here",
        "Order-only sample; no full visitor/zero revenue roster",
        "STOP for current use; not approved based on title", "Sellers/marketplaces documented; selection and entity scope need audit",
        "NC restriction + population/observation scope; shared marketplace is not independent apps",
        "orders,items,payments,sellers/customers described; actual schema not inspected")
dataset("14", "Ta Feng grocery Kaggle rehost", "Original Ta Feng grocery; Kaggle chiranjivdas09 rehost", "C_CANDIDATE_LICENSE_CHAIN",
        ["kg-tafeng-card", "kg-tafeng"], "Uploader declares CC0; original data rights chain not established",
        "Card/search HTTP200; original-licensed artifact not verified",
        "Nov2000-Feb2001 per uploader only", "Transactions asserted; no monetary file audit",
        "UNKNOWN", "UNKNOWN", "STOP", "Potential second retailer, but current license/data gate fails",
        "A rehost CC0 badge is insufficient evidence of original rights/complete longitudinal coverage",
        "NOT_VERIFIED")
dataset("15", "Google GA4 Merchandise Store obfuscated demo", "Google Merchandise Store / Google", "C_OBFUSCATED_DEMO",
        ["google-retail"], "Page CC BY4 does not establish separate dataset terms",
        "Docs HTTP200; Cloud project required; no query execution", "2020-11-01 to 2021-01-31 documented",
        "Obfuscated placeholder value fields; no certified true monetary labels",
        "user_pseudo_id, actual persistence unknown", "UNKNOWN", "STOP", "Same merchant as UA demo, not independent product",
        "Obfuscation and missing actual rows/licensing verification", "GA4 event export schema, placeholders")
dataset("16", "TikTok Shop Sales dataset", "datascikhan / independent Kaggle uploader, not TikTok official", "UNVERIFIED_NOT_B",
        ["kg-tiktok-card"], "Uploader CC0 declared",
        "Public card only; no raw data downloaded without genuine-source substantiation",
        "No verified event/available time coverage", "Revenue/CAC/ROAS field names asserted, actual economic provenance unknown",
        "UNKNOWN", "UNKNOWN", "STOP", "No verified independent products",
        "Many financial fields and production-grade prose do not prove real advertiser or publisher ledger",
        "Net_Revenue,CAC,ROAS as uploader prose; not verified ad ILRD")
dataset("17", "Google UA360 Merchandise Store demo", "Google Merchandise Store / Google", "C_OBFUSCATED_DEMO",
        ["google-ga360"], "Dataset usage terms not independently established from help page",
        "Official legacy docs HTTP200; no query execution", "2016-08-01 to 2017-08-01 documented",
        "Obfuscated Google Analytics session ecommerce sample",
        "Session/client key contract not file-verified", "UNKNOWN", "STOP",
        "Same merchant as GA4 demo, not independent source for cross-product validation",
        "Obfuscated session data and no actual files/zero denominator audit", "ga_sessions_*")

csvwrite("68_DATASET_CATALOG.csv", catalog)

admissions = [
    dict(experiment_id="E68-0", task="New game D7/D28 IAA/IAP value prediction", datasets="DS68-01;03;04",
         data_status="STOP", train_now=False, license="Game-demo terms unresolved; synthetic and inspired sets not genuine income",
         stable_id="Not a verified real player revenue join", history="No verified mature transaction timeline",
         labels="No admitted genuine game revenue", zero_missing="Not identified", time_split="Not executable",
         next_material="Authorized complete all-player revenue/observation ledger", allowed="Documentation/schema audit",
         forbidden="Game LTV accuracy, Axon/Vector gain"),
    dict(experiment_id="E68-1", task="Publisher ad impression revenue forecasting", datasets="DS68-05;16",
         data_status="STOP", train_now=False, license="Criteo NC/current scope unresolved; TikTok provenance unverified",
         stable_id="No verified ILRD user/impression join", history="Not verified", labels="Sales conversion != publisher IAA",
         zero_missing="No complete ad opportunity/value population", time_split="Not executable",
         next_material="Permitted real ILRD with impression_id/currency/precision and observation coverage",
         allowed="Revenue semantics distinction", forbidden="IAA LTV/real ad bidding ROAS"),
    dict(experiment_id="E68-2", task="Independent single-retailer future 7/28 recorded sales", datasets="DS68-06",
         data_status="LIMITED_AUDIT_ONLY", train_now=False, license="Data package CC0 documented; cite original study",
         stable_id="2469 source households, no null keys", history="One full-year release parsed",
         labels="sales_value defined, sufficient event-time span", zero_missing="Source full-purchase claim; household activity/outage not identifiable",
         time_split="Possible event-time split, not yet preregistered/new model trained",
         next_material="Explicit household observation intervals and missingness contract; predefined label/accounting scope",
         allowed="Quality/coverage audit and prospective fixed protocol",
         forbidden="Certified true-zero spending, game LTV or treating outlets as games"),
    dict(experiment_id="E68-3", task="Store A to store B zero-shot transfer, no individual linkage",
         datasets="DS68-07 + DS68-08", data_status="STOP", train_now=False,
         license="REES46 express free-use with dual attribution, no redistribution assumption",
         stable_id="Jewelry positional key unconfirmed; electronics 78.58% missing",
         history="Two complete files; date/schema contradictions remain",
         labels="No compatible certified currency/quantity/payment/refund contract",
         zero_missing="Neither full observable-risk cohort certified", time_split="Cannot certify with current anomalies",
         next_material="Publisher field dictionary, corrected dates/keys, observation roster, comparable monetary semantics",
         allowed="Cross-domain data readiness/schema comparison",
         forbidden="Transfer effect size, cross-game or identity graph claim"),
    dict(experiment_id="E68-4", task="Joint multi-store learning vs store-level aggregate prior",
         datasets="DS68-06;07;08;09;10", data_status="STOP", train_now=False,
         license="Respect individual release license and dataset isolation",
         stable_id="No user crosswalk needed; each namespace separate", history="Only 06/07/08 full files, 09 prefix",
         labels="Different household/person/price/receipt and currency semantics",
         zero_missing="Not certified", time_split="Source maturity must precede target prediction; no target-future normalization",
         next_material=">=2 fully admitted products with compatible target and coverage; fixed target adaptation budget",
         allowed="Prospective hypothesis and schema mapping",
         forbidden="SKUs/outlets relabeled apps, shared-user history or claimed measured gain"),
    dict(experiment_id="E68-5", task="Subscription renewal and 7/28 cash revenue",
         datasets="DS68-11;12", data_status="STOP", train_now=False,
         license="Vibrent CC BY4; KKBox terms/access not verified",
         stable_id="Rental keys exist but no billing join; KKBox unknown",
         history="Rental periods not charge periods", labels="Plan metadata != payments",
         zero_missing="Billing eligibility/paid failures absent", time_split="No mature actual-charge target",
         next_material="User-plan assignments, scheduled/actual payments, failures/refunds, consented stable source key",
         allowed="Rental activity audit", forbidden="Price-times-month fabricated subscription revenue"),
]
csvwrite("68_EXPERIMENT_ADMISSION_MATRIX.csv", admissions)

source_table = [
    "# 第68号原始来源与摘录", "", "每个路径是本轮实际保存的公开元数据或可见文档。下载日期/HTTP状态/原响应和保存文件哈希见台账。",
    "不保留网页跟踪脚本、登录信息或逐用户行；JSON字段定位与可见文本行号是核验位置，不是生产代码证据。", "",
    "| 来源ID | 状态 | 原始URL | 本地记录 | SHA256 |", "|---|---:|---|---|---|",
]
for ident, row in sources.items():
    path = row.get("path")
    source_table.append(f"| {ident} | {row.get('status', row.get('error', 'UNKNOWN'))} | {row['url']} | {path or '请求失败，无正文'} | {row.get('sha256', '')} |")
source_table += [
    "", "## 关键原文短摘录", "",
    "| 证据 | 原文 | 位置与证明边界 |", "|---|---|---|",
    '| 手游IAP数据 | “This comprehensive synthetic dataset” | kg-iap-card.json /description；明确合成，排除真实IAP |',
    '| Gamelytics | “real-world-inspired dataset” | kg-gamelytics-card.json /description；不能升级为运营方真实数据 |',
    '| REES46 | “You can use this dataset for free. Just mention the source of it” | jewelry/electronics/cosmetics等card /description；保留数据页与REES46两项署名 |',
    '| Complete Journey | “It contains all of each household’s purchases” | journey-readme.txt；指同零售商选中家庭的采购，不覆盖全市场/真实停止消费 |',
    '| Complete Journey金额 | “Amount of dollars retailer receives from sale” | journey-transactions-manual.txt /sales_value；不能再次把retail_disc加回收入 |',
    '| Criteo金额 | “the revenue obtained when a conversion took place” | criteo-search-data.txt /SalesAmountInEuro；广告主成交额，不是媒体IAA |',
    '| Criteo范围 | “Data has been sub-sampled and anonymized” | criteo-search-data.txt；不能把所有缺交易视为0 |',
    '| Flood-It! | “internal consistency ... might be somewhat limited” | google-game.txt /Limitations；混淆样本不是可认证真实收入 |',
    '| Vibrent | “Now includes pricing data for outfits, and subscription plans” | kg-vibrent-card.json /description；只证明价格元数据，未证明扣款 |',
]
write("public-experiments/round68/SOURCE_CATALOG.md", "\n".join(source_table))

licenses = """# 68号：数据许可与实际可下载性审计

2026-11-20。本轮不使用UCI Online Retail，不训练模型。核验17个候选：许可、真实性和预测准入分开判断。**可公开下载不等于CC0；页面许可不等于数据许可；文件存在不等于足以预测成熟真实价值。**

## 本轮实际取得

| 发行物 | 实际取得与解析 | 许可证据 | 本轮允许范围 |
|---|---|---|---|
| Complete Journey | 官方数据包作者仓库全量RDS，12,775,661字节，1,469,307行；不是75,000行sample | R数据包DESCRIPTION明示CC0，README明确数据包和原84.51°来源；原门户本轮连接失败 | 本地结构/金额/完整性审计；记录上游CC0声明，未把无法访问原门户写成已核验原合同 |
| REES46 Jewelry | 官方平台所链接的发布者Kaggle完整ZIP，CRC通过，95,911行无表头 | Kaggle通用licenseName为“Data files © Original Authors”，但description明确免费使用并要求数据页+REES46双署名 | 符合公开文字的本地使用和聚合审计；不是CC0，不自行授予原始数据再分发/再识别权限 |
| REES46 Electronics | 完整ZIP，52,914,925字节，2,633,521行，CRC通过 | 同上；REES46原站也列出电子交易、珠宝、化妆品等不同数据源 | 聚合审计；缺键/日期/金额问题导致训练STOP |
| Vibrent | 仅3个相关CSV完整下载：original_orders、spot_rentals、subscription_plan | 原作者研究卡声明CC BY4并给出RecSys2024论文 DOI 10.1145/3640457.3688174 | 带论文署名的租赁行为/字段审计，不将套餐价格视为扣款 |
| Cosmetics | October ZIP HTTP200，仅读取262,144压缩字节后停止；提取表头，未保存事件行 | REES46同一免费使用/双署名条款 | 只证明该URL可取到ZIP前缀与字段结构，不是全量下载、时间连续或质量核验 |

准确URL、时间、字节和SHA256见[下载记录](public-experiments/round68/ASSET_ACQUISITION.json)、[电子交易下载](public-experiments/round68/ASSET_ELECTRONICS.json)；原件位于round68/raw，只读使用，不向报告输出原始匿名键。

## 必须停止或保持未知的授权

- Criteo Sponsored Search官方明示CC BY-NC-SA4。本项目商业增长研发不擅自等同NonCommercial，未下载数据；即使获准，它也是广告主转化销售额，不是媒体IAA。
- Olist官方数据为CC BY-NC-SA4。本轮未下载、未训练；多seller不自动构成独立产品/完整用户账本。
- Ta Feng第三方Kaggle页声明CC0，但原始数据授权链未建立。没有用上传者徽章替代原始权利；未下载。
- Google Flood-It!/GA4/UA样本需要可用Cloud项目。未检查或使用任何现有账号凭证、未启用计费、未提交查询。文档页CC BY4/代码Apache2不能代替BigQuery数据条款核验。
- KKBox竞赛data/rules页面HTTP200只返回网页壳，未取得规则正文和文件，不绕过登录/点击同意。
- “Mobile Game IAP 2025”虽CC0但明确合成；Gamelytics虽Apache2但来源仅“real-world-inspired”，累计收入无时间契约；均不准入真实收入研究。
- TikTok Shop第三方卡片声称CC0及多种收入/CAC/ROAS字段，但不是TikTok官方数据，真实经济来源无法核实。不能因字段齐全或营销措辞判为B级。

## 使用与证据范围

仅在各来源内部聚合其既有匿名household/customer/user键；不同来源的同名数字绝不比较或匹配，也不构造个人跨产品ID。不导出逐行键/预测，不抓取真实账号或广告标识。

每次原GET的公开URL、HTTP状态、采集时间、保存文档SHA256和原响应SHA256保留在FETCH_LEDGER系列；保存的是元数据/可见文档转换件，明确区分原响应哈希。二进制跳转仅记主机，不保存临时签名URL。

所有原00—67报告及66/67结果哈希封存。未修改、训练或重新调优UCI数据；未用合成数据补齐任何缺失金额。
"""
write("68_DATASET_LICENSE_AUDIT.md", licenses)

readiness = """# 68号：跨产品迁移准入

**当前结论：已找到并实际取得新的多商店交易候选，但本轮没有两份同时通过全部六项硬门槛的数据。不能开始69号迁移训练。**这个结论不排除参数共享在理论上可行。

## 不需要个人关联的四组对照

| 对照 | 源数据要求 | 目标数据要求 | 是否需要跨产品个人ID | 现在状态 |
|---|---|---|---|---|
| A训练→B零样本测试 | A成熟金额及决策前历史 | B独立时间成熟金额，完全冻结模型 | 否 | STOP：两个产品的标签、观察范围未同时达标 |
| 多源联合→留出B | 至少两个合格源产品，特征/单位一致 | B不能进入标准化、先验或参数选择 | 否 | STOP：不能将门店/SKU、国家、文件分片改名为产品 |
| 只有产品级聚合先验 | 源产品历史cohort统计及可用时间 | 可辨识相似度与固定适配集 | 否 | STOP：聚合不能修复原标签缺失或未知零值 |
| 共享参数+固定B适配 | 源模型、固定源样本/计算预算 | 相同B适配样本量与时间，单独未来测试 | 否 | STOP：还没合格数据，不生成迁移增益 |

以上都只共享统计或参数。各来源键保留独立命名空间，绝不横向join，不把命名空间当模型输入。household≠个人、门店≠独立商家、SKU≠App、Android/iOS≠两款游戏。

## 目前实际候选组合

### REES46珠宝与电子商店

发布者分别描述为medium jewelry store和large home-appliance/electronics store；REES46原站分别列示。两份全量文件真实可下，来源独立于UCI，**是不同业务域的交易发行物**；商家法人是否独立、是否同运营方不明，不能声称已取得两家实名独立企业完整账本。

- 珠宝：2018-12-01—2021-12-01，95,911行；原站旧日期、Kaggle标题和当前文件覆盖不一致。13列无表头，c0是可解析时间，c3/c7/c8的业务语义仍须发布者字段契约确认。候选用户列缺5,352行（5.58%），候选金额也缺5,352行；2,589条完全相同行未被删除。
- 电子：2,633,521行，user_id缺2,069,352（78.58%），price缺431,954（16.40%）；19,631条1970日期和真实2020记录混在一起，现文件覆盖Jan—Nov2020，而卡片写Apr—Nov。不能“删除异常后就叫完整客户”；675条完全重复也不自动等于重复经济事件。
- 两者没有ISO币种/结算/退款/观察缺失契约。禁止把字段名price当已验真的到账收入，禁止将匿名key偶然相同解释为跨店用户。
- 因源A训练标签必须在目标B预测之前成熟，若以后修复成功，可候选使用2019成熟珠宝窗训练→2020电子未来窗测试；逆方向仅可用2020电子成熟窗口→之后的珠宝窗。不能先用2021珠宝后验训练再预测2020电子，不能把用户历史跨年拼接。
- 目前为STOP，不按这几个例子实际执行。

### Complete Journey与其他零售

1,469,307行、2,469个家庭、457门店、68,509个SKU、155,848个basket。数据包作者明确全量采购，sales_value有金额定义、无缺键，最接近可继续核验的单产品候选。它是2017年的一个零售商家庭面板；多门店不能冒充多App。

若与2019—2021商店做迁移，需要先统一家庭/客户统计单位、币种/价格水平、折扣与退款口径、品类复购周期以及观察机制。跨年份、渠道、品类三种漂移与“共享知识增益”不可混为一谈。只有两域时，A→B一次成功不证明一般迁移，更不能证明游戏迁移。

## 严格零值与可执行替代的区别

Complete Journey“所选家庭全部采购”的声明支持**发布账本范围内无记录**的候选零标签。但数据没有家庭在观察起止、退出、漏传/门店覆盖的信息，不能分辨真实无购买与该家庭的观测缺失。全库某天无记录不自动说明系统故障，也不自动说明停业。日期长度只能证明event-time上可取窗口，不能证明真实到达或完整成熟。

本轮按要求停止训练。未来若研究者选择改为“给定发布账本的记录金额”而非真实未来消费，可单独预注册为**范围更窄的新问题**，不能默默放宽本轮门槛、沿用真实零值/完整LTV措辞。本轮没有执行该替代。

## 达标后才适用的实验设计

1. 每产品分别建立源内客户landmark，只纳入当时已可观察且完整覆盖未来窗口的风险集；历史严格早于t，标签[t,t+7/28天)。不凭未来购买挑客户。
2. 源训练标签全部在目标预测前成熟；客户分桶与时间隔离，target校准/适配/测试互斥。目标测试不参与标准化、先验、相似性、阈值或调参。
3. 固定产品与样本量/计算预算；比较目标单域、源聚合先验、共享参数、共享参数+适配。两域不能凑leave-one-game-out；多域后再leave-one-product-out。
4. 统一价格口径或独立报告原币；不在测试未来均值上缩放。分层报告零值、金额长尾、品类/国家、观察覆盖和时间漂移。
5. 同时报告MAE/RMSE、校准、Top10%召回/金额捕获，客户cluster及时间块不确定性、负迁移；不报告IAA/IAP、真实竞价ROAS、平台增益或因果收益。

## 69号建议

**值得继续数据修复/准入，不值得现在训练。**优先材料：

1. REES46珠宝原生表头/数据字典、电子日期异常与缺键解释、匿名ID作用域及币种/订单/退款定义。
2. 每个候选的完整观察区间、漏传/停采/客户退出标记与实际全量范围，用来区分账本零与未知。
3. 至少第二个同时具备上述条件的数据产品；不要用UCI旧数据、同商家GA4/UA、同商店SKU或套餐价格补数。

如无法公开取得这些材料，应停止当前跨产品金额训练方向；保留已有元数据/聚合审计，而不是通过堆模型绕过数据缺口。
"""
write("68_CROSS_PRODUCT_TRANSFER_READINESS.md", readiness)

report = f"""# 68：全新公开数据源与跨产品用户价值迁移审计

2026-11-20。**找到新的独立零售交易发行物与不同商店候选，但没有找到已满足严格准入的真实游戏收入数据，也没有两份可以立即开展跨产品真实金额训练的数据。**本轮是数据发现和原件审计，训练数0；没有读取UCI原始数据、训练或调优旧模型。

## 1. 结果概览

| 核验对象 | 本轮结果 | 证据层级 |
|---|---|---|
| 独立真实游戏IAA/IAP | 已审候选中，合格A级0；Google官方游戏demo混淆，手游IAP明确合成，Gamelytics缺真实来源/事件时间 | 【官方文档证实】【公开发布者声明】【仍无证据】 |
| 真实媒体广告收入 | 合格B级0；Criteo有真实流量转化金额说明，但那是广告主销售额且NC受限 | 【官方文档证实】，不升级为IAA |
| 新真实零售 | Complete Journey全量RDS解析：{journey['rows']:,}行，2,469家庭 | 【公开发行文件证实】，单零售商面板 |
| 多商店候选 | 珠宝{jewelry['rows']:,}行、电子{electronics['rows']:,}行，完整ZIP与CRC实核 | 【公开发行文件证实】，当前质量/语义STOP |
| 订阅 | Vibrent三个CSV可下，但套餐价格不等于扣款；KKBox规则/data仅页面壳 | 【公开发行文件证实】【无法确认】 |
| 跨产品迁移 | 不关联个人身份在理论上可行；当前0组通过全部训练门槛 | 【机制可行性】，不是实验结果 |

审计17个具名候选，保留{len(sources)}条URL请求台账。完整取得6个相关发行文件，来自4个数据源：Complete Journey、Jewelry、Electronics、Vibrent（3表）；Cosmetics只取ZIP前缀/表头，不能算完整数据集。原包只留本地，不在报告输出任何匿名用户行。

交付：[逐数据清单](68_DATASET_CATALOG.csv)、[许可审计](68_DATASET_LICENSE_AUDIT.md)、[迁移准入](68_CROSS_PRODUCT_TRANSFER_READINESS.md)、[实验矩阵](68_EXPERIMENT_ADMISSION_MATRIX.csv)。

## 2. 分级：真实性优先于名字

- **A级**须是真实游戏收入与玩家行为，不是“real-world-inspired”、游戏市场总额或合成whale标签。Flood-It!来自真实游戏产品，但官方明确样本混淆和占位，且本轮未执行BigQuery查询，不能给其未见金额A级认证。
- **B级**须真实媒体展示收入及展示记录。Criteo Sponsored Search的SalesAmountInEuro是广告主的归因成交额，不能记为IAA、媒体CPM收入或用户D28 LTV。点击、出价、花费也不是广告主游戏的收入。
- **C级**为真实零售/订阅交易。Complete Journey有明确定义的sales_value；REES46声明来源为交易，但原件缺键/语义问题仍要单列。Vibrent只验证了租赁行为与标价，未通过真实订阅收入标签。
- **D级**为点击/安装/列表/行为代理。Google Play listing的Price×Installs不能造实际销售额。真实购买事件中的价格与view/cart上下文价格也必须区分。
- 合成/来源不明单列，不为了四级齐全把它们放进A级或B级。

## 3. 从原件发现的新问题

### Complete Journey：真正独立于UCI的金额面板

发布方为84.51° Complete Journey study，R数据包作者Brad Boehmke与Steven Mortimer公开发行。DESCRIPTION明确CC0，README指明完整家庭采购；下载函数定位data/transactions.rds而非75,000行sample。实际全量{journey['rows']:,}行、{journey['households']:,}家庭、{journey['stores']:,}门店、{journey['baskets']:,}basket，无字段缺失、完全重复0。

时间为2017-01-01 11:53:26至2018-01-01 04:01:20的UTC表示，R POSIXct按epoch秒转换；本地运营时区未认证。366日历跨度、365天有记录，不能将无记录日自动认作系统故障或真实零。sales_value定义为零售商收到的dollars，不是标价、游戏IAA或净利润；11,226条非正sales_value（负数0）、8,869条quantity=0保留审计，没有盲删。

它支持“同一零售商选中家庭、发布账本范围内”的候选未来7/28天任务；不能从无缺字段推导无缺事件。缺少家庭观察区间、漏采/退出与真实到达时间，所以按本轮严格“零值vs缺失”要求，训练仍STOP。[文件核验](public-experiments/round68/AUDIT_JOURNEY.json)

### 两份REES46交易：可下载，不等于可训练

官方REES46 datasets页面列示Jewelry、Electronics等不同零售域，Kaggle原发布者给出免费使用与双署名。不是只有下载链接：两份ZIP实际完整取得、CRC正确，哈希见[原包台账](public-experiments/round68/ASSET_ELECTRONICS.json)及[初始原包](public-experiments/round68/ASSET_ACQUISITION.json)。

| 项目 | 珠宝 | 电子 |
|---|---:|---:|
| 全量行 | 95,911 | 2,633,521 |
| 原生表头 | 无（13列） | 有（8列） |
| 用户键缺失 | 候选c8缺5,352，语义待证 | user_id缺2,069,352，78.58% |
| 金额缺失 | 候选c7缺5,352 | price缺431,954，16.40% |
| 完全相同行 | 2,589 | 675 |
| 时间问题 | 当前实际2018-12—2021-12，与原站旧日期不一致 | 19,631条1970，其他Jan—Nov2020，与卡片Apr—Nov冲突 |
| 真实零与缺失 | 未区分 | 未区分 |

珠宝不能默认第一行是表头，否则会丢失1条记录并把匿名行内容写成字段名；本轮按header=None保留95,911行，列语义不凭名字猜。[珠宝审计](public-experiments/round68/AUDIT_JEWELRY.json)

电子1970日期能被解析，并不代表合法业务时间：初审invalid_times=0只是解析器状态。异常19,631行单独揭示，没有静默过滤后声称连续成熟。其78.58%缺键远大于一般噪声，完整病例训练会改变人群；无缺失机制说明就不能把未见消费设0。[电子审计](public-experiments/round68/AUDIT_ELECTRONICS.json)

### Vibrent：价格表不能造收入

RecSys2024原作者公开CC BY4，实际取得12,558条原始租赁记录、3,928条spot租赁和58条订阅套餐价格。分隔符是分号；用默认逗号会错误读成一列，已纠正解析。原始表有5,438客户键，spot表没有客户键；所取表没有逐用户套餐绑定、实际扣款、续费失败或退款账本。pricing.pricePerMonth.amount不证明真实收入，不能乘租赁月份造未来消费。[订阅核验](public-experiments/round68/AUDIT_VIBRENT.json)

## 4. A/B级优先搜索的反证

1. [Google游戏官方文档]({url('google-game')})明确114天、obfuscated、placeholders及internal consistency限制。GA4通用schema具有event_value_in_usd，并不证明Flood-It!每种事件的真实金额、IAA覆盖或零收入安装分母。未使用Cloud凭证或查询权限。
2. [手游IAP卡片]({url('kg-iap-card')})原文“comprehensive synthetic dataset”；CC0解决不了真实性，SpendingSegment还可能直接编码目标。没有为此下载伪真实训练样本。
3. [Gamelytics]({url('kg-gamelytics-card')})实际文件清单只有reg_data、auth_data、ab_test。前两表有时间，收入表只有user_id/revenue/testgroup；uid与user_id不构成已证同一人契约，不能把累计A/B收入拆成未来28天。
4. [Criteo Sponsored Search]({url('criteo-search-data')})确有SalesAmountInEuro、time_delay_for_conversion、partner_id与user_id官方定义，反而是最有价值的“真实广告流量+归因金额”线索。但它是90天抽样点击、非媒体IAA，且CC BY-NC-SA4当前用途未获准，不下载训练。
5. Google Play列表、TikTok Shop第三方卡片、Kaggle“收入”搜索结果都不足以证明真实事件账本。KKBox的HTTP200页面壳不算规则或文件已取得；Ta Feng再托管CC0不算原始授权。

## 5. 不用个人跨App身份，能否研究迁移

**理论上可以。**同一套历史金额/次数/recency等特征、源产品cohort先验或模型参数可在不同产品共享；客户只在各自命名空间内计算，不需要连接个人。跨商店A→B要验证的是共享规律，绝不是“同一玩家过去在别的游戏花了多少钱”。

当前A→B、联合训练→留出、聚合先验、共享参数+适配均STOP。源产品历史标签要先成熟，再到目标预测时点；产品字典/价格归一化不能读目标未来统计；门店、SKU、品类、平台和数据分片不能假装独立App。具体比较与恢复条件见[迁移准入](68_CROSS_PRODUCT_TRANSFER_READINESS.md)。

## 6. 实验准入与69号

六项硬条件分别检查：许可、稳定源内用户键、历史跨度、成熟真实金额、零值与缺失可分、严格时间外切分。发现某个时间跨度够长不能跳过另外五项。六个实验问题没有一个获准本轮训练；Complete Journey仅LIMITED_AUDIT_ONLY，不是训练GO。

**69号建议：先做“REES46/Complete Journey字段契约与观测覆盖补证”，不要现在做迁移模型。**优先补两商店字段字典/异常日期和缺键说明、准确货币及退款/订单金额契约、客户观察区间/停采标记。若公开原件和作者说明仍无法提供，就停止真实零值/成熟未来价值迁移；可以另议发布账本范围内的受限问题，但不能悄悄换目标。

## 7. 最终五个答案

1. **独立新游戏收入数据？**找到官方游戏demo和若干候选，但真正通过A级真实性、许可、稳定键与成熟标签门槛的0个；B级媒体IAA也0个。不是证明全网没有，而是本轮范围内未建立。
2. **可用多产品收入数据？**找到并取得珠宝/电子不同商店交易，外加独立Complete Journey面板；当前没有两份同时满足训练准入。已取得多源不等于“已取得可用多产品LTV标签”。
3. **无需个人跨App身份的迁移？**方法上可行，当前数据条件下只准做设计与审计，不能报告效果。
4. **哪些支持未来收入？**Complete Journey最接近支持发布账本未来7/28金额；REES46有潜在时间跨度但质量/语义/零值缺口阻止认证；Vibrent、合成IAP、A/B累计收入、混淆demo均不满足本轮真实未来收入目标。
5. **值得69号？**值得有限补证与数据修复，暂不值得启动跨产品训练。没有合格数据则保持STOP，不用UCI、合成数据或大量模型补足。

## 8. 原证据与保留

[原始URL/短摘录/哈希目录](public-experiments/round68/SOURCE_CATALOG.md)、[下载脚本](public-experiments/round68/acquire_assets68.py)、[结构审计脚本](public-experiments/round68/audit_assets68.py)。rdata1.1.0只安装在本轮私有依赖目录，用于读取官方RDS，没有改原数据和既有实验环境。

审计脚本不训练、不输出个人键、不跨数据集匹配、不提交广告或归因事件；只GET公开文档/数据。没有检索Rotate/Meow旧来源，没有调用未经授权Cloud/商业后台。原00—67与66/67结果字节锁定，主证据图以新增节点和边扩展，旧对象原样保留。
"""
write("68_全新公开数据源调查.md", report)

# Extend only the main graph; preserve every original object and metadata field.
graphpath = ROOT / "prediction-system/EVIDENCE_GRAPH.json"
before = load("EVIDENCE_GRAPH.before68.json")
graph = json.loads(graphpath.read_text(encoding="utf-8-sig"))
assert graph == before
new_sources = []
for ident, record in sources.items():
    if not record.get("path"):
        continue
    new_sources.append(dict(
        id="PD68S_" + ident.replace("-", "_"), path=record["path"], sha256=record["sha256"],
        url=record["url"], source_date=record["observed_utc"], http_status=record.get("status"),
        evidence_level="【官方/公开发布元数据或文档】", production_actual_proven=False,
        scope="Dataset availability/license/semantics; no target-game delivery or model consumption",
        authorization="Unauthenticated public document/metadata access",
    ))
for name in ["AUDIT_JOURNEY.json", "AUDIT_JEWELRY.json", "AUDIT_ELECTRONICS.json", "AUDIT_VIBRENT.json"]:
    new_sources.append(dict(
        id="PD68S_" + name[:-5].lower(), path=(OUT / name).relative_to(ROOT).as_posix(),
        sha256=sha(OUT / name), source_date=NOW, evidence_level="【公开发行文件聚合审计】",
        production_actual_proven=False, scope="Source-local aggregate DQ only; no real-person IDs/export or training",
    ))
new_nodes = [
    dict(id="PD68_game_candidates", label="New game/IAA income candidates not admitted", stage="data_audit"),
    dict(id="PD68_new_retail", label="Independent full Complete Journey receipt panel", stage="public_data"),
    dict(id="PD68_multistore", label="REES46 jewelry/electronics complete releases, defects verified", stage="public_data"),
    dict(id="PD68_rental", label="Vibrent rental and plan metadata, not a payment ledger", stage="data_audit"),
    dict(id="PD68_transfer", label="Cross-product value transfer without personal joining: not yet admitted", stage="hypothesis"),
    dict(id="PD68_stop", label="Strict real-zero/mature-value training remains STOP", stage="admission_decision"),
]


def sourceid(ident):
    return "PD68S_" + ident.replace("-", "_")


new_edges = []


def edge(ident, start, end, claim, refs, status, gap, permissions):
    new_edges.append(dict(
        id=ident, source=start, target=end, claim=claim, source_ids=refs, status=status,
        evidence_level="【公开发行文件/文档证实】" if status == "audit_confirmed" else "【仍无证据】",
        reviewed_utc=NOW, diagram_style="solid" if status == "audit_confirmed" else "dashed",
        edge_type="independent_public_dataset_readiness", missing_evidence=gap,
        permission_conditions=permissions, production_actual_proven=False,
        observed_target_game_delivery=False, server_model_training=False,
        six_layers=dict(sdk_capability=False, actual_game_business_callsite=False,
                        request_construction_code=False, production_successful_send=False,
                        server_received=False, server_model_training=False),
    ))


edge("PD68E1", "PD68_game_candidates", "PD68_stop",
     "No audited new genuine game/IAA cohort admitted; synthetic/obfuscated/time/license gaps explicitly retained",
     [sourceid(x) for x in ["google-game", "kg-iap-card", "kg-gamelytics-card", "criteo-search-data"]],
     "audit_confirmed", "Authorized original mature game revenue and observable zero population", "No NC dataset use or Cloud account queries")
edge("PD68E2", "PD68_new_retail", "PD68_stop",
     "Complete one-year 1469307-row household receipt panel exists; observed-zero and missingness remain distinct",
     [sourceid("journey-description"), sourceid("journey-readme"), "PD68S_audit_journey"],
     "audit_confirmed", "Household observation/exit/outage coverage and precise target scope", "CC0 data-package declaration; local aggregate audit only")
edge("PD68E3", "PD68_multistore", "PD68_transfer",
     "Two retail domains have complete public files, but missing keys, header/date/currency defects block valid transfer claims",
     ["PD68S_audit_jewelry", "PD68S_audit_electronics", sourceid("rees46-datasets")],
     "audit_confirmed", "Publisher field dictionary, observation coverage, same accounting contract",
     "Free use with data-page and REES46 attribution; no personal cross-source matching")
edge("PD68E4", "PD68_rental", "PD68_stop",
     "Subscription plan prices and rental periods do not prove observed recurring charges",
     ["PD68S_audit_vibrent", sourceid("kg-vibrent-card")], "audit_confirmed",
     "Customer payment/renewal/refund ledger and observation eligibility", "CC BY4 with original paper citation")
edge("PD68E5", "PD68_transfer", "PD68_stop",
     "No trained shared-value model or empirical transfer gain in round68; hypothetical parameter sharing needs no personal identity join",
     ["PD68S_audit_jewelry", "PD68S_audit_electronics", "PD68S_audit_journey"], "unknown",
     "At least two fully admitted products, preregistered time/customer split and common targets",
     "No cross-product user key construction; no raw UCI use or training")
for key, items in [("nodes", new_nodes), ("edges", new_edges), ("sources", new_sources)]:
    assert not ({x["id"] for x in graph[key]} & {x["id"] for x in items})
    graph[key].extend(items)
graph["public_data_round68"] = dict(
    reviewed_utc=NOW, report="68_全新公开数据源调查.md", candidates=17,
    new_game_training_datasets_admitted=0, publisher_iaa_training_datasets_admitted=0,
    cross_product_training_pairs_admitted=0, model_fits=0, uci_raw_used=False,
    data_status="New complete retail release evidence; strict training STOP",
    new_node_ids=[x["id"] for x in new_nodes], new_edge_ids=[x["id"] for x in new_edges],
    new_source_ids=[x["id"] for x in new_sources],
)
graphpath.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(OUT / "NEW_GRAPH_OBJECTS.json").write_text(json.dumps(dict(
    nodes=new_nodes, edges=new_edges, sources=new_sources), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

index = ROOT / "EVIDENCE_INDEX.md"
assert index.read_bytes() == (OUT / "EVIDENCE_INDEX.before68.md").read_bytes()
addition = """

<a id="pd68"></a>

## PD68 · 全新公开数据源与跨产品迁移准入

- [68号报告](68_全新公开数据源调查.md)、[17候选目录](68_DATASET_CATALOG.csv)、[许可审计](68_DATASET_LICENSE_AUDIT.md)
- [跨产品准入与69建议](68_CROSS_PRODUCT_TRANSFER_READINESS.md)、[6项实验矩阵](68_EXPERIMENT_ADMISSION_MATRIX.csv)
- [原始来源/摘录/哈希](public-experiments/round68/SOURCE_CATALOG.md)、[完整数据下载记录](public-experiments/round68/ASSET_ACQUISITION.json)、[电子交易原包](public-experiments/round68/ASSET_ELECTRONICS.json)
- [Complete Journey](public-experiments/round68/AUDIT_JOURNEY.json)、[珠宝](public-experiments/round68/AUDIT_JEWELRY.json)、[电子](public-experiments/round68/AUDIT_ELECTRONICS.json)、[租赁](public-experiments/round68/AUDIT_VIBRENT.json)
- [最终保留与结构校验](public-experiments/round68/VALIDATION68.json)

新证据：取得独立Complete Journey全量1469307行及两个商店完整交易发行物；电子缺键78.58%、金额缺16.40%及1970异常，珠宝无表头，Vibrent套餐标价非扣款。A级真实游戏/B级媒体IAA准入均0，当前跨产品训练组合0；不关联个人ID的参数/聚合迁移可设计但未执行。严格零值/观测缺失门槛未满足，69号先补证不训练；无UCI原始使用、无新增模型结果、无Axon/Vector效果主张。旧对象与历史报告原样保留。
"""
with index.open("ab") as f:
    f.write(addition.encode("utf-8"))
experiment_index = ROOT / "public-experiments/EXPERIMENT_INDEX.md"
with experiment_index.open("a", encoding="utf-8", newline="\n") as f:
    f.write("\n\n## 68：独立新数据审计，训练STOP\n\n"
            "- [报告](../68_全新公开数据源调查.md)、[17候选](../68_DATASET_CATALOG.csv)、[准入矩阵](../68_EXPERIMENT_ADMISSION_MATRIX.csv)\n"
            "- [跨产品方案与恢复条件](../68_CROSS_PRODUCT_TRANSFER_READINESS.md)、[源证据](round68/SOURCE_CATALOG.md)\n"
            "- 已取得Complete Journey和REES46两商店原件，未满足两产品完整金额/零值门槛；无训练、无旧UCI使用、无平台/手游外推。\n")
print(json.dumps(dict(deliverables=5, candidates=len(catalog), experiments=len(admissions),
                     graph_additions={k: len(v) for k, v in [
                         ("nodes", new_nodes), ("edges", new_edges), ("sources", new_sources)]},
                     model_fits=0), ensure_ascii=False))
