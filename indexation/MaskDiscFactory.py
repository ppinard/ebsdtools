#!/usr/bin/env jython
""" """

# Script information for the file.
__author__ = "Philippe Pinard (philippe.pinard@gmail.com)"
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
import java
import rmlimage.module.ebsd.python.interfaces
import EBSDTools.indexation.masks as masks


# Globals and constants variables.
class MaskDiscFactory(java.lang.Object, rmlimage.module.ebsd.python.interfaces.MaskDiscFactory):

  def create(self, width, height, centroidX, centroidY, radius):
    """
    Create a circular mask for a pattern size of *size* centered at *centroid*
    with a given *radius*

    :arg size: dimensions of the mask (width, height)
    :type size: tuple

    :arg centroid: position in pixels of the center of the disc (x,y)
    :type centroid: tuple

    :arg radius: radius of the disc in pixels
    :type radius: int

    :rtype: :class:`BinMap <rmlimage.kernel.BinMap>`
    """

    return masks.MaskDisc(width, height, centroidX, centroidY, radius)

if __name__ == '__main__':
  factory = MaskDiscFactory()
  binMap = factory.create(100, 100, 0, 0, 50)
  print binMap.height
