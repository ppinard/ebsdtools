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
from math import pi, tan, sin
import os

# Third party modules.

# Local modules.
import RandomUtilities.DrawingTools.drawing as drawing
from EBSDTools.mathTools.mathExtras import zeroPrecision

def houghPeakToLine(rho, theta, patternSize):
  
  if theta < zeroPrecision:
    m = None
    k = rho
  else:
    m = -1.0/tan(theta)
    k = -rho / sin(theta) / patternSize[0] 
  
  return m, k

def lineToNormal():
  pass

if __name__ == '__main__':
  patternSize = (2680,2040)
  patternCenter = (0.5, 0.5)
  detectorDistance = 0.3
  
  im = drawing.ImageLine(patternSize, origin='center')
  
  peaks = [(-812, 145), (-812,35), (350,130), (350,50)] #5deg
  peaks = [(229,53), (229,127), (-980,154), (-980,26)] #85deg
  peaks = [(-1130,7), (-1130, 173), (33,126), (33,55)] #70deg
  
  for peak in peaks:
    m,k = houghPeakToLine(peak[0], peak[1]/180.0*pi, patternSize)
  
    print m, k
  
  
    im.drawLinearFunction(m=m
                            , k=k)
  
  folder = 'I:/Philippe Pinard/workspace/EBSDTools/indexation/test'
  im().save(os.path.join(folder, 'test.jpg'))