#!/usr/bin/env python
"""
================================================================================
:mod:`test_comparison` -- Unit tests for the module :mod:`comparison`.
================================================================================

"""

# Script information for the file.
__author__ = "Philippe Pinard <philippe.pinard@mail.mcgill.ca>"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2009 Philippe Pinard"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = ""
__svnDate__ = ""
__svnId__ = ""

# Standard library modules.
import unittest
import logging

# Third party modules.
import numpy as np

# Local modules.
import comparison

# Globals and constants variables.

class TestComparison(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.s = np.array([210, 218, 212, 216])
        self.s1 = np.array([16.85, 16.40, 17.21, 16.35, 16.52, 17.04, 16.96,
                            17.15, 16.59, 16.57])
        self.s2 = np.array([16.62, 16.75, 17.37, 17.12, 16.98, 16.87, 17.34,
                            17.02, 17.08, 17.27])

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        #self.fail("Test if the TestCase is working.")
        self.assert_(True)

        self.assertAlmostEqual(214.0, np.mean(self.s), 6)
        self.assertAlmostEqual(16.76, np.mean(self.s1), 2)
        self.assertAlmostEqual(17.04, np.mean(self.s2), 2)

    def testnormal_probability_plot(self):
        pass

    def testztest_onesample(self):
        # From Montgomery, Example 2.1
        # Tested with MiniTab

        # H1: mu != 200
        rejected, z, p, (lower, upper) = \
          comparison.ztest_onesample(self.s, 200, 100, alternative="!=", ci=0.95)
        self.assertTrue(rejected)
        self.assertAlmostEqual(2.80, z, 2)
        self.assertAlmostEqual(0.005, p, 3)
        self.assertAlmostEqual(204.20, lower, 2)
        self.assertAlmostEqual(223.80, upper, 2)

        # H1: mu < 200
        rejected, z, p, (lower, upper) = \
          comparison.ztest_onesample(self.s, 200, 100, alternative="<", ci=0.95)
        self.assertFalse(rejected)
        self.assertAlmostEqual(2.80, z, 2)
        self.assertAlmostEqual(0.997, p, 3)
        self.assertAlmostEqual(222.22, lower, 2)
        self.assertEqual(float("inf"), upper)

        # H1: mu > 200
        rejected, z, p, (lower, upper) = \
          comparison.ztest_onesample(self.s, 200, 100, alternative=">", ci=0.95)
        self.assertTrue(rejected)
        self.assertAlmostEqual(2.80, z, 2)
        self.assertAlmostEqual(0.00256, p, 5)
        self.assertEqual(float("-inf"), lower)
        self.assertAlmostEqual(205.78, upper, 2)

    def testztest_twosamples(self):
        pass

    def testttest_onesample(self):
        # Tested with MiniTab

        # H1: mu1 != 200
        rejected, t, p, (lower, upper) = \
          comparison.ttest_onesample(self.s, 200, alternative="!=", ci=0.95)
        self.assertTrue(rejected)
        self.assertAlmostEqual(7.67, t, 2)
        self.assertAlmostEqual(0.005, p, 3)
        self.assertAlmostEqual(208.19, lower, 2)
        self.assertAlmostEqual(219.81, upper, 2)

        # H1: mu1 < 200
        rejected, t, p, (lower, upper) = \
          comparison.ttest_onesample(self.s, 200, alternative="<", ci=0.95)
        self.assertFalse(rejected)
        self.assertAlmostEqual(7.67, t, 2)
        self.assertAlmostEqual(0.998, p, 3)
        self.assertAlmostEqual(218.30, lower, 2)
        self.assertEqual(float("inf"), upper)

        # H1: mu1 > 200
        rejected, t, p, (lower, upper) = \
          comparison.ttest_onesample(self.s, 200, alternative=">", ci=0.95)
        self.assertTrue(rejected)
        self.assertAlmostEqual(7.67, t, 2)
        self.assertAlmostEqual(0.002, p, 3)
        self.assertEqual(float("-inf"), lower)
        self.assertAlmostEqual(209.70, upper, 2)

    def testttest_twosamples(self):
        # From Montgomery, Table 2.2
        # Tested with MiniTab

        # H1: mu1 != mu2 (sigma1 != sigma2)
        rejected, t, p, (lower, upper) = \
          comparison.ttest_twosamples(self.s1, self.s2, alternative="!=", ci=0.95,
                                      equal_var=False)
        self.assertTrue(rejected)
        self.assertAlmostEqual(-2.19, t, 2)
        self.assertAlmostEqual(0.043, p, 3)
        self.assertAlmostEqual(-0.546, lower, 3)
        self.assertAlmostEqual(-0.010, upper, 3)

        # H1: mu1 < mu2 (sigma1 != sigma2)
        rejected, t, p, (lower, upper) = \
          comparison.ttest_twosamples(self.s1, self.s2, alternative="<", ci=0.95,
                                      equal_var=False)
        self.assertTrue(rejected)
        self.assertAlmostEqual(-2.19, t, 2)
        self.assertAlmostEqual(0.0215, p, 3)
        self.assertAlmostEqual(-0.057, lower, 3)
        self.assertEqual(float("inf"), upper)

        # H1: mu1 > mu2 (sigma1 != sigma2)
        rejected, t, p, (lower, upper) = \
          comparison.ttest_twosamples(self.s1, self.s2, alternative=">", ci=0.95,
                                      equal_var=False)
        self.assertFalse(rejected)
        self.assertAlmostEqual(-2.19, t, 2)
        self.assertAlmostEqual(0.9785, p, 3)
        self.assertEqual(float("-inf"), lower)
        self.assertAlmostEqual(-0.499, upper, 3)

        # H1: mu1 != mu2 (sigma1 == sigma2)
        rejected, t, p, (lower, upper) = \
          comparison.ttest_twosamples(self.s1, self.s2, alternative="!=", ci=0.95,
                                      equal_var=True)
        self.assertTrue(rejected)
        self.assertAlmostEqual(-2.19, t, 2)
        self.assertAlmostEqual(0.042, p, 3)
        self.assertAlmostEqual(-0.545, lower, 3)
        self.assertAlmostEqual(-0.011, upper, 3)

        # H1: mu1 < mu2 (sigma1 == sigma2)
        rejected, t, p, (lower, upper) = \
          comparison.ttest_twosamples(self.s1, self.s2, alternative="<", ci=0.95,
                                      equal_var=True)
        self.assertTrue(rejected)
        self.assertAlmostEqual(-2.19, t, 2)
        self.assertAlmostEqual(0.021, p, 3)
        self.assertAlmostEqual(-0.058, lower, 3)
        self.assertEqual(float("inf"), upper)

        # H1: mu1 > mu2 (sigma1 == sigma2)
        rejected, t, p, (lower, upper) = \
          comparison.ttest_twosamples(self.s1, self.s2, alternative=">", ci=0.95,
                                      equal_var=True)
        self.assertFalse(rejected)
        self.assertAlmostEqual(-2.19, t, 2)
        self.assertAlmostEqual(0.979, p, 3)
        self.assertEqual(float("-inf"), lower)
        self.assertAlmostEqual(-0.498, upper, 3)

    def testchisquare_onesample(self):
        # Tested with MiniTab

        # H1: sigma != 20
        rejected, x0, p, (lower, upper) = \
          comparison.chisquare_onesample(self.s, 20, alternative="!=", ci=0.95)
        self.assertFalse(rejected)
        self.assertAlmostEqual(2.0, x0, 2)
        self.assertAlmostEqual(0.855, p, 3)
        self.assertAlmostEqual(4.3, lower, 1)
        self.assertAlmostEqual(185.4, upper, 1)

        # H1: sigma < 20
        rejected, x0, p, (lower, upper) = \
          comparison.chisquare_onesample(self.s, 20, alternative="<", ci=0.95)
        self.assertFalse(rejected)
        self.assertAlmostEqual(2.0, x0, 2)
        self.assertAlmostEqual(0.428, p, 3)
        self.assertAlmostEqual(113.7, lower, 1)
        self.assertEqual(float("inf"), upper)

        # H1: sigma > 20
        rejected, x0, p, (lower, upper) = \
          comparison.chisquare_onesample(self.s, 20, alternative=">", ci=0.95)
        self.assertFalse(rejected)
        self.assertAlmostEqual(2.0, x0, 2)
        self.assertAlmostEqual(0.572, p, 3)
        self.assertEqual(float("-inf"), lower)
        self.assertAlmostEqual(5.1, upper, 1)

    def testftest_twosamples(self):
        # Tested with MiniTab

        # H1: sigma1 != sigma2
        rejected, f0, p = comparison.ftest_twosamples(self.s1, self.s2,
                                                      alternative="!=", ci=0.95)
        self.assertFalse(rejected)
        self.assertAlmostEqual(1.63, f0, 2)
        self.assertAlmostEqual(0.478, p, 3)

        # H1: sigma1 < sigma2 (not tested with MiniTab)
        rejected, f0, p = comparison.ftest_twosamples(self.s1, self.s2,
                                                      alternative="<", ci=0.95)
        self.assertFalse(rejected)
        self.assertAlmostEqual(1.63, f0, 2)
        self.assertAlmostEqual(0.761, p, 3)

        # H1: sigma1 > sigma2 (not tested with MiniTab)
        rejected, f0, p = comparison.ftest_twosamples(self.s1, self.s2,
                                                      alternative=">", ci=0.95)
        self.assertFalse(rejected)
        self.assertAlmostEqual(1.63, f0, 2)
        self.assertAlmostEqual(0.239, p, 3)

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
