#!/usr/bin/env python
"""
================================================================================
:mod:`reflectors` -- Find reflectors
================================================================================

.. module:: reflectors
   :synopsis: Find reflectors
.. moduleauthor:: Philippe Pinard <philippe.pinard@mail.mcgill.ca>

.. inheritance-diagram:: reflectors

"""

# Script information for the file.
__author__ = "Philippe Pinard <philippe.pinard@mail.mcgill.ca>"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2009 Philippe Pinard"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = ""
__svnDate__ = ""
__svnId__ = ""

# Standard library modules.
import copy

# Third party modules.

# Local modules.
import ebsdtools.crystallography.plane as plane
import ebsdtools.crystallography.calculations as calculations

# Globals and constants variables.

class Reflector(dict):
  PLANE = 'plane'
  PLANESPACING = 'planespacing'
  INTENSITY = 'intensity'
  NORMALIZEDINTENSITY = 'normalizedintensity'

  def __init__(self, plane, planespacing, intensity):
    """
    Store the plane, plane spacing and intensity of a reflector.

    :type plane: :class:`plane.Plane`

    :type planespacing: :class:`float`

    :type intensity: :class:`intensity`

    **Attributes**

      * plane (indices): :attr:`plane`
      * plane spacing: :attr:`planespacing`
      * intensity: :attr:`intensity`

    """
    dict.__init__(self)

    self.setdefault(self.PLANE, plane)
    self.setdefault(self.PLANESPACING, planespacing)
    self.setdefault(self.INTENSITY, intensity)

  def __getattr__(self, attr):
    """
    Possible attributes:

      * plane (indices): :attr:`plane`
      * plane spacing: :attr:`planespacing`
      * intensity: :attr:`intensity`

    """
    return self.get(attr)

  def __repr__(self):
    return '{%s d=%f I=%f}' % (self.plane, self.planespacing, self.intensity)

  def __hash__(self):
    """
    Hash only with the plane value to prevent plane with the same indices as
    one plane already in the list to be added.

    .. seealso:: :meth:`plane.Plane.__hash__`

    """
    return hash(self.plane)

class Reflectors(list):
  def __init__(self, unitcell, atoms, scatteringfactors, maxindice=4):
    """
    Find and store reflectors for a set of atoms, unit cell and scattering
    factors.

    :type unitcell: :class:`unitcell.UnitCell`

    :type atoms: :class:`atomsites.AtomSites`

    :type scatteringfactors: derivative of
                            :class:`scatteringfactors.ScatteringFactors`

    :arg maxindice: maxium indice in the reflectors (``default=4``)
    :type maxindice: :class:`int`

    """
    self._unitcell = unitcell
    self._atoms = atoms
    self._scatter = scatteringfactors
    self._maxindice = maxindice

    data = self._compute_reflectors()
    list.__init__(self, data)

    self._calculate_normalized_intensity()

  def _compute_reflectors(self):
    reflectors = set()

    indices_range = range(-self._maxindice, self._maxindice + 1)

    for h in indices_range:
      for k in indices_range:
        for l in indices_range:
          if h == 0 and k == 0 and l == 0: continue # Skip null plane

          # Create plane
          # Only look at positive planes since negative plane are equivalent
          p = plane.Plane(h, k, l)
          p.positive()

          # Calculte the intensities
          intensity = calculations.diffraction_intensity(p
                                                         , self._unitcell
                                                         , self._atoms
                                                         , self._scatter)
          maxintensity = calculations.diffraction_maxintensity(self._unitcell
                                                               , self._atoms
                                                               , self._scatter)

          # Check if the plane diffracts
          if calculations._is_diffracting(intensity, maxintensity):
            planespacing = calculations.planespacing(p, self._unitcell)
            reflector = Reflector(p, planespacing, intensity)
            reflectors.add(reflector)

    return reflectors

  def _calculate_normalized_intensity(self):
    self.sort_by_intensity(reverse=True)

    maxintensity = self[0].intensity

    for refl in self:
      normalizedintensity = refl.intensity / maxintensity
      refl.setdefault(Reflector.NORMALIZEDINTENSITY, normalizedintensity)

  def sort_by_intensity(self, reverse=False):
    """
    Sort reflectors by intensity.

    :arg reverse: ascending or descending order
    :type reverse: :class:`bool`

    """
    compare = lambda x, y: cmp(x.intensity, y.intensity)
    self.sort(cmp=compare, reverse=reverse)

  def sort_by_planespacing(self, reverse=False):
    """
    Sort reflectors by plane spacing.

    :arg reverse: ascending or descending order
    :type reverse: :class:`bool`

    """
    compare = lambda x, y: cmp(x.planespacing, y.planespacing)
    self.sort(cmp=compare, reverse=reverse)

  def get(self, plane):
    """
    Return the :class:`Reflector` for the specified plane.

    :type plane: :class:`plane.Plane`

    :rtype: :class:`Reflector`

    """
    for refl in self:
      if refl.plane == plane:
        return refl

    return None

if __name__ == '__main__': #pragma: no cover
  import DrixUtilities.Runner as Runner
  Runner.Runner().run(runFunction=None)

