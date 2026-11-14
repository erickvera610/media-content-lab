import unittest
import numpy as np
from temporal_robustness import grouped_slices

class TemporalTests(unittest.TestCase):
    def test_days_stay_together_and_cover_all_rows(self):
        days=np.array([9,9,9,9,8,7,6,6,5,4])
        chunks=grouped_slices(days,np.arange(len(days)))
        self.assertEqual([days[c].tolist() for c in chunks],[[9,9,9,9,8],[7,6,6],[5,4]])
        self.assertEqual(sorted(np.concatenate(chunks).tolist()),list(range(len(days))))
        for a,b in zip(chunks,chunks[1:]):
            self.assertGreater(days[a].min(),days[b].max())

    def test_input_order_does_not_change_chronology(self):
        days=np.array([1,3,2,3,1,2])
        chunks=grouped_slices(days,np.array([5,4,3,2,1,0]))
        self.assertEqual([set(days[c]) for c in chunks],[{3},{2},{1}])

    def test_rejects_insufficient_or_invalid_groups(self):
        for days, ids in [(np.array([1,1]),[0,1]),(np.array([3,2,1]),[0,0,1]),
                          (np.array([3,np.nan,1]),[0,1,2]),(np.array([3,2,1]),[0,1,9])]:
            with self.assertRaises(ValueError):grouped_slices(days,np.array(ids))
