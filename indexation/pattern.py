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
import rmlimage.macro.python.cui.MapMath as MapMath

# Local modules.

class Pattern:
  def __init__(self, filepath=None, byteMap=None, maskMap=None):
    """
    Pattern class
    
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
        patternMap = kernel.Transform.getBlueLayer(map)
      else:
        patternMap = map
    elif filepath == None and byteMap != None:
      patternMap = byteMap
    
    assert patternMap.type == 'ByteMap'
    
    #Apply mask
    if maskMap != None:
      assert maskMap.type == 'BinMap'
      assert patternMap.size == maskMap.size
      
      patternMapMask = kernel.ByteMap(patternMap.width, patternMap.height)
      MapMath.andOp(patternMap, maskMap, patternMapMask)
      
      self.patternMap = patternMapMask
    else:
      self.patternMap = patternMap
    
    #Dimensions
    self.height = self.patternMap.height
    self.width = self.patternMap.width
    
    #Undefined results
    self._mean = None
    self._stddev = None
  
  def getPattern(self):
    """
    Return the loaded pattern as a ByteMap
    
    :rtype: :class:`ByteMap <rmlimage.kernel.ByteMap>`
    
    .. note:: the pattern can also be access using the class variable *patternMap*.
    """
    return self.patternMap
  
  def calculateStatistics(self):
    """
    Calculate the mean and standard deviation
    """
    values = []
    for index in range(self.patternMap.size):
      value = self.patternMap.getPixValue(index)
      if value > 0: #Ignore pixel with 0 value since they are outside the mask
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
  pattern.calculateStatistics()
  
  print pattern.getMean(), pattern.getStandardDeviation()