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
rep = 1000

class TestQuaternions(unittest.TestCase):

  def setUp(self):
    unittest.TestCase.setUp(self)
    
  def tearDown(self):
    unittest.TestCase.tearDown(self)
    
  def testSkeleton(self):
    #self.fail("Test if the TestCase is working.")
    self.assertTrue(True)

  def testInit(self):
    #Null quaternion
    q = quaternions.quaternion()
    for i in range(4):
      self.assertEqual(q[i], 0)
    
    #Real quaternion
    for i in range(rep):
      a = random.random() * 100
      q = quaternions.quaternion(a)
      
      self.assertEqual(q[0], a)
      for i in range(3):
        self.assertEqual(q[i+1], 0)
      
    #Pure quaternion
    for i in range(rep):
      x = random.random()
      y = random.random()
      z = random.random()
      q = quaternions.quaternion(x,y,z)
      
      self.assertEqual(q[0], 0)
      self.assertEqual(q[1], x)
      self.assertEqual(q[2], y)
      self.assertEqual(q[3], z)
    
    #Quaternion
    for i in range(rep):
      a = random.random() * 10
      x = random.random() * 10
      y = random.random() * 10
      z = random.random() * 10
      q1 = quaternions.quaternion(a,x,y,z)
      q2 = quaternions.quaternion(a,[x,y,z])
      
      self.assertEqual(q1[0], a)
      self.assertEqual(q1[1], x)
      self.assertEqual(q1[2], y)
      self.assertEqual(q1[3], z)
      self.assertEqual(q2[0], a)
      self.assertEqual(q2[1], x)
      self.assertEqual(q2[2], y)
      self.assertEqual(q2[3], z)

  def testGetItem(self):
    #Test for item outside limits
    q = quaternions.quaternion(1,2,3,4)
    self.assertEqual(q[-1], None)
    self.assertEqual(q[0], 1)
    self.assertEqual(q[1], 2)
    self.assertEqual(q[2], 3)
    self.assertEqual(q[3], 4)
    self.assertEqual(q[4], None)
  
  def testSetItem(self):
    #Test for changing values
    q = quaternions.quaternion(1,2,3,4)
    q[0] = 5
    q[1] = q[2]
    q[2] = q[3]
    q[3] = 1
    self.assertEqual(q, quaternions.quaternion(5, 3, 4, 1))
    
    #Test for item outside limits
    q = quaternions.quaternion(1,2,3,4)
    q[5] = 10
    self.assertEqual(q, quaternions.quaternion(1,2,3,4))

  def testRepr(self):
    pass
  
  def testMul(self):
    #Test for validity
    #http://reference.wolfram.com/mathematica/Quaternions/tutorial/Quaternions.html
    q1 = quaternions.quaternion(2,0,-6,3)
    q2 = quaternions.quaternion(1,3,-2,2)
    self.assertEqual(q1*q2, quaternions.quaternion(-16,0,-1,25))
    self.assertEqual(q2*q1, quaternions.quaternion(-16,12,-19,-11))
    
    #http://www.euclideanspace.com/maths/algebra/realNormedAlgebra/quaternions/arithmetic/index.htm
    q1 = quaternions.quaternion(5,2,1,2)
    q2 = quaternions.quaternion(4,8,25,4)
    self.assertEqual(q1*q2, quaternions.quaternion(-29,2,137,70))
    
    #Test scalar multiplication
    q = 2*quaternions.quaternion(5,2,1,2)
    self.assertEqual(q[0], 10)
    self.assertEqual(q[1], 4)
    self.assertEqual(q[2], 2)
    self.assertEqual(q[3], 4)
    
  def testDiv(self):
    pass
  
  def testAdd(self):
    #Test for validity
    #http://reference.wolfram.com/mathematica/Quaternions/tutorial/Quaternions.html
    q1 = quaternions.quaternion(1,2,3,4)
    q2 = quaternions.quaternion(2,3,4,5)
    self.assertEqual(q1+q2, quaternions.quaternion(3,5,7,9))
    self.assertEqual(q2+q1, quaternions.quaternion(3,5,7,9))
    
    #http://www.euclideanspace.com/maths/algebra/realNormedAlgebra/quaternions/arithmetic/index.htm
    q1 = quaternions.quaternion(5,2,1,2)
    q2 = quaternions.quaternion(4,8,25,4)
    self.assertEqual(q1+q2, quaternions.quaternion(9,10,26,6))
    self.assertEqual(q2+q1, quaternions.quaternion(9,10,26,6))
  
  def testSub(self):
    #Test for validity
    #http://www.euclideanspace.com/maths/algebra/realNormedAlgebra/quaternions/arithmetic/index.htm
    q1 = quaternions.quaternion(5,2,1,2)
    q2 = quaternions.quaternion(4,8,25,4)
    self.assertEqual(q1-q2, quaternions.quaternion(1,-6,-24,-2))
  
  def testAbs(self):
    #Test for validity
    #http://reference.wolfram.com/mathematica/Quaternions/tutorial/Quaternions.html
    q = quaternions.quaternion(4,3,-1,2)
    self.assertEqual(abs(q), sqrt(30))
    
  def testInvert(self):
    #Test for validity
    #http://www.euclideanspace.com/maths/algebra/realNormedAlgebra/quaternions/arithmetic/index.htm
    q = ~quaternions.quaternion(4,3,-1,2)
    self.assertAlmostEqual(q[0], 0.7302967433402214)
    self.assertAlmostEqual(q[1], -0.5477225575051661)
    self.assertAlmostEqual(q[2], 0.18257418583505536)
    self.assertAlmostEqual(q[3], -0.3651483716701107)
  
