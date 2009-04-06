#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Philippe Pinard (philippe.pinard@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2008-2009 Philippe Pinard"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = ""
__svnDate__ = ""
__svnId__ = ""

# Standard library modules.
from math import cos, sqrt

# Third party modules.

# Local modules.
import EBSDTools.mathTools.vectors as vectors
from EBSDTools.mathTools.mathExtras import _acos

def cartesianToReciprocal(a, b, c):
  """
  Convert cartesian basis :math:`(a, b, c)` to reciprocal basis :math:`(a^*, b^*, c^*)`
    
  :arg a, b, c: vectors forming a basis in real (cartesian) space
  :type a, b, c: :class:`vector <EBSDTools.mathTools.vectors.vector>`
  
  :rtype: a tuple containing three :class:`vector <EBSDTools.mathTools.vectors.vector>`
  """
  
  volume = vectors.dot(vectors.cross(a, b), c)
  
  a_ = vectors.cross(b, c) / volume
  b_ = vectors.cross(c, a) / volume
  c_ = vectors.cross(a, b) / volume
  
  return (a_, b_, c_)

def reciprocalToCartesion(a_, b_, c_):
  """
  Convert reciprocal basis :math:`(a^*, b^*, c^*)` to cartesian basis :math:`(a, b, c)`
  
  :arg a\_, b\_, c\_: vectors forming a basis in reciprocal space
  :type a, b, c: :class:`vector <EBSDTools.mathTools.vectors.vector>`
  
  :rtype: a tuple containing three :class:`vector <EBSDTools.mathTools.vectors.vector>`
  """
  return cartesianToReciprocal(a_, b_, c_)

def planeSpacing(plane, L):
  """
  Return the plane spacing of a *plane* in lattice *L*
  
  :arg plane: a plane (hkl)
  :type plane: :class:`vector <EBSDTools.mathTools.vectors.vector>`
  
  :arg L: a lattice
  :type L: :class:`Lattice <EBSDTools.crystallography.lattice.Lattice>`
      
  :rtype: float
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
  Return the interplanar angle between *plane1* and *plane2* in lattice *L*.
  
  :arg plane1: a plane (hkl)
  :type plane1: :class:`vector <EBSDTools.mathTools.vectors.vector>`
  
  :arg plane2: a plane (hkl)
  :type plane2: :class:`vector <EBSDTools.mathTools.vectors.vector>`
  
  :arg L: a lattice
  :type L: :class:`Lattice <EBSDTools.crystallography.lattice.Lattice>`
      
  :rtype: float
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

def MillerToBravaisMiller(plane):
  """
  Convert Miller indices to Bravais-Miller indices 
  
  :arg plane: a plane (hkl)
  :type plane: :class:`vector <EBSDTools.mathTools.vectors.vector>`
  
  :rtype: :class:`vector <EBSDTools.mathTools.vectors.vector>`
  """
  assert len(plane) == 3
  
  return vectors.vector((2*plane[0] - plane[1])/3.0
                        , (2*plane[1] - plane[0])/3.0
                        , -(plane[0] + plane[1])
                        , plane[2])
  

def BravaisMillerToMiller(plane):
  """
  Convert Bravais-Miller indices to Miller indices 
  
  :arg plane: a plane (hkl)
  :type plane: :class:`vector <EBSDTools.mathTools.vectors.vector>`
  
  :rtype: :class:`vector <EBSDTools.mathTools.vectors.vector>`
  """
  assert len(plane) == 4
  
  return vectors.vector(plane[0] - plane[2]
                        , plane[1] - plane[2]
                        , plane[3])
  

if __name__ == '__main__':
  pass
