#!/usr/bin/env python
"""
================================================================================
:mod:`test_cif` -- Unit tests for the module :mod:`cif.`
================================================================================

.. module:: test_cif
   :synopsis: Unit tests for the module :mod:`cif.`

"""

# Script information for the file.
__author__ = "Philippe T. Pinard"
__email__ = "philippe.pinard@gmail.com"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2009 Philippe T. Pinard"
__license__ = "GPL v3"

# Standard library modules.
import unittest
import logging
import os.path
from math import pi
import warnings
warnings.filterwarnings(action='ignore', category=RuntimeWarning)

# Third party modules.

# Local modules.
import DrixUtilities.Files as Files

import ebsdtools.crystallography.cif as cif

# Globals and constants variables.

class TestReader(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)

        relativePath = os.path.join('..', 'testdata', 'aluminum.cif')
        filepath = Files.getCurrentModulePath(__file__, relativePath)
        self.cifAl = cif.Reader(filepath)

        relativePath = os.path.join('..', 'testdata', 'iron.cif')
        filepath = Files.getCurrentModulePath(__file__, relativePath)
        self.cifFe = cif.Reader(filepath)

        relativePath = os.path.join('..', 'testdata', 'zirconium.cif')
        filepath = Files.getCurrentModulePath(__file__, relativePath)
        self.cifZr = cif.Reader(filepath)

        relativePath = os.path.join('..', 'testdata', 'rudimer.cif')
        filepath = Files.getCurrentModulePath(__file__, relativePath)
        self.cifRuDimer = cif.Reader(filepath)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        self.assert_(True)

    def testget(self):
        #Aluminum
        self.assertEqual(self.cifAl.get(cif.CHEMICAL_NAME), 'Aluminum')
        self.assertEqual(self.cifAl.get(cif.PUBL_AUTHOR_NAME), ['Wyckoff R W G'])
        self.assertEqual(self.cifAl.get(cif.JOURNAL_NAME_FULL), 'Crystal Structures')
        self.assertEqual(self.cifAl.get(cif.JOURNAL_PAGE_FIRST), 7)
        self.assertEqual(self.cifAl.get(cif.JOURNAL_PAGE_LAST), 83)
        self.assertEqual(self.cifAl.get(cif.JOURNAL_VOLUME), 1)
        self.assertEqual(self.cifAl.get(cif.JOURNAL_YEAR), 1963)
        self.assertEqual(self.cifAl.get(cif.PUBL_SECTION_TITLE), 'Second edition. Interscience Publishers, New York, New York\nCubic closest packed, ccp, structure\n')
        self.assertEqual(self.cifAl.get(cif.CHEMICAL_FORMULA_SUM), 'Al')
        self.assertEqual(self.cifAl.get(cif.CELL_LENGTH_A), (4.04958, 0.0))
        self.assertEqual(self.cifAl.get(cif.CELL_LENGTH_B), (4.04958, 0.0))
        self.assertEqual(self.cifAl.get(cif.CELL_LENGTH_C), (4.04958, 0.0))
        self.assertEqual(self.cifAl.get(cif.CELL_ANGLE_ALPHA), (90.0, 0.0))
        self.assertEqual(self.cifAl.get(cif.CELL_ANGLE_BETA), (90.0, 0.0))
        self.assertEqual(self.cifAl.get(cif.CELL_ANGLE_GAMMA), (90.0, 0.0))
        self.assertEqual(self.cifAl.get(cif.CELL_VOLUME), (66.409, 0.0))
        self.assertEqual(self.cifAl.get(cif.SYMMETRY_SPACE_GROUP_NAME_HM), 'F m 3 m')
        self.assertEqual(len(self.cifAl.get(cif.SYMMETRY_EQUIV_POS_AS_XYZ)), 192)
        self.assertEqual(self.cifAl.get(cif.SYMMETRY_EQUIV_POS_AS_XYZ)[0], ('x', 'y', 'z'))
        self.assertEqual(self.cifAl.get(cif.SYMMETRY_EQUIV_POS_AS_XYZ)[1], ('x', '1/2+y', '1/2+z'))
        self.assertEqual(self.cifAl.get(cif.SYMMETRY_EQUIV_POS_AS_XYZ)[191], ('1/2-y', '1/2-z', '-x'))
        self.assertEqual(self.cifAl.get(cif.ATOM_SITE_LABEL), ['Al'])
        self.assertEqual(self.cifAl.get(cif.ATOM_SITE_FRACT_X), [(0.0, 0.0)])
        self.assertEqual(self.cifAl.get(cif.ATOM_SITE_FRACT_Y), [(0.0, 0.0)])
        self.assertEqual(self.cifAl.get(cif.ATOM_SITE_FRACT_Z), [(0.0, 0.0)])

        #Iron
        self.assertEqual(self.cifFe.get(cif.CHEMICAL_NAME), 'Iron')
        self.assertEqual(self.cifFe.get(cif.PUBL_AUTHOR_NAME), ['Wilburn D R', 'Bassett W A'])
        self.assertEqual(self.cifFe.get(cif.JOURNAL_NAME_FULL), "American Mineralogist")
        self.assertEqual(self.cifFe.get(cif.JOURNAL_PAGE_FIRST), 591)
        self.assertEqual(self.cifFe.get(cif.JOURNAL_PAGE_LAST), 596)
        self.assertEqual(self.cifFe.get(cif.JOURNAL_VOLUME), 63)
        self.assertEqual(self.cifFe.get(cif.JOURNAL_YEAR), 1978)
        self.assertEqual(self.cifFe.get(cif.PUBL_SECTION_TITLE), 'Hydrostatic compression of iron and related compounds: An overview\nP = 1 Kbar\n')
        self.assertEqual(self.cifFe.get(cif.CHEMICAL_FORMULA_SUM), 'Fe')
        self.assertEqual(self.cifFe.get(cif.CELL_LENGTH_A), (2.866, 0.0))
        self.assertEqual(self.cifFe.get(cif.CELL_LENGTH_B), (2.866, 0.0))
        self.assertEqual(self.cifFe.get(cif.CELL_LENGTH_C), (2.866, 0.0))
        self.assertEqual(self.cifFe.get(cif.CELL_ANGLE_ALPHA), (90.0, 0.0))
        self.assertEqual(self.cifFe.get(cif.CELL_ANGLE_BETA), (90.0, 0.0))
        self.assertEqual(self.cifFe.get(cif.CELL_ANGLE_GAMMA), (90.0, 0.0))
        self.assertEqual(self.cifFe.get(cif.CELL_VOLUME), (23.541, 0.0))
        self.assertEqual(self.cifFe.get(cif.SYMMETRY_SPACE_GROUP_NAME_HM), 'I m 3 m')
        self.assertEqual(len(self.cifFe.get(cif.SYMMETRY_EQUIV_POS_AS_XYZ)), 96)
        self.assertEqual(self.cifFe.get(cif.SYMMETRY_EQUIV_POS_AS_XYZ)[0], ('x', 'y', 'z'))
        self.assertEqual(self.cifFe.get(cif.SYMMETRY_EQUIV_POS_AS_XYZ)[1], ('1/2+x', '1/2+y', '1/2+z'))
        self.assertEqual(self.cifFe.get(cif.SYMMETRY_EQUIV_POS_AS_XYZ)[95], ('1/2-y', '1/2-z', '1/2-x'))
        self.assertEqual(self.cifFe.get(cif.ATOM_SITE_LABEL), ['Fe'])
        self.assertEqual(self.cifFe.get(cif.ATOM_SITE_FRACT_X), [(0.0, 0.0)])
        self.assertEqual(self.cifFe.get(cif.ATOM_SITE_FRACT_Y), [(0.0, 0.0)])
        self.assertEqual(self.cifFe.get(cif.ATOM_SITE_FRACT_Z), [(0.0, 0.0)])

        #Zirconium
        self.assertEqual(self.cifZr.get(cif.CHEMICAL_NAME_MINERAL), 'Zirconium')
        self.assertEqual(self.cifZr.get(cif.PUBL_AUTHOR_NAME), ['Wyckoff R W G'])
        self.assertEqual(self.cifZr.get(cif.JOURNAL_NAME_FULL), 'Crystal Structures')
        self.assertEqual(self.cifZr.get(cif.JOURNAL_PAGE_FIRST), 7)
        self.assertEqual(self.cifZr.get(cif.JOURNAL_PAGE_LAST), 83)
        self.assertEqual(self.cifZr.get(cif.JOURNAL_VOLUME), 1)
        self.assertEqual(self.cifZr.get(cif.JOURNAL_YEAR), 1963)
        self.assertEqual(self.cifZr.get(cif.PUBL_SECTION_TITLE), 'Second edition. Interscience Publishers, New York, New York\nHexagonal closest packed, hcp, structure\n')
        self.assertEqual(self.cifZr.get(cif.CHEMICAL_FORMULA_SUM), 'Zr')
        self.assertEqual(self.cifZr.get(cif.CELL_LENGTH_A), (3.232, 0.0))
        self.assertEqual(self.cifZr.get(cif.CELL_LENGTH_B), (3.232, 0.0))
        self.assertEqual(self.cifZr.get(cif.CELL_LENGTH_C), (5.147, 0.0))
        self.assertEqual(self.cifZr.get(cif.CELL_ANGLE_ALPHA), (90.0, 0.0))
        self.assertEqual(self.cifZr.get(cif.CELL_ANGLE_BETA), (90.0, 0.0))
        self.assertEqual(self.cifZr.get(cif.CELL_ANGLE_GAMMA), (120.0, 0.0))
        self.assertEqual(self.cifZr.get(cif.CELL_VOLUME), (46.562, 0.0))
        self.assertEqual(self.cifZr.get(cif.SYMMETRY_SPACE_GROUP_NAME_HM), 'P 63/m m c')
        self.assertEqual(len(self.cifZr.get(cif.SYMMETRY_EQUIV_POS_AS_XYZ)), 24)
        self.assertEqual(self.cifZr.get(cif.SYMMETRY_EQUIV_POS_AS_XYZ)[0], ('x', 'y', 'z'))
        self.assertEqual(self.cifZr.get(cif.SYMMETRY_EQUIV_POS_AS_XYZ)[1], ('-x', '-x+y', '1/2+z'))
        self.assertEqual(self.cifZr.get(cif.SYMMETRY_EQUIV_POS_AS_XYZ)[23], ('-x', '-y', '-z'))
        self.assertEqual(self.cifZr.get(cif.ATOM_SITE_LABEL)[0], 'Zr')
        self.assertAlmostEqual(self.cifZr.get(cif.ATOM_SITE_FRACT_X)[1][0], 0.33333)
        self.assertAlmostEqual(self.cifZr.get(cif.ATOM_SITE_FRACT_Y)[1][0], 0.66667)
        self.assertAlmostEqual(self.cifZr.get(cif.ATOM_SITE_FRACT_Z)[1][0], 0.2500)

        #Complex Structure
        self.assertEqual(self.cifRuDimer.get(cif.CHEMICAL_FORMULA_SUM), 'C42 H32 O8 Ru2 Sb2')
        self.assertEqual(self.cifRuDimer.get(cif.CELL_LENGTH_A), (11.181, 0.6))
        self.assertEqual(self.cifRuDimer.get(cif.CELL_LENGTH_B), (14.102, 0.5))
        self.assertEqual(self.cifRuDimer.get(cif.CELL_LENGTH_C), (14.180, 0.6))
        self.assertEqual(self.cifRuDimer.get(cif.CELL_ANGLE_ALPHA), (100.15, 0.4))
        self.assertEqual(self.cifRuDimer.get(cif.CELL_ANGLE_BETA), (109.66, 0.3))
        self.assertEqual(self.cifRuDimer.get(cif.CELL_ANGLE_GAMMA), (101.48, 0.3))
        self.assertEqual(self.cifRuDimer.get(cif.CELL_VOLUME), (1990.4, 1.6))
        self.assertEqual(self.cifRuDimer.get('_atom_type_symbol'), ["'C'", "'H'", "'O'", "'Ru'", "'Sb'"])
        self.assertEqual(self.cifRuDimer.get('_diffrn_standards_interval_count'), '?')

    def testget_lattice(self):
        #Aluminium
        Lal = self.cifAl.get_unitcell()
        self.assertAlmostEqual(Lal.a, 4.04958)
        self.assertAlmostEqual(Lal.b, 4.04958)
        self.assertAlmostEqual(Lal.c, 4.04958)
        self.assertAlmostEqual(Lal.a_, 0.24693918)
        self.assertAlmostEqual(Lal.b_, 0.24693918)
        self.assertAlmostEqual(Lal.c_, 0.24693918)
        self.assertAlmostEqual(Lal.alpha, pi / 2)
        self.assertAlmostEqual(Lal.beta, pi / 2)
        self.assertAlmostEqual(Lal.gamma, pi / 2)
        self.assertAlmostEqual(Lal.alpha_, pi / 2)
        self.assertAlmostEqual(Lal.beta_, pi / 2)
        self.assertAlmostEqual(Lal.gamma_, pi / 2)
        self.assertAlmostEqual(Lal.volume, 66.409459993185905)
        self.assertAlmostEqual(Lal.volume_, 0.015058095640329063)

        #Iron
        Lfe = self.cifFe.get_unitcell()
        self.assertAlmostEqual(Lfe.a, 2.866)
        self.assertAlmostEqual(Lfe.b, 2.866)
        self.assertAlmostEqual(Lfe.c, 2.866)
        self.assertAlmostEqual(Lfe.a_, 0.34891835310537334)
        self.assertAlmostEqual(Lfe.b_, 0.34891835310537334)
        self.assertAlmostEqual(Lfe.c_, 0.34891835310537334)
        self.assertAlmostEqual(Lfe.alpha, pi / 2)
        self.assertAlmostEqual(Lfe.beta, pi / 2)
        self.assertAlmostEqual(Lfe.gamma, pi / 2)
        self.assertAlmostEqual(Lfe.alpha_, pi / 2)
        self.assertAlmostEqual(Lfe.beta_, pi / 2)
        self.assertAlmostEqual(Lfe.gamma_, pi / 2)
        self.assertAlmostEqual(Lfe.volume, 23.541197896000003)
        self.assertAlmostEqual(Lfe.volume_, 0.04247872)

        #Zirconium
        Lzr = self.cifZr.get_unitcell()
        self.assertAlmostEqual(Lzr.a, 3.2320)
        self.assertAlmostEqual(Lzr.b, 3.2320)
        self.assertAlmostEqual(Lzr.c, 5.1470)
        self.assertAlmostEqual(Lzr.a_, 0.3572712)
        self.assertAlmostEqual(Lzr.b_, 0.3572712)
        self.assertAlmostEqual(Lzr.c_, 0.1942879)
        self.assertAlmostEqual(Lzr.alpha, pi / 2)
        self.assertAlmostEqual(Lzr.beta, pi / 2)
        self.assertAlmostEqual(Lzr.gamma, 2 * pi / 3)
        self.assertAlmostEqual(Lzr.alpha_, pi / 2)
        self.assertAlmostEqual(Lzr.beta_, pi / 2)
        self.assertAlmostEqual(Lzr.gamma_, pi / 3)
        self.assertAlmostEqual(Lzr.volume, 46.561558)
        self.assertAlmostEqual(Lzr.volume_, 0.02147694)

        #Ru Dimer
        Lrudimer = self.cifRuDimer.get_unitcell()
        self.assertAlmostEqual(Lrudimer.a, 11.181)
        self.assertAlmostEqual(Lrudimer.b, 14.102)
        self.assertAlmostEqual(Lrudimer.c, 14.18)
        self.assertAlmostEqual(Lrudimer.a_, 0.098891163699886597)
        self.assertAlmostEqual(Lrudimer.b_, 0.075010689601430147)
        self.assertAlmostEqual(Lrudimer.c_, 0.0776311)
        self.assertAlmostEqual(Lrudimer.alpha, 100.15 * pi / 180.0)
        self.assertAlmostEqual(Lrudimer.beta, 109.66 * pi / 180.0)
        self.assertAlmostEqual(Lrudimer.gamma, 101.48 * pi / 180.0)
        self.assertAlmostEqual(Lrudimer.alpha_, 1.3041359787536495)
        self.assertAlmostEqual(Lrudimer.beta_, 1.1754554954691976)
        self.assertAlmostEqual(Lrudimer.gamma_, 1.2883909)
        self.assertAlmostEqual(Lrudimer.volume, 1990.4391137313373)
        self.assertAlmostEqual(Lrudimer.volume_, 0.000502401)

    def testget_atomsites(self):
        atomsites = self.cifAl.get_atomsites()
        #    print atomsites
        self.assertEqual(len(atomsites), 4)

        atomsites = self.cifFe.get_atomsites()
        self.assertEqual(len(atomsites), 2)

        atomsites = self.cifZr.get_atomsites()
        self.assertEqual(len(atomsites), 8)
        #
        atomsites = self.cifRuDimer.get_atomsites()
        self.assertEqual(len(atomsites), 172)

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.INFO)
    unittest.main()
