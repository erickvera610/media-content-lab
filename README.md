# Media Prediction Lab

![Tests](https://github.com/erickvera610/media-content-lab/actions/workflows/tests.yml/badge.svg)

> **Recruiter quick view:** real historical data, chronological evaluation, leakage-aware features, regression model comparison, temporal robustness checks, browser inference, experiment tracking, tests, and CI. Start with [RECRUITER_OVERVIEW.md](RECRUITER_OVERVIEW.md), [PORTFOLIO_EVIDENCE.md](PORTFOLIO_EVIDENCE.md), the [real-news demo](https://erickvera610.github.io/media-content-lab/news-demo.html), and `artifacts/news-results.json`.

## Real-data experiment

This project trains and evaluates models on **39,644 historical articles** from the UCI Online News Popularity dataset. Publication-day groups stay together so train, validation, and test remain chronological.

- Train: **21,931**
- Validation: **8,601**
- Test: **9,112**
- Models compared: Ridge regression and histogram gradient boosting
- Selected model: Ridge
- Test log-MAE: **0.6403**
- Training-median baseline log-MAE: **0.6569**
- Relative reduction: **2.52%**
- Original-scale MAE: **2148.4 shares**

The improvement is modest and is reported as such. This is historical single-publisher evidence, not a claim of current publisher performance or causal audience impact.

## Robustness and temporal evaluation

`temporal_robustness.py` evaluates the untouched test period in early, middle, and late chronological slices and measures prediction sensitivity when count-like pre-publication features are perturbed by ±10%.

```bash
python news_train.py
python temporal_robustness.py
```

The goal is to expose drift and sensitivity, not to tune against the test period.

## Leakage controls

Prediction inputs exclude:

- article URL,
- observation age from the prediction vector,
- the target `shares`,
- share-history fields,
- `self_reference_*` fields.

The project uses publication-day grouping and a chronological split. These controls reduce leakage risk but do not prove that every field was available at publication time.

## Demo and reproducibility

**[Open real-news demo](https://erickvera610.github.io/media-content-lab/news-demo.html)** · [Training report](artifacts/news-results.json) · [Source metadata](data/SOURCE.json) · [CI](https://github.com/erickvera610/media-content-lab/actions/workflows/tests.yml)

```bash
python -m pip install -r requirements.txt
python news_train.py
python build_demo_data.py
python -m unittest discover -v
node test_news.cjs
python app.py
```

Local real-data inference is available at `/news`; the public browser demo uses exported trained parameters. The training script records experiments in SQLite using the model checksum as an idempotent key.

## Skills demonstrated

Python, scikit-learn, regression, Ridge, gradient boosting, chronological validation, leakage prevention, MAE/RMSE, temporal robustness, feature sensitivity, model export, browser/Python inference, SQLite experiment tracking, tests, and CI.

## Key files

- `news_train.py` — real-data training and chronological evaluation.
- `temporal_robustness.py` — temporal-slice and feature-sensitivity checks.
- `artifacts/news-results.json` — measured held-out results.
- `RECRUITER_OVERVIEW.md` — recruiter review path and screenshot checklist.
- `PORTFOLIO_EVIDENCE.md` — evidence-focused summary.
- `app.py` — local API/demo backend.

## Limitations

The dataset is historical Mashable metadata. Share exposure windows vary. Publication-time availability of all source fields has not been independently audited. Back-transforming `log1p(shares)` estimates a typical share count, not an arithmetic expected value. The project demonstrates disciplined model evaluation, not causal inference or production forecasting.

## Authorship

Independent AI-assisted learning project in Erik Vera's portfolio. No employer affiliation or proprietary employer data. Code is MIT licensed; third-party data rights and attribution are documented separately.
