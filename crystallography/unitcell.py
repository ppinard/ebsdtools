#!/usr/bin/env python
"""
================================================================================
:mod:`unitcell` -- Lattice's unit cell.
================================================================================

.. module:: unitcell
   :synopsis: Lattice's unit cell.
.. moduleauthor:: Philippe Pinard <philippe.pinard@mail.mcgill.ca>

.. inheritance-diagram:: unitcell

"""

# Script information for the file.
__author__ = "Philippe Pinard (philippe.pinard@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2008-2009 Philippe Pinard"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = ""
__svnDate__ = ""
__svnId__ = ""

# Standard library modules.
from math import sin, cos, pi, sqrt

# Third party modules.

# Local modules.
from mathtools.rotation.trigo import acos
import mathtools.rotation.matrices as matrices

# Globals and constants variables.
TRICLINIC = 'triclinic'
MONOCLINIC = 'monoclinic'
ORTHORHOMBIC = 'orthorhombic'
TETRAGONAL = 'tetragonal'
HEXAGONAL = 'hexgonal'
TRIGONAL = 'trigonal'
CUBIC = 'cubic'

def create_cubic_unitcell(a):
  """
  Create a cubic unit cell.

    * a = b = c
    * alpha = beta = gamma = pi/2

  :arg a: unit cell parameter in angstroms
  :type a: :class:`float`

  :rtype: :class:`Lattice`

  """
  return UnitCell(a, a, a, pi / 2, pi / 2, pi / 2)

def create_trigonal_unitcell(a, alpha):
  """
  Create a trigonal unit cell.

    * a = b = c
    * alpha = beta = gamma

  :arg a: unit cell parameter in angstroms
  :type a: :class:`float`

  :arg alpha: unit cell angle in radians
  :type alpha: :class:`float`

  :rtype: :class:`UnitCell`

  """
  return UnitCell(a, a, a, alpha, alpha, alpha)

def create_hexagonal_unitcell(a, c):
  """
  Create a hexagonal unit cell.

    * a = b
    * alpha = beta = pi/2, gamma == 2pi/3

  :arg a, c: unit cell parameter in angstroms
  :type a, c: :class:`float`

  :rtype: :class:`UnitCell`

  """
  return UnitCell(a, a, c, pi / 2, pi / 2, 2 * pi / 3)

def create_tetragonal_unitcell(a, c):
  """
  Create a tetragonal unit cell.

    * a = b
    * alpha = beta = gamma = pi/2

  :arg a, c: unit cell parameter in angstroms
  :type a, c: :class:`float`

  :rtype: :class:`UnitCell`

  """
  return UnitCell(a, a, c, pi / 2, pi / 2, pi / 2)

def create_orthorhombic_unitcell(a, b, c):
  """
  Create a orthorhombic unit cell.

    * a != b != c
    * alpha = beta = gamma = pi/2

  :arg a, b, c: unit cell parameter in angstroms
  :type a, b, c: :class:`float`

  :rtype: :class:`UnitCell`

  """
  return UnitCell(a, b, c, pi / 2, pi / 2, pi / 2)

def create_monoclinic_unitcell(a, b, c, beta):
  """
  Create a monoclinic unit cell.

    * a != b != c
    * alpha = gamma = pi/2

  :arg a, b, c: unit cell parameter in angstroms
  :type a, b, c: :class:`float`

  :arg beta: unit cell angle in radians
  :type beta: :class:`float`

  :rtype: :class:`UnitCell`

  """
  return UnitCell(a, b, c, pi / 2, beta, pi / 2)

def create_triclinic_unitcell(a, b, c, alpha, beta, gamma):
  """
  Create a triclinic unit cell.

    * a != b != c
    * alpha != beta != gamma

  :arg a, b, c: unit cell parameter in angstroms
  :type a, b, c: :class:`float`

  :arg alpha, beta, gamma: unit cell angle in radians
  :type alpha, beta, gamma: :class:`float`

  :rtype: :class:`UnitCell`

  """
  return UnitCell(a, b, c, alpha, beta, gamma)

