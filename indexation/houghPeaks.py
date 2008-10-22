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
from math import tan, sin, pi
import csv

# Third party modules.

# Local modules.
from EBSDTools.mathTools.mathExtras import zeroPrecision

def houghPeakToKikuchiLine(rho, theta, patternSize):
  if theta < zeroPrecision:
    m = None
    k = rho
  else:
    m = -1.0/tan(theta)
    k = -rho / sin(theta) / patternSize[0] 
  
  return m, k

class rmlImage:
  def __init__(self, peaksListFile):
    reader = csv.reader(open(peaksListFile, 'r'))
    self.peaks = list(reader)[2:]
    
  def getPeaksList(self):
    peaksList = []
    
    for peak in self.peaks:
      peaksList.append({'rho': float(peak[0]), 'theta': float(peak[1])/180.0 * pi})
    
    return peaksList
  

if __name__ == '__main__':
  peaks = rmlImage('I:/Philippe Pinard/workspace/EBSDTools/patternSimulations/rotation/theta_000.csv')
  print peaks.getPeaksList()