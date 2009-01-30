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
from EBSDTools.mathTools.mathExtras import zeroPrecision, _acos

def axisAngleToQuaternion(*data):
  """
  Convert an axis angle :math:`(\\phi, \\vec{n})` to a quaternion
  
  **Parameters:** 
    * ``len(data) == 2``: :math:`(\\phi, \\vec{n})`
    * ``len(data) == 4``: :math:`(\\phi, n_x, n_y, n_z)`
  
  **Equations:**
    * :math:`a = \\cos{\\frac{\\phi}{2}}`
    * :math:`A_x = n_x \\sin{\\frac{\\phi}{2}}`
    * :math:`A_y = n_y \\sin{\\frac{\\phi}{2}}`
    * :math:`A_z = n_z \\sin{\\frac{\\phi}{2}}`
      
  **Reference:**
    Martin Baker (2008) Euclidean Space, `<http://www.euclideansplace.com>`_
    
  :rtype: :class:`quaternion <EBSDTools.mathTools.quaternions.quaternion>`
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
  
  :arg m: a SO3 matrix
  :type m: :class:`matrix <EBSDTools.mathTools.matrices.matrix>`
  
  **Equations:**
    * :math:`a = 0.5\\sqrt{1 + m00 + m11 + m22}`
    * :math:`A_x = \\frac{m21 - m12}{4a}`
    * :math:`A_y = \\frac{m02 - m20}{4a}`
    * :math:`A_z = \\frac{m10 - m01}{4a}`
    
  **Reference:**
    Martin Baker (2008) Euclidean Space, `<http://www.euclideansplace.com>`_
    
  :rtype: :class:`quaternion <EBSDTools.mathTools.quaternions.quaternion>`
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
  Convert Euler angles :math:`(\\theta_1, \\theta_2, \\theta_3)` to a quaternion
    
  The Euler angles have to be in line with Bunge definition of the euler angles.
    * :math:`R(\\theta_3\\vec{k})R(\\theta_2\\vec{i})R(\\theta_1\\vec{k})`
    * Where the rotation is performed from :math:`\\theta_1\\rightarrow\\theta_2\\rightarrow\\theta_3`
  
  :arg angles: euler angles
  :type angles: :class:`eulers <EBSDTools.mathTools.eulers.eulers>`
  
  **References:**
    Inspired by Altmann, Simon (1986) Rotations, Quaternions, and Double Groups and 
      Rollett, Tony (2008) Advanced Characterization and Microstructural Analysis
    
  :rtype: :class:`quaternion <EBSDTools.mathTools.quaternions.quaternion>`
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
    By definition, a quaternion is a real scalar number (:math:`a`) and a vector (:math:`\\vec{A}`): :math:`\\quaternionL{A} = \\quaternion{a}{\\vec{A}}`
    
    **Parameters:**
      =============   ===============   ==================
      ``len(data)``   data              Description
      =============   ===============   ==================
      0               [0,0,0,0]         Null quaternion
      1               [a,0,0,0]         Real quaternion
      2               [a, A]            quaternion
      3               [0, Ax, Ay, Az]   Pure quaternion
      4               [a, Ax, Ay, Az]   quaternion
      =============   ===============   ==================
    
    **Reference:**
      Altmann, Simon (1986) Rotations, Quaternions, and Double Groups
    
    .. note:: The quaternion is always converted to a positive quaternion (see :func:`positive() <EBSDTools.mathTools.quaternions.quaternion.positive>`) since for rotation :math:`q = -q`.
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
    Return the coefficient of one of the four quaternion parameters.
      
    :arg index: integer between 0 and 3
    :type index: int
      
    :rtype: float
    
    **Examples:** ::
      
      >>> q = quaternion(1,2,3,4)
      >>> print q[2]
      >>> 3.0
    """
    
    if index >= 0 and index <= 3:
      if index == 0:
        return self._a
      else:
        return self._A[index-1]
  
  def __setitem__(self, index, value):
    """
    Set a new value for a cofficient.
    
    :arg index: integer between 0 and 3
    :type index: int
    
    :arg value: new real number value of the coefficient
    :type value: float
    
    **Examples:** ::
      
      >>> q = quaternion(1,2,3,4)
      >>> q[3] = 5
      >>> print q
      >>> [[1.0, 2.0, 3.0, 5.0]]
    """
    
    if index >= 0 and index <= 3:
      if index == 0:
        self._a = value
      else:
        self._A[index-1] = value
  
  def __repr__(self):
    """
    .. note:: When ``str(q)`` is called.
    
    Return a string with the four quaternion coefficients.
    
    :rtype: string
    
    **Examples:** ::
      
      >>> q = quaternion(1,2,3,4)
      >>> print q
      >>> [[1.0, 2.0, 3.0, 4.0]]
    """
    return "[[%f, %f, %f, %f]]" % (self._a, self._A[0], self._A[1], self._A[2])
  
  def __mul__(self, other):
    """
    Multiply two quaternions or one quaternion and a scalar.
    Multiplication of quaternions is not commutative (:math:`\\quaternionL{A}\\quaternionL{B} \\neq \\quaternionL{B}\\quaternionL{A}`).
      
    **Equations:**
      * scalar product
          :math:`a\\quaternion{b}{\\vec{B}} = \\quaternion{a}{\\vec{0}}\\quaternion{b}{\\vec{B}}=\\quaternion{ab}{a\\vec{B}}`
      * quaternion product 
          :math:`\\quaternionL{AB} = \\quaternion{a}{\\vec{A}}\\quaternion{b}{\\vec{B}} = \\quaternion{ab-\\vec{A}\\bullet\\vec{B}}{a\\vec{B}+b\\vec{A}+\\vec{A}\\times\\vec{B}}`
    
    **Reference:**
      Altmann, Simon (1986) Rotations, Quaternions, and Double Groups
      
    :rtype: :class:`quaternion <EBSDTools.mathTools.quaternions.quaternion>`
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
    .. seealso:: :func:`__mul__ <EBSDTools.mathTools.quaternions.quaternion.__mul__>`
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
    Division of quaternion by scalar or other quaternion.
    
    **Equations:**
      * scalar division
          :math:`\\frac{\\quaternion{a}{\\vec{A}}}{a} = \\frac{1}{a} \\quaternion{a}{\\vec{A}}`
      * quaternion division (as defined by :math:`\\frac{\\quaternionL{A}}{\\quaternionL{B}} \\equiv \\quaternionL{A}\\quaternionL{B}^{-1} \\neq \\quaternionL{B}^{-1}\\quaternionL{A}`)
          :math:`\\quaternion{a}{\\vec{A}}\\quaternion{b}{\\vec{B}}^{-1} = \\quaternion{ab + \\vec{A}\\bullet\\vec{B}}{b\\vec{A} - a\\vec{B} - \\vec{A}\\times\\vec{B}}`
    
    **Reference:**
      Altmann, Simon (1986) Rotations, Quaternions, and Double Groups
    
    :rtype: :class:`quaternion <EBSDTools.mathTools.quaternions.quaternion>`
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
    Addition of two quaternions.
    
    **Equations:**
      :math:`\\quaternion{a}{\\vec{A}} + \\quaternion{b}{\\vec{B}} = \\quaternion{a + b}{\\vec{A} + \\vec{B}}`
      
    **References:**
      Altmann, Simon (1986) Rotations, Quaternions, and Double Groups
      
    :rtype: :class:`quaternion <EBSDTools.mathTools.quaternions.quaternion>`
    """
    
    return quaternion(self._a + other._a
                      , self._A[0] + other._A[0]
                      , self._A[1] + other._A[1]
                      , self._A[2] + other._A[2])
  
  def __sub__(self, other):
    """
    Substraction of two quaternions.
    
    **Equations:**
      :math:`\\quaternion{a}{\\vec{A}} - \\quaternion{b}{\\vec{B}} = \\quaternion{a - b}{\\vec{A} - \\vec{B}}`
    
    **References:**
      Altmann, Simon (1986) Rotations, Quaternions, and Double Groups
    
    :rtype: :class:`quaternion <EBSDTools.mathTools.quaternions.quaternion>`
    """
    
    return quaternion(self._a - other._a
                      , self._A[0] - other._A[0]
                      , self._A[1] - other._A[1]
                      , self._A[2] - other._A[2])
  
  def __abs__(self):
    """
    .. note:: When ``abs(q)`` is called.
    
    Return the norm of the quaternion: :math:`\\norm{\\quaternionL{A}}`.
    
    **Equations:**
      :math:`\\norm{\\quaternionL{A}} = \\sqrt{\\quaternionL{A}\\conj{\\quaternionL{A}}} = \\sqrt{a^2 + A_x^2 + A_y^2 + A_z^2}`
      
    **References:**
      Martin Baker (2008) Euclidean Space, `<http://www.euclideansplace.com>`_
      Altmann, Simon (1986) Rotations, Quaternions, and Double Groups
      
    :rtype: float
    """
    
    return pow(self._a**2 + self._A[0]**2 + self._A[1]**2 + self._A[2]**2, 0.5)
