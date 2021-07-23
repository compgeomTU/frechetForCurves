from shapely.geometry import Polygon, MultiPolygon
import shapely.ops as so
import numpy as np
import matplotlib.pyplot as plt
import math

class FreeSpaceDiagram:

    dis = None
    multipolygon = None
    x_edges = None
    y_edges = None

    def __init__(self, distance):
        if type(distance).__name__ == "StrongDistance" or \
            type(distance).__name__ == "WeakDistance":
            self.dis = distance
        else:
            raise TypeError(type(distance).__name__)

    def build_multipolygon(self, weighted_vertices = False):
        def addpoint(point):
            if point not in points: points.append(point)

        x_grid = self.dis.getverticaledges()
        y_grid = self.dis.gethorizontaledges()
        x_curve = self.dis.getverticalcurve()
        y_curve = self.dis.gethorizontalcurve()
        fs = self.dis.getfreespace()

        if not weighted_vertices:
            x_vertices = np.ones(x_grid-1, dtype=np.double)
            y_vertices = np.ones(y_grid-1, dtype=np.double)
            x_edges = np.arange(0, x_grid, dtype=np.double)
            y_edges = np.arange(0, y_grid, dtype=np.double)
        else:
            x_vertices = np.empty([x_grid-1], dtype=np.double)
            y_vertices = np.empty([y_grid-1], dtype=np.double)
            x_edges = np.empty([x_grid], dtype=np.double)
            y_edges = np.empty([y_grid], dtype=np.double)
            x_len, x_edges[0] = 0, 0
            y_len, y_edges[0] = 0, 0

            for i in range(x_grid-2):
                length = math.dist([x_curve[i].x, x_curve[i].y], \
                                   [x_curve[i+1].x, x_curve[i+1].y])
                x_vertices[i] = length
                x_len += length
                x_edges[i+1] = x_len

            for i in range(y_grid-2):
                length = math.dist([y_curve[i].x, y_curve[i].y], \
                                   [y_curve[i+1].x, y_curve[i+1].y])
                y_vertices[i] = length
                y_len += length
                y_edges[i+1] = y_len

        polygons = []

        for i in range(x_grid-2):
            for j in range(y_grid-2):
                points = []

                if fs.vertical_end[i][j] != -1:
                    x = x_edges[i] + (fs.vertical_end[i][j] * x_vertices[i])
                    y = y_edges[j]
                    addpoint((x, y))

                if fs.vertical_start[i][j] != -1:
                    x = x_edges[i] + (fs.vertical_start[i][j] * x_vertices[i])
                    y = y_edges[j]
                    addpoint((x, y))

                if fs.horizontal_start[i][j] != -1:
                    x = x_edges[i]
                    y = y_edges[j] + (fs.horizontal_start[i][j] * y_vertices[j])
                    addpoint((x, y))

                if fs.horizontal_end[i][j] != -1:
                    x = x_edges[i]
                    y = y_edges[j] + (fs.horizontal_end[i][j] * y_vertices[j])
                    addpoint((x, y))

                if fs.vertical_start[i][j+1] != -1:
                    x = x_edges[i+1] - ((1 - fs.vertical_start[i][j+1]) * \
                        x_vertices[i])
                    y = y_edges[j+1]
                    addpoint((x, y))

                if fs.vertical_end[i][j+1] != -1:
                    x = x_edges[i+1] - ((1 - fs.vertical_end[i][j+1]) * \
                        x_vertices[i])
                    y = y_edges[j+1]
                    addpoint((x, y))

                if fs.horizontal_end[i+1][j] != -1:
                    x = x_edges[i+1]
                    y = y_edges[j+1] - ((1 - fs.horizontal_end[i+1][j]) * \
                        y_vertices[j])
                    addpoint((x, y))

                if fs.horizontal_start[i+1][j] != -1:
                    x = x_edges[i+1]
                    y = y_edges[j+1] - ((1 - fs.horizontal_start[i+1][j]) * \
                        y_vertices[j])
                    addpoint((x, y))

                if len(points) > 2: polygons.append(Polygon(points))

        self.multipolygon = so.cascaded_union(polygons)
        self.x_edges = x_edges
        self.y_edges = y_edges

    def plot(self):
        fig, ax = plt.subplots()
        ax.set_facecolor('tab:gray')
        ax.set_xticks(self.x_edges)
        ax.set_yticks(self.y_edges)
        ax.set_yticklabels([])
        ax.set_xticklabels([])
        ax.grid(color='black', linewidth = 0.25, alpha = 0.4)

        for geom in self.multipolygon.geoms:
            xs, ys = geom.exterior.xy
            ax.fill(xs, ys, alpha=0.75, fc='w', ec='none')

        plt.gca().set_aspect('equal', adjustable='box')
        plt.show()


# python3 test_pyfrechet_visualize.py
