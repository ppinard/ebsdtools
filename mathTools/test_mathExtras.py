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
from math import pi, acos

# Third party modules.

# Local modules.
import EBSDTools.mathTools.mathExtras as mathExtras

class TestEulers(unittest.TestCase):

  def setUp(self):
    unittest.TestCase.setUp(self)
    
  def tearDown(self):
    unittest.TestCase.tearDown(self)
    
  def testSkeleton(self):
    #self.fail("Test if the TestCase is working.")
    self.assertTrue(True)
  
  def testConstants(self):
    self.assertAlmostEqual(mathExtras.h, 6.62606809633e-34)
    self.assertAlmostEqual(mathExtras.m_e, 9.1093818e-31)
    self.assertAlmostEqual(mathExtras.e, 1.60217646e-19)
    self.assertAlmostEqual(mathExtras.c, 2.99792458e8)
    
    self.assertAlmostEqual(mathExtras.zeroPrecision, 1e-5)
  
  def test_acos(self):
    self.assertEqual(mathExtras._acos(4), 0)
    self.assertEqual(mathExtras._acos(-4), pi)
    self.assertAlmostEqual(mathExtras._acos(0.5), 60/180.0*pi)
    self.assertAlmostEqual(mathExtras._acos(0.45675), acos(0.45675))

if __name__ == '__main__':
  unittest.main()