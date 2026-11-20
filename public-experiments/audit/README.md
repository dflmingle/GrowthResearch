# mobile-game-hf

Code for the study "Forecasting mobile game revenue and downloads across markets and platforms: evaluating the
components of a lifecycle-aware hierarchical probabilistic framework" (Yu-Chin Chen, Taiwan Steel University of Science and Technology).
Archived on Zenodo: https://doi.org/10.5281/zenodo.23133797 (version 1.0.0).

The study forecasts monthly revenue and downloads of Pokémon GO and Pikmin Bloom for a grouped hierarchy (world,
game, game × platform, game × country, game × platform × country; about 620 series per measure), compares
statistical, gradient-boosting, deep-learning and time-series foundation models with eight reconciliation methods,
and evaluates the three components of a lifecycle-aware framework separately: life-cycle and event conditioning of
global models (A), transfer from the older to the younger game (B) and non-negative sample-path reconciliation (C).

## Data

The study uses monthly estimates licensed from a commercial app-market data vendor (two games, iOS and Android, 111
markets, July 2016 to August 2026).
The export is licensed and **may not be redistributed. This archive contains code only: no data and no results
derived from the data.** Researchers with their own access can rebuild the panel with
`python -m hf.data --raw <export>.xlsx --out data/processed` (columns and checks: `docs/data_dictionary.md`).

Without the data, `python -m hf.synth --out data/synthetic` writes a simulated panel with the same structure (two
games with their launch months, two platforms, the 111 market codes, staggered market entry, scales over four orders
of magnitude, sparse small series, event spikes). Every value is simulated; results on it say nothing about the real
games. Every module that reads the panel accepts `--data data/synthetic`.

`data/external/events.csv` is the calendar of scheduled events used as covariates. It was compiled from public
announcements and gives a source for every event (`data/external/events_README.md`).

## Contents

| Path | Content |
| --- | --- |
| `src/hf/` | data pipeline, hierarchy, base models, LightGBM, deep and foundation models, reconciliation (incl. component C), evaluation, model selection, significance tests, event-month and stress analyses, robustness, SHAP and error decomposition, synthetic data |
| `tests/` | pytest suite (tests that need the licensed data are skipped without it) |
| `jobs/` | definitions of the GPU jobs (run on Google Colab, NVIDIA L4) for foundation and deep models, and local run scripts |
| `configs/`, `docs/` | settings of the baseline run; description of the data export |
| `data/external/` | event calendar |

## Setup (Linux or WSL, Python 3.11)

```bash
sudo apt-get install -y libgomp1   # OpenMP runtime for LightGBM
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
```

Foundation and deep models need a GPU; their requirements are listed in `jobs/p2_fm_colab/` and
`jobs/p6_models_colab/` (Moirai 2.0 runs in a separate Python 3.11 environment, see `jobs/p6_models_colab/job.py`).

## Quick start on the synthetic panel (CPU)

```bash
export PYTHONPATH=src
python -m hf.synth --out data/synthetic
python -m hf.baselines --data data/synthetic --target revenue --split all --models fast --out experiments/p1
python -m hf.baselines --data data/synthetic --target downloads --split all --models fast --out experiments/p1
python -m hf.rescore --exp experiments/p1 --data data/synthetic
python -m hf.report --exp experiments/p1 --out experiments/tables --data data/synthetic
python -m hf.selection --exp experiments/p1 --out experiments/tables
python -m hf.significance --exp experiments/p1 --out experiments/tables
python -m hf.gbm run --data data/synthetic --split test --targets revenue --out experiments/lgbm --ref-exp experiments/p1
```

## Pipeline of the study

| Step | Command |
| --- | --- |
| Data | `python -m hf.data --raw <export>.xlsx` |
| Statistical baselines and reconciliation | `bash jobs/run_p1_local.sh` |
| Rescoring, tables | `python -m hf.rescore`, `python -m hf.report` |
| Model selection, tests | `python -m hf.selection`, `python -m hf.significance` |
| LightGBM | `python -m hf.gbm tune`, `python -m hf.gbm run`, `python -m hf.fm score` |
| Foundation models (GPU) | `python -m hf.fm prepare`, job `jobs/p2_fm_colab`, `python -m hf.fm score` |
| Components A and C (GPU job) | `jobs/p3_lahpf_colab`, `jobs/p3_probrec_v2_colab` |
| Twelve validation origins | `jobs/p4_valext_colab` |
| Event months, July 2026 | `python -m hf.eventeval` |
| Robustness | `python -m hf.robust make`, `jobs/p5_robust_colab`, `python -m hf.robust compare` |
| Deep and further foundation models (GPU) | `jobs/p6_models_colab` (`hf.nn`, `hf.fm2`), then `bash jobs/p6_models_colab/post_local.sh` |
| Component B (transfer) | `python -m hf.transfer run`, `python -m hf.transfer evaluate` |
| SHAP, error decomposition | `python -m hf.explain shap`, `python -m hf.explain errors` |
| Revision: selection on validation months before the test period, block-bootstrap intervals, SHAP of the quantile models, life-cycle ablation | `jobs/r1_revision_colab` (`hf.window`, `hf.explain shapq`), then `python jobs/r1_revision_colab/post_local.py`, `python -m hf.explain shapq-tables` and `shapq-fig` |
| Check of the non-negative MinT against the library | `python -m hf.mintcheck` |

The GPU jobs are defined by `jobs/<name>/job.json` (inputs, environment, outputs) and `job.py` (the script run on
the VM). The settings of component C chosen on the validation origins (`jobs/p4_valext_colab/chosen_*.csv`) are
written by the component C job and are not included.

## Design in brief

- Rolling origins with an expanding window from January 2019: twelve monthly validation origins (August 2022 to
  July 2023) and nine quarterly test origins (August 2023 to August 2025), 12 months ahead.
- Accuracy: MASE, RMSSE and a scaled CRPS, interval coverage and width, M5-style weighted measures; one coherent
  configuration per measure is chosen by the mean over levels of the relative weighted RMSSE and scaled CRPS
  (`hf.selection`) on the validation forecasts for target months up to August 2023, the last month before the
  test period (`hf.window`).
- Confidence intervals: circular moving-block bootstrap over the 36 target months of the test period (`hf.window`).
- Panel Diebold–Mariano tests with Newey–West variance and MCB tests (`hf.significance`).
- Decisions taken after first results were known are listed in Section 5.6 of the paper.

## License and citation

Code: MIT License (`LICENSE`); event calendar: CC BY 4.0. Please cite the archive as given in `CITATION.cff` and the
article once published.
