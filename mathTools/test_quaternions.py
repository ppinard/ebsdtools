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

  def testRotate(self):
    #Test of successive rotations
    q = quaternions.quaternion(0,1,0,0) #Vector (1,0,0)
    q1 = quaternions.axisAngleToQuaternion(pi/2.0, (0,0,1)) #90deg rotation along z-axis
    q2 = quaternions.axisAngleToQuaternion(pi/2.0, (1,0,0)) #90deg rotation along x-axis
    
    qq1 = quaternions.rotate(q, [q1])
    self.assertEqual(qq1, quaternions.quaternion(0,0,1,0)) #Vector (0,1,0)
    qq1q2 = quaternions.rotate(qq1, [q2])
    self.assertEqual(qq1q2, quaternions.quaternion(0,0,0,1)) #Vector (0,0,1)
    
    self.assertEqual(qq1q2, quaternions.rotate(q, [q1,q2])) #Order of rotation q1 then q2
    self.assertNotEqual(qq1q2, quaternions.rotate(q, [q2,q1]))
    
    #Test of successive rotations
    q = quaternions.quaternion(0,1,0,0) #Vector (1,0,0)
    q1 = quaternions.eulerAnglesToQuaternion(13, 0, 93)
    q2 = quaternions.eulerAnglesToQuaternion(60, 80, 152)
    q3 = quaternions.eulerAnglesToQuaternion(150,0,12)
    
    qq1 = quaternions.rotate(q, [q1])
    qq1q2 = quaternions.rotate(qq1, [q2])
    qq1q2q3 = quaternions.rotate(qq1q2, [q3])
    
    self.assertEqual(qq1q2q3, quaternions.rotate(q, [q1,q2,q3])) #Order of rotation q1, q2 then q3
    self.assertNotEqual(qq1q2q3, quaternions.rotate(q, [q3,q2,q1]))
  
#  def test__hash__(self):
#    import random
#    
#    hashValues = []
#    
#    for i in range(1000):
#      q = quaternions.quaternion(random.random(), random.random(), random.random(), random.random())
#      hashValue = q.__hash__()
#      if hashValue in hashValues:
#        print q
#      
#      hashValues.append(hashValue)
#    
    
  
  def test(self):
    import vectors
    v = quaternions.quaternion(0,1,0,0) #Vector (1,0,0)
    q1 = quaternions.eulerAnglesToQuaternion(13, 0, 93)
    q2 = quaternions.eulerAnglesToQuaternion(60, 80, 152)
    q3 = quaternions.eulerAnglesToQuaternion(150,0,12)
    
    m1 = quaternions.matrixtoQuaternion([[-0.2415, -0.4756, -0.8458], [-0.7794, -0.4242, 0.4611], [-0.5781, 0.7706, -0.2682]])
    m2 = quaternions.matrixtoQuaternion([[-0.7035, 0.7045, -0.0939], [-0.4704, -0.5606, -0.6815], [-0.5328, -0.4352, 0.7258]])
    
    m = quaternions.matrixtoQuaternion([[-0.2874, -0.1762, -0.9415], [-0.7645, -0.5499,  0.3363], [-0.5770, 0.8164, 0.0233]])
    
    m3 = m1*m2
    
#    print m3.toMatrix()
#    print m.toMatrix()
    
    n1 = vectors.vector(-0.24010292588373822, -0.22683031725977587, -0.085024905374393375)
    n2 = vectors.vector(-0.24617887985919915, 0.23186271949917425, 0.084766186144241265)
    
    n1 = vectors.vector(-0.089639962534049308, 0.089281365367841842, 0.089639962534049322).positive()
    n2 = vectors.vector(-0.089639962534049322, -0.089281365367841842, -0.089639962534049308).positive()
    
    eP1 = n1 / n1.norm()
    eP2 = vectors.cross(n1, n2)
    eP2 /= eP2.norm()
    eP3 = vectors.cross(eP1, eP2)
    
    mP = [eP1.toList(), eP2.toList(), eP3.toList()]
    qP = quaternions.matrixtoQuaternion(mP)
    
    n1 = vectors.vector(1,1,1)
    n2 = vectors.vector(1,-1,-1)
    
    eC1 = n1 / n1.norm()
    eC2 = vectors.cross(n1, n2)
    eC2 /= eC2.norm()
    eC3 = vectors.cross(eC1, eC2)
    
    mC = [eC1.toList(), eC2.toList(), eC3.toList()]
    qC = quaternions.matrixtoQuaternion(mC)
    
    qS = quaternions.axisAngleToQuaternion(-0/180.0*pi, (1,0,0))
    
    qC_ = quaternions.matrixtoQuaternion([[1,0,0], [0,1,0], [0,0,1]])
    
    g = qC.conjugate() * qP * qS.conjugate()
    
    print g
    print g.toEulerAngles()
    print g.toAxisAngle()
    
    g = quaternions.quaternion(1,0,0,0)
    
    gP_ = qC * g * qS
    
    
  
if __name__ == '__main__':
  unittest.main()