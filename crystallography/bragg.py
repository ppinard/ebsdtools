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
from math import sqrt, asin

# Third party modules.

# Local modules.
from EBSDTools.mathTools.mathExtras import h, m_e, e, c

def electronWavelength(energy):
  """
    Return the relativistic electron wavelength
    
    Inputs:
      energy: Energy in eV
    
    Outputs:
      wavelength in $\AA$
  """
  a = h / sqrt(2*m_e*e)
  b = 2*e / (m_e * c**2)
  
  return a / sqrt(energy + b * energy**2) * 1e10

def diffractionAngle(planeSpacing, wavelength, order=1):
  """
    Return the diffraction angle based on Bragg's Law ($n\lambda = 2d\sin\theta$)
    
    Inputs:
      planeSpacing: d (in $\AA$)
      wavelength: $\lambda$ (in $\AA$)
      order: n (integer)
    
    Outputs:
      $\theta$ in radians
  """
  return asin(order*wavelength / (2*planeSpacing))
  