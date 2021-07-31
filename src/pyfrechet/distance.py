## @package pyfrechet
#  Documentation for this module.

from _frechet._strong_distance.lib import createcurves as _sd_createcurves
from _frechet._strong_distance.lib import create_freespace_reachabilitytable \
    as _sd_createfreespace_reachabilitytable

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
    as _wd_createfreespace_reachabilitytable

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

class StrongDistance:

    __curve_1_file: str
    __curve_2_file: str

    def __init__(self, curve_1_file, curve_2_file):
        self.__curve_1_file = curve_1_file
        self.__curve_2_file = curve_2_file
        _sd_createfreespace_reachabilitytable()

    def __str__(self):
        try:
            return f"""Frechet Distance Type  |  {self.__name__}
                       Curve 1 File           |  {self.__curve_1_file}
                       Curve 2 File           |  {self.__curve_2_file}
                    """
        except:
            return f"{self.__name__} is empty."

    @classmethod
    def setCurves(cls, curve_1_file, curve_2_file, \
        reverse_curve2 = False):

        curve1_abs = os.path.abspath(curve_1_file)
        curve2_abs = os.path.abspath(curve_2_file)

        curve1_ascii = curve1_abs.encode('ascii')
        curve2_ascii = curve2_abs.encode('ascii')

        errno = _sd_createcurves(curve1_ascii, curve2_ascii, reverse_curve2)

        if errno != 0:
            raise IOError(f"{os.strerror(errno)} --"
                          f"Check {curve_1_file} and {curve_2_file}"
                          f"filepath and format for error."
                           )

        return cls(curve_1_file, curve_2_file)

    def setFreespace(self, epsilon):
        _sd_setfreespace(epsilon)

    def getCurve2(self):
        return _sd_getcurve2()

    def getCurve1(self):
        return _sd_getcurve1()

    def getCurve2Lenght(self):
        return _sd_getcurve2lenght()

    def getCurve1Lenght(self):
        return _sd_getcurve1lenght()

    def getFreespace(self):
        return _sd_getfreespace()

    def getFileNames(self):
        return self.__curve_1_file, self.__curve_2_file

    def isReachable(self):
        _sd_setreachabilitytable()
        return _sd_isreachable()

class WeakDistance:

    __curve_1_file: str
    __curve_2_file: str
    __epsilon: float

    def __init__(self, curve_1_file, curve_2_file):
        self.__curve_1_file = curve_1_file
        self.__curve_2_file = curve_2_file
        _sd_createfreespace_reachabilitytable()

    def __str__(self):
        try:
            return f"""Frechet Distance Type  |  {self.__name__}
                       Curve 1 File           |  {self.__curve_1_file}
                       Curve 2 File           |  {self.__curve_2_file}
                    """
        except:
            return f"{self.__name__} is empty."

    @classmethod
    def setCurves(cls, curve_1_file, curve_2_file, \
        reverse_curve2 = False):

        self.__curve_1_file = curve_1_file
        self.__curve_2_file = curve_2_file

        curve1_abs = os.path.abspath(curve_1_file)
        curve2_abs = os.path.abspath(curve_2_file)

        curve1_ascii = curve1_abs.encode('ascii')
        curve2_ascii = curve2_abs.encode('ascii')

        errno = _wd_createcurves(curve1_ascii, curve2_ascii, reverse_curve2)

        if errno != 0:
            raise IOError(f"{os.strerror(errno)} --"
                          f"Check {curve_1_file} and {curve_2_file}"
                          f"filepath and format for error."
                           )

        return cls(curve_1_file, curve_2_file)

    def setFreespace(self, epsilon):
        self.__epsilon = epsilon
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

    def getFileNames(self):
        return self.__curve_1_file, self.__curve_2_file

    def isReachable(self):
        if _wd_getcurve1lenght() == 1 or _wd_getcurve2lenght() == 1:
            try:
                return _wd_computemaxdistances(self.__epsilon)
            except ValueError:
                raise ValueError("No value for Epsilon exists because"
                                 "setfreespace() was never called.")
        else:
            return _wd_isreachable()
