#!/usr/bin/env python
"""
================================================================================
:mod:`test_spacegroups` -- Unit tests for the module :mod:`spacegroups`.
================================================================================

.. module:: test_spacegroups
   :synopsis: Unit tests for the module :mod:`spacegroups`.

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

# Globals and constants variables.

class TestSpaceGroups(unittest.TestCase):

  def setUp(self):
    unittest.TestCase.setUp(self)

  def tearDown(self):
    unittest.TestCase.tearDown(self)

  def testSkeleton(self):
    #self.fail("Test if the TestCase is working.")
    self.assert_(True)

  def testspacegrouplist(self):
    self.assertEqual(len(spacegroups.spacegrouplist), 265)

  def testgetspacegroup(self):
    self.assertEqual(spacegroups.getspacegroup(1), spacegroups.sg1)

    self.assertEqual(spacegroups.getspacegroup("P4332"), spacegroups.sg212)

  def testconsistency(self):
    for sg in spacegroups.spacegrouplist:
      num_sym = len(sg.symop_list)
      self.assertEqual(sg.num_sym_equiv, num_sym)

if __name__ == '__main__': #pragma: no cover
  logging.getLogger().setLevel(logging.DEBUG)
  unittest.main()
