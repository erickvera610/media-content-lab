# Portfolio Evidence

This page summarizes the strongest verifiable evidence in this repository for recruiters and technical reviewers. It separates measured results from claims and documents the limits of the experiment.

## Real data

- Dataset: UCI Online News Popularity.
- Historical records: **39,644 real articles** from Mashable.
- Chronological split: **21,931 training / 8,601 validation / 9,112 test** observations.
- Publication-day groups remain together across the split.
- URL and observation-age fields are excluded from prediction inputs.
- Share-history fields are excluded to reduce leakage risk.
- The final test interval is not used for model selection.

## Modeling protocol

The real-data experiment compares:

- Ridge regression.
- Histogram gradient boosting.
- A training-median reference baseline.

Model choice is made on the chronological validation interval. Ridge is selected because the measured validation evidence does not justify the more complex model.

## Measured held-out results

- Test log-MAE: **0.6403**.
- Training-median reference log-MAE: **0.6569**.
- Relative reduction versus the reference: **2.52%**.
- Original-scale MAE: **2148.4 shares**.

The improvement is real but modest. The project reports both the transformed and original scales instead of hiding the larger absolute error.

## Evidence a recruiter can inspect

1. `news_train.py` — real-data training and chronological evaluation.
2. `artifacts/news-results.json` — exported metrics and experiment report.
3. `data/SOURCE.json` — dataset attribution, exact download information, and checksum.
4. `build_demo_data.py` — exported model parameters for the browser demo.
5. `news-demo.html` — public inference demo using the trained model artifact.
6. `/api/news/predict` — local Python inference path using the same model.
7. `test_news.cjs` and Python unit tests — behavior and cross-runtime validation.
8. GitHub Actions — automated reproducibility checks.
9. SQLite experiment logging keyed by model checksum — reproducible experiment tracking without storing private article content.

## Engineering and ML skills demonstrated

Python, scikit-learn, regression, chronological train/validation/test design, leakage prevention, baseline comparison, feature filtering, model selection, quantitative error reporting, model export, browser/Python inference parity, API design, unit testing, CI, data provenance, checksum verification, and lightweight experiment tracking.

## Why this project is stronger than a synthetic demo

The repository preserves earlier synthetic exercises for learning, but the portfolio evidence above comes from a separate real historical dataset with a fixed chronological evaluation protocol. This distinction is intentional: synthetic data demonstrates implementation mechanics, while the UCI experiment provides stronger evidence of handling real data, temporal splits, leakage concerns, baselines, and imperfect model performance.

## Important limitations

- The dataset represents one historical publisher and may not generalize to modern media platforms.
- The target is `log1p(shares)`, not engagement rate.
- Back-transformation does not produce an unbiased arithmetic mean estimate.
- Exposure windows for shares vary.
- Publication-time availability of every candidate feature has not been externally audited.
- The measured gain over the baseline is only **2.52%** on log-MAE.
- The model does not establish causal effects or business impact.
- This is not evidence of current FOX performance or employer data.

## Recruiter takeaway

The strongest signal from this project is not the size of the improvement. It is the end-to-end experimental discipline: real public data, chronological evaluation, explicit leakage controls, model comparison, an honest baseline, reproducible artifacts, an inspectable demo, automated tests, and documented limitations.

## Next evidence milestone

Add a fixed temporal-drift study with multiple historical cutoffs. Report how validation-selected performance changes across later periods, including baseline comparison and degradation by time. This would strengthen the project for data-science and applied-ML internships without overstating predictive power.
