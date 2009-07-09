#!/usr/bin/env jython
""" """

# Script information for the file.
__author__ = "Philippe Pinard (philippe.pinard@gmail.com)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2009 Philippe Pinard"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = ""
__svnDate__ = ""
__svnId__ = ""

# Standard library modules.
import os
import java.io
import unittest

# Third party modules.
import rmlimage.io.IO as IO

# Local modules.
import DrixUtilities.Files as Files

import EBSDTools.indexation.pattern as pattern
import EBSDTools.indexation.masks as masks
import EBSDTools.indexation.hough as hough
import EBSDTools.indexation.qualityIndexes as qualityIndexes
import RandomUtilities.testing.testOthers as testOthers

# Globals and constants variables.

class TestPattern(unittest.TestCase):

  def setUp(self):
    unittest.TestCase.setUp(self)

    self.basepath = Files.getCurrentModulePath(__file__, 'testData')

    self.patt1 = pattern.PatternMap(filepath=os.path.join(self.basepath, 'pattern1.bmp'))
    self.patt2 = pattern.PatternMap(filepath=os.path.join(self.basepath, 'pattern2.jpg'))

    maskMap = masks.MaskDisc(width=168, height=128, centroid=(84,64), radius=59)
    self.patt1_mask = pattern.PatternMap(filepath=os.path.join(self.basepath, 'pattern1.bmp'), maskMap=maskMap)

    self.houghMap1 = hough.HoughMap(self.patt1)
    self.houghMap2 = hough.HoughMap(self.patt2)
    self.houghMap1_mask = hough.HoughMap(self.patt1_mask)

  def tearDown(self):
    unittest.TestCase.tearDown(self)

  def testSkeleton(self):
    #self.fail("Test if the TestCase is working.")
    self.assert_(True)

  def testAverage(self):
    self.assertAlmostEqual(qualityIndexes.average(self.patt1).getValue(), 120.18740699404762)
    self.assertAlmostEqual(qualityIndexes.average(self.patt2).getValue(), 185.03441220238096)
    self.assertAlmostEqual(qualityIndexes.average(self.patt1_mask).getValue(), 119.18599321661014)

  def testStandardDeviation(self):
    self.assertAlmostEqual(qualityIndexes.standardDeviation(self.patt1).getValue(), 21.019284067867865)
    self.assertAlmostEqual(qualityIndexes.standardDeviation(self.patt2).getValue(), 13.694932571995967)
    self.assertAlmostEqual(qualityIndexes.standardDeviation(self.patt1_mask).getValue(), 22.343286284668835)

  def testEntropy(self):
    self.assertAlmostEqual(qualityIndexes.entropy(self.patt1).getValue(), 4.43242443078881)
    self.assertAlmostEqual(qualityIndexes.entropy(self.patt2).getValue(), 3.97832952545196247)
    self.assertAlmostEqual(qualityIndexes.entropy(self.patt1_mask).getValue(), 4.502349539585318)

  def testImageQuality(self):
    self.assertAlmostEqual(qualityIndexes.imageQuality(self.houghMap1).getValue(3), 163.341395359)
    self.assertAlmostEqual(qualityIndexes.imageQuality(self.houghMap2).getValue(3), 170.371520946)
    self.assertAlmostEqual(qualityIndexes.imageQuality(self.houghMap1_mask).getValue(3), 150.780082805)

  def testNumberPeaks(self):
    self.assertEqual(qualityIndexes.numberPeaks(self.houghMap1).getValue(), 13)
    self.assertEqual(qualityIndexes.numberPeaks(self.houghMap2).getValue(), 20)
    self.assertEqual(qualityIndexes.numberPeaks(self.houghMap1_mask).getValue(), 15)

  def testAverageIntensity(self):
    self.assertAlmostEqual(qualityIndexes.averageIntensity(self.houghMap1).getValue(3), 163.341395359)
    self.assertAlmostEqual(qualityIndexes.averageIntensity(self.houghMap2).getValue(3), 170.371520946)
    self.assertAlmostEqual(qualityIndexes.averageIntensity(self.houghMap1_mask).getValue(3), 150.780082805)

  def testStandardDeviationIntensity(self):
    self.assertAlmostEqual(qualityIndexes.standardDeviationIntensity(self.houghMap1).getValue(3), 15.3658991169)
    self.assertAlmostEqual(qualityIndexes.standardDeviationIntensity(self.houghMap2).getValue(3), 9.80636044478)
    self.assertAlmostEqual(qualityIndexes.standardDeviationIntensity(self.houghMap1_mask).getValue(3), 28.1453966376)

if __name__ == '__main__':
  unittest.main()