#  def testNeg(self):
#    #Test formula
#    q = -quaternions.quaternion(4,3,-1,2)
#    self.assertAlmostEqual(q[0], 4)
#    self.assertAlmostEqual(q[1], -3)
#    self.assertAlmostEqual(q[2], 1)
#    self.assertAlmostEqual(q[3], -2)
  
  def testEq(self):
    #Test equality
    q1 = quaternions.quaternion(4,3,2,5)
    q2 = quaternions.quaternion(4,3,2,5)
    self.assertEqual(q1,q2)
    self.assertEqual(q2,q1)
    
    q2 = quaternions.quaternion(4.0,3.0,2.0,5.0)
    self.assertEqual(q1,q2)
    self.assertEqual(q2,q1)
    
    q2 = quaternions.quaternion(4.00000005,3,2,5)
    self.assertEqual(q1,q2)
    self.assertEqual(q2,q1)
    
    q2 = quaternions.quaternion(-4,3,2,5)
    self.assertNotEqual(q1,q2)
    self.assertNotEqual(q2,q1)
    
    q2 = quaternions.quaternion(-4,3,2,5)
    self.assertNotEqual(q1,q2)
    self.assertNotEqual(q2,q1)
    
    q2 = quaternions.quaternion(-4,3,2,5)
    self.assertNotEqual(q1,q2)
    self.assertNotEqual(q2,q1)
    
    q2 = quaternions.quaternion(4,-2.9,2,5)
    self.assertNotEqual(q1,q2)
    self.assertNotEqual(q2,q1)
    
    q2 = quaternions.quaternion(4,3,-2,5)
    self.assertNotEqual(q1,q2)
    self.assertNotEqual(q2,q1)
    
    q2 = quaternions.quaternion(4,3,2,-5)
    self.assertNotEqual(q1,q2)
    self.assertNotEqual(q2,q1)
  
  def testConjugate(self):
    #Test for validity
    #http://www.euclideanspace.com/maths/algebra/realNormedAlgebra/quaternions/arithmetic/index.htm
    q = quaternions.quaternion(4,2,1,1).conjugate()
    self.assertEqual(q, quaternions.quaternion(4,-2,-1,-1))
    
    q = quaternions.quaternion(0.21566554640687682,0.10783277320343841,0,0.9704949588309457).conjugate()
    self.assertEqual(q, quaternions.quaternion(0.21566554640687682,-0.10783277320343841,0,-0.9704949588309457))
  
  def testIsNormalized(self):
    #Test for validity
    #http://www.euclideanspace.com/maths/algebra/realNormedAlgebra/quaternions/arithmetic/index.htm
    q = quaternions.quaternion(4,2,1,1)
    self.assertEqual(q.isnormalized(), False)
    
    q = quaternions.quaternion(0.21566554640687682,0.10783277320343841,0,0.9704949588309457).conjugate()
    self.assertEqual(q.isnormalized(), True)
  
  def testNormalize(self):
    #Test for validity
    #http://www.euclideanspace.com/maths/algebra/realNormedAlgebra/quaternions/arithmetic/index.htm
    q = quaternions.quaternion(4,2,-1,1)
    self.assertEqual(q.normalize(), quaternions.quaternion(0.8528028654224417, 0.42640143271122083, -0.21320071635561041, 0.21320071635561041))
  
  def testVector(self):
    import EBSDTools.mathTools.vectors as vectors
    
    q = quaternions.quaternion(4,2,-1,1)
    self.assertEqual(q.vector(), vectors.vector([2,-1,1]))
  
  def testScalar(self):
    q = quaternions.quaternion(4,2,-1,1)
    self.assertEqual(q.scalar(), 4)
  
#  def testPositive(self):
#    #TODO: Make positive test
#    q = quaternions.quaternion(-1,1,2,3).positive()
#    self.assertEqual(q, quaternions.quaternion(1,-1,-2,-3))
#    
#    q = quaternions.quaternion(0,-1,2,3).positive()
#    self.assertEqual(q, quaternions.quaternion(0,1,-2,-3).positive())
  
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
  

