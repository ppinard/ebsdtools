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
import rmlimage
import rmlimage.kernel as kernel

# Local modules.

class MaskMap(rmlimage.kernel.BinMap):
  def __init__(self, width, height, *args):
    """
    MaskMap class (inherit :class:`BinMap <rmlimage.kernel.BinMap>`
    
    :arg width: width of the mask map
    :type width: int
    
    :arg height: width of the mask map
    :type height: int
    """
    
    rmlimage.kernel.BinMap.__init__(self, width, height, *args)
  
  def getType(self):
    """
    Override the class type to show that *MaskMap* inherits a *BinMap*
    """
    
    return 'BinMap'
  
class MaskDisc(MaskMap):
  def __init__(self, width, height, centroid, radius):
    """
    A circular mask
    
    :arg width: width of the mask map
    :type width: int
    
    :arg height: width of the mask map
    :type height: int
    
    :arg centroid: position in pixels of the center of the disc (x,y)
    :type centroid: tuple of int
    
    :arg radius: radius of the disc in pixels
    :type radius: int
    """
    
    self.centroid = centroid
    self.radius = radius
    
    pixArray = []
    for y in range(height):
      for x in range(width):
        if (x - centroid[0])**2 + (y - centroid[1])**2 < radius**2:
          pixArray.append(1)
        else:
          pixArray.append(0)
    
    MaskMap.__init__(self, width, height, pixArray)
  
  def getRadius(self):
    """
    Return the radius of the circle
    
    :rtype: int
    """
    
    return self.radius
  
  def getCentroid(self):
    """
    Return the centroid of the circle
    
    :rtype: tuple of int
    """
    
    return self.centroid
  
if __name__ == '__main__':
  import rmlimage.io.IO as IO
  mask1 = MaskDisc(168, 128, (84, 64), 59)
  mask1.setFile('test.bmp')
  IO.save(mask1)
  print mask1.height