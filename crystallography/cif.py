#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Philippe Pinard (philippe.pinard@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2009 Philippe Pinard"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = ""
__svnDate__ = ""
__svnId__ = ""

# Standard library modules.
import warnings

# Third party modules.

# Local modules.

# Globals and constants variables.
CELL_VOLUME                     = '_cell_volume'
CELL_LENGTH_A                   = '_cell_length_a'
CELL_LENGTH_B                   = '_cell_length_b'
CELL_LENGTH_C                   = '_cell_length_c'
CELL_ANGLE_ALPHA                = '_cell_angle_alpha'
CELL_ANGLE_BETA                 = '_cell_angle_beta'
CELL_ANGLE_GAMMA                = '_cell_angle_gamma'
CHEMICAL_FORMULA_SUM            = '_chemical_formula_sum'
ATOM_SITE_FRACT_X               = '_atom_site_fract_x'
ATOM_SITE_FRACT_Y               = '_atom_site_fract_y'
ATOM_SITE_FRACT_Z               = '_atom_site_fract_z'
ATOM_SITE_LABEL                 = '_atom_site_label'
CHEMICAL_NAME                   = '_chemical_name'
CHEMICAL_NAME_MINERAL           = '_chemical_name_mineral'
JOURNAL_NAME_FULL               = '_journal_name_full'
JOURNAL_PAGE_FIRST              = '_journal_page_first'
JOURNAL_PAGE_LAST               = '_journal_page_last'
JOURNAL_VOLUME                  = '_journal_volume'
JOURNAL_YEAR                    = '_journal_year'
PUBL_AUTHOR_NAME                = '_publ_author_name'
PUBL_SECTION_TITLE              = '_publ_section_title'
SYMMETRY_EQUIV_POS_AS_XYZ       = '_symmetry_equiv_pos_as_xyz'
SYMMETRY_SPACE_GROUP_NAME_HM    = '_symmetry_space_group_name_H-M'

def _numb(number):
  if '(' in number:
    uncertainty = float(number[number.find('(')+1:number.find(')')])/10.0
    value = float(number[:number.find('(')])
    return (value, uncertainty)
  else:
    return (float(number), 0.0)

#Formatting dictionary
coreDictionary = {CELL_VOLUME: _numb
                  , CELL_LENGTH_A: _numb
                  , CELL_LENGTH_B: _numb
                  , CELL_LENGTH_C: _numb
                  , CELL_ANGLE_ALPHA: _numb
                  , CELL_ANGLE_BETA: _numb
                  , CELL_ANGLE_GAMMA: _numb
                  , CHEMICAL_FORMULA_SUM: lambda value: value.strip("'").strip('"')
                  , ATOM_SITE_FRACT_X: _numb
                  , ATOM_SITE_FRACT_Y: _numb
                  , ATOM_SITE_FRACT_Z: _numb
                  , ATOM_SITE_LABEL: lambda value: value.strip("'").strip('"')
                  , CHEMICAL_NAME: lambda value: value.strip("'").strip('"')
                  , CHEMICAL_NAME_MINERAL: lambda value: value.strip("'").strip('"')
                  , JOURNAL_NAME_FULL: lambda value: value.strip("'").strip('"')
                  , JOURNAL_PAGE_FIRST: int
                  , JOURNAL_PAGE_LAST: int
                  , JOURNAL_VOLUME: int
                  , JOURNAL_YEAR: int
                  , PUBL_AUTHOR_NAME: lambda value: value.strip("'").strip('"')
                  , PUBL_SECTION_TITLE: str
                  , SYMMETRY_EQUIV_POS_AS_XYZ: lambda value: tuple(value.strip("'").strip('"').split(',',2))
                  , SYMMETRY_SPACE_GROUP_NAME_HM: lambda value: value.strip("'").strip('"')
                  }

