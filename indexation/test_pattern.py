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
import RandomUtilities.testing.testOthers as testOthers

# Globals and constants variables.

class TestPattern(unittest.TestCase):

  def setUp(self):
    unittest.TestCase.setUp(self)
    
    self.basepath = os.path.join(EBSDTools.__path__[0], 'indexation/testData')
    
  def tearDown(self):
    unittest.TestCase.tearDown(self)
    
  def testSkeleton(self):
    #self.fail("Test if the TestCase is working.")
    self.assert_(True)
  
  def testInit(self):
    #Byte map (bmp)
    patt = pattern.Pattern(filepath=os.path.join(self.basepath, 'pattern1.bmp'))
    self.assertEqual(patt.width, 168)
    self.assertEqual(patt.height, 128)
    self.assertEqual(patt.patternMap.type, 'ByteMap')
    del patt
    
    #RGB Map (jpg)
    patt = pattern.Pattern(filepath=os.path.join(self.basepath, 'pattern2.jpg'))
    self.assertEqual(patt.width, 168)
    self.assertEqual(patt.height, 128)
    self.assertEqual(patt.patternMap.type, 'ByteMap')
    del patt
    
    #Byte Map from object
    file = java.io.File(os.path.join(self.basepath, 'pattern1.bmp'))
    byteMap = IO.load(file)
    patt = pattern.Pattern(byteMap=byteMap)
    self.assertEqual(patt.width, 168)
    self.assertEqual(patt.height, 128)
    self.assertEqual(patt.patternMap.type, 'ByteMap')
    del patt
  
  def testMean(self):
    patt = pattern.Pattern(filepath=os.path.join(self.basepath, 'pattern1.bmp'))
    self.assert_(testOthers.almostEqual(patt.getMean(), 120.18740699404762))
  
  def testStandardDeviation(self):
    patt = pattern.Pattern(filepath=os.path.join(self.basepath, 'pattern1.bmp'))
    self.assert_(testOthers.almostEqual(patt.getStandardDeviation(), 21.019772814547494))
    self.assert_(testOthers.almostEqual(patt.getStdDev(), 21.019772814547494))
    
    
if __name__ == '__main__':
  unittest.main()
