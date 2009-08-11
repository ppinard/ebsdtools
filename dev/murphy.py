#!/usr/bin/env jython
""" """

# Script information for the file.
__author__ = "Philippe Pinard (philippe.pinard@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2009 Philippe Pinard"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = ""
__svnDate__ = ""
__svnId__ = ""

# Standard library modules.
import sys
import os
import copy
import platform
from math import sqrt

# Third party modules.

# Local modules.
import rmlimage
import rmlimage.module.real as real

# Globals and constants variables.


def _bresenham_loop_lowslope(binMap, start_x, start_y, end_x, end_y):
  """
  Loop for abs(delta_y) <= abs(delta_x)
  Slope less than 1.
  """
  start_x, start_y, end_x, end_y = \
    _positive_deltax(start_x, start_y, end_x, end_y)

  delta_x = end_x - start_x
  delta_y = end_y - start_y

  if end_y >= start_y:
    square_shift = 2 * delta_y
    diagonal_shift = 2 * (delta_y - delta_x)
    threshold = 2*delta_y - delta_x #Threshold between square and diagonal shift

    x = start_x
    y = start_y
    binMap.setPixValue(x, y, 1)
    while x < end_x:
      if threshold <= 0:
        threshold += square_shift
        x += 1
      else:
        threshold += diagonal_shift
        x += 1
        y += 1

      binMap.setPixValue(x, y, 1)
  else: # end_y < start_y
    square_shift = 2 * delta_y
    diagonal_shift = 2 * (delta_y + delta_x)
    threshold = 2*delta_y + delta_x #Threshold between square and diagonal shift

    x = start_x
    y = start_y
    binMap.setPixValue(x, y, 1)
    while x < end_x:
      if threshold >= 0:
        threshold += square_shift
        x += 1
      else:
        threshold += diagonal_shift
        x += 1
        y -= 1

      binMap.setPixValue(x, y, 1)

def _bresenham_loop_highslope(binMap, start_x, start_y, end_x, end_y):
  """
  Loop for abs(delta_y) > abs(delta_x)
  Slope greater than 1.
  """
  tmp = end_x
  end_x = end_y
  end_y = tmp

  tmp = start_x
  start_x = start_y
  start_y = tmp

  start_x, start_y, end_x, end_y = \
    _positive_deltax(start_x, start_y, end_x, end_y)

  delta_x = end_x - start_x
  delta_y = end_y - start_y

  if end_y >= start_y:
    square_shift = 2 * delta_y
    diagonal_shift = 2 * (delta_y - delta_x)
    threshold = 2*delta_y - delta_x #Threshold between square and diagonal shift

    x = start_x
    y = start_y
    binMap.setPixValue(y, x, 1) #inverse
    while x < end_x:
      if threshold <= 0:
        threshold += square_shift
        x += 1
      else:
        threshold += diagonal_shift
        x += 1
        y += 1

      binMap.setPixValue(y, x, 1) #inverse
  else: # end_y < start_y
    square_shift = 2 * delta_y
    diagonal_shift = 2 * (delta_y + delta_x)
    threshold = 2*delta_y + delta_x #Threshold between square and diagonal shift

    x = start_x
    y = start_y
    binMap.setPixValue(y, x, 1) #inverse
    while x < end_x:
      if threshold >= 0:
        threshold += square_shift
        x += 1
      else:
        threshold += diagonal_shift
        x += 1
        y -= 1

      binMap.setPixValue(y, x, 1) #inverse

def _perpendicular(binMap
                   , x, y
                   , parity
                   , diff_para, diff_perp, threshold
                   , square_shift_para, square_shift_perp
                   , diagonal_shift_para, diagonal_shift_perp
                   , thickness):
  _perp(binMap, x, y, parity
        , -diff_para, diff_perp*parity
        , threshold, square_shift_para, square_shift_perp, diagonal_shift_para, diagonal_shift_perp, thickness)

