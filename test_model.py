import unittest
from model import run_model, dataset

class ModelTests(unittest.TestCase):

    def test_beats_mean_on_synthetic_holdout(self):
        r = run_model({})
        self.assertLess(r['test_mae'], r['baseline_mae'])
        self.assertEqual(r['test_samples'], 60)

    def test_partition_ids_disjoint(self):
        rows = dataset()
        a, b, c = [set((r['id'] for r in part)) for part in [rows[:180], rows[180:240], rows[240:]]]
        self.assertFalse(a & b or b & c or a & c)

    def test_reproducible(self):
        self.assertEqual(run_model({}), run_model({}))
