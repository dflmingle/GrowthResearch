"""Source-local aggregate quality audit only: no training, prediction or ID export."""
from pathlib import Path
import hashlib, io, json, re, sys, warnings, zipfile
import numpy as np
import pandas as pd

OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(OUT / ".deps"))


def csvfile(name):
    path = OUT / "raw" / (name + ".download")
    if zipfile.is_zipfile(path):
        archive = zipfile.ZipFile(path)
        assert archive.testzip() is None
        member = archive.namelist()[0]
        body = archive.read(member)
        return io.BytesIO(body), dict(member=member, member_bytes=len(body),
                                    member_sha256=hashlib.sha256(body).hexdigest(),
                                    archive_crc_verified=True)
    return path, dict(member="plain CSV", member_bytes=path.stat().st_size,
                      member_sha256=hashlib.sha256(path.read_bytes()).hexdigest())


def period_summary(times):
    valid = pd.to_datetime(times, errors="coerce", utc=True).dropna()
    daily = valid.dt.floor("D").value_counts().sort_index()
    all_days = pd.date_range(daily.index.min(), daily.index.max(), freq="D")
    return dict(min_timestamp=valid.min().isoformat(), max_timestamp=valid.max().isoformat(),
                observed_days=len(daily), calendar_span_days=len(all_days),
                days_without_any_dataset_row=int(len(all_days.difference(daily.index))),
                monthly_rows={str(k): int(v) for k, v in valid.dt.strftime("%Y-%m").value_counts().sort_index().items()},
                available_at_present=False, completeness_watermark_present=False)


def audit_jewelry():
    src, provenance = csvfile("jewelry")
    # First field is a timestamp, not a header. Do not use a row of IDs as names.
    df = pd.read_csv(src, header=None, dtype="string")
    assert df.shape[1] == 13
    dates = pd.to_datetime(df[0], errors="coerce", utc=True)
    assert dates.notna().all()
    price = pd.to_numeric(df[7], errors="coerce")
    quantity = pd.to_numeric(df[3], errors="coerce")
    ids = df[8]
    return dict(
        artifact="jewelry", provenance=provenance, rows=len(df), columns=13,
        header_present=False, first_row_preserved=True,
        field_mapping_status="Timestamp at c0 observed; c3 quantity/c7 price/c8 user key are positional hypotheses, not a verified publisher schema",
        period=period_summary(dates),
        candidate_user_missing=int(ids.isna().sum()), candidate_user_unique=int(ids.nunique()),
        candidate_amount_missing=int(price.isna().sum()), candidate_amount_nonpositive=int(price.le(0).sum()),
        candidate_quantity_missing=int(quantity.isna().sum()),
        exact_repeated_rows=int(df.duplicated().sum()),
        no_records_deduplicated=True, user_keys_parsed_as_strings=True,
        currency="UNKNOWN; do not infer from website geography",
        customer_active_spells="ABSENT", zero_vs_missing="UNRESOLVED",
        training_admitted=False, raw_keys_or_rows_exported=False,
    )


def audit_electronics():
    src, provenance = csvfile("electronics")
    df = pd.read_csv(src, dtype={"user_id": "string", "order_id": "string"})
    assert "event_time" in df and "price" in df and "user_id" in df
    dates = pd.to_datetime(df.event_time, errors="coerce", utc=True)
    price = pd.to_numeric(df.price, errors="coerce")
    keys = df.user_id
    # Only within this release; never compared with another product's IDs.
    counts = keys.dropna().value_counts()
    return dict(
        artifact="electronics", provenance=provenance, rows=len(df), columns=list(df),
        dtypes={k: str(v) for k, v in df.dtypes.items()},
        missing={k: int(v) for k, v in df.isna().sum().items()},
        period=period_summary(dates), invalid_times=int(dates.isna().sum()),
        distinct_source_user_keys=int(keys.nunique()),
        users_with_multiple_rows=int(counts.ge(2).sum()),
        exact_repeated_rows=int(df.duplicated().sum()), no_records_deduplicated=True,
        amount_nonpositive=int(price.le(0).sum()), amount_missing=int(price.isna().sum()),
        amount_max=float(price.max()), amount_median=float(price.median()),
        currency="UNKNOWN in verified card/header; price is not certified net cash",
        quantity_field_present="quantity" in df, transaction_id_present="order_id" in df,
        customer_active_spells="ABSENT", zero_vs_missing="UNRESOLVED",
        refunds_or_payment_status_present=any(x in df for x in ["refund", "payment_status", "is_cancelled"]),
        training_admitted=False, raw_keys_or_rows_exported=False,
    )


