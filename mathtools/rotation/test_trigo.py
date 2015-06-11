#!/usr/bin/env python
"""
================================================================================
:mod:`test_trigo` -- Unit tests for the module :mod:`trigo`.
================================================================================

"""

# Script information for the file.
__author__ = "Philippe T. Pinard"
__email__ = "philippe.pinard@gmail.com"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2010 Philippe T. Pinard"
__license__ = "GPL v3"

# Standard library modules.
import unittest
import logging
from math import pi, acos

# Third party modules.

# Local modules.
import mathtools.rotation.trigo as trigo

# Globals and constants variables.

class TestTrigo(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        #self.fail("Test if the TestCase is working.")
        self.assert_(True)

    def testacos(self):
        self.assertEqual(trigo.acos(4), 0)
        self.assertEqual(trigo.acos(-4), pi)
        self.assertAlmostEqual(trigo.acos(0.5), 60 / 180.0 * pi)
        self.assertAlmostEqual(trigo.acos(0.45675), acos(0.45675))

    def testsmallangle(self):
        #TODO: test trigo.smallangle
        pass

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()

