#!/usr/bin/env python
"""
================================================================================
:mod:`calculations` -- Various calculations using lattice, atom sites, plane.
================================================================================

.. module:: calculations
   :synopsis: Various calculations using lattice, atom sites, plane.

"""

# Script information for the file.
__author__ = "Philippe T. Pinard"
__email__ = "philippe.pinard@gmail.com"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2009 Philippe T. Pinard"
__license__ = "GPL v3"

# Subversion informations for the file.
__svnRevision__ = ""
__svnDate__ = ""
__svnId__ = ""

# Standard library modules.
from math import sqrt, asin, atan2, pi, cos
from cmath import exp

# Third party modules.

# Local modules.
import mathtools.rotation.matrices as matrices
import mathtools.algebra.vectors as vectors
from mathtools.rotation.trigo import acos

# Globals and constants variables.
from mathtools.constants import m_e, c, h, e

def bonddistance(atom1, atom2, unitcell):
    """
    Calculate the distance between *atom1* and *atom2* of a given *unitcell*.
    
    :type atom1: :class:`atomsite.AtomSite`
    
    :type atom2: :class:`atomsite.AtomSite`
    
    :type unitcell: :class:`unitcell.UnitCell`
    
    :rtype: :class:`float`
    
    **References**
    
      Equation 1.13 from Mathematical Crystallography
    
    """
    atom1vector = atom1.position
    atom2vector = atom2.position
    metricalmatrix = unitcell.metricalmatrix

    # Vector between atom1 and atom2
    vector = atom2vector - atom1vector

    # Distance square
    distance_sq = vector * (metricalmatrix * vector)

    # Distance
    distance = sqrt(distance_sq)

    return distance

def bondangle(atom1, atom2, atom3, unitcell):
    """
    Calculate the bond angle (in radians) between the vector
    from *atom1* to *atom2* and the vector from *atom1* to *atom3*.
    
    :type atom1: :class:`atomsite.AtomSite`
    
    :type atom2: :class:`atomsite.AtomSite`
    
    :type atom3: :class:`atomsite.AtomSite`
    
    :type unitcell: :class:`unitcell.UnitCell`
    
    :rtype: :class:`float`
    
    **References**
    
      Equation 1.13 from Mathematical Crystallography
    
    """
    atom1vector = atom1.position
    atom2vector = atom2.position
    atom3vector = atom3.position
    metricalmatrix = unitcell.metricalmatrix

    # Interatom vectors
    vector12 = atom2vector - atom1vector
    vector13 = atom3vector - atom1vector

    # Dot product
    dotproduct = vector12 * (metricalmatrix * vector13)

    # Bond distance
    bonddistance12 = bonddistance(atom1, atom2, unitcell)
    bonddistance13 = bonddistance(atom1, atom3, unitcell)

    # Cosine
    cosine = dotproduct / (bonddistance12 * bonddistance13)

    # Angle
    angle = acos(cosine)

    return angle

def planespacing(plane, unitcell):
    """
    Calculate the plane spacing between two adjacent planes of a unit cell.
    
    :type plane: :class:`plane.Plane`
    
    :type unitcell: :class:`unitcell.UnitCell`
    
    :rtype: :class:`float`
    
    **References**
    
      Mathematical Crystallography
    
    """
    matrix = matrices.inverse(unitcell.metricalmatrix)

    # s square (d = 1/s^2)
    s_sq = plane * (matrix * plane)

    # plane spacing d
    d = 1.0 / sqrt(s_sq)

    return d

def electronwavelength(energy):
    """
    Return the relativistic electron wavelength.
    
    :arg energy: energy in eV
    :type energy: :class:`float`
    
    :return: wavelength in angstrom
    :rtype: :class:`float`
    
    """
    a = h / sqrt(2 * m_e * e)
    b = 2 * e / (m_e * c ** 2)

    return a / sqrt(energy + b * energy ** 2) * 1e10

def diffractionangle(planespacing, wavelength, order=1):
    """
    Return the diffraction angle based on Bragg's Law
    (:math:`n\\lambda = 2d\\sin \\theta`)
    
    :arg planespacing: d in angstroms
    :type planespacing: float
    
    :arg wavelength: :math:`\\lambda` in angstroms
    :type wavelength: :class:`float`
    
    :arg order: n
    :type order: :class:`int`
    
    :return: :math:`\\theta` in radians
    :rtype: :class:`float`
    
    """
    return asin(order * wavelength / (2 * planespacing))

