#!/usr/bin/env python
"""
================================================================================
:mod:`quaternions` -- Quaternions algebra.
================================================================================

.. module:: quaternions
   :synopsis: Quaternions algebra.

.. inheritance-diagram:: mathtools.rotation.quaternions

"""

# Script information for the file.
__author__ = "Philippe T. Pinard"
__email__ = "philippe.pinard@gmail.com"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2010 Philippe T. Pinard"
__license__ = "GPL v3"

# Standard library modules.
from math import sin, cos, pi, acos, atan2, sqrt

# Third party modules.

# Local modules.
import mathtools.algebra.vectors as vectors
import mathtools.rotation.matrices as matrices
import  mathtools.rotation.eulers as eulers

# Globals and constants variables.

def axisangle_to_quaternion(*data):
    """
    Convert an axis angle :math:`(\\phi, \\vec{n})` to a quaternion.
    
    **Parameters**
    
      * ``len(data) == 2``: :math:`(\\phi, \\vec{n})`
      * ``len(data) == 4``: :math:`(\\phi, n_x, n_y, n_z)`
    
    **Equations**
    
      * :math:`a = \\cos{\\frac{\\phi}{2}}`
      * :math:`A_x = n_x \\sin{\\frac{\\phi}{2}}`
      * :math:`A_y = n_y \\sin{\\frac{\\phi}{2}}`
      * :math:`A_z = n_z \\sin{\\frac{\\phi}{2}}`
    
    **References**
    
      Martin Baker (2008) Euclidean Space, http://www.euclideansplace.com
    
    :rtype: :class:`quaternions.Quaternion`
    """
    if len(data) == 2:
        n = vectors.Vector3D(data[1][0], data[1][1], data[1][2])
    elif len(data) == 4:
        n = vectors.Vector3D(data[1], data[2], data[3])

    n.normalize()
    multiplier = sin(0.5 * data[0])

    return Quaternion(cos(0.5 * data[0]),
                      n[0] * multiplier,
                      n[1] * multiplier,
                      n[2] * multiplier)

def so3matrix_to_quaternion(m):
    """
    Convert a SO3 matrix to a quaternion.
    
    :arg m: a SO3 matrix
    :type m: :class:`matrices.SpecialOrthogonalMatrix3D`
    
    **Equations**
    
      * :math:`a = 0.5\\sqrt{1 + m00 + m11 + m22}`
      * :math:`A_x = \\frac{m21 - m12}{4a}`
      * :math:`A_y = \\frac{m02 - m20}{4a}`
      * :math:`A_z = \\frac{m10 - m01}{4a}`
    
    **References**
    
      Martin Baker (2008) Euclidean Space, http://www.euclideansplace.com
    
      Wikipedia, Rotation representation (mathematics),
      http://en.wikipedia.org/wiki/Rotation_representation_(mathematics)_
    
    :rtype: :class:`quaternions.Quaternion`
    """
    assert matrices.is_special_orthogonal(m)

    A = []
    w = 0.5 * sqrt(m[0][0] + m[1][1] + m[2][2] + 1)

    if round(abs(w), 7) != 0.0:
        #Morawiec & orilib
        A.append((m[1][2] - m[2][1]) / (4 * w))
        A.append((m[2][0] - m[0][2]) / (4 * w))
        A.append((m[0][1] - m[1][0]) / (4 * w))
    else:
        A.append(sqrt((m[0][0] + 1) / 2.0))
        A.append(sqrt((m[1][1] + 1) / 2.0))
        A.append(sqrt((m[2][2] + 1) / 2.0))

        s = A.index(max(A))
        for i in range(len(A)):
            if i != s:
                if m[i][s] < 0:
                    A[i] *= -1
        #        if round(abs(m[i][i])) != 0.0:
        #          A[i] *= m[i][i] / abs(m[i][i])

    return Quaternion(w, A)

