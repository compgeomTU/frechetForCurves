from shapely.geometry import Point, Polygon, LineString
import shapely.ops as so

import numpy as np
import matplotlib.pyplot as plt

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

        ve = np.arange(0, ve_count, dtype=np.double)
        he = np.arange(0, he_count, dtype=np.double)

        grid = np.empty([ve_count, he_count], dtype=np.object)
        fs = self.dis.getfreespace()

        # setting each cell point in free space diagram
        for i in range(ve_count-1):
            for j in range(he_count-1):
                grid[i, j] = (ve[i], he[j])

        polys = []

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
                cell_grid[2], cell_grid[3] = cell_grid[3], cell_grid[2]

                points = []

                def addpoint(point):
                    if point not in points: points.append(point)

                if not np.all(cell_fs == (-1, -1)):

                    # point 1
                    # horizontal start
                    if cell_fs[0][0] != -1:
                        x = cell_grid[0][0] + cell_fs[0][0]
                        y = cell_grid[0][1]
                        addpoint((x, y))

                    # vertical start
                    if cell_fs[0][1] != -1:
                        x = cell_grid[0][0]
                        y = cell_grid[0][1] + cell_fs[0][1]
                        addpoint((x, y))

                    # point 2
                    # vertical end
                    if cell_fs[1][0] != -1:
                        x = cell_grid[1][0]
                        y = cell_grid[1][1] + (cell_fs[1][0] - 1)
                        addpoint((x, y))


                    # horizontal start + 1
                    if cell_fs[1][1] != -1:
                        x = cell_grid[1][0] + cell_fs[1][1]
                        y = cell_grid[1][1]
                        addpoint((x, y))

                    # point 4
                    # horizontal end + 1
                    if cell_fs[2][0] != -1:
                        x = cell_grid[2][0] + (cell_fs[2][0] - 1.0)
                        y = cell_grid[2][1]
                        addpoint((x, y))

                    # vetical end + 1
                    if cell_fs[2][1] != -1:
                        x = cell_grid[2][0]
                        y = cell_grid[2][1] + (cell_fs[2][1] - 1.0)
                        addpoint((x, y))

                    # point 3
                    # vetical start + 1
                    if cell_fs[3][0] != -1:
                        x = cell_grid[3][0]
                        y = cell_grid[3][1] + cell_fs[3][0]
                        addpoint((x, y))

                    # horizontal end
                    if cell_fs[3][1] != -1:
                        x = cell_grid[3][0] + (cell_fs[3][1] - 1)
                        y = cell_grid[3][1]
                        addpoint((x, y))

                    if len(points) > 2:
                        polys.append(Polygon(points))

        multi_poly = so.cascaded_union(polys)
        fig, ax = plt.subplots()
        ax.set_aspect('equal', 'datalim')
        ax.set_facecolor('tab:gray')

        try:
            for geom in multi_poly.geoms:
                xs, ys = geom.exterior.xy
                ax.fill(xs, ys, alpha=0.75, fc='w', ec='none')
        except:
                x, y = multi_poly.exterior.xy
                ax.fill(x, y, alpha=0.75, fc='w', ec='none')
        plt.show()


# python3 test_pyfrechet_visualize.py
