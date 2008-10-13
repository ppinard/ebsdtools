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
from math import pi

# Third party modules.

# Local modules.

def positiveEulers(theta1, theta2, theta3):
  if theta1 < 0:
    theta1 += 2*pi
  if theta3 < 0:
    theta3 += 2*pi
  
  return theta1, theta2, theta3

def negativeEulers(theta1, theta2, theta3):
  if theta1 > pi:
    theta1 -= 2*pi
  if theta3 > pi:
    theta3 -= 2*pi
  
  return theta1, theta2, theta3