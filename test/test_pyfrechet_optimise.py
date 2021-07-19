import sys,os

sys.path.insert(0, "../src/pyfrechet/")

from distance import StrongDistance
from optimise import BinarySearch

sd = StrongDistance.setcurves("test_curve_21.txt", "test_curve_22.txt", False)

bs = BinarySearch(sd)
#bs.setBoundaries(1, 1000)
bs.setPercision(0.00001)
bs.search()
