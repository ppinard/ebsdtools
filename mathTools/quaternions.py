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
from math import sin, cos, pi, acos, atan2, sqrt

# Third party modules.

# Local modules.
import vectors

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
  
  norm = n.norm()
  multiplier = sin(0.5*data[0])
  
  return quaternion(cos(0.5*data[0])
                      , n[0] * multiplier / norm
                      , n[1] * multiplier / norm
                      , n[2] * multiplier / norm)

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
      m: list of list forming a 3D matrix
        the matrix has a special orthogonal (SU3): det(matrix) = 1) and Tr(matrix) > 0
    
    Outputs:
      a quaternion
  """
  #TODO: Modify tex accordingly
  
  trace = 1 + m[0][0] + m[1][1] + m[2][2]
  
  if trace > 0:
    s = 0.5 / sqrt(trace)
    w = 0.25 / s
    x = (m[2][1] - m[1][2]) * s
    y = (m[0][2] - m[2][0]) * s
    z = (m[1][0] - m[0][1]) * s
  else:
    if (m[0][0] > m[1][1]) and (m[0][0] > m[2][2]):
      s = sqrt(1.0 + m[0][0] - m[1][1] - m[2][2] ) * 2 
      w = (m[1][2] - m[2][1]) / s
      x= 0.25 * s
      y= (m[0][1] + m[1][0]) / s
      z= (m[0][2] + m[2][0]) / s
    elif (m[1][1] > m[2][2]): 
      s = sqrt(1.0 + m[1][1] - m[0][0] - m[2][2]) * 2
      w = (m[0][2] - m[2][0]) / s
      x = (m[0][1] + m[1][0]) / s 
      y = 0.25 * s
      z = (m[1][2] + m[2][1]) / s 
    else: 
      s = sqrt(1.0 + m[2][2] - m[0][0] - m[1][1]) * 2
      w = (m[0][1] - m[1][0]) / s
      x = (m[0][2] + m[2][0]) / s 
      y = (m[1][2] + m[2][1]) / s 
      z = 0.25 * s
  
  return quaternion(w,x,y,z)
  
def eulerAnglesToQuaternion(*angles):
  """
    Convert Euler angles ($\theta_1$, $\theta_2$, $\theta_3$) to a quaternion
    
    The Euler angles have to be in line with Bunge definition of the euler angles
      $R(\theta_3\vec{k})R(\theta_2\vec{i})R(\theta_1\vec{k})$
      Where the rotation is performed from $\theta_1\rightarrow\theta_2\rightarrow_3$
    
    References:
      Inspired by Altmann, Simon (1986) Rotations, Quaternions, and Double Groups and
                  Rollett, Tony (2008) Advanced Characterization and Microstructural Analysis
    
    Inputs:
      len(angles) == 1: a tuple or list of three angles (in rad)
      len(angles) == 3: three angles (in rad)
    
    Outputs:
      a quaternion
  """

  if len(angles) == 1:
    a1 = float(angles[0][0])
    a2 = float(angles[0][1])
    a3 = float(angles[0][2])
  elif len(angles) == 3:
    a1 = float(angles[0])
    a2 = float(angles[1])
    a3 = float(angles[2])
  
  c1 = cos(0.5*a1)
  c2 = cos(0.5*a2)
  c3 = cos(0.5*a3)
  s1 = sin(0.5*a1)
  s2 = sin(0.5*a2)
  s3 = sin(0.5*a3)
  
  return quaternion(c1*c2*c3 - s1*c2*s3,
                    c1*s2*c3 + s1*s2*s3,
                    c1*s2*s3 - s1*s2*c3,
                    c1*c2*s3 + s1*c2*c3)

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
      Return a tuple with the four quaternion coefficients
    """
    return "[[%f, %f, %f, %f]]" % (self._a, self._A[0], self._A[1], self._A[2])
  
  def __mul__(self, other):
    """
      Multiply two quaternions or one quaternion and a scaler
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
      return self.conjugate() * pow(abs(self), -2)
  
  def __eq__(self, other):
    """
      Comparison of quaternion
      Check if two quaternion are equal, i.e. if their coefficients are equal
      
      Outputs:
        True: equal
        False: not equal
    """
    
    if (self._a - other._a) < 0.0001 and \
       (self._A[0] - other._A[0]) < 0.0001 and \
       (self._A[1] - other._A[1]) < 0.0001 and \
       (self._A[2] - other._A[2]) < 0.0001:
      return True
    else:
      return False
  
  
  
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
    
    if abs(self) == 1:
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
      if denominator == 0:
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
    
    a = qCalc._a
    A = qCalc._A
    
    return [[1 - 2*A[1]**2 - 2*A[2]**2, 2*A[0]*A[1] - 2*A[2]*a    , 2*A[0]*A[2] + 2*A[1]*a   ],
            [2*A[0]*A[1] + 2*A[2]*a   , 1 - 2*A[0]**2 - 2*A[2]**2 , 2*A[1]*A[2] - 2*A[0]*a   ],
            [2*A[0]*A[2] - 2*A[1]*a   , 2*A[1]*A[2] + 2*A[0]*a    , 1 - 2*A[0]**2 - 2*A[1]**2]]
  
  def toEulerAngles(self):
    """
      Give the euler angles for the quaternion 
      
      Reference:
        Inspired by Martin Baker (2008) Euclidean Space, \url{http://www.euclideansplace.com}
      
      Outputs:
        a tuple of three angles (\theta_1, \theta_2, \theta_3)
    """
    
    qCalc = self.normalize()
    
    if qCalc._A[0] == 0 and qCalc._A[1] == 0:
      theta1 = 2*atan2(qCalc._A[2], qCalc._a)
      theta2 = 0
      theta3 = 0
    elif qCalc._A[0]**2 + qCalc._A[1]**2 > 0.99999 and qCalc._A[0]**2 + qCalc._A[1]**2 < 1.000001:
      theta1 = 2*atan2(-qCalc._A[1], qCalc._A[0])
      theta2 = pi
      theta3 = 0
    else:
      theta1 = atan2(qCalc._A[0]*qCalc._A[2] - qCalc._A[1]*qCalc._a, qCalc._A[1]*qCalc._A[2] + qCalc._A[0]*qCalc._a)
      theta3 = atan2(qCalc._A[0]*qCalc._A[2] + qCalc._A[1]*qCalc._a, qCalc._A[0]*qCalc._a + qCalc._A[1]*qCalc._A[2])
      theta2 = acos(1 - 2*qCalc._A[0]**2 - 2*qCalc._A[1]**2)
    
    return (theta1, theta2, theta3)

  
if __name__ == '__main__':
  h = 0
  k = 1
  l = 1
  tilt = 70 * pi / 180
  
  q1 = axisAngleToQuaternion(-tilt, (1,0,0))
  v1 = quaternion(0, (h,k,l))
  r1 = q1 * v1 * q1.conjugate()
  
  print r1
  print r1.toAxisAngle()
  
  h70 = h
  k70 = k*cos(tilt) + l*sin(tilt)
  l70 = -k*sin(tilt) + l*cos(tilt)
  
  print h70, k70, l70