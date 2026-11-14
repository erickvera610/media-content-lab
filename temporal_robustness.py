"""Temporal-slice and feature-sensitivity checks for the real UCI news model.

No model selection is performed on the test period. The script trains with news_train.train()
and then reports error by chronological thirds of the test publication-day groups, plus modest
feature perturbations to expose sensitivity.
"""
from pathlib import Path
import json, hashlib, platform
import numpy as np
import sklearn
from sklearn.metrics import mean_absolute_error
from news_train import ROOT, prepare, split_days, train, FEATURES


def grouped_slices(days, ids):
    """Split unique publication ages, oldest first; never split a day."""
    days, ids = np.asarray(days), np.asarray(ids)
    if (days.ndim != 1 or ids.ndim != 1 or not np.issubdtype(ids.dtype, np.integer)
            or len(set(ids.tolist())) != len(ids) or np.any(ids < 0)
            or np.any(ids >= len(days)) or not np.isfinite(days).all()):
        raise ValueError('Finite days and unique valid integer row indices required')
    unique = np.sort(np.unique(days[ids]))[::-1]
    if len(unique) < 3:
        raise ValueError('At least three publication-day groups required')
    return [ids[np.isin(days[ids], group)] for group in np.array_split(unique, 3)]


def main():
    report, artifact, model, x, te = train()
    _, y, days, _, source_ids = prepare(ROOT/'data/OnlineNewsPopularity.csv')
    # te is already chronological because prepare() sorts oldest -> newest.
    chunks = grouped_slices(days, te)
    tr, va, _ = split_days(days)
    baseline = float(np.median(y[np.concatenate([tr, va])]))
    old_chunks = np.array_split(te, 3)
    old_overlap = [sorted(set(days[a]) & set(days[b])) for a,b in zip(old_chunks, old_chunks[1:])]
    slices = {}
    for name, ids in zip(('early_test','middle_test','late_test'), chunks):
        pred=model.predict(x[ids])
        slices[name]={'n':int(len(ids)),'log_mae':float(mean_absolute_error(y[ids],pred)),
                      'baseline_log_mae':float(np.mean(np.abs(y[ids]-baseline))),
                      'relative_mae_reduction_pct':float(100*(1-mean_absolute_error(y[ids],pred)/np.mean(np.abs(y[ids]-baseline)))),
                      'publication_day_groups':int(len(np.unique(days[ids]))),
                      'source_row_ids':source_ids[ids].tolist(),
                      'oldest_age_days':float(days[ids].max()),'newest_age_days':float(days[ids].min())}

    # Sensitivity: change only count-like pre-publication features by +/-10%.
    sensitivity={}
    count_features=['n_tokens_title','n_tokens_content','num_hrefs','num_self_hrefs','num_imgs','num_videos','num_keywords']
    idx=[FEATURES.index(k) for k in count_features]
    base=model.predict(x[te])
    for scale in (.9,1.1):
        xp=x[te].copy(); xp[:,idx]*=scale
        pred=model.predict(xp)
        sensitivity[f'count_features_x{scale}']={
            'mean_abs_prediction_shift_log1p':float(np.mean(np.abs(pred-base))),
            'p95_abs_prediction_shift_log1p':float(np.percentile(np.abs(pred-base),95))}

    out={'protocol':'Model selected without test data; test split is divided into thirds of unique publication-day groups, never splitting a day. Baseline is train+validation median, fixed for all periods. Feature sensitivity is descriptive, not a new accuracy benchmark.',
         'code_sha256':{name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in ('temporal_robustness.py','news_train.py')},
         'dataset_sha256':artifact['dataset_sha256'],
         'model_sha256':hashlib.sha256(json.dumps(artifact,sort_keys=True).encode()).hexdigest(),
         'versions':{'python':platform.python_version(),'numpy':np.__version__,'sklearn':sklearn.__version__},
         'previous_row_split_shared_days':old_overlap,
         'day_overlap_between_new_slices':[sorted(set(days[a]) & set(days[b])) for a,b in zip(chunks,chunks[1:])],
         'baseline_log1p_prediction':baseline,
         'selected_model':report['selected_model'],'temporal_slices':slices,'feature_sensitivity':sensitivity,
         'limitations':'Historical single-publisher data; slice differences can reflect both drift and sampling variation.'}
    folder=ROOT/'artifacts'; folder.mkdir(exist_ok=True)
    (folder/'temporal-robustness.json').write_text(json.dumps(out,indent=2))
    print(json.dumps(out,indent=2))

if __name__=='__main__': main()
