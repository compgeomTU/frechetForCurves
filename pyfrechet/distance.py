## @package pyfrechet
#
#  Module for working with Frechet distances.

from _strong_distance.lib import createcurves as _sd_createcurves
from _strong_distance.lib import create_freespace_reachabilitytable \
    as _sd_create_freespace_reachabilitytable

from _strong_distance.lib import setfreespace as _sd_setfreespace
from _strong_distance.lib import setreachabilitytable as \
    _sd_setreachabilitytable

from _strong_distance.lib import getcurve2 as _sd_getcurve2
from _strong_distance.lib import getcurve1 as _sd_getcurve1
from _strong_distance.lib import getcurve1lenght as _sd_getcurve1lenght
from _strong_distance.lib import getcurve2lenght as _sd_getcurve2lenght
from _strong_distance.lib import getfreespace as _sd_getfreespace

from _strong_distance.lib import isreachable as _sd_isreachable

from _weak_distance.lib import createcurves as _wd_createcurves
from _weak_distance.lib import create_freespace_reachabilitytable \
    as _wd_create_freespace_reachabilitytable

from _weak_distance.lib import setfreespace as _wd_setfreespace
from _weak_distance.lib import computemaxdistances as _wd_computemaxdistances

from _weak_distance.lib import getcurve2 as _wd_getcurve2
from _weak_distance.lib import getcurve1 as _wd_getcurve1
from _weak_distance.lib import getcurve1lenght as _wd_getcurve1lenght
from _weak_distance.lib import getcurve2lenght as _wd_getcurve2lenght
from _weak_distance.lib import getfreespace as _wd_getfreespace

from _weak_distance.lib import isreachable as _wd_isreachable

import os
from cffi import FFI
lib = FFI().dlopen("_weak_distance.cpython-39-darwin.so")

## Super class of StrongDistance and WeakDistance.
#
#  Class should not be used as a standalone object. Used in seperate modules
#  to check if StrongDistance and WeakDistance are instances of Distance
class Distance:

    ## Protected - filepath of file containing first curve.
    _curve_1_file: str

    ## Protected - filepath of file containing first curve.
    _curve_2_file: str

    ## Protected - last input of epsilon set to class.
    _epsilon: float

    ## Should be only called by sub classes.
    #  @param self Object pointer.
    #  @param curve_1_file Filepath of curve one.
    #  @param curve_2_file Filepath of curve one.
    def __init__(self, curve_1_file, curve_2_file):
        curve1_abspath = os.path.abspath(curve_1_file)
        curve2_abspath = os.path.abspath(curve_2_file)

        curve1_ascii = curve1_abspath.encode('ascii')
        curve2_ascii = curve2_abspath.encode('ascii')

        self._curve_1_file = curve1_ascii
        self._curve_2_file = curve2_ascii

    ## Formatted string containing curve filepaths and child class name.
    #  @param self Object pointer.
    #  @param name_ Name of sub class.
    #  @return Formatted string.
    def __str__(self, name_):
        try:
            curve_1_file, curve_2_file = self._curve_1_file, self._curve_2_file
        except:
            curve_1_file, curve_2_file = "N/A", "N/A"
        return f"""
                Frechet Distance       |  {name_}
                ========================================
                Curve 1 File           |  {curve_1_file}
                Curve 2 File           |  {curve_2_file}
                """

    ## Protected - raises IOError if sub class's setCurves() fails to read curve file.
    #  @param self Object pointer.
    #  @param errno Error number returned from C program.
    def _checkSetCurvesErrno(self, errno):
        if errno != 0:
            raise IOError(f"{os.strerror(errno)} raised while running setCurves().\n"
                          f"Check file paths and formats for error:\n"
                          f"{self._curve_1_file}\n"
                          f"{self._curve_2_file}"
                           )

    ## Use to get filepaths of curves.
    #  @param self Object pointer.
    #  @returns First curve filepath then second curve filepath.
    def getFileNames(self):
        return self._curve_1_file, self._curve_2_file

    ## Use to get last input of epsilon.
    #  @param self Object pointer.
    #  @returns Epsilon.
    def getEpsilon(self):
        return self._epsilon

