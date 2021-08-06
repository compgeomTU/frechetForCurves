# Author: Will Rodman
# wrodman@tulane.edu
#
# Command line to run program:
# python3 pyfrechet_optimise.py

import sys, os, unittest

sys.path.insert(0, "../src/pyfrechet/")

from distance import StrongDistance
from optimise import BinarySearch

TEST_DATA = "sp500"

if TEST_DATA == "sp500":
    REVERSE_CURVE = False
    CURVE_2_INDEX_0 = (1, 376.230011)

elif TEST_DATA == "trajectory":
    REVERSE_CURVE = True
    CURVE_2_INDEX_0 = (483282.000000, 4213251.000000)

CURVE_1 = f"{TEST_DATA}_data/sample_1.txt"
CURVE_2 = f"{TEST_DATA}_data/sample_2.txt"

class pyfrechet_optimise(unittest.TestCase):

    def setUp(self):
        self.counter = 0

    def test_fail_BinarySearch_instance_argument(self):
        class BadClass(): pass
        with self.assertRaises(TypeError):
            bc = BadClass()
            BinarySearch(bc)

    def test_BinarySearch_default_search(self):
        sd = StrongDistance.setCurves(CURVE_1, CURVE_2, REVERSE_CURVE)
        bs = BinarySearch(sd)
        bs = bs.search()

    def test_BinarySearch_custom_search(self):
        sd = StrongDistance.setCurves(CURVE_1, CURVE_2, REVERSE_CURVE)
        bs = BinarySearch(sd)
        bs.setBoundaries(1, 70)
        bs.setPercision(0.0001)
        eps = bs.search()

    def test_fail_BinarySearch_epsilon_search(self):
        sd = StrongDistance.setCurves(CURVE_1, CURVE_2, REVERSE_CURVE)
        bs = BinarySearch(sd)
        bs.setBoundaries(0.1, 1)
        with self.assertRaises(RecursionError):
            bs.search()


if __name__ == '__main__':
    unittest.main()
