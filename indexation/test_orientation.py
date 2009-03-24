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
from math import pi, sqrt

# Third party modules.

# Local modules.
import EBSDTools.indexation.orientation as orientation
import EBSDTools.indexation.kikuchi as kikuchi
import EBSDTools.mathTools.vectors as vectors
import EBSDTools.mathTools.quaternions as quaternions
import EBSDTools.mathTools.eulers as eulers
import RandomUtilities.testing.testOthers as testOthers

# Globals and constants variables.

class TestOrientation(unittest.TestCase):

  def setUp(self):
    unittest.TestCase.setUp(self)
    
  def tearDown(self):
    unittest.TestCase.tearDown(self)
    
  def testSkeleton(self):
    #self.fail("Test if the TestCase is working.")
    self.assert_(True)
  
  def testCalculateOrientation(self):
    """
    Test using orthogonal lines passing through the pattern center
    """
    line1 = kikuchi.houghPeakToKikuchiLine(0, 0, (100,100)) #Vertical
    line2 = kikuchi.houghPeakToKikuchiLine(0, pi/2.0, (100,100)) #Horizontal
    normal1 = kikuchi.kikuchiLineToNormal(line1[0], line1[1], (0,0), 10, (100,100))
    normal2 = kikuchi.kikuchiLineToNormal(line2[0], line2[1], (0,0), 10, (100,100))
    
    #Test1: eulers=(0,0,0)
    hkl1 = vectors.vector(1,0,0) #Vertical
    hkl2 = vectors.vector(0,0,1) #Horizontal
    q1 = orientation.calculateOrientation(normal1, normal2, hkl1, hkl2)
    q2 = orientation.calculateOrientationWright(normal1, normal2, hkl1, hkl2)
    self.assert_(testOthers.almostEqual(q1, q2))
    print q1, quaternions.eulerAnglesToQuaternion(eulers.eulers(0,pi,0))
    print q1.toEulerAngles()
#    self.assert_(testOthers.eitherEqual(q1.toEulerAngles().toDeg(), [(0,0,0), (360,0,0)]))
    
    #Test2: eulers=(90,0,0)
    hkl1 = vectors.vector(0,1,0) #Vertical
    hkl2 = vectors.vector(0,0,1) #Horizontal
    q1 = orientation.calculateOrientation(normal1, normal2, hkl1, hkl2)
    q2 = orientation.calculateOrientationWright(normal1, normal2, hkl1, hkl2)
    self.assert_(testOthers.almostEqual(q1, q2))
    print q1.toEulerAngles()
#    self.assert_(testOthers.eitherEqual(q1.toEulerAngles().toDeg(), [(0,0,0), (270,0,0)]))
    
    #Test3: eulers=(0,90,0)
    hkl1 = vectors.vector(1,0,0) #Vertical
    hkl2 = vectors.vector(0,1,0) #Horizontal
    q1 = orientation.calculateOrientation(normal1, normal2, hkl1, hkl2)
    q2 = orientation.calculateOrientationWright(normal1, normal2, hkl1, hkl2)
    self.assert_(testOthers.almostEqual(q1, q2))
    print q1.toEulerAngles()
#    self.assert_(testOthers.eitherEqual(q1.toEulerAngles().toDeg(), [(0,90,0), (180,90,0)]))
    
    #Test4: eulers=(90,90,0)
    hkl1 = vectors.vector(0,0,1) #Vertical
    hkl2 = vectors.vector(0,1,0) #Horizontal
    q1 = orientation.calculateOrientation(normal1, normal2, hkl1, hkl2)
    q2 = orientation.calculateOrientationWright(normal1, normal2, hkl1, hkl2)
    self.assert_(testOthers.almostEqual(q1, q2))
    print q1.toEulerAngles()
#    self.assert_(testOthers.eitherEqual(q1.toEulerAngles().toDeg(), [(90,90,0), (270,90,0)]))
    
    #Test5: eulers=(0,90,90)
    hkl1 = vectors.vector(0,1,0) #Vertical
    hkl2 = vectors.vector(1,0,0) #Horizontal
    q1 = orientation.calculateOrientation(normal1, normal2, hkl1, hkl2)
    q2 = orientation.calculateOrientationWright(normal1, normal2, hkl1, hkl2)
    self.assert_(testOthers.almostEqual(q1, q2))
    print q1.toEulerAngles()
#    self.assert_(testOthers.eitherEqual(q1.toEulerAngles().toDeg(), [(0,90,90), (180,90,90)]))
    
    #Test6: eulers=(90,90,90)
    hkl1 = vectors.vector(0,0,1) #Vertical
    hkl2 = vectors.vector(1,0,0) #Horizontal
    q1 = orientation.calculateOrientation(normal1, normal2, hkl1, hkl2)
    q2 = orientation.calculateOrientationWright(normal1, normal2, hkl1, hkl2)
    self.assert_(testOthers.almostEqual(q1, q2))
    print q1.toEulerAngles()
#    self.assert_(testOthers.eitherEqual(q1.toEulerAngles().toDeg(), [(90,90,90), (270,90,90)]))
    
    #Test7: eulers=(90,0,90)
    hkl1 = vectors.vector(1,0,0) #Vertical
    hkl2 = vectors.vector(0,0,1) #Horizontal
    q1 = orientation.calculateOrientation(normal1, normal2, hkl1, hkl2)
    q2 = orientation.calculateOrientationWright(normal1, normal2, hkl1, hkl2)
    self.assert_(testOthers.almostEqual(q1, q2))
    print q1.toEulerAngles()
#    self.assert_(testOthers.eitherEqual(q1.toEulerAngles().toDeg(), [(90,0,90), (0,0,0), (180,0,0)]))
    
    """
    Test using orthogonal lines not passing through the pattern center
    """
    line1 = kikuchi.houghPeakToKikuchiLine(-30, 0, (100,100)) #Vertical
    line2 = kikuchi.houghPeakToKikuchiLine(30, pi/2.0, (100,100)) #Horizontal
    normal1 = kikuchi.kikuchiLineToNormal(line1[0], line1[1], (0,0), 30, (100,100))
    normal2 = kikuchi.kikuchiLineToNormal(line2[0], line2[1], (0,0), 30, (100,100))
    print line1, line2
    print normal1, normal2
    
    #Test1: eulers=(0,0,0)
    hkl1 = vectors.vector(1,1,0) #Vertical
    hkl2 = vectors.vector(0,1,-1) #Horizontal
    q1 = orientation.calculateOrientation(normal1, normal2, hkl1, hkl2)
    print q1 
    print q1.toEulerAngles()
    
    #Test1: eulers=(90,0,0)
    hkl1 = vectors.vector(1,-1,0) #Vertical
    hkl2 = vectors.vector(1,0,-1) #Horizontal
    q1 = orientation.calculateOrientation(normal1, normal2, hkl1, hkl2)
    q2 = orientation.calculateOrientationWright(normal1, normal2, hkl1, hkl2)
    print q1, q2 
    print q1.toEulerAngles()

if __name__ == '__main__':
  unittest.main()
