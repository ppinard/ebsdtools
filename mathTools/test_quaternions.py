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
import random

# Third party modules.

# Local modules.
import EBSDTools.mathTools.quaternions as quaternions

# Globals and constants variables.
rep = 100

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
    import EBSDTools.mathTools.vectors as vectors
    import EBSDTools.mathTools.matrices as matrices
    #Verified with Martin Baker (2008) Quaternion to AxisAngle, \url{http://www.euclideansplace.com}
    
    #Test calculation
    m = matrices.matrix([[1,0,0], [0,0,-1], [0,1,0]])
    self.assertEqual(quaternions.matrixtoQuaternion(m), quaternions.quaternion(sqrt(2)/2.0, sqrt(2)/2.0, 0, 0))
    
    #Test back-conversion
    q1 = quaternions.matrixtoQuaternion(m)
    mQ = q1.toMatrix()
    for i in [0,1,2]:
      for j in [0,1,2]:
        self.assertAlmostEqual(m[i][j], mQ[i][j], 4)
    
    #Random test
    for i in range(rep):
      n = []
      for j in range(2):
        x = random.random() * (-1)**(int(random.random()*10))
        z = random.random() * (-1)**(int(random.random()*10))
        y = random.random() * (-1)**(int(random.random()*10))
        n.append(vectors.vector(x,y,z).normalize())
      
      eP1 = n[0].normalize()
      eP2 = vectors.cross(n[0], n[1])
      eP2 = eP2.normalize()
      eP3 = vectors.cross(eP1, eP2).normalize()
      
      m = matrices.matrix([[eP1[0], eP2[0], eP3[0]],
                           [eP1[1], eP2[1], eP3[1]],
                           [eP1[2], eP2[2], eP3[2]]])
      
      q = quaternions.matrixtoQuaternion(m)
      mQ = q.toMatrix()
      
      for i in [0,1,2]:
        for j in [0,1,2]:
          self.assertAlmostEqual(m[i][j], mQ[i][j], 4)
    
    #Special case when trace + 1 = 0
    
  def testEulerAnglesToQuaternion(self):
    #Verified with Rollett, Tony (2008) Advanced Characterization and Microstructural Analysis
    
    #Test calculation
    self.assertEqual(quaternions.eulerAnglesToQuaternion(0,0,0), quaternions.quaternion(1,0,0,0))
    self.assertEqual(quaternions.eulerAnglesToQuaternion(0,pi/4,0), quaternions.quaternion(cos(0.5*pi/4),sin(0.5*pi/4),0,0))
    
    q1 = quaternions.eulerAnglesToQuaternion(35/180.0*pi,27/180.0*pi,102/180.0*pi)
    q2 = quaternions.axisAngleToQuaternion(102/180.0*pi, (0,0,1)) * quaternions.axisAngleToQuaternion(27/180.0*pi, (1,0,0)) * quaternions.axisAngleToQuaternion(35/180.0*pi, (0,0,1))
    self.assertEqual(q1, q2)
    
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
  
  def test__hash__(self):
    hashValues = []
    
    for i in range(rep):
      q = quaternions.quaternion(random.random(), random.random(), random.random(), random.random())
      hashValue = q.__hash__()
      self.assertFalse(hashValue in hashValues)
      
      hashValues.append(hashValue)
  
  def testPositive(self):
    self.assertEqual(quaternions.quaternion(1,1,1,1).positive(), quaternions.quaternion(1,1,1,1))
    self.assertEqual(quaternions.quaternion(-1,1,1,1).positive(), quaternions.quaternion(1,-1,-1,-1))
    self.assertEqual(quaternions.quaternion(1,1,-1,1).positive(), quaternions.quaternion(1,1,-1,1))
    self.assertEqual(quaternions.quaternion(0,1,1,1).positive(), quaternions.quaternion(0,1,1,1))
    self.assertEqual(quaternions.quaternion(0,-1,1,1).positive(), quaternions.quaternion(0,1,-1,-1))
    self.assertEqual(quaternions.quaternion(0,0,1,-1).positive(), quaternions.quaternion(0,0,1,-1))
    self.assertEqual(quaternions.quaternion(0,0,-1,-1).positive(), quaternions.quaternion(0,0,1,1))
    self.assertEqual(quaternions.quaternion(0,0,0,1).positive(), quaternions.quaternion(0,0,0,1))
    self.assertEqual(quaternions.quaternion(0,0,0,-1).positive(), quaternions.quaternion(0,0,0,1))
    
  
  def testToEulerAngles(self):
    import EBSDTools.mathTools.eulers as eulers
    
