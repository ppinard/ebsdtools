#!/usr/bin/env python
"""
================================================================================
:mod:`test_reflectors` -- Unit tests for the
                                  module :mod:`reflectors`.
================================================================================

.. module:: test_reflectors
   :synopsis: Unit tests for the module :mod:`reflectors`.
.. moduleauthor:: Philippe Pinard <philippe.pinard@mail.mcgill.ca>

"""

# Script information for the file.
__author__ = "Philippe Pinard (philippe.pinard@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2008 Philippe Pinard"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = "$Revision$"
__svnDate__ = "$Date$"
__svnId__ = "$Id$"

# Standard library modules.
import unittest
import logging
import os.path
import warnings

# Third party modules.

# Local modules.
import DrixUtilities.Files as Files

import ebsdtools.crystallography.reflectors as reflectors
import ebsdtools.crystallography.unitcell as unitcell
from ebsdtools.crystallography.plane import Plane
import ebsdtools.crystallography.scatteringfactors as scatteringfactors
from ebsdtools.crystallography.atomsite import AtomSite
from ebsdtools.crystallography.atomsites import AtomSites

# Globals and constants variables.

warnings.filterwarnings('ignore'
                        , category=scatteringfactors.ScatteringFactorWarning)

class TestReflectors(unittest.TestCase):

  def setUp(self):
    unittest.TestCase.setUp(self)

    # Unit cell.
    unitcell_fcc = unitcell.create_cubic_unitcell(5.43)
    unitcell_bcc = unitcell.create_cubic_unitcell(2.87)
    unitcell_hcp = unitcell.create_hexagonal_unitcell(3.21, 5.21)

    # Atom sites.
    atoms_fcc = AtomSites([AtomSite(14, 0.5, 0.5, 0.0)
                                , AtomSite(14, 0.5, 0.0, 0.5)
                                , AtomSite(14, 0.0, 0.5, 0.5)
                                , AtomSite(14, 0.0, 0.0, 0.0)])
    atoms_bcc = AtomSites([AtomSite(14, 0.5, 0.5, 0.5)
                           , AtomSite(14, 0.0, 0.0, 0.0)])
    atoms_hcp = AtomSites([AtomSite(14, 1 / 3.0, 2 / 3.0, 0.5)
                           , AtomSite(14, 0.0, 0.0, 0.0)])

    # Scattering factors
    relativepath = os.path.join('..', 'testdata', 'goodconfiguration.cfg')
    configurationfilepath = Files.getCurrentModulePath(__file__, relativepath)

    scatter = scatteringfactors.ElasticAtomicScatteringFactors(configurationfilepath)

    # Reflectors
    self.refls_fcc = reflectors.Reflectors(unitcell_fcc
                                           , atoms_fcc
                                           , scatter
                                           , maxindice=2)
    self.refls_bcc = reflectors.Reflectors(unitcell_bcc
                                           , atoms_bcc
                                           , scatter
                                           , maxindice=2)
    self.refls_hcp = reflectors.Reflectors(unitcell_hcp
                                           , atoms_hcp
                                           , scatter
                                           , maxindice=2)

  def tearDown(self):
    unittest.TestCase.tearDown(self)

  def testSkeleton(self):
