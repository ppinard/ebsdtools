#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Philippe Pinard (philippe.pinard@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2008 Philippe Pinard"
__license__ = ""
__reference__ = "Altmann (1986) Rotation, Quaternions and Double Groups"

# Subversion informations for the file.
__svnRevision__ = ""
__svnDate__ = ""
__svnId__ = ""

# Standard library modules.
from math import acos

# Third party modules.

# Local modules.

def _acos(angle):
  if angle >= 1.0:
    return 0
  elif angle <= -1.0:
    return pi
  else:
    return acos(angle)

"""
  Physics constants
  References: Wikipedia
"""
h = 6.62606809633e-34
m_e = 9.1093818e-31
e = 1.60217646e-19
c = 2.99792458e8


if __name__ == '__main__':
  print h