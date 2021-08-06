# Author: Will Rodman
# wrodman@tulane.edu
#
# Command line to run program:
# python3 plot_data.py

import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt

import unittest

TEST_DATA = 'sp500'

FILENAME1 = f"{TEST_DATA}_data/sample_1.txt"
FILENAME2 = f"{TEST_DATA}_data/sample_2.txt"

class plot_data(unittest.TestCase):

    global FILENAME1
    global FILENAME2

    def setUp(self):
        print(self._testMethodName)

    def test_plot_data(self):
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
        time.sleep(5)
        plt.close()

if __name__ == '__main__':
    unittest.main()
