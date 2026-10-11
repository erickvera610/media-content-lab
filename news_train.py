"""Public news-share regression with day-grouped chronological holdout."""
import csv,json,hashlib,sqlite3,os,urllib.request,zipfile,io
from pathlib import Path
from datetime import datetime,timezone
os.environ.setdefault('OMP_NUM_THREADS','1')
import numpy as np
import sklearn
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.dummy import DummyRegressor
from sklearn.metrics import mean_absolute_error,mean_squared_error
ROOT=Path(__file__).parent
FEATURES=['n_tokens_title','n_tokens_content','num_hrefs','num_self_hrefs','num_imgs','num_videos','average_token_length','num_keywords',
          'data_channel_is_lifestyle','data_channel_is_entertainment','data_channel_is_bus','data_channel_is_socmed','data_channel_is_tech','data_channel_is_world','is_weekend']
SOURCE=json.loads((ROOT/'data/SOURCE.json').read_text())

def prepare(path):
    if not path.exists():
        with urllib.request.urlopen(SOURCE['download'],timeout=60) as r:archive=zipfile.ZipFile(io.BytesIO(r.read()))
        path.parent.mkdir(exist_ok=True);path.write_bytes(archive.read(next(n for n in archive.namelist() if n.endswith('.csv'))))
    digest=hashlib.sha256(path.read_bytes()).hexdigest()
    if digest!=SOURCE['csv_sha256']:raise ValueError('Dataset checksum mismatch')
    with path.open(newline='') as stream:rows=[{k.strip():v.strip() for k,v in r.items()} for r in csv.DictReader(stream)]
    x=np.array([[float(r[k]) for k in FEATURES] for r in rows]);y=np.log1p([float(r['shares']) for r in rows]);days=np.array([float(r['timedelta']) for r in rows])
    if not np.isfinite(x).all() or not np.isfinite(y).all():raise ValueError('Nonfinite dataset entries')
    order=np.argsort(-days,kind='stable');return x[order],y[order],days[order],np.array([r['url'] for r in rows])[order],order

def split_days(days):
    unique=np.array(sorted(set(days),reverse=True));a,b=int(len(unique)*.6),int(len(unique)*.8)
    return np.where(days>=unique[a-1])[0],np.where((days<unique[a-1])&(days>=unique[b-1]))[0],np.where(days<unique[b-1])[0]

def export(model,name):
    if name=='ridge':
        scale,reg=model.steps[0][1],model.steps[1][1]
        return {'kind':'ridge','mean':scale.mean_.tolist(),'scale':scale.scale_.tolist(),'coef':reg.coef_.tolist(),'intercept':float(reg.intercept_)}
    trees=[]
    for stage in model._predictors:
        nodes=stage[0].nodes
        trees.append([{k:float(n[k]) if k in ['value','num_threshold'] else int(n[k]) for k in ['value','feature_idx','num_threshold','missing_go_to_left','left','right','is_leaf']} for n in nodes])
    return {'kind':'hist_gradient_boosting','baseline':float(model._baseline_prediction[0,0]),'trees':trees}

def infer(artifact,features):
    if set(features)!=set(FEATURES):raise ValueError('All documented feature names required; extra features are rejected')
    x=np.array([features[k] for k in FEATURES],dtype=float)
    if not np.isfinite(x).all() or (x<0).any():raise ValueError('Finite nonnegative features required')
    for i,k in enumerate(FEATURES):
        if k.startswith('data_channel_') or k=='is_weekend':
            if x[i] not in [0,1]:raise ValueError('Channel/weekend values must be 0 or 1')
    m=artifact['model']
    if m['kind']=='ridge':log=float(((x-np.array(m['mean']))/np.array(m['scale']))@np.array(m['coef'])+m['intercept'])
    else:
        log=m['baseline']
        for tree in m['trees']:
            i=0
            while not tree[i]['is_leaf']:
                n=tree[i];i=n['left'] if x[n['feature_idx']]<=n['num_threshold'] else n['right']
            log+=tree[i]['value']
    return {'predicted_log1p_shares':log,'typical_shares_estimate':float(np.expm1(np.clip(log,0,20)))}

