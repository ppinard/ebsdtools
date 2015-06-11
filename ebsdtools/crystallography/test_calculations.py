#!/usr/bin/env python
"""
================================================================================
:mod:`test_calculations` -- Unit tests for the module :mod:`calculations.`
================================================================================

.. module:: test_calculations
   :synopsis: Unit tests for the module :mod:`calculations.`

"""

# Script information for the file.
__author__ = "Philippe T. Pinard"
__email__ = "philippe.pinard@gmail.com"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2009 Philippe T. Pinard"
__license__ = "GPL v3"

# Standard library modules.
import unittest
import logging
from math import pi, sin, cos, sqrt
import copy
import os.path

# Third party modules.

# Local modules.
import DrixUtilities.Files as Files

import ebsdtools.crystallography.calculations as calculations
import ebsdtools.crystallography.atomsite as atomsite
import ebsdtools.crystallography.atomsites as atomsites
import ebsdtools.crystallography.unitcell as unitcell
import ebsdtools.crystallography.plane as plane
import ebsdtools.crystallography.scatteringfactors as scatteringfactors

import mathtools.algebra.vectors as vectors
from mathtools.rotation.trigo import acos

# Globals and constants variables.

class TestCalculations(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        # Manual testing
        self.cubic = unitcell.create_cubic_unitcell(2)
        self.tetragonal = unitcell.create_tetragonal_unitcell(2, 3)
        self.orthorhombic = unitcell.create_orthorhombic_unitcell(1, 2, 3)
        self.trigonal = unitcell.create_trigonal_unitcell(2, 35.0 / 180 * pi)
        self.hexagonal = unitcell.create_hexagonal_unitcell(2, 3)
        self.monoclinic = unitcell.create_monoclinic_unitcell(1, 2, 3, 55.0 / 180 * pi)
        self.triclinic = \
            unitcell.create_triclinic_unitcell(1, 2, 3,
                                               75.0 / 180 * pi, 55.0 / 180 * pi, 35.0 / 180 * pi)

        self.planes = [plane.Plane(1, 0, 0),
                       plane.Plane(1, 1, 0),
                       plane.Plane(1, 1, 1),
                       plane.Plane(2, 0, 2),
                       plane.Plane(1, 2, 3),
                       plane.Plane(4, 5, 6),
                       plane.Plane(0, 9, 2)]

        # Example 1.13 from Mathematical Crystallography (p.31-33)
        self.L1 = unitcell.create_hexagonal_unitcell(4.914, 5.409)

        self.atom1 = atomsite.AtomSite(8, (0.4141, 0.2681, 0.1188))
        self.atom2 = atomsite.AtomSite(14, (0.4699, 0.0, 0.0))
        self.atom3 = atomsite.AtomSite(14, (0.5301, 0.5301, 0.3333))

        # Problem 1.13 from Mathematical Crystallography (p.34)
        alpha = 93.11 / 180.0 * pi
        beta = 115.91 / 180.0 * pi
        gamma = 91.26 / 180.0 * pi
        self.L2 = unitcell.create_triclinic_unitcell(8.173, 12.869, 14.165
                                                     , alpha, beta, gamma)

        self.atom4 = atomsite.AtomSite(8, (0.3419, 0.3587, 0.1333))
        self.atom5 = atomsite.AtomSite(14, (0.5041, 0.3204, 0.1099))
        self.atom6 = atomsite.AtomSite(13, (0.1852, 0.3775, 0.1816))

        # Example 2.16 and Problem 2.9 from Mathematical Crystallography (p.64-65)
        alpha = 114.27 / 180.0 * pi
        beta = 82.68 / 180.0 * pi
        gamma = 94.58 / 180.0 * pi
        self.L3 = unitcell.create_triclinic_unitcell(6.621, 7.551, 17.381
                                                     , alpha, beta, gamma)

        # Problem 2.15 from Mathematical Crystallography (p.79)
        alpha = 113.97 / 180.0 * pi
        beta = 98.64 / 180.0 * pi
        gamma = 67.25 / 180.0 * pi
        self.L4 = unitcell.create_triclinic_unitcell(5.148, 7.251, 5.060
                                                     , alpha, beta, gamma)

        # Scattering factors
        relativepath = os.path.join('..', 'testdata', 'goodconfiguration.cfg')
        configurationfilepath = Files.getCurrentModulePath(__file__, relativepath)

        self.scatter = scatteringfactors.XrayScatteringFactors(configurationfilepath)

        # Atom sites
        self.atomsfcc = atomsites.AtomSites([atomsite.AtomSite(14, 0.5, 0.5, 0.0),
                                             atomsite.AtomSite(14, 0.5, 0.0, 0.5),
                                             atomsite.AtomSite(14, 0.0, 0.5, 0.5),
                                             atomsite.AtomSite(14, 0.0, 0.0, 0.0)])

        self.atomsbcc = atomsites.AtomSites([atomsite.AtomSite(14, 0.5, 0.5, 0.5),
                                             atomsite.AtomSite(14, 0.0, 0.0, 0.0)])

        self.atomshcp = atomsites.AtomSites([atomsite.AtomSite(14, 1 / 3.0, 2 / 3.0, 0.5),
                                             atomsite.AtomSite(14, 0.0, 0.0, 0.0)])

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        #self.fail("Test if the TestCase is working.")
        self.assert_(True)

    def testbonddistance(self):
        # Example 1.13
        bonddistance = calculations.bonddistance(self.atom1, self.atom2, self.L1)
        self.assertAlmostEqual(bonddistance, 1.608, 3)

        bonddistance = calculations.bonddistance(self.atom1, self.atom3, self.L1)
        self.assertAlmostEqual(bonddistance, 1.611, 3)

        # Problem 1.13
        bonddistance = calculations.bonddistance(self.atom4, self.atom5, self.L2)
        self.assertAlmostEqual(bonddistance, 1.5828, 3)

        bonddistance = calculations.bonddistance(self.atom4, self.atom6, self.L2)
        self.assertAlmostEqual(bonddistance, 1.7112, 3)

    def testbondangle(self):
        # Example 1.13
        bond_angle = calculations.bondangle(self.atom1, self.atom2, self.atom3, self.L1)
        self.assertAlmostEqual(bond_angle * 180 / pi, 143.7, 1)

        # Problem 1.13
        bond_angle = calculations.bondangle(self.atom4, self.atom5, self.atom6, self.L2)
        self.assertAlmostEqual(bond_angle * 180 / pi, 165.6, 1)

    def testplanespacing(self):
        # Example 2.3
        hkl = plane.Plane(3, 1, 2)
        self.assertAlmostEqual(calculations.planespacing(hkl, self.L2), 1.964, 3)

    def testplanespacing_cubic(self):
        equation = lambda lat, h, k, l: (h ** 2 + k ** 2 + l ** 2) / lat.a ** 2

        for plane in self.planes:
            spacing = calculations.planespacing(plane, self.cubic)
            expected_spacing = 1.0 / sqrt(equation(self.cubic, *plane))
            self.assertAlmostEqual(spacing, expected_spacing)

    def testplanespacing_tetragonal(self):
        equation = lambda lat, h, k, l: (h ** 2 + k ** 2) / lat.a ** 2 + \
                                        l ** 2 / lat.c ** 2

        for plane in self.planes:
            spacing = calculations.planespacing(plane, self.tetragonal)
            expected_spacing = 1.0 / sqrt(equation(self.tetragonal, *plane))
            self.assertAlmostEqual(spacing, expected_spacing)

    def testplanespacing_hexagonal(self):
        equation = lambda lat, h, k, l: \
          4.0 / 3.0 * ((h ** 2 + h * k + k ** 2) / lat.a ** 2) + \
          l ** 2 / lat.c ** 2

        for plane in self.planes:
            spacing = calculations.planespacing(plane, self.hexagonal)
            expected_spacing = 1.0 / sqrt(equation(self.hexagonal, *plane))
            self.assertAlmostEqual(spacing, expected_spacing)

    def testplanespacing_trigonal(self):
        equation = lambda lat, h, k, l: \
          ((h ** 2 + k ** 2 + l ** 2) * sin(lat.alpha) ** 2 + \
           2 * (h * k + k * l + h * l) * (cos(lat.alpha) ** 2 - cos(lat.alpha))) / \
           (lat.a ** 2 * (1 - 3 * cos(lat.alpha) ** 2 + 2 * cos(lat.alpha) ** 3))

        for plane in self.planes:
            spacing = calculations.planespacing(plane, self.trigonal)
            expected_spacing = 1.0 / sqrt(equation(self.trigonal, *plane))
            self.assertAlmostEqual(spacing, expected_spacing)

    def testplanespacing_orthorhombic(self):
        equation = lambda lat, h, k, l: \
          h ** 2 / lat.a ** 2 + k ** 2 / lat.b ** 2 + l ** 2 / lat.c ** 2

        for plane in self.planes:
            spacing = calculations.planespacing(plane, self.orthorhombic)
            expected_spacing = 1.0 / sqrt(equation(self.orthorhombic, *plane))
            self.assertAlmostEqual(spacing, expected_spacing)

    def testplanespacing_monoclinic(self):
        equation = lambda lat, h, k, l: \
          (1.0 / sin(lat.beta) ** 2) * \
          (h ** 2 / lat.a ** 2 +
           k ** 2 * sin(lat.beta) ** 2 / lat.b ** 2 + \
           l ** 2 / lat.c ** 2 - \
           2 * h * l * cos(lat.beta) / (lat.a * lat.c))

        for plane in self.planes:
            spacing = calculations.planespacing(plane, self.monoclinic)
            expected_spacing = 1.0 / sqrt(equation(self.monoclinic, *plane))
            self.assertAlmostEqual(spacing, expected_spacing)

    def testplanespacing_triclinic(self):
        lat = self.triclinic

        s11 = lat.b ** 2 * lat.c ** 2 * sin(lat.alpha) ** 2
        s22 = lat.a ** 2 * lat.c ** 2 * sin(lat.beta) ** 2
        s33 = lat.a ** 2 * lat.b ** 2 * sin(lat.gamma) ** 2
        s12 = lat.a * lat.b * lat.c ** 2 * (cos(lat.alpha) * cos(lat.beta) - cos(lat.gamma))
        s23 = lat.a ** 2 * lat.b * lat.c * (cos(lat.beta) * cos(lat.gamma) - cos(lat.alpha))
        s13 = lat.a * lat.b ** 2 * lat.c * (cos(lat.gamma) * cos(lat.alpha) - cos(lat.beta))
        v = lat.a * lat.b * lat.c * sqrt(1 - cos(lat.alpha) ** 2 - \
                                         cos(lat.beta) ** 2 - \
                                         cos(lat.gamma) ** 2 + \
                                         2 * cos(lat.alpha) * cos(lat.beta) * cos(lat.gamma))

        equation = lambda h, k, l: \
            (1.0 / v ** 2) * (s11 * h ** 2 + \
                              s22 * k ** 2 + \
                              s33 * l ** 2 + \
                              2 * s12 * h * k + \
                              2 * s23 * k * l + \
                              2 * s13 * h * l)

        for plane in self.planes:
            spacing = calculations.planespacing(plane, self.triclinic)
            expected_spacing = 1.0 / sqrt(equation(*plane))
            self.assertAlmostEqual(spacing, expected_spacing)

    def testelectronwavelength(self):
        #References: Wikipedia
        self.assertAlmostEqual(calculations.electronwavelength(10e3),
                                0.12031075249234069)
        self.assertAlmostEqual(calculations.electronwavelength(200e3)
                               , 0.020538907051308845)

    def testdiffractionangle(self):
        #References: \url{http://hyperphysics.phy-astr.gsu.edu/hbase/quantum/bragg.html}
        angle = calculations.diffractionangle(wavelength=0.12 * 10
                                              , planespacing=1 * 10
                                              , order=1)
        self.assertAlmostEqual(angle / pi * 180, 3.439812767515196)

        angle = calculations.diffractionangle(wavelength=0.2 * 10
                                              , planespacing=5 * 10
                                              , order=1)
        self.assertAlmostEqual(angle / pi * 180, 1.1459919983885926)

        angle = calculations.diffractionangle(wavelength=0.0025 * 10
                                              , planespacing=.25 * 10
                                              , order=1)
        self.assertAlmostEqual(angle / pi * 180, 0.2864800912409137)

    def testzoneaxis(self):
        # Example 2.16
        plane1 = plane.Plane(-0.0963, 0.1243, 0.2018)
        plane2 = plane.Plane(0.1084, -0.0880, 0.2947)
        zone = calculations.zoneaxis(plane1, plane2, self.L3)
        expected_zone = [1.0219, 0.8478, 0.0888]
        self.assertTrue(vectors.almostequal(zone, expected_zone, 3))

        # Problem 2.9
        plane1 = plane.Plane(0.1166, 0.0968, 0.0101)
        plane2 = plane.Plane(-0.0286, 0.0369, 0.0599)
        zone = calculations.zoneaxis(plane1, plane2, self.L3)
        expected_zone = [0.0895, -0.097, -0.0030]
        self.assertTrue(vectors.almostequal(zone, expected_zone, 3))

    def testinterplanarangle(self):
        # Problem 2.15
        plane1 = plane.Plane(1, 0, 0)
        plane2 = plane.Plane(1, 1, 0)
        angle = calculations.interplanarangle(plane1, plane2, self.L4)
        angle *= 180 / pi
        self.assertAlmostEqual(angle, 44.7387, 3)

    def testinterplanarangle_cubic(self):
        equation = lambda h1, k1, l1, h2, k2, l2: \
          (h1 * h2 + k1 * k2 + l1 * l2) / \
          sqrt((h1 ** 2 + k1 ** 2 + l1 ** 2) * (h2 ** 2 + k2 ** 2 + l2 ** 2))

        for plane1 in self.planes:
            for plane2 in self.planes:
                angle = calculations.interplanarangle(plane1, plane2, self.cubic)
                args = copy.deepcopy(plane1)
                args.extend(plane2)
                expected_angle = acos(equation(*args))
                self.assertAlmostEqual(angle, expected_angle)

    def testinterplanarangle_tetragonal(self):
        equation = lambda lat, h1, k1, l1, h2, k2, l2: \
          ((h1 * h2 + k1 * k2) / lat.a ** 2 + l1 * l2 / lat.c ** 2) / \
          sqrt(((h1 ** 2 + k1 ** 2) / lat.a ** 2 + l1 ** 2 / lat.c ** 2) * \
               ((h2 ** 2 + k2 ** 2) / lat.a ** 2 + l2 ** 2 / lat.c ** 2))

        for plane1 in self.planes:
            for plane2 in self.planes:
                angle = calculations.interplanarangle(plane1, plane2, self.tetragonal)
                args = copy.deepcopy(plane1)
                args.extend(plane2)
                expected_angle = acos(equation(self.tetragonal, *args))
                self.assertAlmostEqual(angle, expected_angle)

    def testinterplanarangle_hexagonal(self):
        equation = lambda lat, h1, k1, l1, h2, k2, l2: \
          (h1 * h2 + k1 * k2 + 0.5 * (h1 * k2 + h2 * k1) + \
           (3 * lat.a ** 2) / (4 * lat.c ** 2) * l1 * l2) / \
           sqrt((h1 ** 2 + k1 ** 2 + h1 * k1 + (3 * lat.a ** 2) / \
                 (4 * lat.c ** 2) * l1 ** 2) * \
                 (h2 ** 2 + k2 ** 2 + h2 * k2 + (3 * lat.a ** 2) / \
                  (4 * lat.c ** 2) * l2 ** 2))

        for plane1 in self.planes:
            for plane2 in self.planes:
                angle = calculations.interplanarangle(plane1, plane2, self.hexagonal)
                args = copy.deepcopy(plane1)
                args.extend(plane2)
                expected_angle = acos(equation(self.hexagonal, *args))
                self.assertAlmostEqual(angle, expected_angle)

    def testinterplanarangle_trigonal(self):
        lat = self.trigonal

        v = lat.a ** 3 * sqrt(1 - 3 * cos(lat.alpha) ** 2 + 2 * cos(lat.alpha) ** 3)

        equation = lambda lat, h1, k1, l1, h2, k2, l2: \
          (lat.a ** 4 * d1 * d2) / v ** 2 * \
          (sin(lat.alpha) ** 2 * (h1 * h2 + k1 * k2 + l1 * l2) + \
           (cos(lat.alpha) ** 2 - cos(lat.alpha)) * \
           (k1 * l2 + k2 * l1 + l1 * h2 + l2 * h1 + h1 * k2 + h2 * k1))

        for plane1 in self.planes:
            for plane2 in self.planes:
                d1 = calculations.planespacing(plane1, lat)
                d2 = calculations.planespacing(plane2, lat)
                angle = calculations.interplanarangle(plane1, plane2, self.trigonal)
                args = copy.deepcopy(plane1)
                args.extend(plane2)
                expected_angle = acos(equation(self.trigonal, *args))
                self.assertAlmostEqual(angle, expected_angle, 6)

    def testinterplanarangle_orthorhombic(self):
        equation = lambda lat, h1, k1, l1, h2, k2, l2: \
          (h1 * h2 / lat.a ** 2 + k1 * k2 / lat.b ** 2 + l1 * l2 / lat.c ** 2) / \
          sqrt((h1 ** 2 / lat.a ** 2 + \
                k1 ** 2 / lat.b ** 2 + \
                l1 ** 2 / lat.c ** 2) \
               * (h2 ** 2 / lat.a ** 2 + \
                  k2 ** 2 / lat.b ** 2 + \
                  l2 ** 2 / lat.c ** 2))

        for plane1 in self.planes:
            for plane2 in self.planes:
                angle = calculations.interplanarangle(plane1, plane2, self.orthorhombic)
                args = copy.deepcopy(plane1)
                args.extend(plane2)
                expected_angle = acos(equation(self.orthorhombic, *args))
                self.assertAlmostEqual(angle, expected_angle, 6)

    def testinterplanarangle_monoclinic(self):
        equation = lambda lat, h1, k1, l1, h2, k2, l2: \
          d1 * d2 / sin(lat.beta) ** 2 * \
          (h1 * h2 / lat.a ** 2 + \
           k1 * k2 * sin(lat.beta) ** 2 / lat.b ** 2 + \
           l1 * l2 / lat.c ** 2 - \
           (l1 * h2 + l2 * h1) * cos(lat.beta) / (lat.a * lat.c))

        for plane1 in self.planes:
            for plane2 in self.planes:
                d1 = calculations.planespacing(plane1, self.monoclinic)
                d2 = calculations.planespacing(plane2, self.monoclinic)
                angle = calculations.interplanarangle(plane1, plane2, self.monoclinic)
                args = copy.deepcopy(plane1)
                args.extend(plane2)
                expected_angle = acos(equation(self.monoclinic, *args))
                self.assertAlmostEqual(angle, expected_angle, 6)

    def testinterplanarangle_triclinic(self):
        lat = self.triclinic

        s11 = lat.b ** 2 * lat.c ** 2 * sin(lat.alpha) ** 2
        s22 = lat.a ** 2 * lat.c ** 2 * sin(lat.beta) ** 2
        s33 = lat.a ** 2 * lat.b ** 2 * sin(lat.gamma) ** 2
        s12 = lat.a * lat.b * lat.c ** 2 * (cos(lat.alpha) * cos(lat.beta) - cos(lat.gamma))
        s23 = lat.a ** 2 * lat.b * lat.c * (cos(lat.beta) * cos(lat.gamma) - cos(lat.alpha))
        s13 = lat.a * lat.b ** 2 * lat.c * (cos(lat.gamma) * cos(lat.alpha) - cos(lat.beta))
        v = lat.a * lat.b * lat.c * sqrt(1 - cos(lat.alpha) ** 2 - \
                                         cos(lat.beta) ** 2 - \
                                         cos(lat.gamma) ** 2 + \
                                         2 * cos(lat.alpha) * cos(lat.beta) * cos(lat.gamma))

        equation = lambda lat, h1, k1, l1, h2, k2, l2: \
            d1 * d2 / v ** 2 * (s11 * h1 * h2 + \
                                s22 * k1 * k2 + \
                                s33 * l1 * l2 + \
                                s23 * (k1 * l2 + k2 * l1) + \
                                s13 * (l1 * h2 + l2 * h1) + \
                                s12 * (h1 * k2 + h2 * k1))

        for plane1 in self.planes:
            for plane2 in self.planes:
                d1 = calculations.planespacing(plane1, self.triclinic)
                d2 = calculations.planespacing(plane2, self.triclinic)
                angle = calculations.interplanarangle(plane1, plane2, self.triclinic)
                args = copy.deepcopy(plane1)
                args.extend(plane2)
                expected_angle = acos(equation(self.triclinic, *args))
                self.assertAlmostEqual(angle, expected_angle, 6)

    def testzoneaxis_goniometricangles(self):
        # Example 2.20
        zoneaxis = vectors.Vector3D(0, 1, 0)
        phi, rho = calculations.zoneaxis_goniometricangles(zoneaxis, self.L2)
        phi *= 180 / pi
        rho *= 180 / pi
        self.assertAlmostEqual(phi, -2.919, 2)
        self.assertAlmostEqual(rho, 93.11, 2)

    def testfacepole_goniometricangles(self):
        # Example 2.20
        facepole = vectors.Vector3D(1, 1, 1)
        phi, rho = calculations.facepole_goniometricangles(facepole, self.L2)
        phi *= 180 / pi
        rho *= 180 / pi
        self.assertAlmostEqual(phi, 62.03, 2)
        self.assertAlmostEqual(rho, 69.89, 2)

    def testare_planes_equivalent(self):
        plane1 = plane.Plane(1, 1, 1)
        plane2 = plane.Plane(-1, -1, -1)
        self.assertTrue(calculations.are_planes_equivalent(plane1, plane2,
                                                           self.cubic))

    def testformfactor(self):
        plane1 = plane.Plane(1, 1, 1)
        plane2 = plane.Plane(1, 0, 1)

        # FCC
        formfactor = calculations.formfactor(plane1, self.cubic,
                                             self.atomsfcc, self.scatter)
        expected_formfactor = 27.527840181773566
        self.assertAlmostEqual(abs(formfactor), expected_formfactor)

        formfactor = calculations.formfactor(plane2, self.cubic,
                                             self.atomsfcc, self.scatter)
        expected_formfactor = 0
        self.assertAlmostEqual(abs(formfactor), expected_formfactor)

        # BCC
        formfactor = calculations.formfactor(plane1, self.cubic,
                                             self.atomsbcc, self.scatter)
        expected_formfactor = 0
        self.assertAlmostEqual(abs(formfactor), expected_formfactor)

        formfactor = calculations.formfactor(plane2, self.cubic,
                                             self.atomsbcc, self.scatter)
        expected_formfactor = 15.319715145909786
        self.assertAlmostEqual(abs(formfactor), expected_formfactor)

        # HCP
        formfactor = calculations.formfactor(plane1, self.hexagonal,
                                             self.atomshcp, self.scatter)
        expected_formfactor = 0
        self.assertAlmostEqual(abs(formfactor), expected_formfactor)

        formfactor = calculations.formfactor(plane2, self.hexagonal,
                                             self.atomshcp, self.scatter)
        expected_formfactor = complex(11.800945464186695, -6.8132790404402881)
        self.assertAlmostEqual(formfactor.real, expected_formfactor.real)
        self.assertAlmostEqual(formfactor.imag, expected_formfactor.imag)

    def testmaximum_formfactor(self):
        #FCC
        maximum = \
            calculations.maximum_formfactor(self.cubic, self.atomsfcc, self.scatter)
        expected_maximum = 55.9904
        self.assertAlmostEqual(maximum, expected_maximum)

        # BCC
        maximum = \
            calculations.maximum_formfactor(self.cubic, self.atomsbcc, self.scatter)
        expected_maximum = 27.9952
        self.assertAlmostEqual(maximum, expected_maximum)

        # HCP
        maximum = \
            calculations.maximum_formfactor(self.hexagonal, self.atomshcp, self.scatter)
        expected_maximum = 27.9952
        self.assertAlmostEqual(maximum, expected_maximum)

    def testdiffraction_intensity(self):
        plane1 = plane.Plane(1, 1, 1)
        plane2 = plane.Plane(1, 0, 1)

        # FCC
        intensity = calculations.diffraction_intensity(plane1, self.cubic,
                                                       self.atomsfcc, self.scatter)
        expected_intensity = 757.78198507326738
        self.assertAlmostEqual(intensity, expected_intensity)

        intensity = calculations.diffraction_intensity(plane2, self.cubic,
                                                       self.atomsfcc, self.scatter)
        expected_intensity = 0
        self.assertAlmostEqual(intensity, expected_intensity)

        # BCC
        intensity = calculations.diffraction_intensity(plane1, self.cubic,
                                                       self.atomsbcc, self.scatter)
        expected_intensity = 0
        self.assertAlmostEqual(intensity, expected_intensity)

        intensity = calculations.diffraction_intensity(plane2, self.cubic,
                                                       self.atomsbcc, self.scatter)
        expected_intensity = 234.69367215181771
        self.assertAlmostEqual(intensity, expected_intensity)

        # HCP
        intensity = calculations.diffraction_intensity(plane1, self.cubic,
                                                       self.atomshcp, self.scatter)
        expected_intensity = 0
        self.assertAlmostEqual(intensity, expected_intensity)

        intensity = calculations.diffraction_intensity(plane2, self.cubic,
                                                       self.atomshcp, self.scatter)
        expected_intensity = 176.02025411386322
        self.assertAlmostEqual(intensity, expected_intensity)

    def testdiffraction_maxintensity(self):
        #FCC
        maximum = \
            calculations.diffraction_maxintensity(self.cubic, self.atomsfcc, self.scatter)
        expected_maximum = 55.9904 ** 2
        self.assertAlmostEqual(maximum, expected_maximum)

        # BCC
        maximum = \
            calculations.diffraction_maxintensity(self.cubic, self.atomsbcc, self.scatter)
        expected_maximum = 27.9952 ** 2
        self.assertAlmostEqual(maximum, expected_maximum)

        # HCP
        maximum = \
            calculations.diffraction_maxintensity(self.hexagonal, self.atomshcp, self.scatter)
        expected_maximum = 27.9952 ** 2
        self.assertAlmostEqual(maximum, expected_maximum)

    def testis_diffracting(self):
        #TODO: Test is_diffractiong() with other cases
        plane1 = plane.Plane(1, 1, 1)
        plane2 = plane.Plane(1, 0, 1)

        # FCC
        self.assertTrue(calculations.is_diffracting(plane1,
                                                    self.cubic,
                                                    self.atomsfcc,
                                                    self.scatter))
        self.assertFalse(calculations.is_diffracting(plane2,
                                                     self.cubic,
                                                     self.atomsfcc,
                                                     self.scatter))

        # BCC
        self.assertFalse(calculations.is_diffracting(plane1,
                                                     self.cubic,
                                                     self.atomsbcc,
                                                     self.scatter))
        self.assertTrue(calculations.is_diffracting(plane2,
                                                    self.cubic,
                                                    self.atomsbcc,
                                                    self.scatter))

        # HCP
        self.assertFalse(calculations.is_diffracting(plane1,
                                                     self.hexagonal,
                                                     self.atomshcp,
                                                     self.scatter))
        self.assertTrue(calculations.is_diffracting(plane2,
                                                    self.hexagonal,
                                                    self.atomshcp,
                                                    self.scatter))

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
