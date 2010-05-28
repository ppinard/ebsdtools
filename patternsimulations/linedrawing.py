#!/usr/bin/env python
"""
================================================================================
:mod:`linedrawing` -- Calculations related to drawing line to create pattern.
================================================================================

.. module:: linedrawing
   :synopsis: Calculations related to drawing line to create pattern.
.. moduleauthor:: Philippe Pinard <philippe.pinard@mail.mcgill.ca>

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

# Third party modules.

# Local modules.

# Globals and constants variables.

def slopeintercept_to_points(m, k, width, height, origin_x, origin_y):
  """
  Convert a slope and intercept to two points on the image.

  :arg m: slope (in fraction of the width)
  :type m: float

  :arg k: intercept (in fraction of the width)
  :type k: float

  :arg width: width of the image (in pixels)
  :type width: int

  :arg height: height of the image (in pixels)
  :type height: int

  :arg origin_x: location of the origin in the horizontal direction
                  as a fraction of the width
  :type origin_x: float

  :arg origin_y: location of the origin in the vertical direction
                  as a fraction of the height
  :type origin_y: float

  :return: point 1 and point 2 (in pixels)
  :rtype: two tuples

  **Conditions**
    * if m is not None: :math:`y = mx + kb` or :math:`y=k` if m == 0
        * m: Slope (:math:`0 \leq m \leq 1`)
        * k: y intercept (:math`0 \leq k \leq 1`)

    * if m is None:
        * b: x intercept :math:`x=0` (:math:`0 \leq m \leq 1`)

  """
  # The reference frame.
  a = 1
  b = float(height) / float(width)
  c = (a * origin_x, b * origin_y)

  # Starting and ending point of the line.
  if m is None: # Vertical line
    p0 = (k + c[0], 0)
    p1 = (k + c[0], b)
  else:
    if abs(m) > 1:
      y = -0.1
      x = (y - b + k + c[1]) / (-m) + c[0]
      p0 = (x, y)

      y = b + 0.1
      x = (y - b + k + c[1]) / (-m) + c[0]
      p1 = (x, y)
    elif abs(m) <= 1:
      x = -0.1
      y = -m * (x - c[0]) + b - k - c[1]
      p0 = (x, y)

      x = a + 0.1
      y = -m * (x - c[0]) + b - k - c[1]
      p1 = (x, y)

  # Scaling the reference frame to the image frame.
  p0 = (int(round(p0[0] * width)), int(round(p0[1] * width)))
  p1 = (int(round(p1[0] * width)), int(round(p1[1] * width)))

  return p0, p1

if __name__ == '__main__': #pragma: no cover
  import DrixUtilities.Runner as Runner
  Runner.Runner().run(runFunction=None)