def eulerangles_to_quaternion(angles):
    """
    Convert Euler angles :math:`(\\theta_1, \\theta_2, \\theta_3)`
      to a quaternion.
    
    The Euler angles have to be in line with Bunge definition of
    the euler angles.
    
      * :math:`R(\\theta_3\\vec{k})R(\\theta_2\\vec{i})R(\\theta_1\\vec{k})`
      * Where the rotation is performed from
          :math:`\\theta_1\\rightarrow\\theta_2\\rightarrow\\theta_3`
    
    :arg angles: euler angles
    :type angles: :class:`eulers.Eulers`
    
    **References**
    
      Altmann, Simon (1986) Rotations, Quaternions,
      and Double Groups
    
      Rollett, Tony (2008) Advanced Characterization and
      Microstructural Analysis
    
    :rtype: :class:`quaternions.Quaternion`
    """
    t1 = angles['theta1']
    t2 = angles['theta2']
    t3 = angles['theta3']

    a = cos(t2 / 2.0) * cos((t1 + t3) / 2.0)
    A1 = sin(t2 / 2.0) * cos((t1 - t3) / 2.0)
    A2 = sin(t2 / 2.0) * sin((t1 - t3) / 2.0)
    A3 = cos(t2 / 2.0) * sin((t1 + t3) / 2.0)

    return Quaternion(a, A1, A2, A3)

