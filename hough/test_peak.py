#!/usr/bin/env python
"""
================================================================================
:mod:`test_peak` -- Unit tests for the module :mod:`peak`.
================================================================================

.. module:: test_peak
.. moduleauthor:: Philippe Pinard <philippe.pinard@mail.mcgill.ca>

"""

# Script information for the file.
__author__ = "Philippe Pinard <philippe.pinard@mail.mcgill.ca>"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2009 Philippe Pinard"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = ""
__svnDate__ = ""
__svnId__ = ""

# Standard library modules.
import unittest
import logging

# Third party modules.

# Local modules.
import ebsdtools.hough.peak as peak

# Globals and constants variables.

class TestPeak(unittest.TestCase):

  def setUp(self):
    unittest.TestCase.setUp(self)

    self.peak1 = peak.Peak(3, 0.5)
    self.peak2 = peak.Peak(5, 0.1)

    self.peak3 = peak.Peak(3, 0.5)
    self.peak3.setdefault(peak.OBJECT_ID, 1)

  def tearDown(self):
    unittest.TestCase.tearDown(self)

  def testSkeleton(self):
    #self.fail("Test if the TestCase is working.")
    self.assert_(True)

  def testconstructor(self):
    self.assertEqual(self.peak1.rho, 3)
    self.assertEqual(self.peak1.theta, 0.5)

    self.assertEqual(self.peak2.rho, 5)
    self.assertEqual(self.peak2.theta, 0.1)

  def test__repr__(self):
    self.assertEqual(str(self.peak1), "(3.000000, 0.500000)")
    self.assertEqual(str(self.peak2), "(5.000000, 0.100000)")
    self.assertEqual(str(self.peak3), "(3.000000, 0.500000)")

  def test__hash__(self):
    self.assertNotEqual(hash(self.peak1), hash(self.peak2))
    self.assertEqual(hash(self.peak1), hash(self.peak3))

  def test__eq__(self):
    self.assertNotEqual(self.peak1, self.peak2)
    self.assertEqual(self.peak1, self.peak3)

if __name__ == '__main__': #pragma: no cover
  logging.getLogger().setLevel(logging.DEBUG)
  unittest.main()
