#!/usr/bin/env python
"""
================================================================================
:mod:`test_quaternions` -- Unit tests for the module :mod:`quaternions`.
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
from math import pi, cos, sin, sqrt
import random

# Third party modules.

# Local modules.
import mathtools.rotation.quaternions as quaternions
import mathtools.algebra.vectors as vectors
import mathtools.rotation.matrices as matrices
import  mathtools.rotation.eulers as eulers

# Globals and constants variables.
REPETITIONS = 1000

class TestQuaternion(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.q1 = quaternions.Quaternion(1, -2, 3, 4)
        self.q2 = quaternions.Quaternion(0, -1, 1, 1)
        self.q3 = quaternions.Quaternion(sqrt(2) / 2.0, sqrt(2) / 2.0, 0, 0)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        #self.fail("Test if the TestCase is working.")
        self.assert_(True)

    def testconstructor(self):
        #Null quaternion
        q = quaternions.Quaternion()
        self.assertEqual(q, quaternions.Quaternion(0, 0, 0, 0))

        #Real quaternion
        for _i in range(REPETITIONS):
            a = random.random()
            q = quaternions.Quaternion(a)
            self.assertEqual(q[0], a)
            self.assertEqual(q, quaternions.Quaternion(a, 0, 0, 0))

        #Pure quaternion
        for _i in range(REPETITIONS):
            x = random.random()
            y = random.random()
            z = random.random()
            q = quaternions.Quaternion(x, y, z)
            self.assertEqual(q, quaternions.Quaternion(0, x, y, z))

        #Quaternion
        for _i in range(REPETITIONS):
            a = random.random()
            x = random.random()
            y = random.random()
            z = random.random()
            q1 = quaternions.Quaternion(a, x, y, z)
            q2 = quaternions.Quaternion(a, [x, y, z])
            self.assertEqual(q1, q2)

        # Automatic positive
        expected_q2 = quaternions.Quaternion(0, 1, -1, -1)
        self.assertEqual(self.q2, expected_q2)

    def test__getitem__(self):
        self.assertEqual(self.q1[0], 1)
        self.assertEqual(self.q1[1], -2)
        self.assertEqual(self.q1[2], 3)
        self.assertEqual(self.q1[3], 4)

        func = lambda q, i: q[i]
        self.assertRaises(IndexError, func, self.q1, -1)

    def test__setitem__(self):
        self.q1[0] = 5
        self.q1[1] = self.q1[2]
        self.q1[2] = self.q1[3]
        self.q1[3] = 1
        self.assertEqual(self.q1, quaternions.Quaternion(5, 3, 4, 1))

        func = lambda q, i, value: quaternions.Quaternion.__setitem__(q, i, value)
        self.assertRaises(IndexError, func, self.q1, -1, 10)

    def test__repr__(self):
        expected_str = '[[1.000000, -2.000000, 3.000000, 4.000000]]'
        self.assertEqual(str(self.q1), expected_str)

    def test__mul__(self):
        #Test for validity
        #http://reference.wolfram.com/mathematica/Quaternions/tutorial/Quaternions.html
        q1 = quaternions.Quaternion(2, 0, -6, 3)
        q2 = quaternions.Quaternion(1, 3, -2, 2)
        self.assertEqual(q1 * q2, quaternions.Quaternion(-16, 0, -1, 25))

        #http://www.euclideanspace.com/maths/algebra/realNormedAlgebra/quaternions/arithmetic/index.htm
        q1 = quaternions.Quaternion(5, 2, 1, 2)
        q2 = quaternions.Quaternion(4, 8, 25, 4)
        self.assertEqual(q1 * q2, quaternions.Quaternion(-29, 2, 137, 70))

        #Test scalar multiplication
        q = 2 * quaternions.Quaternion(5, 2, 1, 2)
        self.assertEqual(q[0], 10)
        self.assertEqual(q[1], 4)
        self.assertEqual(q[2], 2)
        self.assertEqual(q[3], 4)

    def test__rmul__(self):
        #Test for validity
        #http://reference.wolfram.com/mathematica/Quaternions/tutorial/Quaternions.html
        q1 = quaternions.Quaternion(2, 0, -6, 3)
        q2 = quaternions.Quaternion(1, 3, -2, 2)
        self.assertEqual(q2 * q1, quaternions.Quaternion(-16, 12, -19, -11))
        self.assertNotEqual(q1 * q2, q2 * q1)

        #Test scalar multiplication
        q = quaternions.Quaternion(5, 2, 1, 2) * 2
        self.assertEqual(q[0], 10)
        self.assertEqual(q[1], 4)
        self.assertEqual(q[2], 2)
        self.assertEqual(q[3], 4)

    def test__div__(self):
        division = self.q1 / self.q2
        answer = quaternions.Quaternion(5.196152422706632, 1.1547005383792515, 0.57735026918962584, -1.1547005383792519)
        self.assertTrue(quaternions.almostequal(division, answer))

        division = self.q1 / 4.0
        answer = quaternions.Quaternion(0.25, -0.5, 0.75, 1.0)
        self.assertTrue(quaternions.almostequal(division, answer))

    def test__add__(self):
        #Test for validity
        #http://reference.wolfram.com/mathematica/Quaternions/tutorial/Quaternions.html
        q1 = quaternions.Quaternion(1, 2, 3, 4)
        q2 = quaternions.Quaternion(2, 3, 4, 5)
        self.assertEqual(q1 + q2, quaternions.Quaternion(3, 5, 7, 9))
        self.assertEqual(q2 + q1, quaternions.Quaternion(3, 5, 7, 9))

        #http://www.euclideanspace.com/maths/algebra/realNormedAlgebra/quaternions/arithmetic/index.htm
        q1 = quaternions.Quaternion(5, 2, 1, 2)
        q2 = quaternions.Quaternion(4, 8, 25, 4)
        self.assertEqual(q1 + q2, quaternions.Quaternion(9, 10, 26, 6))
        self.assertEqual(q2 + q1, quaternions.Quaternion(9, 10, 26, 6))

    def test__sub__(self):
        #Test for validity
        #http://www.euclideanspace.com/maths/algebra/realNormedAlgebra/quaternions/arithmetic/index.htm
        q1 = quaternions.Quaternion(5, 2, 1, 2)
        q2 = quaternions.Quaternion(4, 8, 25, 4)
        self.assertEqual(q1 - q2, quaternions.Quaternion(1, -6, -24, -2))

    def test__abs__(self):
        #Test for validity
        #http://reference.wolfram.com/mathematica/Quaternions/tutorial/Quaternions.html
        q = quaternions.Quaternion(4, 3, -1, 2)
        self.assertEqual(abs(q), sqrt(30))

    def test__invert__(self):
        #Test for validity
        #http://www.euclideanspace.com/maths/algebra/realNormedAlgebra/quaternions/arithmetic/index.htm
        q = ~quaternions.Quaternion(4, 3, -1, 2)
        expected_q = quaternions.Quaternion(0.7302967433402214, -0.5477225575051661, 0.18257418583505536, -0.3651483716701107)
        self.assertTrue(quaternions.almostequal(q, expected_q))

    def test__eq__(self):
        q1 = quaternions.Quaternion(4, 3, 2, 5)

        q2 = quaternions.Quaternion(4, 3, 2, 5)
        self.assertTrue(q1 == q2)
        self.assertTrue(q2 == q1)

        q2 = quaternions.Quaternion(4.0, 3.0, 2.0, 5.0)
        self.assertTrue(q1 == q2)
        self.assertTrue(q2 == q1)

        q2 = quaternions.Quaternion(4.00000005, 3, 2, 5)
        self.assertFalse(q1 == q2)
        self.assertFalse(q2 == q1)

    def test__ne__(self):
        q1 = quaternions.Quaternion(4, 3, 2, 5)

        q2 = quaternions.Quaternion(-4, 3, 2, 5)
        self.assertTrue(q1 != q2)
        self.assertTrue(q2 != q1)

        q2 = quaternions.Quaternion(-4, 3, 2, 5)
        self.assertTrue(q1 != q2)
        self.assertTrue(q2 != q1)

        q2 = quaternions.Quaternion(-4, 3, 2, 5)
        self.assertTrue(q1 != q2)
        self.assertTrue(q2 != q1)

        q2 = quaternions.Quaternion(4, -2.9, 2, 5)
        self.assertTrue(q1 != q2)
        self.assertTrue(q2 != q1)

        q2 = quaternions.Quaternion(4, 3, -2, 5)
        self.assertTrue(q1 != q2)
        self.assertTrue(q2 != q1)

        q2 = quaternions.Quaternion(4, 3, 2, -5)
        self.assertTrue(q1 != q2)
        self.assertTrue(q2 != q1)

    def test__hash__(self):
        expected_hash = -294937315
        self.assertEqual(hash(self.q1), expected_hash)

    def testget_vector(self):
        expected_vector = vectors.Vector3D(-2, 3, 4)
        self.assertEqual(self.q1.get_vector(), expected_vector)

    def testget_scalar(self):
        expected_scalar = 1
        self.assertEqual(self.q1.get_scalar(), expected_scalar)

    def testto_tuple(self):
        expected_tuple = (1, -2, 3, 4)
        self.assertEqual(self.q1.to_tuple(), expected_tuple)

    def testto_list(self):
        expected_list = [1, -2, 3, 4]
        self.assertEqual(self.q1.to_list(), expected_list)

    def testto_axisangle(self):
        # From http://www.euclideanspace.com/maths/geometry/rotations/conversions/quaternionToAngle/index.htm
        angle, axis = self.q3.to_axisangle()
        self.assertAlmostEqual(angle, pi / 2.0)
        self.assertAlmostEqual(axis[0], 1.0)
        self.assertAlmostEqual(axis[1], 0.0)
        self.assertAlmostEqual(axis[2], 0.0)

    def testto_so3matrix(self):
        # From http://www.euclideanspace.com/maths/geometry/rotations/conversions/quaternionToMatrix/index.htm
        matrix = self.q3.to_so3matrix()
        expected_matrix = matrices.SO3Matrix(1, 0, 0, 0, 0, 1, 0, -1, 0)
        self.assertTrue(matrices.almostequal(matrix, expected_matrix))

    def testto_eulerangles(self):
        # Random eulers
        for _i in range(REPETITIONS):
            euler1 = random.random() * 360
            euler2 = random.random() * 180
            euler3 = random.random() * 360

            e = eulers.eulers_deg_to_eulers_rad(euler1, euler2, euler3)
            q1 = quaternions.eulerangles_to_quaternion(e)
            q2 = quaternions.axisangle_to_quaternion(e[1], (0, 0, 1)) * \
                 quaternions.axisangle_to_quaternion(e[2], (1, 0, 0)) * \
                 quaternions.axisangle_to_quaternion(e[3], (0, 0, 1))
            self.assertTrue(quaternions.almostequal(q1, q2))

            qangles = q1.to_eulerangles().to_deg()
            self.assertAlmostEqual(euler2, qangles[1])
            self.assertAlmostEqual(euler1, qangles[0])
            self.assertAlmostEqual(euler3, qangles[2])

        # Special case when theta2 = 0
        for _i in range(REPETITIONS):
            euler1 = random.random() * 360
            euler2 = 0.0
            euler3 = random.random() * (360 - euler1)

            e = eulers.eulers_deg_to_eulers_rad(euler1, euler2, euler3)
            q = quaternions.eulerangles_to_quaternion(e)

            qangles = q.to_eulerangles().to_deg()
            euler13 = euler1 + euler3
            self.assertAlmostEqual(euler13, qangles[0])
            self.assertAlmostEqual(0.0, qangles[1])
            self.assertAlmostEqual(0.0, qangles[2])

            euler3 = random.random() * 360
            euler2 = 0.0
            euler1 = random.random() * (360 - euler3)

            e = eulers.eulers_deg_to_eulers_rad(euler1, euler2, euler3)
            q = quaternions.eulerangles_to_quaternion(e)

            qangles = q.to_eulerangles().to_deg()
            euler13 = euler1 + euler3
            self.assertAlmostEqual(euler13, qangles[0])
            self.assertAlmostEqual(0.0, qangles[1])
            self.assertAlmostEqual(0.0, qangles[2])

        # Special case when theta2 = pi
        for _i in range(REPETITIONS):
            euler1 = random.random() * 360
            euler2 = 180
            euler3 = random.random() * (360 - euler1)

            e = eulers.eulers_deg_to_eulers_rad(euler1, euler2, euler3)
            q = quaternions.eulerangles_to_quaternion(e)

            qangles = q.to_eulerangles().to_deg()
            euler13 = euler1 - euler3
            e = eulers.Eulers(euler13 / 180.0 * pi, pi, 0.0)
            e.positive()
            angles = e.to_deg()
            self.assertAlmostEqual(angles[0], qangles[0])
            self.assertAlmostEqual(angles[1], qangles[1])
            self.assertAlmostEqual(angles[2], qangles[2])

            euler3 = random.random() * 360
            euler2 = 180
            euler1 = random.random() * (360 - euler3)

            e = eulers.eulers_deg_to_eulers_rad(euler1, euler2, euler3)
            q = quaternions.eulerangles_to_quaternion(e)

            qangles = q.to_eulerangles().to_deg()
            euler13 = euler1 - euler3
            e = eulers.Eulers(euler13 / 180.0 * pi, pi, 0.0)
            e.positive()
            angles = e.to_deg()
            self.assertAlmostEqual(angles[0], qangles[0])
            self.assertAlmostEqual(angles[1], qangles[1])
            self.assertAlmostEqual(angles[2], qangles[2])

class TestQuaternions(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.q1 = quaternions.Quaternion(1, -2, 3, 4)
        self.q2 = quaternions.Quaternion(0, -1, 1, 1)
        self.q3 = quaternions.Quaternion(sqrt(2) / 2.0, sqrt(2) / 2.0, 0, 0)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        #self.fail("Test if the TestCase is working.")
        self.assert_(True)

    def testnorm(self):
        expected_norm = 5.4772255750516612
        self.assertAlmostEqual(quaternions.norm(self.q1), expected_norm)

        expected_norm = 1.7320508075688772
        self.assertAlmostEqual(quaternions.norm(self.q2), expected_norm)

        expected_norm = 1.0
        self.assertAlmostEqual(quaternions.norm(self.q3), expected_norm)

    def testconjugate(self):
        #Test for validity
        #http://www.euclideanspace.com/maths/algebra/realNormedAlgebra/quaternions/arithmetic/index.htm
        q = quaternions.Quaternion(4, 2, 1, 1)
        expected_conjugate = quaternions.Quaternion(4, -2, -1, -1)
        self.assertEqual(quaternions.conjugate(q), expected_conjugate)

        q = quaternions.Quaternion(0.21566554640687682, 0.10783277320343841, 0, 0.9704949588309457)
        expected_conjugate = quaternions.Quaternion(0.21566554640687682, -0.10783277320343841, 0, -0.9704949588309457)
        self.assertEqual(quaternions.conjugate(q), expected_conjugate)

    def testisnormalized(self):
        #Test for validity
        #http://www.euclideanspace.com/maths/algebra/realNormedAlgebra/quaternions/arithmetic/index.htm
        q = quaternions.Quaternion(4, 2, 1, 1)
        self.assertFalse(quaternions.isnormalized(q))

        q = quaternions.Quaternion(0.21566554640687682, 0.10783277320343841, 0, 0.9704949588309457)
        self.assertTrue(quaternions.isnormalized(q))

    def testnormalize(self):
        #Test for validity
        #http://www.euclideanspace.com/maths/algebra/realNormedAlgebra/quaternions/arithmetic/index.htm
        q = quaternions.Quaternion(4, 2, -1, 1)
        expected_normalize = quaternions.Quaternion(0.8528028654224417, 0.42640143271122083, -0.21320071635561041, 0.21320071635561041)
        self.assertEqual(quaternions.normalize(q), expected_normalize)

    def testpositive(self):
        q = quaternions.Quaternion(0, 0, 0, -1)
        expected_positive = quaternions.Quaternion(0, 0, 0, 1)
        quaternions.positive(q)
        self.assertEqual(q, expected_positive)

        q = quaternions.Quaternion(-1, 1, 1, -1)
        expected_positive = quaternions.Quaternion(1, -1, -1, 1)
        quaternions.positive(q)
        self.assertEqual(q, expected_positive)

    def testrotate(self):
        #Test of successive rotations
        q = quaternions.Quaternion(0, 1, 0, 0) #Vector (1,0,0)
        q1 = quaternions.axisangle_to_quaternion(pi / 2.0, (0, 0, 1)) #90deg rotation along z-axis
        q2 = quaternions.axisangle_to_quaternion(pi / 2.0, (1, 0, 0)) #90deg rotation along x-axis

        qq1 = quaternions.rotate(q, [q1])
        expected_qq1 = quaternions.Quaternion(0, 0, 1, 0)
        self.assertTrue(quaternions.almostequal(expected_qq1, qq1))

        # Vector (0,1,0)

        qq1q2 = quaternions.rotate(qq1, [q2])
        expected_qq1q2 = quaternions.Quaternion(0, 0, 0, 1)
        self.assertTrue(quaternions.almostequal(qq1q2, expected_qq1q2)) #Vector (0,0,1)

        expected_qq1q2 = quaternions.rotate(q, [q1, q2])
        self.assertTrue(quaternions.almostequal(qq1q2, expected_qq1q2)) #Order of rotation q1 then q2

        notexpected_qq1q2 = quaternions.rotate(q, [q2, q1])
        self.assertFalse(quaternions.almostequal(qq1q2, notexpected_qq1q2))

        #Test of successive rotations
        q = quaternions.Quaternion(0, 1, 0, 0) #Vector (1,0,0)
        q1 = quaternions.eulerangles_to_quaternion(eulers.Eulers(13, 0, 93))
        q2 = quaternions.eulerangles_to_quaternion(eulers.Eulers(60, 80, 152))
        q3 = quaternions.eulerangles_to_quaternion(eulers.Eulers(150, 0, 12))

        qq1 = quaternions.rotate(q, [q1])
        qq1q2 = quaternions.rotate(qq1, [q2])
        qq1q2q3 = quaternions.rotate(qq1q2, [q3])

        #Order of rotation q1, q2 then q3
        expected_qq1q2q3 = quaternions.rotate(q, [q1, q2, q3])
        self.assertTrue(quaternions.almostequal(qq1q2q3, expected_qq1q2q3))

        notexpected_qq1q2q3 = quaternions.rotate(q, [q3, q2, q1])
        self.assertFalse(quaternions.almostequal(qq1q2q3, notexpected_qq1q2q3))

    def testmisorientation(self):
        #TODO: Test misorientation
        pass

    def testalmostequal(self):
        q1 = quaternions.Quaternion(1, -2, 3, 5)
        self.assertFalse(quaternions.almostequal(self.q1, q1))

        q1 = quaternions.Quaternion(1, -2, 3, 4.00000001)
        self.assertTrue(quaternions.almostequal(self.q1, q1))
        self.assertTrue(quaternions.almostequal(q1, self.q1))

class TestQuaternionsConversion(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        #self.fail("Test if the TestCase is working.")
        self.assert_(True)

    def testaxisangle_to_quaternion(self):
        #Verified with Martin Baker (2008) Quaternion to AxisAngle, \url{http://www.euclideansplace.com}

        #Test input data
        q = quaternions.axisangle_to_quaternion(0, (1, 0, 0))
        expected_q = quaternions.Quaternion(1, 0, 0, 0)
        self.assertTrue(quaternions.almostequal(q, expected_q))

        #Test calculation
        q = quaternions.axisangle_to_quaternion(pi / 2, (1, 0, 0))
        expected_q = quaternions.Quaternion(sqrt(2) / 2.0, sqrt(2) / 2.0, 0, 0)
        self.assertTrue(quaternions.almostequal(q, expected_q))

        #Test back-conversion
        q1 = quaternions.axisangle_to_quaternion(pi / 3, (1, 1, 1))
        angle, axis = q1.to_axisangle()
        self.assertAlmostEqual(angle, pi / 3.0)
        self.assertAlmostEqual(axis[0], 1.0 / sqrt(3))
        self.assertAlmostEqual(axis[1], 1.0 / sqrt(3))
        self.assertAlmostEqual(axis[2], 1.0 / sqrt(3))

    def testso3matrix_to_quaternion(self):
        # Verified with Martin Baker (2008) Quaternion to AxisAngle, \url{http://www.euclideansplace.com}

        # Test calculation
        m = matrices.SO3Matrix([[1, 0, 0], [0, 0, -1], [0, 1, 0]])
        q = quaternions.so3matrix_to_quaternion(m)
        expected_q = quaternions.Quaternion(sqrt(2) / 2.0, -sqrt(2) / 2.0, 0, 0)
        self.assertTrue(quaternions.almostequal(q, expected_q))

        # Test back-conversion
        q1 = quaternions.so3matrix_to_quaternion(m)
        mq = q1.to_so3matrix()
        self.assertTrue(matrices.almostequal(m, mq))

        # Random test
        for _i in range(REPETITIONS):
            n = []
            for _j in range(2):
                x = random.random() * (-1) ** (int(random.random()*10))
                z = random.random() * (-1) ** (int(random.random()*10))
                y = random.random() * (-1) ** (int(random.random()*10))
                n.append(vectors.normalize(vectors.Vector3D(x, y, z)))

            eP1 = vectors.normalize(n[0])
            eP2 = vectors.cross(n[0], n[1])
            eP2.normalize()
            eP3 = vectors.normalize(vectors.cross(eP1, eP2))

            m = matrices.SO3Matrix([[eP1[0], eP2[0], eP3[0]],
                                    [eP1[1], eP2[1], eP3[1]],
                                    [eP1[2], eP2[2], eP3[2]]])

            q = quaternions.so3matrix_to_quaternion(m)
            mq = q.to_so3matrix()

            self.assertTrue(matrices.almostequal(m, mq))

    # Special case when trace + 1 = 0
    #TODO: Test so3matrix_to_quaternion Special case when trace + 1 = 0

    def testEulerAnglesToQuaternion(self):
        #Verified with Rollett, Tony (2008) Advanced Characterization and Microstructural Analysis

        #Test calculation
        e = eulers.Eulers(0, 0, 0)
        q = quaternions.eulerangles_to_quaternion(e)
        expected_q = quaternions.Quaternion(1, 0, 0, 0)
        self.assertTrue(quaternions.almostequal(q, expected_q))

        e = eulers.Eulers(0, pi / 4, 0)
        q = quaternions.eulerangles_to_quaternion(e)
        expected_q = quaternions.Quaternion(cos(0.5 * pi / 4), sin(0.5 * pi / 4), 0, 0)
        self.assertTrue(quaternions.almostequal(q, expected_q))

        e = eulers.Eulers(35 / 180.0 * pi, 27 / 180.0 * pi, 102 / 180.0 * pi)
        q = quaternions.eulerangles_to_quaternion(e)
        expected_q = quaternions.axisangle_to_quaternion(35 / 180.0 * pi, (0, 0, 1)) * \
                     quaternions.axisangle_to_quaternion(27 / 180.0 * pi, (1, 0, 0)) * \
                     quaternions.axisangle_to_quaternion(102 / 180.0 * pi, (0, 0, 1))
        self.assertTrue(quaternions.almostequal(q, expected_q))

        for _i in range(REPETITIONS):
            e1 = random.random() * 360
            e2 = random.random() * 180
            e3 = random.random() * 360

            e = eulers.eulers_deg_to_eulers_rad(e1, e2, e3)
            q = quaternions.eulerangles_to_quaternion(e)
            expected_q = quaternions.axisangle_to_quaternion(e[1], (0, 0, 1)) * \
                         quaternions.axisangle_to_quaternion(e[2], (1, 0, 0)) * \
                         quaternions.axisangle_to_quaternion(e[3], (0, 0, 1))
            self.assertTrue(quaternions.almostequal(q, expected_q))

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
