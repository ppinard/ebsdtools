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
import EBSDTools.indexation.qualityIndexes as qualityIndexes
import RandomUtilities.testing.testOthers as testOthers

# Globals and constants variables.

class TestPattern(unittest.TestCase):

  def setUp(self):
    unittest.TestCase.setUp(self)
    
    self.basepath = os.path.join(EBSDTools.__path__[0], 'indexation/testData')
    
    self.patt1 = pattern.Pattern(filepath=os.path.join(self.basepath, 'pattern1.bmp'))
    self.patt2 = pattern.Pattern(filepath=os.path.join(self.basepath, 'pattern2.jpg'))
    
    maskMap = masks.createMaskDisc(width=168, height=128, centroid=(84,64), radius=59)
    self.patt1_mask = pattern.Pattern(filepath=os.path.join(self.basepath, 'pattern1.bmp'), maskMap=maskMap)
    
  def tearDown(self):
    unittest.TestCase.tearDown(self)
    
  def testSkeleton(self):
    #self.fail("Test if the TestCase is working.")
    self.assert_(True)
  
  def testAverage(self):
    self.assert_(testOthers.almostEqual(qualityIndexes.average().calculate(self.patt1), 120.18740699404762))
    self.assert_(testOthers.almostEqual(qualityIndexes.average().calculate(self.patt2), 185.03441220238096))
    self.assert_(testOthers.almostEqual(qualityIndexes.average().calculate(self.patt1_mask), 119.18599321661014))
    
  def testStandardDeviation(self):
    self.assert_(testOthers.almostEqual(qualityIndexes.standardDeviation().calculate(self.patt1), 21.019284067867865))
    self.assert_(testOthers.almostEqual(qualityIndexes.standardDeviation().calculate(self.patt2), 13.694932571995967))
    self.assert_(testOthers.almostEqual(qualityIndexes.standardDeviation().calculate(self.patt1_mask), 22.343286284668835))
  
  def testEntropy(self):
    self.assert_(testOthers.almostEqual(qualityIndexes.entropy().calculate(self.patt1), 4.43242443078881))
    self.assert_(testOthers.almostEqual(qualityIndexes.entropy().calculate(self.patt2), 3.97832952545196247))
    self.assert_(testOthers.almostEqual(qualityIndexes.entropy().calculate(self.patt1_mask), 4.502349539585318))

if __name__ == '__main__':
  unittest.main()
