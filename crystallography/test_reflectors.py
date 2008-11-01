#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Philippe Pinard (philippe.pinard@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2008 Philippe Pinard"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = "$Revision$"
__svnDate__ = "$Date$"
__svnId__ = "$Id$"

# Standard library modules.
import unittest
import logging
from math import pi, sin, sqrt

# Third party modules.

# Local modules.
import EBSDTools.crystallography.reflectors as reflectors
import EBSDTools.crystallography.lattice as lattice

# Globals and constants variables.

class TestReciprocal(unittest.TestCase):

  def setUp(self):
    unittest.TestCase.setUp(self)
    
    self.Lbcc = lattice.Lattice(a=2.87, b=2.87, c=2.87, alpha=pi/2, beta=pi/2, gamma=pi/2, atoms = {(0,0,0): 26, (0.5,0.5,0.5): 26})
    self.Lfcc = lattice.Lattice(a=5.43, b=5.43, c=5.43, alpha=pi/2, beta=pi/2, gamma=pi/2, atoms = {(0,0,0): 14, (0.5,0.5,0): 14, (0.5,0,0.5): 14, (0,0.5,0.5): 14})
#    self.Lhexagonal = lattice.Lattice(a=2, b=2, c=3, alpha=pi/2, beta=pi/2, gamma=120.0/180*pi)
#TODO: HCP crystal
    
  def tearDown(self):
    unittest.TestCase.tearDown(self)

  def testSkeleton(self):
