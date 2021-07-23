from shapely.geometry import Polygon, LineString
import shapely.ops as so

import numpy as np
import matplotlib.pyplot as plt

import math

class FreeSpaceDiagram:

    def __init__(self, distance):
        if type(distance).__name__ == "StrongDistance" or \
            type(distance).__name__ == "WeakDistance":
            self.dis = distance
        else:
            raise TypeError(type(distance).__name__)

    def plot(self, weighted_vertices = False):
        ve_count = self.dis.getverticaledges()
        he_count = self.dis.gethorizontaledges()
        vc = self.dis.getverticalcurve()
        hc = self.dis.gethorizontalcurve()
        fs = self.dis.getfreespace()
        grid = np.empty([ve_count, he_count], dtype=np.object)

        polys = []
        lss = []

        if not weighted_vertices:
            vv = np.ones(ve_count-1, dtype=np.double)
            hv = np.ones(he_count-1, dtype=np.double)
            ve = np.arange(0, ve_count, dtype=np.double)
            he = np.arange(0, he_count, dtype=np.double)

        else:
            vv = np.empty([ve_count-1], dtype=np.double)
            v = 0
            ve = np.empty([ve_count], dtype=np.double)
            ve[0] = 0
            for i in range(ve_count-2):
                l = math.dist([vc[i].x, vc[i].y], [vc[i+1].x, vc[i+1].y])
                v += l
                vv[i] = l
                ve[i+1] = v

            hv = np.empty([he_count-1], dtype=np.double)
            h = 0
            he = np.empty([he_count], dtype=np.double)
            he[0] = 0
            for i in range(he_count-2):
                l = math.dist([hc[i].x, hc[i].y], [hc[i+1].x, hc[i+1].y])
                h += l
                hv[i] = l
                he[i+1] = h

        # setting each cell point in free space diagram
        for i in range(ve_count-1):
            for j in range(he_count-1):
                grid[i, j] = (ve[i], he[j])

        def addpoint(point):
            if point not in points: points.append(point)

        # loop for every cell in free space diagram
        for i in range(ve_count-2):
            for j in range(he_count-2):

                cell_fs = np.array([(fs.horizontal_start[i][j],   fs.vertical_start[i][j]),       # idx 0: bottom left courner
                                    (fs.vertical_end[i][j],       fs.horizontal_start[i+1][j+1]), # idx 1: top left courner
                                    (fs.horizontal_end[i+1][j+1], fs.vertical_end[i+1][j+1]),     # idx 2: top right courner
                                    (fs.vertical_start[i+1][j+1], fs.horizontal_end[i][j])        # idx 3: bottom right courner
                                    ])

                # Array: [p1, p2, p4, p3]
                cell_grid = np.reshape(grid[i:i+2, j:j+2], 4)
                cell_grid[[2, 3]] = cell_grid[[3, 2]]

                points = []

                # checks free space values courner clockwise
                if not np.all(cell_fs == (-1, -1)):

                    # point 1
                    # horizontal start
                    if cell_fs[0][0] != -1:
                        x = cell_grid[0][0] + (cell_fs[0][0] * vv[i])
                        y = cell_grid[0][1]
                        addpoint((x, y))

                    # vertical start
                    if cell_fs[0][1] != -1:
                        x = cell_grid[0][0]
                        y = cell_grid[0][1] + (cell_fs[0][1] * hv[j])
                        addpoint((x, y))

                    # point 2
                    # vertical end
                    if cell_fs[1][0] != -1:
                        x = cell_grid[1][0]
                        y = cell_grid[1][1] + ((cell_fs[1][0] - 1) * hv[j])
                        addpoint((x, y))

                    # horizontal start + 1
                    if cell_fs[1][1] != -1:
                        x = cell_grid[1][0] + (cell_fs[1][1] * vv[i])
                        y = cell_grid[1][1]
                        addpoint((x, y))

                    # point 4
                    # horizontal end + 1
                    if cell_fs[2][0] != -1:
                        x = cell_grid[2][0] + ((cell_fs[2][0] - 1.0) * vv[i])
                        y = cell_grid[2][1]
                        addpoint((x, y))

                    # vetical end + 1
                    if cell_fs[2][1] != -1:
                        x = cell_grid[2][0]
                        y = cell_grid[2][1] + ((cell_fs[2][1] - 1.0) * hv[j])
                        addpoint((x, y))

                    # point 3
                    # vetical start + 1
                    if cell_fs[3][0] != -1:
                        x = cell_grid[3][0]
                        y = cell_grid[3][1] + (cell_fs[3][0] * hv[j])
                        addpoint((x, y))

                    # horizontal end
                    if cell_fs[3][1] != -1:
                        x = cell_grid[3][0] + ((cell_fs[3][1] - 1.0) * vv[i])
                        y = cell_grid[3][1]
                        addpoint((x, y))

                    if len(points) > 2:
                        polys.append(Polygon(points))
                    else:
                        lss.append(LineString(points))

        fig, ax = plt.subplots()
        ax.set_facecolor('tab:gray')

        ax.set_xticks(ve)
        ax.set_yticks(he)
        ax.set_yticklabels([])
        ax.set_xticklabels([])
        ax.grid(color='black', linewidth = 0.25, alpha = 0.4)

        for poly in polys:
            x, y = poly.exterior.xy
            ax.fill(x, y, alpha= 0.8, fc='w', ec='none')

        for ls in lss:
            x, y = ls.xy
            ax.plot(x, y, color="white", alpha=0.8, linewidth=1.5)

        plt.gca().set_aspect('equal', adjustable='box')
        plt.show()