#  _perp2(binMap, x, y, parity
#        , diff_para, -diff_perp*parity
#        , threshold, square_shift_para, square_shift_perp, diagonal_shift_para, diagonal_shift_perp, thickness)

def _perp(binMap
                   , x, y
                   , parity
                   , diff_para, diff_perp, threshold
                   , square_shift_para, square_shift_perp
                   , diagonal_shift_para, diagonal_shift_perp
                   , thickness):
  while diff_para <= thickness:
#    if diff_para < 0:
    setPixValue(binMap, x, y)

    if diff_perp < threshold: #Square move
      y += 1
      diff_perp += square_shift_perp
      diff_para += square_shift_para
    else: #diagonal move
      x -= 1
      y += 1
      diff_perp += diagonal_shift_para
      diff_para += diagonal_shift_perp

def _perp2(binMap
                   , x, y
                   , parity
                   , diff_para, diff_perp, threshold
                   , square_shift_para, square_shift_perp
                   , diagonal_shift_para, diagonal_shift_perp
                   , thickness):
  while diff_para <= thickness:
#    if diff_para < 0:
    setPixValue(binMap, x, y)

    if diff_perp < threshold: #Square move
      y -= 1
      diff_perp += square_shift_perp
      diff_para += square_shift_para
    else: #diagonal move
      x += 1
      y -= 1
      diff_perp += diagonal_shift_para
      diff_para += diagonal_shift_perp


def _murphy_loop(binMap, start_x, start_y, end_x, end_y, thickness):
  """
  Loop for abs(delta_y) <= abs(delta_x)
  Slope less than 1.
  """
#  start_x, start_y, end_x, end_y = \
#    _positive_deltax(start_x, start_y, end_x, end_y)

  if start_x > end_x:
    start_x, end_x = swap(start_x, end_x)
    start_y, end_y = swap(start_y, end_y)

  delta_x = end_x - start_x #u
  delta_y = end_y - start_y #v

  normalization_constant = sqrt(delta_x**2 + delta_y**2)
  thickness = 2.0*thickness*normalization_constant
  print 'thickness', thickness

  diff_para = 0 #d0
  diff_perp = 0 #d1

  square_shift_para = 2*delta_x #ku
  square_shift_perp = 2*delta_y #kv
  diagonal_shift_para = 2*(delta_y - delta_x) #kd
  diagonal_shift_perp = 2*(delta_y + delta_x) #ks
  threshold = delta_x - 2*delta_y #kt

  if start_y <= end_y:
    parity = 1
  else:
    parity = -1

  count_x = 0
  count_y = 0
  x = start_x
  y = start_y

  print start_x, start_y, end_x, end_y, parity

  while count_x <= delta_x:
    _perpendicular(binMap, x, y, parity, diff_para, diff_perp, threshold, square_shift_para, square_shift_perp, diagonal_shift_para, diagonal_shift_perp, thickness)

    if diff_para < threshold:
      x += 1
    else:
      diff_para -= square_shift_para
      if diff_perp < threshold: #normal start
        diff_perp += square_shift_perp
        x += 1
        y += 1
      else: #double square move (need extra perpendicular)
        y += parity
        diff_perp += diagonal_shift_para
        _perpendicular(binMap, x, y, parity, diff_para, diff_perp, threshold, square_shift_para, square_shift_perp, diagonal_shift_para, diagonal_shift_perp, thickness)
        x += 1
    diff_para += square_shift_perp
    count_x += 1

def _positive_deltax(start_x, start_y, end_x, end_y):
  delta_x = end_x - start_x
  if delta_x < 0:
    tmp = start_x
    start_x = end_x
    end_x = tmp

  return start_x, start_y, end_x, end_y

def swap(a, b):
  tmp = a
  a = b
  b = tmp

  return a, b

def setPixValue(binMap, x, y):
  if x >= 0 and x < binMap.width and y >= 0 and y < binMap.height:
    value = binMap.getPixValue(x, y)
    binMap.setPixValue(x, y, 1)