def audit_vibrent():
    results = {}
    for name in ["vibrent-orders", "vibrent-plans", "vibrent-spot"]:
        src, provenance = csvfile(name)
        df = pd.read_csv(src, sep=";", dtype="string")
        entry = dict(rows=len(df), columns=list(df), provenance=provenance,
                     delimiter="semicolon", missing={k: int(v) for k, v in df.isna().sum().items()})
        if "customer.id" in df:
            entry["distinct_source_customer_keys"] = int(df["customer.id"].nunique())
        for col in ["rentalPeriod.start", "rentalPeriod.end"]:
            if col in df:
                entry[col] = period_summary(df[col])
        entry["actual_payment_ledger_present"] = False
        results[name] = entry
    return dict(
        artifact="vibrent", tables=results,
        price_semantics="Subscription plan price metadata, not observed recurring customer charges",
        join_gap="No verified per-user plan assignment/payment-time/paid/refunded record in downloaded tables",
        subscription_renewal_prediction_admitted=False, training_admitted=False,
        raw_keys_or_rows_exported=False,
    )


def audit_journey():
    import rdata
    with warnings.catch_warnings(record=True) as caught:
        df = rdata.read_rds(OUT / "raw/completejourney.download")
    # R POSIXct is epoch seconds; retain UTC as file time representation, not physical storefront timezone.
    dates = pd.to_datetime(df.transaction_timestamp, unit="s", utc=True)
    amounts = pd.to_numeric(df.sales_value, errors="coerce")
    return dict(
        artifact="completejourney", reader="rdata " + rdata.__version__,
        rds_conversion_warnings=sorted({str(w.message) for w in caught}),
        time_decode="R POSIXct epoch seconds -> UTC representation; operational timezone not certified",
        rows=len(df), columns=list(df),
        missing={k: int(v) for k, v in df.isna().sum().items()}, period=period_summary(dates),
        households=int(df.household_id.nunique()), stores=int(df.store_id.nunique()),
        products=int(df.product_id.nunique()), baskets=int(df.basket_id.nunique()),
        exact_repeated_rows=int(df.duplicated().sum()), no_records_deduplicated=True,
        nonpositive_sales_value=int(amounts.le(0).sum()), negative_sales_value=int(amounts.lt(0).sum()),
        zero_quantity=int(df.quantity.eq(0).sum()), amount_max=float(amounts.max()),
        amount_semantics="sales_value: dollars retailer receives from sale, per publisher receipt-line documentation",
        currency="Dollars per publisher; ISO currency code not present",
        multiple_independent_products=False, explanation="store_id outlets and product_id SKUs are not independent apps/merchants",
        documentation_full_purchase_panel=True,
        customer_active_spells="ABSENT", zero_vs_missing="Source-wide all-purchase claim supports ledger-zero only; per-household outages/exit not identifiable",
        conditional_ledger_value_task="Plausible after defining observation coverage; no real-zero certification",
        training_admitted=False, raw_keys_or_rows_exported=False,
    )


if __name__ == "__main__":
    functions = [audit_jewelry, audit_electronics, audit_vibrent, audit_journey]
    for fn in functions:
        name = fn.__name__.removeprefix("audit_")
        destination = OUT / ("AUDIT_" + name.upper() + ".json")
        if destination.exists():
            raise RuntimeError("Preserve existing audit: " + str(destination))
        result = fn()
        destination.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"audit": name, "status": "COMPLETE", "rows": result.get("rows"),
                          "training_admitted": result.get("training_admitted")}), flush=True)
