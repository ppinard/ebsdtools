#!/usr/bin/env python
"""
================================================================================
:mod:`cif` -- Parse cif file (crystallography information file).
================================================================================

.. module:: cif
   :synopsis: Parse cif file (crystallography information file).

.. inheritance-diagram:: ebsdtools.crystallography.cif

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
from math import pi
import warnings

# Third party modules.

# Local modules.
import ebsdtools.crystallography.unitcell as unitcell
import ebsdtools.crystallography.atomsite as atomsite
import ebsdtools.crystallography.atomsites as atomsites

import DatabasesTools.ElementProperties as ElementProperties

# Globals and constants variables.
CELL_VOLUME = '_cell_volume'
CELL_LENGTH_A = '_cell_length_a'
CELL_LENGTH_B = '_cell_length_b'
CELL_LENGTH_C = '_cell_length_c'
CELL_ANGLE_ALPHA = '_cell_angle_alpha'
CELL_ANGLE_BETA = '_cell_angle_beta'
CELL_ANGLE_GAMMA = '_cell_angle_gamma'
CHEMICAL_FORMULA_SUM = '_chemical_formula_sum'
ATOM_SITE_FRACT_X = '_atom_site_fract_x'
ATOM_SITE_FRACT_Y = '_atom_site_fract_y'
ATOM_SITE_FRACT_Z = '_atom_site_fract_z'
ATOM_SITE_LABEL = '_atom_site_label'
CHEMICAL_NAME = '_chemical_name'
CHEMICAL_NAME_MINERAL = '_chemical_name_mineral'
JOURNAL_NAME_FULL = '_journal_name_full'
JOURNAL_PAGE_FIRST = '_journal_page_first'
JOURNAL_PAGE_LAST = '_journal_page_last'
JOURNAL_VOLUME = '_journal_volume'
JOURNAL_YEAR = '_journal_year'
PUBL_AUTHOR_NAME = '_publ_author_name'
PUBL_SECTION_TITLE = '_publ_section_title'
SYMMETRY_EQUIV_POS_AS_XYZ = '_symmetry_equiv_pos_as_xyz'
SYMMETRY_SPACE_GROUP_NAME_HM = '_symmetry_space_group_name_H-M'

def _numb(number):
    """
    Convert a string number into a float.
    Take into account if the string contains a value and an error.
    
    :arg number: a number
    :type number: :class:`str`
    
    """
    if '(' in number:
        uncertainty = float(number[number.find('(') + 1:number.find(')')]) / 10.0
        value = float(number[:number.find('(')])
        return (value, uncertainty)
    else:
        return (float(number), 0.0)

# Formatting dictionary.
coredict = {CELL_VOLUME: _numb,
            CELL_LENGTH_A: _numb,
            CELL_LENGTH_B: _numb,
            CELL_LENGTH_C: _numb,
            CELL_ANGLE_ALPHA: _numb,
            CELL_ANGLE_BETA: _numb,
            CELL_ANGLE_GAMMA: _numb,
            CHEMICAL_FORMULA_SUM: lambda value: value.strip("'").strip('"'),
            ATOM_SITE_FRACT_X: _numb,
            ATOM_SITE_FRACT_Y: _numb,
            ATOM_SITE_FRACT_Z: _numb,
            ATOM_SITE_LABEL: lambda value: value.strip("'").strip('"'),
            CHEMICAL_NAME: lambda value: value.strip("'").strip('"'),
            CHEMICAL_NAME_MINERAL: lambda value: value.strip("'").strip('"'),
            JOURNAL_NAME_FULL: lambda value: value.strip("'").strip('"'),
            JOURNAL_PAGE_FIRST: int,
            JOURNAL_PAGE_LAST: int,
            JOURNAL_VOLUME: int,
            JOURNAL_YEAR: int,
            PUBL_AUTHOR_NAME: lambda value: value.strip("'").strip('"'),
            PUBL_SECTION_TITLE: str,
            SYMMETRY_EQUIV_POS_AS_XYZ: lambda value: tuple(value.strip("'").strip('"').split(',', 2)),
            SYMMETRY_SPACE_GROUP_NAME_HM: lambda value: value.strip("'").strip('"')
            }

class Reader(dict):
    def __init__(self, filepath):
        """
        Read cif file in accordance with the International Tables
        for Crystallography: Volume G Definition and Exchange of
        Crystallographic data
        
        :arg filepath: path of the cif file
        :type filepath: :class:`str`
        
        **Examples**::
        
          >>> ciffile = cif.Reader('test.cif')
          >>> print ciffile.get(cif.CHEMICAL_NAME)
          >>> test
          >>> print ciffile.get(cif.CELL_LENGTH_A)
          >>> (2.500, 0.2) # (value, statistical uncertainty)
          >>> print ciffile.get(cif.SYMMETRY_EQUIV_POS_AS_XYZ)
          >>> [('x','y','z'), ('-x','1/2+y','z')]
        
        **Definitions**
        
          * A *data name* or *tag* is an identifier
            (a string of characters beginning with an underscore character)
            of the content of an associated data value.
          * A *data value* is a string of characters representing a particular item
            of information. It may represent a single numerical value: a letter,
            word or phrase; extended discursive text.
          * A *data item* is a specific piece of information defined by a
            *data name* and its associated *data value*.
        
        **Tags**
        
          * :const:`CELL_VOLUME`
          * :const:`CELL_LENGTH_A`
          * :const:`CELL_LENGTH_B`
          * :const:`CELL_LENGTH_C`
          * :const:`CELL_ANGLE_ALPHA`
          * :const:`CELL_ANGLE_BETA`
          * :const:`CELL_ANGLE_GAMMA`
          * :const:`CHEMICAL_FORMULA_SUM`
          * :const:`ATOM_SITE_FRACT_X`
          * :const:`ATOM_SITE_FRACT_Y`
          * :const:`ATOM_SITE_FRACT_Z`
          * :const:`ATOM_SITE_LABEL`
          * :const:`CHEMICAL_NAME`
          * :const:`CHEMICAL_NAME_MINERAL`
          * :const:`JOURNAL_NAME_FULL`
          * :const:`JOURNAL_PAGE_FIRST`
          * :const:`JOURNAL_PAGE_LAST`
          * :const:`JOURNAL_VOLUME`
          * :const:`JOURNAL_YEAR`
          * :const:`PUBL_AUTHOR_NAME`
          * :const:`PUBL_SECTION_TITLE`
          * :const:`SYMMETRY_EQUIV_POS_AS_XYZ`
          * :const:`SYMMETRY_SPACE_GROUP_NAME_HM`
        
        """
        file = open(filepath, 'r')

        self.lines = []
        for line in file.readlines():
            if line[-1] == '\n' or line[-1] == '\r':
                line = line[:-1]
            elif line[-2:] == '\r\n':
                line = line[:-2]

            line = line.strip()

            if len(line) > 0:
                if line[0] != '#': #Ignore comments
                    self.lines.append(line)

        dataitems = self._parse()
        dict.__init__(self, dataitems)

    def _parse(self):
        dataitems = {}
        inloop_header = False
        inloop_data = False
        loopdatanames = []
        loopdata = ''
        inquoteblock = False
        quotestring = ''
        dataname = None

        for line in self.lines:
            if inloop_data and (line[0] == '_' or line == 'loop_'):
                inloop_data = False # Leave loop
                self.__loopdump(dataitems, dataname, loopdata, loopdatanames)
                loopdata = '' # Clear loopdata
                dataname = None

            if line[0] == '_':
                dataitem = line.split(None, 1)

                assert len(dataitem) > 0 and len(dataitem) <= 2, \
                        "No empty line and should not be more than two items"

                if len(dataitem) == 2:
                    dataname, datavalue = dataitem

                    # Save values
                    dataitems.setdefault(dataname, self._format_datavalue(dataname, datavalue))

                    dataname = None
                else:
                    dataname = dataitem[0]

                    if inloop_header: # Store loop data names
                        dataitems.setdefault(dataname, [])
                        loopdatanames.append(dataname)

            elif line[0] == ';':
                inquoteblock = not inquoteblock # Enter or leave quotation

                if inquoteblock == False: # After leaving
                    dataitems.setdefault(dataname, self._format_datavalue(dataname, quotestring))
                    quotestring = ''
                    dataname = None

            elif line == 'loop_':
                inloop_header = True
                inloop_data = False
                loopdatanames = []
                loopdata = ''

            else:
                if inloop_header:
                    inloop_header = False
                    inloop_data = True
                if inloop_data: # Store loop information
                    loopdata += ' ' + line
                elif inquoteblock: # Store quotation string
                    quotestring += line + '\n'
                elif dataname != None:
                    # Save values
                    dataitems.setdefault(dataname, self._format_datavalue(dataname, line))
                    dataname = None

        # Last entry
        if inloop_data:
            self.__loopdump(dataitems, dataname, loopdata, loopdatanames)

        return dataitems

    def _format_datavalue(self, dataname, datavalue):
        if dataname in coredict:
            return coredict[dataname](datavalue)
        else:
            warnings.warn('No format for %s' % dataname, RuntimeWarning)
            return datavalue

    def __split_data(self, loopdata):
        charnum = 0
        inquotation1 = False
        inquotation2 = False
        data = []
        dataitem = ''

        while charnum < len(loopdata):
            char = loopdata[charnum]

            if char == "'":
                inquotation1 = not inquotation1
            if char == '"':
                inquotation2 = not inquotation2

            if char == ' ' and inquotation1 == False and inquotation2 == False:
                if len(dataitem) > 0:
                    data.append(dataitem)
                dataitem = ''
            else:
                dataitem += char

            charnum += 1

        #Last entry
        if len(dataitem) > 0:
            data.append(dataitem)

        return data

    def __loopdump(self, dataitems, dataname, loopdata, loopdatanames):
        data = self.__split_data(loopdata)

        for i in range(len(data) / len(loopdatanames)):
            for j, dataname in enumerate(loopdatanames):
                dataId = i * len(loopdatanames) + j
                dataitems[dataname].append(self._format_datavalue(dataname, data[dataId]))

    def get(self, dataname):
        """
        Return the value for a given data name (tag).
        The common data names are stored as global variables.
        
        :arg dataname: name of the parameter (starting with an underscore)
        :type dataname: :class:`str`
        
        :rtype: various, depending on the data name
        
        """
        return dict.get(self, dataname)

    def keys(self):
        """
        Return a :class:`list` of all the data names defined in the cif.
        
        :rtype: :class:`list`
        
        """
        return dict.keys(self)

    def get_unitcell(self):
        """
        Return a :class:`unitcell.UnitCell` class from the cif.
        
        :rtype: :class:`unitcell.UnitCell`
        
        """
        a = self.get(CELL_LENGTH_A)[0]
        b = self.get(CELL_LENGTH_B)[0]
        c = self.get(CELL_LENGTH_C)[0]
        alpha = self.get(CELL_ANGLE_ALPHA)[0] * pi / 180.0
        beta = self.get(CELL_ANGLE_BETA)[0] * pi / 180.0
        gamma = self.get(CELL_ANGLE_GAMMA)[0] * pi / 180.0

        return unitcell.UnitCell(a, b, c, alpha, beta, gamma)

    def get_atomsites(self):
        """
        Return a :class:`list` of :class:`atomsite.AtomSite` from the cif.
        
        :rtype: : keyword:`list`
        
        """
        atoms = atomsites.AtomSites()

        symmetry_equiv_pos_as_xyz = self.get(SYMMETRY_EQUIV_POS_AS_XYZ)
        atom_site_labels = self.get(ATOM_SITE_LABEL)
        atom_site_fract_xs = self.get(ATOM_SITE_FRACT_X)
        atom_site_fract_ys = self.get(ATOM_SITE_FRACT_Y)
        atom_site_fract_zs = self.get(ATOM_SITE_FRACT_Z)

        for i, atom_site_label in enumerate(atom_site_labels):
            # Remove digits after the chemical symbol
            if len(atom_site_label) > 1 and atom_site_label[1].isdigit():
                symbol = atom_site_label[0]
            else:
                symbol = atom_site_label[:2]

            atomicnumber = ElementProperties.getAtomicNumberBySymbol(symbol)

            atom = atomsite.AtomSite(atomicnumber,
                                     atom_site_fract_xs[i][0],
                                     atom_site_fract_ys[i][0],
                                     atom_site_fract_zs[i][0])
            atoms.append(atom)

        # Apply symmetry equivalent positions
        for atom in atoms:
            x, y, z = tuple(atom.position)
            atomicnumber = atom.atomicnumber

            for equiv_pos in symmetry_equiv_pos_as_xyz:
                equiv_x, equiv_y, equiv_z = equiv_pos

                # Allow float division
                equiv_x = equiv_x.replace('1/', '1.0/').replace('2/', '2.0/').replace('3/', '3.0/').replace('4/', '4.0/').replace('6/', '6.0/')
                equiv_y = equiv_y.replace('1/', '1.0/').replace('2/', '2.0/').replace('3/', '3.0/').replace('4/', '4.0/').replace('6/', '6.0/')
                equiv_z = equiv_z.replace('1/', '1.0/').replace('2/', '2.0/').replace('3/', '3.0/').replace('4/', '4.0/').replace('6/', '6.0/')

                # Replace x, y, z by the value
                newx = eval(equiv_x.replace('x', str(x)).replace('y', str(y)).replace('z', str(z)))
                newy = eval(equiv_y.replace('x', str(x)).replace('y', str(y)).replace('z', str(z)))
                newz = eval(equiv_z.replace('x', str(x)).replace('y', str(y)).replace('z', str(z)))

                # Add if new position
                newatom = atomsite.AtomSite(atomicnumber, newx, newy, newz)
                try:
                    atoms.append(newatom)
                except atomsites.AtomSitePositionError:
                    pass

        return atoms

if __name__ == '__main__': #pragma: no cover
    import DrixUtilities.Runner as Runner
    Runner.Runner().run(runFunction=None)
