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
import rmlimage.io.IO as IO
import rmlimage.kernel as kernel
import rmlshared.math.Stats as Stats

# Local modules.

class Pattern:
  def __init__(self, filepath=None, byteMap=None):
    """
    Pattern class
    
    Two optional constructors: 
    
      - from a file (bitmap)
      - from a :class:`ByteMap <rmlimage.kernel.ByteMap>`
      
    :arg filepath: file path of a bitmap file
    :type filepath: str
    
    :arg byteMap: byteMap of a pattern
    :type byteMap: :class:`ByteMap <rmlimage.kernel.ByteMap>`
    """
    if filepath != None and byteMap == None:
      file = java.io.File(filepath)
      map = IO.load(file)
      if map.type == 'RGBMap':
        self.patternMap = kernel.Transform.getBlueLayer(map)
      else:
        self.patternMap = map
    elif filepath == None and byteMap != None:
      self.patternMap = byteMap
    
    assert self.patternMap.type == 'ByteMap'
    
    self.height = self.patternMap.height
    self.width = self.patternMap.width
    
    self._mean = None
    self._stddev = None
    
  def calculateStatistics(self, maskMap=None):
    """
    Calculate the mean and standard deviation
    
    A mask can be applied before calculating the mean
    
    :arg maskMap: binary map of a mask to be applied to the diffraction pattern before doing the Hough transform
    :type maskMap: :class:`BinMap <rmlimage.kernel.BinMap>`
    """
    if maskMap != None:
      assert maskMap.type == 'BinMap'
      assert self.patternMap.size == maskMap.size
      
      currentMap = kernel.ByteMap(self.patternMap.width, self.patternMap.height)
      MapMath.andOp(self.patternMap, maskMap, currentMap)
    else:
      currentMap = self.patternMap
    
    values = []
    for index in range(currentMap.size):
      value = currentMap.getPixValue(index)
      if value > 0:
        values.append(value)
    
    self._mean = Stats.average(values)
    self._stddev = Stats.standardDeviation(values)
  
  def getMean(self):
    """
    Return the mean of the pattern
    
    :rtype: float
    """
    if self._mean == None: self.calculateStatistics()
    
    return self._mean
  
  def getStandardDeviation(self):
    """
    Return the mean of the pattern
    
    :rtype: float
    """
    if self._stddev == None: self.calculateStatistics()
    
    return self._stddev
  
  getStdDev = getStandardDeviation
  
if __name__ == '__main__':
  pattern = Pattern(filepath='testData/pattern1.bmp')
  pattern.calculateStatistics(maskMap=None)
  
  print pattern.getMean(), pattern.getStandardDeviation()