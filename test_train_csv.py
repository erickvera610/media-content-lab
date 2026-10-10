import csv, tempfile, unittest
from pathlib import Path
from datetime import datetime, timedelta
from model import dataset
from train_csv import fit_csv
class CSVTests(unittest.TestCase):
    def test_chronological_training(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"posts.csv"
            with path.open("w",newline="") as stream:
                writer=csv.DictWriter(stream,fieldnames=["timestamp","duration_seconds","hour","video","engagement_rate"])
                writer.writeheader()
                for i,r in enumerate(dataset()):
                    writer.writerow({"timestamp":(datetime(2025,1,1)+timedelta(days=i)).isoformat(), **{k:r[k] for k in writer.fieldnames if k!="timestamp"}})
            report=fit_csv(path)
            self.assertEqual(report["split"],{"train":180,"validation":60,"test":60})
            self.assertLess(report["test_mae"],report["baseline_mae"])
            self.assertLess(report["boundaries"]["last_validation"], report["boundaries"]["first_test"])
