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
from math import pi, sin, cos, sqrt

# Third party modules.

# Local modules.
import reciprocal
import mathTools.vectors as vectors

# Globals and constants variables.

class TestReciprocal(unittest.TestCase):

  def setUp(self):
    unittest.TestCase.setUp(self)
    
    self.Lcubic = reciprocal.lattice(a=2, b=2, c=2, alpha=pi/2, beta=pi/2, gamma=pi/2)
    self.Ltetragonal = reciprocal.lattice(a=2, b=2, c=3, alpha=pi/2, beta=pi/2, gamma=pi/2)
    self.Lorthorhombic = reciprocal.lattice(a=1, b=2, c=3, alpha=pi/2, beta=pi/2, gamma=pi/2)
    self.Lrhombohedral = reciprocal.lattice(a=2, b=2, c=2, alpha=35.0/180*pi, beta=35.0/180*pi, gamma=35.0/180*pi)
    self.Lhexagonal = reciprocal.lattice(a=2, b=2, c=3, alpha=pi/2, beta=pi/2, gamma=120.0/180*pi)
    self.Lmonoclinic = reciprocal.lattice(a=1, b=2, c=3, alpha=pi/2, beta=55.0/180*pi, gamma=pi/2)
    self.Ltriclinic = reciprocal.lattice(a=1, b=2, c=3, alpha=75.0/180*pi, beta=55.0/180*pi, gamma=35.0/180*pi)

  def tearDown(self):
    unittest.TestCase.tearDown(self)

  def testSkeleton(self):