class Quaternion(object):
    def __init__(self, *data):
        """
        By definition, a Quaternion is a real scalar number
        (:math:`a`) and a vector (:math:`\\vec{A}`):
        :math:`\\mathcal{A} = \\llbracket a, \\vec{A} \\rrbracket`.
        
        **Parameters**
          =============   ===============   ==================
          ``len(data)``   data              Description
          =============   ===============   ==================
          0               [0,0,0,0]         Null Quaternion
          1               [a,0,0,0]         Real Quaternion
          2               [a, A]            Quaternion
          3               [0, Ax, Ay, Az]   Pure Quaternion
          4               [a, Ax, Ay, Az]   Quaternion
          =============   ===============   ==================
        
        **References**
        
          Altmann, Simon (1986) Rotations, Quaternions, and Double Groups
        
        .. note:: The Quaternion is always converted to a positive Quaternion
                  (see :func:`quaternions.positive`)
                  since for rotation :math:`q = -q`.
        """
        if len(data) == 0:
            self._a = 0
            self._A = vectors.Vector3D(0, 0, 0)
        elif len(data) == 1:
            self._a = data[0]
            self._A = vectors.Vector3D(0, 0, 0)
        elif len(data) == 2:
            self._a = data[0]
            self._A = vectors.Vector3D(data[1][0], data[1][1], data[1][2])
        elif len(data) == 3:
            self._a = 0
            self._A = vectors.Vector3D(data[0], data[1], data[2])
        elif len(data) == 4:
            self._a = data[0]
            self._A = vectors.Vector3D(data[1], data[2], data[3])

        # Convert the Quaternion to a positive Quaternion since q=-q
        self.positive()

    def __getitem__(self, index):
        """
        Return the coefficient of one of the four quaternion parameters.
        
        :arg index: integer between 0 and 3
        :type index: :class:`int`
        
        :rtype: :class:`float`
        
        **Examples** ::
        
          >>> q = Quaternion(1,2,3,4)
          >>> print q[2]
          >>> 3.0
        """
        if index >= 0 and index <= 3:
            if index == 0:
                return self._a
            else:
                return self._A[index - 1]
        else:
            raise IndexError, "Index must range between 0 and 3"

    def __setitem__(self, index, value):
        """
        Set a new value for a coefficient.
        
        :arg index: integer between 0 and 3
        :type index: :class:`int`
        
        :arg value: new real number value of the coefficient
        :type value: :class:`float`
        
        **Examples** ::
        
          >>> q = Quaternion(1,2,3,4)
          >>> q[3] = 5
          >>> print q
          >>> [[1.0, 2.0, 3.0, 5.0]]
        """
        if index >= 0 and index <= 3:
            if index == 0:
                self._a = value
            else:
                self._A[index - 1] = value
        else:
            raise IndexError, "Index must range between 0 and 3"

    def __repr__(self):
        """
        .. note:: When ``str(q)`` is called.
        
        Return a string with the four quaternion coefficients.
        
        :rtype: :class:`str`
        
        **Examples** ::
        
          >>> q = Quaternion(1,2,3,4)
          >>> print q
          >>> [[1.0, 2.0, 3.0, 4.0]]
        """
        return "[[%f, %f, %f, %f]]" % (self._a, self._A[0], self._A[1], self._A[2])

    def __mul__(self, other):
        """
        Multiply two quaternions or one quaternion and a scalar.
        Multiplication of quaternions is not commutative
        (:math:`\\mathcal{A}\\mathcal{B} \\neq \\mathcal{B}\\mathcal{A}`).
        
        **Equations**
        
          * scalar product
              :math:`a\\llbracket b, \\vec{B} \\rrbracket = \\llbracket a, \\vec{0} \\rrbracket \\llbracket b, \\vec{B} \\rrbracket} = \\llbracket ab, a\\vec{B} \\rrbracket`
          * quaternion product
              :math:`\\mathcal{AB} = \\llbracket a, \\vec{A} \\rrbracket \\llbracket b, \\vec{B} \\rrbracket = \\llbracket ab-\\vec{A}\\bullet\\vec{B}, a\\vec{B}+b\\vec{A}+\\vec{A}\\times\\vec{B} \\rrbracket`
        
        **References**
        
          Altmann, Simon (1986) Rotations, Quaternions, and Double Groups
        
        :rtype: :class:`quaternions.Quaternion`
        """
        #TODO: Implement multiplication with the multiplication table
        qOut = Quaternion()

        if isinstance(other, Quaternion):
            qOut[0] = self._a * other._a - vectors.dot(self._A, other._A)

            v3 = vectors.cross(self._A, other._A)
            for i in [0, 1, 2]:
                qOut[i + 1] = self._a * other._A[i] + other._a * self._A[i] + v3[i]

        elif isinstance(other, float) or isinstance(other, int):
            qOut[0] = other * self._a

            for i in [0, 1, 2]:
                qOut[i + 1] = other * self._A[i]

        qOut.positive()
        return qOut

    def __rmul__(self, other):
        """
        .. seealso:: :meth:`quaternions.Quaternion.__mul__`
        """
        return self * other

    def __div__(self, other):
        """
        Division of quaternion by scalar or other quaternion.
        
        **Equations**
        
          * scalar division
            :math:`\\frac{\\llbracket a, \\vec{A} \\rrbracket}{a} = \\frac{1}{a} \\llbracket a, \\vec{A} \\rrbracket`
          * quaternion division (as defined by :math:`\\frac{\\mathcal{A}}{\\mathcal{B}} \\equiv \\mathcal{A}\\mathcal{B}^{-1} \\neq \\mathcal{B}^{-1}\\mathcal{A}`)
            :math:`\\llbracket a, \\vec{A} \\rrbracket \\llbracket b, \\vec{B} \\rrbracket^{-1} = \\llbracket ab + \\vec{A}\\bullet\\vec{B}, b\\vec{A} - a\\vec{B} - \\vec{A}\\times\\vec{B} \\rrbracket`
        
        **References**
        
          Altmann, Simon (1986) Rotations, Quaternions, and Double Groups
        
        :rtype: :class:`quaternions.Quaternion`
        """
        if isinstance(other, float) or isinstance(other, int): #inverse scalar product
            return (1 / other) * self
        elif isinstance(other, Quaternion):
            return self * (~other)

    def __rdiv__(self, other):
        raise NotImplementedError

    def __add__(self, other):
        """
        Addition of two quaternions.
        
        **Equations**
        
          :math:`\\llbracket a, \\vec{A} \\rrbracket + \\llbracket b, \\vec{B} \\rrbracket = \\llbracket a + b, \\vec{A} + \\vec{B} \\rrbracket`
        
        **References**
        
          Altmann, Simon (1986) Rotations, Quaternions, and Double Groups
        
        :rtype: :class:`quaternions.Quaternion`
        """
        return Quaternion(self._a + other._a,
                          self._A[0] + other._A[0],
                          self._A[1] + other._A[1],
                          self._A[2] + other._A[2])

    def __sub__(self, other):
        """
        Substraction of two quaternions.
        
        **Equations**
        
          :math:`\\llbracket a, \\vec{A} \\rrbracket - \\llbracket b, \\vec{B} \\rrbracket = \\llbracket a - b, \\vec{A} - \\vec{B} \\rrbracket`
        
        **References**
        
          Altmann, Simon (1986) Rotations, Quaternions, and Double Groups
        
        :rtype: :class:`quaternions.Quaternion`
        """
        return Quaternion(self._a - other._a,
                          self._A[0] - other._A[0],
                          self._A[1] - other._A[1],
                          self._A[2] - other._A[2])

    def __abs__(self):
        """
        .. note:: When ``abs(q)`` is called.
        
        Return the norm of the Quaternion: :math:`{\\left\| \\mathcal{A} \\right\|`.
        
        **Equations**
        
          :math:`\\left\| \\mathcal{A} \\right\| = \\sqrt{\\mathcal{A} \\mathcal{A}^\\ast} = \\sqrt{a^2 + A_x^2 + A_y^2 + A_z^2}`
        
        **References**
        
          Martin Baker (2008) Euclidean Space, http://www.euclideansplace.com
        
          Altmann, Simon (1986) Rotations, Quaternions, and Double Groups
        
        :rtype: :class:`float`
        """
        return pow(self._a ** 2 + self._A[0] ** 2 + self._A[1] ** 2 + self._A[2] ** 2, 0.5)
        #    return pow((self * self.conjugate())()[0], 0.5)

    def __invert__(self):
        """
        .. note:: When ``~q`` is called.
        
        Return the inverse of the Quaternion: :math:`\\mathcal{A}^{-1}`.
        
        **Equations**
        
          * For non-normalized quaternion
            :math:`\\mathcal{A}^{-1} = A^\\ast \\left\| A \\right\|^{-2}`
          * For normalized quaternion
            :math:`\\mathcal{A}^{-1} = \\mathcal{A}^\\ast`
        
        **References**
        
          Altmann, Simon (1986) Rotations, Quaternions, and Double Groups
        
        :rtype: :class:`quaternions.Quaternion`
        """
        if self.isnormalized():
            return self.conjugate()
        else:
            return self.conjugate() / abs(self)

    def __eq__(self, other):
        """
        .. note:: When ``q1 == q2`` is called.
        
        Comparison of quaternion.
        Check if two quaternion are equal, i.e. if their coefficients are equal.
        
        :rtype: :class:`bool`
        """
        equality = True

        equality = equality and self._a == other._a
        equality = equality and self._A[0] == other._A[0]
        equality = equality and self._A[1] == other._A[1]
        equality = equality and self._A[2] == other._A[2]

        return equality

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        """
        Return a unique integer to be use as dictionary key.
        
        **References**
        
          http://effbot.org/zone/python-hash.htm
        
        :rtype: :class:`int`
        """
        a = hash(self._a)
        b = hash(self._A[0]) * 10 ** len(str(a))
        c = hash(self._A[1]) * 10 ** (len(str(a)) + len(str(b)))
        d = hash(self._A[2]) * 10 ** (len(str(a)) + len(str(b)) + len(str(c)))

        value = a + b + c + d

        return value

    def get_vector(self):
        """
        Return the vector part of the Quaternion: :math:`\\vec{A}`.
        
        :rtype: :class:`vectors.Vector3D`
        """
        return self._A

    def get_scalar(self):
        """
        Return the scalar part of the Quaternion: :math:`a`.
        
        :rtype: :class:`float`
        """
        return self._a

    def to_tuple(self):
        """
        Return the 4 coefficients of the Quaternion as a tuple.
        
        :rtype: :class:`tuple`
        """
        return (self._a, self._A[0], self._A[1], self._A[2])

    def to_list(self):
        """
        Return the 4 coefficients of the Quaternion as a list.
        
        :rtype: :class:`list`
        """
        return [self._a, self._A[0], self._A[1], self._A[2]]

    def to_axisangle(self):
        """
        Give the axis angle or euler-rodrigues :math:`(\\phi, \\vec{n})`
        representation of the quaternion.
        
        **References**
        
          Martin Baker (2008) Euclidean Space, http://www.euclideansplace.com
        
        :rtype: a :class:`tuple` of :math:`\\phi` (in rad) and :math:`\\vec{n}`
        """
        qcalc = normalize(self)

        phi = 2.0 * acos(qcalc._a)

        denominator = pow(1 - qcalc._a ** 2, 0.5)

        n = []
        for i in [0, 1, 2]:
            if round(abs(denominator), 7) == 0.0:
                n.append(self._A[i])
            else:
                n.append(self._A[i] / denominator)

        return (phi, n)

    def to_so3matrix(self):
        """
        Give the SO3 matrix for the quaternion.
        
        **References**
        
          Martin Baker (2008) Euclidean Space http://www.euclideansplace.com
        
        :rtype: :class:`matrices.SpecialOrthogonalMatrix3D`
        """
        qcalc = normalize(self)

        q0 = qcalc._a
        q1 = qcalc._A[0]
        q2 = qcalc._A[1]
        q3 = qcalc._A[2]

        #Orilib
        m_list = [[q0 ** 2 + q1 ** 2 - q2 ** 2 - q3 ** 2, 2 * (q1 * q2 + q0 * q3), 2 * (q1 * q3 - q0 * q2)],
                  [2 * (q1 * q2 - q0 * q3), q0 ** 2 - q1 ** 2 + q2 ** 2 - q3 ** 2, 2 * (q2 * q3 + q0 * q1)],
                  [2 * (q1 * q3 + q0 * q2), 2 * (q2 * q3 - q0 * q1), q0 ** 2 - q1 ** 2 - q2 ** 2 + q3 ** 2]]
        m = matrices.SpecialOrthogonalMatrix3D(m_list)

        return m

    def to_eulerangles(self):
        """
        Give the euler angles for the quaternion.
        
        **References**
        
          Martin Baker (2008) Euclidean Space http://www.euclideansplace.com
        
        :rtype: :class:`eulers.Eulers`
        """
        qcalc = normalize(self)

        q0 = qcalc._a
        q1 = qcalc._A[0]
        q2 = qcalc._A[1]
        q3 = qcalc._A[2]

        x = (q0 ** 2 + q3 ** 2) * (q1 ** 2 + q2 ** 2)

        if round(abs(x), 7 * 2) == 0.0:
            if round(abs(q1), 7) == 0.0 and round(abs(q2), 7) == 0.0:
                theta1 = atan2(2 * q0 * q3, q0 ** 2 - q3 ** 2)
                theta2 = 0
                theta3 = 0
            elif round(abs(q0), 7) == 0.0 and round(abs(q3), 7) == 0.0:
                theta1 = atan2(2 * q1 * q2, q1 ** 2 - q2 ** 2)
                theta2 = pi
                theta3 = 0
        else:
            theta1 = atan2(q3, q0) + atan2(q2, q1)
            theta2 = acos(1 - 2 * q1 ** 2 - 2 * q2 ** 2)
            theta3 = atan2(q3, q0) - atan2(q2, q1)
            assert round(abs(theta2 - acos(q0 ** 2 - q1 ** 2 - q2 ** 2 + q3 ** 2)), 7) == 0.0

        assert round(abs(2 * atan2(sqrt(q1 ** 2 + q2 ** 2), sqrt(q0 ** 2 + q3 ** 2)) - theta2)) == 0.0

        e1 = eulers.Eulers(theta1, theta2, theta3)
        e1.positive()
        return e1

    def norm(self):
        """
        .. seealso:: :func:`quaternions.norm`
        """
        return norm(self)

    def conjugate(self):
        """
        .. seealso:: :func:`quaternions.conjugate`
        """
        return conjugate(self)

    def isnormalized(self):
        """
        .. seealso:: :func:`quaternions.isnormalized`
        """
        return isnormalized(self)

    def normalize(self):
        """
        .. seealso:: :func:`quaternions.isnormalized`
        """
        return normalize(self)

    def positive(self):
        """
        .. seealso:: :func:`quaternions.positive`
        """
        positive(self)