## Frechet Distance API
#
#  Class can be used to load curves from files, build free space data structure
#  and check if paths exist in free space.
class StrongDistance(Distance):

    ## Constructs an empty object with no curves
    #  @param self Object pointer.
    def __init__(self):
        _sd_create_freespace_reachabilitytable()

    ## Formatted string containing curve filepaths and child class name.
    #  @param self Object pointer.
    #  @return Formatted string.
    def __str__(self):
        return super().__str__(self.__class__.__name__)

    ## Creates instance that includes two curves from two separate files.
    #  @param cls Class pointer.
    #  @param curve_1_file Filepath of file containing first curve.
    #  @param curve_2_file Filepath of file containing second curve.
    #  @param reverse_curve_2 True if coordinates for second curve need to be reversed.
    #  @return Object pointer.
    @classmethod
    def setCurves(cls, curve_1_file, curve_2_file, reverse_curve_2=False):
        self = cls.__new__(cls)
        super(StrongDistance, self).__init__(curve_1_file, curve_2_file)
        errno = _sd_createcurves(self._curve_1_file, self._curve_2_file, \
                                 reverse_curve_2)
        self._checkSetCurvesErrno(errno)
        self.__init__()
        return self

    ## Use to set free space data structure for epsilon.
    #  @param self Object pointer.
    #  @param epsilon Epsilon.
    def setFreeSpace(self, epsilon):
        self._epsilon = epsilon
        _sd_setfreespace(epsilon)

    ## Use to get coodinates of first curve
    #  @param self Object pointer.
    #  @return Array of coordinates; array of structs containing variables 'x' and 'y.'
    def getCurve1(self):
        return _sd_getcurve1()

    ## Use to get coodinates of second curve
    #  @param self Object pointer.
    #  @return Array of coordinates; array of structs containing variables 'x' and 'y.'
    def getCurve2(self):
        return _sd_getcurve2()

    ## Use to get number of coodinates for first curve
    #  @param self Object pointer.
    #  @return Lenght of array returned by getCurve1().
    def getCurve1Lenght(self):
        return _sd_getcurve1lenght()

    ## Use to get number of coodinates for second curve
    #  @param self Object pointer.
    #  @return Lenght of array returned by getCurve2().
    def getCurve2Lenght(self):
        return _sd_getcurve2lenght()

    ## Use to get free space data struct
    #  @param self Object pointer.
    #  @return Typedef struct freespace.
    def getFreeSpace(self):
        return _sd_getfreespace()

    ## Use to check if path exists inside free space.
    #  @param self Object pointer.
    #  @return True if path exists; False if path is not found.
    def isReachable(self):
        _sd_setreachabilitytable()
        return _sd_isreachable()

## Weak Frechet Distance API
#
#  Class can be used to load curves from files, build free space data structure
#  and check if paths exist in free space.
class WeakDistance(Distance):

    ## Constructs an empty object with no curves
    #  @param self Object pointer.
    def __init__(self):
        _wd_create_freespace_reachabilitytable()

    ## Formatted string containing curve filepaths and child class name.
    #  @param self Object pointer.
    #  @return Formatted string.
    def __str__(self):
        return super().__str__(self.__class__.__name__)

    ## Creates instance that includes two curves from two separate files.
    #  @param cls Class pointer.
    #  @param curve_1_file Filepath of file containing first curve.
    #  @param curve_2_file Filepath of file containing second curve.
    #  @param reverse_curve_2 True if coordinates for second curve need to be reversed.
    #  @return Object pointer.
    @classmethod
    def setCurves(cls, curve_1_file, curve_2_file, reverse_curve_2=False):
        self = cls.__new__(cls)
        super(WeakDistance, self).__init__(curve_1_file, curve_2_file)
        errno = _wd_createcurves(self._curve_1_file, self._curve_2_file, \
                                 reverse_curve_2)
        self._checkSetCurvesErrno(errno)
        self.__init__()
        return self

    ## Use to set free space data structure for epsilon.
    #  @param self Object pointer.
    #  @param epsilon Epsilon.
    def setFreeSpace(self, epsilon):
        self._epsilon = epsilon
        _wd_setfreespace(epsilon)

    ## Use to get coodinates of first curve
    #  @param self Object pointer.
    #  @return Array of coordinates; array of structs containing variables 'x' and 'y.'
    def getCurve1(self):
        return _wd_getcurve1()

    ## Use to get coodinates of second curve
    #  @param self Object pointer.
    #  @return Array of coordinates; array of structs containing variables 'x' and 'y.'
    def getCurve2(self):
        return _wd_getcurve2()

    ## Use to get number of coodinates for first curve
    #  @param self Object pointer.
    #  @return Lenght of array returned by getCurve1().
    def getCurve1Lenght(self):
        return _wd_getcurve1lenght()

    ## Use to get number of coodinates for second curve
    #  @param self Object pointer.
    #  @return Lenght of array returned by getCurve2().
    def getCurve2Lenght(self):
        return _wd_getcurve2lenght()

    ## Use to get free space data struct
    #  @param self Object pointer.
    #  @return Typedef struct freespace.
    def getFreeSpace(self):
        return _wd_getfreespace()

    ## Use to check if path exists inside free space.
    #  @param self Object pointer.
    #  @return True if path exists; False if path is not found.
    def isReachable(self):
        if _wd_getcurve1lenght() == 1 or _wd_getcurve2lenght() == 1:
            try:
                return _wd_computemaxdistances(super()._epsilon)
            except ValueError:
                raise ValueError("No value for Epsilon exists because"
                                 "setfreespace() was never called.")
        else:
            return _wd_isreachable()
