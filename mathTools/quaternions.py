#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Philippe Pinard (philippe.pinard@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2008 Philippe Pinard"
__license__ = ""
__reference__ = "Altmann (1986) Rotation, Quaternions and Double Groups"

# Subversion informations for the file.
__svnRevision__ = ""
__svnDate__ = ""
__svnId__ = ""

# Standard library modules.
from math import sin, cos, pi, acos, atan2, sqrt, asin, atan

# Third party modules.

# Local modules.
import EBSDTools.mathTools.vectors as vectors
import EBSDTools.mathTools.matrices as matrices
import EBSDTools.mathTools.eulers as eulers
from EBSDTools.mathTools.mathExtras import zeroPrecision

def axisAngleToQuaternion(*data):
  """
    Convert ($\phi$, $\vec{n}$) to a quaternion
    
    Equations:
      $a = \cos{\frac{\phi}{2}}$
      $A_x = n_x * \sin{\frac{\phi}{2}}$
      $A_y = n_y * \sin{\frac{\phi}{2}}$
      $A_z = n_z * \sin{\frac{\phi}{2}}$
        
        Where $\vec{n}$ needs to be a normalized vector (automatically normalized by this function)
    
    Reference:
      Martin Baker (2008) Euclidean Space, \url{http://www.euclideansplace.com}
      
    Inputs:
      len(data) == 2: (phi, n)
      len(data) == 4: (phi, n_x, n_y, n_z)
    
    Outputs:
      a quaternion
  """
  
  if len(data) == 2:
    n = vectors.vector(data[1][0], data[1][1], data[1][2])
  elif len(data) == 4:
    n = vectors.vector(data[1], data[2], data[3])
  
  n = n.normalize()
  multiplier = sin(0.5*data[0])
  
  return quaternion(cos(0.5*data[0])
                      , n[0] * multiplier
                      , n[1] * multiplier
                      , n[2] * multiplier)

def matrixtoQuaternion(m):
  """
    Convert a SO3 matrix to a quaternion
    
    Equations:
      $a = 0.5*\sqrt{1 + m00 + m11 + m22}$
      $A_x = \frac{m21 - m12}{4a}$
      $A_y = \frac{m02 - m20}{4a}$
      $A_z = \frac{m10 - m01}{4a}$
    
    Reference:
      Martin Baker (2008) Euclidean Space, \url{http://www.euclideansplace.com}
    
    Inputs:
      m: a matrix
    
    Outputs:
      a quaternion
  """
  assert isinstance(m, matrices.matrix)
  assert m.isSU3()
  
  A = []
  w = 0.5 * sqrt(m[0][0] + m[1][1] + m[2][2] + 1)
  
  if abs(w) > zeroPrecision:
    #Morawiec & orilib
    A.append((m[1][2] - m[2][1]) / (4*w))
    A.append((m[2][0] - m[0][2]) / (4*w))
    A.append((m[0][1] - m[1][0]) / (4*w))
  else:
    A.append(sqrt((m[0][0]+1)/2.0))
    A.append(sqrt((m[1][1]+1)/2.0))
    A.append(sqrt((m[2][2]+1)/2.0))
    
    s = A.index(max(A))
    for i in range(len(A)):
      if i != s:
        if abs(m[i][i]) > zeroPrecision:
          A[i] *= m[i][i] / abs(m[i][i])
    
  return quaternion(w, A)

#def matrixtoQuaternionBaker(m):
#  w = 0.5 * sqrt(m[0][0] + m[1][1] + m[2][2] + 1)
#  
#  if abs(w) > zeroPrecision:
##    Martin Baker
#    B = []
#    B.append((m[2][1] - m[1][2]) / (4*w))
#    B.append((m[0][2] - m[2][0]) / (4*w))
#    B.append((m[1][0] - m[0][1]) / (4*w))
#    
#  return quaternion(w,B)
#
#def matrixtoQuaternionOrilib(m):
#  w = 0.5 * sqrt(m[0][0] + m[1][1] + m[2][2] + 1)
#  
#  if abs(w) > zeroPrecision:
#    #Morawiec & orilib
#    A = []
#    A.append((m[1][2] - m[2][1]) / (4*w))
#    A.append((m[2][0] - m[0][2]) / (4*w))
#    A.append((m[0][1] - m[1][0]) / (4*w))
#  
#  return quaternion(w,A)

