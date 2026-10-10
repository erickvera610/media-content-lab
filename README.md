# Media Prediction Lab

The original ranking calculator is preserved in the Python API. The featured application now trains a regularized regression model to predict synthetic engagement before publication.

**[Open the live demo](https://erickvera610.github.io/media-content-lab/)** · [Spanish tutorial](TUTORIAL_ES.md) · [Case study](CASE_STUDY.md) · [Measured results](benchmark-results.json)

## Understand it in one minute

Pre-publication metadata → regularized regression → validation tuning → final test

Use duration, planned publication hour and video/article format. Do not use likes, shares, comments or observed views as prediction features: they are outcomes. Shuffle 300 independent synthetic observations into 180 training, 60 validation and 60 test records. Select ridge strength on validation, refit with training plus validation, and compare test MAE with a constant-mean baseline.

## Measured evidence

Reproduced with Python by `python benchmark.py`. Execution timestamp is recorded in the JSON report. Synthetic JavaScript values may differ because the random generator differs.

| Measurement | Result |
|---|---|
| mean test mae | 0.0049 |
| mean baseline mae | 0.0130 |
| seeds beating baseline | 5 |

## Run locally

Python 3.11 or 3.12, standard library only. No API keys.

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

All outcome labels are generated from a known artificial relationship. Success demonstrates implementation and evaluation mechanics, not real audience prediction. Hour is treated linearly; cyclical encoding would be more realistic. If repeated posts from the same author were used, a grouped or chronological split would be required.

## Daily practical exercises

One dated fictional scenario runs daily through GitHub Actions. `exercises/YYYY-MM-DD/result.json` preserves inputs and outputs; `samples/latest.json` holds the latest input. Bot-authored report commits document script execution, not manual daily development. [Daily Spanish guide](EJERCICIOS_DIARIOS_ES.md).

## Authorship and relevance

Independent AI-assisted learning project in Erik Vera's portfolio. No affiliation with FOX, Tesla or BCG. The documentation distinguishes supplied implementation from improvements the learner actually makes. Code is MIT licensed; third-party data provenance is documented separately.

## Featured portfolio

- [Road Vision Lab](https://github.com/erickvera610/road-vision-lab)
- [Demand Forecasting Lab](https://github.com/erickvera610/consulting-demand-lab)
- [Media Prediction Lab](https://github.com/erickvera610/media-content-lab)
- [Classification Evaluation Lab](https://github.com/erickvera610/ml-model-lab)
- [Incident Workflow Lab](https://github.com/erickvera610/incident-response-lab)
