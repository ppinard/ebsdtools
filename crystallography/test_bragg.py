#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Philippe Pinard (philippe.pinard@gmail.com)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2008-2009 Philippe Pinard"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = ""
__svnDate__ = ""
__svnId__ = ""

# Standard library modules.
import unittest
from math import pi

# Third party modules.

# Local modules.
import EBSDTools.crystallography.bragg as bragg
from RandomUtilities.testing.testOthers import almostEqual

# Globals and constants variables.

class TestBragg(unittest.TestCase):

  def setUp(self):
    unittest.TestCase.setUp(self)
    
  def tearDown(self):
    unittest.TestCase.tearDown(self)
    
  def testSkeleton(self):
    #self.fail("Test if the TestCase is working.")
    self.assert_(True)
  
  def testElectronWavelength(self):
    #References: Wikipedia
    self.assert_(almostEqual(bragg.electronWavelength(10e3), 0.12031075249234069))
    self.assert_(almostEqual(bragg.electronWavelength(200e3), 0.020538907051308845))
  
  def testDiffractionAngle(self):
    #References: \url{http://hyperphysics.phy-astr.gsu.edu/hbase/quantum/bragg.html}
    self.assert_(almostEqual(bragg.diffractionAngle(wavelength=0.12*10, planeSpacing=1*10, order=1) / pi * 180, 3.439812767515196))
    self.assert_(almostEqual(bragg.diffractionAngle(wavelength=0.2*10, planeSpacing=5*10, order=1) / pi * 180, 1.1459919983885926))
    self.assert_(almostEqual(bragg.diffractionAngle(wavelength=0.0025*10, planeSpacing=.25*10, order=1) / pi * 180, 0.2864800912409137))

if __name__ == '__main__':
  unittest.main()