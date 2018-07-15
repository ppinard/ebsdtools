#!/usr/bin/env python
"""
================================================================================
:mod:`test_plane` -- Unit tests for the module :mod:`plane`.
================================================================================

.. module:: test_plane
   :synopsis: Unit tests for the module :mod:`plane`.

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
import ebsdtools.crystallography.plane as plane

# Globals and constants variables.

class TestPlane(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.plane1 = plane.Plane(3, 3, 3)
        self.plane2 = plane.Plane(1, -2, 1, 0)
        self.plane3 = plane.Plane(-1, -2, 1, 0)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testcontructor(self):
        self.assertEqual(self.plane1.indices, (3.0, 3.0, 3.0))
        self.assertEqual(self.plane2.indices, (1.0, -2.0, 0.0))
        self.assertEqual(self.plane3.indices, (-1.0, -2.0, 0.0))

    def testsimplify(self):
        indices = self.plane1.simplify().indices
        self.assertEqual(indices, (1.0, 1.0, 1.0))

        indices = self.plane2.simplify().indices
        self.assertEqual(indices, (1.0, -2.0, 0.0))

        indices = self.plane3.simplify().indices
        self.assertEqual(indices, (1.0, 2.0, 0.0))

    def testto_bravais(self):
        bravais = self.plane1.indices_bravais
        self.assertEqual(bravais, [3.0, 3.0, -6.0, 3.0])

        bravais = self.plane2.indices_bravais
        self.assertEqual(bravais, [1.0, -2.0, 1.0, 0.0])

        bravais = self.plane3.indices_bravais
        self.assertEqual(bravais, [-1.0, -2.0, 3.0, 0.0])

    def testhash(self):
        self.assertEqual(5050908322398645920, hash(self.plane1))

class TestPlaneFunctions(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.miller1 = [1, 1, 0]
        self.miller2 = [1, -2, 0]
        self.bravais1 = [1, 1, -2, 0]
        self.bravais2 = [1, -2, 1, 0]

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testmiller_to_bravais(self):
        bravais = plane.miller_to_bravais(self.miller1)
        self.assertEqual(bravais, self.bravais1)

        bravais = plane.miller_to_bravais(self.miller2)
        self.assertEqual(bravais, self.bravais2)

    def testbravais_to_miller(self):
        miller = plane.bravais_to_miller(self.bravais1)
        self.assertEqual(miller, self.miller1)

        miller = plane.bravais_to_miller(self.bravais2)
        self.assertEqual(miller, self.miller2)

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
