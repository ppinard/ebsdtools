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
from math import atan, pi, sin, cos

# Third party modules.

# Local modules.

# Globals and constants variables.

def linespace_to_houghspace(m, k):
  """
  Convert the slope and intercept of a line to a Hough peak.

  **Equations**

    * :math:`\\theta = -\\arccot(m)`
    * :math:`\\rho = k\\sin\\theta`

  :arg m: slope
  :type m: :class:`float`

  :arg k: intercept
  :type k: :class:`float`

  """
  if m is None: # Slope is infinity
    theta = 0.0
    rho = k
  else:
    theta = pi / 2.0 + atan(m)
    rho = k * sin(theta)

  return rho, theta

def houghspace_to_linespace(rho, theta):
  """
  Convert a Hough peak into the slope and intercept of a line.

  **Equations**

    * :math:`m = \\frac{-\\cos\\theta}{\\sin\\theta}`
    * :math:`k = \\frac{\\rho}{\\sin\\theta}`

  :arg rho: rho
  :type rho: :class:`float`

  :arg theta: theta
  :type theta: :class:`float`

  """
  try:
    m = -cos(theta) / sin(theta)
  except ZeroDivisionError:
    m = None

  try:
    k = rho / sin(theta)
  except ZeroDivisionError:
    k = rho

  return m, k

def angle_between_houghpeaks(peak1, peak2):
  """
  Calculate the angle between two Hough peaks.

  **Equations**

    :math:`\\alpha = min(\\theta_1 - \\theta2, \\theta_2 - \\theta_1)`

  **References**

    www.tpub.com/math2/5.htm

  :arg peak1: first peak
  :type peak1: :class:`peaks.Peak`

  :arg peak2: second peak
  :type peak2: :class:`peaks.Peak`

  """
  theta1 = peak1.theta
  theta2 = peak2.theta

  # Complementary angles
  alpha1 = theta1 - theta2
  alpha2 = theta2 - theta1

  # Return acute angle
  alpha = min(alpha1, alpha2)
  return alpha

if __name__ == '__main__': #pragma: no cover
  import DrixUtilities.Runner as Runner
  Runner.Runner().run(runFunction=None)