def zoneaxis(plane1, plane2, unitcell):
    """
    Calculate the zone axis of *plane1* and *plane2* of a unit cell.
    
    :type plane1: :class:`plane.Plane`
    
    :type plane2: :class:`plane.Plane`
    
    :arg unitcell: unit cell of *plane1* and *plane2*
    :type unitcell: :class:`unitcell.UnitCell`
    
    :rtype: :class:`vectors.Vector3D`
    
    **References**
    
      Theorem 2.14 from Mathematical Crystallography
    
    """
    metricalmatrix = unitcell.metricalmatrix
    volume_ = unitcell.volume_ # reciprocal volume

    s1_ = metricalmatrix * plane1
    s2_ = metricalmatrix * plane2

    crossproduct = vectors.cross(s1_, s2_)

    zone = volume_ * crossproduct

    return zone

def interplanarangle(plane1, plane2, unitcell):
    """
    Return the interplanar angle between *plane1* and *plane2* of a unit cell.
    
    :type plane1: :class:`plane.Plane`
    
    :type plane2: :class:`plane.Plane`
    
    :arg unitcell: unit cell of *plane1* and *plane2*
    :type unitcell: :class:`unitcell.UnitCell`
    
    :return: angle between *plane1* and *plane2* in radians
    :rtype: :class:`float`
    
    """
    b = matrices.inverse(matrices.transpose(unitcell.cartesianmatrix))

    plane1_c = b * plane1
    plane2_c = b * plane2

    return vectors.angle(plane1_c, plane2_c)

def zoneaxis_goniometricangles(zoneaxis, unitcell):
    """
    Return the goniometric angles (:math:`\\phi` and :math:`\\rho`)
    for a zone axis of a given unit cell.
    
    :type zoneaxis: :class:`vectors.Vector3D`
    
    :type unitcell: :class:`unitcell.UnitCell`
    
    :return: (:math:`\\phi`, :math:`\\rho`)
    :rtype: :class:`tuple`
    
    **References**
    
      Example 2.20 from Mathematical Crystallography
    
    """
    a = unitcell.cartesianmatrix

    # Change basis of zone axis (lattice basis) into the cartesian basis
    r_c = a * zoneaxis

    # Normalize r_c to have a unit length
    r_c.normalize()

    # Find phi and rho
    rho = acos(r_c[2])
    phi = atan2(r_c[0], r_c[1])

    return phi, rho

def facepole_goniometricangles(facepole, unitcell):
    """
    Return the goniometric angles (:math:`\\phi` and :math:`\\rho`)
    for a face pole of a given unit cell.
    
    :type facepole: :class:`vectors.Vector3D`
    
    :type unitcell: :class:`unitcell.UnitCell`
    
    :return: (:math:`\\phi`, :math:`\\rho`)
    :rtype: :class:`tuple`
    
    **References**
    
      Example 2.20 from Mathematical Crystallography
    
    """
    b = matrices.inverse(matrices.transpose(unitcell.cartesianmatrix))

    # Change basis of face pole (reciprocal basis) into the cartesian basis
    s_c = b * facepole

    # Normalize r_c to have a unit length
    s_c.normalize()

    # Find phi and rho
    rho = acos(s_c[2])
    phi = atan2(s_c[0], s_c[1])

    return phi, rho

def are_planes_equivalent(plane1, plane2, unitcell):
    """
    Return *True* if *plane1* and *plane2* are equivalent.
    In other words, check if the planes are part of the same family.
    
    **Conditions**
    
      * interplanar angle = 0 or pi
      * plane spacing of *plane1* == plane spacing of *plane2*
    
    :type plane1: :class:`plane.Plane`
    
    :type plane2: :class:`plane.Plane`
    
    :arg unitcell: unit cell of *plane1* and *plane2*
    :type unitcell: :class:`unitcell.UnitCell`
    
    :rtype: :class:`bool`
    
    """
    # Plane spacing
    d1 = planespacing(plane1, unitcell)
    d2 = planespacing(plane2, unitcell)

    # Dot product between plane1 and plane2
    dotproduct = cos(interplanarangle(plane1, plane2, unitcell))

    # Conditions
    if round(abs(dotproduct), 7) == 1 and round(abs(d2 - d1) , 7) == 0:
        return True
    else:
        return False

