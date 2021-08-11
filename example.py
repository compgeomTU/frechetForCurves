import sys, os, unittest

sys.path.insert(0, "src/pyfrechet/")
from distance import StrongDistance, WeakDistance
from optimise import BinarySearch

strong_distance = StrongDistance.setCurves("test/trajectory_data/sample_1.txt", "test/trajectory_data/sample_2.txt", reverse_curve_2=True)
binary_search = BinarySearch(strong_distance)

binary_search.setBoundaries(left=50, right=100)
binary_search.setPercision(0.001)
eps = binary_search.search()
print(eps)