class UnitCell:
  def __init__(self, a, b, c, alpha, beta, gamma):
    """
    Store the dimensions and angles of a unit cell forming a unit cell.
    The reciprocal basis and volume are automatically calculated.

    :arg a, b, c: unit cell parameter in angstroms
    :type a, b, c: :class:`float`

    :arg alpha, beta, gamma: unit cell angle in radians
    :type alpha, beta, gamma: :class:`float`

    **Attributes**

      * unit cell parameter dimensions: :attr:`a`, :attr:`b`, :attr:`c`
      * unit cell angle: :attr:`alpha`, :attr:`beta`, :attr:`gamma`
      * reciprocal unit cell parameter dimensions: :attr:`a_`, :attr:`b_`
        , :attr:`c_`
      * reciprocal unit cell angle: :attr:`alpha_`, :attr:`beta_`
        , :attr:`gamma_`
      * volume: :attr:`volume`
      * reciprocal volume: :attr:`volume_`
      * metrical matrix: :attr:`metricalmatrix` (:class:`matrices.Matrix3D`)
      * carterian matrix: :attr:`cartesianmatrix` (:class:`matrices.Matrix3D`)
      * crystal system: :attr:`crystalsystem`

    **References**

      Mathematical Crystallography

    """
    self.a = float(a)
    self.b = float(b)
    self.c = float(c)
    self.alpha = float(alpha)
    self.beta = float(beta)
    self.gamma = float(gamma)

    self._calculate_reciprocal_angles()

    self._calculate_metrical_matrix()
    self._calculate_cartesian_matrix()

    self._calculate_volume()
    self._calculate_reciprocal_volume()

    self._calculate_reciprocal_bases()

    self._find_crystalsystem()

  def _calculate_reciprocal_bases(self):
    self.a_ = self.b * self.c * sin(self.alpha) / self.volume
    self.b_ = self.a * self.c * sin(self.beta) / self.volume
    self.c_ = self.a * self.b * sin(self.gamma) / self.volume

  def _calculate_reciprocal_angles(self):
    self.alpha_ = acos((cos(self.beta) * cos(self.gamma) - cos(self.alpha)) / (sin(self.beta) * sin(self.gamma)))
    self.beta_ = acos((cos(self.alpha) * cos(self.gamma) - cos(self.beta)) / (sin(self.alpha) * sin(self.gamma)))
    self.gamma_ = acos((cos(self.alpha) * cos(self.beta) - cos(self.gamma)) / (sin(self.alpha) * sin(self.beta)))

  def _calculate_volume(self):
    """
    Calculate the volume of the unit cell.

    **References**

      Theorem 2.13 from Mathematical Crystallography

    """
    self.volume = sqrt(matrices.det(self.metricalmatrix))

  def _calculate_reciprocal_volume(self):
    """
    Calculate the reciprocal volume of the unit cell.

    **References**

      Theorem 2.14 from Mathematical Crystallography

    """
    self.volume_ = 1.0 / self.volume

  def _calculate_metrical_matrix(self):
    """
    Calculate the metrical matrix (G) of the unit cell.

    **References**

      Equation 1.12 and 2.14 from Mathematical Crystallography

    """
    g11 = self.a * self.a
    g12 = self.a * self.b * cos(self.gamma)
    g13 = self.a * self.c * cos(self.beta)
    g21 = g12
    g22 = self.b * self.b
    g23 = self.b * self.c * cos(self.alpha)
    g31 = g13
    g32 = g23
    g33 = self.c * self.c

    self.metricalmatrix = matrices.Matrix3D([g11, g12, g13]
                                            , [g21, g22, g23]
                                            , [g31, g32, g33])

  def _calculate_cartesian_matrix(self):
    """
    Calculate the matrix to change basis from the natural basis of a crystal
    :math:`(\\vec{a}, \\vec{b}, \\vec{c})` to the cartesian basis
    :math:`(\\vec{i}, \\vec{j}, \\vec{k})`.

    The cartesian basis is defined as follows:

      * :math:`\\vec{k}` is in the direction of :math:`\\vec{c}`
      * :math:`\\vec{j}` is in the direction of :math:`\\vec{c} \times \\vec{a}`
      * :math:`\\vec{i}` is in perpendicular to the plane of :math:`\\vec{k}`
        and :math:`\\vec{j}`

    **References**

      Equation 2.31 from Mathematical Crystallography

    """
    g11 = self.a * sin(self.beta)
    g12 = -self.b * sin(self.alpha) * cos(self.gamma_)
    g13 = 0
    g21 = 0
    g22 = self.b * sin(self.alpha) * sin(self.gamma_)
    g23 = 0
    g31 = self.a * cos(self.beta)
    g32 = self.b * cos(self.alpha)
    g33 = self.c

    self.cartesianmatrix = matrices.Matrix3D([g11, g12, g13]
                                             , [g21, g22, g23]
                                             , [g31, g32, g33])

  def _find_crystalsystem(self):
    """
    Find the crystal system of the unit cell.

    Possible answers:

      * :const:`TRICLINIC`
      * :const:`MONOCLINIC`
      * :const:`ORTHORHOMBIC`
      * :const:`TETRAGONAL`
      * :const:`HEXAGONAL`
      * :const:`TRIGONAL`
      * :const:`CUBIC`

    :rtype: :class:`str`

    """
    almostequal = lambda x, y: round(abs(x - y), 7) == 0

    if almostequal(self.a, self.b) and \
        almostequal(self.b, self.c) and \
        almostequal(self.alpha, pi / 2) and \
        almostequal(self.beta, pi / 2) and \
        almostequal(self.gamma, pi / 2):
      self.crystalsystem = CUBIC

    elif almostequal(self.a, self.b) and \
        almostequal(self.b, self.c) and \
        almostequal(self.alpha, self.beta) and \
        almostequal(self.beta, self.gamma):
      self.crystalsystem = TRIGONAL

    elif almostequal(self.a, self.b) and \
        almostequal(self.alpha, pi / 2) and \
        almostequal(self.beta, pi / 2) and \
        almostequal(self.gamma, 2 * pi / 3):
      self.crystalsystem = HEXAGONAL

    elif almostequal(self.a, self.b) and \
        almostequal(self.alpha, pi / 2) and \
        almostequal(self.beta, pi / 2) and \
        almostequal(self.gamma, pi / 2):
      self.crystalsystem = TETRAGONAL

    elif almostequal(self.alpha, pi / 2) and \
        almostequal(self.beta, pi / 2) and \
        almostequal(self.gamma, pi / 2):
      self.crystalsystem = ORTHORHOMBIC

    elif almostequal(self.alpha, pi / 2) and \
        almostequal(self.gamma, pi / 2):
      self.crystalsystem = MONOCLINIC

    else:
      self.crystalsystem = TRICLINIC

if __name__ == '__main__': #pragma: no cover
  import DrixUtilities.Runner as Runner
  Runner.Runner().run(runFunction=None)
