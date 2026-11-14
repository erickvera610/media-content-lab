# Temporal evaluation repair — November 13, 2026

## Problem and implementation

The train/validation/test split already kept publication days together. However, the temporal diagnostic then used `np.array_split(test_rows, 3)`, which could split one publication day across adjacent test slices. On the real dataset, ages **102 and 58 days** each appeared in two adjacent slices. This was a diagnostic grouping defect, not evidence that the training split leaked test data.

`grouped_slices` now divides unique publication-day ages into three chronological groups and assigns every article from a day to exactly one slice. Larger age means older publication. It validates finite ages and unique, in-range integer row indices. At least three distinct days are required.

The report also adds a baseline fixed to the median log1p(shares) of train+validation, per-slice relative MAE reduction, all source row IDs, dataset/model/code hashes, software versions and explicit boundary-overlap checks. No model or hyperparameter is selected using these test slices. The same existing training procedure is rerun; the trained demo is not replaced.

## Measured evidence

| Test slice | Articles | Complete days | Age range (oldest→newest) | Ridge log-MAE | Fixed baseline log-MAE | Relative reduction |
|---|---:|---:|---|---:|---:|---:|
| Early | 2,979 | 49 | 152→104 | 0.667179 | 0.696478 | 4.21% |
| Middle | 3,317 | 48 | 103→56 | 0.624934 | 0.631237 | 1.00% |
| Late | 2,816 | 48 | 55→8 | 0.630076 | 0.645239 | 2.35% |

All 9,112 test articles are assigned once. No day crosses a new boundary. Relative reduction is `100 * (1 - model_MAE / baseline_MAE)`; all errors above are on **log1p(shares)**, not raw share counts. The baseline prediction is 7.313886831633462. A single overall score hides this variation.

[Raw report with row IDs](artifacts/temporal-robustness.json)

## Reproduce and validate

```bash
python -m pip install -r requirements.txt
python temporal_robustness.py
python -m unittest discover -v
node test_news.cjs
node test_demo.cjs
node test_enhanced.cjs
```

The first run downloads the public UCI data if absent and verifies its recorded SHA-256. Existing CI runs the temporal script and uploads JSON evidence.

All **18 Python tests passed locally**, including three new tests for uneven group sizes and complete coverage, shuffled row indices, and invalid input. The browser/Python news prediction parity check and both other JavaScript suites passed. Remote CI success is not asserted here.

## Interpretation and limitations

This repairs evaluation integrity rather than improving predictive accuracy. Differences across periods may reflect sampling variation and distribution changes; they do not establish drift or statistical significance. Data are historical, from one publisher, with varying exposure windows. Publication-time availability of all features is not independently verified. The existing ±10% count-feature perturbations remain descriptive synthetic sensitivity checks, not causal experiments. Independent AI-assisted portfolio work; public dataset attribution remains in data/SOURCE.json.
