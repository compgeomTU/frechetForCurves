from shapely.geometry import Polygon, MultiPolygon
import shapely.ops as so

import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

import numpy as np
import math

from distance import *

class FreespaceDiagram:

    def __init__(self, distance):
        if isinstance(distance, StrongDistance) or \
           isinstance(distance, WeakDistance):
            self.dis = distance
            self.__x_grid = distance.getCurve2Lenght()
            self.__y_grid = distance.getCurve1Lenght()
            self.__x_curve = distance.getCurve2()
            self.__y_curve = distance.getCurve1()
        else:
            raise TypeError(f"{distance.__name__} is not a valid distance."
                            f"Must be of type {StrongDistance.__name__} or "
                            f"{WeakDistance.__name__}."
                            )

    def _build_cells(self, weighted_cells=False):
        if not weighted_cells:
            self.__x_vertices = np.ones(self.__x_grid-1, dtype=np.double)
            self.__y_vertices = np.ones(self.__y_grid-1, dtype=np.double)
            self.__x_edges = np.arange(0, self.__x_grid, dtype=np.double)
            self.__y_edges = np.arange(0, self.__y_grid, dtype=np.double)
        else:
            self.__x_vertices = np.empty([self.__x_grid-1], dtype=np.double)
            self.__y_vertices = np.empty([self.__y_grid-1], dtype=np.double)
            self.__x_edges = np.empty([self.__x_grid], dtype=np.double)
            self.__y_edges = np.empty([self.__y_grid], dtype=np.double)
            x_len, self.__x_edges[0] = 0, 0
            y_len, self.__y_edges[0] = 0, 0

            for i in range(self.__x_grid-2):
                length = math.dist([self.__x_curve[i].x, self.__x_curve[i].y], \
                                   [self.__x_curve[i+1].x, self.__x_curve[i+1].y])
                self.__x_vertices[i] = length
                x_len += length
                self.__x_edges[i+1] = x_len

            for i in range(self.__y_grid-2):
                length = math.dist([self.__y_curve[i].x, self.__y_curve[i].y], \
                                   [self.__y_curve[i+1].x, self.__y_curve[i+1].y])
                self.__y_vertices[i] = length
                y_len += length
                self.__y_edges[i+1] = y_len

    def _build_freespace(self, epsilon):
        def addpoint(point):
            if point not in points: points.append(point)

        self.dis.setFreespace(epsilon)
        fs = self.dis.getFreespace()

        polygons = []
        for i in range(self.__x_grid-2):
            for j in range(self.__y_grid-2):
                points = []

                if fs.vertical_end[i][j] != -1:
                    x = self.__x_edges[i] + (fs.vertical_end[i][j] * \
                        self.__x_vertices[i])
                    y = self.__y_edges[j]
                    addpoint((x, y))

                if fs.vertical_start[i][j] != -1:
                    x = self.__x_edges[i] + (fs.vertical_start[i][j] * \
                        self.__x_vertices[i])
                    y = self.__y_edges[j]
                    addpoint((x, y))

                if fs.horizontal_start[i][j] != -1:
                    x = self.__x_edges[i]
                    y = self.__y_edges[j] + (fs.horizontal_start[i][j] * \
                        self.__y_vertices[j])
                    addpoint((x, y))

                if fs.horizontal_end[i][j] != -1:
                    x = self.__x_edges[i]
                    y = self.__y_edges[j] + (fs.horizontal_end[i][j] * \
                        self.__y_vertices[j])
                    addpoint((x, y))

                if fs.vertical_start[i][j+1] != -1:
                    x = self.__x_edges[i+1] - ((1 - fs.vertical_start[i][j+1]) * \
                        self.__x_vertices[i])
                    y = self.__y_edges[j+1]
                    addpoint((x, y))

                if fs.vertical_end[i][j+1] != -1:
                    x = self.__x_edges[i+1] - ((1 - fs.vertical_end[i][j+1]) * \
                        self.__x_vertices[i])
                    y = self.__y_edges[j+1]
                    addpoint((x, y))

                if fs.horizontal_end[i+1][j] != -1:
                    x = self.__x_edges[i+1]
                    y = self.__y_edges[j+1] - ((1 - fs.horizontal_end[i+1][j]) * \
                        self.__y_vertices[j])
                    addpoint((x, y))

                if fs.horizontal_start[i+1][j] != -1:
                    x = self.__x_edges[i+1]
                    y = self.__y_edges[j+1] - ((1 - fs.horizontal_start[i+1][j]) * \
                        self.__y_vertices[j])
                    addpoint((x, y))

                if len(points) > 2: polygons.append(Polygon(points))
        return so.cascaded_union(polygons)

    def plot(self, min_epsilon, max_epsilon, precision, \
             weighted_cells = False, gridlines = False):

        self._build_cells(weighted_cells=weighted_cells)
        f1, f2 = self.dis.getFileNames()

        multipolygons = {}
        for eps in range(min_epsilon, max_epsilon+precision, precision):
            print(f"FreeSpaceDiagram -- Building Frame for EPS: {eps}\n")
            multipolygons[float(eps)] = self._build_freespace(eps)

        fig, ax = plt.subplots()
        plt.subplots_adjust(left=0.2, bottom=0.2)

        ax_slider = plt.axes([0.25, 0.1, 0.65, 0.03])
        slider = Slider(
            ax=ax_slider,
            label="Epsilon",
            valmin=min_epsilon,
            valmax=max_epsilon,
            valstep=precision,
            valinit=max_epsilon-precision,
            color='red'
        )

        def update(val):
            ax.clear()
            ax.set_facecolor('tab:gray')
            ax.set_title("Freespace Diagram")
            ax.set_xlabel(f2)
            ax.set_ylabel(f1)

            if gridlines:
                ax.set_xticks(self.__x_edges)
                ax.set_yticks(self.__y_edges)
                ax.set_yticklabels([])
                ax.set_xticklabels([])
                ax.grid(color='black', linewidth = 0.25, alpha = 0.4)
            else:
                ax.grid(False)

            try:
                for geom in multipolygons[val].geoms:
                    xs, ys = geom.exterior.xy
                    ax.fill(xs, ys, alpha=0.75, fc='w', ec='none')
            except:
                xs, ys = multipolygons[val].exterior.xy
                ax.fill(xs, ys, alpha=0.75, fc='w', ec='none')
            fig.canvas.draw_idle()

        update(max_epsilon-precision)
        slider.on_changed(update)

        plt.gca().set_aspect('equal', adjustable='datalim')
        plt.show()
