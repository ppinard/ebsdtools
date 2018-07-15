#!/usr/bin/env python
"""
================================================================================
:mod:`vectors` -- Vectorial algebra.
================================================================================

.. module:: vectors
   :synopsis: Vectorial algebra.

.. inheritance-diagram:: mathtools.algebra.vectors

"""

# Script information for the file.
__author__ = "Philippe T. Pinard"
__email__ = "philippe.pinard@gmail.com"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2010 Philippe T. Pinard"
__license__ = "GPL v3"

# Standard library modules.
from math import sqrt
import copy
from functools import total_ordering
from collections import Sequence

# Third party modules.

# Local modules.
from mathtools.rotation.trigo import acos

# Globals and constants variables.

class VectorOperationError(ArithmeticError):
    """
    Exception raised when incorrect operations are done using vectors.
    
    """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

@total_ordering
class Vector(Sequence):
    
    def __init__(self, *data):
        """
        A vector of n elements.
        
        **Parameters**
        
          elements of the vector as a tuple, a list or a sequence of numbers
        
        **Examples** ::
        
          v = vector([1,2,3])
          v = vector((1,2,3))
          v = vector(1,2,3)
        """
        vector = []

        if len(data) == 0:
            vector = []
        elif len(data) == 1:
            if isinstance(data[0], list):
                vector = data[0]
            elif isinstance(data[0], tuple):
                vector = list(data[0])
            else:
                vector = [data[0]]
        elif len(data) > 1:
            vector = []
            for datum in data:
                vector.append(datum)

        self._vector = vector

    def __cmp__(self, other):
        """
        Comparison of two vectors.
        
          * If the two vectors have the same length, the smaller vector
            is the one whose the sum of its components is smaller.
          * If the two vectors have different length, the vector with
            the smallest length is the smallest
        """
        c = cmp(len(self), len(other))
        if c != 0:
            return c

        return cmp(sum(self), sum(other))

    def __ge__(self, other):
        return cmp(self, other) >= 0

    def __gt__(self, other):
        return cmp(self, other) > 0

    def __le__(self, other):
        return cmp(self, other) <= 0

    def __lt__(self, other):
        return cmp(self, other) < 0

    def __add__(self, other):
        """
        Addition (``+``) of two vectors
        """
        if len(self) != len(other):
            raise VectorOperationError, "Cannot add vectors of different lengths"

        output = copy.deepcopy(self)
        for i in range(len(output)):
            output[i] += other[i]

        return output

    def __neg__(self):
        """
        Negation of a vector.
        
        **Example:** ::
        
          v = vector(1,2,3)
          -v == vector(-1,-2,-3) # Equivalent
        """
        output = copy.deepcopy(self)
        for i in range(len(output)):
            output[i] = -output[i]

        return output

    def __sub__(self, other):
        """
        Subtraction (``-``) of two vectors.
        """
        return self + (-other)

    def __mul__(self, other):
        """
        Multiplication (``*``) by a scalar.
        """
        # Scalar multiplication
        if isinstance(other, float) or isinstance(other, int):
            output = copy.deepcopy(self)
            for i in range(len(output)):
                output[i] *= other

            return output

        # Vector multiplication
        # answer = v^T * v
        elif isinstance(other, Vector):
            assert len(self) == len(other), \
                  "Both vectors must have the same length to be multiplied"

        #TODO: Replace by dot product
            answer = 0
            for i in range(len(self)):
                answer += self[i] * other[i]

            return answer

        else:
            raise TypeError, \
                "Vector can only be multiplied by a scalar value or another vector"

    def __rmul__(self, other):
        return self * other

    def __div__(self, other):
        """
        Division (``/``) by a scalar.
        """
        return self * (1.0 / float(other))

    def clear(self):
        """
        Clear all the items in the vector.
        """
        for i in range(len(self)):
            self[i] = 0.0

    def norm(self):
        """
        Return the norm of the vector.
        
        :rtype: :class:`float`
        """
        return sqrt(dot(self, self))

    def normalize(self):
        """
        .. seealso:: :func:`vectors.normalize`
        
        **Examples**::
        
          >>> v = vectors.Vector(0,4,3)
          >>> v.normalize()
          >>> print v
          >>> (0, 0.8, 0.6)
        """
        type(self).__init__(self, *normalize(self))

    def positive(self):
        """
        .. seealso:: :func:`vectors.positive`
        """
        type(self).__init__(self, *positive(self))

