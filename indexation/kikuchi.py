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
from math import tan, sin, pi, asin, sqrt, atan2, atan, cos

# Third party modules.
import rmlimage.plugin.ebsd.Drawing as Drawing


# Local modules.
from EBSDTools.mathTools.mathExtras import zeroPrecision
import EBSDTools.mathTools.vectors as vectors

def kikuchiLineToNormalOld(m, k, patternCenter, detectorDistance):
  #Shift line to a pattern centre at (0,0)
  if m != None:
      k -= -m*patternCenter[0] + patternCenter[1]
  else:
    k -= patternCenter[0]
  
  #Build two vectors (x2-x1 and x1-x0) to calculate the normal
  x0 = vectors.vector(0,0,0)
  
  if m == None:
    x1 = vectors.vector(k, detectorDistance, 0.0)
    x2 = vectors.vector(k, detectorDistance, 0.1)
  elif abs(m) < zeroPrecision:
    x1 = vectors.vector(0.0, detectorDistance, k)
    x2 = vectors.vector(0.1, detectorDistance, k)
  else:
    x1 = vectors.vector(0.0, detectorDistance, k)
    if abs(k) > zeroPrecision:
      x2 = vectors.vector(-k/m, detectorDistance, 0.0)
    else: # abs(k) < zeroPrecision:
      x2 = vectors.vector((1-k)/m, detectorDistance, 1.0)
  
  n = vectors.cross(x2-x1, x1-x0)
  
  return n

def kikuchiLineToNormal(p1, p2, patternCenter, detectorDistance):
  """
  
  """
  x1 = p1[0] - patternCenter[0]; z1 = p1[1] - patternCenter[1]
  x2 = p2[0] - patternCenter[0]; z2 = p2[1] - patternCenter[1]
  
  v1 = vectors(x1,detectorDistance,z1)
  v2 = vectors(x2,detectorDistance,z2)
  
  n = vectors.cross(v1, v2)
  
  print n
  
  

def houghPeakToKikuchiLine(rho, theta, patternSize):
  """
  Return the Kikuchi line from a Hough peak.
  :return: (x1,y1), (x2,y1)
  :rtype: list
  
  .. note:: The origin is located at (width/2, height/2) of the image.
  
  :arg rho: :math:`\\rho`
  :type rho: float
  
  :arg theta: :math:`\\theta`
  :type theta: float
  
  :arg patternSize: (width, height) of the pattern
  :type patternSize: tuple
  """
  javaLine = Drawing.getLine(rho, theta, patternSize[0], patternSize[1])
  return [(javaLine.getX1(), javaLine.getY1()), (javaLine.getX2(), javaLine.getY2())]

def kikuchiLineToHoughPeak(p1, p2, patternSize):
  """
  Return the Hough Peak of a Kikuchi line
  :return: (rho, theta)
  :rtype: tuple
  
  :arg p1: (x1,y1) of the first point
  :type p1: tuple
  
  :arg p2: (x2,y2) of the second point
  :type p2: tuple
  
  :arg patternSize: (width, height) of the pattern
  :type patternSize: tuple
  """
  x1 = p1[0]; y1 = p1[1]
  x2 = p2[0]; y2 = p2[1]
  
#  h = sqrt((x2-x1)**2 + (y2-y1)**2)
#  rho = abs((x2-x1)*(y1-patternSize[1]/2) - (x1-patternSize[0]/2)*(y2-y1))/h
#  
#  u = vectors.vector(x2-x1, y2-y1)
#  v = vectors.vector(y2-y1, -(x2-x1))
#  print u,v
#  
#  if v[1] < 0: v= -v
##  if v[0] < 0: rho = -rho
#  
#  theta = atan2(v[1],v[0])
  
  
  if y1-y2 > 0:
    theta = atan((x2-x1) / (y1-y2))
  else:
    theta = atan((x1-x2) / (y2-y1))

  rho = x1*cos(theta) + y1*sin(theta)
  
  return rho, theta

if __name__ == '__main__':
  pass
    