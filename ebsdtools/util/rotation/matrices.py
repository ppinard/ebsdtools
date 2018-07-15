#!/usr/bin/env python
"""
================================================================================
:mod:`matrices` -- 3D matrices algebra.
================================================================================

.. module:: matrices
   :synopsis: 3D matrices algebra.

.. inheritance-diagram:: mathtools.rotation.matrices

"""

# Script information for the file.
__author__ = "Philippe T. Pinard"
__email__ = "philippe.pinard@gmail.com"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2010 Philippe T. Pinard"
__license__ = "GPL v3"

# Standard library modules.
import copy

# Third party modules.

# Local modules.
import mathtools.algebra.vectors as vectors

# Globals and constants variables.

class Matrix3D(object):
    def __init__(self, *data):
        """
        Define a 3x3 matrix.
        
        **Parameters**
          =============   =========================================
          ``len(data)``   Description
          =============   =========================================
          0               Zero matrix
          1               List of lists [[a,b,c], [d,e,f], [g,h,i]]
          3               Lists [a,b,c], [d,e,f], [g,h,i]
          9               a,b,c,d,e,f,g,h,i
          =============   =========================================
        
        """
        if len(data) == 0:
            self._m = [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
        elif len(data) == 1:
            self._m = data[0]
        elif len(data) == 3:
            self._m = [data[0], data[1], data[2]]
        elif len(data) == 9:
            self._m = [[data[0], data[1], data[2]],
                       [data[3], data[4], data[5]],
                       [data[6], data[7], data[8]]]

    def __getitem__(self, index):
        """
        Return the coefficient or row of the matrix.
        
        :arg index: integer between 0 and 2
        :type index: :class:`int`
        
        :rtype: :class:`float` or :class:`list`
        
        **Examples** ::
        
          >>> m = matrix([[1,2,3], [4,5,6], [7,8,9]])
          >>> print m[1][2]
          >>> 5
        """
        if index >= 0 and index <= 2:
            return self._m[index]

    def __repr__(self):
        """
        Return a string of the matrix.
        
        :rtype: :class:`str`
        """
        return "%f, %f, %f\n%f, %f, %f\n%f, %f, %f" % (self._m[0][0], self._m[0][1], self._m[0][2], self._m[1][0], self._m[1][1], self._m[1][2], self._m[2][0], self._m[2][1], self._m[2][2])

    def __mul__(self, other):
        """
        Multiply
        
          * two matrices
          * one matrix and a scalar.
          * one matrix and a :class:`vectors.Vector3D`
        
        Multiplication of matrices is not commutative
        (:math:`\\mathrm{A}\\mathrm{B} \\neq \\mathrm{B}\\mathrm{A}`)
        
        :rtype: :class:`matrices.Matrix3D`
        """
        # Matrix times matrix
        if isinstance(self, Matrix3D) and isinstance(other, Matrix3D):
            # Check type to set correct object for the output.
            if type(self) != type(other):
                m = Matrix3D()
            else:
                m = copy.deepcopy(self)
                m.clear()

            for i in range(3):
                for j in range(3):
                    for k in range(3):
                        m[i][j] += self._m[i][k] * other._m[k][j]

            return m

        # Matrix times Vector
        elif isinstance(other, vectors.Vector3D):
            v = vectors.Vector3D(0.0, 0.0, 0.0)

            for i in range(3):
                for j in range(3):
                    v[i] += self._m[i][j] * other[j]

            return v

        # Matrix * scalar
        elif isinstance(other, int) or isinstance(other, float):
            # Check type to set correct object for the output.
            # Only a multiplication by one can keep the type of the objet intact.
            if other == 1.0:
                return self
            else:
                m = Matrix3D()

            for i in range(3):
                for j in range(3):
                    m[i][j] = other * self._m[i][j]

            return m

        # Incorrect arguments
        else:
            raise TypeError, "Incorrect multiplier type"

    def __rmul__(self, other):
        return self * other

    def __eq__(self, other):
        """
        .. note:: When ``m1 == m2`` is called.
        
        Comparison of matrices.
        Check if two matrices are equal, i.e. if all their elements are equal
        
        :rtype: :class:`bool`
        
        """
        equality = True

        for i in range(3):
            for j in range(3):
                equality = equality and self._m[i][j] == other._m[i][j]

        return equality

    def __ne__(self, other):
        return not self == other

    def clear(self):
        """
        Clear all the items in the matrix.
        """
        for i in range(3):
            for j in range(3):
                self._m[i][j] = 0.0

    def to_list(self):
        """
        Return the matrix in a list form
        
        :rtype: :class:`list`
        """
        return self._m

    def det(self):
        """
        .. seealso:: :func:`matrices.det`
        """
        return det(self)

    def transpose(self):
        """
        .. seealso:: :func:`matrices.transpose`
        """
        type(self).__init__(self, transpose(self))

    def inverse(self):
        """
        .. seealso:: :func:`matrices.inverse`
        """
        type(self).__init__(self, inverse(self))

    def trace(self):
        """
        .. seealso:: :func:`matrices.trace`
        """
        return trace(self)

    def is_special_orthogonal(self):
        """
        .. seealso:: :func:`matrices.is_special_orthogonal`
        """
        return is_special_orthogonal(self)

class SpecialOrthogonalMatrix3D(Matrix3D):
    def __init__(self, *data):
        """
        Define a special orthogonal matrix.
        
        **Conditions**
        
          * :math:`\\mathrm{det}(\\mathrm{M}) = +1`
          * :math:`\\mathrm{M}^{-1} == \\mathrm{M}^T`
        
        **Parameters**
          =============   =========================================
          ``len(data)``   Description
          =============   =========================================
          0               Zero matrix
          1               List of lists [[a,b,c], [d,e,f], [g,h,i]]
          3               Lists [a,b,c], [d,e,f], [g,h,i]
          9               a,b,c,d,e,f,g,h,i
          =============   =========================================
        
        """
        Matrix3D.__init__(self, *data)

        if not is_special_orthogonal(self):
            raise TypeError, \
                    "The matrix cannot be considered a special orthogonal matrix"

SO3Matrix = SpecialOrthogonalMatrix3D

class IdentityMatrix3D(Matrix3D):
    def __init__(self):
        m = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        Matrix3D.__init__(self, m)

def det(m):
    """
    Return the determinant of the matrix: :math:`\\mathrm{det}(\\mathrm{M})`.
    
    :arg m: a matrix
    :type m: :class:`matrices.Matrix3D`
    
    :rtype: :class:`float`
    """
    a = m[0][0] * m[1][1] * m[2][2] + m[0][1] * m[1][2] * m[2][0] + m[0][2] * m[2][1] * m[1][0]
    b = m[0][0] * m[1][2] * m[2][1] + m[0][1] * m[2][2] * m[1][0] + m[0][2] * m[2][0] * m[1][1]

    return a - b

def transpose(m):
    """
    Return the transpose of the matrix: :math:`\\mathrm{M}^T`.
    
    :arg m: a matrix
    :type m: :class:`matrices.Matrix3D`
    
    :rtype: :class:`matrices.Matrix3D`
    """
    newm = copy.deepcopy(m)

    for i in range(3):
        for j in range(3):
            newm[i][j] = m[j][i]

    return newm

def inverse(m):
    """
    Return the inverse of the matrix: :math:`\\mathrm{M}^T`.
    
    :arg m: a matrix
    :type m: :class:`matrices.Matrix3D`
    
    :rtype: :class:`matrices.Matrix3D`
    
    **References**
    
      Algorithm from Alexander Thomas
        http://www.dr-lex.be/random/matrix_inv.html
    """
    determinant = det(m)
    if determinant == 0:
        raise ValueError, "Matrices with a determinant equal to 0 cannot be inverted"

    a11 = (m[2][2] * m[1][1] - m[2][1] * m[1][2]) / determinant
    a12 = (-(m[2][2] * m[0][1] - m[2][1] * m[0][2])) / determinant
    a13 = (m[1][2] * m[0][1] - m[1][1] * m[0][2]) / determinant

    a21 = (-(m[2][2] * m[1][0] - m[2][0] * m[1][2])) / determinant
    a22 = (m[2][2] * m[0][0] - m[2][0] * m[0][2]) / determinant
    a23 = (-(m[1][2] * m[0][0] - m[1][0] * m[0][2])) / determinant

    a31 = (m[2][1] * m[1][0] - m[2][0] * m[1][1]) / determinant
    a32 = (-(m[2][1] * m[0][0] - m[2][0] * m[0][1])) / determinant
    a33 = (m[1][1] * m[0][0] - m[1][0] * m[0][1]) / determinant

    newm = copy.deepcopy(m)
    newm._m = [[a11, a12, a13], [a21, a22, a23], [a31, a32, a33]]

    return newm

def trace(m):
    """
    Return the trace of the matrix: :math:`\\mathrm{Tr}(\\mathrm{M})`.
    
    :arg m: a matrix
    :type m: :class:`matrices.Matrix3D`
    
    :rtype: :class:`float`
    """
    return m[0][0] + m[1][1] + m[2][2]

def almostequal(m1, m2, places=7):
    """
    Return *True* if the matrices *m1* and *m2* are almost equal.
    
    :arg m1: a matrix
    :type m1: :class:`matrices.Matrix3D`
    
    :arg m2: a matrix
    :type m2: :class:`matrices.Matrix3D`
    
    :arg places: given number of decimal places (``default=7``)
    :type places: :class:`int`
    
    :rtype: :class:`bool`
    """
    equality = True

    for i in range(3):
        for j in range(3):
            equality = equality and round(abs(m2[i][j] - m1[i][j]), places) == 0

    return equality

def is_special_orthogonal(m):
    """
    Return *True* if the matrix can be considered as a special orthogonal matrix.
    
    .. seealso:: :class:`matrices.SpecialOrthogonalMatrix3D`
    """
    if round(det(m) - 1.0, 7) == 0 and almostequal(inverse(m), transpose(m)):
        return True
    else:
        return False

if __name__ == '__main__': #pragma: no cover
    import DrixUtilities.Runner as Runner
    Runner.Runner().run(runFunction=None)
