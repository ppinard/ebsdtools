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
from math import pi, sin, cos

# Third party modules.
import numpy

# Local modules.
import matplotlibtools.figure as figure
import matplotlibtools.figurewx as figurewx

# Globals and constants variables.

def squarewave(x, f, b):
  r = 0

  for k in range(2):
    r += sin((2 * k - 1) * 2 * pi * f * x) / (2 * k - 1)

  return 4 / pi * r

def squarewave2(x, f, b):
  r = cos(x)

  if r < 0:
    return - 1
  else:
    return 1

def sinc(x, f):

  try:
    r = sin(f * pi * x) / (f * pi * x)
  except ZeroDivisionError:
    r = 0

  if r > 0.0:
    r = 1

  return r

def graph():
  thickness = 4
  f = thickness / 4.0
  b = 0
  print 2 * pi * f

  fig = figurewx.FigureWx()

  xs = numpy.arange(-thickness / 2, thickness / 2, 0.1)
#  ys = []
#  for x in xs:
#    ys.append(squarewave2(x, 1.0 / f, b))
#
#  fig.add_serie_scatter(x=xs, y=ys)
#
  ys = []
  for x in xs:
    ys.append(sinc(x, f))

  marker = figure.marker_params(ms=0)
  fig.add_serie_scatter(x=xs, y=ys, params_marker=marker)
#
#  ys = []
#  for x in xs:
#    y = sinc(x, f, b) + squarewave2(x, 1.0 / f, b)
#    ys.append(y)
#
#  fig.add_serie_scatter(x=xs, y=ys)


  fig.script_axis(subplot_id=1
                  , axis_id='ax1'
                  , scripttext='axhline(y=0.0)')


  fig.show()

if __name__ == '__main__': #pragma: no cover
  import DrixUtilities.Runner as Runner
  Runner.Runner().run(runFunction=graph)

