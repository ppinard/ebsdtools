#!/usr/bin/env python
"""
================================================================================
:mod:`plane` -- A lattice plane.
================================================================================

.. module:: plane
  :synopsis: A lattice plane
.. moduleauthor:: Philippe Pinard <philippe.pinard@mail.mcgill.ca>

.. inheritance-diagram:: plane

"""

# Script information for the file.
__author__ = "Philippe Pinard <philippe.pinard@mail.mcgill.ca>"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2009 Philippe Pinard"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = ""
__svnDate__ = ""
__svnId__ = ""

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

# Third party modules.

# Local modules.
import mathtools.algebra.vectors as vectors

# Globals and constants variables.

class Plane(vectors.Vector3D):
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
      vectors.Vector3D.__init__(self, args)
    elif len(args) == 4:
      plane = bravais_to_miller(args)
      vectors.Vector3D.__init__(self, plane)
    else:
      raise AttributeError, "A plane is defined by 3 or 4 indices"

    assert self != vectors.Vector3D(0, 0, 0), "A plane cannot be a zero vector"

  def __hash__(self):
    """
    Hash algorithm for a tuple.

    **References**

      http://effbot.org/zone/python-hash.htm

    """
    c_mul = lambda a, b: eval(hex((long(a) * b) & 0xFFFFFFFFL)[:-1])

    value = 0x345678
    for item in self:
      value = c_mul(1000003, value) ^ hash(item)
    value = value ^ len(self)
    if value == -1:
      value = -2
    return value

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

    vectors.Vector3D.__init__(self
                              , vectors.Vector3D.__div__(self
                                                         , commondenominator))

  def to_bravais(self):
    """
    Give the Bravais-Miller indices of the plane.
    """
    return miller_to_bravais(self)

def miller_to_bravais(plane):
  """
  Convert Miller indices to Bravais-Miller indices.

  :math:`i = -(h+k)`

  :arg plane: a plane (hkl)
  :type plane: :class:`list`

  :rtype: :class:`list`
  """
  assert len(plane) == 3

  return [plane[0]
          , plane[1]
          , -(plane[0] + plane[1])
          , plane[2]]

def bravais_to_miller(plane):
  """
  Convert Bravais-Miller indices to Miller indices.

  :math:`(h, k, i, l) \\leftarrow (h, k, l)`

  :arg plane: a plane (hkil)
  :type plane: :class:`list`

  :rtype: :class:`list`
  """
  assert len(plane) == 4

  return [plane[0]
          , plane[1]
          , plane[3]]

if __name__ == '__main__': #pragma: no cover
  import DrixUtilities.Runner as Runner
  Runner.Runner().run(runFunction=None)
