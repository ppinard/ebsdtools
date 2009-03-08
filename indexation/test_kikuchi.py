#!/usr/bin/env jython
""" """

# Script information for the file.
__author__ = "Philippe Pinard (philippe.pinard@gmail.com)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2009 Philippe Pinard"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = ""
__svnDate__ = ""
__svnId__ = ""

# Standard library modules.
import os
import unittest
from math import pi

# Third party modules.

# Local modules.
import EBSDTools.indexation.kikuchi as kikuchi
from EBSDTools.mathTools.mathExtras import zeroPrecision

# Globals and constants variables.

class TestKikuchi(unittest.TestCase):

  def setUp(self):
    unittest.TestCase.setUp(self)
    
  def tearDown(self):
    unittest.TestCase.tearDown(self)
    
  def testSkeleton(self):
    #self.fail("Test if the TestCase is working.")
    self.assert_(True)
  
  def testHoughPeakKikuchiLine(self):
    patternSizes = range(100,1000,50) #Different pattern sizes
    patternSizes = [101]
    thetas = range(1,36) #From 0 to 180deg
    
    for patternSize in patternSizes:
      for rho in [50,-50]: #range(-patternSize/2,patternSize/2,10): #Rho from -patternSize/2 to +patternSize/2
        for theta in thetas:
          p1, p2 = kikuchi.houghPeakToKikuchiLine(rho, theta*5*pi/180.0, (patternSize, patternSize))
          print p1,p2, rho, theta*5
          r, angle = kikuchi.kikuchiLineToHoughPeak(p1,p2, (patternSize, patternSize))
          
          print r, rho
          print angle/pi*180.0, theta*5
#          self.assert_(abs(r - rho) < zeroPrecision)
          self.assert_(abs(angle - theta*5*pi/180.0) < zeroPrecision)

if __name__ == '__main__':
  unittest.main()
