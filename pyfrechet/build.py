# This program builds shares object files that can be called from python
#
# Author: Will Rodman
# wrodman@tulane.edu

from cffi import FFI
import os

strong_distance_ffi = FFI()
weak_distance_ffi = FFI()

distance_cdef = """
    typedef struct point point;

    struct point {
      double x, y;
    };

    typedef struct freespace freespace;

    struct freespace {
      double **vertical_start;
      double **vertical_end;
      double **horizontal_start;
      double **horizontal_end;
    };

    int createcurves(char* curve1filename, char* curve2filename, bool reversecurve2);

    void create_freespace_reachabilitytable();

    void setfreespace(double epsilon);

    freespace getfreespace();

    point* getcurve1();

    point* getcurve2();

    int getcurve1lenght();

    int getcurve2lenght();

    bool isreachable();
"""

strong_distance_cdef = """
    void setreachabilitytable();
"""

weak_distance_cdef = """
    bool computemaxdistances(double epsilon);
"""

strong_distance_ffi.cdef(distance_cdef)
strong_distance_ffi.cdef(strong_distance_cdef)
weak_distance_ffi.cdef(distance_cdef)
weak_distance_ffi.cdef(weak_distance_cdef)

if __name__ == "__main__":
    strong_distance_ffi.compile(verbose = True)
    weak_distance_ffi.compile(verbose = True)
    os.remove("_strong_distance.c")
    os.remove("_strong_distance.o")
    os.remove("strong_distance.o")
    os.remove("_weak_distance.c")
    os.remove("_weak_distance.o")
    os.remove("weak_distance.o")
