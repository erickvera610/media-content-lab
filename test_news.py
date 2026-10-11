import unittest,json,hashlib
from pathlib import Path
import numpy as np
from news_train import split_days,train,infer,FEATURES
class NewsTests(unittest.TestCase):
    def test_day_groups_do_not_cross_boundaries(self):
        days=np.repeat(np.arange(20)[::-1],3);a,b,c=split_days(days)
        self.assertFalse(set(days[a])&set(days[b]) or set(days[a])&set(days[c]) or set(days[b])&set(days[c]))
        self.assertGreater(days[a].min(),days[b].max());self.assertGreater(days[b].min(),days[c].max())
    def test_exported_parameters_match_library(self):
        report,artifact,model,x,test=train()
        for idx in test[:10]:
            r=infer(artifact,dict(zip(FEATURES,x[idx])))
            self.assertAlmostEqual(r['predicted_log1p_shares'],model.predict(x[[idx]])[0],places=9)
        self.assertEqual(report['rows'],39644)
    def test_leaking_and_invalid_features_rejected(self):
        artifact=json.loads((Path(__file__).parent/'artifacts/news-model.json').read_text());features=dict.fromkeys(FEATURES,0)
        for bad in [{**features,'shares':100},{**features,'num_imgs':float('nan')},{**features,'is_weekend':2}]:
            with self.assertRaises(ValueError):infer(artifact,bad)
    def test_model_identity(self):
        folder=Path(__file__).parent/'artifacts';report=json.loads((folder/'news-results.json').read_text())
        self.assertEqual(hashlib.sha256((folder/'news-model.json').read_bytes()).hexdigest(),report['model_sha256'])