#    return pow((self * self.conjugate())()[0], 0.5)
  
  def __invert__(self):
    """
    .. note:: When ``~q`` is called.
    
    Return the inverse of the quaternion: :math:`\\quaternionL{A}^{-1}`.
    
    **Equations:**
      * For non-normalized quaternion
          :math:`\\quaternionL{A}^{-1} = \\conj{A} \\norm{A}^{-2}`
      * For normalized quaternion
          :math:`\\quaternionL{A}^{-1} = \\conj{\\quaternionL{A}}`
      
    **References:**
      Altmann, Simon (1986) Rotations, Quaternions, and Double Groups
    
    :rtype: :class:`quaternion <EBSDTools.mathTools.quaternions.quaternion>`
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
    .. note:: When ``q1 == q2`` is called.
    
    Comparison of quaternion.
    Check if two quaternion are equal, i.e. if their coefficients are equal.
      
    :rtype: bool
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
    Return a unique integer to be use as dictionary key.
      
    **References:**
      `<http://effbot.org/zone/python-hash.htm>`_
      
    :rtype: int
    """
    
    a = hash(self._a)
    b = hash(self._A[0])* 10**len(str(a))
    c = hash(self._A[1])* 10**(len(str(a))+len(str(b)))
    d = hash(self._A[2])* 10**(len(str(a))+len(str(b))+len(str(c)))
    
    value = a + b + c + d
    
    return value
  
  def conjugate(self):
    """
    Return the conjugate of the quaternion: :math:`\\conj{\\quaternionL{A}}`
    
    **Equations:**
      The conjugate is defined by the inverse of the vector part of the quaternion: :math:`\\conj{\\quaternionL{A}} = \\conj{\\quaternion{a}{\\vec{A}}} = \\quaternion{a}{-\\vec{A}}`
      
    **References:**
      Altmann, Simon (1986) Rotations, Quaternions, and Double Groups
    
    :rtype: :class:`quaternion <EBSDTools.mathTools.quaternions.quaternion>`
    """
    
    return quaternion(self._a
                      , -self._A[0]
                      , -self._A[1]
                      , -self._A[2])
  
  def isnormalized(self):
    """
    Check if the quaternion is normalized.
    
    **Equations:**
      :math:`\\norm{\\quaternionL{A}} = 1`
      
    **References:**
      Altmann, Simon (1986) Rotations, Quaternions, and Double Groups
    
    :rtype: bool
    """
    
    if abs(abs(self) - 1) < zeroPrecision:
      return True
    else:
      return False
  
  
  
  def normalize(self):
    """
    Normalize quaternion.
    
    **Equations:**
      :math:`\\frac{\\quaternionL{A}}{\\norm{\\quaternionL{A}}}`
    
    **References:**
      Confuted (2008) Rotations in Three Dimensions, Part V: Quaternions, `<http://cpprogramming.com/tutorial/3d/quaternions.html>`_
      
    :rtype: :class:`quaternion <EBSDTools.mathTools.quaternions.quaternion>`
    """
    
    norm = abs(self)
    return quaternion(self._a/norm
                      , self._A[0]/norm
                      , self._A[1]/norm
                      , self._A[2]/norm)
  
  def positive(self):
    """
    Return a positive quaternion: The first non-zero term is positive
      
    :rtype: :class:`quaternion <EBSDTools.mathTools.quaternions.quaternion>`
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
  
  def vector(self):
    """
    Return the vector part of the quaternion: :math:`\\vec{A}`.
    
    :rtype: :class:`vector <EBSDTools.mathTools.vectors.vector>`
    """
    
    return self._A
  
  def scalar(self):
    """
    Return the scalar part of the quaternion: :math:`a`.
    
    :rtype: float
    """
    
    return self._a
  
  def toTuple(self):
    """
    Return the 4 coefficients of the quaternion as a tuple.
      
    :rtype: typle
    """
    return (self._a, self._A[0], self._A[1], self._A[2])
  
  def toAxisAngle(self):
    """
    Give the axis angle or euler-rodrigues :math:`(\\phi, \\vec{n})` representation of the quaternion.
      
    **References:**
      Martin Baker (2008) Euclidean Space, `<http://www.euclideansplace.com>`_
      
    :rtype: a tuple of :math:`\\phi` (in rad) and :math:`\\vec{n}`
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
    Give the SO3 matrix for the quaternion.
      
    **References:**
      Martin Baker (2008) Euclidean Space, `<http://www.euclideansplace.com>`_
      
    :rtype: :class:`matrix <EBSDTools.mathTools.matrices.matrix>`
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
    Give the euler angles for the quaternion.
      
    **Reference:**
      Inspired by Martin Baker (2008) Euclidean Space, `<http://www.euclideansplace.com>`_
    
    :rtype: :class:`eulers <EBSDTools.mathTools.eulers.eulers>`
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
  
  
  
