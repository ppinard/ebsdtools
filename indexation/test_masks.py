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
    self.maskmap1 = masks.MaskDisc(width=168, height=128, centroid_x=84, centroid_y=64, radius=59)

    #In the corner
    self.maskmap2 = masks.MaskDisc(width=168, height=128, centroid_x=0, centroid_y=0, radius=59)

  def tearDown(self):
    unittest.TestCase.tearDown(self)

    shutil.rmtree(self.tmpfolder)

  def testSkeleton(self):
    #self.fail("Test if the TestCase is working.")
    self.assert_(True)

  def test__init__(self):
    self.maskmap1.setFile(os.path.join(self.tmpfolder, 'test_maskDisc.bmp'))
    IO.save(self.maskmap1)
    self.assertTrue(testImage.equal(os.path.join(self.tmpfolder, 'test_maskDisc.bmp')
                                    , os.path.join(self.basepath, 'maskDisc.bmp')))

    #In the corner
    self.maskmap2.setFile(os.path.join(self.tmpfolder, 'test_maskDisc2.bmp'))
    IO.save(self.maskmap2)
    self.assertTrue(testImage.equal(os.path.join(self.tmpfolder, 'test_maskDisc2.bmp')
                                    , os.path.join(self.basepath, 'maskDisc2.bmp')))

  def testgetradius(self):
    self.assertEqual(self.maskmap1.getradius(), 59)
    self.assertEqual(self.maskmap2.getradius(), 59)

  def testgetcentroid_x(self):
    self.assertEqual(self.maskmap1.getcentroid_x(), 84)
    self.assertEqual(self.maskmap2.getcentroid_x(), 0)

  def testgetcentroid_y(self):
    self.assertEqual(self.maskmap1.getcentroid_y(), 64)
    self.assertEqual(self.maskmap2.getcentroid_y(), 0)

  def testgetcentroid(self):
    self.assertEqual(self.maskmap1.getcentroid(), (84, 64))
    self.assertEqual(self.maskmap2.getcentroid(), (0, 0))

  def testgetbinmap(self):
    self.assertEqual(self.maskmap1.getbinmap().height, 128)
    self.assertEqual(self.maskmap2.getbinmap().height, 128)

if __name__ == '__main__': #pragma: no cover
  logging.getLogger().setLevel(logging.DEBUG)
  unittest.main()
