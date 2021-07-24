import sys,os

sys.path.insert(0, "../src/pyfrechet/")

from distance import StrongDistance
from visualize import FreeSpaceDiagram

sd = StrongDistance.setcurves("test_curve_1.txt", "test_curve_2.txt", True)
fsd = FreeSpaceDiagram(sd)
fsd.plot(10, 300, 10)
