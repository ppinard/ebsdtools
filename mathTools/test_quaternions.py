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
from math import pi, cos, sin, sqrt

# Third party modules.

# Local modules.
import EBSDTools.mathTools.quaternions as quaternions

# Globals and constants variables.

class TestQuaternions(unittest.TestCase):

  def setUp(self):
    unittest.TestCase.setUp(self)
    
  def tearDown(self):
    unittest.TestCase.tearDown(self)
    
  def testSkeleton(self):
    #self.fail("Test if the TestCase is working.")
    self.assertTrue(True)

  def testAxisAngleToQuaternion(self):
    #Verified with Martin Baker (2008) Quaternion to AxisAngle, \url{http://www.euclideansplace.com}
    
    #Test input data
    self.assertEqual(quaternions.axisAngleToQuaternion(0,(1,0,0)), quaternions.quaternion(1,0,0,0))
    self.assertEqual(quaternions.axisAngleToQuaternion(0,1,0,0), quaternions.quaternion(1,0,0,0))

    #Test calculation
    self.assertEqual(quaternions.axisAngleToQuaternion(pi/2, (1,0,0)), quaternions.quaternion(sqrt(2)/2.0, sqrt(2)/2.0, 0, 0))
    
    #Test back-conversion
    q1 = quaternions.axisAngleToQuaternion(pi/3, (1,1,1))
    self.assertAlmostEqual(q1.toAxisAngle()[0], pi/3, 3)
    self.assertEqual(q1.toAxisAngle()[1][0], q1.toAxisAngle()[1][1], q1.toAxisAngle()[1][2])
  
  def testMatrixToQuaternion(self):
    #Verified with Martin Baker (2008) Quaternion to AxisAngle, \url{http://www.euclideansplace.com}
    
    #Test calculation
    m = [[1,0,0], [0,0,-1], [0,1,0]]
    self.assertEqual(quaternions.matrixtoQuaternion(m), quaternions.quaternion(sqrt(2)/2.0, sqrt(2)/2.0, 0, 0))
    
    #Test back-conversion
    q1 = quaternions.matrixtoQuaternion(m)
    mQ = q1.toMatrix()
    for i in [0,1,2]:
      for j in [0,1,2]:
        self.assertAlmostEqual(m[i][j], mQ[i][j], 3)
    
  def testEulerAnglesToQuaternion(self):
    #Verified with Rollett, Tony (2008) Advanced Characterization and Microstructural Analysis
    
    #Test calculation
    self.assertEqual(quaternions.eulerAnglesToQuaternion(0,0,0), quaternions.quaternion(1,0,0,0))
    self.assertEqual(quaternions.eulerAnglesToQuaternion(0,pi/4,0), quaternions.quaternion(cos(0.5*pi/4),sin(0.5*pi/4),0,0))
    
    #Test back-conversion
    eulers = (pi/4,0,0)
    results = quaternions.eulerAnglesToQuaternion(eulers).toEulerAngles()
    for i in [0,1,2]:
      self.assertAlmostEqual(results[i], eulers[i], 3)
    
    eulers = (0,pi/4,0)
    results = quaternions.eulerAnglesToQuaternion(eulers).toEulerAngles()
    for i in [0,1,2]:
      self.assertAlmostEqual(results[i], eulers[i], 3)
    
    eulers = (pi/6,pi/4,0)
    results = quaternions.eulerAnglesToQuaternion(eulers).toEulerAngles()
    for i in [0,1,2]:
      self.assertAlmostEqual(results[i], eulers[i], 3)
      
    results = quaternions.eulerAnglesToQuaternion((0,0,pi/4)).toEulerAngles()
    eulers = (pi/4, 0, 0) #because of when \theta_2 == 0, \theta_1 = \theta_1 + \theta_3 and \theta_3 = 0
    for i in [0,1,2]:
      self.assertAlmostEqual(results[i], eulers[i], 3)
    
    results = quaternions.eulerAnglesToQuaternion((0,pi,pi/4)).toEulerAngles()
    eulers = (-pi/4, pi, 0) #because of when \theta_2 == \pi, \theta_1 = \theta_1 - \theta_3 and \theta_3 = \pi
    for i in [0,1,2]:
      self.assertAlmostEqual(results[i], eulers[i], 3)

if __name__ == '__main__':
  unittest.main()