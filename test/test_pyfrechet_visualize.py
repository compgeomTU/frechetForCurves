import sys,os

sys.path.insert(0, "../src/pyfrechet/")

from distance import StrongDistance
from visualize import FreeSpaceDiagram

sd = StrongDistance.setcurves("test_curve_1.txt", "test_curve_2.txt", True)
sd.setfreespace(70)
fsd = FreeSpaceDiagram(sd)
fsd.build_multipolygon(True)
fsd.plot()
