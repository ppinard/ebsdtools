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

# Third party modules.
import rmlimage.io.IO as IO #To be removed
import rmlimage.kernel as kernel
import rmlimage.plugin.ebsd.Transform as Transform
import rmlimage.macro.python.cui.Analysis as Analysis
import rmlimage.macro.command.cui.Filter as Filter
import rmlimage.kernel.Contrast as Contrast
import rmlshared.math.Stats as Stats
import rmlimage.plugin.ebsd.Convolution as Convolution
import rmlimage.kernel.Kernel as Kernel
import rmlimage.kernel.MathMorph as MathMorph
import rmlimage.kernel.Edit as Edit
import rmlimage.kernel.Threshold as Threshold

# Local modules.
import RandomUtilities.sort.sortDict as sortDict

# Globals and constants variables.
FINDPEAKS_TOP_HAT         = 'tophat'
FINDPEAKS_BUTTERFLY       = 'butterfly'

class Hough:
  def __init__(self, pattern):
    """
    Create a Hough class
    
    :arg pattern: a pattern
    :type pattern: :class:`Pattern <EBSDTools.indexation.pattern.Pattern>`
    """
    self.pattern = pattern
    
    self.houghMap = None
    self._peaks = None
    self._IQ = None
  
  def calculateHough(self, angleIncrement=0.5):
    """
    Calculate the Hough Transform. 
    
    A median and a contrast expansion is performed before doing the Hough transform.
    
    :arg angleIncrement: angle increment (in deg)
    :type angleIncrement: float
    """
    patternMap = self.pattern.patternMap.duplicate()
    
    Filter.median(patternMap)
    Contrast.expansion(patternMap)
    
#    self.houghMap = EBSD.houghTransform(patternMap, angleIncrement*pi/180.0)
    tt = Transform()
    self.houghMap = tt.hough(patternMap, angleIncrement*pi/180.0)
    
  def findPeaks(self, method=FINDPEAKS_TOP_HAT, **args):
    """
    Find the peaks in the Hough transform with the classic Top Hat thresholding
    """
    
    if self.houghMap == None: self.calculateHough()
    
    if method == FINDPEAKS_TOP_HAT:
      self._findPeaks_top_hat(**args)
    elif method == FINDPEAKS_BUTTERFLY:
      self._findPeaks_butterfly(**args)
  
  def _findPeaks_top_hat(self, **args):
    #Get peaks from Hough
    peaksMap = EBSD.houghThresholding(self.houghMap)
    identMap = Analysis.identify(peaksMap)
    assert self.houghMap.size == identMap.size
    
    #Get intensities of peaks from Hough Transform
    intensities = {}
    for objectId in range(0,identMap.getObjectCount()):
      intensities[objectId] = []
    
    for index in range(identMap.size):
      objectId = identMap.pixArray[index]
      if objectId > 0:
        houghPixelValue = self.houghMap.getPixValue(index)
        intensities[objectId-1].append(houghPixelValue)
    
    #Get centroid of peaks
    centroids = []
    centroidsXY = []
    
    xS, yS = Analysis.measureCentroid(identMap)
    for i in range(len(xS)):
      x = int(round(xS[i])); y = int(round(yS[i]))
      r = self.houghMap.getR(x, y)
      theta = self.houghMap.getTheta(x, y)
      
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
  
  def _findPeaks_butterfly(self, **args):
    houghMap = self.houghMap.duplicate()
    
    #Crop white edges on top and bottom
    cropDistanceY = int(args['radius'] / houghMap.getDeltaR()) - 6
    houghMap.setROI(0, houghMap.height/2-cropDistanceY, houghMap.width-1, houghMap.height/2+cropDistanceY)
    houghMap_crop = Edit.crop(houghMap)
    houghMap.resetROI()
    
    houghMap_crop.setFile('hough1.bmp')
    IO.save(houghMap_crop)
    
    MathMorph.closing(houghMap_crop, 1)
    
    #3x3
#    k = [[0,-2,0], [1,3,1], [0,-2,0]]
    
    #9x9
    k = [[-10, -15, -22, -22, -22, -22, -22, -15, -10],
         [ -1,  -6, -13, -22, -22, -22, -13,  -6,  -1],
         [  3,   6,   4,  -3, -22,  -3,   4,   6,   3],
         [  3,  11,  19,  28,  42,  28,  19,  11,   3],
         [  3,  11,  27,  42,  42,  42,  27,  11,   3],
         [  3,  11,  19,  28,  42,  28,  19,  11,   3],
         [  3,   6,   4,  -3, -22,  -3,   4,   6,   3],
         [ -1,  -6, -13, -22, -22, -22, -13,  -6,  -1],
         [-10, -15, -22, -22, -22, -22, -22, -15, -10]]
    
    kernel = Kernel(k, 1)
    Convolution.convolve(houghMap_crop, kernel)
    
    houghMap.setFile('hough1_b.bmp')
    IO.save(houghMap_crop)
    
    #Thresholding
    peaksMap = Threshold.iterative(houghMap_crop)
    
    #Clean peaks (small peaks)
    
    
    identMap = Analysis.identify(peaksMap)
    print identMap.getObjectCount()
    
    peaksMap.setFile('peaks_b.bmp')
    IO.save(peaksMap)
  
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
    
    if self.houghMap == None: self.calculateHough()
    
    return self.houghMap
  
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
  import EBSDTools.indexation.masks as masks
  import EBSDTools.indexation.pattern as pattern
  
  maskMap = masks.createMaskDisc(width=168, height=128, centroid=(84,64), radius=65)
  P = pattern.Pattern(filepath='testData/pattern1.bmp', maskMap=maskMap)
  H = Hough(P)
  H.calculateHough(angleIncrement=0.5)
  H.findPeaks(method=FINDPEAKS_BUTTERFLY, radius=59)