# Author: Will Rodman
# wrodman@tulane.edu
#
# Command line to run program:
# python3 pyfrechet_distance.py

import sys, os, unittest
sys.path.insert(0, "../src")
from distance import Distance, StrongDistance, WeakDistance


TEST_DATA = "sp500"

if TEST_DATA == "sp500":
    REVERSE_CURVE = False
    CURVE_2_INDEX_0 = (1, 376.230011)

elif TEST_DATA == "trajectory":
    REVERSE_CURVE = True
    CURVE_2_INDEX_0 = (483282.000000, 4213251.000000)

CURVE_1 = f"{TEST_DATA}_data/sample_1.txt"
CURVE_2 = f"{TEST_DATA}_data/sample_2.txt"

class pyfrechet_distance(unittest.TestCase):

    global REVERSE_CURVE
    global CURVE_2_INDEX_0

    global CURVE_1
    global CURVE_2

    def setUp(self):
        print(self._testMethodName)

    def test_fail_create_StrongDistance_object(self):
        with self.assertRaises(IOError):
            StrongDistance.setCurves("BAD_FILE.txt", "BAD_FILE.txt")

    def test_create_StrongDistance_object(self):
        sd = StrongDistance()
        print("__str__() of empty StrongDistance() object")
        print(sd)
        sd = StrongDistance.setCurves(CURVE_1, CURVE_2, REVERSE_CURVE)
        print("__str__() of StrongDistance() object after @classmethod")
        print(sd)

    def test_StrongDistance_instance(self):
        sd = StrongDistance.setCurves(CURVE_1, CURVE_2, REVERSE_CURVE)
        self.assertIsInstance(sd, Distance, \
                              "StrongDistance in not instance")

    def test_StrongDistance_getCurve(self):
        sd = StrongDistance.setCurves(CURVE_1, CURVE_2, REVERSE_CURVE)
        c2 = sd.getCurve2()
        self.assertEqual(c2[0].x, CURVE_2_INDEX_0[0], \
                         "Failed to return correct value")
        self.assertEqual(c2[0].y, CURVE_2_INDEX_0[1], \
                         "Failed to return correct value")

    def test_StrongDistance_getFreespace(self):
        sd = StrongDistance.setCurves(CURVE_1, CURVE_2, REVERSE_CURVE)
        sd.setFreeSpace(10)
        fs = sd.getFreeSpace()
        for i in range(sd.getCurve1Lenght()-1):
            for j in range(sd.getCurve2Lenght()-1):
                self.assertTrue(-1 <= fs.horizontal_start[i][j] <= 1, \
                                "Invalid free space value")
                self.assertTrue(-1 <= fs.horizontal_end[i][j] <= 1, \
                                "Invalid free space value")
                self.assertTrue(-1 <= fs.vertical_start[i][j] <= 1, \
                                "Invalid free space value")
                self.assertTrue(-1 <= fs.vertical_end[i][j] <= 1, \
                                "Invalid free space value")

if __name__ == '__main__':
    unittest.main()