#    self.fail("Test if the testcase is working.")
    self.assert_(True)
  
  def testLattice(self):
    #cubic
    self.assertAlmostEqual(self.Lcubic.a, 2.0, 3)
    self.assertAlmostEqual(self.Lcubic.b, 2.0, 3)
    self.assertAlmostEqual(self.Lcubic.c, 2.0, 3)
    self.assertAlmostEqual(self.Lcubic.a_, 0.5, 3)
    self.assertAlmostEqual(self.Lcubic.b_, 0.5, 3)
    self.assertAlmostEqual(self.Lcubic.c_, 0.5, 3)
    self.assertAlmostEqual(self.Lcubic.alpha, pi/2, 3)
    self.assertAlmostEqual(self.Lcubic.beta, pi/2, 3)
    self.assertAlmostEqual(self.Lcubic.gamma, pi/2, 3)
    self.assertAlmostEqual(self.Lcubic.alpha_, pi/2, 3)
    self.assertAlmostEqual(self.Lcubic.beta_, pi/2, 3)
    self.assertAlmostEqual(self.Lcubic.gamma_, pi/2, 3)
    self.assertAlmostEqual(self.Lcubic.volume, 8.0, 3)
    self.assertAlmostEqual(self.Lcubic.volume_, 0.125, 3)
    
    self.assertAlmostEqual(self.Lcubic.a_, 1.0/2.0, 3)
    self.assertAlmostEqual(self.Lcubic.b_, 1.0/2.0, 3)
    self.assertAlmostEqual(self.Lcubic.c_, 1.0/2.0, 3)
    self.assertAlmostEqual(self.Lcubic.volume, 2.0**3, 3)
    
    #tetragonal
    self.assertAlmostEqual(self.Ltetragonal.a, 2.0, 3)
    self.assertAlmostEqual(self.Ltetragonal.b, 2.0, 3)
    self.assertAlmostEqual(self.Ltetragonal.c, 3.0, 3)
    self.assertAlmostEqual(self.Ltetragonal.a_, 0.5, 3)
    self.assertAlmostEqual(self.Ltetragonal.b_, 0.5, 3)
    self.assertAlmostEqual(self.Ltetragonal.c_, 0.3333, 3)
    self.assertAlmostEqual(self.Ltetragonal.alpha, pi/2, 3)
    self.assertAlmostEqual(self.Ltetragonal.beta, pi/2, 3)
    self.assertAlmostEqual(self.Ltetragonal.gamma, pi/2, 3)
    self.assertAlmostEqual(self.Ltetragonal.alpha_, pi/2, 3)
    self.assertAlmostEqual(self.Ltetragonal.beta_, pi/2, 3)
    self.assertAlmostEqual(self.Ltetragonal.gamma_, pi/2, 3)
    self.assertAlmostEqual(self.Ltetragonal.volume, 12.0, 3)
    self.assertAlmostEqual(self.Ltetragonal.volume_, 0.0833, 3)
    
    self.assertAlmostEqual(self.Ltetragonal.a_, 1.0/2.0, 3)
    self.assertAlmostEqual(self.Ltetragonal.b_, 1.0/2.0, 3)
    self.assertAlmostEqual(self.Ltetragonal.c_, 1.0/3.0, 3)
    self.assertAlmostEqual(self.Ltetragonal.volume, 2.0**2*3.0, 3)
    
    #orthorhombic
    self.assertAlmostEqual(self.Lorthorhombic.a, 1.0, 3)
    self.assertAlmostEqual(self.Lorthorhombic.b, 2.0, 3)
    self.assertAlmostEqual(self.Lorthorhombic.c, 3.0, 3)
    self.assertAlmostEqual(self.Lorthorhombic.a_, 1.0, 3)
    self.assertAlmostEqual(self.Lorthorhombic.b_, 0.5, 3)
    self.assertAlmostEqual(self.Lorthorhombic.c_, 0.3333, 3)
    self.assertAlmostEqual(self.Lorthorhombic.alpha, pi/2, 3)
    self.assertAlmostEqual(self.Lorthorhombic.beta, pi/2, 3)
    self.assertAlmostEqual(self.Lorthorhombic.gamma, pi/2, 3)
    self.assertAlmostEqual(self.Lorthorhombic.alpha_, pi/2, 3)
    self.assertAlmostEqual(self.Lorthorhombic.beta_, pi/2, 3)
    self.assertAlmostEqual(self.Lorthorhombic.gamma_, pi/2, 3)
    self.assertAlmostEqual(self.Lorthorhombic.volume, 6.0, 3)
    self.assertAlmostEqual(self.Lorthorhombic.volume_, 0.1666, 3)
    
    self.assertAlmostEqual(self.Lorthorhombic.a_, 1.0/1.0, 3)
    self.assertAlmostEqual(self.Lorthorhombic.b_, 1.0/2.0, 3)
    self.assertAlmostEqual(self.Lorthorhombic.c_, 1.0/3.0, 3)
    self.assertAlmostEqual(self.Lorthorhombic.volume, 1.0*2.0*3.0, 3)
    
    #rhombohedral
    self.assertAlmostEqual(self.Lrhombohedral.a, 2.0, 3)
    self.assertAlmostEqual(self.Lrhombohedral.b, 2.0, 3)
    self.assertAlmostEqual(self.Lrhombohedral.c, 2.0, 3)
    self.assertAlmostEqual(self.Lrhombohedral.a_, 0.9763, 3)
    self.assertAlmostEqual(self.Lrhombohedral.b_, 0.9763, 3)
    self.assertAlmostEqual(self.Lrhombohedral.c_, 0.9763, 3)
    self.assertAlmostEqual(self.Lrhombohedral.alpha, 35.0/180*pi, 3)
    self.assertAlmostEqual(self.Lrhombohedral.beta, 35.0/180*pi, 3)
    self.assertAlmostEqual(self.Lrhombohedral.gamma, 35.0/180*pi, 3)
    self.assertAlmostEqual(self.Lrhombohedral.alpha_, 2.0378, 3)
    self.assertAlmostEqual(self.Lrhombohedral.beta_, 2.0378, 3)
    self.assertAlmostEqual(self.Lrhombohedral.gamma_, 2.0378, 3)
    self.assertAlmostEqual(self.Lrhombohedral.volume, 2.3499, 3)
    self.assertAlmostEqual(self.Lrhombohedral.volume_, 0.4255, 3)
    
    #hexagonal
    self.assertAlmostEqual(self.Lhexagonal.a, 2.0, 3)
    self.assertAlmostEqual(self.Lhexagonal.b, 2.0, 3)
    self.assertAlmostEqual(self.Lhexagonal.c, 3.0, 3)
    self.assertAlmostEqual(self.Lhexagonal.a_, 0.5773, 3)
    self.assertAlmostEqual(self.Lhexagonal.b_, 0.5773, 3)
    self.assertAlmostEqual(self.Lhexagonal.c_, 0.3333, 3)
    self.assertAlmostEqual(self.Lhexagonal.alpha, pi/2, 3)
    self.assertAlmostEqual(self.Lhexagonal.beta, pi/2, 3)
    self.assertAlmostEqual(self.Lhexagonal.gamma, 120.0/180*pi, 3)
    self.assertAlmostEqual(self.Lhexagonal.alpha_, pi/2, 3)
    self.assertAlmostEqual(self.Lhexagonal.beta_, pi/2, 3)
    self.assertAlmostEqual(self.Lhexagonal.gamma_, 60.0/180*pi, 3)
    self.assertAlmostEqual(self.Lhexagonal.volume, 10.3923, 3)
    self.assertAlmostEqual(self.Lhexagonal.volume_, 0.0962, 3)
    
    self.assertAlmostEqual(self.Lhexagonal.a_, 2.0/3.0*sqrt(3)/2.0, 3)
    self.assertAlmostEqual(self.Lhexagonal.b_, 2.0/3.0*sqrt(3)/2.0, 3)
    self.assertAlmostEqual(self.Lhexagonal.c_, 1.0/3.0, 3)
    self.assertAlmostEqual(self.Lhexagonal.volume, 0.5*sqrt(3)*2.0**2*3.0, 3)
    
    #monoclinic
    self.assertAlmostEqual(self.Lmonoclinic.a, 1.0, 3)
    self.assertAlmostEqual(self.Lmonoclinic.b, 2.0, 3)
    self.assertAlmostEqual(self.Lmonoclinic.c, 3.0, 3)
    self.assertAlmostEqual(self.Lmonoclinic.a_, 1.2207, 3)
    self.assertAlmostEqual(self.Lmonoclinic.b_, 0.5, 3)
    self.assertAlmostEqual(self.Lmonoclinic.c_, 0.4069, 3)
    self.assertAlmostEqual(self.Lmonoclinic.alpha, pi/2, 3)
    self.assertAlmostEqual(self.Lmonoclinic.beta, 55.0/180*pi, 3)
    self.assertAlmostEqual(self.Lmonoclinic.gamma, pi/2, 3)
    self.assertAlmostEqual(self.Lmonoclinic.alpha_, pi/2, 3)
    self.assertAlmostEqual(self.Lmonoclinic.beta_, 125.0/180*pi, 3)
    self.assertAlmostEqual(self.Lmonoclinic.gamma_, pi/2, 3)
    self.assertAlmostEqual(self.Lmonoclinic.volume, 4.9149, 3)
    self.assertAlmostEqual(self.Lmonoclinic.volume_, 0.2034, 3)
    
    self.assertAlmostEqual(self.Lmonoclinic.a_, 1.0/(1*sin(125.0/180*pi)), 3)
    self.assertAlmostEqual(self.Lmonoclinic.b_, 1.0/2.0, 3)
    self.assertAlmostEqual(self.Lmonoclinic.c_, 1.0/(3*sin(125.0/180*pi)), 3)
    self.assertAlmostEqual(self.Lmonoclinic.volume, 1.0*2.0*3.0*sin(125.0/180*pi), 3)
    
    #triclinic
    self.assertAlmostEqual(self.Ltriclinic.a, 1.0, 3)
    self.assertAlmostEqual(self.Ltriclinic.b, 2.0, 3)
    self.assertAlmostEqual(self.Ltriclinic.c, 3.0, 3)
    self.assertAlmostEqual(self.Ltriclinic.a_, 2.3009, 3)
    self.assertAlmostEqual(self.Ltriclinic.b_, 0.9756, 3)
    self.assertAlmostEqual(self.Ltriclinic.c_, 0.4554, 3)
    self.assertAlmostEqual(self.Ltriclinic.alpha, 75.0/180*pi, 3)
    self.assertAlmostEqual(self.Ltriclinic.beta, 55.0/180*pi, 3)
    self.assertAlmostEqual(self.Ltriclinic.gamma, 35.0/180*pi, 3)
    self.assertAlmostEqual(self.Ltriclinic.alpha_, 1.1049, 3)
    self.assertAlmostEqual(self.Ltriclinic.beta_, 2.2818, 3)
    self.assertAlmostEqual(self.Ltriclinic.gamma_, 2.5823, 3)
    self.assertAlmostEqual(self.Ltriclinic.volume, 2.5187, 3)
    self.assertAlmostEqual(self.Ltriclinic.volume_, 0.3970, 3)
  
  def testPlaneSpacing(self):
    planes = []
    
    #cubic
    for plane in planes:
      d2_1 = (plane[0]**2 + plane[1]**2 + plane[2]**2) / self.Lcubic.a**2 
      print reciprocal.planeSpacing(plane, self.Lcubic)


if __name__ == '__main__':
  logging.getLogger().setLevel(logging.DEBUG)
  unittest.main()