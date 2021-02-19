from distutils.core import setup
from distutils.extension import Extension
import sysconfig
import sys

# CFLAGS="$(root-config --cflags)" LDFLAGS="$(root-config --libs)" python setup.py build_ext --inplace

# Trick from https://gist.github.com/ctokheim/6c34dc1d672afca0676a
# to allow compilation directly from cpp file
if '--use-cython' in sys.argv:
    USE_CYTHON = True
    sys.argv.remove('--use-cython')
else:
    USE_CYTHON = False
ext = '.pyx' if USE_CYTHON else '.cpp'

sourcefiles  = ["histUtils" + ext]

extensions=[Extension('histUtils',
            sourcefiles,
            language='c++',
            extra_compile_args=sysconfig.get_config_var('CFLAGS').split(),
            extra_link_args= sysconfig.get_config_var('LDFLAGS').split(),
            )]

if USE_CYTHON:
    from Cython.Build import cythonize
    extensions = cythonize(extensions)

setup(
  ext_modules=extensions
)
