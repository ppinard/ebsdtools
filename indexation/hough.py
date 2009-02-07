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
from math import pi
if os.name == 'java': import java.io

# Third party modules.
if os.name == 'java':
  import rmlimage.io.IO as IO
  import rmlimage.kernel as kernel
  import rmlimage.macro.python.cui.EBSD as EBSD
  import rmlimage.macro.command.cui.Analysis as Analysis
  import rmlimage.macro.command.cui.MapMath as MapMath
  import rmlshared.math.Stats as Stats

# Local modules.

def createMaskDisc(width, height, centroid, radius):
  """
  Create a circular mask for a pattern size of *size* centered at *centroid* with a given *radius*
  
  :arg size: dimensions of the mask (width, height)
  :type size: tuple
  
  :arg centroid: position in pixels of the center of the disc (x,y)
  :type centroid: tuple
  
  :arg radius: radius of the disc in pixels
  :type radius: int
  
  :rtype: :class:`BinMap <rmlimage.kernel.BinMap>`
  """
  pixArray = []
  
  for y in range(height):
    for x in range(width):
      if (x - centroid[0])**2 + (y - centroid[1])**2 < radius**2:
        pixArray.append(1)
      else:
        pixArray.append(0)
  
  binMap = kernel.BinMap(width, height, pixArray)
  
  return binMap

