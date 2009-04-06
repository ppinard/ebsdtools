#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Philippe Pinard (philippe.pinard@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2008-2009 Philippe Pinard"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = "$Revision$"
__svnDate__ = "$Date$"
__svnId__ = "$Id$"

# Standard library modules.
import unittest
import warnings
from math import pi, sqrt, sin

# Third party modules.

# Local modules.
import EBSDTools.crystallography.lattice as lattice
from RandomUtilities.testing.testOthers import almostEqual

# Globals and constants variables.

warnings.filterwarnings('ignore', category=UserWarning)

class TestLattice(unittest.TestCase):
  def setUp(self):
    unittest.TestCase.setUp(self)
    
    self.Lcubic = lattice.Lattice(a=2, b=2, c=2, alpha=pi/2, beta=pi/2, gamma=pi/2)
    self.Ltetragonal = lattice.Lattice(a=2, b=2, c=3, alpha=pi/2, beta=pi/2, gamma=pi/2)
    self.Lorthorhombic = lattice.Lattice(a=1, b=2, c=3, alpha=pi/2, beta=pi/2, gamma=pi/2)
    self.Lrhombohedral = lattice.Lattice(a=2, b=2, c=2, alpha=35.0/180*pi, beta=35.0/180*pi, gamma=35.0/180*pi)
    self.Lhexagonal = lattice.Lattice(a=2, b=2, c=3, alpha=pi/2, beta=pi/2, gamma=120.0/180*pi)
    self.Lmonoclinic = lattice.Lattice(a=1, b=2, c=3, alpha=pi/2, beta=55.0/180*pi, gamma=pi/2)
    self.Ltriclinic = lattice.Lattice(a=1, b=2, c=3, alpha=75.0/180*pi, beta=55.0/180*pi, gamma=35.0/180*pi)

  def tearDown(self):
    unittest.TestCase.tearDown(self)

  def testSkeleton(self):
