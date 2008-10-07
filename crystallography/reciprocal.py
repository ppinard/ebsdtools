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

def _acos(angle):
  if angle >= 1.0:
    return 0
  elif angle <= -1.0:
    return pi
  else:
    return acos(angle)

class lattice:
  def __init__(self, a, b, c, alpha, beta, gamma):
    """
      
      Inputs:
        a, b, c: lattice parameter
        alpha, beta, gamma: lattice angle in rad
    """
    
    self.a = float(a)
    self.b = float(b)
    self.c =  float(c)
    self.alpha =  float(alpha)
    self.beta =  float(beta)
    self.gamma =  float(gamma)
    
    self.__calculateReciprocalAngle()
    self.__calculateLatticeVolume()
    self.__calculateReciprocalBasis()
    self.__calculateReciprocalVolume()
  
  def __calculateReciprocalAngle(self):
    self.alpha_ = acos((cos(self.beta)*cos(self.gamma) - cos(self.alpha)) / (sin(self.beta)*sin(self.gamma)))
    self.beta_ = acos((cos(self.alpha)*cos(self.gamma) - cos(self.beta)) / (sin(self.alpha)*sin(self.gamma)))
    self.gamma_ = acos((cos(self.alpha)*cos(self.beta) - cos(self.gamma)) / (sin(self.alpha)*sin(self.beta)))
  
  def __calculateLatticeVolume(self):
    self.volume = self.a*self.b*self.c*sin(self.alpha_)*sin(self.beta)*sin(self.gamma)
  
  def __calculateReciprocalBasis(self):
    self.a_ = self.b*self.c*sin(self.alpha) / self.volume
    self.b_ = self.a*self.c*sin(self.beta) / self.volume
    self.c_ = self.a*self.b*sin(self.gamma) / self.volume
  
  def __calculateReciprocalVolume(self):
    self.volume_ = 1.0 / self.volume
    
  def __call__(self):
    return {'a': self.a
            , 'b': self.b
            , 'c': self.c
            , 'a*': self.a_
            , 'b*': self.b_
            , 'c*': self.c_
            , 'alpha': self.alpha
            , 'beta': self.beta
            , 'gamma': self.gamma
            , 'alpha*': self.alpha_
            , 'beta*': self.beta_
            , 'gamma*': self.gamma_
            , 'V': self.volume
            , 'V*': self.volume_
            }
  
def cartesianToReciprocal(a, b, c):
  """
    Convert cartesian basis $(a, b, c)$ to reciprocal basis $(a^\ast, b^\ast, c^\ast)$
    
    Inputs:
      a, b, c: vectors
    
    Outputs:
      a tuple containing $(a^\ast, b^\ast, c^\ast)$
  """
  
  volume = vectors.dot(vectors.cross(a, b), c)
  print volume
  
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

def planeSpacing(plane, L):
  """
    Calculate the plane spacing
    
    Inputs:
      plane: a vector representing (hkl). h, k and l must be integer
      L: class lattice
      
    Outputs:
      float of the plane spacing in units of the lattice parameters
  """
  h = float(plane[0])
  k = float(plane[1])
  l = float(plane[2])
  
  r_2 = h**2 * L.a_**2 + \
       k**2 * L.b_**2 + \
       l**2 * L.c_**2 + \
       2 * h * k * L.a_ * L.b_ * cos(L.gamma_) + \
       2 * h * l * L.a_ * L.c_ * cos(L.beta_) + \
       2 * k * l * L.b_ * L.c_ * cos(L.alpha_)
  
  return 1.0/sqrt(r_2)

def interplanarAngle(plane1, plane2, L):
  """
    Calculate the interplanar spacing
    
    Inputs:
      plane1: a vector representing (hkl). h, k and l must be integer
      plane2: same as plane1
      L: class lattice
      
    Outputs:
      float of the angle in rad between plane1 and plane2
  """
  h1 = float(plane1[0]) 
  k1 = float(plane1[1])
  l1 = float(plane1[2])
  h2 = float(plane2[0])
  k2 = float(plane2[1])
  l2 = float(plane2[2])
  
  r_1r_2 = h1*h2*L.a_**2 + k1*k2*L.b_**2 + l1*l2*L.c_**2 + \
           (h1*k2 + h2*k1)*L.a_*L.b_*cos(L.gamma_) + \
           (h1*l2 + h2*l1)*L.a_*L.c_*cos(L.beta_) + \
           (k1*l2 + k2*l1)*L.b_*L.c_*cos(L.alpha_)
           
  r_1 = 1.0 / planeSpacing(plane1, L)
  r_2 = 1.0 / planeSpacing(plane2, L)
  
  costheta = r_1r_2 / (r_1 * r_2)
  
  return _acos(costheta)

if __name__ == '__main__':
  h = 1
  k = 0
  l = 0
  
  L = lattice(a=1, b=1, c=2, alpha=pi/2, beta=pi/2, gamma=120/180.0*pi)
  
  print planeSpacing([h,k,l], L)
  print interplanarAngle([h,k,l], [1,1,0], L) / pi * 180
  
  print L
#  r_ = h**2 * (a_.norm())**2 + \
#       k**2 * (b_.norm())**2 + \
#       l**2 * (c_.norm())**2 + \
#       2 * h * k * a_.norm() * b_.norm() * cos(gamma_) + \
#       2 * h * l * a_.norm() * c_.norm() * cos(beta_) + \
#       2 * k * l * b_.norm() * c_.norm() * cos(alpha_)
  
#  print _cubic(h, k, l, 1)
#  print hexagonal(h, k, l, 1, 2.0)
#  print 1.0/sqrt(r_)
#  
  