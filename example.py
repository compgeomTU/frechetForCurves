import sys, os, unittest

sys.path.insert(0, "src/pyfrechet/")
from distance import StrongDistance, WeakDistance
from visualize import FreeSpaceDiagram

strong_distance = StrongDistance.setCurves("test/trajectory_data/sample_1.txt", "test/trajectory_data/sample_2.txt", reverse_curve_2=True)
strong_distance.setFreeSpace(100)

free_space_diagram = FreeSpaceDiagram(strong_distance)
free_space_diagram.plot()
