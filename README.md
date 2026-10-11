# Media Prediction Lab

![Tests](https://github.com/erickvera610/media-content-lab/actions/workflows/tests.yml/badge.svg)

## New: trained model on 39,644 real historical articles

**[Inspect the real-news demo](https://erickvera610.github.io/media-content-lab/news-demo.html)** · [Reviewer evidence](RECRUITER_GUIDE.md) · [Training report](artifacts/news-results.json) · [CI tests](https://github.com/erickvera610/media-content-lab/actions/workflows/tests.yml)

The UCI Online News Popularity data contains historical Mashable article metadata. Compare ridge regression and histogram gradient boosting on the first chronological validation interval. Ridge was selected; increased model complexity was not rewarded just for being more elaborate.

Train/validation/test counts: **21,931 / 8,601 / 9,112**. Entire publication-day groups remain together. URL and observation age are excluded from prediction inputs; share-history fields are also excluded to reduce leakage risk. No test-based selection.

Test log-MAE: **0.6403**, compared with the training-median reference **0.6569** — **2.52% reduction**. Original-scale MAE remains high (2148.4 shares); the improvement is modest. Report both scales.

The public browser uses exported trained parameters. Local `/news` uses `/api/news/predict` with the same model. The training script also writes an idempotent SQLite experiment record keyed by model checksum; it does not store private article content.

```bash
python -m pip install -r requirements.txt
python news_train.py
python build_demo_data.py
python -m unittest discover -v
node test_news.cjs
python app.py
# Open http://127.0.0.1:8000/news
```

`news_train.py` downloads the public CSV if missing and checks its SHA-256. The large raw CSV is not committed. Dataset attribution, exact download and checksum: [data/SOURCE.json](data/SOURCE.json). CC BY 4.0 data license; cite Fernandes, Vinagre and Cortez (2015), UCI DOI 10.24432/C5NS3V. Repository MIT license covers project code.

The target is log1p(shares), not an engagement rate. Back-transformation estimates a typical share count, not the arithmetic expected mean. Share exposure windows vary; publication-time availability of all fields has not been externally audited. This is historical one-publisher evidence, not current FOX performance or causal impact.


The original ranking calculator is preserved in the Python API. The featured application now trains a regularized regression model to predict synthetic engagement before publication.

**[Open the live demo](https://erickvera610.github.io/media-content-lab/)** · [Spanish tutorial](TUTORIAL_ES.md) · [Case study](CASE_STUDY.md) · [Measured results](benchmark-results.json)

## Understand it in one minute

Pre-publication metadata → regularized regression → validation tuning → final test

Use duration, planned publication hour and video/article format. Do not use likes, shares, comments or observed views as prediction features: they are outcomes. Shuffle 300 independent synthetic observations into 180 training, 60 validation and 60 test records. Select ridge strength on validation, refit with training plus validation, and compare test MAE with a constant-mean baseline.

## Train on your own dated publications

The Python CSV trainer learns regression weights from pre-publication metadata. It sorts records chronologically, uses the first 60% for training, the next 20% for ridge selection, and the final 20% for evaluation. It saves coefficients, feature order, split dates, MAE, RMSE and the training-mean baseline in inspectable JSON.

```bash
python train_csv.py posts.csv --output trained-model.json
```

CSV columns: `timestamp,duration_seconds,hour,video,engagement_rate`. Use ISO timestamps with consistent timezone handling, duration 10–180 seconds, integer hour 0–23, video 0/1 and outcome rate 0–1. Supply at least 50 unique dated records. Measure every engagement label over the same observation window. Likes, shares and observed views never enter the feature vector.

The automated test uses explicitly synthetic records to verify chronological training. That CSV-trainer test is synthetic. The new UCI evaluation above provides separate historical real-data evidence. The original browser exercise remains synthetic; news-demo.html uses the real-data trained model. Hour is still linear; cross-author generalization and temporal drift need further evaluation.

## Measured evidence

Reproduced with Python by `python benchmark.py`. Execution timestamp is recorded in the JSON report. Synthetic JavaScript values may differ because the random generator differs.

| Measurement | Result |
|---|---|
| mean test mae | 0.0049 |
| mean baseline mae | 0.0130 |
| seeds beating baseline | 5 |

## Run locally

Python 3.11 or 3.12. Core synthetic exercises use the standard library; the real-data models require the declared Python dependencies. No API keys.

```bash
git clone https://github.com/erickvera610/media-content-lab.git
cd media-content-lab
python app.py
```

Open http://127.0.0.1:8000. Stop with Ctrl+C. The public browser demo requires no installation.

## Reproduce and inspect

```bash
python -m unittest discover -v
node test_enhanced.cjs
python benchmark.py
python daily_exercise.py
```

Use `core.run({"mode":"model","seed":42,"duration":60,"hour":18,"video":1})`. The output includes test error, baseline error, weights and ten held-out predictions.

## Read the source

- `core.py`: public algorithm entry point and preserved original exercise.
- `model.py`: featured implementation.
- `enhanced.js`: browser implementation, readable without a build system.
- `app.py`: localhost HTTP API.
- `test_*.py` and `test_enhanced.cjs`: behavior and edge cases.
- `benchmark.py`: evidence generator.

## Limitations

In the original synthetic exercise, outcome labels are generated from a known artificial relationship. The separate UCI experiment has the limitations documented above. Success demonstrates implementation and evaluation mechanics, not real audience prediction. Hour is treated linearly; cyclical encoding would be more realistic. If repeated posts from the same author were used, a grouped or chronological split would be required.

## Daily practical exercises

One dated fictional scenario runs daily through GitHub Actions. `exercises/YYYY-MM-DD/result.json` preserves inputs and outputs; `samples/latest.json` holds the latest input. Bot-authored report commits document script execution, not manual daily development. [Daily Spanish guide](EJERCICIOS_DIARIOS_ES.md).

## Authorship and relevance

Independent AI-assisted learning project in Erik Vera's portfolio. No affiliation with FOX, Tesla or BCG. The documentation distinguishes supplied implementation from improvements the learner actually makes. Code is MIT licensed; third-party data provenance is documented separately.

## Three featured portfolio projects

- [ML Model Lab](https://github.com/erickvera610/ml-model-lab): model selection and public-data evaluation.
- [Road Vision Lab](https://github.com/erickvera610/road-vision-lab): image processing and explicit failure analysis.
- [Media Content Lab](https://github.com/erickvera610/media-content-lab): regression and chronological evaluation.
