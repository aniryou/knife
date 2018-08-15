import os
import numpy
from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

libraries = []
if os.name == 'posix':
    libraries.append('m')

extensions = [
    Extension("distance_fast", ["distance_fast.pyx"],
        include_dirs = [numpy.get_include()],
        libraries=libraries),
]

setup(
    ext_modules = cythonize(extensions)
)