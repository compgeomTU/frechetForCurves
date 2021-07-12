# This program tests the functionality of the frechet distance c source code
# wrapped using the CFFI API.
#
# Author: Will Rodman
# wrodman@tulane.edu

# roughting system path to _frechet package
import sys
import math
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker

sys.path.insert(0, "../PyFrechet")

# importing frechet functions from package
# shares functions must be renamed if inside same scope to avoid collisions
from _frechet._strong_distance.lib import createcurves
from _frechet._strong_distance.lib import create_freespace_reachabilitytable
from _frechet._strong_distance.lib import setfreespace

from _frechet._strong_distance.lib import gethorizontaledges
from _frechet._strong_distance.lib import getverticaledges
from _frechet._strong_distance.lib import getfreespace
from _frechet._strong_distance.lib import gethorizontalcurve
from _frechet._strong_distance.lib import getverticalcurve



# filepaths to test curves
# all string arguments must be in encoded as ASCII before passing though CFFI
curve1 = "test_curve_1.txt".encode('ascii')
curve2 = "test_curve_2.txt".encode('ascii')



createcurves(curve1, curve2, True);
create_freespace_reachabilitytable();
setfreespace(500);
fs = getfreespace()
hc = gethorizontalcurve()
vc = getverticalcurve()
he = gethorizontaledges()
ve = getverticaledges()



hv = []
vv = []
for i in range(he-1):
  hv.append(math.dist(
        [hc[i].x, hc[i].y], [hc[i+1].x, hc[i+1].y]))
for i in range(ve-1):
    vv.append(math.dist(
        [vc[i].x, vc[i].y], [vc[i+1].x, vc[i+1].y]))



x = []
y = []
free_x = []
free_y = []

for i in range(ve-1):
    for j in range(he-1):

        if fs.vertical_start[i][j] == -1.0:
            y.append(j + fs.vertical_start[i][j])
            x.append(i)
        else:
            free_y.append(j + fs.vertical_start[i][j])
            free_x.append(i)

        if fs.vertical_start[i][j] == -1.0:
            y.append(j + fs.vertical_end[i][j])
            x.append(i)
        else:
            free_y.append(j + fs.vertical_end[i][j])
            free_x.append(i)

        if fs.horizontal_start[i][j] == -1.0:
            y.append(j)
            x.append(i + fs.horizontal_start[i][j])
        else:
            free_y.append(j)
            free_x.append(i + fs.horizontal_start[i][j])

        if fs.horizontal_end[i][j] == -1.0:
            y.append(j)
            x.append(i + fs.horizontal_end[i][j])
        else:
            free_y.append(j)
            free_x.append(i + fs.horizontal_end[i][j])

fig, ax = plt.subplots()
plt.plot(x, y, 'o', c = 'grey', markersize = 12)
plt.plot(free_x, free_y, 'o', c = 'white', markersize = 9.5)

plt.show()


# python3 test_free_space.py
