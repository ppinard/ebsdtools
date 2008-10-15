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
import EBSDTools.mathTools.vectors as vectors

# Globals and constants variables.

class TestVectors(unittest.TestCase):

  def setUp(self):
    unittest.TestCase.setUp(self)
    
  def tearDown(self):
    unittest.TestCase.tearDown(self)
    
  def testSkeleton(self):
    #self.fail("Test if the TestCase is working.")
    self.assertTrue(True)
  

    
if __name__ == '__main__':
  unittest.main()