class Vector3D(Vector):
    def __init__(self, *data):
        """
        A three-dimensional vector.
        
          v = vector([1,2,3])
          v = vector((1,2,3))
          v = vector(1,2,3)
        
        """
        if len(data) == 0:
            raise ValueError, "The vector must have a length of 3"
        elif len(data) == 1:
            if len(data[0]) != 3:
                raise ValueError, "The vector must have a length of 3"
        elif len(data) != 3:
            raise ValueError, "The vector must have a length of 3"

        Vector.__init__(self, *data)

def normalize(vector):
    """
    Return a normalized vector ``vector.norm == 1``.
    
    :arg vector: a vector
    :type vector: :class:`vectors.Vector`
    
    :rtype: :class:`vectors.Vector`
    
    """
    norm = vector.norm()

    output = copy.deepcopy(vector)
    output /= norm

    return output

def positive(vector):
    """
    Return a positive vector:
    a vector where its first non-zero component is positive.
    
    :arg vector: a vector
    :type vector: :class:`vectors.Vector`
    
    :rtype: :class:`vectors.Vector`
    
    """
    output = copy.deepcopy(vector)

    for i in range(len(vector)):
        if vector[i] == 0:
            continue
        elif vector[i] < 0:
            output = -output
            break
        else:
            break

    return output

def dot(v1, v2):
    """
    Return the dot product between *v1* and *v2*.
    
    :arg v1: the first vector
    :type v1: :class:`vectors.Vector`
    
    :arg v2: the second vector
    :type v2: :class:`vectors.Vector`
    
    :rtype: :class:`float`
    
    """
    product = 0.0

    if len(v1) == len(v2):
        for i in range(len(v1)):
            product += v1[i] * v2[i]
    else:
        raise VectorOperationError, "The dot product cannot be perfomed on vectors of different lengths"

    return product

def cross(v1, v2):
    """
    Return the cross product between *v1* and *v2*.
    Only valid for :class:`vectors.Vector3D`
    
    :arg v1: the first vector
    :type v1: :class:`vectors.Vector3D`
    
    :arg v2: the second vector
    :type v2: :class:`vectors.Vector3D`
    
    :rtype: :class:`vectors.Vector3D`
    
    """
    if len(v1) == len(v2) and len(v1) == 3:
        return Vector3D(v1[1] * v2[2] - v1[2] * v2[1],
                        v1[2] * v2[0] - v1[0] * v2[2],
                        v1[0] * v2[1] - v1[1] * v2[0])
    else:
        raise TypeError, "Both vectors must be a Vector3D"

def angle(v1, v2):
    """
    Return the angle in radians between *v1* and *v2*.
    
    :arg v1: the first vector
    :type v1: :class:`vectors.Vector`
    
    :arg v2: the second vector
    :type v2: :class:`vectors.Vector`
    
    :return: angle in radians
    :rtype: :class:`float`
    
    """
    costheta = directioncosine(v1, v2)
    return acos(costheta)

def directioncosine(v1, v2):
    """
    Return the direction cosine between *v1* and *v2*.
    
    :arg v1: the first vector
    :type v1: :class:`vectors.Vector`
    
    :arg v2: the second vector
    :type v2: :class:`vectors.Vector`
    
    :rtype: :class:`float`
    
    """
    costheta = dot(v1, v2) / (v1.norm() * v2.norm())
    return costheta

def tripleproduct(v1, v2, v3):
    """
    Return the triple product of *v1*, *v2* and *v3*.
    Only valid for ``len(v1) == len(v2) == 3``.
    
    :arg v1: the first vector
    :type v1: :class:`vectors.Vector3D`
    
    :arg v2: the second vector
    :type v2: :class:`vectors.Vector3D`
    
    :arg v3: the third vector
    :type v3: :class:`vectors.Vector3D`
    
    :rtype: :class:`float`
    
    """
    return dot(cross(v1, v2), v3)

def almostequal(v1, v2, places=7):
    """
    Return *True* if the vectors *v1* and *v2* are almost equal.
    
    :arg v1: a vector
    :type v1: :class:`vectors.Vector`
    
    :arg v2: a vector
    :type v2: :class:`vectors.Vector`
    
    :arg places: given number of decimal places (``default=7``)
    :type places: :class:`int`
    
    :rtype: :class:`bool`
    
    """
    equality = True

    equality = equality and len(v1) == len(v2)

    for i in range(len(v1)):
        try:
            equality = equality and round(abs(v2[i] - v1[i]), places) == 0
        except IndexError:
            equality = False

    return equality

if __name__ == '__main__': #pragma: no cover
    import DrixUtilities.Runner as Runner
    Runner.Runner().run(runFunction=None)
