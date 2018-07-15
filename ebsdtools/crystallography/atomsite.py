#!/usr/bin/env python
"""
================================================================================
:mod:`atomsite` -- Store the location and atomic number of an atom.
================================================================================

.. module:: atomsite
   :synopsis: Store the location and atomic number of an atom

.. inheritance-diagram:: ebsdtools.crystallography.atomsite

"""

# Script information for the file.
__author__ = "Philippe T. Pinard"
__email__ = "philippe.pinard@gmail.com"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2009 Philippe T. Pinard"
__license__ = "GPL v3"

# Standard library modules.

# Third party modules.

# Local modules.
import ebsdtools.util.element_properties as ep

# Globals and constants variables.

class AtomSite(object):

    def __init__(self, atomicnumber, *args):
        """
        Store the location and atomic number of an atom site.
        
        :arg atomicnumber: atomic number
        :type atomicnumber: :class:`int`
        
        :arg x, y, z: position of the atom as a fraction of the lattice basis
        :type x, y, z: :class:`tuple` or 3 :class:`float`
        
        **Attributes**
        
          * :attr:`atomicnumber`: atomic number of the atom (:class:`int`)
          * :attr:`position`: position of the atom (:class:`vectors.Vector3D`)
        
        """
        # Atomic number
        self._atomicnumber = int(atomicnumber)

        # Position
        if len(args) == 1:
            x = float(args[0][0])
            y = float(args[0][1])
            z = float(args[0][2])
        elif len(args) == 3:
            x = float(args[0])
            y = float(args[1])
            z = float(args[2])
        else:
            raise AttributeError("Wrong location of the atom site")

        # Convert fraction to always be between 0.0 and 1.0
        while x < 0: x += 1
        while y < 0: y += 1
        while z < 0: z += 1

        while x >= 1: x -= 1
        while y >= 1: y -= 1
        while z >= 1: z -= 1

        assert x >= 0.0 and x <= 1.0, \
                "Atom position can only be a fraction between 0.0 and 1.0"
        assert y >= 0.0 and y <= 1.0, \
                "Atom position can only be a fraction between 0.0 and 1.0"
        assert z >= 0.0 and z <= 1.0, \
                "Atom position can only be a fraction between 0.0 and 1.0"

        # Save position
        self._position = (x, y, z)

    def __repr__(self):
        symbol = ep.get_symbol(self.atomicnumber)
        return "<%s(%s->%s)>" % (self.__class__.__name__, symbol, self.position)

    @property
    def atomicnumber(self):
        return self._atomicnumber

    z = atomicnumber

    @property
    def position(self):
        return self._position


