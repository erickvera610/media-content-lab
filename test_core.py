import unittest
from core import rank,run
class Tests(unittest.TestCase):
    def test_rate_ranking(self):
        rows=[dict(title='a',views=100,likes=10,shares=0,comments=0),dict(title='b',views=1000,likes=20,shares=0,comments=0)]
        self.assertEqual(rank(rows)[0]['title'],'a')
    def test_filter(self):self.assertEqual(rank([dict(views=0,likes=0,shares=0,comments=0)]),[])
    def test_invalid(self):
        with self.assertRaises(ValueError):rank([dict(views=100,likes=-1,shares=0,comments=0)])
    def test_reproducible(self):self.assertEqual(run({}),run({}))
