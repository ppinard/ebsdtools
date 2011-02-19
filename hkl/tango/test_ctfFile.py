#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Philippe T. Pinard"
__email__ = "philippe.pinard@gmail.com"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2010 Philippe T. Pinard"
__license__ = "GPL v3"

# Standard library modules.
import os
import unittest
import logging

# Third party modules.

# Local modules.
import DrixUtilities.Files as Files

import ebsdtools.hkl.tango.ctfFile as ctfFile

class TestCtfFile(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        relativePath = os.path.join('testdata', 'test_ctfFile.ctf')
        filepath = Files.getCurrentModulePath(__file__, relativePath)

        self.ctf = ctfFile.ctf(filepath)

    def tearDown(self):
        del self.ctf #Require in jython not to overload the memory
        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        #self.fail("Test if the testcase is working.")
        self.assert_(True)

    def test__init__(self):
        self.assertEquals(len(self.ctf._data), 8652)

    def test_parseHeader(self):
        self.assertEquals(self.ctf._firstPhaseLine, 13)
        self.assertEquals(self.ctf._firstDataLine, 19)

    def testGetProjectName(self):
        self.assertEqual(self.ctf.getProjectName(), 'T009_04')

    def testGetProjectFolderName(self):
        self.assertEqual(self.ctf.getProjectFolderName(), 'T009')

    def testGetProjectFolderPath(self):
        self.assertEqual(os.path.normpath(self.ctf.getProjectFolderPath()), os.path.normpath('D:/data/T/T009'))

    def testGetProjectImagesFolderName(self):
        self.assertEqual(self.ctf.getProjectImagesFolderName(), 'T009Images')

    def testGetProjectImagesFolderPath(self):
        self.assertEqual(os.path.normpath(self.ctf.getProjectImagesFolderPath()), os.path.normpath('D:/data/T/T009/T009_04Images'))

    def testGetAuthor(self):
        self.assertEquals(self.ctf.getAuthor(), '[Unknown]')

    def testGetJobMode(self):
        self.assertEquals(self.ctf.getJobMode(), 'Grid')

    def testGetXCells(self):
        self.assertEquals(self.ctf.getXCells(), 103)

    def testGetYCells(self):
        self.assertEquals(self.ctf.getYCells(), 84)

    def testGetSize(self):
        self.assertEquals(self.ctf.getSize(), 8652)

    def testGetWidth(self):
        self.assertEquals(self.ctf.getWidth(), 103)

    def testGetHeight(self):
        self.assertEquals(self.ctf.getHeight(), 84)

    def testGetXStep(self):
        self.assertEquals(self.ctf.getXStep(), 0.2)

    def testGetYStep(self):
        self.assertEquals(self.ctf.getYStep(), 0.2)

    def testGetAcquisitionEuler1(self):
        self.assertEquals(self.ctf.getAcquisitionEuler1(), 0)

    def testGetAcquisitionEuler2(self):
        self.assertEquals(self.ctf.getAcquisitionEuler2(), 0)

    def testGetAcquisitionEuler3(self):
        self.assertEquals(self.ctf.getAcquisitionEuler3(), 0)

    def testGetAcquisitionEulers(self):
        self.assertEquals(self.ctf.getAcquisitionEulers(), (0, 0, 0))

    def testGetMagnification(self):
        self.assertEquals(self.ctf.getMagnification(), 6000)

    def testGetCoverage(self):
        self.assertEquals(self.ctf.getCoverage(), 100)

    def testGetDevice(self):
        self.assertEquals(self.ctf.getDevice(), 0)

    def testGetAcceleratingVoltage(self):
        self.assertEquals(self.ctf.getAcceleratingVoltage(), 15)

    def testGetTiltAngle(self):
        self.assertEquals(self.ctf.getTiltAngle(), 70)

    def testGetTiltAxis(self):
        self.assertEquals(self.ctf.getTiltAxis(), 0)

    def testGetNumberPhases(self):
        self.assertEquals(self.ctf.getNumberPhases(), 5)

    def testGetPhases(self):
        self.assert_(isinstance(self.ctf.getPhases(), dict))
        self.assertEqual(len(self.ctf.getPhases()), 5)
        self.assertEqual(len(self.ctf.getPhases(1)), 10)

    def testGetPhaseName(self):
        self.assertEqual(self.ctf.getPhaseName(1), 'iron Gamma Cr_Fe_Ni_')
        self.assertEqual(self.ctf.getPhaseName(2), 'Iron Alpha PH')
        self.assertEqual(self.ctf.getPhaseName(3), 'Austenite')
        self.assertEqual(self.ctf.getPhaseName(4), 'Fe Martensite')
        self.assertEqual(self.ctf.getPhaseName(5), 'Copper')

    def testGetPhaseLatticeParameterA(self):
        self.assertEqual(self.ctf.getPhaseLatticeParameterA(1), 3.5911)
        self.assertEqual(self.ctf.getPhaseLatticeParameterA(2), 2.87)
        self.assertEqual(self.ctf.getPhaseLatticeParameterA(3), 3.618)
        self.assertEqual(self.ctf.getPhaseLatticeParameterA(4), 2.859)
        self.assertEqual(self.ctf.getPhaseLatticeParameterA(5), 3.608)

    def testGetPhaseLatticeParameterB(self):
        self.assertEqual(self.ctf.getPhaseLatticeParameterB(1), 3.5911)
        self.assertEqual(self.ctf.getPhaseLatticeParameterB(2), 2.87)
        self.assertEqual(self.ctf.getPhaseLatticeParameterB(3), 3.618)
        self.assertEqual(self.ctf.getPhaseLatticeParameterB(4), 2.859)
        self.assertEqual(self.ctf.getPhaseLatticeParameterB(5), 3.608)

    def testGetPhaseLatticeParameterC(self):
        self.assertEqual(self.ctf.getPhaseLatticeParameterC(1), 3.5911)
        self.assertEqual(self.ctf.getPhaseLatticeParameterC(2), 2.87)
        self.assertEqual(self.ctf.getPhaseLatticeParameterC(3), 3.618)
        self.assertEqual(self.ctf.getPhaseLatticeParameterC(4), 3.016)
        self.assertEqual(self.ctf.getPhaseLatticeParameterC(5), 3.608)

    def getPhaseLatticeParameters(self, id):
        pass

    def testGetPhaseLatticeAngleAlpha(self):
        self.assertEqual(self.ctf.getPhaseLatticeAngleAlpha(1), 90)
        self.assertEqual(self.ctf.getPhaseLatticeAngleAlpha(2), 90)
        self.assertEqual(self.ctf.getPhaseLatticeAngleAlpha(3), 90)
        self.assertEqual(self.ctf.getPhaseLatticeAngleAlpha(4), 90)
        self.assertEqual(self.ctf.getPhaseLatticeAngleAlpha(5), 90)

    def testGetPhaseLatticeAngleBeta(self):
        self.assertEqual(self.ctf.getPhaseLatticeAngleBeta(1), 91)
        self.assertEqual(self.ctf.getPhaseLatticeAngleBeta(2), 92)
        self.assertEqual(self.ctf.getPhaseLatticeAngleBeta(3), 93)
        self.assertEqual(self.ctf.getPhaseLatticeAngleBeta(4), 94)
        self.assertEqual(self.ctf.getPhaseLatticeAngleBeta(5), 95)

    def testGetPhaseLatticeAngleGamma(self):
        self.assertEqual(self.ctf.getPhaseLatticeAngleGamma(1), 90)
        self.assertEqual(self.ctf.getPhaseLatticeAngleGamma(2), 90)
        self.assertEqual(self.ctf.getPhaseLatticeAngleGamma(3), 90)
        self.assertEqual(self.ctf.getPhaseLatticeAngleGamma(4), 90)
        self.assertEqual(self.ctf.getPhaseLatticeAngleGamma(5), 95)

    def testGetPhaseLatticeAngles(self):
        pass

    def testGetPhaseSpaceGroupNo(self):
        self.assertEqual(self.ctf.getPhaseSpaceGroupNo(1), 225)
        self.assertEqual(self.ctf.getPhaseSpaceGroupNo(2), 229)
        self.assertEqual(self.ctf.getPhaseSpaceGroupNo(3), 225)
        self.assertEqual(self.ctf.getPhaseSpaceGroupNo(4), 139)
        self.assertEqual(self.ctf.getPhaseSpaceGroupNo(5), 225)

    def testGetNumberPixels(self):
        self.assertEqual(self.ctf.getNumberPixels(), 8652)

    def testGetPixelIndex(self):
        self.assertEqual(self.ctf.getPixelIndex((0, 0)), 1)
        self.assertEqual(self.ctf.getPixelIndex((1, 1)), self.ctf.getXCells() + 2)

    def testGetPixelCoordinate(self):
        self.assertEqual(self.ctf.getPixelCoordinate(1), (0, 0))
        self.assertEqual(self.ctf.getPixelCoordinate(self.ctf.getWidth() + 2), (1, 1))
        self.assertEqual(self.ctf.getPixelCoordinate(self.ctf.getSize()), (self.ctf.getWidth() - 1, self.ctf.getHeight() - 1))

    def testGetPixelIndexLabel(self):
        self.assertEqual(self.ctf.getPixelIndexLabel(coord=(0, 0)), '0001')
        self.assertEqual(self.ctf.getPixelIndexLabel(coord=(1, 1)), '0105')
        self.assertEqual(self.ctf.getPixelIndexLabel(index=1), '0001')
        self.assertEqual(self.ctf.getPixelIndexLabel(index=105), '0105')

    def testGetPixelImageLabel(self):
        self.assertEqual(self.ctf.getPixelImageLabel(coord=(0, 0)), 'T009_040001')
        self.assertEqual(self.ctf.getPixelImageLabel(coord=(1, 1)), 'T009_040105')
        self.assertEqual(self.ctf.getPixelImageLabel(index=1), 'T009_040001')
        self.assertEqual(self.ctf.getPixelImageLabel(index=105), 'T009_040105')

    def testGetPixelResults_coordinate(self):
        coord = (0, 0)
        self.assertEquals(self.ctf.getPixelResults_coordinate(coord), {'euler3': 26.411999999999999, 'euler2': 6.2182000000000004, 'euler1': 15.380000000000001, 'bc': 59, 'bands': 6, 'bs': 62, 'y': 0.0, 'mad': 0.82709999999999995, 'errorcode': 0, 'error': 'Success', 'phase': 2, 'x': 0.0})

        coord = (self.ctf.getWidth(), self.ctf.getHeight())
        self.assertEquals(self.ctf.getPixelResults_coordinate(coord), {})

    def testGetPixelResults_index(self):
        index = 1
        self.assertEquals(self.ctf.getPixelResults_index(index), {'euler3': 26.411999999999999, 'euler2': 6.2182000000000004, 'euler1': 15.380000000000001, 'bc': 59, 'bands': 6, 'bs': 62, 'y': 0.0, 'mad': 0.82709999999999995, 'errorcode': 0, 'error': 'Success', 'phase': 2, 'x': 0.0})

        index = len(self.ctf._data) + 1
        self.assertEquals(self.ctf.getPixelResults_index(index), {})

    def testResultsLinetoDict(self):
        pass

    def testGetPixelArray(self):
        self.assertEquals(self.ctf.getPixelArray(key='euler3')[0], 26.412)

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
