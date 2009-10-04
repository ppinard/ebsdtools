#!/usr/bin/env python
"""
================================================================================
:mod:`atomsites` -- Store the locations of the atoms.
================================================================================

.. module:: atomsites
   :synopsis: Store the locations of the atoms.
.. moduleauthor:: Philippe Pinard <philippe.pinard@mail.mcgill.ca>

.. inheritance-diagram:: atomsites

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

# Third party modules.

# Local modules.
import mathtools.algebra.vectors as vectors

# Globals and constants variables.

class AtomSites(list):
  def __init__(self, data=[]):
    """
    Store the *atomsite* in a :class:`list`.

    """
    self._assert_newitems(data)
    list.__init__(self, data)

  def _assert_newitems(self, items):
    """
    Assert that two *atomsite* don't have the same position.

    """
    if not isinstance(items, list):
      items = [items]

    for item in items:
      for atom in self:
        if vectors.almostequal(item.position
                               , atom.position):
          raise AtomSitePositionError, "Position already exists"

  def __setitem__(self, i, y):
    self._assert_newitems(y)
    list.__setitem__(self, i, y)

  def append(self, object):
    self._assert_newitems(object)
    list.append(self, object)

  def extend(self, iterable):
    self._assert_newitems(iterable)
    list.extend(self, iterable)

  def insert(self, index, object):
    self._assert_newitems(object)
    list.insert(self, index, object)

class AtomSitePositionError(ValueError):
  """
  Exception raised when the position of an new atomsite already exists in the
  atomsites list.

  """
  def __init__(self, value):
    self.value = value

  def __str__(self):
    return repr(self.value)

if __name__ == '__main__': #pragma: no cover
  import DrixUtilities.Runner as Runner
  Runner.Runner().run(runFunction=None)
