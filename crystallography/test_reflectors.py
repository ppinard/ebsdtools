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
import warnings
from math import pi, sin, sqrt

# Third party modules.

# Local modules.
import EBSDTools.crystallography.reflectors as reflectors
import EBSDTools.crystallography.lattice as lattice
from RandomUtilities.testing.testOthers import almostEqual

# Globals and constants variables.

warnings.filterwarnings('ignore', category=UserWarning)

class TestReciprocal(unittest.TestCase):

  def setUp(self):
    unittest.TestCase.setUp(self)
    
    self.Lbcc = lattice.Lattice(a=2.87
                                , b=2.87
                                , c=2.87
                                , alpha=pi/2
                                , beta=pi/2
                                , gamma=pi/2
                                , atoms = {(0,0,0): 26, (0.5,0.5,0.5): 26}
                                , reflectorsMaxIndice=2)
    self.Lfcc = lattice.Lattice(a=5.43
                                , b=5.43
                                , c=5.43
                                , alpha=pi/2
                                , beta=pi/2
                                , gamma=pi/2
                                , atoms = {(0,0,0): 14, (0.5,0.5,0): 14, (0.5,0,0.5): 14, (0,0.5,0.5): 14}
                                , reflectorsMaxIndice=2)
    self.Lhcp = lattice.Lattice(a=3.21
                                , b=3.21
                                , c=5.21
                                , alpha=pi/2
                                , beta=pi/2
                                , gamma=120.0/180*pi
                                , atoms = {(0,0,0): 13, (1/3.0, 2/3.0, 0.5): 13}
                                , reflectorsMaxIndice=2)
    
  def tearDown(self):
    unittest.TestCase.tearDown(self)

  def testSkeleton(self):
#    self.fail("Test if the testcase is working.")
    self.assert_(True)
  
  def testScatteringFactors(self):
    scatterF = reflectors.scatteringFactors()
    
    self.assert_(almostEqual(scatterF.getScatteringFactor(14, 0.5), 0.742519788187))
    self.assert_(almostEqual(scatterF.getScatteringFactor(14, 3), 0.0349033998305))
    self.assert_(almostEqual(scatterF.getScatteringFactor(14, 6.1), 0.00650227565622))
    
    self.assert_(almostEqual(scatterF.getScatteringFactor(29, 0.5), 1.46390369208))
    self.assert_(almostEqual(scatterF.getScatteringFactor(29, 3), 0.0652299842623))
    self.assert_(almostEqual(scatterF.getScatteringFactor(29, 6.1), 0.000336590516491))
    
    self.assert_(almostEqual(scatterF.getScatteringFactor(79, 0.5), 3.07239344718))
    self.assert_(almostEqual(scatterF.getScatteringFactor(79, 3), 0.186031146844))
    self.assert_(almostEqual(scatterF.getScatteringFactor(79, 6.1), 0.0332559532))
  
  def testGetReflectorsDict(self):
