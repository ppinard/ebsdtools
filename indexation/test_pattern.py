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

# Globals and constants variables.

class TestPatternMap(unittest.TestCase):

  def setUp(self):
    unittest.TestCase.setUp(self)

    self.basepath = os.path.join(EBSDTools.__path__[0], 'indexation/testData')

    self.patt1 = pattern.PatternMap(filepath=os.path.join(self.basepath, 'pattern1.bmp'))
    self.patt2 = pattern.PatternMap(filepath=os.path.join(self.basepath, 'pattern2.jpg'))

    file = java.io.File(os.path.join(self.basepath, 'pattern1.bmp'))
    byteMap = IO.load(file)
    self.patt1Bytemap = pattern.PatternMap(byteMap=byteMap)

    self.maskMap = masks.MaskDisc(width=168, height=128, centroid=(84,64), radius=59)
    self.patt1Mask = pattern.PatternMap(filepath=os.path.join(self.basepath, 'pattern1.bmp'), maskMap=self.maskMap)

    file = java.io.File(os.path.join(self.basepath, 'pattern1Masked.bmp'))
    byteMap = IO.load(file)
    self.expectedPatt1Masked = pattern.PatternMap(byteMap=byteMap)

  def tearDown(self):
    unittest.TestCase.tearDown(self)

  def testSkeleton(self):
    #self.fail("Test if the TestCase is working.")
    self.assert_(True)

  def test__init__(self):
    self.assertEqual(self.patt1.width, 168)
    self.assertEqual(self.patt1.height, 128)
    self.assertEqual(self.patt1.getType(), 'ByteMap')

    self.assertEqual(self.patt2.width, 168)
    self.assertEqual(self.patt2.height, 128)
    self.assertEqual(self.patt2.getType(), 'ByteMap')

    self.assertEqual(self.patt1Bytemap.width, 168)
    self.assertEqual(self.patt1Bytemap.height, 128)
    self.assertEqual(self.patt1Bytemap.getType(), 'ByteMap')

    self.assertEqual(self.patt1Mask.width, 168)
    self.assertEqual(self.patt1Mask.height, 128)
    self.assertEqual(self.patt1Mask.getType(), 'ByteMap')

  def test_applyMask(self):
    self.patt1Mask.assertPixEquals(self.expectedPatt1Masked)

    self.patt1.applyMask(self.maskMap)
    self.patt1.assertPixEquals(self.patt1Mask)

  def test_getMaskMap(self):
    self.assertEqual(self.patt1.getMaskMap(), None)
    self.assertEqual(self.patt2.getMaskMap(), None)
    self.assertEqual(self.patt1Bytemap.getMaskMap(), None)
    self.patt1Mask.getMaskMap().assertPixEquals(self.maskMap)

  def test_getOriginalPattern(self):
    self.patt1.getOriginalPattern().assertPixEquals(self.patt1)
    self.patt2.getOriginalPattern().assertPixEquals(self.patt2)
    self.patt1Bytemap.getOriginalPattern().assertPixEquals(self.patt1Bytemap)
    self.patt1Mask.getOriginalPattern().assertPixEquals(self.patt1)

if __name__ == '__main__':
  unittest.main()
