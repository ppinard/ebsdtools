#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Philippe T. Pinard"
__email__ = "philippe.pinard@gmail.com"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2010 Philippe T. Pinard"
__license__ = "GPL v3"

# Standard library modules.
import unittest
import logging
import os

# Third party modules.

# Local modules.
import DrixUtilities.Files as Files

import ebsdtools.hkl.tango.txtFile as txtFile

# Globals and constants variables.

class TestCtfFile(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        testDataFolder = Files.getCurrentModulePath(__file__, 'testdata')
        self.testTxtFilepath = os.path.join(testDataFolder, 'test_txtFile.txt')

        self.txt = txtFile.txt(self.testTxtFilepath)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        #self.fail("Test if the testcase is working.")
        self.assert_(True)

    def testInit(self):
        self.assertEqual(self.txt.header, ['phase', 'x', 'y', 'euler1', 'euler2', 'euler3', 'mad', 'bc', 'bs', 'bands', 'error', 'reliabilityindex', 'edxcount1', 'edxcount2'])

    def testSetHeader(self):
        self.txt.setHeader(['a', 'b', 'c'])
        self.assertEqual(self.txt.header, ['a', 'b', 'c'])

    def testGetEDXanalyses(self):
        self.assertEqual(self.txt.getEDXanalyses(), 2)

    def testGetStepSize(self):
        self.assertEqual(self.txt.getStepSize(), 0.03)

    def testGetSize(self):
        self.assertEqual(self.txt.getSize(), (31, 1))

    def testGetColumnPos(self):
        self.assertEqual(self.txt.getColumnPos('x'), 1)
        self.assertEqual(self.txt.getColumnPos('bc'), 7)
        self.assertEqual(self.txt.getColumnPos('euler2'), 4)

    def testGetPixelResults(self):
        coord = (0, 0)
        self.assertEquals(self.txt.getPixelResults(coord), {'edxcount2': 2911.4000000000001, 'euler3': 0.0, 'euler2': 0.0, 'euler1': 0.0, 'bc': 37, 'bands': 0, 'error': 'No solution', 'reliabilityindex': 1.0, 'errorcode': 3, 'y': 0.0, 'edxcount1': 698.52999999999997, 'mad': 0.0, 'bs': 164, 'phase': 0, 'x': 0.0})

        coord = self.txt.getSize()
        coord = (coord[0], coord[1])
        self.assertEquals(self.txt.getPixelResults(coord), {})

    def testResultsLinetoDict(self):
        pass

    def testGetPixelArray(self):
        self.assertEquals(self.txt.getPixelArray(key='euler3')[0], 0.0)


if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
