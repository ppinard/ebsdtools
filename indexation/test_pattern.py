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
import EBSDTools
import EBSDTools.indexation.pattern as pattern
import EBSDTools.indexation.masks as masks
import RandomUtilities.testing.testOthers as testOthers

# Globals and constants variables.

class TestPattern(unittest.TestCase):

  def setUp(self):
    unittest.TestCase.setUp(self)
    
    self.basepath = os.path.join(EBSDTools.__path__[0], 'indexation/testData')
    
    self.patt1 = pattern.Pattern(filepath=os.path.join(self.basepath, 'pattern1.bmp'))
    self.patt2 = pattern.Pattern(filepath=os.path.join(self.basepath, 'pattern2.jpg'))
    
    file = java.io.File(os.path.join(self.basepath, 'pattern1.bmp'))
    byteMap = IO.load(file)
    self.patt1_bytemap = pattern.Pattern(byteMap=byteMap)
    
    maskMap = masks.createMaskDisc(width=168, height=128, centroid=(84,64), radius=59)
    self.patt1_mask = pattern.Pattern(filepath=os.path.join(self.basepath, 'pattern1.bmp'), maskMap=maskMap)
    
  def tearDown(self):
    unittest.TestCase.tearDown(self)
    
  def testSkeleton(self):
    #self.fail("Test if the TestCase is working.")
    self.assert_(True)
  
  def testInit(self):
    self.assertEqual(self.patt1.width, 168)
    self.assertEqual(self.patt1.height, 128)
    self.assertEqual(self.patt1.patternMap.type, 'ByteMap')
    
    self.assertEqual(self.patt2.width, 168)
    self.assertEqual(self.patt2.height, 128)
    self.assertEqual(self.patt2.patternMap.type, 'ByteMap')
    
    self.assertEqual(self.patt1_bytemap.width, 168)
    self.assertEqual(self.patt1_bytemap.height, 128)
    self.assertEqual(self.patt1_bytemap.patternMap.type, 'ByteMap')
    
    self.assertEqual(self.patt1_mask.width, 168)
    self.assertEqual(self.patt1_mask.height, 128)
    self.assertEqual(self.patt1_mask.patternMap.type, 'ByteMap')
  
  def testMean(self):
    self.assert_(testOthers.almostEqual(self.patt1.getMean(), 120.18740699404762))
    
    self.assert_(testOthers.almostEqual(self.patt1_bytemap.getMean(), 120.18740699404762))
    
    self.assert_(testOthers.almostEqual(self.patt2.getMean(), 185.03441220238096))
    
    self.assert_(testOthers.almostEqual(self.patt1_mask.getMean(), 119.18599321661014))
    
  def testStandardDeviation(self):
    self.assert_(testOthers.almostEqual(self.patt1.getStandardDeviation(), 21.019772814547494))
    self.assert_(testOthers.almostEqual(self.patt1.getStdDev(), 21.019772814547494))
    
    self.assert_(testOthers.almostEqual(self.patt1_bytemap.getStandardDeviation(), 21.019772814547494))
    self.assert_(testOthers.almostEqual(self.patt1_bytemap.getStdDev(), 21.019772814547494))
    
    self.assert_(testOthers.almostEqual(self.patt2.getStandardDeviation(), 13.695251010663885))
    self.assert_(testOthers.almostEqual(self.patt2.getStdDev(), 13.695251010663885))
    
    self.assert_(testOthers.almostEqual(self.patt1_mask.getStandardDeviation(), 22.344310430902024))
    self.assert_(testOthers.almostEqual(self.patt1_mask.getStdDev(), 22.344310430902024))

if __name__ == '__main__':
  unittest.main()
