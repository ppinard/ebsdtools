#!/usr/bin/env python
"""
================================================================================
:mod:`test_atomsite` -- Unit tests for the module :mod:`atomsite.`
================================================================================

.. module:: test_atomsite
   :synopsis: Unit tests for the module :mod:`atomsite.`

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
import ebsdtools.crystallography.atomsite as atomsite

# Globals and constants variables.

class TestAtomSite(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.atom1 = atomsite.AtomSite(13, 0, 0.5, 1.5)
        self.atom2 = atomsite.AtomSite(14, (0.3, -0.8, 0.1))

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testconstructor(self):
        self.assertEqual(self.atom1.atomicnumber, 13)
        self.assertEqual(self.atom2.atomicnumber, 14)

        self.assertAlmostEqual(self.atom1.position[0], 0.0, 4)
        self.assertAlmostEqual(self.atom1.position[1], 0.5, 4)
        self.assertAlmostEqual(self.atom1.position[2], 0.5, 4)
        self.assertAlmostEqual(self.atom2.position[0], 0.3, 4)
        self.assertAlmostEqual(self.atom2.position[1], 0.2, 4)
        self.assertAlmostEqual(self.atom2.position[2], 0.1, 4)

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
