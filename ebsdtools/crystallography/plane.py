#!/usr/bin/env python
"""
================================================================================
:mod:`plane` -- A lattice plane.
================================================================================

.. module:: plane
  :synopsis: A lattice plane

.. inheritance-diagram:: ebsdtools.crystallography.plane

"""

# Script information for the file.
__author__ = "Philippe T. Pinard"
__email__ = "philippe.pinard@gmail.com"
__version__ = "0.1"

# Standard library modules.
try:
    from fractions import gcd
except ImportError: # For jython 2.5
    def gcd(a, b):
        """Calculate the Greatest Common Divisor of a and b.
        
        Unless b==0, the result will have the same sign as b (so that when
        b is divided by it, the result comes out positive).
        """
        while b:
            a, b = b, a % b
        return a
import operator

# Third party modules.

# Local modules.

# Globals and constants variables.

class Plane(object):

    def __init__(self, *args):
        """
        Define a plane of a lattice.
        The plane can be given using the Miller indices or the Bravais indices.
        A plane given in Bravais indices is automatically converted to a Miller
        indices plane.
        
        :arg h, k, i, l: indices
        :type h, k, i, l: :class:`int`
        """
        if len(args) == 3:
            indices = args
        elif len(args) == 4:
            indices = bravais_to_miller(args)
        else:
            raise AttributeError("A plane is defined by 3 or 4 indices")

        self._indices = tuple(indices)

        assert self._indices != (0, 0, 0), "A plane cannot be a zero vector"

    def __hash__(self):
        """
        Hash algorithm for a tuple.
        
        **References**
        
          http://effbot.org/zone/python-hash.htm
        
        """
        return hash(self._indices)

    def __repr__(self):
        args = (self.__class__.__name__,) + self.indices
        return '<%s(%s, %s, %s)>' % args

    def __getitem__(self, index):
        return self._indices[index]

    def simplify(self):
        """
        Simplify the indices so that the largest common integer of the
        plane's indices is 1.
        """
        commondenominator = gcd(self[0], gcd(self[1], self[2]))

        if self[0] < 0:
            commondenominator = -abs(commondenominator)
        else:
            commondenominator = abs(commondenominator)

        return self.__class__(*map(operator.truediv, self._indices,
                                   [commondenominator] * 3))

    @property
    def indices(self):
        return self._indices

    @property
    def indices_bravais(self):
        return miller_to_bravais(self._indices)

def miller_to_bravais(plane):
    """
    Convert Miller indices to Bravais-Miller indices.
    
    :math:`i = -(h+k)`
    
    :arg plane: a plane (hkl)
    :type plane: :class:`list`
    
    :rtype: :class:`list`
    """
    assert len(plane) == 3

    return [plane[0], plane[1], -(plane[0] + plane[1]), plane[2]]

def bravais_to_miller(plane):
    """
    Convert Bravais-Miller indices to Miller indices.
    
    :math:`(h, k, i, l) \\leftarrow (h, k, l)`
    
    :arg plane: a plane (hkil)
    :type plane: :class:`list`
    
    :rtype: :class:`list`
    """
    assert len(plane) == 4

    return [plane[0], plane[1], plane[3]]
