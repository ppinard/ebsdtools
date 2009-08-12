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

# Local modules.

# Interfaces
import rmlimage.module.ebsd.python.interfaces

class MaskMap(rmlimage.core.BinMap):
  def __init__(self, width, height, *args):
    """
    MaskMap class (inherit :class:`BinMap <rmlimage.kernel.BinMap>`

    :arg width: width of the mask map
    :type width: int

    :arg height: width of the mask map
    :type height: int
    """
    rmlimage.core.BinMap.__init__(self, width, height, *args)

  def getType(self):
    """
    Override the class type to show that *MaskMap* inherits a *BinMap*
    """
    return 'BinMap'

  def getbinmap(self):
    """
    Return the *BinMap*.
    """
    return self

class MaskDisc(MaskMap, rmlimage.module.ebsd.python.interfaces.MaskDisc):
  def __init__(self, width, height, centroid_x, centroid_y, radius):
    """
    A circular mask

    :arg width: width of the mask map
    :type width: :keyword:`int`

    :arg height: width of the mask map
    :type height: :keyword:`int`

    :arg centroid_x: x position in pixels of the center of the disc
    :type centroid_x: :keyword:`int`

    :arg centroid_y: y position in pixels of the center of the disc
    :type centroid_y: :keyword:`int`

    :arg radius: radius of the disc in pixels
    :type radius: :keyword:`int`
    """
    self._centroid_x = centroid_x
    self._centroid_y = centroid_y
    self._radius = radius

    pixarray = []
    for y in range(height):
      for x in range(width):
        if (x - centroid_x)**2 + (y - centroid_y)**2 < radius**2:
          pixarray.append(1)
        else:
          pixarray.append(0)

    MaskMap.__init__(self, width, height, pixarray)

  def getradius(self):
    """
    Return the radius of the circle

    :rtype: :keyword:`int
    """
    return self._radius

  def getcentroid_x(self):
    """
    Return the x coordinate of the centroid of the circle

    :rtype: :keyword:`int`
    """
    return self._centroid_x

  def getcentroid_y(self):
    """
    Return the y coordinate of the centroid of the circle

    :rtype: :keyword:`int`
    """
    return self._centroid_y

  def getcentroid(self):
    """
    Return the centroid of the circle

    :rtype: :keyword:`tuple`
    """
    return self._centroid_x, self._centroid_y
