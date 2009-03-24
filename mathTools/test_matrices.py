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
import numpy
import scipy.linalg
import random

# Third party modules.

# Local modules.
import EBSDTools.mathTools.matrices as matrices

# Globals and constants variables.
class TestMatrices(unittest.TestCase):

  def setUp(self):
    unittest.TestCase.setUp(self)
    
    self.m1 = matrices.matrix([[1,2,3],[4,5,6],[7,8,9]])
    self.m2 = matrices.matrix([1,2,3],[4,5,6],[7,8,9])
    self.m3 = matrices.matrix(1,2,3,4,5,6,7,8,9)
    
  def tearDown(self):
    unittest.TestCase.tearDown(self)
    
  def testSkeleton(self):
    #self.fail("Test if the TestCase is working.")
    self.assert_(True)
  
  def test__eq__(self):
    self.assertEqual(self.m1, self.m2)
    self.assertEqual(self.m2, self.m3)
    self.assertEqual(self.m1, self.m3)
  
  def test__getitem__(self):
    for i in range(3):
      for j in range(3):
        value = (i*3) + (j+1)
        self.assertEqual(self.m1[i][j], value)
        self.assertEqual(self.m2[i][j], value)
        self.assertEqual(self.m3[i][j], value)
  
  def test__setitem__(self):
    m = matrices.matrix(9,2,3,4,9,6,7,8,9)
    self.m1[0][0] = 9
    self.m1[1][1] = 9
    self.m1[2][2] = 9
    
    self.assertEqual(self.m1, m)
  
  def test__mul__(self):
    m1_ = numpy.array(self.m1.toList())
    m2_ = numpy.array(self.m2.toList())
    
    #Matrix multiplication
    mm = self.m1 * self.m2
    mm_ = numpy.dot(m1_, m2_)
    
    for i in range(3):
      for j in range(3):
        self.assertAlmostEqual(mm[i][j], mm_[i][j])
    
    #Scalar multiplication
    mm = self.m1 * 4
    mm_ = m1_ * 4
    
    for i in range(3):
      for j in range(3):
        self.assertAlmostEqual(mm[i][j], mm_[i][j])
  
  def testDet(self):
    for k in range(100):
      m = []
      for i in range(3):
        r = []
        for j in range(3):
          r.append(random.random())
        m.append(r)
      
      m_ = numpy.array(m)
      
      self.assertAlmostEqual(scipy.linalg.det(m_), matrices.det(m_), 4)
  
  def testTranspose(self):
    m1_ = numpy.array(self.m1.toList())
    m1t = matrices.transpose(self.m1)
    m1_t = m1_.T
    
    for i in range(3):
      for j in range(3):
        self.assertAlmostEqual(m1t[i][j], m1_t[i][j], 4)
    
if __name__ == '__main__':
  unittest.main()