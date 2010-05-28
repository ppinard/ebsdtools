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
from math import pi, sin

# Third party modules.
import rmlimage.module.real.core as real

# Local modules.
import ebsdtools.patternsimulations.pattern as pattern
from ebsdtools.patternsimulations.linedrawing import slopeintercept_to_points

# Globals and constants variables.

class PatternRMLImage(pattern.Pattern):
  def __init__(self, width=2688, height=2048):
    pattern.Pattern.__init__(self, width, height, pattern.COLORMODE_GRAYSCALE)

  def _create_pattern_canvas(self):
    return real.RealMap(self._width, self._height)

  def _draw_band(self, canvas, band):
    # Get parameters
    x0, y0, x1, y1 = self._get_band_coordinates(band)
    colorarray = self._get_band_colorarray(band)

    # Create temporary map to store the band
    tmpmap = real.RealMap(self._width, self._height)
    real.Drawing.line(tmpmap, x0, y0, x1, y1, colorarray)

    # Add temporary map to the canvas
    real.MapMath.addition(canvas, tmpmap, canvas)

  def _get_band_coordinates(self, band):
    """
    Get the x0, y0, x1, y1 coordinates for a given slope and intercept.

    """
    m = band.m
    k = band.k

    p0, p1 = slopeintercept_to_points(m, k
                                      , self._width, self._height
                                      , origin_x=0.5, origin_y=0.5)

    x0, y0 = p0; x1, y1 = p1

    return x0, y0, x1, y1

  def _get_band_colorarray(self, band):
    raise NotImplementedError

class PatternFullSolidBand(PatternRMLImage):

  def _get_band_colorarray(self, band):
    """
    Create an array corresponding to the variation of the intensity across
    a band.

      * ``len(array) == band.thickness``
      * ``max(array) == band.normalizedintensity``

    """
    thickness = band.thickness
    intensity = band.normalizedintensity

    return [intensity] * thickness

def _sinc(x, f):
  try:
    r = sin(f * pi * x) / (f * pi * x)
  except ZeroDivisionError:
    r = 1

  if r > 0.0:
    r = 1

  return r

class PatternFullProfiledBand(PatternRMLImage):

  def _get_band_colorarray(self, band):
    """
    Create an array corresponding to the variation of the intensity across
    a band.

      * ``len(array) == band.thickness``
      * ``max(array) == band.normalizedintensity``

    """
    thickness = band.thickness
    intensity = band.normalizedintensity
    colorarray = []
    f = 4.0 / thickness

    for x in range(-thickness / 2, thickness / 2):
      colorarray.append(_sinc(x, f) * intensity)

    return colorarray

if __name__ == '__main__': #pragma: no cover
  import DrixUtilities.Runner as Runner
  Runner.Runner().run(runFunction=None)

