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
from math import sqrt

# Third party modules.

# Local modules.
import rmlimage
import rmlimage.module.real as real

# Globals and constants variables.

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

  _perp2(binMap, x, y, parity
        , diff_para, -diff_perp*parity
        , threshold, square_shift_para, square_shift_perp, diagonal_shift_para, diagonal_shift_perp, thickness)

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

  return start_x, start_y, end_x, end_y

def setPixValue(binMap, x, y):
  if x >= 0 and x < binMap.width and y >= 0 and y < binMap.height:
    value = binMap.getPixValue(x, y)
    binMap.setPixValue(x, y, 1)

def murphy_thick_line(binMap, start_x, start_y, end_x, end_y, thickness):

  _murphy_loop(binMap, start_x, start_y, end_x, end_y, thickness)

def main():
  realMap = real.core.RealMap(2001,2001)

  murphy_thick_line(realMap, 5, 5, 1500, 900, 30)

  byteMap = real.core.Contrast.expansion(realMap)
  byteMap.setFile('test.bmp')
  rmlimage.io.IO.save(byteMap)

if __name__ == '__main__':
  main()