#  def testRotate(self):
#    #Test of successive rotations
#    q = quaternions.quaternion(0,1,0,0) #Vector (1,0,0)
#    q1 = quaternions.axisAngleToQuaternion(pi/2.0, (0,0,1)) #90deg rotation along z-axis
#    q2 = quaternions.axisAngleToQuaternion(pi/2.0, (1,0,0)) #90deg rotation along x-axis
#    
#    qq1 = quaternions.rotate(q, [q1])
#    self.assertEqual(qq1, quaternions.quaternion(0,0,1,0)) #Vector (0,1,0)
#    qq1q2 = quaternions.rotate(qq1, [q2])
#    self.assertEqual(qq1q2, quaternions.quaternion(0,0,0,1)) #Vector (0,0,1)
#    
#    self.assertEqual(qq1q2, quaternions.rotate(q, [q1,q2])) #Order of rotation q1 then q2
#    self.assertNotEqual(qq1q2, quaternions.rotate(q, [q2,q1]))
#    
#    #Test of successive rotations
#    q = quaternions.quaternion(0,1,0,0) #Vector (1,0,0)
#    q1 = quaternions.eulerAnglesToQuaternion(13, 0, 93)
#    q2 = quaternions.eulerAnglesToQuaternion(60, 80, 152)
#    q3 = quaternions.eulerAnglesToQuaternion(150,0,12)
#    
#    qq1 = quaternions.rotate(q, [q1])
#    qq1q2 = quaternions.rotate(qq1, [q2])
#    qq1q2q3 = quaternions.rotate(qq1q2, [q3])
#    
#    self.assertEqual(qq1q2q3, quaternions.rotate(q, [q1,q2,q3])) #Order of rotation q1, q2 then q3
#    self.assertNotEqual(qq1q2q3, quaternions.rotate(q, [q3,q2,q1]))
  
  def test__hash__(self):
    hashValues = []
    
    for i in range(rep):
      q = quaternions.quaternion(random.random(), random.random(), random.random(), random.random())
      hashValue = q.__hash__()
      self.assertFalse(hashValue in hashValues)
      
      hashValues.append(hashValue)
  
#  def testPositive(self):
#    self.assertEqual(quaternions.quaternion(1,1,1,1).positive(), quaternions.quaternion(1,1,1,1))
#    self.assertEqual(quaternions.quaternion(-1,1,1,1).positive(), quaternions.quaternion(1,-1,-1,-1))
#    self.assertEqual(quaternions.quaternion(1,1,-1,1).positive(), quaternions.quaternion(1,1,-1,1))
#    self.assertEqual(quaternions.quaternion(0,1,1,1).positive(), quaternions.quaternion(0,1,1,1))
#    self.assertEqual(quaternions.quaternion(0,-1,1,1).positive(), quaternions.quaternion(0,1,-1,-1))
#    self.assertEqual(quaternions.quaternion(0,0,1,-1).positive(), quaternions.quaternion(0,0,1,-1))
#    self.assertEqual(quaternions.quaternion(0,0,-1,-1).positive(), quaternions.quaternion(0,0,1,1))
#    self.assertEqual(quaternions.quaternion(0,0,0,1).positive(), quaternions.quaternion(0,0,0,1))
#    self.assertEqual(quaternions.quaternion(0,0,0,-1).positive(), quaternions.quaternion(0,0,0,1))
#    
#  
  
  def testEulerAnglesToQuaternion(self):
    import EBSDTools.mathTools.eulers as eulers
    #Verified with Rollett, Tony (2008) Advanced Characterization and Microstructural Analysis
    
    #Test calculation
    e = eulers.eulers(0,0,0)
    self.assertEqual(quaternions.eulerAnglesToQuaternion(e), quaternions.quaternion(1,0,0,0))
    
    e = eulers.eulers(0,pi/4,0)
    self.assertEqual(quaternions.eulerAnglesToQuaternion(e), quaternions.quaternion(cos(0.5*pi/4),sin(0.5*pi/4),0,0))
    
    e = eulers.eulers(35/180.0*pi,27/180.0*pi,102/180.0*pi)
    q1 = quaternions.eulerAnglesToQuaternion(e)
    q2 = quaternions.axisAngleToQuaternion(35/180.0*pi, (0,0,1)) * quaternions.axisAngleToQuaternion(27/180.0*pi, (1,0,0)) * quaternions.axisAngleToQuaternion(102/180.0*pi, (0,0,1))
    self.assertEqual(q1, q2)
    
    for i in range(10):
      e1 = random.random() * 360
      e2 = random.random() * 180
      e3 = random.random() * 360
    
      e = eulers.degEulersToRadEulers(e1, e2, e3)
      q1 = quaternions.eulerAnglesToQuaternion(e)
      q2 = quaternions.axisAngleToQuaternion(e[1], (0,0,1)) * quaternions.axisAngleToQuaternion(e[2], (1,0,0)) * quaternions.axisAngleToQuaternion(e[3], (0,0,1))
      self.assertEqual(q1,q2)
  
  def testToEulerAngles(self):
    import EBSDTools.mathTools.eulers as eulers
    
