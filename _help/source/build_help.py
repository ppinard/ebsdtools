#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Philippe Pinard (philippe.pinard@gmail.com)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2009 Philippe Pinard"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = ""
__svnDate__ = ""
__svnId__ = ""

# Standard library modules.
import os

# Third party modules.

# Local modules.
import EBSDTools

command = 'sphinx-build -b html'
command += r' -D pngmath="c:\program files\miktex 2.7\miktex\bin\latex.exe"'
command += r' -D pngmath_latex_preamble="\usepackage{math}"'
command += ' ' + os.path.join(EBSDTools.__path__[0], 'help/source')
command += ' ' + os.path.join(EBSDTools.__path__[0], 'help/build/html') 

print command

os.system(command)