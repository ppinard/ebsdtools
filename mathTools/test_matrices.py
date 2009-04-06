#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Philippe Pinard (philippe.pinard@gmail.com)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2008-2009 Philippe Pinard"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = ""
__svnDate__ = ""
__svnId__ = ""

# Standard library modules.
import os
import unittest
import random
if not os.name == 'java':
  import numpy

# Third party modules.

# Local modules.
import EBSDTools.mathTools.matrices as matrices
from RandomUtilities.testing.testOthers import almostEqual

# Globals and constants variables.
rep = 100

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
    for i in range(3):
      for j in range(3):
        self.assert_(almostEqual(self.m1[i][j], self.m1[i][j]))
        self.assert_(almostEqual(self.m2[i][j], self.m2[i][j]))
        self.assert_(almostEqual(self.m3[i][j], self.m3[i][j]))
  
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
    
    for i in range(3):
      for j in range(3):
        self.assert_(almostEqual(self.m1[i][j], m[i][j]))
  
  def test__mul__(self):
    if not os.name == 'java':
      m1_ = numpy.array(self.m1.toList())
      m2_ = numpy.array(self.m2.toList())
    
      #Matrix multiplication
      mm = self.m1 * self.m2
      mm_ = numpy.dot(m1_, m2_)
      
      for i in range(3):
        for j in range(3):
          self.assert_(almostEqual(mm[i][j], mm_[i][j]))
      
      #Scalar multiplication
      mm = self.m1 * 4
      mm_ = m1_ * 4
      
      for i in range(3):
        for j in range(3):
          self.assert_(almostEqual(mm[i][j], mm_[i][j]))
  
  def testDet(self):
    if not os.name == 'java':
      for k in range(rep):
        m = []
        for i in range(3):
          r = []
          for j in range(3):
            r.append(random.random())
          m.append(r)
        
        m_ = numpy.array(m)
        
        self.assert_(almostEqual(numpy.linalg.det(m_), matrices.matrix(m).det()))
  
  def testTranspose(self):
    if not os.name == 'java':
      m1_ = numpy.array(self.m1.toList())
      m1t = self.m1.transpose()
      m1_t = m1_.T
      
      for i in range(3):
        for j in range(3):
          self.assert_(almostEqual(m1t[i][j], m1_t[i][j]))
    
if __name__ == '__main__':
  unittest.main()