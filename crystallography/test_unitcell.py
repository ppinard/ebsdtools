#!/usr/bin/env python
"""
================================================================================
:mod:`test_unitcell` -- Unit tests for the module :mod:`unitcell`.
================================================================================

.. module:: test_unitcell
   :synopsis: Unit tests for the module :mod:`unitcell`.

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
from math import pi, sqrt, sin

# Third party modules.

# Local modules.
import ebsdtools.crystallography.unitcell as unitcell
import mathtools.rotation.matrices as matrices

# Globals and constants variables.

class TestUnitCell(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)

        self.cubic = unitcell.create_cubic_unitcell(2)
        self.tetragonal = unitcell.create_tetragonal_unitcell(2, 3)
        self.orthorhombic = unitcell.create_orthorhombic_unitcell(1, 2, 3)
        self.trigonal = unitcell.create_trigonal_unitcell(2, 35.0 / 180 * pi)
        self.hexagonal = unitcell.create_hexagonal_unitcell(2, 3)
        self.monoclinic = unitcell.create_monoclinic_unitcell(1, 2, 3, 55.0 / 180 * pi)
        self.triclinic = \
            unitcell.create_triclinic_unitcell(1, 2, 3,
                                               75.0 / 180 * pi, 55.0 / 180 * pi, 35.0 / 180 * pi)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        #    self.fail("Test if the testcase is working.")
        self.assert_(True)

    def testcubic(self):
        self.assertAlmostEqual(self.cubic.a, 2.0)
        self.assertAlmostEqual(self.cubic.b, 2.0)
        self.assertAlmostEqual(self.cubic.c, 2.0)
        self.assertAlmostEqual(self.cubic.a_, 0.5)
        self.assertAlmostEqual(self.cubic.b_, 0.5)
        self.assertAlmostEqual(self.cubic.c_, 0.5)
        self.assertAlmostEqual(self.cubic.alpha, pi / 2)
        self.assertAlmostEqual(self.cubic.beta, pi / 2)
        self.assertAlmostEqual(self.cubic.gamma, pi / 2)
        self.assertAlmostEqual(self.cubic.alpha_, pi / 2)
        self.assertAlmostEqual(self.cubic.beta_, pi / 2)
        self.assertAlmostEqual(self.cubic.gamma_, pi / 2)
        self.assertAlmostEqual(self.cubic.volume, 8.0)
        self.assertAlmostEqual(self.cubic.volume_, 0.125)

        self.assertAlmostEqual(self.cubic.a_, 1.0 / 2.0)
        self.assertAlmostEqual(self.cubic.b_, 1.0 / 2.0)
        self.assertAlmostEqual(self.cubic.c_, 1.0 / 2.0)
        self.assertAlmostEqual(self.cubic.volume, 2.0 ** 3)

        self.assertEqual(self.cubic.crystalsystem, unitcell.CUBIC)

    def testtetragonal(self):
        self.assertAlmostEqual(self.tetragonal.a, 2.0)
        self.assertAlmostEqual(self.tetragonal.b, 2.0)
        self.assertAlmostEqual(self.tetragonal.c, 3.0)
        self.assertAlmostEqual(self.tetragonal.a_, 0.5)
        self.assertAlmostEqual(self.tetragonal.b_, 0.5)
        self.assertAlmostEqual(self.tetragonal.c_, 0.333333333)
        self.assertAlmostEqual(self.tetragonal.alpha, pi / 2)
        self.assertAlmostEqual(self.tetragonal.beta, pi / 2)
        self.assertAlmostEqual(self.tetragonal.gamma, pi / 2)
        self.assertAlmostEqual(self.tetragonal.alpha_, pi / 2)
        self.assertAlmostEqual(self.tetragonal.beta_, pi / 2)
        self.assertAlmostEqual(self.tetragonal.gamma_, pi / 2)
        self.assertAlmostEqual(self.tetragonal.volume, 12.0)
        self.assertAlmostEqual(self.tetragonal.volume_, 0.083333333)

        self.assertAlmostEqual(self.tetragonal.a_, 1.0 / 2.0)
        self.assertAlmostEqual(self.tetragonal.b_, 1.0 / 2.0)
        self.assertAlmostEqual(self.tetragonal.c_, 1.0 / 3.0)
        self.assertAlmostEqual(self.tetragonal.volume, 2.0 ** 2 * 3.0)

        self.assertEqual(self.tetragonal.crystalsystem, unitcell.TETRAGONAL)

    def testorthorhombic(self):
        self.assertAlmostEqual(self.orthorhombic.a, 1.0)
        self.assertAlmostEqual(self.orthorhombic.b, 2.0)
        self.assertAlmostEqual(self.orthorhombic.c, 3.0)
        self.assertAlmostEqual(self.orthorhombic.a_, 1.0)
        self.assertAlmostEqual(self.orthorhombic.b_, 0.5)
        self.assertAlmostEqual(self.orthorhombic.c_, 0.33333333)
        self.assertAlmostEqual(self.orthorhombic.alpha, pi / 2)
        self.assertAlmostEqual(self.orthorhombic.beta, pi / 2)
        self.assertAlmostEqual(self.orthorhombic.gamma, pi / 2)
        self.assertAlmostEqual(self.orthorhombic.alpha_, pi / 2)
        self.assertAlmostEqual(self.orthorhombic.beta_, pi / 2)
        self.assertAlmostEqual(self.orthorhombic.gamma_, pi / 2)
        self.assertAlmostEqual(self.orthorhombic.volume, 6.0)
        self.assertAlmostEqual(self.orthorhombic.volume_, 0.166666666)

        self.assertAlmostEqual(self.orthorhombic.a_, 1.0 / 1.0)
        self.assertAlmostEqual(self.orthorhombic.b_, 1.0 / 2.0)
        self.assertAlmostEqual(self.orthorhombic.c_, 1.0 / 3.0)
        self.assertAlmostEqual(self.orthorhombic.volume, 1.0 * 2.0 * 3.0)

        self.assertEqual(self.orthorhombic.crystalsystem, unitcell.ORTHORHOMBIC)

    def testtrigonal(self):
        self.assertAlmostEqual(self.trigonal.a, 2.0)
        self.assertAlmostEqual(self.trigonal.b, 2.0)
        self.assertAlmostEqual(self.trigonal.c, 2.0)
        self.assertAlmostEqual(self.trigonal.a_, 0.9763044673403796)
        self.assertAlmostEqual(self.trigonal.b_, 0.9763044673403796)
        self.assertAlmostEqual(self.trigonal.c_, 0.9763044673403796)
        self.assertAlmostEqual(self.trigonal.alpha, 35.0 / 180 * pi)
        self.assertAlmostEqual(self.trigonal.beta, 35.0 / 180 * pi)
        self.assertAlmostEqual(self.trigonal.gamma, 35.0 / 180 * pi)
        self.assertAlmostEqual(self.trigonal.alpha_, 2.0378901672656156)
        self.assertAlmostEqual(self.trigonal.beta_, 2.0378901672656156)
        self.assertAlmostEqual(self.trigonal.gamma_, 2.0378901672656156)
        self.assertAlmostEqual(self.trigonal.volume, 2.349990010446501)
        self.assertAlmostEqual(self.trigonal.volume_, 0.42553372378378695)

        self.assertEqual(self.trigonal.crystalsystem, unitcell.TRIGONAL)

    def testhexagonal(self):
        self.assertAlmostEqual(self.hexagonal.a, 2.0)
        self.assertAlmostEqual(self.hexagonal.b, 2.0)
        self.assertAlmostEqual(self.hexagonal.c, 3.0)
        self.assertAlmostEqual(self.hexagonal.a_, 0.5773502691896257)
        self.assertAlmostEqual(self.hexagonal.b_, 0.5773502691896257)
        self.assertAlmostEqual(self.hexagonal.c_, 0.333333333)
        self.assertAlmostEqual(self.hexagonal.alpha, pi / 2)
        self.assertAlmostEqual(self.hexagonal.beta, pi / 2)
        self.assertAlmostEqual(self.hexagonal.gamma, 120.0 / 180 * pi)
        self.assertAlmostEqual(self.hexagonal.alpha_, pi / 2)
        self.assertAlmostEqual(self.hexagonal.beta_, pi / 2)
        self.assertAlmostEqual(self.hexagonal.gamma_, 60.0 / 180 * pi)
        self.assertAlmostEqual(self.hexagonal.volume, 10.392304845413264)
        self.assertAlmostEqual(self.hexagonal.volume_, 0.09622504486493763)

        self.assertAlmostEqual(self.hexagonal.a_, 2.0 / 3.0 * sqrt(3) / 2.0)
        self.assertAlmostEqual(self.hexagonal.b_, 2.0 / 3.0 * sqrt(3) / 2.0)
        self.assertAlmostEqual(self.hexagonal.c_, 1.0 / 3.0)
        self.assertAlmostEqual(self.hexagonal.volume, 0.5 * sqrt(3) * 2.0 ** 2 * 3.0)

        self.assertEqual(self.hexagonal.crystalsystem, unitcell.HEXAGONAL)

    def testmonoclinic(self):
        self.assertAlmostEqual(self.monoclinic.a, 1.0)
        self.assertAlmostEqual(self.monoclinic.b, 2.0)
        self.assertAlmostEqual(self.monoclinic.c, 3.0)
        self.assertAlmostEqual(self.monoclinic.a_, 1.220774588761456)
        self.assertAlmostEqual(self.monoclinic.b_, 0.5)
        self.assertAlmostEqual(self.monoclinic.c_, 0.40692486292048535)
        self.assertAlmostEqual(self.monoclinic.alpha, pi / 2)
        self.assertAlmostEqual(self.monoclinic.beta, 55.0 / 180 * pi)
        self.assertAlmostEqual(self.monoclinic.gamma, pi / 2)
        self.assertAlmostEqual(self.monoclinic.alpha_, pi / 2)
        self.assertAlmostEqual(self.monoclinic.beta_, 125.0 / 180 * pi)
        self.assertAlmostEqual(self.monoclinic.gamma_, pi / 2)
        self.assertAlmostEqual(self.monoclinic.volume, 4.914912265733951)
        self.assertAlmostEqual(self.monoclinic.volume_, 0.20346243146024268)

        self.assertAlmostEqual(self.monoclinic.a_,
                               1.0 / (1 * sin(125.0 / 180 * pi)))
        self.assertAlmostEqual(self.monoclinic.b_, 1.0 / 2.0)
        self.assertAlmostEqual(self.monoclinic.c_,
                               1.0 / (3 * sin(125.0 / 180 * pi)))
        self.assertAlmostEqual(self.monoclinic.volume,
                               1.0 * 2.0 * 3.0 * sin(125.0 / 180 * pi))

        self.assertEqual(self.monoclinic.crystalsystem, unitcell.MONOCLINIC)

    def testtriclinic(self):
        self.assertAlmostEqual(self.triclinic.a, 1.0)
        self.assertAlmostEqual(self.triclinic.b, 2.0)
        self.assertAlmostEqual(self.triclinic.c, 3.0)
        self.assertAlmostEqual(self.triclinic.a_, 2.3009777700230383)
        self.assertAlmostEqual(self.triclinic.b_, 0.9756704877739889)
        self.assertAlmostEqual(self.triclinic.c_, 0.45544788689872767)
        self.assertAlmostEqual(self.triclinic.alpha, 75.0 / 180 * pi)
        self.assertAlmostEqual(self.triclinic.beta, 55.0 / 180 * pi)
        self.assertAlmostEqual(self.triclinic.gamma, 35.0 / 180 * pi)
        self.assertAlmostEqual(self.triclinic.alpha_, 1.1049925940211875)
        self.assertAlmostEqual(self.triclinic.beta_, 2.281813838221562)
        self.assertAlmostEqual(self.triclinic.gamma_, 2.582348070021294)
        self.assertAlmostEqual(self.triclinic.volume, 2.518735744968272)
        self.assertAlmostEqual(self.triclinic.volume_, 0.3970245794929935)

        self.assertEqual(self.triclinic.crystalsystem, unitcell.TRICLINIC)

    def testmetricalmatrix(self):
        # Example from Mathematical Crystallography
        L = unitcell.create_hexagonal_unitcell(4.914, 5.409)

        metricalmatrix = L.metricalmatrix
        expected_metricalmatrix = matrices.Matrix3D([24.1474, -12.0737, 0.0],
                                                    [-12.0737, 24.1474, 0.0],
                                                    [0.0, 0.0, 29.2573])
        self.assertTrue(matrices.almostequal(metricalmatrix,
                                             expected_metricalmatrix, 4))

    def testcartesianmatrix(self):
        alpha = 93.11 / 180.0 * pi
        beta = 115.91 / 180.0 * pi
        gamma = 91.26 / 180.0 * pi
        L = unitcell.create_triclinic_unitcell(8.173, 12.869, 14.165,
                                               alpha, beta, gamma)

        cartesianmatrix = L.cartesianmatrix
        expected_cartesianmatrix = matrices.Matrix3D([7.3513, -0.65437, 0.0],
                                                     [0.0, 12.8333, 0.0],
                                                     [-3.5716, -0.69886, 14.165])
        self.assertTrue(matrices.almostequal(cartesianmatrix,
                                             expected_cartesianmatrix, 2))

        # Identity G = A^T A
        g = matrices.transpose(cartesianmatrix) * cartesianmatrix
        self.assertTrue(matrices.almostequal(g, L.metricalmatrix, 4))


if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.INFO)
    unittest.main()
