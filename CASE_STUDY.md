# Case study: Media Prediction Lab

## 1. Problem and intended user

The original ranking calculator is preserved in the Python API. The featured application now trains a regularized regression model to predict synthetic engagement before publication.

## 2. Data and information flow

Pre-publication metadata → regularized regression → validation tuning → final test

## 3. Why these choices

Use duration, planned publication hour and video/article format. Do not use likes, shares, comments or observed views as prediction features: they are outcomes. Shuffle 300 independent synthetic observations into 180 training, 60 validation and 60 test records. Select ridge strength on validation, refit with training plus validation, and compare test MAE with a constant-mean baseline.

## 4. Reproducible evidence

| Measurement | Result |
|---|---|
| mean test mae | 0.0049 |
| mean baseline mae | 0.0130 |
| seeds beating baseline | 5 |

Generated at 2026-10-10T18:37:12.360036+00:00 by the Python benchmark. Read every run in [benchmark-results.json](benchmark-results.json). These results apply only to the documented benchmark. No production performance claim is made.

## 5. What could go wrong

All outcome labels are generated from a known artificial relationship. Success demonstrates implementation and evaluation mechanics, not real audience prediction. Hour is treated linearly; cyclical encoding would be more realistic. If repeated posts from the same author were used, a grouped or chronological split would be required.

## 6. Next substantive improvement

Añade codificación cíclica para la hora y compara con el modelo actual. Después usa un dataset público permitido, documenta privacidad y evita que el mismo creador aparezca en entrenamiento y prueba.

Open an issue, create a branch, implement the improvement, run the checks, and explain the change in a pull request. Do not describe automated report commits as personal code development.
