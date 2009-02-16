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

# Third party modules.
import rmlimage.io.IO as IO
import rmlimage.kernel as kernel

# Local modules.

class image:
  def __init__(self, byteMap):
    self._map = byteMap
  
  def within(self, x, y):
    if x >= 0 and x <= self._map.width and \
       y >= 0 and y <= self._map.height:
      return True
    else:
      return False
  
  def getPixel(self, x, y):
    return self._map.getPixValue(x,y)
  
  def setPixel(self, x, y, value):
    self._map.setPixValue(x, y, value)
  
  def getMap(self):
    return self._map
  

def within(im, x, y):
  if x >= 0 and x <= im.width and \
     y >= 0 and y <= im.height:
    return True
  else:
    return False

def flood_fill(im, x, y, value):
  "Flood fill on a region of non-BORDER_COLOR pixels."
  BORDER_COLOR = 0
  
  if not within(im, x, y) or im.getPixValue(x, y) == BORDER_COLOR:
    return
  
  edge = [(x, y)]
  im.setPixValue(x, y, value)
  
  while edge:
    newedge = []
    for (x, y) in edge:
      for (s, t) in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
        if within(im, s, t) and \
          im.getPixValue(s, t) not in (BORDER_COLOR, value):
            im.setPixValue(s, t, value)
            newedge.append((s, t))
    edge = newedge
  
if __name__ == '__main__':
  
  map = kernel.ByteMap(9, 9)
  
  pixArray = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
  for index, pix in enumerate(pixArray):
    if pix == 1:
      map.setPixValue(index, 0)
    else:
      map.setPixValue(index, 255)
  
#  map.setFile('seedfill.bmp')
#  IO.save(map)
  
  for x in range(9):
    for y in range(9):
      flood_fill(map, x, y, 128)  
  
  map.setFile('seedfilled.bmp')
  IO.save(map)