def eulerAnglesToQuaternion(angles):
  """
    Convert Euler angles ($\theta_1$, $\theta_2$, $\theta_3$) to a quaternion
    
    The Euler angles have to be in line with Bunge definition of the euler angles
      $R(\theta_3\vec{k})R(\theta_2\vec{i})R(\theta_1\vec{k})$
      Where the rotation is performed from $\theta_1\rightarrow\theta_2\rightarrow_3$
    
    References:
      Inspired by Altmann, Simon (1986) Rotations, Quaternions, and Double Groups and
                  Rollett, Tony (2008) Advanced Characterization and Microstructural Analysis
    
    Inputs:
      angles: a eulers
    
    Outputs:
      a quaternion
  """
  
  assert isinstance(angles, eulers.eulers)
  
  t1 = angles['theta1']
  t2 = angles['theta2']
  t3 = angles['theta3']
  
#  return axisAngleToQuaternion(a3, (0,0,1)) * axisAngleToQuaternion(a2, (1,0,0)) * axisAngleToQuaternion(a1, (0,0,1))
#  
  a  =  cos(t2/2.0)*cos((t1 + t3)/2.0)
  A1 =  sin(t2/2.0)*cos((t1 - t3)/2.0)
  A2 =  sin(t2/2.0)*sin((t1 - t3)/2.0)
  A3 =  cos(t2/2.0)*sin((t1 + t3)/2.0)
  
#  a  =  cos(t2/2.0)*cos((t1 + t3)/2.0)
#  A1 =  -sin(t2/2.0)*cos((t1 - t3)/2.0)
#  A2 =  -sin(t2/2.0)*sin((t1 - t3)/2.0)
#  A3 =  cos(t2/2.0)*sin((t1 + t3)/2.0)
  
  return quaternion(a, A1, A2, A3)
  
#  c1 = cos(0.5*a1)
#  c2 = cos(0.5*a2)
#  c3 = cos(0.5*a3)
#  s1 = sin(0.5*a1)
#  s2 = sin(0.5*a2)
#  s3 = sin(0.5*a3)
#  
#  return quaternion(c1*c2*c3 - s1*c2*s3,
#                    c1*s2*c3 + s1*s2*s3,
#                    c1*s2*s3 - s1*s2*c3,
#                    c1*c2*s3 + s1*c2*c3)

