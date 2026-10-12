# Recruiter Quick View

## What this project proves

This repository demonstrates regression on 39,644 real historical articles with chronological splitting, leakage-aware feature design, baseline comparison, model selection, reproducible artifacts, and a browser/Python inference path.

## Best evidence to inspect first

1. `artifacts/news-results.json` — real-data training/test report.
2. `temporal_robustness.py` — early/middle/late test-slice evaluation and feature-sensitivity checks.
3. `news_train.py` — chronological grouped split, model comparison, and export logic.
4. `news-demo.html` — public inference demo using trained parameters.
5. `data/SOURCE.json` — dataset attribution and checksum.
6. GitHub Actions — automated testing.

## Skills shown

Python, scikit-learn, Ridge regression, gradient boosting, chronological validation, leakage prevention, temporal evaluation, feature sensitivity, MAE/RMSE, model export, APIs, SQLite experiment tracking, tests, and CI.

## Important interpretation

The measured improvement over the median baseline is modest. That is useful evidence: the project reports the real result rather than exaggerating it. Historical Mashable data does not establish current publisher performance or causal audience impact.

## Recommended interview demo

Run:

```bash
python news_train.py
python temporal_robustness.py
python app.py
```

Explain why publication-day groups stay together, why share-history variables are excluded, and whether error changes from the early to late test slices.

## Screenshot/result checklist

Capture:

- the real-news browser demo,
- the train/validation/test counts,
- selected model and baseline comparison,
- temporal-slice MAE table,
- one or two prediction examples with the limitations visible.

Every visual should point back to a reproducible JSON artifact or script.
