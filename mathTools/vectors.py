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
from math import sqrt

# Third party modules.

# Local modules.

def dotproduct(v1, v2):
  """
    Return the dot product between 3D vector $\vec{v1}$ and $\vec{v2}$
    
    Equations:
      $=\vec{v1} \bullet \vec{v2}$
  """
  
  return v1[0]*v2[0] + v1[1]*v2[1] + v1[2]*v2[2]

def crossproduct(v1, v2):
  """
    Return the cross product between 3D vector $\vec{v1}$ and $\vec{v2}$
    
    Equations:
      $=\vec{v1} \times \vec{v2}$
  """
  
  return (v1[1]*v2[2] - v1[2]*v2[1],
          v1[2]*v2[0] - v1[0]*v2[2],
          v1[0]*v2[1] - v1[1]*v2[0])

def norm(v):
  """
    Return the norm (length) of a vector
    
    Equations:
      $|\vec{v}| = \sqrt{v_x^2 + v_y^2 + v_z^2}
  """
  
  return sqrt(v[0]**2 + v[1]**2 + v[2]**2)