#    self.fail("Test if the testcase is working.")
    self.assert_(True)
  
  def testScatteringFactors(self):
    scatterF = reflectors.scatteringFactors()
    
    self.assertAlmostEqual(scatterF.getScatteringFactor(14, 0.5), 0.742519788187, 3)
    self.assertAlmostEqual(scatterF.getScatteringFactor(14, 3), 0.0349033998305, 3)
    self.assertAlmostEqual(scatterF.getScatteringFactor(14, 6.1), 0.00650227565622, 3)
    
    self.assertAlmostEqual(scatterF.getScatteringFactor(29, 0.5), 1.46390369208, 3)
    self.assertAlmostEqual(scatterF.getScatteringFactor(29, 3), 0.0652299842623, 3)
    self.assertAlmostEqual(scatterF.getScatteringFactor(29, 6.1), 0.000336590516491, 3)
    
    self.assertAlmostEqual(scatterF.getScatteringFactor(79, 0.5), 3.07239344718, 3)
    self.assertAlmostEqual(scatterF.getScatteringFactor(79, 3), 0.186031146844, 3)
    self.assertAlmostEqual(scatterF.getScatteringFactor(79, 6.1), 0.0332559532, 3)
  
  def testGetReflectorsDict(self):
    #bcc
    planesBCC = reflectors.Reflectors(self.Lbcc,maxIndice=1)
    self.assertEqual(planesBCC.getReflectorsDict(), planesBCC.reflectors)
    
    #fcc
    planesFCC = reflectors.Reflectors(self.Lfcc,maxIndice=1)
    self.assertEqual(planesFCC.getReflectorsDict(), planesFCC.reflectors)
  
  def testGetReflectorsList(self):
    #bcc
    planesBCC = reflectors.Reflectors(self.Lbcc,maxIndice=4).getReflectorsList()
    planesBCC_ = [(0, 1, 1), (1, 1, 0), (1, 0, 1), (1, -1, 0), (1, 0, -1), (0, 1, -1)]
    
    for plane in planesBCC_:
      self.assertTrue(plane in planesBCC)
      self.assertEqual((plane[0] + plane[1] + plane[2]) % 2, 0)
    
    planesBCC = reflectors.Reflectors(self.Lbcc,maxIndice=2).getReflectorsList()
    planesBCC_ = [(1, 0, 1), (1, 1, 0), (1, 0, -1), (1, -1, 0), (0, 2, 0), (2, 0, 0), (0, 0, 2), (1, 1, 2), (1, 2, 1), (2, 1, 1), (1, -2, -1), (2, 1, -1), (2, -1, -1), (1, 1, -2), (1, -1, -2), (1, 2, -1), (2, -1, 1), (1, -2, 1), (1, -1, 2), (0, 2, 2), (2, 0, 2), (2, 2, 0), (2, -2, 0), (2, 0, -2), (0, 2, -2), (2, 2,2), (2, -2, -2), (2, -2, 2), (2, 2, -2)]
    
    for plane in planesBCC_:
      self.assertTrue(plane in planesBCC)
      self.assertEqual((plane[0] + plane[1] + plane[2]) % 2, 0)
    
    #fcc
    planesFCC = reflectors.Reflectors(self.Lfcc,maxIndice=4).getReflectorsList()
    planesFCC_ = [(1, 1, 1), (1, -1, -1), (1, 1, -1), (1, -1, 1)]
    
    for plane in planesFCC_:
      self.assertTrue(plane in planesFCC)
      if plane[0] % 2 == 0: 
        self.assertEqual(plane[1] % 2, 0)
        self.assertEqual(plane[2] % 2, 0)
      else: # plane[0] % 2 == 1
        self.assertEqual(plane[1] % 2, 1)
        self.assertEqual(plane[2] % 2, 1)
    
    planesFCC = reflectors.Reflectors(self.Lfcc,maxIndice=4).getReflectorsList()
    planesFCC_ = [(1, 1, 1), (1, -1, -1), (1, 1, -1), (1, -1, 1), (0, 2, 0), (0, 0, 2), (2, 0, 0), (0, 2, 2), (2, 0, 2), (2, 2, 0), (0, 2, -2), (2, 0, -2), (2, -2, 0), (2, 2, 2), (2, -2, 2), (2, -2, -2), (2, 2, -2)]
    
    for plane in planesFCC_:
      self.assertTrue(plane in planesFCC)
      if plane[0] % 2 == 0: 
        self.assertEqual(plane[1] % 2, 0)
        self.assertEqual(plane[2] % 2, 0)
      else: # plane[0] % 2 == 1
        self.assertEqual(plane[1] % 2, 1)
        self.assertEqual(plane[2] % 2, 1)
  
  def testGetReflectorInfo(self):
    #bcc
    planesBCC = reflectors.Reflectors(self.Lbcc,maxIndice=1).getReflectorInfo((1,0,1))
    self.assertEqual(len(planesBCC), 4)
    self.assertEqual(planesBCC['normalized intensity'], 1.0)
    self.assertAlmostEqual(planesBCC['plane spacing'], 2.029396, 3)
    
    planesFCC = reflectors.Reflectors(self.Lfcc,maxIndice=1).getReflectorInfo((1,1,1))
    self.assertEqual(len(planesFCC), 4)
    self.assertEqual(planesFCC['normalized intensity'], 1.0)
    self.assertAlmostEqual(planesFCC['plane spacing'], 3.13501196, 3)
  
  def testGetReflectorPlaneSpacing(self):
    #Compared with HKL Channel 5 Phases Database
    
    #bcc
    planesBCC = reflectors.Reflectors(self.Lbcc,maxIndice=2)
    self.assertAlmostEqual(planesBCC.getReflectorPlaneSpacing((1,0,1)), 2.0294, 3)
    self.assertAlmostEqual(planesBCC.getReflectorPlaneSpacing((1,-1,0)), 2.0294, 3)
    self.assertAlmostEqual(planesBCC.getReflectorPlaneSpacing((2,0,0)), 1.4350, 3)
    self.assertAlmostEqual(planesBCC.getReflectorPlaneSpacing((1,-1,2)), 1.1717, 3)
    self.assertAlmostEqual(planesBCC.getReflectorPlaneSpacing((2,0,2)), 1.0147, 3)
    
    #fcc
    planesFCC = reflectors.Reflectors(self.Lfcc,maxIndice=2)
    self.assertAlmostEqual(planesFCC.getReflectorPlaneSpacing((1,1,1)), 3.1350, 3)
    self.assertAlmostEqual(planesFCC.getReflectorPlaneSpacing((1,-1,1)), 3.1350, 3)
    self.assertAlmostEqual(planesFCC.getReflectorPlaneSpacing((2,-2,0)), 1.9201, 3)
  
  def testGetReflectorIntensity(self):
    #bcc
    planesBCC = reflectors.Reflectors(self.Lbcc,maxIndice=2)
    self.assertAlmostEqual(planesBCC.getReflectorIntensity((1,0,1)), 0.018535906894, 3)
    self.assertAlmostEqual(planesBCC.getReflectorIntensity((1,-1,0)), 0.018535906894, 3)
    self.assertAlmostEqual(planesBCC.getReflectorIntensity((2,0,0)), 0.00230481501653, 3)
    
    #fcc
    planesFCC = reflectors.Reflectors(self.Lfcc,maxIndice=2)
    self.assertAlmostEqual(planesFCC.getReflectorIntensity((1,1,1)), 0.0859145669508, 3)
    self.assertAlmostEqual(planesFCC.getReflectorIntensity((1,-1,1)), 0.0859145669508, 3)
    self.assertAlmostEqual(planesFCC.getReflectorIntensity((2,-2,0)), 0.0152361124413, 3)
  
  def testGetReflectorNormalizedIntensity(self):
    #bcc
    planesBCC = reflectors.Reflectors(self.Lbcc,maxIndice=2)
    self.assertAlmostEqual(planesBCC.getReflectorNormalizedIntensity((1,0,1)), 1.0, 3)
    self.assertAlmostEqual(planesBCC.getReflectorNormalizedIntensity((1,-1,0)), 1.0, 3)
    self.assertAlmostEqual(planesBCC.getReflectorNormalizedIntensity((2,0,0)), 0.124343256023, 3)
    
    #fcc
    planesFCC = reflectors.Reflectors(self.Lfcc,maxIndice=2)
    self.assertAlmostEqual(planesFCC.getReflectorNormalizedIntensity((1,1,1)), 1.0, 3)
    self.assertAlmostEqual(planesFCC.getReflectorNormalizedIntensity((1,-1,1)), 1.0, 3)
    self.assertAlmostEqual(planesFCC.getReflectorNormalizedIntensity((2,-2,0)), 0.177340269316, 3)
  
  
if __name__ == '__main__':
  unittest.main()