class quaternion:
  def __init__(self, *data):
    """
      By definition is a real scalar number (a) and a vector (\vec{A})
      
      Reference:
        Altmann, Simon (1986) Rotations, Quaternions, and Double Groups
      
      Inputs:
        len(data) == 0: Null quaternion [0,0,0,0]
        len(data) == 1: Real quaternion [a,0,0,0]
        len(data) == 2: [a, A]
        len(data) == 3: Pure quaternion [0, Ax, Ay, Az]
        len(data) == 4: [a, Ax, Ay, Az]
    """
    
    if len(data) == 0:
      self._a = 0
      self._A = vectors.vector(0,0,0)
    elif len(data) == 1:
      self._a = data[0]
      self._A = vectors.vector(0,0,0)
    elif len(data) == 2:
      self._a = data[0]
      self._A = vectors.vector(data[1][0], data[1][1], data[1][2])
    elif len(data) == 3:
      self._a = 0
      self._A = vectors.vector(data[0], data[1], data[2])
    elif len(data) == 4:
      self._a = data[0]
      self._A = vectors.vector(data[1], data[2], data[3])
    
    #Convert the quaternion to a positive quaternion since q=-q
    self.positive()
    
  def __getitem__(self, index):
    """
      Return the coefficient of one of the four quaternion parameters
      
      Inputs:
        index: integer between 0 and 3
      
      Outputs:
        real value of the quaternion's coefficient
    """
    
    if index >= 0 and index <= 3:
      if index == 0:
        return self._a
      else:
        return self._A[index-1]
  
  def __setitem__(self, index, value):
    """
      Set a new value for a cofficient
      
      Inputs:
        index: integer between 0 and 3
        value: new real number value of the coefficient
    """
    
    if index >= 0 and index <= 3:
      if index == 0:
        self._a = value
      else:
        self._A[index-1] = value
  
  def __repr__(self):
    """
      Return a string with the four quaternion coefficients
    """
    return "[[%f, %f, %f, %f]]" % (self._a, self._A[0], self._A[1], self._A[2])
  
  def __mul__(self, other):
    """
      Multiply two quaternions or one quaternion and a scalar
      Multiplication of quaternions is not commutative (AB \neq BA)
      
      Multiplication is defined as
      = [ab - \vec{A}\bullet\vec{B}, a\vec{B} + b\vec{A} + \vec{A}\times\vec{B}]
      
      Reference:
        Altmann, Simon (1986) Rotations, Quaternions, and Double Groups
      
      Outputs:
        a quaternion
    """
    
    #TODO: Implement multiplication with the multiplication table
    
    qOut = quaternion()
    
    if isinstance(other, quaternion):
      qOut[0] = self._a * other._a - vectors.dot(self._A, other._A)
      
      v3 = vectors.cross(self._A, other._A)
      for i in [0,1,2]:
        qOut[i+1] = self._a * other._A[i] + other._a * self._A[i] + v3[i]
      
    elif isinstance(other, float) or isinstance(other, int):
      qOut[0] = other * self._a
      
      for i in [0,1,2]:
        qOut[i+1] = other * self._A[i]
    
    qOut.positive()
    return qOut

  def __rmul__(self, other):
    """
      Multiply two quaternions or one quaternion and a scaler
      Multiplication of quaternions is not commutative (AB \neq BA)
      
      Reference:
        Altmann, Simon (1986) Rotations, Quaternions, and Double Groups
      
      Outputs:
        a quaternion
    """
    
    qOut = quaternion()
    
    if isinstance(other, quaternion):
      qOut[0] = other._a * self._a - vectors.dot(other._A, self._A)
      
      v3 = vectors.cross(other._A, self._A)
      for i in [0,1,2]:
        qOut[i+1] = other._a * self._A[i] + self._a * other._A[i] + v3[i]
      
    elif isinstance(other, float) or isinstance(other, int):
      qOut[0] = other * self._a
      
      for i in [0,1,2]:
        qOut[i+1] = other * self._A[i]
    
    qOut.positive()
    return qOut
  
  def __div__(self, other):
    """
      Division of quaternion by scalar or other quaternion
      
      Reference:
        Altmann, Simon (1986) Rotations, Quaternions, and Double Groups
      
      Outputs:
        a quaternion
      
    """
    
    if isinstance(other, float) or isinstance(other, int): #inverse scalar product
      return (1/other)*self
    elif isinstance(other, quaternion):
      return self*(~other)
  
  def __rdiv__(self, other):
    pass
  #TODO: Fix __rdiv__
  
  def __add__(self, other):
    """
      Addition of two quaternions
      
      References:
        Altmann, Simon (1986) Rotations, Quaternions, and Double Groups
      
      Outputs:
        A quaternion
    """
    
    return quaternion(self._a + other._a
                      , self._A[0] + other._A[0]
                      , self._A[1] + other._A[1]
                      , self._A[2] + other._A[2])
  
  def __sub__(self, other):
    """
      Substraction of two quaternions
      
      References:
        Altmann, Simon (1986) Rotations, Quaternions, and Double Groups
      
      Outputs:
        A quaternion
    """
    
    return quaternion(self._a - other._a
                      , self._A[0] - other._A[0]
                      , self._A[1] - other._A[1]
                      , self._A[2] - other._A[2])
  
  def __abs__(self):
    """
      Return the norm of the quaternion
      
      The norm is defined by the multiplication of the quaternion by its conjugate
      = \sqrt{A\conj{A}}
      or
      = \sqrt{a^2 + A_x^2 + A_y^2 + A_z^2}
      
      References:
        Martin Baker (2008) Euclidean Space, \url{http://www.euclideansplace.com}
        Altmann, Simon (1986) Rotations, Quaternions, and Double Groups
      
      Outputs:
        a float
      
    """
    
    return pow(self._a**2 + self._A[0]**2 + self._A[1]**2 + self._A[2]**2, 0.5)
#    return pow((self * self.conjugate())()[0], 0.5)
  
  def __invert__(self):
    """
      Return the inverse of the quaternion
      
      For non-normalized quaternion, the inverse is defined as
      = \conj{A} \norm{A}^{-2}
      
      References:
        Altmann, Simon (1986) Rotations, Quaternions, and Double Groups
      
      Outputs:
        a quaternion
    """
    
    if self.isnormalized():
      return self.conjugate()
    else:
      return self.conjugate() / abs(self)
  
