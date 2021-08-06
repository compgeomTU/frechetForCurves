## @package pyfrechet
#  Documentation for this module.

from _frechet._strong_distance.lib import createcurves as _sd_createcurves
from _frechet._strong_distance.lib import create_freespace_reachabilitytable \
    as _sd_create_freespace_reachabilitytable

from _frechet._strong_distance.lib import setfreespace as _sd_setfreespace
from _frechet._strong_distance.lib import setreachabilitytable as \
    _sd_setreachabilitytable

from _frechet._strong_distance.lib import getcurve2 as _sd_getcurve2
from _frechet._strong_distance.lib import getcurve1 as _sd_getcurve1
from _frechet._strong_distance.lib import getcurve1lenght as \
    _sd_getcurve1lenght
from _frechet._strong_distance.lib import getcurve2lenght as \
    _sd_getcurve2lenght
from _frechet._strong_distance.lib import getfreespace as \
    _sd_getfreespace

from _frechet._strong_distance.lib import isreachable as _sd_isreachable

from _frechet._weak_distance.lib import createcurves as _wd_createcurves
from _frechet._weak_distance.lib import create_freespace_reachabilitytable \
    as _wd_create_freespace_reachabilitytable

from _frechet._weak_distance.lib import setfreespace as _wd_setfreespace
from _frechet._weak_distance.lib import computemaxdistances as \
    _wd_computemaxdistances

from _frechet._weak_distance.lib import getcurve2 as _wd_getcurve2
from _frechet._weak_distance.lib import getcurve1 as _wd_getcurve1
from _frechet._weak_distance.lib import getcurve1lenght as \
    _wd_getcurve1lenght
from _frechet._weak_distance.lib import getcurve2lenght as \
    _wd_getcurve2lenght
from _frechet._weak_distance.lib import getfreespace as \
    _wd_getfreespace

from _frechet._weak_distance.lib import isreachable as _wd_isreachable

import os

class Distance:

    _curve_1_file: str
    _curve_2_file: str

    _epsilon: float

    def __init__(self, curve_1_file, curve_2_file):
        curve1_abspath = os.path.abspath(curve_1_file)
        curve2_abspath = os.path.abspath(curve_2_file)

        curve1_ascii = curve1_abspath.encode('ascii')
        curve2_ascii = curve2_abspath.encode('ascii')

        self._curve_1_file = curve1_ascii
        self._curve_2_file = curve2_ascii

    def __str__(self, name):
        try:
            curve_1_file, curve_2_file = self._curve_1_file, self._curve_2_file
        except:
            curve_1_file, curve_2_file = "N/A", "N/A"
        return f"""
                Frechet Distance       |  {name}
                ========================================
                Curve 1 File           |  {curve_1_file}
                Curve 2 File           |  {curve_2_file}
                """


    def _checkSetCurvesErrno(self, errno):
        if errno != 0:
            raise IOError(f"{os.strerror(errno)} raised while running setCurves().\n"
                          f"Check file paths and formats for error:\n"
                          f"{self._curve_1_file}\n"
                          f"{self._curve_2_file}"
                           )

    def getFileNames(self): return self._curve_1_file, self._curve_2_file

    def getEpsilon(self): return self._epsilon

class StrongDistance(Distance):

    def __init__(self):
        _sd_create_freespace_reachabilitytable()

    def __str__(self):
        return super().__str__(self.__class__.__name__)

    @classmethod
    def setCurves(cls, curve_1_file, curve_2_file, reverse_curve2=False):
        self = cls.__new__(cls)
        super(StrongDistance, self).__init__(curve_1_file, curve_2_file)
        errno = _sd_createcurves(self._curve_1_file, self._curve_2_file, \
                                 reverse_curve2)
        self._checkSetCurvesErrno(errno)
        self.__init__()
        return self

    def setFreeSpace(self, epsilon):
        self._epsilon = epsilon
        _sd_setfreespace(epsilon)

    def getCurve2(self):
        return _sd_getcurve2()

    def getCurve1(self):
        return _sd_getcurve1()

    def getCurve2Lenght(self):
        return _sd_getcurve2lenght()

    def getCurve1Lenght(self):
        return _sd_getcurve1lenght()

    def getFreeSpace(self):
        return _sd_getfreespace()

    def isReachable(self):
        _sd_setreachabilitytable()
        return _sd_isreachable()

class WeakDistance(Distance):

    def __init__(self):
        _wd_create_freespace_reachabilitytable()

    def __str__(self):
        return super().__str__(self.__class__.__name__)

    @classmethod
    def setCurves(cls, curve_1_file, curve_2_file, reverse_curve2=False):
        self = cls.__new__(cls)
        super(WeakDistance, self).__init__(curve_1_file, curve_2_file)
        errno = _wd_createcurves(self._curve_1_file, self._curve_2_file, \
                                 reverse_curve2)
        self._checkSetCurvesErrno(errno)
        self.__init__()
        return self

    def setFreeSpace(self, epsilon):
        self._epsilon = epsilon
        _wd_setfreespace(epsilon)

    def getCurve2(self):
        return _wd_getcurve2()

    def getCurve1(self):
        return _wd_getcurve1()

    def getCurve2Lenght(self):
        return _wd_getcurve2lenght()

    def getCurve1Lenght(self):
        return _wd_getcurve1lenght()

    def getFreeSpace(self):
        return _wd_getfreespace()

    def isReachable(self):
        if _wd_getcurve1lenght() == 1 or _wd_getcurve2lenght() == 1:
            try:
                return _wd_computemaxdistances(super()._epsilon)
            except ValueError:
                raise ValueError("No value for Epsilon exists because"
                                 "setfreespace() was never called.")
        else:
            return _wd_isreachable()
