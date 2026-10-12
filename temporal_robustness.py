"""Temporal-slice and feature-sensitivity checks for the real UCI news model.

No model selection is performed on the test period. The script trains with news_train.train()
and then reports error by chronological thirds of the untouched test set, plus modest
feature perturbations to expose sensitivity.
"""
from pathlib import Path
import json
import numpy as np
from sklearn.metrics import mean_absolute_error
from news_train import ROOT, prepare, split_days, train, FEATURES


def main():
    report, artifact, model, x, te = train()
    _, y, days, _, _ = prepare(ROOT/'data/OnlineNewsPopularity.csv')
    # te is already chronological because prepare() sorts oldest -> newest.
    chunks = np.array_split(te, 3)
    slices = {}
    for name, ids in zip(('early_test','middle_test','late_test'), chunks):
        pred=model.predict(x[ids])
        slices[name]={'n':int(len(ids)),'log_mae':float(mean_absolute_error(y[ids],pred)),
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

    out={'protocol':'Model selected without test data; test split is reported in chronological thirds. Feature sensitivity is descriptive, not a new accuracy benchmark.',
         'selected_model':report['selected_model'],'temporal_slices':slices,'feature_sensitivity':sensitivity,
         'limitations':'Historical single-publisher data; slice differences can reflect both drift and sampling variation.'}
    folder=ROOT/'artifacts'; folder.mkdir(exist_ok=True)
    (folder/'temporal-robustness.json').write_text(json.dumps(out,indent=2))
    print(json.dumps(out,indent=2))

if __name__=='__main__': main()