class Hough:
  def __init__(self, filepath):
    file = java.io.File(filepath)
    map = IO.load(file)
    if map.type == 'RGBMap':
      self._map = kernel.Transform.getBlueLayer(map)
    else:
      self._map = map
    
    assert self._map.type == 'ByteMap'
    
    self.height = self._map.height
    self.width = self._map.width
    
    self._houghMap = None
    self._peaks = None
    self._IQ = None
  
  def calculateHough(self, angleIncrement=0.5, maskMap = None):
    """
    Calculate the Hough Transform
    
    :arg angleIncrement: angle increment (in deg)
    :type angleIncrement: float
    
    :arg maskMap: binary map of a mask to be applied to the diffraction pattern before doing the Hough transform
    :type maskMap: :class:`BinMap <rmlimage.kernel.BinMap>`
    """
    
    if maskMap != None:
      assert maskMap.type == 'BinMap'
      assert self._map.size == maskMap.size
      
      newMap = kernel.ByteMap(self._map.width, self._map.height)
      MapMath.and(self._map, maskMap, newMap)
      
      self._houghMap = EBSD.houghTransform(newMap, angleIncrement*pi/180.0)
    else:
      self._houghMap = EBSD.houghTransform(self._map, angleIncrement*pi/180.0)
  
  def findPeaks(self):
    """
    Find the peaks in the Hough transform with the classic Top Hat thresholding
    """
    
    if self._houghMap == None: self.calculateHough()
    
    #Get peaks from Hough
    peaksMap = EBSD.houghThresholding(self._houghMap)
    identMap = Analysis.identify(peaksMap)
    assert self._houghMap.size == identMap.size
    
    #Get intensities of peaks from Hough Transform
    intensities = {}
    for objectId in range(0,identMap.getObjectCount()):
      intensities[objectId] = []
    
    for index in range(identMap.size):
      objectId = identMap.pixArray[index]
      if objectId > 0:
        houghPixelValue = abs(self._houghMap.pixArray[index])
        intensities[objectId-1].append(houghPixelValue)
    
    #Get centroid of peaks
    centroids = []
    
    xS, yS = Analysis.measureCentroid(identMap)
    for i in range(len(xS)):
      x = int(round(xS[i])); y = int(round(yS[i]))
      r = self._houghMap.getR(x, y)
      theta = self._houghMap.getTheta(x, y)
      
      centroids.append((r,theta))
    
    #Get area of peaks
    areas = Analysis.measureArea(identMap)
    
    #Store information in self._peaks
    self._peaks = {}
    for objectId in range(0,identMap.getObjectCount()):
      averageIntensity = Stats.average(intensities[objectId])
      stdDevIntensity = Stats.standardDeviation(intensities[objectId])
      centroidX = centroids[objectId]
      centroidY = centroids[objectId]
      area = areas[objectId]
      
      peak = {'intensity': {'average': averageIntensity, 'standard deviation': stdDevIntensity}
              , 'centroid': (centroidX, centroidY)
              , 'area': area}
      self._peaks[objectId] = peak
  
  def calculateImageQuality(self):
    """
    Calculate the pattern quality.
    
    **Equations:**
      :math:`\\mathrm{IQ} = \\frac{1}{N} \\sum\\limits_{i=0}^{N}{H(\\rho_i, \\theta_i)}`
    
    **References:**
      Wright2006
    """
    
    if self._peaks == None: self.findPeaks()
    
    IQ = 0
    IQerr = 0
    
    for peakId in self._peaks.keys():
      IQ += self._peaks[peakId]['intensity']['average']
      IQerr += self._peaks[peakId]['intensity']['standard deviation']
    
    if len(self._peaks) > 0:
      IQ /= len(self._peaks)
      IQerr /= len(self._peaks)
    
    self._IQ = (IQ, IQerr)
  
  def getHoughMap(self):
    """
    Return the HoughMap object
    
    :rtype: :class:`HoughMap <rmlimage.plugin.ebsd.HoughMap>`
    """
    
    if self._houghMap == None: self.calculateHough()
    
    return self._houghMap
  
  def getPeaks(self):
    """
    Return the peaks dictionary containing:
    
    ==========   ====================================================
    key          Description
    ==========   ====================================================
    intensity    ``{'average': float, 'standard deviation': float}``
    centroid     (:math:`\\rho`, :math:`\\theta`)
    area         in pixels
    ==========   ====================================================
    
    :rtype: dict
    """
    
    if self._peaks == None: self.findPeaks()
    
    return self._peaks
  
  def getPeaksCount(self):
    """
    Return the number of detected peaks
    
    :rtype: int
    """
    if self._peaks == None: self.findPeaks()
    
    return len(self._peaks)
  
  def getPeakIntensity(self, peakId):
    """
    Return the average intensity of a peak
    
    :arg peakId: id of the peak
    :type peakId: int
    
    :rtype: float
    """
    if self._peaks == None: self.findPeaks()
    
    return self._peaks[peakId]['intensity']['average']
  
  def getPeakCentroid(self, peakId):
    """
    Return the centroid (:math:`\\rho`, :math:`\\theta`) of a peak
    
    :arg peakId: id of the peak
    :type peakId: int
    
    :rtype: tuple
    """
    if self._peaks == None: self.findPeaks()
    
    return self._peaks[peakId]['centroid']
  
  def getPeakArea(self, peakId):
    """
    Return the area of a peak in pixel
    
    :arg peakId: id of the peak
    :type peakId: int
    
    :rtype: float
    """
    if self._peaks == None: self.findPeaks()
    
    return self._peaks[peakId]['area']
  
  def getImageQuality(self):
    """
    Return the image quality and its error of the Hough Transform
    
    .. seealso:: :func:`calculateImageQuality <EBSDTools.indexation.hough.Hough.calculateImageQuality>`
    
    :rtype: tuple
    :return: (value, error) of the image quality
    """
    if self._IQ == None: self.calculateImageQuality()
    
    return self._IQ
  
  getIQ = getImageQuality

if __name__ == '__main__':
  """
  
  """
  
  maskMap = createMaskDisc(width=168, height=128, centroid=(84,64), radius=59)
  
  hough = Hough('i:/Philippe Pinard/workspace/DeformationSamplePrep/si_pattern.bmp')
  print hough.calculateHough(maskMap=maskMap)
  print hough.getPeaks()
  print hough.getImageQuality()

  