#    self.fail("Test if the testcase is working.")
    self.assert_(True)
  
  def testLattice(self):
    #cubic
    self.assert_(almostEqual(self.Lcubic.a, 2.0))
    self.assert_(almostEqual(self.Lcubic.b, 2.0))
    self.assert_(almostEqual(self.Lcubic.c, 2.0))
    self.assert_(almostEqual(self.Lcubic.a_, 0.5))
    self.assert_(almostEqual(self.Lcubic.b_, 0.5))
    self.assert_(almostEqual(self.Lcubic.c_, 0.5))
    self.assert_(almostEqual(self.Lcubic.alpha, pi/2))
    self.assert_(almostEqual(self.Lcubic.beta, pi/2))
    self.assert_(almostEqual(self.Lcubic.gamma, pi/2))
    self.assert_(almostEqual(self.Lcubic.alpha_, pi/2))
    self.assert_(almostEqual(self.Lcubic.beta_, pi/2))
    self.assert_(almostEqual(self.Lcubic.gamma_, pi/2))
    self.assert_(almostEqual(self.Lcubic.volume, 8.0))
    self.assert_(almostEqual(self.Lcubic.volume_, 0.125))
    
    self.assert_(almostEqual(self.Lcubic.a_, 1.0/2.0))
    self.assert_(almostEqual(self.Lcubic.b_, 1.0/2.0))
    self.assert_(almostEqual(self.Lcubic.c_, 1.0/2.0))
    self.assert_(almostEqual(self.Lcubic.volume, 2.0**3))
    
    #tetragonal
    self.assert_(almostEqual(self.Ltetragonal.a, 2.0))
    self.assert_(almostEqual(self.Ltetragonal.b, 2.0))
    self.assert_(almostEqual(self.Ltetragonal.c, 3.0))
    self.assert_(almostEqual(self.Ltetragonal.a_, 0.5))
    self.assert_(almostEqual(self.Ltetragonal.b_, 0.5))
    self.assert_(almostEqual(self.Ltetragonal.c_, 0.333333))
    self.assert_(almostEqual(self.Ltetragonal.alpha, pi/2))
    self.assert_(almostEqual(self.Ltetragonal.beta, pi/2))
    self.assert_(almostEqual(self.Ltetragonal.gamma, pi/2))
    self.assert_(almostEqual(self.Ltetragonal.alpha_, pi/2))
    self.assert_(almostEqual(self.Ltetragonal.beta_, pi/2))
    self.assert_(almostEqual(self.Ltetragonal.gamma_, pi/2))
    self.assert_(almostEqual(self.Ltetragonal.volume, 12.0))
    self.assert_(almostEqual(self.Ltetragonal.volume_, 0.083333))
    
    self.assert_(almostEqual(self.Ltetragonal.a_, 1.0/2.0))
    self.assert_(almostEqual(self.Ltetragonal.b_, 1.0/2.0))
    self.assert_(almostEqual(self.Ltetragonal.c_, 1.0/3.0))
    self.assert_(almostEqual(self.Ltetragonal.volume, 2.0**2*3.0))
    
    #orthorhombic
    self.assert_(almostEqual(self.Lorthorhombic.a, 1.0))
    self.assert_(almostEqual(self.Lorthorhombic.b, 2.0))
    self.assert_(almostEqual(self.Lorthorhombic.c, 3.0))
    self.assert_(almostEqual(self.Lorthorhombic.a_, 1.0))
    self.assert_(almostEqual(self.Lorthorhombic.b_, 0.5))
    self.assert_(almostEqual(self.Lorthorhombic.c_, 0.333333))
    self.assert_(almostEqual(self.Lorthorhombic.alpha, pi/2))
    self.assert_(almostEqual(self.Lorthorhombic.beta, pi/2))
    self.assert_(almostEqual(self.Lorthorhombic.gamma, pi/2))
    self.assert_(almostEqual(self.Lorthorhombic.alpha_, pi/2))
    self.assert_(almostEqual(self.Lorthorhombic.beta_, pi/2))
    self.assert_(almostEqual(self.Lorthorhombic.gamma_, pi/2))
    self.assert_(almostEqual(self.Lorthorhombic.volume, 6.0))
    self.assert_(almostEqual(self.Lorthorhombic.volume_, 0.166666))
    
    self.assert_(almostEqual(self.Lorthorhombic.a_, 1.0/1.0))
    self.assert_(almostEqual(self.Lorthorhombic.b_, 1.0/2.0))
    self.assert_(almostEqual(self.Lorthorhombic.c_, 1.0/3.0))
    self.assert_(almostEqual(self.Lorthorhombic.volume, 1.0*2.0*3.0))
    
    #rhombohedral
    self.assert_(almostEqual(self.Lrhombohedral.a, 2.0))
    self.assert_(almostEqual(self.Lrhombohedral.b, 2.0))
    self.assert_(almostEqual(self.Lrhombohedral.c, 2.0))
    self.assert_(almostEqual(self.Lrhombohedral.a_, 0.9763044673403796))
    self.assert_(almostEqual(self.Lrhombohedral.b_, 0.9763044673403796))
    self.assert_(almostEqual(self.Lrhombohedral.c_, 0.9763044673403796))
    self.assert_(almostEqual(self.Lrhombohedral.alpha, 35.0/180*pi))
    self.assert_(almostEqual(self.Lrhombohedral.beta, 35.0/180*pi))
    self.assert_(almostEqual(self.Lrhombohedral.gamma, 35.0/180*pi))
    self.assert_(almostEqual(self.Lrhombohedral.alpha_, 2.0378901672656156))
    self.assert_(almostEqual(self.Lrhombohedral.beta_, 2.0378901672656156))
    self.assert_(almostEqual(self.Lrhombohedral.gamma_, 2.0378901672656156))
    self.assert_(almostEqual(self.Lrhombohedral.volume, 2.349990010446501))
    self.assert_(almostEqual(self.Lrhombohedral.volume_, 0.42553372378378695))
    
    #hexagonal
    self.assert_(almostEqual(self.Lhexagonal.a, 2.0))
    self.assert_(almostEqual(self.Lhexagonal.b, 2.0))
    self.assert_(almostEqual(self.Lhexagonal.c, 3.0))
    self.assert_(almostEqual(self.Lhexagonal.a_, 0.5773502691896257))
    self.assert_(almostEqual(self.Lhexagonal.b_, 0.5773502691896257))
    self.assert_(almostEqual(self.Lhexagonal.c_, 0.333333))
    self.assert_(almostEqual(self.Lhexagonal.alpha, pi/2))
    self.assert_(almostEqual(self.Lhexagonal.beta, pi/2))
    self.assert_(almostEqual(self.Lhexagonal.gamma, 120.0/180*pi))
    self.assert_(almostEqual(self.Lhexagonal.alpha_, pi/2))
    self.assert_(almostEqual(self.Lhexagonal.beta_, pi/2))
    self.assert_(almostEqual(self.Lhexagonal.gamma_, 60.0/180*pi))
    self.assert_(almostEqual(self.Lhexagonal.volume, 10.392304845413264))
    self.assert_(almostEqual(self.Lhexagonal.volume_, 0.09622504486493763))
    
    self.assert_(almostEqual(self.Lhexagonal.a_, 2.0/3.0*sqrt(3)/2.0))
    self.assert_(almostEqual(self.Lhexagonal.b_, 2.0/3.0*sqrt(3)/2.0))
    self.assert_(almostEqual(self.Lhexagonal.c_, 1.0/3.0))
    self.assert_(almostEqual(self.Lhexagonal.volume, 0.5*sqrt(3)*2.0**2*3.0))
    
    #monoclinic
    self.assert_(almostEqual(self.Lmonoclinic.a, 1.0))
    self.assert_(almostEqual(self.Lmonoclinic.b, 2.0))
    self.assert_(almostEqual(self.Lmonoclinic.c, 3.0))
    self.assert_(almostEqual(self.Lmonoclinic.a_, 1.220774588761456))
    self.assert_(almostEqual(self.Lmonoclinic.b_, 0.5))
    self.assert_(almostEqual(self.Lmonoclinic.c_, 0.40692486292048535))
    self.assert_(almostEqual(self.Lmonoclinic.alpha, pi/2))
    self.assert_(almostEqual(self.Lmonoclinic.beta, 55.0/180*pi))
    self.assert_(almostEqual(self.Lmonoclinic.gamma, pi/2))
    self.assert_(almostEqual(self.Lmonoclinic.alpha_, pi/2))
    self.assert_(almostEqual(self.Lmonoclinic.beta_, 125.0/180*pi))
    self.assert_(almostEqual(self.Lmonoclinic.gamma_, pi/2))
    self.assert_(almostEqual(self.Lmonoclinic.volume, 4.914912265733951))
    self.assert_(almostEqual(self.Lmonoclinic.volume_, 0.20346243146024268))
    
    self.assert_(almostEqual(self.Lmonoclinic.a_, 1.0/(1*sin(125.0/180*pi))))
    self.assert_(almostEqual(self.Lmonoclinic.b_, 1.0/2.0))
    self.assert_(almostEqual(self.Lmonoclinic.c_, 1.0/(3*sin(125.0/180*pi))))
    self.assert_(almostEqual(self.Lmonoclinic.volume, 1.0*2.0*3.0*sin(125.0/180*pi)))
    
    #triclinic
    self.assert_(almostEqual(self.Ltriclinic.a, 1.0))
    self.assert_(almostEqual(self.Ltriclinic.b, 2.0))
    self.assert_(almostEqual(self.Ltriclinic.c, 3.0))
    self.assert_(almostEqual(self.Ltriclinic.a_, 2.3009777700230383))
    self.assert_(almostEqual(self.Ltriclinic.b_, 0.9756704877739889))
    self.assert_(almostEqual(self.Ltriclinic.c_, 0.45544788689872767))
    self.assert_(almostEqual(self.Ltriclinic.alpha, 75.0/180*pi))
    self.assert_(almostEqual(self.Ltriclinic.beta, 55.0/180*pi))
    self.assert_(almostEqual(self.Ltriclinic.gamma, 35.0/180*pi))
    self.assert_(almostEqual(self.Ltriclinic.alpha_, 1.1049925940211875))
    self.assert_(almostEqual(self.Ltriclinic.beta_, 2.281813838221562))
    self.assert_(almostEqual(self.Ltriclinic.gamma_, 2.582348070021294))
    self.assert_(almostEqual(self.Ltriclinic.volume, 2.518735744968272))
    self.assert_(almostEqual(self.Ltriclinic.volume_, 0.3970245794929935))

  def testGetReflectors(self):
    #Reflectors tested in test_reflectors.py
    pass
    
  def testGetAtomsPositions(self):
    atoms = {(0,0,0): 14,
           (0.5,0.5,0): 14,
           (0.5,0,0.5): 14,
           (0,0.5,0.5): 14}
    
    L1 = lattice.Lattice(a=1, b=1, c=1, alpha=pi/2.0, beta=pi/2.0, gamma=pi/2.0, atoms=atoms)
    
    atomsPositions = L1.getAtomsPositions()
    for atomsPosition in atomsPositions:
      self.assert_(atomsPosition in atoms.keys())
  
if __name__ == '__main__':
  unittest.main()