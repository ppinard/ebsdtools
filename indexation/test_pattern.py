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

class TestPatternMap(unittest.TestCase):

  def setUp(self):
    unittest.TestCase.setUp(self)
    
    self.basepath = os.path.join(EBSDTools.__path__[0], 'indexation/testData')
    
    self.patt1 = pattern.PatternMap(filepath=os.path.join(self.basepath, 'pattern1.bmp'))
    self.patt2 = pattern.PatternMap(filepath=os.path.join(self.basepath, 'pattern2.jpg'))
    
    file = java.io.File(os.path.join(self.basepath, 'pattern1.bmp'))
    byteMap = IO.load(file)
    self.patt1_bytemap = pattern.PatternMap(byteMap=byteMap)
    
    self.maskMap = masks.MaskDisc(width=168, height=128, centroid=(84,64), radius=59)
    self.patt1_mask = pattern.PatternMap(filepath=os.path.join(self.basepath, 'pattern1.bmp'), maskMap=self.maskMap)
    
  def tearDown(self):
    unittest.TestCase.tearDown(self)
    
  def testSkeleton(self):
    #self.fail("Test if the TestCase is working.")
    self.assert_(True)
  
  def testInit(self):
    self.assertEqual(self.patt1.width, 168)
    self.assertEqual(self.patt1.height, 128)
    self.assertEqual(self.patt1.getType(), 'ByteMap')
    
    self.assertEqual(self.patt2.width, 168)
    self.assertEqual(self.patt2.height, 128)
    self.assertEqual(self.patt2.getType(), 'ByteMap')
    
    self.assertEqual(self.patt1_bytemap.width, 168)
    self.assertEqual(self.patt1_bytemap.height, 128)
    self.assertEqual(self.patt1_bytemap.getType(), 'ByteMap')
    
    self.assertEqual(self.patt1_mask.width, 168)
    self.assertEqual(self.patt1_mask.height, 128)
    self.assertEqual(self.patt1_mask.getType(), 'ByteMap')
  
  def testGetMaskMap(self):
    self.assertEqual(self.patt1.getMaskMap(), None)
    self.assertEqual(self.patt2.getMaskMap(), None)
    self.assertEqual(self.patt1_bytemap.getMaskMap(), None)
    self.assertEqual(self.patt1_mask.getMaskMap().pixArray, self.maskMap.pixArray)
  
  def testGetOriginalPattern(self):
    self.assertEqual(self.patt1.getOriginalPattern().pixArray, self.patt1.pixArray)
    self.assertEqual(self.patt2.getOriginalPattern().pixArray, self.patt2.pixArray)
    self.assertEqual(self.patt1_bytemap.getOriginalPattern().pixArray, self.patt1_bytemap.pixArray)
    self.assertEqual(self.patt1_mask.getOriginalPattern().pixArray, self.patt1.pixArray)
  
if __name__ == '__main__':
  unittest.main()
