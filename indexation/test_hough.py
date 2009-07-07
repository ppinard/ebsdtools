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
import unittest

# Third party modules.
import rmlimage.io.IO as IO

# Local modules.
import EBSDTools
import EBSDTools.indexation.hough as hough
import EBSDTools.indexation.masks as masks
import EBSDTools.indexation.pattern as pattern
import RandomUtilities.testing.testImage as testImage

# Globals and constants variables.

class TestHough(unittest.TestCase):

  def setUp(self):
    unittest.TestCase.setUp(self)

    self.basepath = os.path.join(EBSDTools.__path__[0], 'indexation/testData')

    pattern1 = pattern.PatternMap(filepath=os.path.join(self.basepath, 'pattern1.bmp'))
    self.hough1 = hough.HoughMap(pattern1, angleIncrement=0.5)
    self.hough1_angle2 = hough.HoughMap(pattern1, angleIncrement=2)

    pattern2 = pattern.PatternMap(filepath=os.path.join(self.basepath, 'pattern2.jpg'))
    self.hough2 = hough.HoughMap(pattern2)

    maskMap = masks.MaskDisc(width=168, height=128, centroid=(84,64), radius=59)
    pattern1_mask = pattern.PatternMap(filepath=os.path.join(self.basepath, 'pattern1.bmp'), maskMap=maskMap)
    self.hough1_mask = hough.HoughMap(pattern1_mask)

  def tearDown(self):
    unittest.TestCase.tearDown(self)

  def testSkeleton(self):
    #self.fail("Test if the TestCase is working.")
    self.assert_(True)

  def testInit(self):
    #Byte map (bmp)
    self.assertEqual(self.hough1.patternMap.width, 168)
    self.assertEqual(self.hough1.patternMap.height, 128)

    #RGB Map (jpg)
    self.assertEqual(self.hough2.patternMap.width, 168)
    self.assertEqual(self.hough2.patternMap.height, 128)

  def testCalculateHough(self):
    #Default
    houghMap = self.hough1
    houghMap.setFile(os.path.join(self.basepath, 'test_hough1.bmp'))
    IO.save(houghMap)
    self.assert_(testImage.equal(os.path.join(self.basepath, 'test_hough1.bmp'), os.path.join(self.basepath, 'hough1.bmp')))

    #Different angle increment
    houghMap = self.hough1_angle2
    houghMap.setFile(os.path.join(self.basepath, 'test_hough2.bmp'))
    IO.save(houghMap)
    self.assert_(testImage.equal(os.path.join(self.basepath, 'test_hough2.bmp'), os.path.join(self.basepath, 'hough2.bmp')))

    #With mask
    houghMap = self.hough1_mask
    houghMap.setFile(os.path.join(self.basepath, 'test_hough3.bmp'))
    IO.save(houghMap)
    self.assert_(testImage.equal(os.path.join(self.basepath, 'test_hough3.bmp'), os.path.join(self.basepath, 'hough3.bmp')))

  def testFindPeaks(self):
#TODO: testFindPeaks in test_hough.py
    pass

  def testCalculateImageQuality(self):
#TODO: testCalculateImageQuality in test_hough.py
    pass

def cleanup():
  files = os.listdir(os.path.join(EBSDTools.__path__[0], 'indexation/testData/'))

  for file in files:
    if 'test_' in file:
      os.remove(os.path.join(EBSDTools.__path__[0], 'indexation/testData/', file))

if __name__ == '__main__':
  try:
    unittest.main()
  finally:
    pass
#    cleanup()
