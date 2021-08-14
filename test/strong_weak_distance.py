# Author: Will Rodman
# wrodman@tulane.edu
#
# Command line to run program:
# python3 strong_weak_distance.py

import sys, unittest
sys.path.insert(0, "../src")

from _frechet._strong_distance.lib import createcurves as _sd_createcurves
from _frechet._strong_distance.lib import create_freespace_reachabilitytable as \
    _sd_create_freespace_reachabilitytable
from _frechet._strong_distance.lib import setfreespace as _sd_setfreespace
from _frechet._strong_distance.lib import setreachabilitytable as \
    _sd_setreachabilitytable
from _frechet._strong_distance.lib import isreachable as _sd_isreachable

from _frechet._weak_distance.lib import createcurves as _wd_createcurves
from _frechet._weak_distance.lib import create_freespace_reachabilitytable as \
    _wd_create_freespace_reachabilitytable
from _frechet._weak_distance.lib import setfreespace as _wd_setfreespace
from _frechet._weak_distance.lib import isreachable as _wd_isreachable
from _frechet._weak_distance.lib import computemaxdistances as \
    _wd_computemaxdistances

TEST_DATA = "sp500"

if TEST_DATA == "sp500":
    REACHABLE_EPSILON = 5
    UNREACHABLE_EPSILON = 1
    REVERSE_CURVE = False
elif TEST_DATA == "trajectory":
    REACHABLE_EPSILON = 70
    UNREACHABLE_EPSILON = 60
    REVERSE_CURVE = True

CURVE_1 = f"{TEST_DATA}_data/sample_1.txt".encode('ascii')
CURVE_2 = f"{TEST_DATA}_data/sample_2.txt".encode('ascii')

class strong_weak_distance(unittest.TestCase):

    global REACHABLE_EPSILON
    global UNREACHABLE_EPSILON
    global REVERSE_CURVE

    global CURVE_1
    global CURVE_2

    def setUp(self):
        print(self._testMethodName)

    def test_strong_distance_create_memory(self):
        errno = _sd_createcurves(CURVE_1, CURVE_2, REVERSE_CURVE)
        self.assertEqual(0, errno, "_sd_createcurves() raised and error")

        _sd_create_freespace_reachabilitytable()

    def test_strong_distance_unrechable_epsilon(self):
        _sd_setfreespace(UNREACHABLE_EPSILON);
        _sd_setreachabilitytable();
        bool_ = _sd_isreachable()
        self.assertFalse(bool_, f"Eplison {UNREACHABLE_EPSILON} was reachable")

    def test_strong_distance_rechable_epsilon(self):
        _sd_setfreespace(REACHABLE_EPSILON);
        _sd_setreachabilitytable();
        bool_ = _sd_isreachable()
        self.assertTrue(bool_, f"Eplison {REACHABLE_EPSILON} was unreachable")

    def test_weak_distance_create_memory(self):
        errno = _wd_createcurves(CURVE_1, CURVE_2, REVERSE_CURVE)
        self.assertEqual(0, errno, "_wd_createcurves() raised and error")

        _wd_create_freespace_reachabilitytable()

    def test_weak_distance_unrechable_epsilon(self):
        _wd_setfreespace(UNREACHABLE_EPSILON);
        bool_ = _wd_isreachable()
        self.assertFalse(bool_, f"Eplison {UNREACHABLE_EPSILON} was reachable")

    def test_weak_distance_rechable_epsilon(self):
        _wd_setfreespace(REACHABLE_EPSILON);
        bool_ = _wd_isreachable()
        self.assertTrue(bool_, f"Eplison {REACHABLE_EPSILON} was unreachable")

if __name__ == '__main__':
    unittest.main()