#    bcc
    planesBCC = self.Lbcc.getReflectors()
    self.assertEqual(planesBCC.getReflectorsDict(), planesBCC.reflectors)
    
    #fcc
    planesFCC = self.Lfcc.getReflectors()
    self.assertEqual(planesFCC.getReflectorsDict(), planesFCC.reflectors)
    
    #hcp
    planesHCP = self.Lhcp.getReflectors()
    self.assertEqual(planesHCP.getReflectorsDict(), planesHCP.reflectors)
  
  def testGetReflectorsList(self):
    #bcc
    planesBCC = self.Lbcc.getReflectors().getReflectorsList()
    planesBCC_ = [(0, 1, 1), (1, 1, 0), (1, 0, 1), (1, -1, 0), (1, 0, -1), (0, 1, -1)]
    
    for plane in planesBCC_:
      self.assert_(plane in planesBCC)
      self.assertEqual((plane[0] + plane[1] + plane[2]) % 2, 0)
    
    planesBCC = self.Lbcc.getReflectors().getReflectorsList()
    planesBCC_ = [(1, 0, 1), (1, 1, 0), (1, 0, -1), (1, -1, 0), (0, 2, 0), (2, 0, 0), (0, 0, 2), (1, 1, 2), (1, 2, 1), (2, 1, 1), (1, -2, -1), (2, 1, -1), (2, -1, -1), (1, 1, -2), (1, -1, -2), (1, 2, -1), (2, -1, 1), (1, -2, 1), (1, -1, 2), (0, 2, 2), (2, 0, 2), (2, 2, 0), (2, -2, 0), (2, 0, -2), (0, 2, -2), (2, 2,2), (2, -2, -2), (2, -2, 2), (2, 2, -2)]
    
    for plane in planesBCC_:
      self.assert_(plane in planesBCC)
      self.assertEqual((plane[0] + plane[1] + plane[2]) % 2, 0)
    
    #fcc
    planesFCC = self.Lfcc.getReflectors().getReflectorsList()
    planesFCC_ = [(1, 1, 1), (1, -1, -1), (1, 1, -1), (1, -1, 1)]
    
    for plane in planesFCC_:
      self.assert_(plane in planesFCC)
      if plane[0] % 2 == 0: 
        self.assertEqual(plane[1] % 2, 0)
        self.assertEqual(plane[2] % 2, 0)
      else: # plane[0] % 2 == 1
        self.assertEqual(plane[1] % 2, 1)
        self.assertEqual(plane[2] % 2, 1)
    
    planesFCC = self.Lfcc.getReflectors().getReflectorsList()
    planesFCC_ = [(1, 1, 1), (1, -1, -1), (1, 1, -1), (1, -1, 1), (0, 2, 0), (0, 0, 2), (2, 0, 0), (0, 2, 2), (2, 0, 2), (2, 2, 0), (0, 2, -2), (2, 0, -2), (2, -2, 0), (2, 2, 2), (2, -2, 2), (2, -2, -2), (2, 2, -2)]
    
    for plane in planesFCC_:
      self.assert_(plane in planesFCC)
      if plane[0] % 2 == 0: 
        self.assertEqual(plane[1] % 2, 0)
        self.assertEqual(plane[2] % 2, 0)
      else: # plane[0] % 2 == 1
        self.assertEqual(plane[1] % 2, 1)
        self.assertEqual(plane[2] % 2, 1)
    
#    hcp
    planesHCP = self.Lhcp.getReflectors().getReflectorsList()
    for plane in planesHCP:
      #From Rollett 2008
      condition1 = (plane[0] + 2*plane[1]) % 3 < 0
      condition2 = plane[2] % 2 == 1
      self.assertNotEqual(condition1 and condition2, True)
  
  def testGetReflectorInfo(self):
    #bcc
    planesBCC = self.Lbcc.getReflectors().getReflectorInfo((1,0,1))
    self.assertEqual(len(planesBCC), 5)
    self.assertEqual(planesBCC['normalized intensity'], 1.0)
    self.assert_(almostEqual(planesBCC['plane spacing'], 2.029396))
    self.assertEqual(planesBCC['family'], 0)
    
    planesFCC = self.Lfcc.getReflectors().getReflectorInfo((1,1,1))
    self.assertEqual(len(planesFCC), 5)
    self.assertEqual(planesFCC['normalized intensity'], 1.0)
    self.assert_(almostEqual(planesFCC['plane spacing'], 3.13501196))
    self.assertEqual(planesFCC['family'], 0)
    
    planesHCP = self.Lhcp.getReflectors().getReflectorInfo((1,0,-1))
    self.assertEqual(len(planesHCP), 5)
    self.assert_(almostEqual(planesHCP['normalized intensity'], 0.61380371))
    self.assert_(almostEqual(planesHCP['plane spacing'], 2.4526403))
    self.assertEqual(planesHCP['family'], 2)
