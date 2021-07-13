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
    as _wd_create_freespace_reachabilitytable

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



class StrongDistance:

    def __init__(self):
        _sd_createfreespace_reachabilitytable()

    @classmethod
    def setcurves(cls, curve1_filepath, curve2_filepath, \
        reverse_curve2 = False):

        curve1_filepath_ascii = curve1_filepath.encode('ascii')
        curve2_filepath_ascii = curve2_filepath.encode('ascii')

        return_code = _sd_createcurves(curve1_filepath_ascii, \
            curve2_filepath_ascii, reverse_curve2)

        if return_code != 0:

            if return_code == 101:
                raise FileNotFoundError(f"failed to open {curve1_filepath}")

            if return_code == 102:
                raise IOError(f"failed to parse {curve1_filepath}")

            if return_code == 103:
                raise FileNotFoundError(f"failed to open {curve2_filepath}")

            if return_code == 104:
                raise IOError(f"failed to parse {curve2_filepath}")

        return cls()

    def setfreespace(epsilon):
        _sd_setfreespace(epsilon)

    def getverticalcurve():
        return _sd_getverticalcurve()

    def gethorizontalcurve():
        return _sd_gethorizontalcurve()

    def getverticaledges():
        return _sd_getverticaledges()

    def gethorizontaledges():
        return _sd_gethorizontaledges()

    def getfreespace():
        return _sd_getverticaledges()

    def isreachable():
        _sd_setreachabilitytable()
        return _sd_isreachable()

class WeakDistance:

    eps = None

    def __init__(self):
        _wd_createfreespace_reachabilitytable()

    @classmethod
    def  setcurves(cls, curve1_filepath, curve2_filepath, reverse_curve2 = False):
        curve1_filepath_ascii = curve1_filepath.encode('ascii')
        curve2_filepath_ascii = curve2_filepath.encode('ascii')

        return_code = _wd_createcurves(curve1_filepath_ascii, \
        curve2_filepath_ascii, reverse_curve2)

        if return_code != 0:

            if return_code == 101:
                raise FileNotFoundError(f"failed to open {curve1_filepath}")

            if return_code == 102:
                raise IOError(f"failed to parse {curve1_filepath}")

            if return_code == 103:
                raise FileNotFoundError(f"failed to open {curve2_filepath}")

            if return_code == 104:
                raise IOError(f"failed to parse {curve2_filepath}")

        return cls()

    def setfreespace(self, epsilon):
        self.eps = epsilon
        _wd_setfreespace(epsilon)

    def getverticalcurve():
        return _wd_getverticalcurve()

    def gethorizontalcurve():
        return _wd_gethorizontalcurve()

    def getverticaledges():
        return _wd_getverticaledges()

    def gethorizontaledges():
        return _wd_gethorizontaledges()

    def getfreespace():
        return _wd_getverticaledges()

    def isreachable(self):
        if _wd_gethorizontaledges() == 1 or _wd_getverticaledges() == 1:
            return _wd_computemaxdistances(self.eps)
        else:
            return _wd_isreachable()
