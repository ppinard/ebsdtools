#!/usr/bin/env python
"""
================================================================================
:mod:`spacegroup` -- Symmetry from space group
================================================================================

.. module:: spacegroup
   :synopsis: Symmetry from space group
.. moduleauthor:: Dr. Ethan Merritt <merritt@u.washington.edu>
.. moduleauthor:: Philippe Pinard <philippe.pinard@mail.mcgill.ca>

.. note:: From PymmLib 1.0

.. inheritance-diagram:: spacegroup

"""

# Script information for the file.
__author__ = "Dr. Ethan Merritt <merritt@u.washington.edu>"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2002 PyMMLib Development Group"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = ""
__svnDate__ = ""
__svnId__ = ""

# Standard library modules.

# Third party modules.

# Local modules.
import mathtools.algebra.vectors as vectors
import mathtools.rotation.matrices as matrices

import ebsdtools.crystallography.atomsites as atomsites
import ebsdtools.crystallography.atomsite as atomsite

# Globals and constants variables.

class SymOp(object):
  def __init__(self, r, t):
    """
    A subclass of the tuple class for performing one symmetry operation.

    :arg r: rotation matrix
    :type r: :class:`matrices.Matrix3D`

    :arg t: translation vector
    :type t: :class:`vectors.Vector3D`

    """
    self.r = r
    self.t = t

  def __str__(self):
    x = "[%6.3f %6.3f %6.3f %6.3f]\n" % (
        self.r[0][0], self.r[0][1], self.r[0][2], self.t[0])
    x += "[%6.3f %6.3f %6.3f %6.3f]\n" % (
        self.r[1][0], self.r[1][1], self.r[1][2], self.t[1])
    x += "[%6.3f %6.3f %6.3f %6.3f]\n" % (
        self.r[2][0], self.r[2][1], self.r[2][2], self.t[2])
    return x

  def __call__(self, atom):
    """
    Return the symmetry operation on an *atomsite*.

    :math:`= RV + T`

    :arg atom: atomsite to apply the symmetry operation
    :type atom: :class:`atomsite.AtomSite`

    """
    position = atom.position
    atomicnumber = atom.atomicnumber

    newposition = self.r * position + self.t

    return atomsite.AtomSite(atomicnumber, newposition)

  def __eq__(self, other):
    equality = True

    equality = equality and self.r == other.r
    equality = equality and self.t == other.t

    return equality

  def __ne__(self, other):
    return not self == other

  def almostequal(self, other):

    equality = True

    equality = equality and matrices.almostequal(self.r, other.r)
    equality = equality and vectors.almostequal(self.t, other.t)

    return equality

  def is_identity(self):
    """
    Returns *True* if this :class:`SymOp` is a identity symmetry operation
    (no rotation, no translation), otherwise returns *False*.

    :rtype: :class:`bool`

    """
    if matrices.almostequal(self.r, matrices.IdentityMatrix3D) and \
        vectors.almostequal(self.t, vectors.Vector3D()):
      return True

class SpaceGroup(object):
  def __init__(self
               , number=None
               , num_sym_equiv=None
               , num_primitive_sym_equiv=None
               , short_name=None
               , point_group_name=None
               , crystal_system=None
               , pdb_name=None
               , symop_list=None):
    """
    Contains the various names and symmetry operations for one space group.

    **Attributes**

      * :attr:`number`: number of the space group
      * :attr:`num_sym_equiv`: number of symmetry operations
      * :attr:`num_primitive_sym_equiv`: number of primitive symmetry operations
      * :attr:`short_name`: short name (e.g. Pmmm)
      * :attr:`point_group_name`: point group name
      * :attr:`crystal_system`: crystal system (e.g. :const:`MONOCLINIC`)
      * :attr:`pdb_name`: name in the PDB database
      * :attr:`symop_list`: :class:`list` of :class:`SymOp`
                            , symmetry operations

    """
    self.number = number
    self.num_sym_equiv = num_sym_equiv
    self.num_primitive_sym_equiv = num_primitive_sym_equiv
    self.short_name = short_name
    self.point_group_name = point_group_name
    self.crystal_system = crystal_system
    self.pdb_name = pdb_name
    self.symop_list = symop_list

  def iter_symops(self):
    """
    Iterates over all symmetry operations in the :class:`SpaceGroup`.

    """
    return iter(self.symop_list)

  def check_group_name(self, name):
    """
    Checks if the given name is a name for this space group,
    returns *True* or *False*.
    The space group name can be in several forms:
    the short name, the longer PDB-style name, or the space group number.

    :arg name: name can be

        * :attr:`short_name`
        * :attr:`pdb_name`
        * :attr:`number`

    """
    if name == self.short_name:       return True
    if name == self.pdb_name:         return True
    if name == self.number:           return True
    return False

  def iter_equivalent_atomsites(self, atom):
    """
    Iterate the symmetry equivalent atomsites of the given atom.

    :arg atom: atomsite to apply the symmetry operation
    :type atom: :class:`atomsite.AtomSite`

    :rtype: :class:`atomsite.Atomsite`

    """
    for symop in self.symop_list:
      yield symop(atom)

  def equivalent_atomsites(self, atom):
    """
    Return the symmetry equivalent atomsites of the given atom.
    Duplicate atomsite are removed.
    In other words, only unique atom site are returned.

    :arg atom: atomsite to apply the symmetry operation
    :type atom: :class:`atomsite.AtomSite`

    :rtype: :class:`atomsites.Atomsites`

    """
    atoms = atomsites.AtomSites()

    for symop in self.symop_list:
      newatom = symop(atom)
      try:
        atoms.append(newatom)
      except atomsites.AtomSitePositionError:
        pass

    return atoms

if __name__ == '__main__': #pragma: no cover
  import DrixUtilities.Runner as Runner
  Runner.Runner().run(runFunction=None)
