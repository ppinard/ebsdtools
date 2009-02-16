#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Philippe Pinard (philippe.pinard@gmail.com)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2008 Philippe Pinard"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = ""
__svnDate__ = ""
__svnId__ = ""

# Standard library modules.
import unittest
from math import sqrt

# Third party modules.

# Local modules.
import EBSDTools.mathTools.vectors as vectors

# Globals and constants variables.

class TestVectors(unittest.TestCase):

  def setUp(self):
    unittest.TestCase.setUp(self)
    
    self.u = vectors.vector(1,2,3)
    self.v = vectors.vector([4,5,6])
    self.w = vectors.vector(1,0,0)
    self.x = vectors.vector(1,0,0,0,-5,6)
    self.y = vectors.vector([1,2,3,4])
    self.z = vectors.vector(8,9)
    
    
  def tearDown(self):
    unittest.TestCase.tearDown(self)
    
  def testSkeleton(self):
    #self.fail("Test if the TestCase is working.")
    self.assert_(True)
  
  def test__repr__(self):
    self.assertEqual(str(self.u), '[1, 2, 3]')
    self.assertEqual(str(self.v), '[4, 5, 6]')
    self.assertEqual(str(self.x), '[1, 0, 0, 0, -5, 6]')
  
  def test__getslice__(self):
    self.assertEqual(self.u[1:], vectors.vector(2,3))
    self.assertEqual(self.v[-2:], vectors.vector(5,6))
    self.assertEqual(self.y[2:-1], vectors.vector(3))
    self.assertEqual(self.z[:], vectors.vector(8,9))
  
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
    self.assertEqual(self.u, vectors.vector(1,3))
    self.assertEqual(len(self.x), 4)
    self.assertEqual(self.x, vectors.vector(1,0,-5,6))
  
  def test__lt__(self):
    self.assert_(self.u < self.v)
    self.assert_(self.u < self.x)
    self.assertFalse(self.u < self.w)
    self.assert_(self.z < self.u)
  
  def test__le__(self):
    self.assert_(self.u <= self.u)
    self.assert_(self.u <= self.v)
  
  def test__gt__(self):
    self.assert_(self.x > self.u)
    self.assert_(self.x > self.v)
    self.assertFalse(self.w > self.u)
  
  def test__ge__(self):
    self.assert_(self.x >= self.x)
    self.assert_(self.x >= self.u)
  
  def test__eq__(self):
    self.assert_(self.u == self.u)
    self.assert_(self.x == self.x)
    self.assertFalse(self.u == self.v)
  
  def test__ne__(self):
    self.assertFalse(self.u != self.u)
    self.assertFalse(self.x != self.x)
    self.assert_(self.u != self.v)
  
  def test__add__(self):
    self.assertEqual(self.u+self.w, vectors.vector(2,2,3))
    self.assertEqual(self.u+self.v, self.v+self.u)
    self.assertEqual(self.u+self.x, vectors.vector())
  
  def test__neg__(self):
    self.assertEqual(-self.u, vectors.vector(-1,-2,-3))
    self.assertEqual(-self.x, vectors.vector(-1,0,0,0,5,-6))
  
  def test__sub__(self):
    self.assertEqual(self.v-self.u, vectors.vector(3,3,3))
    self.assertEqual(self.v-self.u, self.v + -self.u)
    self.assertNotEqual(self.v-self.u, self.u-self.v)
    self.assertEqual(self.u+self.x, vectors.vector())
  
  def test__mul__(self):
    self.assertEqual(2*self.u, vectors.vector(2,4,6))
    self.assertEqual(2*self.w, vectors.vector(2,0,0))
    self.assertEqual(2*self.u, self.u*2)
  
  def test__div__(self):
    self.assertEqual(self.u/2.0, 0.5*self.u)
    self.assertEqual(self.v/3.0, 1/3.0*self.v)
  
  def test__len__(self):
    self.assertEqual(len(self.u), 3)
    self.assertEqual(len(self.x), 6)
    self.assertEqual(len(self.y), 4)
    self.assertEqual(len(self.z), 2)
  
  def testNorm(self):
    self.assertEqual(self.u.norm(), sqrt(1**2 + 2**2 + 3**2))
    self.assertEqual(self.x.norm(), sqrt(1**2 + 5**2 + 6**2))
  
  def testNormalize(self):
    self.assertEqual(self.w.normalize(), self.w)
    self.assertEqual(self.u.normalize(), self.u / self.u.norm())
  
  def testDot(self):
    self.assertEqual(vectors.dot(self.u, self.w), 1.0)
    self.assertEqual(vectors.dot(self.u, self.v), vectors.dot(self.v, self.u))
    self.assertEqual(vectors.dot(self.u, self.x), 0)
  
  def testCross(self):
    self.assertEqual(vectors.cross(self.u, self.v), vectors.vector(-3,6,-3))
    self.assertEqual(vectors.cross(self.u, self.u), vectors.vector(0,0,0))
  
  def testAngle(self):
    self.assertEqual(vectors.angle(self.u, self.u) , 0)
    self.assertEqual(vectors.angle(self.u, 2*self.u) , 0)
    self.assertAlmostEqual(vectors.angle(self.u, self.v), 0.225726128553, 3)
    
  
if __name__ == '__main__':
  unittest.main()