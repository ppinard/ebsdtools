#!/usr/bin/env jython
""" """

# Script information for the file.
__author__ = "Philippe Pinard (philippe.pinard@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2009 Philippe Pinard"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = ""
__svnDate__ = ""
__svnId__ = ""

# Standard library modules.
import platform
from math import tan, sin, pi, asin, sqrt, atan2, atan, cos

# Third party modules.
if platform.system() == 'Java': import rmlimage.plugin.ebsd.Drawing as Drawing

# Local modules.
from EBSDTools.mathTools.mathExtras import zeroPrecision
import EBSDTools.mathTools.vectors as vectors

def kikuchiLineToNormal(p1, p2, patternCenter, detectorDistance, patternSize):
  """
  Return the normal of a Kikuchi line. 
  
  .. note:: The normal is always pointing in the positive :math:`z`
  
  :arg p1: one point of the Kikuchi line :math:`(x,z)` in pixels
  :type p1: tuple
  
  :arg p2: another point of the Kikuchi line :math:`(x,z)` in pixels
  :type p2: tuple
  
  :arg patternCenter: location of the pattern center :math:`(x,z)` in pixels
  :type patternCenter: tuple
  
  :arg detectorDistance: distance between the sample and the detector in :math:`y` in pixels
  :type detectorDistance: float
  
  :arg patternSize: dimensions of the pattern (width, height) in pixels
  :type patternSize: tuple
  
  :return: normal vector
  :rtype: :class:`vector <EBSDTools.mathTools.vectors.vector>`
  """
  x1 = p1[0] - patternCenter[0] - patternSize[0]/2; z1 = p1[1] - patternCenter[1] - patternSize[1]/2
  x2 = p2[0] - patternCenter[0] - patternSize[0]/2; z2 = p2[1] - patternCenter[1] - patternSize[1]/2
  
  v1 = vectors.vector(x1,detectorDistance,z1)
  v2 = vectors.vector(x2,detectorDistance,z2)
  
  n = vectors.cross(v1, v2)
  
  n = n.normalize()
  
  #Adjust that the normal always have a position z
#  if n[2] < 0: n = -n
  
  return n

def houghPeakToKikuchiLine(rho, theta, patternSize):
  """
  Return the Kikuchi line from a Hough peak.
  :return: (x1,y1), (x2,y2)
  :rtype: list
  
  :arg rho: :math:`\\rho` (in pixels) where :math:`-\\rho_{\\text{max}} \leq \\rho < \\rho_{\\text{max}}` 
    and :math:`\\rho_{\\text{max}} = \\sqrt{\\left(\\frac{\\text{width}}{2}\\right)^2 + \\left(\\frac{\\text{height}}{2}\\right)^2}`
  :type rho: float
  
  :arg theta: :math:`\\theta` (in radians) where :math:`0 \\leq \\theta < \\pi`
  :type theta: float
  
  :arg patternSize: dimensions of the pattern (width, height) in pixels
  :type patternSize: tuple
  """
  javaLine = Drawing.getLine(rho, theta, patternSize[0], patternSize[1])
  return [(javaLine.getX1(), javaLine.getY1()), (javaLine.getX2(), javaLine.getY2())]


if __name__ == '__main__':
  pass
    