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
from math import pi

# Third party modules.
import scitools.multipleloop as multipleloop

# Local modules.
import EBSDTools.indexation.kikuchi as kikuchi
import EBSDTools.mathTools.vectors as vectors
import RandomUtilities.testing.testOthers as testOthers

# Globals and constants variables.

class TestKikuchi(unittest.TestCase):

  def setUp(self):
    unittest.TestCase.setUp(self)
    
    self._parameters = {'angle': range(0,180,5)
                        , 'rho': [-49] + range(-40,50,10) + [49]
                        , 'detectorDistance': range(1,10,1)
                        }
    self._patternSize = (100,100)
    
  def tearDown(self):
    unittest.TestCase.tearDown(self)
    
  def testSkeleton(self):
    #self.fail("Test if the TestCase is working.")
    self.assert_(True)
  
  def testHoughPeakKikuchiLine(self):
    #Vertical line centered
    line = kikuchi.houghPeakToKikuchiLine(0,0,(100,100))
    testOthers.assertAlmostEqual(line[0], (50.0, 0.0))
    testOthers.assertAlmostEqual(line[1], (50.0, 99.0))
    
    #Top left to bottom right line
    line = kikuchi.houghPeakToKikuchiLine(0,45/180.0*pi,(100,100))
    testOthers.assertAlmostEqual(line[0], (1.0, 99.0))
    testOthers.assertAlmostEqual(line[1], (99.0, 1.0))
    
    #Bottom left to top right line
    line = kikuchi.houghPeakToKikuchiLine(0,135/180.0*pi,(100,100))
    testOthers.assertAlmostEqual(line[0], (0.0, 0.0))
    testOthers.assertAlmostEqual(line[1], (99.0, 99.0))
    
    #Horizontal line centered
    line = kikuchi.houghPeakToKikuchiLine(0,90/180.0*pi,(100,100))
    testOthers.assertAlmostEqual(line[0], (0.0, 50.0))
    testOthers.assertAlmostEqual(line[1], (99.0, 50.0))
  
  def testKikuchiLineToNormal_Graph(self):
    parameters = {'angle': self._parameters['angle']
                  , 'rho': self._parameters['rho']}
    
    resultsFile = open('test_kikuchi.csv','w')
    
    for angle in parameters['angle']:
      for rho in parameters['rho']:
        line = kikuchi.houghPeakToKikuchiLine(rho,angle/180.0*pi,self._patternSize)
        normal = kikuchi.kikuchiLineToNormal(line[0], line[1], (0,0), 10, self._patternSize)
      
        resultsFile.write('%f,%f,%f,' % (normal[0], normal[1], normal[2]))
      
      resultsFile.write('\n')
  
    resultsFile.close()
    
#    Run test_kikuchi_graph.py
  
  def testKikuchiLineToNormal(self):
    """
    Back calculation of the line slope from the normal: line -> normal -> line (slope)
    """
    parameters = self._parameters.copy()
    parameters['angle'].remove(0) #Slope undefined at theta = 0
    (allTests, names, varied) = multipleloop.combine(parameters)
    
    for values in allTests:
      test = dict(zip(names, values))
      
      line = kikuchi.houghPeakToKikuchiLine(test['rho'], test['angle']/180.0*pi,self._patternSize)
      slope = (line[1][1] - line[0][1]) / (line[1][0] - line[0][0])
      
      normal = kikuchi.kikuchiLineToNormal(line[0], line[1], (10,10), test['detectorDistance'], self._patternSize)
      v1 = vectors.vector(0,test['detectorDistance'],0)
      line_ = vectors.cross(v1, normal).normalize()
      slope_ = line_[2] / line_[0]
      
      testOthers.assertAlmostEqual(slope, slope_)
    
    """
    Value verification with the pattern center 
    """
    #Horizontal line
    #{rho=10, pc=(10,0)} == {rho=0, pc=(0,0)}
    line1 = kikuchi.houghPeakToKikuchiLine(10, 0/180.0*pi,self._patternSize)
    normal1 = kikuchi.kikuchiLineToNormal(line1[0], line1[1], (10,0), 10, self._patternSize)
    line2 = kikuchi.houghPeakToKikuchiLine(0, 0/180.0*pi,self._patternSize)
    normal2 = kikuchi.kikuchiLineToNormal(line2[0], line2[1], (0,0), 10, self._patternSize)
    testOthers.assertAlmostEqual(normal1.toList(), normal2.toList())
    
    #{rho=20, pc=(10,0)} == {rho=10, pc=(0,0)}
    line1 = kikuchi.houghPeakToKikuchiLine(20, 0/180.0*pi,self._patternSize)
    normal1 = kikuchi.kikuchiLineToNormal(line1[0], line1[1], (10,0), 10, self._patternSize)
    line2 = kikuchi.houghPeakToKikuchiLine(10, 0/180.0*pi,self._patternSize)
    normal2 = kikuchi.kikuchiLineToNormal(line2[0], line2[1], (0,0), 10, self._patternSize)
    testOthers.assertAlmostEqual(normal1.toList(), normal2.toList())
    
    #Vertical line
    #{rho=10, pc=(0,10)} == {rho=0, pc=(0,0)}
    line1 = kikuchi.houghPeakToKikuchiLine(10, 90/180.0*pi,self._patternSize)
    normal1 = kikuchi.kikuchiLineToNormal(line1[0], line1[1], (0,10), 10, self._patternSize)
    line2 = kikuchi.houghPeakToKikuchiLine(0, 90/180.0*pi,self._patternSize)
    normal2 = kikuchi.kikuchiLineToNormal(line2[0], line2[1], (0,0), 10, self._patternSize)
    testOthers.assertAlmostEqual(normal1.toList(), normal2.toList())
    
    #{rho=20, pc=(0,10)} == {rho=10, pc=(0,0)}
    line1 = kikuchi.houghPeakToKikuchiLine(20, 90/180.0*pi,self._patternSize)
    normal1 = kikuchi.kikuchiLineToNormal(line1[0], line1[1], (0,10), 10, self._patternSize)
    line2 = kikuchi.houghPeakToKikuchiLine(10, 90/180.0*pi,self._patternSize)
    normal2 = kikuchi.kikuchiLineToNormal(line2[0], line2[1], (0,0), 10, self._patternSize)
    testOthers.assertAlmostEqual(normal1.toList(), normal2.toList())


if __name__ == '__main__':
  unittest.main()
