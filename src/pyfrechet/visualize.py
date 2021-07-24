from shapely.geometry import Polygon, MultiPolygon
import shapely.ops as so

import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

import numpy as np
import math

class FreeSpaceDiagram:
    dis = None

    x_grid = None
    y_grid = None
    x_curve = None
    y_curve = None

    x_vertices = None
    y_vertices = None
    x_edges = None
    y_edges = None

    def __init__(self, distance):
        if type(distance).__name__ == "StrongDistance" or \
            type(distance).__name__ == "WeakDistance":
            self.dis = distance
            self.x_grid = distance.getverticaledges()
            self.y_grid = distance.gethorizontaledges()
            self.x_curve = distance.getverticalcurve()
            self.y_curve = distance.gethorizontalcurve()
        else:
            raise TypeError(type(distance).__name__)

    def build_cells(self, weighted_vertices=False):
        if not weighted_vertices:
            self.x_vertices = np.ones(self.x_grid-1, dtype=np.double)
            self.y_vertices = np.ones(self.y_grid-1, dtype=np.double)
            self.x_edges = np.arange(0, self.x_grid, dtype=np.double)
            self.y_edges = np.arange(0, self.y_grid, dtype=np.double)
        else:
            self.x_vertices = np.empty([self.x_grid-1], dtype=np.double)
            self.y_vertices = np.empty([self.y_grid-1], dtype=np.double)
            self.x_edges = np.empty([self.x_grid], dtype=np.double)
            self.y_edges = np.empty([self.y_grid], dtype=np.double)
            x_len, self.x_edges[0] = 0, 0
            y_len, self.y_edges[0] = 0, 0

            for i in range(self.x_grid-2):
                length = math.dist([self.x_curve[i].x, self.x_curve[i].y], \
                                   [self.x_curve[i+1].x, self.x_curve[i+1].y])
                self.x_vertices[i] = length
                x_len += length
                self.x_edges[i+1] = x_len

            for i in range(self.y_grid-2):
                length = math.dist([self.y_curve[i].x, self.y_curve[i].y], \
                                   [self.y_curve[i+1].x, self.y_curve[i+1].y])
                self.y_vertices[i] = length
                y_len += length
                self.y_edges[i+1] = y_len

    def build_freespace(self, epsilon):
        def addpoint(point):
            if point not in points: points.append(point)

        self.dis.setfreespace(epsilon)
        fs = self.dis.getfreespace()

        polygons = []
        for i in range(self.x_grid-2):
            for j in range(self.y_grid-2):
                points = []

                if fs.vertical_end[i][j] != -1:
                    x = self.x_edges[i] + (fs.vertical_end[i][j] * \
                        self.x_vertices[i])
                    y = self.y_edges[j]
                    addpoint((x, y))

                if fs.vertical_start[i][j] != -1:
                    x = self.x_edges[i] + (fs.vertical_start[i][j] * \
                        self.x_vertices[i])
                    y = self.y_edges[j]
                    addpoint((x, y))

                if fs.horizontal_start[i][j] != -1:
                    x = self.x_edges[i]
                    y = self.y_edges[j] + (fs.horizontal_start[i][j] * \
                        self.y_vertices[j])
                    addpoint((x, y))

                if fs.horizontal_end[i][j] != -1:
                    x = self.x_edges[i]
                    y = self.y_edges[j] + (fs.horizontal_end[i][j] * \
                        self.y_vertices[j])
                    addpoint((x, y))

                if fs.vertical_start[i][j+1] != -1:
                    x = self.x_edges[i+1] - ((1 - fs.vertical_start[i][j+1]) * \
                        self.x_vertices[i])
                    y = self.y_edges[j+1]
                    addpoint((x, y))

                if fs.vertical_end[i][j+1] != -1:
                    x = self.x_edges[i+1] - ((1 - fs.vertical_end[i][j+1]) * \
                        self.x_vertices[i])
                    y = self.y_edges[j+1]
                    addpoint((x, y))

                if fs.horizontal_end[i+1][j] != -1:
                    x = self.x_edges[i+1]
                    y = self.y_edges[j+1] - ((1 - fs.horizontal_end[i+1][j]) * \
                        self.y_vertices[j])
                    addpoint((x, y))

                if fs.horizontal_start[i+1][j] != -1:
                    x = self.x_edges[i+1]
                    y = self.y_edges[j+1] - ((1 - fs.horizontal_start[i+1][j]) * \
                        self.y_vertices[j])
                    addpoint((x, y))

                if len(points) > 2: polygons.append(Polygon(points))
        return so.cascaded_union(polygons)

    def plot(self, min_epsilon, max_epsilon, precision):
        self.build_cells(weighted_vertices=True)
        valinit = (min_epsilon + precision)

        multipolygons = {}
        for eps in range(min_epsilon, max_epsilon+precision, precision):
            print(f".plot() -- Building Frame for EPS: {eps}\n")
            multipolygons[eps] = self.build_freespace(eps)

        fig, ax = plt.subplots()
        ax_slider = plt.axes([0.2, -0.05, 0.5, 0.2])
        slider = Slider(
            ax=ax_slider,
            label="Epsilon",
            valmin=min_epsilon,
            valmax=max_epsilon,
            valstep=precision,
            color='red'
        )
        slider.label.set_size(20)

        def update(val):
            ax.clear()
            ax.set_facecolor('tab:gray')
            #ax.set_xticks(self.x_edges)
            #ax.set_yticks(self.y_edges)
            #ax.set_yticklabels([])
            #ax.set_xticklabels([])
            #ax.grid(color='black', linewidth = 0.25, alpha = 0.4)
            ax.grid(False)

            for geom in multipolygons[int(val)].geoms:
                xs, ys = geom.exterior.xy
                ax.fill(xs, ys, alpha=0.75, fc='w', ec='none')
            fig.canvas.draw_idle()

        update(min_epsilon)
        slider.on_changed(update)

        plt.gca().set_aspect('equal', adjustable='box')
        plt.show()


# python3 test_pyfrechet_visualize.py
