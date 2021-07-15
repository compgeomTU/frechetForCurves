from _frechet._strong_distance.lib import createcurves as _sd_createcurves
from _frechet._strong_distance.lib import create_freespace_reachabilitytable \
    as _sd_createfreespace_reachabilitytable

from _frechet._strong_distance.lib import setfreespace as _sd_setfreespace
from _frechet._strong_distance.lib import setreachabilitytable as \
    _sd_setreachabilitytable

from _frechet._strong_distance.lib import getverticalcurve as \
    _sd_getverticalcurve
from _frechet._strong_distance.lib import gethorizontalcurve as \
    _sd_gethorizontalcurve
from _frechet._strong_distance.lib import gethorizontaledges as \
    _sd_gethorizontaledges
from _frechet._strong_distance.lib import getverticaledges as \
    _sd_getverticaledges
from _frechet._strong_distance.lib import getfreespace as \
    _sd_getfreespace

from _frechet._strong_distance.lib import isreachable as _sd_isreachable

from _frechet._weak_distance.lib import createcurves as _wd_createcurves
from _frechet._weak_distance.lib import create_freespace_reachabilitytable \
    as _wd_createfreespace_reachabilitytable

from _frechet._weak_distance.lib import setfreespace as _wd_setfreespace
from _frechet._weak_distance.lib import computemaxdistances as \
    _wd_computemaxdistances

from _frechet._weak_distance.lib import getverticalcurve as \
    _wd_getverticalcurve
from _frechet._weak_distance.lib import gethorizontalcurve as \
    _wd_gethorizontalcurve
from _frechet._weak_distance.lib import gethorizontaledges as \
    _wd_gethorizontaledges
from _frechet._weak_distance.lib import getverticaledges as \
    _wd_getverticaledges
from _frechet._weak_distance.lib import getfreespace as \
    _wd_getfreespace

from _frechet._weak_distance.lib import isreachable as _wd_isreachable

import os

class StrongDistance:

    def __init__(self):
        _sd_createfreespace_reachabilitytable()

    @classmethod
    def setcurves(cls, curve_1_filepath, curve_2_filepath, \
        reverse_curve2 = False):

        c1_abs_fp_ascii = os.path.abspath(curve_1_filepath).encode('ascii')
        c2_abs_fp_ascii = os.path.abspath(curve_2_filepath).encode('ascii')

        exit_status = _sd_createcurves(c1_abs_fp_ascii, c2_abs_fp_ascii, \
            reverse_curve2)

        if exit_status != 0: raise IOError(os.strerror(exit_status))

        return cls()

    def setfreespace(self, epsilon):
        _sd_setfreespace(epsilon)

    def getverticalcurve(self):
        return _sd_getverticalcurve()

    def gethorizontalcurve(self):
        return _sd_gethorizontalcurve()

    def getverticaledges(self):
        return _sd_getverticaledges()

    def gethorizontaledges(self):
        return _sd_gethorizontaledges()

    def getfreespace(self):
        return _sd_getfreespace()

    def isreachable(self):
        _sd_setreachabilitytable()
        return _sd_isreachable()

class WeakDistance:

    eps = None

    def __init__(self):
        _wd_createfreespace_reachabilitytable()

    @classmethod
    def  setcurves(cls, curve_1_filepath, curve_2_filepath, reverse_curve2 = False):

        c1_abs_fp_ascii = os.path.abspath(curve_1_filepath).encode('ascii')
        c2_abs_fp_ascii = os.path.abspath(curve_2_filepath).encode('ascii')

        exit_status = _wd_createcurves(c1_abs_fp_ascii, c2_abs_fp_ascii, \
            reverse_curve2)

        if exit_status != 0: raise IOError(os.strerror(exit_status))

        return cls()

    def setfreespace(self, epsilon):
        self.eps = epsilon
        _wd_setfreespace(epsilon)

    def getverticalcurve(self):
        return _wd_getverticalcurve()

    def gethorizontalcurve(self):
        return _wd_gethorizontalcurve()

    def getverticaledges(self):
        return _wd_getverticaledges()

    def gethorizontaledges(self):
        return _wd_gethorizontaledges()

    def getfreespace(self):
        return _wd_getfreespace()

    def isreachable(self):
        if _wd_gethorizontaledges() == 1 or _wd_getverticaledges() == 1:
            return _wd_computemaxdistances(self.eps)
        else:
            return _wd_isreachable()