#  def __neg__(self):
#    """
#      Return the negative of the quaternion
#    """
#    
#    return quaternion(-self._a, -self._A[0], -self._A[1], -self._A[2])
  
  def __eq__(self, other):
    """
      Comparison of quaternion
      Check if two quaternion are equal, i.e. if their coefficients are equal
      
      Outputs:
        True: equal
        False: not equal
    """
    
    if abs(self._a - other._a) < zeroPrecision and \
       abs(self._A[0] - other._A[0]) < zeroPrecision and \
       abs(self._A[1] - other._A[1]) < zeroPrecision and \
       abs(self._A[2] - other._A[2]) < zeroPrecision:
      return True
    else:
      return False
  
  def __hash__(self):
    """
      Return a unique integer to be use as dictionary key
      
      References:
        http://effbot.org/zone/python-hash.htm
      
      Outputs:
        an integer
    """
    a = hash(self._a)
    b = hash(self._A[0])* 10**len(str(a))
    c = hash(self._A[1])* 10**(len(str(a))+len(str(b)))
    d = hash(self._A[2])* 10**(len(str(a))+len(str(b))+len(str(c)))
    
    value = a + b + c + d
    
    return value
  
  def conjugate(self):
    """
      Return the conjugate of the quaternion
      
      The conjugate is defined by the inverse of the vector part of the quaternion
      = (a, -\vec{A})
      
      References:
        Altmann, Simon (1986) Rotations, Quaternions, and Double Groups
      
      Outputs:
        a quaternion
    """
    
    return quaternion(self._a
                      , -self._A[0]
                      , -self._A[1]
                      , -self._A[2])
  
  def isnormalized(self):
    """
      Check if the quaternion is normalized
      
      References:
        Altmann, Simon (1986) Rotations, Quaternions, and Double Groups
      
      Outputs:
        a bool
    """
    
    if abs(abs(self) - 1) < zeroPrecision:
      return True
    else:
      return False
  
  
  
  def normalize(self):
    """
      Normalize quaternion
      
      References:
        Confuted (2008) Rotations in Three Dimensions, Part V: Quaternions, \url{http://cpprogramming.com/tutorial/3d/quaternions.html}
      
      Outputs:
        a quaternion
    """
    
    norm = abs(self)
    return quaternion(self._a/norm
                      , self._A[0]/norm
                      , self._A[1]/norm
                      , self._A[2]/norm)
  
  def vector(self):
    return self._A
  
  def scalar(self):
    return self._a
  
  def positive(self):
    """
      Return a positive quaternion: The first non-zero term is positive
      
      Outputs:
        a quaternion
    """
    
    output = []
    
    qIndices = [self._a, self._A[0], self._A[1], self._A[2]]
    
    for qIndice in qIndices:
      if abs(qIndice) < zeroPrecision:
        continue
      elif qIndice < zeroPrecision:
        self._a = -self._a
        self._A = -self._A
        return
      elif qIndice > zeroPrecision:
        break
    
#    return self
  
  def toAxisAngle(self):
    """
      Give the axis angle or euler-rodrigues (\phi, \vec{n}) representation of the quaternion
      
      References:
        Martin Baker (2008) Euclidean Space, \url{http://www.euclideansplace.com}
      
      Outputs:
        a tuple of \phi (in rad) and \vec{n}
    """
    
    qCalc = self.normalize()
    
    phi = 2.0*acos(qCalc._a)
    
    denominator = pow(1-qCalc._a**2, 0.5)
    
    n = []
    for i in [0,1,2]:
      if abs(denominator) < zeroPrecision:
        n.append(self._A[i])
      else:
        n.append(self._A[i]/denominator)
    
    return (phi, n)
  
  def toMatrix(self):
    """
      Give the SO3 matrix for the quaternion
      
      References:
        Martin Baker (2008) Euclidean Space, \url{http://www.euclideansplace.com}
      
      Outputs:
        a list of 3 lists of 3 items
    """
    
    qCalc = self.normalize()
    assert qCalc.isnormalized()
    
    q0 = qCalc._a
    q1 = qCalc._A[0]
    q2 = qCalc._A[1]
    q3 = qCalc._A[2]
    
    #Orilib
    m = matrices.matrix([[q0**2 + q1**2 - q2**2 - q3**2, 2*(q1*q2 + q0*q3), 2*(q1*q3 - q0*q2)],
                         [2*(q1*q2 - q0*q3), q0**2 - q1**2 + q2**2 - q3**2, 2*(q2*q3 + q0*q1)],
                         [2*(q1*q3 + q0*q2), 2*(q2*q3 - q0*q1), q0**2 - q1**2 - q2**2 + q3**2]])
    
    #Assert that the matrix is orthogonal
    assert m.isSU3()
    
    return m