def train():
    x,y,days,urls,ids=prepare(ROOT/'data/OnlineNewsPopularity.csv');tr,va,te=split_days(days)
    candidates={'ridge':make_pipeline(StandardScaler(),Ridge(alpha=10)),
                'hist_gradient_boosting':HistGradientBoostingRegressor(max_iter=80,max_leaf_nodes=15,max_depth=5,early_stopping=False,random_state=42)}
    validation={}
    for name,m in candidates.items():m.fit(x[tr],y[tr]);validation[name]=float(mean_absolute_error(y[va],m.predict(x[va])))
    name=min(validation,key=validation.get);model=candidates[name];fit=np.concatenate([tr,va]);model.fit(x[fit],y[fit])
    pred=model.predict(x[te]);baseline=DummyRegressor(strategy='median').fit(x[fit],y[fit]);base=baseline.predict(x[te])
    report={'executed_at_utc':datetime.now(timezone.utc).isoformat(),'dataset':'UCI Online News Popularity (Mashable, historical 2013–2014)',
        'source':SOURCE,'sklearn_version':sklearn.__version__,'rows':len(x),'feature_order':FEATURES,
        'excluded':'shares is target; url is metadata; timedelta orders dates only; keyword/share-history statistics and self_reference_* are excluded to reduce leakage risk.',
        'target':'log1p(shares)','split':{k:len(v) for k,v in [('train',tr),('validation',va),('test',te)]},
        'split_days':{k:{'oldest_age_days':float(days[v].max()),'newest_age_days':float(days[v].min())} for k,v in [('train',tr),('validation',va),('test',te)]},
        'split_indices_sha256':{k:hashlib.sha256(ids[v].tobytes()).hexdigest() for k,v in [('train',tr),('validation',va),('test',te)]},
        'protocol':'Oldest 60% of unique publication-day groups train, next 20% validation, latest 20% test; no day crosses boundaries. Selection uses validation log-MAE, then refit train+validation.',
        'validation_log_mae':validation,'selected_model':name,
        'test':{'log_mae':float(mean_absolute_error(y[te],pred)),'baseline_log_mae':float(mean_absolute_error(y[te],base)),
                'log_rmse':float(np.sqrt(mean_squared_error(y[te],pred))),
                'shares_mae':float(mean_absolute_error(np.expm1(y[te]),np.expm1(np.clip(pred,0,20)))),
                'baseline_shares_mae':float(mean_absolute_error(np.expm1(y[te]),np.expm1(base)))},
        'examples':[{'source_row_id':int(ids[idx]),'features':dict(zip(FEATURES,x[idx].tolist())),
                     'actual_shares':int(round(np.expm1(y[idx]))),'predicted_log1p_shares':float(pred[i]),
                     'typical_shares_estimate':float(np.expm1(np.clip(pred[i],0,20)))} for i,idx in enumerate(te[:12])],
        'limitations':'Historical one-publisher sample; target exposure windows vary. Publication-time availability of all source features is not externally audited. Temporal split does not guarantee absence of all leakage. Not causal, not current FOX performance, not an expected arithmetic mean of shares.'}
    artifact={'feature_order':FEATURES,'model':export(model,name),'target':'log1p(shares)','dataset_sha256':SOURCE['csv_sha256']}
    return report,artifact,model,x,te

if __name__=='__main__':
    report,artifact,_,_,_=train();folder=ROOT/'artifacts';folder.mkdir(exist_ok=True)
    text=json.dumps(artifact,separators=(',',':'),allow_nan=False);report['model_sha256']=hashlib.sha256(text.encode()).hexdigest()
    (folder/'news-model.json').write_text(text);(folder/'news-results.json').write_text(json.dumps(report,indent=2,allow_nan=False))
    from experiment_store import save,list_runs
    save(folder/'experiments.sqlite3',report)
    (folder/'experiment-records.json').write_text(json.dumps(list_runs(folder/'experiments.sqlite3'),indent=2))
    print(json.dumps({'rows':report['rows'],'split':report['split'],'selected_model':report['selected_model'],'test':report['test']}))