#    self.fail("Test if the testcase is working.")
    self.assert_(True)

  def testplane(self):
    # BCC
    planes_bcc = [Plane(0, 1, 1), Plane(1, 1, 0), Plane(1, 0, 1)
                  , Plane(1, -1, 0), Plane(1, 0, -1), Plane(0, 1, -1)
                  , Plane(0, 2, 0), Plane(2, 0, 0)
                  , Plane(0, 0, 2), Plane(1, 1, 2), Plane(1, 2, 1)
                  , Plane(2, 1, 1), Plane(1, -2, -1), Plane(2, 1, -1)
                  , Plane(2, -1, -1), Plane(1, 1, -2), Plane(1, -1, -2)
                  , Plane(1, 2, -1), Plane(2, -1, 1), Plane(1, -2, 1)
                  , Plane(1, -1, 2), Plane(0, 2, 2), Plane(2, 0, 2)
                  , Plane(2, 2, 0), Plane(2, -2, 0), Plane(2, 0, -2)
                  , Plane(0, 2, -2), Plane(2, 2, 2), Plane(2, -2, -2)
                  , Plane(2, -2, 2), Plane(2, 2, -2)]

    for refl in self.refls_bcc:
      plane = refl.plane
      self.assertTrue(plane in planes_bcc)
      self.assertEqual((plane[0] + plane[1] + plane[2]) % 2, 0)

    # FCC
    planes_fcc = [Plane(1, 1, 1), Plane(1, -1, -1), Plane(1, 1, -1)
                  , Plane(1, -1, 1), Plane(0, 2, 0), Plane(0, 0, 2)
                  , Plane(2, 0, 0), Plane(0, 2, 2), Plane(2, 0, 2)
                  , Plane(2, 2, 0), Plane(0, 2, -2), Plane(2, 0, -2)
                  , Plane(2, -2, 0), Plane(2, 2, 2), Plane(2, -2, 2)
                  , Plane(2, -2, -2), Plane(2, 2, -2)]

    for refl in self.refls_fcc:
      plane = refl.plane
      self.assertTrue(plane in planes_fcc)

      if plane[0] % 2 == 0:
        self.assertEqual(plane[1] % 2, 0)
        self.assertEqual(plane[2] % 2, 0)
      else: # plane[0] % 2 == 1
        self.assertEqual(plane[1] % 2, 1)
        self.assertEqual(plane[2] % 2, 1)

    # HCP
    for refl in self.refls_hcp:
      plane = refl.plane
      # From Rollett 2008
      condition1 = (plane[0] + 2 * plane[1]) % 3 < 0
      condition2 = plane[2] % 2 == 1
      self.assertNotEqual(condition1 and condition2, True)

  def testplanespacing(self):
    ## Compared with HKL Channel 5 Phases Database
    # BCC
    refl = self.refls_bcc.get(Plane(1, 0, 1))
    self.assertAlmostEqual(refl.planespacing, 2.0293964620053915)

    refl = self.refls_bcc.get(Plane(1, -1, 0))
    self.assertAlmostEqual(refl.planespacing, 2.0293964620053915)

    refl = self.refls_bcc.get(Plane(2, 0, 0))
    self.assertAlmostEqual(refl.planespacing, 1.4349999999999998)

    refl = self.refls_bcc.get(Plane(1, -1, 2))
    self.assertAlmostEqual(refl.planespacing, 1.1716725936312868)

    refl = self.refls_bcc.get(Plane(2, 0, 2))
    self.assertAlmostEqual(refl.planespacing, 1.0146982310026957)

    # FCC
    refl = self.refls_fcc.get(Plane(1, 1, 1))
    self.assertAlmostEqual(refl.planespacing, 3.1350119616996683)

    refl = self.refls_fcc.get(Plane(1, -1, 1))
    self.assertAlmostEqual(refl.planespacing, 3.1350119616996683)

    refl = self.refls_fcc.get(Plane(2, -2, 0))
    self.assertAlmostEqual(refl.planespacing, 1.919794910921476)

    # HCP
    refl = self.refls_hcp.get(Plane(0, 0, 2))
    self.assertAlmostEqual(refl.planespacing, 2.6050000000000004)

    refl = self.refls_hcp.get(Plane(1, 0, -1))
    self.assertAlmostEqual(refl.planespacing, 2.4526403546701228)

    refl = self.refls_hcp.get(Plane(2, -1, 0))
    self.assertAlmostEqual(refl.planespacing, 1.6050000000000002)

  def testintensity(self):
    # BCC
    refl = self.refls_bcc.get(Plane(1, 0, 1))
    self.assertAlmostEqual(refl.intensity, 0.0044562961611491949)

    refl = self.refls_bcc.get(Plane(1, -1, 0))
    self.assertAlmostEqual(refl.intensity, 0.0044562961611491949)

    refl = self.refls_bcc.get(Plane(2, 0, 0))
    self.assertAlmostEqual(refl.intensity, 0.0013809857316082104)

    # FCC
    refl = self.refls_fcc.get(Plane(1, 1, 1))
    self.assertAlmostEqual(refl.intensity, 0.0859145669508)

    refl = self.refls_fcc.get(Plane(1, -1, 1))
    self.assertAlmostEqual(refl.intensity, 0.0859145669508)

    refl = self.refls_fcc.get(Plane(2, -2, 0))
    self.assertAlmostEqual(refl.intensity, 0.0152361124413)

    # HCP
    refl = self.refls_hcp.get(Plane(0, 0, 2))
    self.assertAlmostEqual(refl.intensity, 0.0099153044364262422)

    refl = self.refls_hcp.get(Plane(1, 0, -1))
    self.assertAlmostEqual(refl.intensity, 0.0059739159485949992)

    refl = self.refls_hcp.get(Plane(2, -1, 0))
    self.assertAlmostEqual(refl.intensity, 0.002165252452505663)

  def testnormalizedintensity(self):
    # BCC
    refl = self.refls_bcc.get(Plane(1, 0, 1))
    self.assertAlmostEqual(refl.normalizedintensity, 1.0)

    refl = self.refls_bcc.get(Plane(1, -1, 0))
    self.assertAlmostEqual(refl.normalizedintensity, 1.0)

    refl = self.refls_bcc.get(Plane(2, 0, 0))
    self.assertAlmostEqual(refl.normalizedintensity, 0.30989541127178588)

    # FCC
    refl = self.refls_fcc.get(Plane(1, 1, 1))
    self.assertAlmostEqual(refl.normalizedintensity, 1.0)

    refl = self.refls_fcc.get(Plane(1, -1, 1))
    self.assertAlmostEqual(refl.normalizedintensity, 1.0)

    refl = self.refls_fcc.get(Plane(2, -2, 0))
    self.assertAlmostEqual(refl.normalizedintensity, 0.177340269316)

    # HCP
    refl = self.refls_hcp.get(Plane(0, 0, 2))
    self.assertAlmostEqual(refl.normalizedintensity, 1.0)

    refl = self.refls_hcp.get(Plane(1, 0, -1))
    self.assertAlmostEqual(refl.normalizedintensity, 0.60249445560626358)

    refl = self.refls_hcp.get(Plane(2, -1, 0))
    self.assertAlmostEqual(refl.normalizedintensity, 0.21837478278035422)

if __name__ == '__main__': #pragma: no cover
  logging.getLogger().setLevel(logging.DEBUG)
  unittest.main()