#  def toMatrixBaker(self):
#    qCalc = self.normalize()
#    assert qCalc.isnormalized()
#    
#    q0 = qCalc._a
#    q1 = qCalc._A[0]
#    q2 = qCalc._A[1]
#    q3 = qCalc._A[2]
#    
#    #Morawiec & Martin Baker
#    m1 = matrices.matrix([[q0**2 + q1**2 - q2**2 - q3**2, 2*(q1*q2 - q0*q3), 2*(q1*q3 + q0*q2)],
#                         [2*(q1*q2 + q0*q3), q0**2 - q1**2 + q2**2 - q3**2, 2*(q2*q3 - q0*q1)],
#                         [2*(q1*q3 - q0*q2), 2*(q2*q3 + q0*q1), q0**2 - q1**2 - q2**2 + q3**2]])
#    
#    #Assert that the matrix is orthogonal
#    assert m1.isSU3()
#    
#    return m1
#  
#  def toMatrixOrilib(self):
#    qCalc = self.normalize()
#    assert qCalc.isnormalized()
#    
#    q0 = qCalc._a
#    q1 = qCalc._A[0]
#    q2 = qCalc._A[1]
#    q3 = qCalc._A[2]
#    #Orilib
#    m2 = matrices.matrix([[q0**2 + q1**2 - q2**2 - q3**2, 2*(q1*q2 + q0*q3), 2*(q1*q3 - q0*q2)],
#                         [2*(q1*q2 - q0*q3), q0**2 - q1**2 + q2**2 - q3**2, 2*(q2*q3 + q0*q1)],
#                         [2*(q1*q3 + q0*q2), 2*(q2*q3 - q0*q1), q0**2 - q1**2 - q2**2 + q3**2]])
#    
#    #Assert that the matrix is orthogonal
#    assert m2.isSU3()
#    
#    return m2
  
  def toEulerAngles(self):
    """
      Give the euler angles for the quaternion 
      
      Reference:
        Inspired by Martin Baker (2008) Euclidean Space, \url{http://www.euclideansplace.com}
      
      Outputs:
        a eulers
    """
    
    qCalc = self.normalize()
    assert qCalc.isnormalized()
    
    q0 = qCalc._a
    q1 = qCalc._A[0]
    q2 = qCalc._A[1]
    q3 = qCalc._A[2]
    
    x = (q0**2 + q3**2)*(q1**2 + q2**2)
    
    if abs(x) < zeroPrecision**2:
      if abs(q1) < zeroPrecision and abs(q2) < zeroPrecision:
        theta1 = atan2(2*q0*q3, q0**2 - q3**2)
        theta2 = 0
        theta3 = 0
      elif abs(q0) < zeroPrecision and abs(q3) < zeroPrecision:
        theta1 = atan2(2*q1*q2, q1**2 - q2**2)
        theta2 = pi
        theta3 = 0
    else:
      theta1 = atan2(q3,q0) + atan2(q2, q1)
      theta2 = acos(1 - 2*q1**2 - 2*q2**2)
      theta3 = atan2(q3,q0) - atan2(q2, q1)
      assert abs(theta2 - acos(q0**2 - q1**2 -q2**2 + q3**2)) < zeroPrecision
    
    assert abs(2*atan2(sqrt(q1**2+q2**2), sqrt(q0**2+q3**2)) - theta2) < zeroPrecision
    
    e1 = eulers.eulers(theta1, theta2, theta3)
    return e1.positive()
  
  def toTuple(self):
    """
      Return the 4 coefficients of the quaternion as a tuple
      
      Inputs:
        None
        
      Outputs:
        a tuple
    """
    return (self._a, self._A[0], self._A[1], self._A[2])
  
def rotate(qIn, qRotations):
  """
    Return the input quaternion (qIn) by all the rotation quaternion in qRotations
    Order of rotation: qRotations[0], qRotations[1], qRotations[2], ...
    
    Inputs:
      qIn: a quaternion to be rotated
      qRotations: a list of quaternions defining rotations
    
    Outputs:
      a quaternion
  """
  qOut = qIn
  
  for qRotation in qRotations:
    qOut = qRotation * qOut * qRotation.conjugate()
  
  return qOut

def similar(q1, q2, angularPrecision):
  if abs(q1._a - q2._a) < cos(angularPrecision/2.0) and \
      abs(q1._A[0] - q2._A[0]) < sin(angularPrecision/2.0) and \
      abs(q1._A[1] - q2._A[1]) < sin(angularPrecision/2.0) and \
      abs(q1._A[2] - q2._A[2]) < sin(angularPrecision/2.0):
    return True
  else:
    return False

if __name__ == '__main__':
  q = quaternion(-0.76889497255171957, 0.44598102610297174, 0.12136262327573186, -0.44178338494387015)
  print q.toEulerAngles()
  print q.toAxisAngle()
  
  