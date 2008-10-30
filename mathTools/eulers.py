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
from math import pi

# Third party modules.

# Local modules.

def positiveEulers(*thetas):
  """
    Convert eulers from 
      -pi < theta0 < pi
      0 < theta1 < pi
      -pi < theta2 < pi
    to
      0 < theta0 < 2pi
      0 < theta1 < pi
      0 < theta2 < 2pi
  """
  if len(thetas) == 1:
    theta0 = thetas[0][0]
    theta1 = thetas[0][1]
    theta2 = thetas[0][2]
  elif len(thetas) == 3:
    theta0 = thetas[0]
    theta1 = thetas[1]
    theta2 = thetas[2]
  
  if theta0 < 0:
    theta0 += 2*pi
  if theta2 < 0:
    theta2 += 2*pi
  
  return theta0, theta1, theta2

def negativeEulers(theta0, theta1, theta2):
  """
    Convert eulers from
      0 < theta0 < 2pi
      0 < theta1 < pi
      0 < theta2 < 2pi
    to
      -pi < theta0 < pi
      0 < theta1 < pi
      -pi < theta2 < pi
  """
  if theta0 > pi:
    theta0 -= 2*pi
  if theta2 > pi:
    theta2 -= 2*pi
  
  return theta0, theta1, theta2

def degEulers(*thetas):
  """
    Convert from rad to deg
  """
  if len(thetas) == 1:
    theta0 = thetas[0][0]
    theta1 = thetas[0][1]
    theta2 = thetas[0][2]
  elif len(thetas) == 3:
    theta0 = thetas[0]
    theta1 = thetas[1]
    theta2 = thetas[2]
    
  theta0 *= 180.0 / pi
  theta1 *= 180.0 / pi
  theta2 *= 180.0 / pi
  
  return theta0, theta1, theta2