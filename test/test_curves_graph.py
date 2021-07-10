# This program tests graphs both test curves using matplotlib.
#
# Author: Will Rodman
# wrodman@tulane.edu

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

curve1 = pd.read_csv(filepath_or_buffer = "test_curve_1.txt", delimiter = " ",
                    names = ["x", "y"], index_col = False)
curve2 = pd.read_csv(filepath_or_buffer = "test_curve_2.txt", delimiter = " ",
                    names = ["x", "y"], index_col = False)

curve1["x"] = curve1["x"].astype("float64")

plt.title("Sample Data Used in Dr.Wenk's Frechet Distance Program")
plt.plot(curve1["x"], curve1["y"], label = "test_curve_1.txt")
plt.plot(curve2["x"], curve2["y"], label = "test_curve_2.txt")
plt.legend(loc = "upper left")
plt.show()
