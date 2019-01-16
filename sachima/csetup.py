from distutils.core import setup
from Cython.Build import cythonize

# python setup.py build_ext --inplace
setup(name="LAPP", ext_modules=cythonize("L.pyx"))