#    #Random eulers
    for i in range(rep):
      euler1 = random.random() * 360
      euler2 = random.random() * 180
      euler3 = random.random() * 360
      
      e = eulers.degEulersToRadEulers(euler1, euler2, euler3)
      q = quaternions.eulerAnglesToQuaternion(e)
      q2 = quaternions.axisAngleToQuaternion(e[1], (0,0,1)) * quaternions.axisAngleToQuaternion(e[2], (1,0,0)) * quaternions.axisAngleToQuaternion(e[3], (0,0,1))
      self.assertEqual(q, q2)
      
      qAngles = q.toEulerAngles().toDeg()
      self.assertAlmostEqual(euler2, qAngles[1], 4)
      self.assertAlmostEqual(euler1, qAngles[0], 4)
      self.assertAlmostEqual(euler3, qAngles[2], 4)
    
    #Special case when theta2 = 0 
    for i in range(rep):
      euler1 = random.random() * 360
      euler2 = 0.0
      euler3 = random.random() * (360 - euler1)
      
      e = eulers.degEulersToRadEulers(euler1, euler2, euler3)  
      q = quaternions.eulerAnglesToQuaternion(e)
      
      qAngles = q.toEulerAngles().toDeg()
      euler13 = euler1 + euler3
      self.assertAlmostEqual(euler13, qAngles[0])
      self.assertAlmostEqual(0.0, qAngles[1])
      self.assertAlmostEqual(0.0, qAngles[2])
      
      euler3 = random.random() * 360
      euler2 = 0.0
      euler1 = random.random() * (360 - euler3)
      
      e = eulers.degEulersToRadEulers(euler1, euler2, euler3) 
      q = quaternions.eulerAnglesToQuaternion(e)
      
      qAngles = q.toEulerAngles().toDeg()
      euler13 = euler1 + euler3
      self.assertAlmostEqual(euler13, qAngles[0])
      self.assertAlmostEqual(0.0, qAngles[1])
      self.assertAlmostEqual(0.0, qAngles[2])
    
    #Special case when theta2 = pi
    for i in range(rep):
      euler1 = random.random() * 360
      euler2 = 180
      euler3 = random.random() * (360 - euler1)
      
      e = eulers.degEulersToRadEulers(euler1, euler2, euler3)
      q = quaternions.eulerAnglesToQuaternion(e)
      
      qAngles = q.toEulerAngles().toDeg()
      euler13 = euler1 - euler3
      angles = eulers.degEulers(eulers.positiveEulers((euler13/180.0*pi, pi, 0.0)))
      self.assertAlmostEqual(angles[0], qAngles[0])
      self.assertAlmostEqual(angles[1], qAngles[1])
      self.assertAlmostEqual(angles[2], qAngles[2])
      
      euler3 = random.random() * 360
      euler2 = 180
      euler1 = random.random() * (360 - euler3)
      
      e = eulers.degEulersToRadEulers(euler1, euler2, euler3)
      q = quaternions.eulerAnglesToQuaternion(e)
      
      qAngles = q.toEulerAngles().toDeg()
      euler13 = euler1 - euler3
      angles = eulers.degEulers(eulers.positiveEulers((euler13/180.0*pi, pi, 0.0)))
      self.assertAlmostEqual(angles[0], qAngles[0])
      self.assertAlmostEqual(angles[1], qAngles[1])
      self.assertAlmostEqual(angles[2], qAngles[2])
  
  def testMatrixToQuaternion(self):
    import EBSDTools.mathTools.vectors as vectors
    import EBSDTools.mathTools.matrices as matrices
    #Verified with Martin Baker (2008) Quaternion to AxisAngle, \url{http://www.euclideansplace.com}
    
    #Test calculation
    m = matrices.matrix([[1,0,0], [0,0,-1], [0,1,0]])
    self.assertEqual(quaternions.matrixtoQuaternion(m), quaternions.quaternion(sqrt(2)/2.0, -sqrt(2)/2.0, 0, 0))
    
    #Test back-conversion
    q1 = quaternions.matrixtoQuaternion(m)
    mQ = q1.toMatrix()
    for i in [0,1,2]:
      for j in [0,1,2]:
        self.assertAlmostEqual(m[i][j], mQ[i][j], 4)
    
    #Random test
    for i in range(10):
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
    
  
  
if __name__ == '__main__':
  unittest.main()