#!/usr/bin/env python
"""
================================================================================
:mod:`test_band` -- Unit tests for the module :mod:`band`.
================================================================================

.. module:: test_band
   :synopsis: Unit tests for the module :mod:`band`.
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
import ebsdtools.patternsimulations.band as band
import ebsdtools.crystallography.reflectors as reflectors

# Globals and constants variables.

class TestBand(unittest.TestCase):

  def setUp(self):
    unittest.TestCase.setUp(self)

    self.reflector = reflectors.Reflector((1, 0, 0), 1, 1.0)
    self.band = band.Band(self.reflector)

    self.band.setdefault(band.Band.SLOPE, 0.2)
    self.band.setdefault(band.Band.INTERCEPT, 0.3)
    self.band.setdefault(band.Band.THICKNESS, 0.4)
    self.band.setdefault(band.Band.HALFWIDTHS, (0.5, 0.5))
    self.band.setdefault(band.Band.EDGEINTERCEPTS, (0.5, 0.5))

  def tearDown(self):
    unittest.TestCase.tearDown(self)

  def testSkeleton(self):
    #self.fail("Test if the TestCase is working.")
    self.assert_(True)

  def testconstructor(self):
    self.assertEqual(self.band.plane, self.reflector.plane)
    self.assertEqual(self.band.planespacing, self.reflector.planespacing)
    self.assertEqual(self.band.intensity, self.reflector.intensity)

    self.assertEqual(self.band.m, 0.2)
    self.assertEqual(self.band.k, 0.3)
    self.assertEqual(self.band.thickness, 0.4)
    self.assertEqual(self.band.halfwidths, (0.5, 0.5))
    self.assertEqual(self.band.edgeintercepts, (0.5, 0.5))

if __name__ == '__main__': #pragma: no cover
  logging.getLogger().setLevel(logging.DEBUG)
  unittest.main()
