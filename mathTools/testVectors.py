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
from math import sqrt

# Third party modules.

# Local modules.
import vectors

# Globals and constants variables.

class TestVectors(unittest.TestCase):

  def setUp(self):
    unittest.TestCase.setUp(self)
    
  def tearDown(self):
    unittest.TestCase.tearDown(self)
    
  def testSkeleton(self):
    #self.fail("Test if the TestCase is working.")
    self.assertTrue(True)
  
  def testDotproduct(self):
    #Examples from Wikipedia: Dot Product
    self.assertEqual(vectors.dotproduct((1,3,-5), (4,-2,-1)), 3)
  
  def testCrossproduct(self):
    #Examples from Wikipedia: Cross Product
    self.assertEqual(vectors.crossproduct((1,2,3), (4,5,6)), (-3,6,-3))
    self.assertEqual(vectors.crossproduct((3,0,0), (0,2,0)), (0,0,6))

  def testNorm(self):
    self.assertAlmostEqual(vectors.norm((1,0,0)), 1.0, 3)
    self.assertAlmostEqual(vectors.norm((1,1,0)), sqrt(2), 3)
    self.assertAlmostEqual(vectors.norm((1,1,1)), sqrt(3), 3)
    self.assertAlmostEqual(vectors.norm((1,2,1)), sqrt(6), 3)
    
if __name__ == '__main__':
  unittest.main()