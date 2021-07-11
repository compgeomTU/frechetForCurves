# This program tests the functionality of the frechet distance c source code
# wrapped using the CFFI API.
#
# Author: Will Rodman
# wrodman@tulane.edu

# roughting system path to _frechet package
import sys
import math

sys.path.insert(0, "../PyFrechet")

# importing frechet functions from package
# shares functions must be renamed if inside same scope to avoid collisions
from _frechet._strong_distance.lib import createcurves
from _frechet._strong_distance.lib import create_freespace_reachabilitytable
from _frechet._strong_distance.lib import setfreespace

from _frechet._strong_distance.lib import gethorizontalverticies
from _frechet._strong_distance.lib import getverticalverticies
from _frechet._strong_distance.lib import getfreespace
from _frechet._strong_distance.lib import gethorizontalcurve
from _frechet._strong_distance.lib import getverticalcurve



# filepaths to test curves
# all string arguments must be in encoded as ASCII before passing though CFFI
curve1 = "test_curve_1.txt".encode('ascii')
curve2 = "test_curve_2.txt".encode('ascii')



print("TESTING\n")

createcurves(curve1, curve2, True);
create_freespace_reachabilitytable();
setfreespace(70);



hv = int(gethorizontalverticies())
vv = int(getverticalverticies())
fs = getfreespace()
hc = gethorizontalcurve()
vc = getverticalcurve()



hc_eds = []
vc_eds = []
for i in range(hv-1):
  hc_eds.append(math.dist(
        [hc[i].x, hc[i].y], [hc[i+1].x, hc[i+1].y]))

for i in range(vv-1):
    vc_eds.append(math.dist(
        [vc[i].x, vc[i].y], [vc[i+1].x, vc[i+1].y]))



SAMPLE_SIZE = 20
hc_ed = 0
vc_ed = 0

hs = []
he = []
vs = []
ve = []
for i in range(SAMPLE_SIZE): #range(hv-1):

    ths =[]
    the =[]
    tvs = []
    tve = []
    for j in range(SAMPLE_SIZE): #range(vv-1):

        if (fs.horizontal_end[i][j] != -1.0) and \
           (fs.horizontal_start[i][j] != -1.0) and \
           (fs.vertical_start[i][j] != -1.0) and \
           (fs.vertical_end[i][j] != -1.0):

            whs = hc_ed + (fs.horizontal_start[i][j] * hc_eds[i])

            ths.append(whs)

            if j == 0: hc_ed += hc_eds[i]

            whe = hc_ed - (fs.horizontal_end[i][j] * hc_eds[i])
            the.append(whe)

            wvs = vc_ed + (fs.vertical_start[i][j] * vc_eds[j])
            tvs.append(wvs)

            vc_ed += vc_eds[j]

            wve = vc_ed - (fs.vertical_end[i][j] * vc_eds[j])
            tve.append(wve)

    hs.append(ths)
    he.append(the)
    vs.append(tvs)
    ve.append(tve)



print(hs)


# python3 test_free_space.py
