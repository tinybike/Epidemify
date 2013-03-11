#!/usr/bin/env python
"""
Setup file for Cython compilation.

(c) Jack Peterson (jack@tinybike.net), 3/10/2013
"""

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import os

# Pass filename (without .py extension) as commandline argument
filename = raw_input('Python file: ')

# Copy .py file to .pyx file
bash_copy = 'cp %s.py %s.pyx' % (filename, filename)
os.system(bash_copy)

ext_modules = [Extension(filename, [filename + '.pyx'])]

setup(
	name = filename + '_so',
	cmdclass = {'build_ext': build_ext},
	ext_modules = ext_modules
)
