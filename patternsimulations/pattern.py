#!/usr/bin/env python
"""
================================================================================
:mod:`module` -- ??
================================================================================

.. currentmodule:: module
.. moduleauthor:: Philippe Pinard <philippe.pinard@mail.mcgill.ca>

.. inheritance-diagram:: module

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
from math import sin, cos, atan

# Third party modules.

# Local modules.
from ebsdtools.patternsimulations.band import Band
from ebsdtools.crystallography.plane import Plane
import ebsdtools.crystallography.calculations as calculations

import mathtools.rotation.quaternions as quaternions
import mathtools.algebra.vectors as vectors

# Globals and constants variables.
COLORMODE_RGB = 'rgb'
COLORMODE_GRAYSCALE = 'grayscale'

def compute_planeequation_on_camera(plane
                                    , patterncenter_x=0.0
                                    , patterncenter_y=0.0
                                    , detectordistance=1.0
                                    ):
  """
  Return the slope and intercept of the projection of a plane (hkl)
  on a detector located at *detectordistance* and *patterncenter*

  :arg plane: diffracted plane
  :type plane: :class:`plane.Plane`

  :arg patterncenter_x: location of the pattern center
  in the horizontal direction (``default=0.0``)
  :type patterncenter_x: :class:`float`

  :arg patterncenter_y: location of the pattern center
  in the vertical direction (``default=0.0``)
  :type patterncenter_y: :class:`float`

  .. note:: A pattern center of ``(0.0, 0.0)`` is centered

  :arg detectordistance: distance between the sample and
  the detector window [default=1.0]
  :type detectordistance: float

  :return: :math:`(m, k)` the slope m and y-intercept k
  :rtype: tuple

  """
  nx = plane[0]
  ny = plane[1]
  nz = plane[2]

  if round(abs(nz), 7) > 0.0:
    m = -(nx / nz)
#    b = (h/l)*patternCenter[0] - detectordistance*k/l + patternCenter[1]
    k = -detectordistance * ny / nz
  else:
    if round(abs(nx), 7) > 0.0:
      m = None
#      b = -detectordistance*k/h + patternCenter[0]
      k = -detectordistance * ny / nx
    else: # Plane parallel to the screen
      m = None
      k = None

  return m, k

class Pattern(object):
  def __init__(self, width=2688, height=2048, colormode=COLORMODE_GRAYSCALE):
    self._width = width
    self._height = height
    self._colormode = colormode

    self._init_variables()

  def _init_variables(self):
    self._reflectors = []

    self._patterncenter_x = 0.0
    self._patterncenter_y = 0.0
    self._detectordistance = 0.3

    self._energy = 20e3

    self._numberreflectors = 32

    self._rotation = quaternions.Quaternion(1) # unit quaternion

    self._bands = []

  def set_reflectors(self, reflectors):
    """
    Set the reflectors for the pattern.

    :type reflectors: :class:`crystallography.reflectors.Reflectors`

    """
    self._reflectors = reflectors

  def set_patterncenter(self, x, y):
    """
    Set the coordinates of the pattern center.

    :type x, y: :class:`float`

    """
    self._patterncenter_x = float(x)
    self._patterncenter_y = float(y)

  def set_detectordistance(self, detectordistance):
    """
    Set the detector distance.

    :type detectordistance: :class:`float`

    """
    self._detectordistance = float(detectordistance)

  def set_energy(self, energy):
    """
    Set the energy of the incident electron beam in eV.

    :type energy: :class:`float`

    """
    self._energy = float(energy)

  def set_numberreflectors(self, number):
    """
    Set the maximum number of reflectors displayed in the pattern.

    :type number: :class:`int`

    """
    self._numberreflectors = int(number)

  def set_rotation(self, rotation):
    """
    Set the rotation of the pattern using a :class:`quaternions.Quaternion`.

    :type rotation: :class:`quaternions.Quaternion`

    """
    self._rotation = rotation

  def _get_slope_intercept(self, reflector):
    """
    Return the slope (m) and intercept (k) for a given *reflector* after
    its rotation.

    """
    # Apply rotation
    qrefl = quaternions.Quaternion(0, reflector.plane)
    refl_rotated = quaternions.rotate(qrefl, [self._rotation]).get_vector()
    plane = Plane(*refl_rotated)

    # Calculate slope and intercept
    m, k = compute_planeequation_on_camera(plane
                                           , self._patterncenter_x
                                           , self._patterncenter_y
                                           , self._detectordistance)

    return m, k

  def _get_band_halfwidths(self, reflector, m, k):

    ## Calculate the alpha angle: angle between the diffraction plane normal
    ## and the screen.
    x0 = vectors.Vector3D(0, 0, 0)

    # Vertical line
    if m is None:
      x1 = vectors.Vector3D(k, self._detectordistance, 0.0)
      x2 = vectors.Vector3D(k, self._detectordistance, 0.1)

    # Horizontal line
    elif round(abs(m), 7) == 0.0:
      x1 = vectors.Vector3D(0.0, self._detectordistance, k)
      x2 = vectors.Vector3D(0.1, self._detectordistance, k)

    # Oblique line
    else:
      x1 = vectors.Vector3D(0.0, self._detectordistance, k)

      # Intercept greater than 0.0
      if round(abs(k)) > 0.0:
        x2 = vectors.Vector3D(-k / m, self._detectordistance, 0.0)

      # Intercept less than 0.0
      else:
        x2 = vectors.Vector3D((1 - k) / m, self._detectordistance, 1.0)

    n = vectors.cross(x2 - x1, x1 - x0)
    s = vectors.Vector3D(n[0], 0, n[2])
    d = n.norm() / (x2 - x1).norm()
    alpha = vectors.angle(n, s)

    ## Calculate the diffraction angle
    planespacing = reflector.planespacing
    wavelength = calculations.electronwavelength(self._energy)
    theta = calculations.diffractionangle(planespacing, wavelength)

    ## Calculate the half-widths of the band (top and bottom or left and right)
    width_top = d * sin(theta) / cos(alpha - theta)
    width_bottom = d * sin(theta) / cos(alpha + theta)

    return width_top, width_bottom

  def _get_edges_intercepts(self, m, k, width_top, width_bottom):

    # Calculate the beta angle: angle between the band and the x-axis
    if m is None:
      beta = 0.0
    else:
      beta = atan(m)

    k_top = k + width_top / cos(beta)
    k_bottom = k - width_bottom / cos(beta)

    return k_top, k_bottom

  def _get_band_thickness(self, width):
    #The +1 prevents line with 0 thickness
    return int(2 * width * self._width) + 1

  def _calculate_bands(self):
    """
    Calculate the bands with the given parameters.

    """
    bands = []

    # Sort reflectors by decreasing order of intensity.
    self._reflectors.sort_by_intensity(reverse=True)

    # Select the reflectors
    reflectors = self._reflectors[:self._numberreflectors]

    # Create bands
    for index, reflector in enumerate(reflectors):
      band = Band(reflector)

      # Slope and intercept as of a PC = (0.0, 0.0).
      m, k = self._get_slope_intercept(reflector)

      # Skip plane parallel to the screen
      if m is None and k is None:
        continue

      # Half-width of the band.
      width_top, width_bottom = self._get_band_halfwidths(reflector, m, k)
      band.setdefault(Band.HALFWIDTHS, (width_top, width_bottom))

      # Slope and intercept translated to the correct PC.
      if m is None: # Vertical line
        k += self._patterncenter_x
      else: #Horizontal and oblique
        k += -m * self._patterncenter_x + self._patterncenter_y
      band.setdefault(Band.SLOPE, m)
      band.setdefault(Band.INTERCEPT, k)

      # Intercepts of the band edges
      k_top, k_bottom = self._get_edges_intercepts(m, k
                                                   , width_top, width_bottom)
      band.setdefault(Band.EDGEINTERCEPTS, (k_top, k_bottom))

      # Thickness
      thickness = self._get_band_thickness(max(width_top, width_bottom))
      band.setdefault(Band.THICKNESS, thickness)

      bands.append(band)

    self._bands = bands

  def draw(self):
    self._calculate_bands()

    canvas = self._create_pattern_canvas()

    for band in self._bands:
      self._draw_band(canvas, band)

    return canvas

  def _create_pattern_canvas(self):
    raise NotImplementedError

  def _draw_band(self, canvas, band):
    raise NotImplementedError

if __name__ == '__main__': #pragma: no cover
  import DrixUtilities.Runner as Runner
  Runner.Runner().run(runFunction=None)

