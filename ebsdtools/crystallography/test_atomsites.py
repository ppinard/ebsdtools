#!/usr/bin/env python
"""
================================================================================
:mod:`test_atomsites` -- Unit tests for the module :mod:`atomsites.`
================================================================================

.. module:: test_atomsites
   :synopsis: Unit tests for the module :mod:`atomsites.`

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
import ebsdtools.crystallography.atomsites as atomsites
import ebsdtools.crystallography.atomsite as atomsite

# Globals and constants variables.

class TestAtomSites(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.atoms = atomsites.AtomSites()

        self.atom1 = atomsite.AtomSite(13, 0, 0, 0)
        self.atom2 = atomsite.AtomSite(13, 0, 0.5, 0.5)
        self.atom3 = atomsite.AtomSite(13, 0.5, 0, 0.5)
        self.atom4 = atomsite.AtomSite(13, 0, 0.5, 0.5)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testadd(self):
        self.atoms.add(self.atom1)
        self.assertEqual(1, len(self.atoms))
        self.assertIn(self.atom1, self.atoms)

        self.atoms.add(self.atom1)
        self.assertEqual(1, len(self.atoms))
        self.assertIn(self.atom1, self.atoms)

    def testdiscard(self):
        self.atoms.add(self.atom1)
        self.assertEqual(1, len(self.atoms))
        self.assertIn(self.atom1, self.atoms)

        self.atoms.discard(self.atom1)
        self.assertEqual(len(self.atoms), 0)
        self.assertNotIn(self.atom1, self.atoms)

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
