#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Philippe Pinard (philippe.pinard@gmail.com)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2008 Philippe Pinard"
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
import EBSDTools.mathTools.eulers as eulers

# Globals and constants variables.

class TestQuaternions(unittest.TestCase):

  def setUp(self):
    unittest.TestCase.setUp(self)
    
  def tearDown(self):
    unittest.TestCase.tearDown(self)
    
  def testSkeleton(self):
    #self.fail("Test if the TestCase is working.")
    self.assertTrue(True)
  
  def testPositiveEulers(self):
    self.assertEqual(eulers.positiveEulers(0,0,0), (0,0,0))
    self.assertEqual(eulers.positiveEulers(pi, 0, pi), (pi,0,pi))
    self.assertEqual(eulers.positiveEulers(-pi/2.0, 0, -pi), (3.0*pi/2.0, 0, pi))
  
  def testNegativeEulers(self):
    self.assertEqual(eulers.negativeEulers(0,0,0), (0,0,0))
    self.assertEqual(eulers.negativeEulers(pi, 0, pi), (pi,0,pi))
    self.assertEqual(eulers.negativeEulers(3.0*pi/2.0, 0, pi), (-pi/2.0, 0, pi))
  
if __name__ == '__main__':
  unittest.main()