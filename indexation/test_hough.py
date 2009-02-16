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
import RandomUtilities.testing.testImage as testImage

# Globals and constants variables.

class TestBragg(unittest.TestCase):

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
    maskMap = hough.createMaskDisc(width=168, height=128, centroid=(84,64), radius=59)
    maskMap.setFile(os.path.join(self.basepath, 'test_maskDisc.bmp'))
    IO.save(maskMap)
    self.assert_(testImage.equal(os.path.join(self.basepath, 'test_maskDisc.bmp'), os.path.join(self.basepath, 'maskDisc.bmp')))
    
    #In the corner
    maskMap = hough.createMaskDisc(width=168, height=128, centroid=(0,0), radius=59)
    maskMap.setFile(os.path.join(self.basepath, 'test_maskDisc2.bmp'))
    IO.save(maskMap)
    self.assert_(testImage.equal(os.path.join(self.basepath, 'test_maskDisc2.bmp'), os.path.join(self.basepath, 'maskDisc2.bmp')))
  
  def testInit(self):
    #Byte map (bmp)
    hh = hough.Hough(os.path.join(self.basepath, 'pattern1.bmp'))
    self.assertEqual(hh.width, 168)
    self.assertEqual(hh.height, 128)
    self.assertEqual(hh._map.type, 'ByteMap')
    del hh
    
    #RGB Map (jpg)
    hh = hough.Hough(os.path.join(self.basepath, 'pattern2.jpg'))
    self.assertEqual(hh.width, 168)
    self.assertEqual(hh.height, 128)
    self.assertEqual(hh._map.type, 'ByteMap')
    del hh
  
  def testCalculateHough(self):
    #Default
    hh = hough.Hough(os.path.join(self.basepath, 'pattern1.bmp'))
    hh.calculateHough(angleIncrement=0.5, maskMap=None)
    houghMap = hh.getHoughMap()
    houghMap.setFile(os.path.join(self.basepath, 'test_hough1.bmp'))
    IO.save(houghMap)
    self.assert_(testImage.equal(os.path.join(self.basepath, 'test_hough1.bmp'), os.path.join(self.basepath, 'hough1.bmp')))
    del hh
    
    #Different angle increment
    hh = hough.Hough(os.path.join(self.basepath, 'pattern1.bmp'))
    hh.calculateHough(angleIncrement=2, maskMap=None)
    houghMap = hh.getHoughMap()
    houghMap.setFile(os.path.join(self.basepath, 'test_hough2.bmp'))
    IO.save(houghMap)
    self.assert_(testImage.equal(os.path.join(self.basepath, 'test_hough2.bmp'), os.path.join(self.basepath, 'hough2.bmp')))
    del hh
    
    #With mask
    maskMap = hough.createMaskDisc(width=168, height=128, centroid=(84,64), radius=59)
    hh = hough.Hough(os.path.join(self.basepath, 'pattern1.bmp'))
    hh.calculateHough(angleIncrement=0.5, maskMap=maskMap)
    houghMap = hh.getHoughMap()
    houghMap.setFile(os.path.join(self.basepath, 'test_hough3.bmp'))
    IO.save(houghMap)
    self.assert_(testImage.equal(os.path.join(self.basepath, 'test_hough3.bmp'), os.path.join(self.basepath, 'hough3.bmp')))
    del hh
  
  def testFindPeaks(self):
    pass
  
  def testCalculateImageQuality(self):
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
    cleanup()