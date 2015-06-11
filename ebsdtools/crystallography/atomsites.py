#!/usr/bin/env python
"""
================================================================================
:mod:`atomsites` -- Store the locations of the atoms.
================================================================================

.. module:: atomsites
   :synopsis: Store the locations of the atoms.

.. inheritance-diagram:: ebsdtools.crystallography.atomsites

"""
# Script information for the file.
__author__ = "Philippe T. Pinard"
__email__ = "philippe.pinard@gmail.com"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2009 Philippe T. Pinard"
__license__ = "GPL v3"

# Subversion informations for the file.
__svnRevision__ = ""
__svnDate__ = ""
__svnId__ = ""

# Standard library modules.

# Third party modules.

# Local modules.
import mathtools.algebra.vectors as vectors
from ebsdtools.crystallography.atomsite import AtomSite

# Globals and constants variables.

def create_fcc_atomsites(atomicnumber):
    return AtomSites([AtomSite(atomicnumber, 0.5, 0.5, 0.0),
                      AtomSite(atomicnumber, 0.5, 0.0, 0.5),
                      AtomSite(atomicnumber, 0.0, 0.5, 0.5),
                      AtomSite(atomicnumber, 0.0, 0.0, 0.0)])

def create_bcc_atomsites(atomicnumber):
    return AtomSites([AtomSite(atomicnumber, 0.5, 0.5, 0.5),
                      AtomSite(atomicnumber, 0.0, 0.0, 0.0)])

def create_hcp_atomsites(atomicnumber):
    return AtomSites([AtomSite(atomicnumber, 1 / 3.0, 2 / 3.0, 0.5),
                      AtomSite(atomicnumber, 0.0, 0.0, 0.0)])

def create_single_atomsites(atomicnumber):
    return AtomSites([AtomSite(atomicnumber, 0.0, 0.0, 0.0)])

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
                if vectors.almostequal(item.position, atom.position):
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