class cifreader:
  def __init__(self, filename):
    """
    Read cif file in accordance with the International Tables for Crystallography: Volume G Definition and Exchange of Crystallographic data
    
    :arg filename: path of the cif file
    :type filename: str
    
    **Examples:**::
      
      >>> cif = cif.cifreader('test.cif')
      >>> print cif.getValue(cif.CHEMICAL_NAME)
      >>> test
      >>> print cif.getValue(cif.CELL_LENGTH_A)
      >>> (2.500, 0.2) #(value, statistical uncertainty)
      >>> print cif.getValue(cif.SYMMETRY_EQUIV_POS_AS_XYZ)
      >>> [('x','y','z'), ('-x','1/2+y','z')]
    
    **Definitions:**
      
      * A *data name* or *tag* is an identifier (a string of characters beginning with an underscore character) of the content of an associated data value.
      * A *data value* is a string of characters representing a particular item of information. It may represent a single numerical value; a letter, word or phrase; extended discursive text.
      * A *data item* is a specific piece of information defined by a *data name* and its associated *data value*.
      
    """
    file = open(filename, 'r')
    
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
    
    self._parse()
  
  def _parse(self):
    self._dataitems = {}
    inloopHeader = False
    inloopData = False
    loopdatanames = []
    loopdata = ''
    inquoteblock = False
    quotestring = ''
    dataname = None
    
    for line in self.lines:
      if inloopData and (line[0] == '_' or line == 'loop_'):
        inloopData = False #Leave loop
        self.__loopdump(dataname, loopdata, loopdatanames)
        loopdata = '' #Clear loopdata
        dataname = None
      
      if line[0] == '_':
        dataitem = line.split(None, 1)
        assert len(dataitem) > 0 and len(dataitem) <= 2 #No empty line and should not be more than two items
        if len(dataitem) == 2:
          dataname, datavalue = dataitem
          self._dataitems.setdefault(dataname, self._formatDatavalue(dataname, datavalue)) #Save values
          dataname = None
        else:
          dataname = dataitem[0]
          if inloopHeader: #Store loop data names
            self._dataitems.setdefault(dataname, [])
            loopdatanames.append(dataname)
      elif line[0] == ';':
        inquoteblock = not inquoteblock #Enter or leave quotation
        
        if inquoteblock == False: #After leaving
          self._dataitems.setdefault(dataname, self._formatDatavalue(dataname, quotestring))
          quotestring = ''
          dataname = None
      elif line == 'loop_':
        inloopHeader = True
        inloopData = False
        loopdatanames = []
        loopdata = ''
      else:
        if inloopHeader:
          inloopHeader = False
          inloopData = True
        if inloopData: #Store loop information
          loopdata += ' ' + line
        elif inquoteblock: #Store quotation string
          quotestring += line + '\n'
        elif dataname != None:
          self._dataitems.setdefault(dataname, self._formatDatavalue(dataname, line)) #Save values
          dataname = None
    
    #Last entry
    if inloopData:
      self.__loopdump(dataname, loopdata, loopdatanames)
    
  def _formatDatavalue(self, dataname, datavalue):
    if dataname in coreDictionary:
      return coreDictionary[dataname](datavalue)
    else:
      warnings.warn('No format for %s' % dataname, RuntimeWarning)
      return datavalue
  
  def __splitData(self, loopdata):
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
  
  def __loopdump(self, dataname, loopdata, loopdatanames):
    data = self.__splitData(loopdata)
    for i in range(len(data)/len(loopdatanames)):
      for j, dataname in enumerate(loopdatanames):
        dataId = i*len(loopdatanames) + j
        self._dataitems[dataname].append(self._formatDatavalue(dataname, data[dataId]))
  
  def getValue(self, dataname):
    """
    Return the value for a given data name (tag). The common data names are stored as global variables.
    
    :arg dataname: Name of the parameter (starting with an underscore)
    :type dataname: str
    
    :rtype: various, depending on the data name
    """
    return self._dataitems[dataname]
  
  def getDatanames(self):
    """
    Return a list of all the data names defined in the cif
    
    :rtype: list
    """
    return self._dataitems.keys()
  
if __name__ == '__main__':
  import pprint
  warnings.simplefilter('ignore', RuntimeWarning)
  pp = pprint.PrettyPrinter(indent=4)
  cif = cifreader('testData/iron.cif')
  
  pp.pprint(cif._dataitems)
#  print cif.getValue(CELL_VOLUME)
