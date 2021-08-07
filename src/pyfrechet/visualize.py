from shapely.geometry import Polygon, MultiPolygon
import shapely.ops as so

import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

import numpy as np
import math

from distance import Distance

class FreeSpaceDiagram:

    __polys: dict
    __buildSlider: bool

    def __init__(self, distance):
        if isinstance(distance, Distance):
            self.__dis = distance
            self.__x_grid = distance.getCurve2Lenght()
            self.__y_grid = distance.getCurve1Lenght()
            self.__x_curve = distance.getCurve2()
            self.__y_curve = distance.getCurve1()
            self.__polys = dict()
            self.__buildSlider = False
        else:
            name_ = distance.__class__.__name__
            raise TypeError(f"{name_} is not a valid argument."
                            f"Must be of type StrongDistance or WeakDistance."
                            )

    def __build_cells(self, weighted_cells):
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

    def __build_freespace(self):
        def addpoint(point):
            if point not in points: points.append(point)

        fs = self.__dis.getFreeSpace()

        polygons = list()
        for i in range(self.__x_grid-2):
            for j in range(self.__y_grid-2):
                points = list()

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

    def addSlider(self, min_epsilon, max_epsilon, precision):
        self.__buildSlider = True
        self.__min_epsilon = min_epsilon
        self.__max_epsilon = max_epsilon
        self.__precision = precision

    def plot(self, weighted_cells=False, gridlines=False):
        f1, f2 = self.__dis.getFileNames()
        self.__build_cells(weighted_cells=weighted_cells)
        fig, ax = plt.subplots()

        if self.__buildSlider:
            plt.subplots_adjust(bottom=0.2)

            for eps in np.arange(self.__min_epsilon,
                                 self.__max_epsilon+self.__precision, \
                                 self.__precision):
                self.__dis.setFreeSpace(eps)
                self.__polys[float(eps)] = self.__build_freespace()

            ax_slider = plt.axes([0.25, 0.1, 0.65, 0.03])
            slider = Slider(
                ax=ax_slider,
                label="Epsilon",
                valmin=self.__min_epsilon,
                valmax=self.__max_epsilon,
                valstep=self.__precision,
                valinit=self.__max_epsilon-self.__min_epsilon,
                color='red'
            )
        else:
            self.__polys[self.__dis.getEpsilon()] = self.__build_freespace()

        def update(val):
            ax.clear()
            ax.set_facecolor('tab:gray')
            name_ = self.__dis.__class__.__name__
            ax.set_title(f"{name_} Free Space Diagram  |  Epsilon: {val}")
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

            if self.__polys[val].geom_type == 'MultiPolygon':
                for geom in self.__polys[val].geoms:
                    xs, ys = geom.exterior.xy
                    ax.fill(xs, ys, alpha=0.75, fc='w', ec='none')
            elif self.__polys[val].geom_type == 'Polygon':
                xs, ys = self.__polys[val].exterior.xy
                ax.fill(xs, ys, alpha=0.75, fc='w', ec='none')
            fig.canvas.draw_idle()

        if self.__buildSlider:
            update(self.__max_epsilon-self.__precision)
            slider.on_changed(update)
        else:
            update(self.__dis.getEpsilon())

        plt.show()

    def close(self): plt.close()
