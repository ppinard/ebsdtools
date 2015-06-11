#!/usr/bin/env python
"""
================================================================================
:mod:`test_matrices` -- Unit tests for the module :mod:`matrices`.
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
from math import sqrt
import copy
try:
    import numpy
except ImportError:
    numpy = None

# Third party modules.

# Local modules.
import mathtools.rotation.matrices as matrices
import mathtools.algebra.vectors as vectors

# Globals and constants variables.
REPETITIONS = 100

class TestMatrix3D(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.m1 = matrices.Matrix3D([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        self.m2 = matrices.Matrix3D([1, 2, 3], [4, 5, 6], [7, 8, 9])
        self.m3 = matrices.Matrix3D(1, 2, 3, 4, 5, 6, 7, 8, 9)
        self.m4 = matrices.Matrix3D(2, 2, 2, 3, 3, 3, 4, 4, 4)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        #self.fail("Test if the TestCase is working.")
        self.assert_(True)

    def test__getitem__(self):
        for i in range(3):
            for j in range(3):
                value = (i * 3) + (j + 1)
                self.assertEqual(self.m1[i][j], value)
                self.assertEqual(self.m2[i][j], value)
                self.assertEqual(self.m3[i][j], value)

    def test__setitem__(self):
        m = matrices.Matrix3D(9, 2, 3, 4, 9, 6, 7, 8, 9)
        self.m1[0][0] = 9
        self.m1[1][1] = 9
        self.m1[2][2] = 9

        for i in range(3):
            for j in range(3):
                self.assertEqual(self.m1[i][j], m[i][j])

    def test__repr__(self):
        expected_str = '1.000000, 2.000000, 3.000000\n4.000000, 5.000000, 6.000000\n7.000000, 8.000000, 9.000000'
        self.assertEqual(str(self.m1), expected_str)

    def test__mul__(self):
        if numpy is not None:
            m1np = numpy.array(self.m1.to_list())
            m2np = numpy.array(self.m2.to_list())

            # Matrix multiplication
            mm = self.m1 * self.m2
            mmnp = numpy.dot(m1np, m2np)

            for i in range(3):
                for j in range(3):
                    self.assertAlmostEqual(mm[i][j], mmnp[i][j])

            # Scalar multiplication
            mm = self.m1 * 4
            mmnp = m1np * 4

            for i in range(3):
                for j in range(3):
                    self.assertAlmostEqual(mm[i][j], mmnp[i][j])

            # Vector multiplication
            v1 = vectors.Vector3D(1, 1, 1)
            v1np = numpy.array([1, 1, 1])

            vv = self.m1 * v1
            vvnp = numpy.dot(m1np, v1np)

            for i in range(3):
                self.assertAlmostEqual(vv[i], vvnp[i])

    def test__rmul__(self):
        self.assertEqual(self.m1 * 4, 4 * self.m1)
        self.assertNotEqual(self.m1 * self.m4, self.m4 * self.m1)

        if numpy is not None:
            m1np = numpy.array(self.m1.to_list())
            m2np = numpy.array(self.m2.to_list())

            #Matrix multiplication
            mm = self.m2 * self.m1
            mmnp = numpy.dot(m2np, m1np)

            for i in range(3):
                for j in range(3):
                    self.assertAlmostEqual(mm[i][j], mmnp[i][j])

            #Scalar multiplication
            mm = 4 * self.m1
            mmnp = 4 * m1np

            for i in range(3):
                for j in range(3):
                    self.assertAlmostEqual(mm[i][j], mmnp[i][j])

    def test__eq__(self):
        self.assertTrue(self.m1 == self.m2)
        self.assertTrue(self.m1 == self.m3)
        self.assertTrue(self.m2 == self.m3)

    def test__ne__(self):
        self.assertTrue(self.m1 != self.m4)

    def testto_list(self):
        expected_list = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        self.assertEqual(self.m1.to_list(), expected_list)

    def testtranspose(self):
        m1 = copy.deepcopy(self.m1)
        m1.transpose()
        self.assertEqual(m1, matrices.transpose(self.m1))

class TestSpecialOrthogonalMatrix3D(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.m1 = matrices.SpecialOrthogonalMatrix3D(1, 0, 0, 0, sqrt(3) / 2, 1.0 / 2, 0, -1.0 / 2, sqrt(3) / 2)
        self.m2 = matrices.SpecialOrthogonalMatrix3D(0.36, 0.48, -0.8, -0.8, 0.6, 0, 0.48, 0.64, 0.6)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        #self.fail("Test if the TestCase is working.")
        self.assert_(True)

    def testconstructor(self):
        # Example of a matrix with a determinant of 1,
        # but that the inverse is not equal to the transpose
        m = matrices.Matrix3D(3, -4, 1, 5, 3, -7, -9, 2, 6)
        self.assertEqual(matrices.det(m), 1)
        self.assertRaises(TypeError, matrices.SpecialOrthogonalMatrix3D, m.to_list())

    def test__mul__(self):
        mm = self.m1 * self.m2
        self.assertTrue(isinstance(mm, matrices.SpecialOrthogonalMatrix3D))

        mm = self.m1 * 4
        self.assertFalse(isinstance(mm, matrices.SpecialOrthogonalMatrix3D))
        self.assertTrue(isinstance(mm, matrices.Matrix3D))

        mm = self.m1 * 1.0
        self.assertTrue(isinstance(mm, matrices.SpecialOrthogonalMatrix3D))

        # If a special orthogonal matrix is multiplied with a regular matrix,
        # the results is a regular Matrix3D object.
        m = matrices.Matrix3D(1, 2, 3, 4, 5, 6, 7, 8, 9)
        mm = self.m1 * m
        self.assertFalse(isinstance(mm, matrices.SpecialOrthogonalMatrix3D))
        self.assertTrue(isinstance(mm, matrices.Matrix3D))

    def test__rmul__(self):
        mm = self.m2 * self.m1
        self.assertTrue(isinstance(mm, matrices.SpecialOrthogonalMatrix3D))

        mm = 4 * self.m1
        self.assertFalse(isinstance(mm, matrices.SpecialOrthogonalMatrix3D))
        self.assertTrue(isinstance(mm, matrices.Matrix3D))

        mm = 1.0 * self.m1
        self.assertTrue(isinstance(mm, matrices.SpecialOrthogonalMatrix3D))

        # If a special orthogonal matrix is multiplied with a regular matrix,
        # the results is a regular Matrix3D object.
        m = matrices.Matrix3D(1, 2, 3, 4, 5, 6, 7, 8, 9)
        mm = m * self.m1
        self.assertFalse(isinstance(mm, matrices.SpecialOrthogonalMatrix3D))
        self.assertTrue(isinstance(mm, matrices.Matrix3D))

class TestMatrices(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.m1 = matrices.Matrix3D(1, 2, 3, 0, 1, 4, 5, 6, 0)
        self.m_so3 = matrices.Matrix3D(0.36, 0.48, -0.8, -0.8, 0.6, 0, 0.48, 0.64, 0.6)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        #self.fail("Test if the TestCase is working.")
        self.assert_(True)

    def testdet(self):
        self.assertEqual(matrices.det(self.m1), 1.0)

        if numpy is not None:
            for _k in range(REPETITIONS):
                m = []
                for _i in range(3):
                    r = []
                    for _j in range(3):
                        r.append(random.random())
                    m.append(r)

                m_ = numpy.array(m)

                self.assertAlmostEqual(numpy.linalg.det(m_), matrices.det(matrices.Matrix3D(m)))

    def testtranspose(self):
        expected_m1_transpose = matrices.Matrix3D(1, 0, 5, 2, 1, 6, 3, 4, 0)
        m1_transpose = matrices.transpose(self.m1)
        self.assertEqual(expected_m1_transpose, m1_transpose)

    def testinverse(self):
        expected_m1_inverse = matrices.Matrix3D(-24, 18, 5, 20, -15, -4, -5, 4, 1)
        m1_inverse = matrices.inverse(self.m1)
        self.assertEqual(expected_m1_inverse, m1_inverse)

    def testtrace(self):
        trace = matrices.trace(self.m1)
        self.assertEqual(trace, 2)

    def testalmostequal(self):
        m = matrices.Matrix3D(1, 2, 3, 0, 1, 4, 5, 6, 1)
        self.assertFalse(matrices.almostequal(self.m1, m))

        m = matrices.Matrix3D(1, 2, 3, 0, 1, 4, 5, 6, 0.0000000001)
        self.assertTrue(matrices.almostequal(self.m1, m))
        self.assertTrue(matrices.almostequal(m, self.m1))

    def testis_special_orthogonal(self):
        self.assertFalse(matrices.is_special_orthogonal(self.m1))
        self.assertTrue(matrices.is_special_orthogonal(self.m_so3))

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
