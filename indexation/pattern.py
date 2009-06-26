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
import os
import java.io

# Third party modules.
import rmlimage
import rmlimage.io.IO as IO
import rmlimage.macro.python.cui.MapMath as MapMath

# Local modules.

class PatternMap(rmlimage.core.ByteMap):
  def __init__(self, filepath=None, byteMap=None, maskMap=None):
    """
    PatternMap class (inherit :class:`ByteMap <rmlimage.kernel.ByteMap>`

    Store the information related to an EBSD pattern.

    Two optional constructors:

      - from a file (bitmap)
      - from a :class:`ByteMap <rmlimage.kernel.ByteMap>`

    If a *maskMap* is given, the mask is apply to the pattern and to all subsequent calculations. For mask constructor, see :mod:`masks <EBSDTools.indexation.masks>`

    :arg filepath: file path of a bitmap file
    :type filepath: str

    :arg byteMap: byteMap of a pattern
    :type byteMap: :class:`ByteMap <rmlimage.kernel.ByteMap>`

    :arg maskMap: binary map of a mask to be applied to the diffraction pattern before doing the Hough transform
    :type maskMap: :class:`BinMap <rmlimage.kernel.BinMap>`
    """
    #Load map
    if filepath != None and byteMap == None:
      file = java.io.File(filepath)
      map = IO.load(file)

      if map.type == 'RGBMap':
        self.originalPattern = rmlimage.core.Transform.getBlueLayer(map)
      else:
        self.originalPattern = map
    elif filepath == None and byteMap != None:
      self.originalPattern = byteMap

    assert self.originalPattern.type == 'ByteMap'

    rmlimage.core.ByteMap.__init__(self, self.originalPattern.width, self.originalPattern.height, self.originalPattern.pixArray)

    #Apply mask
    self.maskMap = None
    self.applyMask(maskMap)

  def applyMask(self, maskMap=None):
    """
    Apply a mask on the original pattern

    :arg maskMap: binary map of a mask to be applied to the diffraction pattern before doing the Hough transform
    :type maskMap: :class:`BinMap <rmlimage.kernel.BinMap>`
    """
    if maskMap == None and self.maskMap == None: return

    if maskMap != None:
      self.maskMap = maskMap

    assert self.maskMap.getType() == 'BinMap'
    assert self.originalPattern.size == self.maskMap.size

    patternMapMask = rmlimage.core.ByteMap(self.originalPattern.width, self.originalPattern.height)
    MapMath.andOp(self.originalPattern, self.maskMap, patternMapMask)

    self = patternMapMask

  def getMaskMap(self):
    """
    Return the mask map used

    :rtype: :class:`BinMap <rmlimage.kernel.BinMap>` or ``None`` if no mask was applied
    """

    return self.maskMap

  def getOriginalPattern(self):
    """
    Return the original pattern before the mask was applied (if any)

    :rtype: :class:`ByteMap <rmlimage.kernel.ByteMap>`
    """

    return self.originalPattern

  def getType(self):
    """
    Override the class type to show that *PatternMap* inherits a *ByteMap*
    """

    return 'ByteMap'

if __name__ == '__main__':
  patt = PatternMap(filepath='testData/pattern1.bmp')