#  
  def testGetReflectorPlaneSpacing(self):
    #Compared with HKL Channel 5 Phases Database
    
    #bcc
    planesBCC = self.Lbcc.getReflectors()
    self.assert_(almostEqual(planesBCC.getReflectorPlaneSpacing((1,0,1)), 2.0293964620053915))
    self.assert_(almostEqual(planesBCC.getReflectorPlaneSpacing((1,-1,0)), 2.0293964620053915))
    self.assert_(almostEqual(planesBCC.getReflectorPlaneSpacing((2,0,0)), 1.4349999999999998))
    self.assert_(almostEqual(planesBCC.getReflectorPlaneSpacing((1,-1,2)), 1.1716725936312868))
    self.assert_(almostEqual(planesBCC.getReflectorPlaneSpacing((2,0,2)), 1.0146982310026957))
    
    #fcc
    planesFCC = self.Lfcc.getReflectors()
    self.assert_(almostEqual(planesFCC.getReflectorPlaneSpacing((1,1,1)), 3.1350119616996683))
    self.assert_(almostEqual(planesFCC.getReflectorPlaneSpacing((1,-1,1)), 3.1350119616996683))
    self.assert_(almostEqual(planesFCC.getReflectorPlaneSpacing((2,-2,0)), 1.919794910921476))

    #hcp
    planesHCP = self.Lhcp.getReflectors()
    self.assert_(almostEqual(planesHCP.getReflectorPlaneSpacing((0,0,2)), 2.6050000000000004))
    self.assert_(almostEqual(planesHCP.getReflectorPlaneSpacing((1,0,-1)), 2.4526403546701228))
    self.assert_(almostEqual(planesHCP.getReflectorPlaneSpacing((2,-1,0)), 1.6050000000000002))
  
  def testGetReflectorIntensity(self):
    #bcc
    planesBCC = self.Lbcc.getReflectors()
    self.assert_(almostEqual(planesBCC.getReflectorIntensity((1,0,1)), 0.018535906894))
    self.assert_(almostEqual(planesBCC.getReflectorIntensity((1,-1,0)), 0.018535906894))
    self.assert_(almostEqual(planesBCC.getReflectorIntensity((2,0,0)), 0.00230481501653))
    
    #fcc
    planesFCC = self.Lfcc.getReflectors()
    self.assert_(almostEqual(planesFCC.getReflectorIntensity((1,1,1)), 0.0859145669508))
    self.assert_(almostEqual(planesFCC.getReflectorIntensity((1,-1,1)), 0.0859145669508))
    self.assert_(almostEqual(planesFCC.getReflectorIntensity((2,-2,0)), 0.0152361124413))
    
    #hcp
    planesHCP = self.Lhcp.getReflectors()
    self.assert_(almostEqual(planesHCP.getReflectorIntensity((0,0,2)), 0.0121889606511))
    self.assert_(almostEqual(planesHCP.getReflectorIntensity((1,0,-1)), 0.00748162928987))
    self.assert_(almostEqual(planesHCP.getReflectorIntensity((2,-1,0)), 0.00102537971942))
    
  def testGetReflectorNormalizedIntensity(self):
    #bcc
    planesBCC = self.Lbcc.getReflectors()
    self.assert_(almostEqual(planesBCC.getReflectorNormalizedIntensity((1,0,1)), 1.0))
    self.assert_(almostEqual(planesBCC.getReflectorNormalizedIntensity((1,-1,0)), 1.0))
    self.assert_(almostEqual(planesBCC.getReflectorNormalizedIntensity((2,0,0)), 0.124343256023))
    
    #fcc
    planesFCC = self.Lfcc.getReflectors()
    self.assert_(almostEqual(planesFCC.getReflectorNormalizedIntensity((1,1,1)), 1.0))
    self.assert_(almostEqual(planesFCC.getReflectorNormalizedIntensity((1,-1,1)), 1.0))
    self.assert_(almostEqual(planesFCC.getReflectorNormalizedIntensity((2,-2,0)), 0.177340269316))
    
    #hcp
    planesHCP = self.Lhcp.getReflectors()
    self.assert_(almostEqual(planesHCP.getReflectorNormalizedIntensity((0,0,2)), 1.0))
    self.assert_(almostEqual(planesHCP.getReflectorNormalizedIntensity((1,0,-1)), 0.613803711737))
    self.assert_(almostEqual(planesHCP.getReflectorNormalizedIntensity((2,-1,0)), 0.0841236384928))
  
if __name__ == '__main__':
  unittest.main()