import sys,os

sys.path.insert(0, "../src/pyfrechet/")

from distance import StrongDistance
from visualize import FreeSpaceDiagram

sd = StrongDistance.setcurves("test_curve_21.txt", "test_curve_22.txt", False)
sd.setfreespace(1.5)
fsd = FreeSpaceDiagram(sd)
fsd.plot()
