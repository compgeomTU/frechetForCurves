# Author: Will Rodman
# wrodman@tulane.edu
#
# Command line to run program:
# python3 pyfrechet_optimise.py

import sys, os, unittest

sys.path.insert(0, "../pyfrechet")

from distance import StrongDistance
from optimise import BinarySearch

TEST_DATA = "sp500"

if TEST_DATA == "sp500":
    REACHABLE_EPSILON = 5
    UNREACHABLE_EPSILON = 1
    REVERSE_CURVE = False

elif TEST_DATA == "trajectory":
    REACHABLE_EPSILON = 70
    UNREACHABLE_EPSILON = 60
    REVERSE_CURVE = True

CURVE_1 = f"{TEST_DATA}_data/sample_1.txt"
CURVE_2 = f"{TEST_DATA}_data/sample_2.txt"

class pyfrechet_optimise(unittest.TestCase):

    global REACHABLE_EPSILON
    global UNREACHABLE_EPSILON
    global REVERSE_CURVE

    global CURVE_1
    global CURVE_2

    def test_fail_BinarySearch_instance_argument(self):
        class BadClass(): pass
        with self.assertRaises(TypeError):
            bc = BadClass()
            BinarySearch(bc)

    def test_BinarySearch_default_search(self):
        sd = StrongDistance.setCurves(CURVE_1, CURVE_2, REVERSE_CURVE)
        BinarySearch(sd).search()

    def test_BinarySearch_custom_search(self):
        sd = StrongDistance.setCurves(CURVE_1, CURVE_2, REVERSE_CURVE)
        bs = BinarySearch(sd)
        bs.setBoundaries(UNREACHABLE_EPSILON, REACHABLE_EPSILON)
        bs.setPercision(0.01)
        epsilon = bs.search()
        self.assertTrue(UNREACHABLE_EPSILON <= epsilon <= REACHABLE_EPSILON)

    def test_fail_BinarySearch_epsilon_search(self):
        sd = StrongDistance.setCurves(CURVE_1, CURVE_2, REVERSE_CURVE)
        bs = BinarySearch(sd)
        bs.setBoundaries(0, UNREACHABLE_EPSILON)
        with self.assertRaises(RecursionError):
            bs.search()


if __name__ == '__main__':
    unittest.main()