def bresenham(binMap, start_x, start_y, end_x, end_y, thickness, recursive=True):
  steep = abs(end_y - start_y) > abs(end_x - start_x)
  if steep:
    start_x, start_y = swap(start_x, start_y)
    end_x, end_y = swap(end_x, end_y)

  if start_x > end_x:
    start_x, end_x = swap(start_x, end_x)
    start_y, end_y = swap(start_y, end_y)

  deltax = end_x - start_x
  deltay = abs(end_y - start_y)
  errorx = deltax / 2
  y = start_y

  try:
    slope = -1.0 / (float(end_y - start_y) / float(end_x - start_x))
  except ZeroDivisionError:
    slope = 1e99
  thickness_step = sqrt(thickness**2 / (1.0 + slope**2))
#  print slope, thickness_step

  if start_y < end_y:
    ystep = 1
  else:
    ystep = -1

  for x in range(start_x, end_x+1):
    if recursive:
      x0 = x + thickness_step
      x1 = x - thickness_step
      y0 = y - slope*(x - x0)
      y1 = y - slope*(x - x1)
#      print x0, y0, x1, y1
      bresenham(binMap, int(x1), int(y1), int(x0), int(y0), thickness, recursive=False)

    if steep:
      setPixValue(binMap, y, x)
    else:
      setPixValue(binMap, x, y)

    errorx -= deltay

    if errorx < 0:
      y += ystep
      errorx += deltax

      if recursive:
        x0 = x + thickness_step
        x1 = x - thickness_step
        y0 = y - slope*(x - x0)
        y1 = y - slope*(x - x1)
        bresenham(binMap, int(x1), int(y1), int(x0), int(y0), thickness, recursive=False)


def bresenham_thin_line(binMap, start_x, start_y, end_x, end_y):
  """
  Algorithm to draw thin line from the Bresenham line algorithm.

  Reference:
  Andrew Diamond (http://www.mathworks.com/matlabcentral/fileexchange/1929)
  """
  delta_x = end_x - start_x #u
  delta_y = end_y - start_y #v
  print delta_x, delta_y

  if abs(delta_y) <= abs(delta_x):
    print "abs(delta_y) <= abs(delta_x)"
    _bresenham_loop_lowslope(binMap, start_x, start_y, end_x, end_y)
  else: #abs(delta_y) > abs(delta_x)
    print "abs(delta_y) > abs(delta_x)"
    _bresenham_loop_highslope(binMap, start_x, start_y, end_x, end_y)

def murphy_thick_line(binMap, start_x, start_y, end_x, end_y, thickness):

  _murphy_loop(binMap, start_x, start_y, end_x, end_y, thickness)


realMap = real.core.RealMap(2000,2000)

#bresenham(realMap, 5, 5, 15, 5, 5)
#bresenham(binMap, 20, 20, 0, 0)
#bresenham(binMap, 0, 20, 20, 0)
#bresenham(binMap, 20, 0, 0, 20)
#
#bresenham(binMap, 0, 0, 10, 20)
#bresenham(binMap, 10, 20, 0, 0)
#bresenham(binMap, 0, 20, 10, 0)
#bresenham(binMap, 10, 0, 0, 20)

#murphy_thick_line(realMap, 5, 5, 1500, 900, 0)
#murphy_thick_line(realMap, 1999, 900, 5, 5, 0)
#murphy_thick_line(realMap, 1500, 5, 5, 900, 0)
#murphy_thick_line(realMap, 5, 900, 1999, 5, 90)

bresenham(realMap, 5, 5, 1500, 900, 90)
#bresenham(realMap, 1999, 900, 5, 5, 90)
#bresenham(realMap, 1500, 5, 5, 900, 90)
#bresenham(realMap, 5, 900, 1999, 5, 90)

bresenham(realMap, 500, 5, 500, 900, 90)

#murphy_thick_line(realMap, 5, 1999, 1999, 1000, 90)



byteMap = real.core.Contrast.expansion(realMap)
byteMap.setFile('test.bmp')
rmlimage.io.IO.save(byteMap)
