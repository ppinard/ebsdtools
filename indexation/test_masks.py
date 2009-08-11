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
import logging
import tempfile
import shutil

# Third party modules.
import rmlimage.io.IO as IO

# Local modules.
import DrixUtilities.Files as Files
import EBSDTools.indexation.masks as masks
import RandomUtilities.testing.testImage as testImage

# Globals and constants variables.

class TestMasks(unittest.TestCase):

  def setUp(self):
    unittest.TestCase.setUp(self)

    self.basepath = Files.getCurrentModulePath(__file__, 'testData')
    self.tmpfolder = tempfile.mkdtemp()

    #Centered
    self.maskMap1 = masks.MaskDisc(width=168, height=128, centroid_x=84, centroid_y=64, radius=59)

    #In the corner
    self.maskMap2 = masks.MaskDisc(width=168, height=128, centroid_x=0, centroid_y=0, radius=59)

  def tearDown(self):
    unittest.TestCase.tearDown(self)

    shutil.rmtree(self.tmpfolder)

  def testSkeleton(self):
    #self.fail("Test if the TestCase is working.")
    self.assert_(True)

  def test__init__(self):
    self.maskMap1.setFile(os.path.join(self.tmpfolder, 'test_maskDisc.bmp'))
    IO.save(self.maskMap1)
    self.assertTrue(testImage.equal(os.path.join(self.tmpfolder, 'test_maskDisc.bmp')
                                    , os.path.join(self.basepath, 'maskDisc.bmp')))

    #In the corner
    self.maskMap2.setFile(os.path.join(self.tmpfolder, 'test_maskDisc2.bmp'))
    IO.save(self.maskMap2)
    self.assertTrue(testImage.equal(os.path.join(self.tmpfolder, 'test_maskDisc2.bmp')
                                    , os.path.join(self.basepath, 'maskDisc2.bmp')))

  def testget_radius(self):
    self.assertEqual(self.maskMap1.getradius(), 59)
    self.assertEqual(self.maskMap2.getradius(), 59)

  def testget_centroid_x(self):
    self.assertEqual(self.maskMap1.getcentroid_x(), 84)
    self.assertEqual(self.maskMap2.getcentroid_x(), 0)

  def testget_centroid_y(self):
    self.assertEqual(self.maskMap1.getcentroid_y(), 64)
    self.assertEqual(self.maskMap2.getcentroid_y(), 0)

  def testget_centroid(self):
    self.assertEqual(self.maskMap1.getcentroid(), (84, 64))
    self.assertEqual(self.maskMap2.getcentroid(), (0, 0))

if __name__ == '__main__': #pragma: no cover
  logging.getLogger().setLevel(logging.DEBUG)
  unittest.main()
