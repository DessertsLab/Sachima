from distutils.core import setup
from Cython.Build import cythonize

setup(name='LAPP',
      ext_modules=cythonize("L.pyx"))

#  python setup.py build_ext --inplace