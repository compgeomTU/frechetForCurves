# This program tests the functionality of the frechet distance c source code
# wrapped using the CFFI API.
#
# Author: Will Rodman
# wrodman@tulane.edu

# roughting system path to _frechet package
import sys
sys.path.insert(0, "../PyFrechet")

# importing frechet functions from package
# shares functions must be renamed if inside same scope to avoid collisions
from _frechet._strong_distance.lib import createcurves as _sd_createcurves
from _frechet._strong_distance.lib import create_freespace_reachabilitytable as _sd_createfreespace_reachabilitytable
from _frechet._strong_distance.lib import setfreespace as _sd_setfreespace
from _frechet._strong_distance.lib import setreachabilitytable as _sd_setreachabilitytable
from _frechet._strong_distance.lib import isreachable as _sd_isreachable

from _frechet._weak_distance.lib import createcurves as _wd_createcurves
from _frechet._weak_distance.lib import create_freespace_reachabilitytable as _wd_create_freespace_reachabilitytable
from _frechet._weak_distance.lib import setfreespace as _wd_setfreespace
from _frechet._weak_distance.lib import isreachable as _wd_isreachable
from _frechet._weak_distance.lib import computemaxdistances as _wd_computemaxdistances

# filepaths to test curves
# all string arguments must be in encoded as ASCII before passing though CFFI
curve1 = "test_curve_1.txt".encode('ascii')
curve2 = "test_curve_2.txt".encode('ascii')

# tests if strong frechet distance functions can find path inside free space
# the minimum epsilon for the test curves is ~67.5
print("TESTING '_frechet._strong_distance.lib':\n")

_sd_createcurves(curve1, curve2, True)
_sd_createfreespace_reachabilitytable();

_sd_setfreespace(60);
_sd_setreachabilitytable();
if _sd_isreachable() == False:
    print("     TEST -- PASSED: Eplison 60 was un reachable")
else:
    print("     TEST -- FAILED: Eplison 60 was reachable")

_sd_setfreespace(70);
_sd_setreachabilitytable();
if _sd_isreachable() == True:
    print("     TEST -- PASSED: Eplison 70 was reachable\n")
else:
    print("     TEST -- FAILED: Eplison 70 was us reachable\n")

# tests if weak frechet distance functions can find path inside free space
# the minimum epsilon for the test curves is ~67.5
print("TESTING '_frechet._weak_distance.lib':\n")

_wd_createcurves(curve1, curve2, True)
_wd_create_freespace_reachabilitytable();

_wd_setfreespace(60);
if _wd_isreachable() == False:
    print("     TEST -- PASSED: Eplison 60 was un reachable")
else:
    print("     TEST -- FAILED: Eplison 60 was reachable")

_wd_setfreespace(70);
if _wd_isreachable() == True:
    print("     TEST -- PASSED: Eplison 70 was reachable\n")
else:
    print("     TEST -- FAILED: Eplison 70 was us reachable\n")
