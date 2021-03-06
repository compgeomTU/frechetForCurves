# Author: Will Rodman
# wrodman@tulane.edu
#
# Command line to run program:
# python3 pyfrechet_visualize.py

import sys, os, unittest
sys.path.insert(0, "../")
from pyfrechet.distance import StrongDistance
from pyfrechet.visualize import FreeSpaceDiagram, Trajectories

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
            FreeSpaceDiagram(bc)

    def test_FreeSpaceDiagram_plot(self):
        sd = StrongDistance.setCurves(CURVE_1, CURVE_2, REVERSE_CURVE)
        sd.setFreeSpace(REACHABLE_EPSILON)
        fsd = FreeSpaceDiagram(sd)
        fsd.plot()

    def test_FreeSpaceDiagram__addEpsilonSlider(self):
        sd = StrongDistance.setCurves(CURVE_1, CURVE_2, REVERSE_CURVE)
        fsd = FreeSpaceDiagram(sd)
        fsd.addEpsilonSlider(UNREACHABLE_EPSILON, REACHABLE_EPSILON, 1)
        fsd.plot()

    def test_FreeSpaceDiagram__weighted_cells(self):
        sd = StrongDistance.setCurves(CURVE_1, CURVE_2, REVERSE_CURVE)
        fsd = FreeSpaceDiagram(sd)
        sd.setFreeSpace(REACHABLE_EPSILON)
        fsd.plot(True, False)

    def test_FreeSpaceDiagram__gridlines(self):
        sd = StrongDistance.setCurves(CURVE_1, CURVE_2, REVERSE_CURVE)
        fsd = FreeSpaceDiagram(sd)
        sd.setFreeSpace(REACHABLE_EPSILON)
        fsd.plot(True, True)

    def test_Trajectories(self):
        sd = StrongDistance.setCurves(CURVE_1, CURVE_2, REVERSE_CURVE)
        t = Trajectories(sd)
        t.plot()

    

if __name__ == '__main__':
    unittest.main()
