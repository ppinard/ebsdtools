#!/usr/bin/env python
"""
================================================================================
:mod:`test_eulers` -- Unit tests for the module :mod:`eulers`.
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
import random
from math import pi

# Third party modules.

# Local modules.
import mathtools.rotation.eulers as eulers

# Globals and constants variables.
REPETITIONS = 1000

class TestEulers(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.e1 = eulers.Eulers(0.1, 0.2, 0.3)
        self.e2 = eulers.Eulers([0.4, 0.5, 0.6])
        self.e3 = eulers.Eulers((0.7, 0.8, 0.9))

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        #self.fail("Test if the TestCase is working.")
        self.assert_(True)

    def testeulers_deg_to_eulers_rad(self):
        for _i in range(REPETITIONS):
            euler1 = random.random() * 360
            euler2 = random.random() * 180
            euler3 = random.random() * 360

            e1 = eulers.eulers_deg_to_eulers_rad(euler1, euler2, euler3)

            self.assertAlmostEqual(e1.to_deg()[0], euler1)
            self.assertAlmostEqual(e1.to_deg()[1], euler2)
            self.assertAlmostEqual(e1.to_deg()[2], euler3)

    def test__getitem__(self):
        self.assertEqual(self.e1['theta1'], 0.1)
        self.assertEqual(self.e1['theta2'], 0.2)
        self.assertEqual(self.e1['theta3'], 0.3)

        self.assertEqual(self.e2['phi1'], 0.4)
        self.assertEqual(self.e2['phi'], 0.5)
        self.assertEqual(self.e2['phi2'], 0.6)

        self.assertEqual(self.e3['alpha'], 0.7)
        self.assertEqual(self.e3['beta'], 0.8)
        self.assertEqual(self.e3['gamma'], 0.9)

    def test__setitem__(self):
        value = 9.9
        self.e1['theta1'] = 9.9
        self.assertEqual(value, self.e1['theta1'])

        value = 9.9
        self.e2['phi1'] = 9.9
        self.assertEqual(value, self.e2['phi1'])

        value = 9.9
        self.e3['alpha'] = 9.9
        self.assertEqual(value, self.e3['alpha'])

        value = 9.9
        self.e1[1] = 9.9
        self.assertEqual(value, self.e1[1])

    def test__str__(self):
        expected_str = '(0.100000, 0.200000, 0.300000)'
        self.assertEqual(str(self.e1), expected_str)

        expected_str = '(0.400000, 0.500000, 0.600000)'
        self.assertEqual(str(self.e2), expected_str)

        expected_str = '(0.700000, 0.800000, 0.900000)'
        self.assertEqual(str(self.e3), expected_str)

    def test__eq__(self):
        euler = eulers.Eulers(0.1, 0.2, 0.3)
        self.assertTrue(self.e1 == euler)

        euler = eulers.Eulers(0.4, 0.5, 0.6)
        self.assertTrue(self.e2 == euler)

        euler = eulers.Eulers(0.7, 0.8, 0.9)
        self.assertTrue(self.e3 == euler)

    def test__ne__(self):
        self.assertTrue(self.e1 != self.e2)
        self.assertTrue(self.e1 != self.e3)
        self.assertTrue(self.e2 != self.e3)

    def testto_deg(self):
            expected_eulers_deg = (0.1 / pi * 180.0, 0.2 / pi * 180.0, 0.3 / pi * 180.0)
            eulers_deg = self.e1.to_deg()
            self.assertAlmostEqual(expected_eulers_deg[0], eulers_deg[0])
            self.assertAlmostEqual(expected_eulers_deg[1], eulers_deg[1])
            self.assertAlmostEqual(expected_eulers_deg[2], eulers_deg[2])

            expected_eulers_deg = (0.4 / pi * 180.0, 0.5 / pi * 180.0, 0.6 / pi * 180.0)
            eulers_deg = self.e2.to_deg()
            self.assertAlmostEqual(expected_eulers_deg[0], eulers_deg[0])
            self.assertAlmostEqual(expected_eulers_deg[1], eulers_deg[1])
            self.assertAlmostEqual(expected_eulers_deg[2], eulers_deg[2])

            expected_eulers_deg = (0.7 / pi * 180.0, 0.8 / pi * 180.0, 0.9 / pi * 180.0)
            eulers_deg = self.e3.to_deg()
            self.assertAlmostEqual(expected_eulers_deg[0], eulers_deg[0])
            self.assertAlmostEqual(expected_eulers_deg[1], eulers_deg[1])
            self.assertAlmostEqual(expected_eulers_deg[2], eulers_deg[2])

    def testto_rad(self):
        expected_eulers_deg = (0.1, 0.2, 0.3)
        eulers_deg = self.e1.to_rad()
        self.assertAlmostEqual(expected_eulers_deg[0], eulers_deg[0])
        self.assertAlmostEqual(expected_eulers_deg[1], eulers_deg[1])
        self.assertAlmostEqual(expected_eulers_deg[2], eulers_deg[2])

        expected_eulers_deg = (0.4, 0.5, 0.6)
        eulers_deg = self.e2.to_rad()
        self.assertAlmostEqual(expected_eulers_deg[0], eulers_deg[0])
        self.assertAlmostEqual(expected_eulers_deg[1], eulers_deg[1])
        self.assertAlmostEqual(expected_eulers_deg[2], eulers_deg[2])

        expected_eulers_deg = (0.7, 0.8, 0.9)
        eulers_deg = self.e3.to_rad()
        self.assertAlmostEqual(expected_eulers_deg[0], eulers_deg[0])
        self.assertAlmostEqual(expected_eulers_deg[1], eulers_deg[1])
        self.assertAlmostEqual(expected_eulers_deg[2], eulers_deg[2])

    def testpositive(self):
        e1 = eulers.positive(eulers.Eulers(0, 0, 0)).to_rad()
        self.assertAlmostEqual(e1[0], 0.0)
        self.assertAlmostEqual(e1[1], 0.0)
        self.assertAlmostEqual(e1[2], 0.0)

        eulers1 = eulers.Eulers(pi, 0, pi)
        eulers1.positive()
        e1 = eulers1.to_rad()
        self.assertAlmostEqual(e1[0], pi)
        self.assertAlmostEqual(e1[1], 0.0)
        self.assertAlmostEqual(e1[2], pi)

        eulers1 = eulers.Eulers(-pi / 2.0, 0, -pi / 3)
        eulers1.positive()
        e1 = eulers1.to_rad()
        self.assertAlmostEqual(e1[0], 3.0 * pi / 2.0)
        self.assertAlmostEqual(e1[1], 0.0)
        self.assertAlmostEqual(e1[2], 5.0 * pi / 3.0)

    def testnegative(self):
        e1 = eulers.negative(eulers.Eulers(0, 0, 0)).to_rad()
        self.assertAlmostEqual(e1[0], 0.0)
        self.assertAlmostEqual(e1[1], 0.0)
        self.assertAlmostEqual(e1[2], 0.0)

        eulers1 = eulers.Eulers(pi, 0, pi)
        eulers1.negative()
        e1 = eulers1.to_rad()
        self.assertAlmostEqual(e1[0], pi)
        self.assertAlmostEqual(e1[1], 0.0)
        self.assertAlmostEqual(e1[2], pi)

        eulers1 = eulers.Eulers(3.0 * pi / 2.0, 0, 5 * pi / 3)
        eulers1.negative()
        e1 = eulers1.to_rad()
        self.assertAlmostEqual(e1[0], -pi / 2.0)
        self.assertAlmostEqual(e1[1], 0)
        self.assertAlmostEqual(e1[2], -pi / 3)

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
