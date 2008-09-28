#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Philippe Pinard (philippe.pinard@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2008 Philippe Pinard"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = ""
__svnDate__ = ""
__svnId__ = ""

# Standard library modules.
from math import sin, cos, pi, acos, atan2, exp, sqrt

# Third party modules.

# Local modules.
import mathTools.vectors

def primitiveToReciprocal(a, b, c):
  volume = mathTools.vectors.dotproduct(mathTools.vectors.crossproduct(a, b), c)
  
  a_ = mathTools.vectors.crossproduct(b, c) / volume
  b_ = mathTools.vectors.crossproduct(c, a) / volume
  c_ = mathTools.vectors.crossproduct(a, b) / volume
  
  return (a_, b_, c_)

if __name__ == '__main__':
  print primitiveToReciprocal((0.5,0.5,0), (0.5,0,0.5), (0,0.5,0.5))
  