import sys,os

sys.path.insert(0, "../src/pyfrechet/")

from distance import StrongDistance
from visualize import FreespaceDiagram

sd = StrongDistance.setCurves("test_IVV.txt", "test_SPY.txt", False)
fsd = FreespaceDiagram(sd)
fsd.plot(0, 10, 1, True, True)

# python3 test_pyfrechet_visualize.py
