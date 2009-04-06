#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Philippe Pinard (philippe.pinard@gmail.com)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2008-2009 Philippe Pinard"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = ""
__svnDate__ = ""
__svnId__ = ""

# Standard library modules.
import unittest
from math import pi
import random

# Third party modules.

# Local modules.
import EBSDTools.mathTools.eulers as eulers
from RandomUtilities.testing.testOthers import almostEqual

# Globals and constants variables.
rep = 1000

class TestEulers(unittest.TestCase):

  def setUp(self):
    unittest.TestCase.setUp(self)
    
  def tearDown(self):
    unittest.TestCase.tearDown(self)
    
  def testSkeleton(self):
    #self.fail("Test if the TestCase is working.")
    self.assert_(True)
  
  def testInit(self):
    e1 = eulers.eulers(0.1,0.2,0.3)
    e2 = eulers.eulers([0.1,0.2,0.3])
    e3 = eulers.eulers((0.1,0.2,0.3))
    
    for i in range(3):
      self.assertEqual(e1.toRad()[i], e2.toRad()[i])
      self.assertEqual(e2.toRad()[i], e3.toRad()[i])
      self.assertEqual(e1.toRad()[i], e3.toRad()[i])
    
    e4 = eulers.eulers()
    self.assertEqual(e4.toRad(), (0,0,0))
  
  def testDegEulersToRadEulers(self):
    for i in range(rep):
      euler1 = random.random() * 360
      euler2 = random.random() * 180
      euler3 = random.random() * 360
      
      e1 = eulers.degEulersToRadEulers(euler1,euler2,euler3)
      
      self.assert_(almostEqual(e1.toDeg()[0], euler1))
      self.assert_(almostEqual(e1.toDeg()[1], euler2))
      self.assert_(almostEqual(e1.toDeg()[2], euler3))
      self.assert_(almostEqual(e1['theta1deg'], euler1))
      self.assert_(almostEqual(e1['theta2deg'], euler2))
      self.assert_(almostEqual(e1['theta3deg'], euler3))
  
  def testGetAttributes(self):
    for i in range(rep):
      euler1 = random.random()
      euler2 = random.random()
      euler3 = random.random()
      
      e1 = eulers.eulers(euler1,euler2,euler3)
      self.assertEqual(e1['theta1'], euler1)
      self.assertEqual(e1['theta2'], euler2)
      self.assertEqual(e1['theta3'], euler3)
      self.assertEqual(e1['theta1rad'], euler1)
      self.assertEqual(e1['theta2rad'], euler2)
      self.assertEqual(e1['theta3rad'], euler3)
      self.assert_(almostEqual(e1['theta1deg'], euler1 * 180.0 /pi))
      self.assert_(almostEqual(e1['theta2Deg'], euler2 * 180.0 /pi))
      self.assert_(almostEqual(e1['theta3dEg'], euler3 * 180.0 /pi))
      
      self.assertEqual(e1[1], euler1)
      self.assertEqual(e1[2], euler2)
      self.assertEqual(e1[3], euler3)
      
      self.assertEqual(e1['phi1'], euler1)
      self.assertEqual(e1['phi'], euler2)
      self.assertEqual(e1['phi2'], euler3)
      self.assertEqual(e1['phi1RAD'], euler1)
      self.assertEqual(e1['phiRAD'], euler2)
      self.assertEqual(e1['phi2RAD'], euler3)
      self.assert_(almostEqual(e1['phi1deg'], euler1 * 180.0 /pi))
      self.assert_(almostEqual(e1['phideg'], euler2 * 180.0 /pi))
      self.assert_(almostEqual(e1['phi2deg'], euler3 * 180.0 /pi))
      
      self.assertEqual(e1['alpha'], euler1)
      self.assertEqual(e1['beta'], euler2)
      self.assertEqual(e1['gamma'], euler3)
  
#  def testCheckIntegrity(self):
#    self.assertRaises(AssertionError, eulers.eulers, 4,4,4)
#    
#    #Negative definition
#    self.assertRaises(AssertionError, eulers.eulers, -pi/4, pi/4, 2*pi)
#    self.assertRaises(AssertionError, eulers.eulers, -pi/4,-pi/4, pi/4)
#    self.assertRaises(AssertionError, eulers.eulers, -pi/4, pi/4, 2*pi)
#    
#    #Positive definition
#    self.assertRaises(AssertionError, eulers.eulers,  pi/4, pi/4, 3*pi)
#    self.assertRaises(AssertionError, eulers.eulers,  pi/4,-pi/4, 2*pi)
  
  def testPositive(self):
    e1 = eulers.eulers(0,0,0).positive().toRad()
    self.assert_(almostEqual(e1[0], 0.0))
    self.assert_(almostEqual(e1[1], 0.0))
    self.assert_(almostEqual(e1[2], 0.0))
    
    e1 = eulers.eulers(pi, 0, pi).positive().toRad()
    self.assert_(almostEqual(e1[0], pi))
    self.assert_(almostEqual(e1[1], 0.0))
    self.assert_(almostEqual(e1[2], pi))
    
    e1 = eulers.eulers(-pi/2.0, 0, -pi/3).positive().toRad()
    self.assert_(almostEqual(e1[0], 3.0*pi/2.0))
    self.assert_(almostEqual(e1[1], 0.0))
    self.assert_(almostEqual(e1[2], 5.0*pi/3.0))
    
  def testNegative(self):
    e1 = eulers.eulers(0,0,0).negative().toRad()
    self.assert_(almostEqual(e1[0], 0.0))
    self.assert_(almostEqual(e1[1], 0.0))
    self.assert_(almostEqual(e1[2], 0.0))
    
    
    e1 = eulers.eulers(pi, 0, pi).negative().toRad()
    self.assert_(almostEqual(e1[0], pi))
    self.assert_(almostEqual(e1[1], 0.0))
    self.assert_(almostEqual(e1[2], pi))
    
    e1 = eulers.eulers(3.0*pi/2.0, 0, 5*pi/3).negative().toRad()
    self.assert_(almostEqual(e1[0], -pi/2.0))
    self.assert_(almostEqual(e1[1], 0))
    self.assert_(almostEqual(e1[2], -pi/3))
  
if __name__ == '__main__':
  unittest.main()