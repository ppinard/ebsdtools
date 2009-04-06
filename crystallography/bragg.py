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
from math import sqrt, asin

# Third party modules.

# Local modules.
from EBSDTools.mathTools.mathExtras import h, m_e, e, c

def electronWavelength(energy):
  """
  Return the relativistic electron wavelength
    
  :arg energy: Energy in :math:`eV`
  :type energy: float
  
  :return: wavelength in :math:`\\angstrom`
  :rtype: float
  """
  a = h / sqrt(2*m_e*e)
  b = 2*e / (m_e * c**2)
  
  return a / sqrt(energy + b * energy**2) * 1e10

def diffractionAngle(planeSpacing, wavelength, order=1):
  """
  Return the diffraction angle based on Bragg's Law (:math:`n\lambda = 2d\\sin \\theta`)
    
  :arg planeSpacing: d in angstroms
  :type planeSpacing: float
  
  :arg wavelength: :math:`\\lambda` in angstroms
  :type wavelength: float
  
  :arg order: n 
  :type order: integer
    
  :return: :math:`\\theta` in radians
  :rtype: float
  """
  return asin(order*wavelength / (2*planeSpacing))
  