#    #Random eulers
    for i in range(rep):
      euler1 = random.random() * 360
      euler2 = random.random() * 180
      euler3 = random.random() * 360
    
      angles = eulers.negativeEulers(euler1/180.0*pi, euler2/180.0*pi, euler3/180.0*pi) 
      
      q = quaternions.eulerAnglesToQuaternion(angles)
      
      qAngles = eulers.degEulers(eulers.positiveEulers(q.toEulerAngles()))
      self.assertAlmostEqual(euler1, qAngles[0], 4)
      self.assertAlmostEqual(euler2, qAngles[1], 4)
      self.assertAlmostEqual(euler3, qAngles[2], 4)
#    
    #Special case when theta2 = 0 
    for i in range(rep):
      euler1 = random.random() * 360
      euler2 = 0.0
      euler3 = random.random() * (360 - euler1)
      
      angles = eulers.negativeEulers(euler1/180.0*pi, euler2/180.0*pi, euler3/180.0*pi) 
      
      q = quaternions.eulerAnglesToQuaternion(angles)
      
      qAngles = eulers.degEulers(eulers.positiveEulers(q.toEulerAngles()))
      euler13 = euler1 + euler3
      self.assertAlmostEqual(euler13, qAngles[0])
      self.assertAlmostEqual(0.0, qAngles[1])
      self.assertAlmostEqual(0.0, qAngles[2])
      
      euler3 = random.random() * 360
      euler2 = 0.0
      euler1 = random.random() * (360 - euler3)
      
      angles = eulers.negativeEulers(euler1/180.0*pi, euler2/180.0*pi, euler3/180.0*pi) 
      
      q = quaternions.eulerAnglesToQuaternion(angles)
      
      qAngles = eulers.degEulers(eulers.positiveEulers(q.toEulerAngles()))
      euler13 = euler1 + euler3
      self.assertAlmostEqual(euler13, qAngles[0])
      self.assertAlmostEqual(0.0, qAngles[1])
      self.assertAlmostEqual(0.0, qAngles[2])
    
    #Special case when theta2 = pi
    for i in range(rep):
      euler1 = random.random() * 360
      euler2 = 180
      euler3 = random.random() * (360 - euler1)
      
      angles = eulers.negativeEulers(euler1/180.0*pi, euler2/180.0*pi, euler3/180.0*pi) 
      
      q = quaternions.eulerAnglesToQuaternion(angles)
      
      qAngles = eulers.degEulers(eulers.positiveEulers(q.toEulerAngles()))
      
      euler13 = euler1 - euler3
      angles = eulers.degEulers(eulers.positiveEulers((euler13/180.0*pi, pi, 0.0)))
      self.assertAlmostEqual(angles[0], qAngles[0])
      self.assertAlmostEqual(angles[1], qAngles[1])
      self.assertAlmostEqual(angles[2], qAngles[2])
      
      euler3 = random.random() * 360
      euler2 = 180
      euler1 = random.random() * (360 - euler3)
      
      angles = eulers.negativeEulers(euler1/180.0*pi, euler2/180.0*pi, euler3/180.0*pi) 
      
      q = quaternions.eulerAnglesToQuaternion(angles)
      
      qAngles = eulers.degEulers(eulers.positiveEulers(q.toEulerAngles()))
      
      euler13 = euler1 - euler3
      angles = eulers.degEulers(eulers.positiveEulers((euler13/180.0*pi, pi, 0.0)))
      self.assertAlmostEqual(angles[0], qAngles[0])
      self.assertAlmostEqual(angles[1], qAngles[1])
      self.assertAlmostEqual(angles[2], qAngles[2])
  
    
  
  
if __name__ == '__main__':
  unittest.main()