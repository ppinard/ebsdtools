#!/usr/bin/env jython
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
from math import pi

# Third party modules.
import rmlimage.module.real.io as io
import rmlimage.module.real.core as real
import rmlimage.io

# Local modules.
import DrixUtilities.Files as Files

import ebsdtools.patternsimulations.rmlimage.pattern as pattern
import ebsdtools.crystallography.reflectors as reflectors
import ebsdtools.crystallography.atomsites as atomsites
import ebsdtools.crystallography.unitcell as unitcell
import ebsdtools.crystallography.scatteringfactors as scatteringfactors

import mathtools.rotation.quaternions as quaternions
import mathtools.rotation.eulers as eulers

# Globals and constants variables.

class TestPatternFullSolidBand(unittest.TestCase):

  def setUp(self):
    unittest.TestCase.setUp(self)

    self.pattern = pattern.PatternFullSolidBand()

  def tearDown(self):
    unittest.TestCase.tearDown(self)

  def testSkeleton(self):
    #self.fail("Test if the TestCase is working.")
    self.assert_(True)

  def testdraw(self):
    self._init_pattern()

    pattern = self.pattern.draw()
    pattern.setFile('/tmp/pattern.rmp')
    io.IO.save(pattern)

    bytemap = real.Contrast.expansion(pattern)
    bytemap.setFile('/tmp/pattern.bmp')
    rmlimage.io.IO.save(bytemap)

  def _init_pattern(self):
    # Reflectors
    cell = unitcell.create_cubic_unitcell(3)
    atoms = atomsites.create_fcc_atomsites(14)

#    triclinic = unitcell.create_triclinic_unitcell(4, 5, 6
#                                                   , 75.0 / 180 * pi
#                                                   , 55.0 / 180 * pi
#                                                   , 35.0 / 180 * pi)
#    atoms = atomsites.create_single_atomsites(79)

    relativepath = os.path.join('..', '..', 'testdata', 'goodconfiguration.cfg')
    configurationfilepath = Files.getCurrentModulePath(__file__, relativepath)
    scatter = scatteringfactors.XrayScatteringFactors(configurationfilepath)

    self.reflectors = reflectors.Reflectors(cell, atoms, scatter)
    self.pattern.set_reflectors(self.reflectors)

    self.pattern.set_numberreflectors(len(self.reflectors))
    self.pattern.set_energy(30e3)
#    self.pattern.set_detectordistance(0.468)
    self.pattern.set_detectordistance(0.3)
#    self.pattern.set_patterncenter(-0.027, 0.196)
    self.pattern.set_patterncenter(0, 0)

#    angles = eulers.eulers_deg_to_eulers_rad(27.1, 35.7, 28.9)
#    rotation = quaternions.eulerangles_to_quaternion(angles)
#    self.pattern.set_rotation(rotation)

#class TestPatternFullProfiledBand(unittest.TestCase):
#
#  def setUp(self):
#    unittest.TestCase.setUp(self)
#
#    self.pattern = pattern.PatternFullProfiledBand()
#
#  def tearDown(self):
#    unittest.TestCase.tearDown(self)
#
#  def testSkeleton(self):
#    #self.fail("Test if the TestCase is working.")
#    self.assert_(True)
#
#  def testdraw(self):
#    self._init_pattern()
#
#    pattern = self.pattern.draw()
#    pattern.setFile('/tmp/patternreal.rmp')
#    io.IO.save(pattern)
#
#  def _init_pattern(self):
#    # Reflectors
#    cell = unitcell.create_cubic_unitcell(3)
#    atoms = atomsites.create_fcc_atomsites(14)
#
#    relativepath = os.path.join('..', '..', 'testdata', 'goodconfiguration.cfg')
#    configurationfilepath = Files.getCurrentModulePath(__file__, relativepath)
#    scatter = scatteringfactors.XrayScatteringFactors(configurationfilepath)
#
#    self.reflectors = reflectors.Reflectors(cell, atoms, scatter)
#    self.pattern.set_reflectors(self.reflectors)
#    self.pattern.set_numberreflectors(len(self.reflectors))

if __name__ == '__main__': #pragma: no cover
  logging.getLogger().setLevel(logging.DEBUG)
  unittest.main()