def formfactor(plane, unitcell, atomsites, scatteringfactors):
    """
    Calculate the form factor (F) for a given plane, set of atoms and scattering
    factors.
    
    :type plane: :class:`plane.Plane`
    
    :type unitcell: :class:`unitcell.UnitCell`
    
    :type atomsites: :class:`atomsites.AtomSites`
    
    :type scatteringfactors: derivative of
                              :class:`scatteringfactors.ScatteringFactors`
    
    **Equation**
    
      :math:`F = \\sum\\limits_{i=1}^N {\\exp{\\left(2\\pi i\\left[(h, k, l)\\cdot (u_i, v_i, w_i)\\right]\\right)}}`
    
    """
    F = 0.0
    d = planespacing(plane, unitcell)

    for atom in atomsites:
        position = atom.position
        atomicnumber = atom.atomicnumber

        x = 2 * pi * vectors.dot(plane, position)
        fi = scatteringfactors.get(atomicnumber, d)
        F += fi * exp(complex(0.0, x))

    return F

def maximum_formfactor(unitcell, atomsites, scatteringfactors):
    """
    Return the maximum value of the form factor for a given unit cell,
    atom sites and scattering factors.
    
    :type unitcell: :class:`unitcell.UnitCell`
    
    :type atomsites: :class:`atomsites.AtomSites`
    
    :type scatteringfactors: derivative of
                              :class:`scatteringfactors.ScatteringFactors`
    
    :rtype: :class:`float`
    
    """
    F = 0.0

    for atom in atomsites:
        atomicnumber = atom.atomicnumber
        fi = scatteringfactors._get(atomicnumber, 0.0)
        F += fi

    return F

def diffraction_intensity(plane, unitcell, atomsites, scatteringfactors):
    """
    Calculate the diffraction intensity (I) from the form factor (F).
    
    :type plane: :class:`plane.Plane`
    
    :type unitcell: :class:`unitcell.UnitCell`
    
    :type atomsites: :class:`atomsites.AtomSites`
    
    :type scatteringfactors: derivative of
                              :class:`scatteringfactors.ScatteringFactors`
    
    :rtype: :class:`float`
    
    **Equation**
    
      :math:`I = F^2`
    
    """
    F = formfactor(plane, unitcell, atomsites, scatteringfactors)

    try:
        intensity = (F * F.conjugate()).real
    except AttributeError:
        intensity = F * F

    return intensity

def diffraction_maxintensity(unitcell, atomsites, scatteringfactors):
    """
    Return the maximum diffraction intensity for a given unit cell,
    atom sites and scattering factors.
    
    :type unitcell: :class:`unitcell.UnitCell`
    
    :type atomsites: :class:`atomsites.AtomSites`
    
    :type scatteringfactors: derivative of
                              :class:`scatteringfactors.ScatteringFactors`
    
    :rtype: :class:`float`
    
    .. seealso:: :func:`diffractionintensity`
    
    """
    F = maximum_formfactor(unitcell, atomsites, scatteringfactors)

    try:
        intensity = (F * F.conjugate()).real
    except AttributeError:
        intensity = F * F

    return intensity

def is_diffracting(plane, unitcell, atomsites,
                   scatteringfactors, fraction=1e-14):
    """
    Evaluate if a plane is diffracting for a given set of atom sites and the
    specified scattering factors.
    
    The intensity has to be greater than fraction * (maximum intensity)
    to be diffracting.
    
    :type plane: :class:`plane.Plane`
    
    :type unitcell: :class:`unitcell.UnitCell`
    
    :type atomsites: :class:`atomsites.AtomSites`
    
    :type scatteringfactors: derivative of
                              :class:`scatteringfactors.ScatteringFactors`
    
    :arg fraction: criteria for diffraction
    :type fraction: :class:`float`
    
    **Condition**
    
      * a plane diffracts if :math:`I > 0`
    
    """
    maximum_intensity = diffraction_maxintensity(unitcell, atomsites,
                                                 scatteringfactors)
    intensity = diffraction_intensity(plane, unitcell, atomsites, scatteringfactors)

    return _is_diffracting(intensity, maximum_intensity, fraction)

def _is_diffracting(intensity, maximum_intensity, fraction=1e-14):
    """
    Evaluate if a plane is diffracting if
    
      intensity > (maximum_intensity * fraction)
    
    :arg intensity: diffraction intensity
    :type intensity: :class:`float`
    
    :arg maximum_intensity: maximum intensity for a unit cell and set of atoms
    :type maximum_intensity: maximum_intensity
    
    :arg fraction: criteria for diffraction
    :type fraction: :class:`float`
    
    :rtype: :class:`bool`
    
    """
    lowerlimit = fraction * maximum_intensity

    if intensity > lowerlimit:
        return True
    else:
        return False

if __name__ == '__main__': #pragma: no cover
    import DrixUtilities.Runner as Runner
    Runner.Runner().run(runFunction=None)

