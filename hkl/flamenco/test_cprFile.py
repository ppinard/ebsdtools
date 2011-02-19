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

import ebsdtools.hkl.flamenco.cprFile as cprFile

# Globals and constants variables.

class TestCprFile(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        testDataFolder = Files.getCurrentModulePath(__file__, '')
        self.testCprFilepath = os.path.join(testDataFolder, 'cprmaster.cpr')

        self.cpr = cprFile.cpr(self.testCprFilepath)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        #self.fail("Test if the testcase is working.")
        self.assert_(True)

    def testInit(self):
        keysMaster = len(self.cpr.getCprDict().keys())
        keysDefaultParameters = len(self.cpr.defaultParameters.keys())

        self.assertEquals(keysMaster, keysDefaultParameters)

    def testDefaultParameters(self):
        for section in self.cpr.defaultParameters.keys():
            for option in self.cpr.defaultParameters[section]:
                if self.cpr.defaultParameters[section][option][1] != None:
                    self.assert_(self.cpr.validateMinMax(section, option, self.cpr.defaultParameters[section][option][1])[0])

    def testValidateMinMax(self):
        for section in self.cpr.defaultParameters.keys():
            for option in self.cpr.defaultParameters[section]:
                type = self.cpr.defaultParameters[section][option][0]

                self.assert_(self.cpr.validateMinMax(section, option, self.cpr.defaultParameters[section][option][2])[0])
                self.assert_(self.cpr.validateMinMax(section, option, self.cpr.defaultParameters[section][option][3])[0])

    def testValidateSpecial(self):
        binnings = ["No binning", "2x2 binning", "4x4 binning", "8x8 binning", "8x8 superfast"]

        for binning in binnings:
            self.assert_(self.cpr.validateSpecial("FG_DCam parameters", "binning", binning)[0])

        gains = ["Low", "High"]

        for gain in gains:
            self.assert_(self.cpr.validateSpecial("Invalid Binning", "gain", gain)[0])

    def testCrossRef(self):
        self.cpr.crossRef("FG_DCam parameters", "binning", "4x4 binning")

        right = 335
        bottom = 255

        self.assertEquals(self.cpr.defaultParameters["AOI3DHough"]["right"][1], right)
        self.assertEquals(self.cpr.defaultParameters["AOI3DHough"]["bottom"][1], bottom)
        self.assertEquals(self.cpr.defaultParameters["AOI3DHough"]["right"][3], right)
        self.assertEquals(self.cpr.defaultParameters["AOI3DHough"]["bottom"][3], bottom)
        self.assertEquals(self.cpr.defaultParameters["AOI3DHough"]["left"][3], right)
        self.assertEquals(self.cpr.defaultParameters["AOI3DHough"]["top"][3], bottom)

        if self.cpr.setParameter('Job', 'xcells', 10)[0] and self.cpr.setParameter('Job', 'ycells', 2)[0]:
            self.assertAlmostEqual(self.cpr.getParameter('Job', 'noofpoints'), 20)

    def testGetParameter(self):
        if self.cpr.setParameter('ProjectionParameters', 'vhratio', 1.0)[0]:
            self.assertAlmostEquals(self.cpr.getParameter('ProjectionParameters', 'vhratio'), 1.0)
        else:
            self.fail

    def testSetParameter(self):
        self.assert_(self.cpr.setParameter('ProjectionParameters', 'vhratio', 1.0)[0])
        self.assert_(not self.cpr.setParameter('ProjectionParameters', 'vhratio', -1.0)[0])

    def testFormatValue(self):
        self.assertEquals(self.cpr.formatValue("AOI3DHough", "right", '1'), 1)

    def testValuetoParameter(self):
        pass

    def testParametertoValue(self):
        pass

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
