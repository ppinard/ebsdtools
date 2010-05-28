#!/usr/bin/env python
"""
================================================================================
:mod:`test_calculations` -- Unit tests for the module :mod:`calculations`.
================================================================================

.. module:: test_calculations
   :synopsis: Unit tests for the module :mod:`calculations`.
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
from math import pi

# Third party modules.

# Local modules.
import ebsdtools.hough.calculations as calculations

# Globals and constants variables.

class TestCalculations(unittest.TestCase):

  def setUp(self):
    unittest.TestCase.setUp(self)

  def tearDown(self):
    unittest.TestCase.tearDown(self)

  def testSkeleton(self):
    #self.fail("Test if the TestCase is working.")
    self.assert_(True)

  def testlinespace_to_houghspace(self):
    rho, theta = calculations.linespace_to_houghspace(m=None, k=2)
    self.assertAlmostEqual(rho, 2.0)
    self.assertAlmostEqual(theta, 0.0)

    rho, theta = calculations.linespace_to_houghspace(m=0, k=2)
    self.assertAlmostEqual(rho, 2.0)
    self.assertAlmostEqual(theta, pi / 2.0)

    rho, theta = calculations.linespace_to_houghspace(m=1, k=0)
#    self.assertAlmostEqual(rho, 0.0)
#    self.assertAlmostEqual(theta, pi / 4.0)

    rho, theta = calculations.linespace_to_houghspace(m=1, k= -2)
#    print rho, theta

  def testhoughspace_to_linespace(self):
    m, k = calculations.houghspace_to_linespace(0, 0)
    self.assertEqual(m, None)
    self.assertAlmostEqual(k, 0.0)

    m, k = calculations.houghspace_to_linespace(2, 0)
    self.assertEqual(m, None)
    self.assertAlmostEqual(k, 2.0)

    m, k = calculations.houghspace_to_linespace(-2, 0)
    self.assertEqual(m, None)
    self.assertAlmostEqual(k, -2.0)

    m, k = calculations.houghspace_to_linespace(2, pi / 2.0)
    print m, k

if __name__ == '__main__': #pragma: no cover
  logging.getLogger().setLevel(logging.DEBUG)
  unittest.main()
