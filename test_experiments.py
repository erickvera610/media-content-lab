import unittest,tempfile,json
from pathlib import Path
from experiment_store import save,list_runs
class ExperimentTests(unittest.TestCase):
    def test_repeated_model_is_one_record_and_survives_reopen(self):
        report=json.loads((Path(__file__).parent/'artifacts/news-results.json').read_text())
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/'experiments.db';save(path,report);save(path,report)
            rows=list_runs(path);self.assertEqual(len(rows),1);self.assertEqual(rows[0]['model_sha'],report['model_sha256'])
