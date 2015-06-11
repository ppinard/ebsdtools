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
from mathtools.algebra.vectors import almostequal

# Globals and constants variables.

class TestAtomSite(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.atom1 = atomsite.AtomSite(13, 0, 0.5, 1.5)
        self.atom2 = atomsite.AtomSite(14, (0.3, -0.8, 0.1))

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        #self.fail("Test if the TestCase is working.")
        self.assert_(True)

    def testconstructor(self):
        self.assertEqual(self.atom1.atomicnumber, 13)
        self.assertEqual(self.atom2.atomicnumber, 14)

        self.assertTrue(almostequal(self.atom1.position, [0, 0.5, 0.5]))
        self.assertTrue(almostequal(self.atom2.position, [0.3, 0.2, 0.1]))

    def test__repr__(self):
        self.assertEqual(str(self.atom1), "Al->[0.0, 0.5, 0.5]")
        self.assertEqual(str(self.atom2), "Si->[0.29999999999999999, 0.19999999999999996, 0.10000000000000001]")

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
