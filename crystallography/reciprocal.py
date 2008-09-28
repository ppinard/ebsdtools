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
import mathTools.vectors as vectors

def cartesianToReciprocal(a, b, c):
  """
    Convert cartesian basis $(a, b, c)$ to reciprocal basis $(a^\ast, b^\ast, c^\ast)$
    
    Inputs:
      a, b, c: vectors
    
    Outputs:
      a tuple containing $(a^\ast, b^\ast, c^\ast)$
  """
  
  volume = vectors.dot(vectors.cross(a, b), c)
  
  a_ = vectors.cross(b, c) / volume
  b_ = vectors.cross(c, a) / volume
  c_ = vectors.cross(a, b) / volume
  
  return (a_, b_, c_)

def reciprocalToCartesion(a_, b_, c_):
  """
    Convert reciprocal basis $(a^\ast, b^\ast, c^\ast)$ to cartesian basis $(a, b, c)$
    
    Inputs:
      a_, b_, c_: vectors
    
    Outputs:
      a tuple containing $(a, b, c)$
  """
  return cartesianToReciprocal(a_, b_, c_)


def _cubic(h, k, l, a):
  d2 = (h**2 + k**2 + l**2) / a**2
  
  return sqrt(1.0/d2)
  
if __name__ == '__main__':
  c = vectors.vector(0.5,0.5,0)
  b = vectors.vector(0.5,0  ,0.5)
  a = vectors.vector(0  ,0.5,0.5)
#  a = vectors.vector(1,0,0)
#  b = vectors.vector(0,1,0)
#  c = vectors.vector(0,0,1)
  
  alpha = vectors.angle(b, c)
  beta = vectors.angle(a, c)
  gamma = vectors.angle(a, b)
  
  print alpha, beta, gamma
  
  a_, b_, c_ = cartesianToReciprocal(a, b, c)
  print a_, b_, c_
  
  alpha_ = vectors.angle(b_, c_)
  beta_ = vectors.angle(a_, c_)
  gamma_ = vectors.angle(a_, b_)
  
  print alpha_, beta_, gamma_
  
  h = 1
  k = 0
  l = 0
  
  r_ = h**2 * (a_.norm())**2 + \
       k**2 * (b_.norm())**2 + \
       l**2 * (c_.norm())**2 + \
       2 * h * k * a_.norm() * b_.norm() * cos(gamma_) + \
       2 * h * l * a_.norm() * c_.norm() * cos(beta_) + \
       2 * k * l * b_.norm() * c_.norm() * cos(alpha_)
  
  print _cubic(h, k, l, 1)
  print 1.0/sqrt(r_)
  
  