# This program tests graphs both test curves using matplotlib.
#
# Author: Will Rodman
# wrodman@tulane.edu

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

FILENAME1 = "test_IVV.txt"
FILENAME2 = "test_SPY.txt"

curve1 = pd.read_csv(filepath_or_buffer = FILENAME1, delimiter = " ",
                    names = ["x", "y"], index_col = False)
curve2 = pd.read_csv(filepath_or_buffer = FILENAME2, delimiter = " ",
                    names = ["x", "y"], index_col = False)

curve1["x"] = curve1["x"].astype("float64")

plt.title(f"Trajectory Curves from {FILENAME1} and {FILENAME2}")
plt.plot(curve1["x"], curve1["y"], label = FILENAME1, color="blue")
plt.plot(curve2["x"], curve2["y"], label = FILENAME2, color="red")
plt.legend(loc = "upper left")
plt.show()
