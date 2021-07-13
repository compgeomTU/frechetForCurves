# This program builds shares object files that can be called from python
#
# Author: Will Rodman
# wrodman@tulane.edu

from cffi import FFI
import shutil

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

    point* gethorizontalcurve();

    point* getverticalcurve();

    int gethorizontaledges();

    int getverticaledges();

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

strong_distance_ffi.set_source("_frechet._strong_distance",
                    """
                    #include "../../frechet/distance.h"
                    #include "../../frechet/strong_distance.h"
                    """,
                    sources = ["../frechet/strong_distance.c"],
                    libraries = ["m"])

weak_distance_ffi.set_source("_frechet._weak_distance",
                    """
                    #include "../../frechet/distance.h"
                    #include "../../frechet/weak_distance.h"
                    """,
                    sources = ["../frechet/weak_distance.c"],
                    libraries = ["m"])

if __name__ == "__main__":
    weak_distance_ffi.compile(verbose = True)
    strong_distance_ffi.compile(verbose = True)
    shutil.move("./_frechet", "../pyfrechet/_frechet")
