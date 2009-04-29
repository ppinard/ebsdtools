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
import java.io

# Third party modules.
import rmlimage.io.IO as IO
import rmlimage.kernel as kernel
import rmlimage.macro.python.cui.EBSD as EBSD
import rmlimage.macro.python.cui.Analysis as Analysis
import rmlimage.macro.python.cui.MapMath as MapMath
import rmlimage.macro.command.cui.Filter as Filter
import rmlimage.kernel.Contrast as Contrast
import rmlshared.math.Stats as Stats

# Local modules.
import RandomUtilities.sort.sortDict as sortDict

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
  
  def calculateHough(self, angleIncrement=0.5, maskMap=None):
    """
    Calculate the Hough Transform. 
    
    A median and a contrast expansion is performed before doing the Hough transform.
    
    :arg angleIncrement: angle increment (in deg)
    :type angleIncrement: float
    
    :arg maskMap: binary map of a mask to be applied to the diffraction pattern before doing the Hough transform
    :type maskMap: :class:`BinMap <rmlimage.kernel.BinMap>`
    """
    
    if maskMap != None:
      assert maskMap.type == 'BinMap'
      assert self._map.size == maskMap.size
      
      self._maskMap = kernel.ByteMap(self._map.width, self._map.height)
      MapMath.andOp(self._map, maskMap, self._maskMap)
    else:
      self._maskMap = self._map
    
#    MapMath.subtraction(self._maskMap, 128, self._maskMap)
    Filter.median(self._maskMap)
    Contrast.expansion(self._maskMap)
    
    self._houghMap = EBSD.houghTransform(self._maskMap, angleIncrement*pi/180.0)
    
  
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
        houghPixelValue = self._houghMap.getPixValue(index)
        intensities[objectId-1].append(houghPixelValue)
    
    #Get centroid of peaks
    centroids = []
    centroidsXY = []
    
    xS, yS = Analysis.measureCentroid(identMap)
    for i in range(len(xS)):
      x = int(round(xS[i])); y = int(round(yS[i]))
      r = self._houghMap.getR(x, y)
      theta = self._houghMap.getTheta(x, y)
      
      centroids.append((r,theta))
      centroidsXY.append((x,y))
    
    #Get area of peaks
    areas = Analysis.measureArea(identMap)
    
    #Store information in self._peaks
    self._peaks = {}
    for objectId in range(0,identMap.getObjectCount()):
      averageIntensity = Stats.average(intensities[objectId])
      stdDevIntensity = Stats.standardDeviation(intensities[objectId])
      centroid = centroids[objectId]
      centroidXY = centroidsXY[objectId]
      area = areas[objectId]
      
      peak = {'intensity': {'average': averageIntensity, 'standard deviation': stdDevIntensity}
              , 'centroid': centroid
              , 'centroidXY': centroidXY
              , 'area': area}
      self._peaks[objectId] = peak
  
  def calculateImageQuality(self, numberPeaks=None):
    """
    Calculate the pattern quality.
    
    :arg numberPeaks: number of peaks to use in the calculation (``default=None``: use all)
    :type numberPeaks: int or ``None``
    
    **Equations:**
      :math:`\\mathrm{IQ} = \\frac{1}{N} \\sum\\limits_{i=0}^{N}{H(\\rho_i, \\theta_i)}`
    
    **References:**
      Wright2006
    """
    
    if self._peaks == None: self.findPeaks()
    
    peaks = []
    for peakId in self._peaks.keys():
      peaks.append(self._peaks[peakId]['intensity'])
    
    peaks =sortDict.sortListByKey(peaks, 'average', reverse=True)
    if numberPeaks == None or numberPeaks > len(peaks): 
      numberPeaks = len(peaks)
    
    IQ = 0
    IQerr = 0
    
    for peakId in range(numberPeaks):
      IQ += peaks[peakId]['average']
      IQerr += peaks[peakId]['standard deviation']
    
    if len(self._peaks) > 0:
      IQ /= numberPeaks
      IQerr /= numberPeaks
    
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
  
  maskMap.setFile(r'i:\philippe pinard\workspace\DeformationSamplePrep\maskk.bmp')
  
  IO.save(maskMap)
  
  hough = Hough(r'i:\philippe pinard\workspace\DeformationSamplePrep\data\patterns\TiB_diamond-05_1_000005.jpg')

  print hough.calculateHough(maskMap=maskMap)
  hough.findPeaks()
  hough.calculateImageQuality(4)
  print hough.getImageQuality()

  
