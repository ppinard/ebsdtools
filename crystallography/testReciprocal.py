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
import lattice
from mathTools.mathExtras import _acos

# Globals and constants variables.

class TestReciprocal(unittest.TestCase):

  def setUp(self):
    unittest.TestCase.setUp(self)
    
    self.Lcubic = lattice.Lattice(a=2, b=2, c=2, alpha=pi/2, beta=pi/2, gamma=pi/2)
    self.Ltetragonal = lattice.Lattice(a=2, b=2, c=3, alpha=pi/2, beta=pi/2, gamma=pi/2)
    self.Lorthorhombic = lattice.Lattice(a=1, b=2, c=3, alpha=pi/2, beta=pi/2, gamma=pi/2)
    self.Lrhombohedral = lattice.Lattice(a=2, b=2, c=2, alpha=35.0/180*pi, beta=35.0/180*pi, gamma=35.0/180*pi)
    self.Lhexagonal = lattice.Lattice(a=2, b=2, c=3, alpha=pi/2, beta=pi/2, gamma=120.0/180*pi)
    self.Lmonoclinic = lattice.Lattice(a=1, b=2, c=3, alpha=pi/2, beta=55.0/180*pi, gamma=pi/2)
    self.Ltriclinic = lattice.Lattice(a=1, b=2, c=3, alpha=75.0/180*pi, beta=55.0/180*pi, gamma=35.0/180*pi)
    
    self.planes = [vectors.vector(1,0,0),
                   vectors.vector(1,1,0),
                   vectors.vector(1,1,1),
                   vectors.vector(2,0,2),
                   vectors.vector(1,2,3),
                   vectors.vector(4,5,6),
                   vectors.vector(0,9,2)]

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
    for plane in self.planes:
      h = plane[0]
      k = plane[1]
      l = plane[2]
      
      #cubic
      d2_1 = (plane[0]**2 + plane[1]**2 + plane[2]**2) / self.Lcubic.a**2 
      self.assertAlmostEqual(reciprocal.planeSpacing(plane, self.Lcubic), 1.0/sqrt(d2_1), 3)
    
      #tetragonal
      d2_1 = (plane[0]**2 + plane[1]**2) / self.Ltetragonal.a**2 + plane[2]**2 / self.Ltetragonal.c**2 
      self.assertAlmostEqual(reciprocal.planeSpacing(plane, self.Ltetragonal), 1.0/sqrt(d2_1), 3)
    
      #Hexagonal
      d2_1 = 4.0 / 3.0 * ((plane[0]**2 + plane[0]*plane[1] + plane[1]**2) / self.Lhexagonal.a**2) + plane[2]**2 / self.Lhexagonal.c**2
      self.assertAlmostEqual(reciprocal.planeSpacing(plane, self.Lhexagonal), 1.0/sqrt(d2_1), 3)
    
      #Rhombohedral
      d2_1 = ((h**2 + k**2 + l**2) * sin(self.Lrhombohedral.alpha)**2 + 2*(h*k + k*l + h*l)*(cos(self.Lrhombohedral.alpha)**2 - cos(self.Lrhombohedral.alpha))) / \
              (self.Lrhombohedral.a**2 * (1 - 3*cos(self.Lrhombohedral.alpha)**2 + 2*cos(self.Lrhombohedral.alpha)**3))
      self.assertAlmostEqual(reciprocal.planeSpacing(plane, self.Lrhombohedral), 1.0/sqrt(d2_1), 3)
    
      #Orthorhombic
      d2_1 = h**2 / self.Lorthorhombic.a**2 + k**2 / self.Lorthorhombic.b**2 + l**2 / self.Lorthorhombic.c**2
      self.assertAlmostEqual(reciprocal.planeSpacing(plane, self.Lorthorhombic), 1.0/sqrt(d2_1), 3)
      
      #Monoclinic
      d2_1 = (1.0 / sin(self.Lmonoclinic.beta)**2) * (h**2 / self.Lmonoclinic.a**2 + k**2*sin(self.Lmonoclinic.beta)**2 / self.Lmonoclinic.b**2 + l**2 / self.Lmonoclinic.c**2 - 2*h*l*cos(self.Lmonoclinic.beta) / (self.Lmonoclinic.a * self.Lmonoclinic.c))
      self.assertAlmostEqual(reciprocal.planeSpacing(plane, self.Lmonoclinic), 1.0/sqrt(d2_1), 3)
      
      #Triclinic
      s11 = self.Ltriclinic.b**2*self.Ltriclinic.c**2*sin(self.Ltriclinic.alpha)**2
      s22 = self.Ltriclinic.a**2*self.Ltriclinic.c**2*sin(self.Ltriclinic.beta)**2
      s33 = self.Ltriclinic.a**2*self.Ltriclinic.b**2*sin(self.Ltriclinic.gamma)**2
      s12 = self.Ltriclinic.a*self.Ltriclinic.b*self.Ltriclinic.c**2*(cos(self.Ltriclinic.alpha)*cos(self.Ltriclinic.beta) - cos(self.Ltriclinic.gamma))
      s23 = self.Ltriclinic.a**2*self.Ltriclinic.b*self.Ltriclinic.c*(cos(self.Ltriclinic.beta)*cos(self.Ltriclinic.gamma) - cos(self.Ltriclinic.alpha))
      s13 = self.Ltriclinic.a*self.Ltriclinic.b**2*self.Ltriclinic.c*(cos(self.Ltriclinic.gamma)*cos(self.Ltriclinic.alpha) - cos(self.Ltriclinic.beta))
      v = self.Ltriclinic.a*self.Ltriclinic.b*self.Ltriclinic.c*sqrt(1 - cos(self.Ltriclinic.alpha)**2 - cos(self.Ltriclinic.beta)**2 - cos(self.Ltriclinic.gamma)**2 + 2*cos(self.Ltriclinic.alpha)*cos(self.Ltriclinic.beta)*cos(self.Ltriclinic.gamma))
      
      d2_1 = (1.0 / v**2)*(s11*h**2 + s22*k**2 + s33*l**2 + 2*s12*h*k + 2*s23*k*l + 2*s13*h*l)
      self.assertAlmostEqual(reciprocal.planeSpacing(plane, self.Ltriclinic), 1.0/sqrt(d2_1), 3)
  
  def testInterplanarAngle(self):
    for plane1 in self.planes:
      h1 = plane1[0]
      k1 = plane1[1]
      l1 = plane1[2]
      
      for plane2 in self.planes:
        h2 = plane2[0]
        k2 = plane2[1]
        l2 = plane2[2]
        
        #cubic
        cosphi = (h1*h2 + k1*k2 + l1*l2) / sqrt((h1**2+k1**2+l1**2)*(h2**2+k2**2+l2**2))
        self.assertAlmostEqual(reciprocal.interplanarAngle(plane1, plane2, self.Lcubic), _acos(cosphi), 3)
        
        #tetragonal
        cosphi = ((h1*h2 + k1*k2)/self.Ltetragonal.a**2 + l1*l2/self.Ltetragonal.c**2) / \
                  sqrt(((h1**2+k1**2)/self.Ltetragonal.a**2 + l1**2/self.Ltetragonal.c**2)*((h2**2+k2**2)/self.Ltetragonal.a**2 + l2**2/self.Ltetragonal.c**2))
        self.assertAlmostEqual(reciprocal.interplanarAngle(plane1, plane2, self.Ltetragonal), _acos(cosphi), 3)
        
        #hexagonal
        cosphi = (h1*h2 + k1*k2 + 0.5*(h1*k2 + h2*k1) + (3*self.Lhexagonal.a**2)/(4*self.Lhexagonal.c**2)*l1*l2) / \
                  sqrt((h1**2 + k1**2 + h1*k1 + (3*self.Lhexagonal.a**2)/(4*self.Lhexagonal.c**2)*l1**2)*(h2**2 + k2**2 + h2*k2 + (3*self.Lhexagonal.a**2)/(4*self.Lhexagonal.c**2)*l2**2))
        self.assertAlmostEqual(reciprocal.interplanarAngle(plane1, plane2, self.Lhexagonal), _acos(cosphi), 3)
        
        #rhombohedral
        v = self.Lrhombohedral.a**3*sqrt(1 - 3*cos(self.Lrhombohedral.alpha)**2 + 2*cos(self.Lrhombohedral.alpha)**3)
        d1 = reciprocal.planeSpacing(plane1, self.Lrhombohedral)
        d2 = reciprocal.planeSpacing(plane2, self.Lrhombohedral)
        cosphi = (self.Lrhombohedral.a**4*d1*d2)/v**2 * (sin(self.Lrhombohedral.alpha)**2*(h1*h2 + k1*k2 + l1*l2) + \
                                      (cos(self.Lrhombohedral.alpha)**2 - cos(self.Lrhombohedral.alpha))*(k1*l2 + k2*l1 + l1*h2 + l2*h1 + h1*k2 + h2*k1))
        self.assertAlmostEqual(reciprocal.interplanarAngle(plane1, plane2, self.Lrhombohedral), _acos(cosphi), 3)
        
        #orthorhombic
        cosphi = (h1*h2/self.Lorthorhombic.a**2 + k1*k2/self.Lorthorhombic.b**2 + l1*l2/self.Lorthorhombic.c**2) / \
                  sqrt((h1**2/self.Lorthorhombic.a**2 + k1**2/self.Lorthorhombic.b**2 + l1**2/self.Lorthorhombic.c**2)*(h2**2/self.Lorthorhombic.a**2 + k2**2/self.Lorthorhombic.b**2 + l2**2/self.Lorthorhombic.c**2))
        self.assertAlmostEqual(reciprocal.interplanarAngle(plane1, plane2, self.Lorthorhombic), _acos(cosphi), 3)
        
        #monoclinic
        d1 = reciprocal.planeSpacing(plane1, self.Lmonoclinic)
        d2 = reciprocal.planeSpacing(plane2, self.Lmonoclinic)
        cosphi = d1*d2/sin(self.Lmonoclinic.beta)**2 * (h1*h2/self.Lmonoclinic.a**2 + k1*k2*sin(self.Lmonoclinic.beta)**2/self.Lmonoclinic.b**2 + l1*l2/self.Lmonoclinic.c**2 - (l1*h2+l2*h1)*cos(self.Lmonoclinic.beta)/(self.Lmonoclinic.a*self.Lmonoclinic.c))
        self.assertAlmostEqual(reciprocal.interplanarAngle(plane1, plane2, self.Lmonoclinic), _acos(cosphi), 3)
        
        #triclinic
        d1 = reciprocal.planeSpacing(plane1, self.Ltriclinic)
        d2 = reciprocal.planeSpacing(plane2, self.Ltriclinic)
        s11 = self.Ltriclinic.b**2*self.Ltriclinic.c**2*sin(self.Ltriclinic.alpha)**2
        s22 = self.Ltriclinic.a**2*self.Ltriclinic.c**2*sin(self.Ltriclinic.beta)**2
        s33 = self.Ltriclinic.a**2*self.Ltriclinic.b**2*sin(self.Ltriclinic.gamma)**2
        s12 = self.Ltriclinic.a*self.Ltriclinic.b*self.Ltriclinic.c**2*(cos(self.Ltriclinic.alpha)*cos(self.Ltriclinic.beta) - cos(self.Ltriclinic.gamma))
        s23 = self.Ltriclinic.a**2*self.Ltriclinic.b*self.Ltriclinic.c*(cos(self.Ltriclinic.beta)*cos(self.Ltriclinic.gamma) - cos(self.Ltriclinic.alpha))
        s13 = self.Ltriclinic.a*self.Ltriclinic.b**2*self.Ltriclinic.c*(cos(self.Ltriclinic.gamma)*cos(self.Ltriclinic.alpha) - cos(self.Ltriclinic.beta))
        v = self.Ltriclinic.a*self.Ltriclinic.b*self.Ltriclinic.c*sqrt(1 - cos(self.Ltriclinic.alpha)**2 - cos(self.Ltriclinic.beta)**2 - cos(self.Ltriclinic.gamma)**2 + 2*cos(self.Ltriclinic.alpha)*cos(self.Ltriclinic.beta)*cos(self.Ltriclinic.gamma))
        cosphi = d1*d2/v**2 * (s11*h1*h2 + s22*k1*k2 + s33*l1*l2 + s23*(k1*l2+k2*l1) + s13*(l1*h2+l2*h1) + s12*(h1*k2+h2*k1))
        self.assertAlmostEqual(reciprocal.interplanarAngle(plane1, plane2, self.Ltriclinic), _acos(cosphi), 3)
        
        
if __name__ == '__main__':
  logging.getLogger().setLevel(logging.DEBUG)
  unittest.main()
  
  
  
  
  
  