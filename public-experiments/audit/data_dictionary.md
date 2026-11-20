# Data dictionary

Source: licensed export of a commercial app-market data vendor, pulled 2026-09-24 (`data/raw/`, not
redistributed). Two apps, Pokémon GO and
Pikmin Bloom, on iOS and Android, 111 countries plus an all-countries total ("所有"), monthly from 2014-01 to
2026-09. September 2026 is partial, so the analysis sample ends at **2026-08**.

## `data/processed/panel.parquet` — one row per game × platform × country × month

| Column | Type | Meaning |
| --- | --- | --- |
| `game` | str | `PoGO` (Pokémon GO) or `Pikmin` (Pikmin Bloom) |
| `platform` | str | `iOS` or `Android` (from the app id: `com.*` is Android) |
| `country` | str | ISO 3166-1 alpha-2 code (111 countries) |
| `month` | date | First day of the month |
| `revenue` | float | Gross in-app revenue, USD (missing → 0) |
| `downloads` | float | New installs (missing → 0) |

**Scope (research plan, 2026-09-29): revenue and downloads only.** The export has 16 columns; `hf.data.load_raw`
drops every other measure (DAU, session length, sessions per user, ARPDAU, time spent, cumulative revenue per
download) as soon as the file is read, so they cannot enter a model, a feature or the entry dates.
`hf.data.validate` checks that country rows sum to the all-countries total (revenue and downloads, exactly) and
that neither measure is negative.

## `data/processed/entry.csv` — one row per bottom series

| Column | Meaning |
| --- | --- |
| `game`, `platform`, `country` | Bottom-series key |
| `entry_month` | First month with revenue or downloads above zero |
| `entry_type` | `launch_wave` (entry by 2017-01 for PoGO, 2021-11 for Pikmin; 316 series), `coverage_expansion` (≥5 series of the same game appearing in the same later month, which is the data vendor widening coverage rather than a launch; 60), `late_entry` (other later entries; 45) |

## Hierarchy (`hf.hierarchy`)

Grouped structure world → game → {platform, country} → platform × country. Bottom series start at their
entry month (no zero padding before entry). At each forecast origin only bottoms with at least 6 months of
history are included, and bottoms that are zero over the whole train + test window are dropped (which
changes no aggregate and no scaled metric). In the pilot window 2021-10..2026-08 with zero padding the
hierarchy has 620 revenue series (1/2/4/216/397 by level) and 629 download series (1/2/4/211/411).

## `data/external/events.csv` — dated events (176 rows)

`game, event_type, event_name, start_date, end_date, scope, countries, source_url, confidence, notes`.
Event types: country_launch, anniversary, global_ticketed_event, season_start, monetization_change,
feature_launch, covid_policy, other. Every row cites a source; see `events_README.md` for gaps.

## Forecast files (`experiments/*/forecasts/*.parquet`)

Long schema, one row per series × month × base model × reconciliation method:
`target, origin, unique_id, level, ds, h, model, method, mean, lo80, hi80, lo95, hi95`.
`method = base` is the unreconciled forecast. Point-only models (Croston variants) have empty interval columns.

## Score, weight and monthly-loss files

`experiments/<exp>/scores/<tag>.parquet`: one row per series × origin × model × method with MASE, RMSSE, sCRPS,
cov80/95, width80/95 (interval width divided by the MASE scale), MSIS95, neg_share; `_hb` files split by horizon
bucket. `experiments/<exp>/weights.parquet`: `target, origin, unique_id, level, weight`, each series' share of its
level total over the 12 months up to the origin. `experiments/<exp>/monthly/<tag>.parquet`: weighted loss sums
per `target, origin, level, model, method, ds` (`w_sse, wsum_sse, w_scrps, wsum_scrps`) for the panel DM test.

## Foundation-model files

`data/processed/fm_inputs.parquet` (`python -m hf.fm prepare`): `target, origin, unique_id, ds, y`, the training
part of every node of the per-origin hierarchy, i.e. exactly the contexts the statistical baselines see. The Colab
job `jobs/p2_fm_colab` returns `fm_forecasts_<model>.parquet` (`target, origin, model, unique_id, ds, h,
q0.025, q0.1, q0.5, q0.9, q0.975`) and `fm_fitted_<model>.parquet` (rolling one-step-ahead medians over the 24
months before each origin, used as in-sample residuals). `python -m hf.fm score` reconciles and scores them
with the P1 code.
