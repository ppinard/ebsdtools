#!/usr/bin/env python
"""
================================================================================
:mod:`test_scatteringfactors` -- Unit tests for the
                                  module :mod:`scatteringfactors`.
================================================================================

.. module:: test_scatteringfactors
   :synopsis: Unit tests for the module :mod:`scatteringfactors`.

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
import os.path
from math import pi
import warnings

# Third party modules.

# Local modules.
import DrixUtilities.Files as Files

import ebsdtools.crystallography.scatteringfactors as scatteringfactors
warnings.filterwarnings(action='ignore'
                        , category=scatteringfactors.ScatteringFactorWarning)

# Globals and constants variables.

class ScatteringFactors(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        #self.fail("Test if the TestCase is working.")
        self.assert_(True)

class TestElasticAtomicScatteringFactors(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        relativepath = os.path.join('..', 'testdata', 'goodconfiguration.cfg')
        configurationfilepath = Files.getCurrentModulePath(__file__, relativepath)

        self.scatter = scatteringfactors.ElasticAtomicScatteringFactors(configurationfilepath)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        #self.fail("Test if the TestCase is working.")
        self.assert_(True)

    def test_read(self):
        self.assertEqual(len(self.scatter.coefficients_0_2), 98)
        self.assertEqual(len(self.scatter.coefficients_2_6), 98)

        columns = ['a1', 'a2', 'a3', 'a4', 'a5',
                   'b1', 'b2', 'b3', 'b4', 'b5']

        for atomicnumber in range(1, 98 + 1):
            data = self.scatter.coefficients_0_2.get(atomicnumber)
            self.assertNotEqual(data, None)

            for column in columns:
                self.assertTrue(isinstance(data[column], float))

            data = self.scatter.coefficients_2_6.get(atomicnumber)
            for column in columns:
                self.assertTrue(isinstance(data[column], float))

    def testget(self):
        ## Aluminium
        # s = 0.5
        factor = self.scatter.get(14, 4 * pi)
        expected_factor = 0.742519788187
        self.assertAlmostEqual(factor, expected_factor)

        # s = 3.0
        factor = self.scatter.get(14, 2.0 / 3.0 * pi)
        expected_factor = 0.0349033998305
        self.assertAlmostEqual(factor, expected_factor)

        # s = 6.1
        factor = self.scatter.get(14, 2.0 / 6.1 * pi)
        expected_factor = 0.00650227565622
        self.assertAlmostEqual(factor, expected_factor)

        ## Copper
        # s = 0.5
        factor = self.scatter.get(29, 4 * pi)
        expected_factor = 1.46390369208
        self.assertAlmostEqual(factor, expected_factor)

        # s = 3.0
        factor = self.scatter.get(29, 2.0 / 3.0 * pi)
        expected_factor = 0.0652299842623
        self.assertAlmostEqual(factor, expected_factor)

        # s = 6.1
        factor = self.scatter.get(29, 2.0 / 6.1 * pi)
        expected_factor = 0.000336590516491
        self.assertAlmostEqual(factor, expected_factor)

        ## Gold
        # s = 0.5
        factor = self.scatter.get(79, 4 * pi)
        expected_factor = 3.07239344718
        self.assertAlmostEqual(factor, expected_factor)

        # s = 3.0
        factor = self.scatter.get(79, 2.0 / 3.0 * pi)
        expected_factor = 0.186031146844
        self.assertAlmostEqual(factor, expected_factor)

        # s = 6.1
        factor = self.scatter.get(79, 2.0 / 6.1 * pi)
        expected_factor = 0.0332559532
        self.assertAlmostEqual(factor, expected_factor)

class TestXrayScatteringFactors(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        relativepath = os.path.join('..', 'testdata', 'goodconfiguration.cfg')
        configurationfilepath = Files.getCurrentModulePath(__file__, relativepath)

        self.scatter = scatteringfactors.XrayScatteringFactors(configurationfilepath)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        #self.fail("Test if the TestCase is working.")
        self.assert_(True)

    def test_read(self):
        self.assertEqual(len(self.scatter.coefficients_0_2), 210)
        self.assertEqual(len(self.scatter.coefficients_2_6), 97)

        columns = ['a1', 'a2', 'a3', 'a4',
                   'b1', 'b2', 'b3', 'b4',
                   'c']
        for atomicnumber in range(1, 98 + 1):
            data = self.scatter.coefficients_0_2.get((atomicnumber, 0))
            self.assertNotEqual(data, None)

            for column in columns:
                self.assertTrue(isinstance(data[column], float))

            model = data[scatteringfactors.XrayScatteringFactors.MODEL]
            self.assertTrue(model in scatteringfactors.XrayScatteringFactors.MODELS)

        columns = ['a0', 'a1', 'a2', 'a3']
        for atomicnumber in range(2, 98 + 1):
            data = self.scatter.coefficients_2_6.get((atomicnumber, 0))
            self.assertNotEqual(data, None)

            for column in columns:
                self.assertTrue(isinstance(data[column], float))

            model = data[scatteringfactors.XrayScatteringFactors.MODEL]
            self.assertTrue(model in scatteringfactors.XrayScatteringFactors.MODELS)

    def testget(self):
        ## Aluminium
        # s = 0.5
        factor = self.scatter.get(14, 1.0)
        expected_factor = 6.2400885119901508
        self.assertAlmostEqual(factor, expected_factor)

        # s = 3.0
        factor = self.scatter.get(14, 1.0 / 6.0)
        expected_factor = 0.72266443008234738
        self.assertAlmostEqual(factor, expected_factor)

        # s = 6.1
        factor = self.scatter.get(14, 1.0 / (2 * 6.1))
        expected_factor = 0.10091802161492447
        self.assertAlmostEqual(factor, expected_factor)

        ## Copper
        # s = 0.5
        factor = self.scatter.get(29, 1.0)
        expected_factor = 13.70070197002754
        self.assertAlmostEqual(factor, expected_factor)

        # s = 3.0
        factor = self.scatter.get(29, 1.0 / 6.0)
        expected_factor = 2.0104488387433492
        self.assertAlmostEqual(factor, expected_factor)

        # s = 6.1
        factor = self.scatter.get(29, 1.0 / (2 * 6.1))
        expected_factor = 0.9191770170219552
        self.assertAlmostEqual(factor, expected_factor)

        ## Gold
        # s = 0.5
        factor = self.scatter.get(79, 1.0)
        expected_factor = 46.906655657698153
        self.assertAlmostEqual(factor, expected_factor)

        # s = 3.0
        factor = self.scatter.get(79, 1.0 / 6.0)
        expected_factor = 9.7301060945727169
        self.assertAlmostEqual(factor, expected_factor)

        # s = 6.1
        factor = self.scatter.get(79, 1.0 / (2 * 6.1))
        expected_factor = 4.2485964205405162
        self.assertAlmostEqual(factor, expected_factor)

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