def norm(q):
    """
    .. seealso:: :meth:`quaternions.Quaternion.__abs__`
    """
    return abs(q)

def conjugate(q):
    """
    Return the conjugate of the quaternion: :math:`\\mathcal{A}^\\ast`.
    
    :arg q: a quaternion
    :type q: :class:`quaternions.Quaternion`
    
    **Equations**
    
      The conjugate is defined by the inverse of the vector part of
      the quaternion: :math:`\\mathcal{A}^\\ast = \\llbracket a, \\vec{A} \\rrbracket^\\ast = \\llbracket a, -\\vec{A} \\rrbracket`
    
    **References**
    
      Altmann, Simon (1986) Rotations, Quaternions, and Double Groups
    
    :rtype: :class:`quaternions.Quaternion`
    """
    return Quaternion(q._a, -q._A[0], -q._A[1], -q._A[2])

def isnormalized(q):
    """
    Check if the quaternion is normalized.
    
    :arg q: a quaternion
    :type q: :class:`quaternions.Quaternion`
    
    **Equations**
    
      :math:`\\left\| \\mathcal{A} \\right\| = 1`
    
    **References**
    
      Altmann, Simon (1986) Rotations, Quaternions, and Double Groups
    
    :rtype: :class:`bool`
    """
    if round(abs(abs(q) - 1.0), 7) == 0:
        return True
    else:
        return False

