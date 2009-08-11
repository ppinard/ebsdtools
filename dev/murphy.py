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


def swap(a, b):
  tmp = a
  a = b
  b = tmp

  return a, b

def setPixValue(binMap, x, y):
  if x >= 0 and x < binMap.width and y >= 0 and y < binMap.height:
    value = binMap.getPixValue(x, y)
    binMap.setPixValue(x, y, 1)

def bresenham_mod_thick_line(map, start_x, start_y, end_x, end_y, thickness):
  """
  Draw line with a certain *thickness*

  :arg map: map where to draw the line
  :arg start_x: x coordinate of the start point of the line
  :arg start_y: y coordinate of the start point of the line
  :arg end_x: x coordinate of the end point of the line
  :arg end_y: y coordinate of the end point of the line
  :arg thickness: thickness of the line

  Algorithm is an adaptation of Murphy's line algorithm
  and Bresenham's line algorithm (wikipedia).
  """
  _bresenham_loop(map, start_x, start_y, end_x, end_y, thickness, recursive=False)

def _bresenham_loop(map, start_x, start_y, end_x, end_y, thickness, recursive=False):
  """
  :arg recursive: *True* when the function is in a recursive loop
  """
  #Initialisation of start and end points
  #depending on slope and initial points
  steep = abs(end_y - start_y) > abs(end_x - start_x)
  if steep:
    start_x, start_y = swap(start_x, start_y)
    end_x, end_y = swap(end_x, end_y)

  if start_x > end_x:
    start_x, end_x = swap(start_x, end_x)
    start_y, end_y = swap(start_y, end_y)

  if start_y < end_y:
    ystep = 1
  else:
    ystep = -1

  #Values for step and diagonal moves
  deltax = end_x - start_x
  deltay = abs(end_y - start_y)
  #Error between the ideal and drawn line
  error = deltax / 2

  #Find the slope of the perpendicular to the line
  #The step in x requires to reach the border of the line
  #is given by *thickness_xstep*
  if not recursive:
    try:
      slope = -float(end_x - start_x) / float(end_y - start_y)
    except ZeroDivisionError:
      slope = None
      thickness_xstep = 0
    else:
      thickness_xstep = sqrt(thickness**2 / (1.0 + slope**2))

  #Loop over all x
  y = start_y
  for x in range(start_x, end_x+1):
    #Draw perpendicular to the line
    if not recursive:
      x0 = x + thickness_xstep
      x1 = x - thickness_xstep
      if slope == None:
        y0 = y + thickness
        y1 = y - thickness
      else:
        y0 = y - slope*(x - x0)
        y1 = y - slope*(x - x1)

      if steep:
        _bresenham_loop(map, int(y1), int(x1), int(y0), int(x0), thickness, recursive=True)
      else:
        _bresenham_loop(map, int(x1), int(y1), int(x0), int(y0), thickness, recursive=True)

    #Draw pixel in map
    if steep:
      setPixValue(map, y, x)
    else:
      setPixValue(map, x, y)

    error -= deltay
    #If error is less than 0, make a step in y
    #The line can no longer be horizontal, since it's deviation
    #from the ideal line is too great.
    if error < 0:
      y += ystep
      error += deltax

      #Draw perpendicular to the line for the added pixel
      if not recursive:
        x0 = x + thickness_xstep
        x1 = x - thickness_xstep
        if slope == None:
          y0 = y + thickness
          y1 = y - thickness
        else:
          y0 = y - slope*(x - x0)
          y1 = y - slope*(x - x1)

        if steep:
          _bresenham_loop(map, int(y1), int(x1), int(y0), int(x0), thickness, recursive=True)
        else:
          _bresenham_loop(map, int(x1), int(y1), int(x0), int(y0), thickness, recursive=True)


def main():
  realMap = real.core.RealMap(2001,2001)

  bresenham_mod_thick_line(realMap, 5, 5, 1500, 900, 30)
  bresenham_mod_thick_line(realMap, 1999, 900, 5, 5, 30)
  bresenham_mod_thick_line(realMap, 1500, 5, 5, 900, 30)
  bresenham_mod_thick_line(realMap, 5, 900, 1999, 5, 90)

  bresenham_mod_thick_line(realMap, 500, 5, 500, 900, 30)
  bresenham_mod_thick_line(realMap, 5, 1500, 900, 1500, 60)

  byteMap = real.core.Contrast.expansion(realMap)
  byteMap.setFile('test.bmp')
  rmlimage.io.IO.save(byteMap)

if __name__ == '__main__':
  main()
