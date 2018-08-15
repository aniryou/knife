#!python
#cython: boundscheck=False
#cython: wraparound=False
#cython: cdivision=True

import cython
import numpy as np
cimport numpy as np
np.import_array()  # required in order to use C-API

ctypedef np.float64_t DTYPE_t
ctypedef np.intp_t ITYPE_t

from libc.math cimport sqrt, cos, sin, atan2
cdef DTYPE_t INF = np.inf
cdef DTYPE_t PI = np.pi

@cython.boundscheck(False) # turn off bounds-checking for entire function
@cython.wraparound(False)  # turn off negative index wrapping for entire function
def dist(np.ndarray[DTYPE_t, ndim=2] x1, np.ndarray[DTYPE_t, ndim=2] x2):
    cdef int nrow = x1.shape[0]
    cdef int ncol = x1.shape[1]
    cdef np.ndarray[DTYPE_t, ndim=1] h = np.zeros([nrow], dtype=np.float64)
    cdef DTYPE_t lat1
    cdef DTYPE_t lat2
    cdef DTYPE_t lon1
    cdef DTYPE_t lon2
    cdef DTYPE_t dlat
    cdef DTYPE_t dlon
    cdef DTYPE_t a
    for i in range(nrow):
        lat1 = x1[i,0] * PI / 180.0
        lon1 = x1[i,1] * PI / 180
        lat2 = x2[i,0] * PI / 180
        lon2 = x2[i,1] * PI / 180
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat/2) * sin(dlat/2) + cos(lat1) * cos(lat2) * sin(dlon/2) * sin(dlon/2)
        h[i] = 2.0 * 6371 * atan2(sqrt(a), sqrt(1-a))
    return h