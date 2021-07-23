from shapely.geometry import Polygon, LineString

import numpy as np
import matplotlib.pyplot as plt
import random
import math

class FreeSpaceDiagram:

    def __init__(self, distance):
        if type(distance).__name__ == "StrongDistance" or \
            type(distance).__name__ == "WeakDistance":
            self.dis = distance
        else:
            raise TypeError(type(distance).__name__)

    def plot(self, weighted_vertices = False):

        def addpoint(point):
            if point not in points: points.append(point)

        x_axis = self.dis.getverticaledges()
        y_axis = self.dis.gethorizontaledges()
        x_curve = self.dis.getverticalcurve()
        y_curve = self.dis.gethorizontalcurve()
        fs = self.dis.getfreespace()

        grid = np.empty([x_axis, y_axis], dtype="d, d")

        if not weighted_vertices:
            x_vertices = np.ones(x_axis-1, dtype=np.double)
            y_vertices = np.ones(y_axis-1, dtype=np.double)
            x_edges = np.arange(0, x_axis, dtype=np.double)
            y_edges = np.arange(0, y_axis, dtype=np.double)
        else:
            pass

        for i in range(x_axis-1):
            for j in range(y_axis-1):
                grid[i, j] = (x_edges[i], y_edges[j])

        fig, ax = plt.subplots()

        ax.set_facecolor('tab:gray')
        ax.set_xticks(x_edges)
        ax.set_yticks(y_edges)
        ax.set_yticklabels([])
        ax.set_xticklabels([])
        ax.grid(color='black', linewidth = 0.25, alpha = 0.4)

        for i in range(x_axis-2): #range(x_axis-2):
            for j in range(y_axis-2): #range(y_axis-2):

                points = []

                if fs.vertical_end[i][j] != -1:
                    x = grid[i][j][0] + fs.vertical_end[i][j]
                    y = grid[i][j][1]
                    addpoint((x, y))

                if fs.vertical_start[i][j] != -1:
                    x = grid[i][j][0] + fs.vertical_start[i][j]
                    y = grid[i][j][1]
                    addpoint((x, y))

                if fs.horizontal_start[i][j] != -1:
                    x = grid[i][j][0]
                    y = grid[i][j][1] + fs.horizontal_start[i][j]
                    addpoint((x, y))

                if fs.horizontal_end[i][j] != -1:
                    x = grid[i][j][0]
                    y = grid[i][j][1] + fs.horizontal_end[i][j]
                    addpoint((x, y))

                if fs.vertical_start[i][j+1] != -1:
                    x = grid[i+1][j+1][0] - (1 - fs.vertical_start[i][j+1])
                    y = grid[i+1][j+1][1]
                    addpoint((x, y))

                if fs.vertical_end[i][j+1] != -1:
                    x = grid[i+1][j+1][0] - (1 - fs.vertical_end[i][j+1])
                    y = grid[i+1][j+1][1]
                    addpoint((x, y))

                if fs.horizontal_end[i+1][j] != -1:
                    x = grid[i+1][j+1][0]
                    y = grid[i+1][j+1][1] - (1 - fs.horizontal_end[i+1][j])
                    addpoint((x, y))

                if fs.horizontal_start[i+1][j] != -1:
                    x = grid[i+1][j+1][0]
                    y = grid[i+1][j+1][1] - (1 - fs.horizontal_start[i+1][j])
                    addpoint((x, y))


                if len(points) > 2:
                    x, y = Polygon(points).exterior.xy
                    ax.fill(x, y, alpha= 0.8, fc='w', ec='none')

        plt.gca().set_aspect('equal', adjustable='box')
        plt.show()


# python3 test_pyfrechet_visualize.py
