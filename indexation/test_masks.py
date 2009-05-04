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
import EBSDTools.indexation.masks as masks
import RandomUtilities.testing.testImage as testImage

# Globals and constants variables.

class TestMasks(unittest.TestCase):

  def setUp(self):
    unittest.TestCase.setUp(self)
    
    self.basepath = os.path.join(EBSDTools.__path__[0], 'indexation/testData')
    
  def tearDown(self):
    unittest.TestCase.tearDown(self)
    
  def testSkeleton(self):
    #self.fail("Test if the TestCase is working.")
    self.assert_(True)
  
  def testCreateMaskDisc(self):
    #Centered
    maskMap = masks.createMaskDisc(width=168, height=128, centroid=(84,64), radius=59)
    maskMap.setFile(os.path.join(self.basepath, 'test_maskDisc.bmp'))
    IO.save(maskMap)
    self.assert_(testImage.equal(os.path.join(self.basepath, 'test_maskDisc.bmp'), os.path.join(self.basepath, 'maskDisc.bmp')))
    
    #In the corner
    maskMap = masks.createMaskDisc(width=168, height=128, centroid=(0,0), radius=59)
    maskMap.setFile(os.path.join(self.basepath, 'test_maskDisc2.bmp'))
    IO.save(maskMap)
    self.assert_(testImage.equal(os.path.join(self.basepath, 'test_maskDisc2.bmp'), os.path.join(self.basepath, 'maskDisc2.bmp')))

def cleanup():
  files = os.listdir(os.path.join(EBSDTools.__path__[0], 'indexation/testData/'))

  for file in files:
    if 'test_' in file:
      os.remove(os.path.join(EBSDTools.__path__[0], 'indexation/testData/', file))

if __name__ == '__main__':
  try:
    unittest.main()
  finally:
    cleanup()