#!/usr/bin/env python
"""
================================================================================
:mod:`test_module` -- Unit tests for the module :mod:`module`.
================================================================================

.. currentmodule:: test_module
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
import os.path

# Third party modules.

# Local modules.
import DrixUtilities.Files as Files

import ebsdtools.patternsimulations.pattern as pattern
import ebsdtools.crystallography.reflectors as reflectors
import ebsdtools.crystallography.atomsites as atomsites
import ebsdtools.crystallography.unitcell as unitcell
import ebsdtools.crystallography.scatteringfactors as scatteringfactors
import ebsdtools.patternsimulations.band as band

import mathtools.rotation.quaternions as quaternions

# Globals and constants variables.

class TestPattern(unittest.TestCase):

  def setUp(self):
    unittest.TestCase.setUp(self)

    self.pattern = pattern.Pattern()

  def tearDown(self):
    unittest.TestCase.tearDown(self)

  def testSkeleton(self):
    #self.fail("Test if the TestCase is working.")
    self.assert_(True)

  def test_init_variables(self):
    self.assertEqual(self.pattern._reflectors, [])
    self.assertEqual(self.pattern._patterncenter_x, 0.0)
    self.assertEqual(self.pattern._patterncenter_y, 0.0)
    self.assertEqual(self.pattern._detectordistance, 0.3)
    self.assertEqual(self.pattern._energy, 20e3)
    self.assertEqual(self.pattern._numberreflectors, 32)
    self.assertEqual(self.pattern._rotation, quaternions.Quaternion(1))
    self.assertEqual(self.pattern._bands, [])

  def testset_reflectors(self):
    reflectors = 'abc'
    self.pattern.set_reflectors(reflectors)
    self.assertEqual(self.pattern._reflectors, reflectors)

  def testset_patterncenter(self):
    x = 1.0
    y = 2.0
    self.pattern.set_patterncenter(x, y)
    self.assertEqual(self.pattern._patterncenter_x, x)
    self.assertEqual(self.pattern._patterncenter_y, y)

  def testset_detectordistance(self):
    detectordistance = 0.5
    self.pattern.set_detectordistance(detectordistance)
    self.assertEqual(self.pattern._detectordistance, detectordistance)

  def testset_energy(self):
    energy = 15
    self.pattern.set_energy(energy)
    self.assertEqual(self.pattern._energy, energy)

  def testset_numberreflectors(self):
    number = 54
    self.pattern.set_numberreflectors(number)
    self.assertEqual(self.pattern._numberreflectors, number)

  def testset_rotation(self):
    rotation = 'abc'
    self.pattern.set_rotation(rotation)
    self.assertEqual(self.pattern._rotation, rotation)

  def test_get_slope_intercept(self):
    self._init_pattern()

    reflector = self.reflectors[0]
    m, k = self.pattern._get_slope_intercept(reflector)
    self.assertAlmostEqual(m, 1.0)
    self.assertAlmostEqual(k, 0.3)

    reflector = self.reflectors[8]
    m, k = self.pattern._get_slope_intercept(reflector)
    self.assertAlmostEqual(m, 0.0)
    self.assertAlmostEqual(k, 0.3)

  def test_get_band_halfwidths(self):
    self._init_pattern()

    reflector = self.reflectors[0]
    m, k = self.pattern._get_slope_intercept(reflector)
    width_top, width_bottom = self.pattern._get_band_halfwidths(reflector, m, k)
    self.assertAlmostEqual(width_top , 0.0106700330794)
    self.assertAlmostEqual(width_bottom, 0.011040241968)

  def test_get_edges_intercepts(self):
    self._init_pattern()

    reflector = self.reflectors[0]
    m, k = self.pattern._get_slope_intercept(reflector)
    width_top, width_bottom = self.pattern._get_band_halfwidths(reflector, m, k)
    k_top, k_bottom = self.pattern._get_edges_intercepts(m, k
                                                         , width_top
                                                         , width_bottom)
    self.assertAlmostEqual(k_top , 0.315089705492)
    self.assertAlmostEqual(k_bottom, 0.284386740077)

  def test_get_band_thickness(self):
    width = 0.01
    thickness = self.pattern._get_band_thickness(width)
    self.assertAlmostEqual(thickness, 54)

  def test_calculate_bands(self):
    self._init_pattern()
    self.pattern._calculate_bands()

    # 32 - 2 parallel plane to the screen = 30
    self.assertEqual(len(self.pattern._bands), 30)

  def _init_pattern(self):
    # Reflectors
    cell = unitcell.create_cubic_unitcell(3)
    atoms = atomsites.create_fcc_atomsites(14)

    relativepath = os.path.join('..', 'testdata', 'goodconfiguration.cfg')
    configurationfilepath = Files.getCurrentModulePath(__file__, relativepath)
    scatter = scatteringfactors.XrayScatteringFactors(configurationfilepath)

    self.reflectors = reflectors.Reflectors(cell, atoms, scatter)
    self.pattern.set_reflectors(self.reflectors)

if __name__ == '__main__': #pragma: no cover
  logging.getLogger().setLevel(logging.DEBUG)
  unittest.main()
