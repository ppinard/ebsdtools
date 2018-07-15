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
import operator
from collections import MutableSet

# Third party modules.

# Local modules.
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

class AtomSites(MutableSet):

    def __init__(self, precision=1e-4, sites=None):
        """
        Store the *atomsite* in a :class:`list`.
        
        """
        self._sites = set()
        self._precision = precision

        if sites is not None:
            self.extend(sites)

    def _create_precise_atomsite(self, site):
        x, y, z, = map(int, map(operator.truediv,
                                site.position,
                                [self._precision] * 3))
        return (site.atomicnumber, (x, y, z))

    def _create_orginal_atomsite(self, atomicnumber, position):
        x, y, z, = map(operator.mul, position, [self._precision] * 3)
        return AtomSite(atomicnumber, (x, y, z))

    def __repr__(self):
        return '<%s(%i sites)>' % (self.__class__.__name__, len(self))

    def __contains__(self, site):
        return self._create_precise_atomsite(site) in self._sites

    def __iter__(self):
        for atomicnumber, position in self._sites:
            yield self._create_orginal_atomsite(atomicnumber, position)

    def __len__(self):
        return len(self._sites)

    def add(self, site):
        self._sites.add(self._create_precise_atomsite(site))

    def discard(self, site):
        self._sites.discard(self._create_precise_atomsite(site))