def rotate(qIn, qRotations):
  """
  Return the input quaternion (*qIn*) by all the rotation quaternion in *qRotations*.
  Order of rotation: ``qRotations[0]``, ``qRotations[1]``, ``qRotations[2]``, ...
  
  :arg qIn: a quaternion to be rotated
  :type qIn: :class:`quaternion <EBSDTools.mathTools.quaternions.quaternion>`
  
  :arg qRotations: a list of quaternions defining rotations
  :type qRotations: a list of :class:`quaternion <EBSDTools.mathTools.quaternions.quaternion>`
  
  **Equations:**
    :math:`\\quaternionL{A^\prime} = \\quaternionL{B}\\quaternionL{A}\\conj{\\quaternionL{B}}`
  
  :rtype: :class:`quaternion <EBSDTools.mathTools.quaternions.quaternion>`
  """
  qOut = qIn
  
  for qRotation in qRotations:
    qOut = qRotation * qOut * qRotation.conjugate()
  
  return qOut

def misorientation(q1, q2):
  """
  Calculate the misorientation (in rad) between two quaternions.
  
  :arg q1, q2: the quaternions 
  :type q1, q2: :class:`quaternion <EBSDTools.mathTools.quaternions.quaternion>`
  
  **Equations:**
    :math:`\\omega = 2\\arccos{\\left(\\quaternionL{A}\\cdot\\quaternionL{B}\\right)}`
    
  :rtype: float
  """
  
  dotProduct = q1[0]*q2[0] + q1[1]*q2[1] + q1[2]*q2[2] + q1[3]*q2[3]
  
  return 2*_acos(dotProduct)

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
  
  