def normalize(q):
    """
    Normalize quaternion.
    
    :arg q: a quaternion
    :type q: :class:`quaternions.Quaternion`
    
    **Equations**
    
      :math:`\\frac{\\mathcal{A}}{\\left\| \\mathcal{A} \\right\|}`
    
    **References**
    
      Confuted (2008) Rotations in Three Dimensions
      , Part V: Quaternions, http://cpprogramming.com/tutorial/3d/quaternions.html
    
    :rtype: :class:`quaternions.Quaternion`
    """
    norm = abs(q)
    return Quaternion(q._a / norm, q._A[0] / norm, q._A[1] / norm, q._A[2] / norm)

def positive(q):
    """
    Make the quaternion positive.
    The first non-zero term is positive.
    
    :arg q: a quaternion
    :type q: :class:`quaternions.Quaternion`
    """
    qindices = q.to_list()

    for qindice in qindices:
        if round(abs(qindice), 7) == 0.0:
            continue
        elif qindice < 0.0:
            q._a = -q._a
            q._A = -q._A
            return
        elif qindice > 0.0:
            break

def rotate(qin, qrotations):
    """
    Return the input quaternion (*qin*) by all the rotation
    quaternion in *qrotations*.
    Order of rotation: ``qrotations[0]``, ``qrotations[1]``
    , ``qrotations[2]``, ...
    
    :arg qin: a quaternion to be rotated
    :type qin: :class:`quaternions.Quaternion`
    
    :arg qrotations: a list of quaternions defining rotations
    :type qrotations: a list of :class:`quaternions.Quaternion`
    
    **Equations**
    
      :math:`\\mathcal{A^\prime} = \\mathcal{B} \\mathcal{A} \\mathcal{B}^\\ast`
    
    :rtype: :class:`quaternions.Quaternion`
    """
    qout = qin

    for qrotation in qrotations:
        qout = qrotation * qout * qrotation.conjugate()

    return qout

