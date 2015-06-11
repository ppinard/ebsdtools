#!/usr/bin/env python
"""
================================================================================
:mod:`test_vectors` -- Unit tests for the module :mod:`vectors`.
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
import copy
from math import sqrt

# Third party modules.

# Local modules.
import mathtools.algebra.vectors as vectors

# Globals and constants variables.

class TestVector(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.u = vectors.Vector(1, 2, 3)
        self.v = vectors.Vector([4, 5, 6])
        self.w = vectors.Vector(1, 0, 0)
        self.x = vectors.Vector(1, 0, 0, 0, -5, 6)
        self.y = vectors.Vector([1, 2, 3, 4])
        self.z = vectors.Vector(8, 9)
        self.a = vectors.Vector(-1, -2, 3)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        #self.fail("Test if the TestCase is working.")
        self.assert_(True)

    def test__lt__(self):
        self.assertTrue(self.u < self.v)
        self.assertTrue(self.u < self.x)
        self.assertTrue(not self.u < self.w)
        self.assertTrue(self.z < self.u)

    def test__le__(self):
        self.assertTrue(self.u <= self.u)
        self.assertTrue(self.u <= self.v)

    def test__gt__(self):
        self.assertTrue(self.x > self.u)
        self.assertTrue(self.x > self.v)
        self.assertTrue(not self.w > self.u)

    def test__ge__(self):
        self.assertTrue(self.x >= self.x)
        self.assertTrue(self.x >= self.u)

    def test__eq__(self):
        self.assertTrue(self.u == self.u)
        self.assertTrue(self.x == self.x)
        self.assertTrue(not self.u == self.v)

    def test__ne__(self):
        self.assertTrue(not self.u != self.u)
        self.assertTrue(not self.x != self.x)
        self.assertTrue(self.u != self.v)

    def test__repr__(self):
        self.assertEqual(str(self.u), '[1, 2, 3]')
        self.assertEqual(str(self.v), '[4, 5, 6]')
        self.assertEqual(str(self.x), '[1, 0, 0, 0, -5, 6]')

    def test__getslice__(self):
        self.assertEqual(self.u[1:], vectors.Vector(2, 3))
        self.assertEqual(self.v[-2:], vectors.Vector(5, 6))
        self.assertEqual(self.y[2:-1], vectors.Vector(3))
        self.assertEqual(self.z[:], vectors.Vector(8, 9))

    def test_getitem__(self):
        self.assertEqual(self.u[2], 3)
        self.assertEqual(self.v[2], 6)
        self.assertEqual(self.w[2], 0)
        self.assertEqual(self.y[2], 3)

    def test__setitem__(self):
        self.u[0] = 99
        self.v[0] = 99
        self.z[0] = 99
        self.assertEqual(self.u[0], 99)
        self.assertEqual(self.v[0], 99)
        self.assertEqual(self.z[0], 99)

    def test__delitem__(self):
        del self.u[1]
        del self.x[1]
        del self.x[1]

        self.assertEqual(len(self.u), 2)
        self.assertEqual(self.u, vectors.Vector(1, 3))
        self.assertEqual(len(self.x), 4)
        self.assertEqual(self.x, vectors.Vector(1, 0, -5, 6))

    def test__add__(self):
        self.assertEqual(self.u + self.w, vectors.Vector(2, 2, 3))
        self.assertEqual(self.u + self.v, self.v + self.u)

        func = lambda a, b: a + b
        self.assertRaises(vectors.VectorOperationError, func, self.x, self.u)

    def test__neg__(self):
        self.assertEqual(-self.u, vectors.Vector(-1, -2, -3))
        self.assertEqual(-self.x, vectors.Vector(-1, 0, 0, 0, 5, -6))

    def test__sub__(self):
        self.assertEqual(self.v - self.u, vectors.Vector(3, 3, 3))
        self.assertEqual(self.v - self.u, self.v + -self.u)
        self.assertNotEqual(self.v - self.u, self.u - self.v)

        func = lambda a, b: a - b
        self.assertRaises(vectors.VectorOperationError, func, self.x, self.u)

    def test__mul__(self):
        self.assertEqual(2 * self.u, vectors.Vector(2, 4, 6))
        self.assertEqual(2 * self.w, vectors.Vector(2, 0, 0))
        self.assertEqual(2 * self.u, self.u * 2)

    #TODO: Test vector multiplication

    def test__div__(self):
        self.assertEqual(self.u / 2.0, 0.5 * self.u)
        self.assertEqual(self.v / 3.0, 1 / 3.0 * self.v)

        func = lambda a, b: a / b
        self.assertRaises(TypeError, func, self.x, self.u)

    def test__len__(self):
        self.assertEqual(len(self.u), 3)
        self.assertEqual(len(self.x), 6)
        self.assertEqual(len(self.y), 4)
        self.assertEqual(len(self.z), 2)

    def testnorm(self):
        self.assertEqual(self.u.norm(), sqrt(1 ** 2 + 2 ** 2 + 3 ** 2))
        self.assertEqual(self.x.norm(), sqrt(1 ** 2 + 5 ** 2 + 6 ** 2))

    def testnormalize(self):
        w = copy.deepcopy(self.w)
        w.normalize()
        self.assertEqual(w, self.w)

        u = copy.deepcopy(self.u)
        u.normalize()
        self.assertEqual(u, self.u / self.u.norm())

    def testpositive(self):
        w = copy.deepcopy(self.w)
        w.positive()
        self.assertEqual(w, self.w)

        a = copy.deepcopy(self.a)
        a.positive()
        self.assertEqual(a, vectors.Vector(1, 2, -3))
        self.assertEqual(self.a, vectors.Vector(-1, -2, 3))

class TestVector3D(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.u = vectors.Vector3D(1, 2, 3)
        self.v = vectors.Vector3D([4, 5, 6])
        self.w = vectors.Vector3D(1, 0, 0)
        self.a = vectors.Vector3D(-1, -2, 3)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        #self.fail("Test if the TestCase is working.")
        self.assert_(True)

    def testconstructor(self):
        self.assertRaises(ValueError, vectors.Vector3D, 1, 0, 0, 0, -5 , 6)
        self.assertRaises(ValueError, vectors.Vector3D, [1, 2, 3, 4])
        self.assertRaises(ValueError, vectors.Vector3D, 8, 9)
        self.assertRaises(ValueError, vectors.Vector3D)

    def testnormalize(self):
        u = copy.deepcopy(self.u)
        u.normalize()
        self.assertEqual(u, self.u / self.u.norm())
        self.assertTrue(isinstance(u, vectors.Vector3D))

class TestVectors(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.u = vectors.Vector3D(1, 2, 3)
        self.v = vectors.Vector3D([4, 5, 6])
        self.w = vectors.Vector(1, 0, 0)
        self.x = vectors.Vector(1, 0, 0, 0, -5, 6)
        self.a = vectors.Vector(-1, -2, 3)
        self.b = vectors.Vector(0, 0, -1, -2, 3)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        #self.fail("Test if the TestCase is working.")
        self.assert_(True)

    def testnormalize(self):
        self.assertEqual(vectors.normalize(self.w), self.w)
        self.assertEqual(vectors.normalize(self.u), self.u / self.u.norm())

    def testpositive(self):
        self.assertEqual(vectors.positive(self.a), vectors.Vector(1, 2, -3))
        self.assertEqual(vectors.positive(self.b), vectors.Vector(0, 0, 1, 2, -3))
        self.assertEqual(vectors.positive(self.u), self.u)

    def testdot(self):
        self.assertEqual(vectors.dot(self.u, self.w), 1.0)
        self.assertEqual(vectors.dot(self.u, self.v), vectors.dot(self.v, self.u))

        func = lambda a, b: vectors.dot(a, b)
        self.assertRaises(vectors.VectorOperationError, func, self.u, self.x)

    def testcross(self):
        self.assertEqual(vectors.cross(self.u, self.v), vectors.Vector(-3, 6, -3))
        self.assertEqual(vectors.cross(self.u, self.u), vectors.Vector(0, 0, 0))

    def testangle(self):
        self.assertEqual(vectors.angle(self.u, self.u) , 0)
        self.assertEqual(vectors.angle(self.u, 2 * self.u) , 0)
        self.assertAlmostEqual(vectors.angle(self.u, self.v), 0.225726128553)

    def testdirectioncosine(self):
        self.assertEqual(vectors.directioncosine(self.u, self.u) , 1.0)
        self.assertEqual(vectors.directioncosine(self.u, 2 * self.u) , 1.0)
        self.assertAlmostEqual(vectors.directioncosine(self.u, self.v), 0.97463184619707621)

    def testtripleproduct(self):
        tp = vectors.tripleproduct(self.u, self.v, self.w)
        self.assertEqual(tp, -3.0)

        tp = vectors.tripleproduct(self.v, self.w, self.u)
        self.assertEqual(tp, -3.0)

        tp = vectors.tripleproduct(self.w, self.u, self.v)
        self.assertEqual(tp, -3.0)

        tp = vectors.tripleproduct(self.u, self.w, self.v)
        self.assertEqual(tp, 3.0)

    def testalmostequal(self):
        u = vectors.Vector3D(1, 2, 5)
        self.assertFalse(vectors.almostequal(self.u, u))

        u = vectors.Vector3D(1, 2, 3.00000001)
        self.assertTrue(vectors.almostequal(self.u, u))
        self.assertTrue(vectors.almostequal(u, self.u))

        self.assertFalse(vectors.almostequal(self.u, self.x))

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
