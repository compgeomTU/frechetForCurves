import sys,os

sys.path.insert(0, "../src/pyfrechet/")

from distance import StrongDistance
from optimise import BinarySearch

sd = StrongDistance.setcurves("test_curve_1.txt", "test_curve_2.txt", True)

bs = BinarySearch(sd)
bs.setBoundaries(10, 100)
bs.setPercision(0.00001)
bs.search()