def misorientation(q1, q2):
    """
    Calculate the misorientation (in rad) between two quaternions.
    
    :arg q1, q2: the quaternions
    :type q1, q2: :class:`quaternions.Quaternion`
    
    **Equations**
    
      :math:`\\omega = 2\\arccos{\\left(\\mathcal{A}\\cdot\\mathcal{B}\\right)}`
    
    :rtype: :class:`float`
    """
    dotproduct = q1[0] * q2[0] + q1[1] * q2[1] + q1[2] * q2[2] + q1[3] * q2[3]

    return 2 * acos(dotproduct)

def almostequal(q1, q2, places=7):
    """
    Return *True* if the quaternions *q1* and *q2* are almost equal.
    
    :arg q1: a quaternion
    :type q1: :class:`quaternions.Quaternion`
    
    :arg q2: a quaternion
    :type q2: :class:`quaternions.Quaternion`
    
    :arg places: given number of decimal places (``default=7``)
    :type places: :class:`int`
    
    :rtype: :class:`bool`
    """
    equality = True

    equality = equality and round(abs(q2._a - q1._a), places) == 0

    for i in range(3):
        equality = equality and round(abs(q2._A[i] - q1._A[i]), places) == 0

    return equality

if __name__ == '__main__': #pragma: no cover
    import DrixUtilities.Runner as Runner
    Runner.Runner().run(runFunction=None)
