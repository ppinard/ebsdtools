#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Philippe Pinard (philippe.pinard@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2009 Philippe Pinard"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = "$Revision$"
__svnDate__ = "$Date$"
__svnId__ = "$Id$"

# Standard library modules.
import unittest
import warnings

# Third party modules.

# Local modules.
import EBSDTools.crystallography.cif as cif
from RandomUtilities.testing.testOthers import almostEqual

# Globals and constants variables.

warnings.filterwarnings('ignore', category=RuntimeWarning)

class TestCif(unittest.TestCase):
  def setUp(self):
    unittest.TestCase.setUp(self)
    
    self.cifAl = cif.cifreader('testData/aluminum.cif')
    self.cifFe = cif.cifreader('testData/iron.cif')
    self.cifZr = cif.cifreader('testData/zirconium.cif')
    self.cifRuDimer = cif.cifreader('testData/rudimer.cif')

  def tearDown(self):
    unittest.TestCase.tearDown(self)

  def testSkeleton(self):
#    self.fail("Test if the testcase is working.")
    self.assert_(True)
  
  def testGetValue(self):
    #Aluminum
    self.assertEqual(self.cifAl.getValue(cif.CHEMICAL_NAME), 'Aluminum')
    self.assertEqual(self.cifAl.getValue(cif.PUBL_AUTHOR_NAME), ['Wyckoff R W G'])
    self.assertEqual(self.cifAl.getValue(cif.JOURNAL_NAME_FULL), 'Crystal Structures')
    self.assertEqual(self.cifAl.getValue(cif.JOURNAL_PAGE_FIRST), 7)
    self.assertEqual(self.cifAl.getValue(cif.JOURNAL_PAGE_LAST), 83)
    self.assertEqual(self.cifAl.getValue(cif.JOURNAL_VOLUME), 1)
    self.assertEqual(self.cifAl.getValue(cif.JOURNAL_YEAR), 1963)
    self.assertEqual(self.cifAl.getValue(cif.PUBL_SECTION_TITLE), 'Second edition. Interscience Publishers, New York, New York\nCubic closest packed, ccp, structure\n')
    self.assertEqual(self.cifAl.getValue(cif.CHEMICAL_FORMULA_SUM), 'Al')
    self.assertEqual(self.cifAl.getValue(cif.CELL_LENGTH_A), (4.04958, 0.0))
    self.assertEqual(self.cifAl.getValue(cif.CELL_LENGTH_B), (4.04958, 0.0))
    self.assertEqual(self.cifAl.getValue(cif.CELL_LENGTH_C), (4.04958, 0.0))
    self.assertEqual(self.cifAl.getValue(cif.CELL_ANGLE_ALPHA), (90.0, 0.0))
    self.assertEqual(self.cifAl.getValue(cif.CELL_ANGLE_BETA), (90.0, 0.0))
    self.assertEqual(self.cifAl.getValue(cif.CELL_ANGLE_GAMMA), (90.0, 0.0))
    self.assertEqual(self.cifAl.getValue(cif.CELL_VOLUME), (66.409, 0.0))
    self.assertEqual(self.cifAl.getValue(cif.SYMMETRY_SPACE_GROUP_NAME_HM), 'F m 3 m')
    self.assertEqual(len(self.cifAl.getValue(cif.SYMMETRY_EQUIV_POS_AS_XYZ)), 192)
    self.assertEqual(self.cifAl.getValue(cif.SYMMETRY_EQUIV_POS_AS_XYZ)[0], ('x','y','z'))
    self.assertEqual(self.cifAl.getValue(cif.SYMMETRY_EQUIV_POS_AS_XYZ)[1], ('x','1/2+y','1/2+z'))
    self.assertEqual(self.cifAl.getValue(cif.SYMMETRY_EQUIV_POS_AS_XYZ)[191], ('1/2-y','1/2-z','-x'))
    self.assertEqual(self.cifAl.getValue(cif.ATOM_SITE_LABEL), ['Al'])
    self.assertEqual(self.cifAl.getValue(cif.ATOM_SITE_FRACT_X), [(0.0,0.0)])
    self.assertEqual(self.cifAl.getValue(cif.ATOM_SITE_FRACT_Y), [(0.0,0.0)])
    self.assertEqual(self.cifAl.getValue(cif.ATOM_SITE_FRACT_Z), [(0.0,0.0)])
    
    #Iron
    self.assertEqual(self.cifFe.getValue(cif.CHEMICAL_NAME), 'Iron')
    self.assertEqual(self.cifFe.getValue(cif.PUBL_AUTHOR_NAME), ['Wilburn D R', 'Bassett W A'])
    self.assertEqual(self.cifFe.getValue(cif.JOURNAL_NAME_FULL), "American Mineralogist")
    self.assertEqual(self.cifFe.getValue(cif.JOURNAL_PAGE_FIRST), 591)
    self.assertEqual(self.cifFe.getValue(cif.JOURNAL_PAGE_LAST), 596)
    self.assertEqual(self.cifFe.getValue(cif.JOURNAL_VOLUME), 63)
    self.assertEqual(self.cifFe.getValue(cif.JOURNAL_YEAR), 1978)
    self.assertEqual(self.cifFe.getValue(cif.PUBL_SECTION_TITLE), 'Hydrostatic compression of iron and related compounds: An overview\nP = 1 Kbar\n')
    self.assertEqual(self.cifFe.getValue(cif.CHEMICAL_FORMULA_SUM), 'Fe')
    self.assertEqual(self.cifFe.getValue(cif.CELL_LENGTH_A), (2.866, 0.0))
    self.assertEqual(self.cifFe.getValue(cif.CELL_LENGTH_B), (2.866, 0.0))
    self.assertEqual(self.cifFe.getValue(cif.CELL_LENGTH_C), (2.866, 0.0))
    self.assertEqual(self.cifFe.getValue(cif.CELL_ANGLE_ALPHA), (90.0, 0.0))
    self.assertEqual(self.cifFe.getValue(cif.CELL_ANGLE_BETA), (90.0, 0.0))
    self.assertEqual(self.cifFe.getValue(cif.CELL_ANGLE_GAMMA), (90.0, 0.0))
    self.assertEqual(self.cifFe.getValue(cif.CELL_VOLUME), (23.541, 0.0))
    self.assertEqual(self.cifFe.getValue(cif.SYMMETRY_SPACE_GROUP_NAME_HM), 'I m 3 m')
    self.assertEqual(len(self.cifFe.getValue(cif.SYMMETRY_EQUIV_POS_AS_XYZ)), 96)
    self.assertEqual(self.cifFe.getValue(cif.SYMMETRY_EQUIV_POS_AS_XYZ)[0], ('x','y','z'))
    self.assertEqual(self.cifFe.getValue(cif.SYMMETRY_EQUIV_POS_AS_XYZ)[1], ('1/2+x','1/2+y','1/2+z'))
    self.assertEqual(self.cifFe.getValue(cif.SYMMETRY_EQUIV_POS_AS_XYZ)[95], ('1/2-y','1/2-z','1/2-x'))
    self.assertEqual(self.cifFe.getValue(cif.ATOM_SITE_LABEL), ['Fe'])
    self.assertEqual(self.cifFe.getValue(cif.ATOM_SITE_FRACT_X), [(0.0,0.0)])
    self.assertEqual(self.cifFe.getValue(cif.ATOM_SITE_FRACT_Y), [(0.0,0.0)])
    self.assertEqual(self.cifFe.getValue(cif.ATOM_SITE_FRACT_Z), [(0.0,0.0)])
    
    #Zirconium
    self.assertEqual(self.cifZr.getValue(cif.CHEMICAL_NAME_MINERAL), 'Zirconium')
    self.assertEqual(self.cifZr.getValue(cif.PUBL_AUTHOR_NAME), ['Wyckoff R W G'])
    self.assertEqual(self.cifZr.getValue(cif.JOURNAL_NAME_FULL), 'Crystal Structures')
    self.assertEqual(self.cifZr.getValue(cif.JOURNAL_PAGE_FIRST), 7)
    self.assertEqual(self.cifZr.getValue(cif.JOURNAL_PAGE_LAST), 83)
    self.assertEqual(self.cifZr.getValue(cif.JOURNAL_VOLUME), 1)
    self.assertEqual(self.cifZr.getValue(cif.JOURNAL_YEAR), 1963)
    self.assertEqual(self.cifZr.getValue(cif.PUBL_SECTION_TITLE), 'Second edition. Interscience Publishers, New York, New York\nHexagonal closest packed, hcp, structure\n')
    self.assertEqual(self.cifZr.getValue(cif.CHEMICAL_FORMULA_SUM), 'Zr')
    self.assertEqual(self.cifZr.getValue(cif.CELL_LENGTH_A), (3.232, 0.0))
    self.assertEqual(self.cifZr.getValue(cif.CELL_LENGTH_B), (3.232, 0.0))
    self.assertEqual(self.cifZr.getValue(cif.CELL_LENGTH_C), (5.147, 0.0))
    self.assertEqual(self.cifZr.getValue(cif.CELL_ANGLE_ALPHA), (90.0, 0.0))
    self.assertEqual(self.cifZr.getValue(cif.CELL_ANGLE_BETA), (90.0, 0.0))
    self.assertEqual(self.cifZr.getValue(cif.CELL_ANGLE_GAMMA), (120.0, 0.0))
    self.assertEqual(self.cifZr.getValue(cif.CELL_VOLUME), (46.562, 0.0))
    self.assertEqual(self.cifZr.getValue(cif.SYMMETRY_SPACE_GROUP_NAME_HM), 'P 63/m m c')
    self.assertEqual(len(self.cifZr.getValue(cif.SYMMETRY_EQUIV_POS_AS_XYZ)), 24)
    self.assertEqual(self.cifZr.getValue(cif.SYMMETRY_EQUIV_POS_AS_XYZ)[0], ('x','y','z'))
    self.assertEqual(self.cifZr.getValue(cif.SYMMETRY_EQUIV_POS_AS_XYZ)[1], ('-x','-x+y','1/2+z'))
    self.assertEqual(self.cifZr.getValue(cif.SYMMETRY_EQUIV_POS_AS_XYZ)[23], ('-x','-y','-z'))
    self.assertEqual(self.cifZr.getValue(cif.ATOM_SITE_LABEL)[0], 'Zr')
    self.assert_(almostEqual(self.cifZr.getValue(cif.ATOM_SITE_FRACT_X)[1][0], 0.333333))
    self.assert_(almostEqual(self.cifZr.getValue(cif.ATOM_SITE_FRACT_Y)[1][0], 0.666666))
    self.assert_(almostEqual(self.cifZr.getValue(cif.ATOM_SITE_FRACT_Z)[1][0], 0.2500))
    
    #Complex Structure
    self.assertEqual(self.cifRuDimer.getValue(cif.CHEMICAL_FORMULA_SUM), 'C42 H32 O8 Ru2 Sb2')
    self.assertEqual(self.cifRuDimer.getValue(cif.CELL_LENGTH_A), (11.181, 0.6))
    self.assertEqual(self.cifRuDimer.getValue(cif.CELL_LENGTH_B), (14.102, 0.5))
    self.assertEqual(self.cifRuDimer.getValue(cif.CELL_LENGTH_C), (14.180, 0.6))
    self.assertEqual(self.cifRuDimer.getValue(cif.CELL_ANGLE_ALPHA), (100.15, 0.4))
    self.assertEqual(self.cifRuDimer.getValue(cif.CELL_ANGLE_BETA), (109.66, 0.3))
    self.assertEqual(self.cifRuDimer.getValue(cif.CELL_ANGLE_GAMMA), (101.48, 0.3))
    self.assertEqual(self.cifRuDimer.getValue(cif.CELL_VOLUME), (1990.4, 1.6))
    self.assertEqual(self.cifRuDimer.getValue('_atom_type_symbol'), ["'C'", "'H'", "'O'", "'Ru'", "'Sb'"])
    self.assertEqual(self.cifRuDimer.getValue('_diffrn_standards_interval_count'), '?')
    
if __name__ == '__main__':
  unittest.main()