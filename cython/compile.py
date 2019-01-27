from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [
    Extension("func_01", ["func_01.py"])
    # Extension("mymodule2", ["mymodule2.py"])
]

setup(name='My Program Name',
      cmdclass={'build_ext': build_ext},
      ext_modules=ext_modules
)
