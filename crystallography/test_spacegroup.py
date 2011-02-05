#!/usr/bin/env python
"""
================================================================================
:mod:`test_spacegroup` -- Unit tests for the module :mod:`spacegroup`.
================================================================================

.. module:: test_spacegroup
   :synopsis: Unit tests for the module :mod:`spacegroup`.

"""

# Script information for the file.
__author__ = "Philippe T. Pinard"
__email__ = "philippe.pinard@gmail.com"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2009 Philippe T. Pinard"
__license__ = "GPL v3"

# Standard library modules.
import unittest
import logging

# Third party modules.

# Local modules.
import ebsdtools.crystallography.spacegroups as spacegroups
import ebsdtools.crystallography.atomsite as atomsite

# Globals and constants variables.

class TestSpaceGroup(unittest.TestCase):

  def setUp(self):
    unittest.TestCase.setUp(self)

    self.sg = spacegroups.sg25
    self.atom1 = atomsite.AtomSite(13, 1, 0, 0)
    self.atom2 = atomsite.AtomSite(13, 0.1, 0.1, 0.1)

  def tearDown(self):
    unittest.TestCase.tearDown(self)

  def testSkeleton(self):
    #self.fail("Test if the TestCase is working.")
    self.assert_(True)

  def testconstructor(self):
    self.assertEqual(self.sg.number, 25)
    self.assertEqual(self.sg.num_sym_equiv, 4)
    self.assertEqual(self.sg.num_primitive_sym_equiv, 4)
    self.assertEqual(self.sg.short_name, "Pmm2")
    self.assertEqual(self.sg.point_group_name, "PGmm2")
    self.assertEqual(self.sg.crystal_system, spacegroups.ORTHORHOMBIC)
    self.assertEqual(self.sg.pdb_name, "P m m 2")
    self.assertEqual(len(self.sg.symop_list), 4)

  def testiter_symops(self):
    symops = list(self.sg.iter_symops())
    self.assertEqual(len(symops), len(self.sg.symop_list))

  def testcheck_group_name(self):
    self.assertTrue(self.sg.check_group_name(25))
    self.assertTrue(self.sg.check_group_name("Pmm2"))
    self.assertTrue(self.sg.check_group_name("P m m 2"))

    self.assertFalse(self.sg.check_group_name(26))
    self.assertFalse(self.sg.check_group_name("Pmc21"))
    self.assertFalse(self.sg.check_group_name("P m c 21"))

  def testiter_equivalent_positions(self):
    equiv_atoms = list(self.sg.iter_equivalent_atomsites(self.atom1))
    self.assertEqual(len(equiv_atoms), 4)

    equiv_atoms = list(self.sg.iter_equivalent_atomsites(self.atom2))
    self.assertEqual(len(equiv_atoms), 4)

  def testequivalent_atomsites(self):
    equiv_atoms = self.sg.equivalent_atomsites(self.atom1)
    self.assertEqual(len(equiv_atoms), 1)

    equiv_atoms = self.sg.equivalent_atomsites(self.atom2)
    self.assertEqual(len(equiv_atoms), 4)

if __name__ == '__main__': #pragma: no cover
  logging.getLogger().setLevel(logging.DEBUG)
  unittest.main()
