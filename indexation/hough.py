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
import rmlimage.core
import rmlimage.module.ebsd as ebsd
import rmlimage.macro.python.cui as macro

import rmlshared.math as math

# Local modules.
import RandomUtilities.sort.sortDict as sortDict

# Globals and constants variables.
FINDPEAKS_TOP_HAT         = 'tophat'
FINDPEAKS_BUTTERFLY       = 'butterfly'

class HoughMap(ebsd.core.HoughMap):
  def __init__(self, patternMap, angleIncrement=0.5):
    """
    Create a Hough class (inherit :class:`HoughMap <rmlimage.plugin.ebsd.HoughMap>`

    Calculate the Hough Transform.
        A median and a contrast expansion is performed before doing the Hough transform.
MathMorph.median(houghMap_crop, 3)
    :arg patternMap: a pattern map
    :type patternMap: :class:`PatternMap <EBSDTools.indexation.pattern.PatternMap>`

    :arg angleIncrement: angle increment (in deg)
    :type angleIncrement: float
    """
    self.patternMap = patternMap

    #Calculate Hough
    patternHoughMap = self.patternMap.duplicate()

    rmlimage.core.MathMorph.median(patternHoughMap)
    rmlimage.core.Contrast.expansion(patternHoughMap)

    houghMap = ebsd.core.Transform().hough(patternHoughMap, angleIncrement*pi/180.0)

    ebsd.core.HoughMap.__init__(self, houghMap)

  def findPeaks(self, method=FINDPEAKS_TOP_HAT):
    """
    Find the peaks in the Hough transform with the classic Top Hat thresholding
    """

    if method == FINDPEAKS_TOP_HAT:
      self._findPeaks_top_hat()
    elif method == FINDPEAKS_BUTTERFLY:
      self._findPeaks_butterfly()

  def _findPeaks_top_hat(self, **args):
    #Get peaks from Hough
    peaksMap = ebsd.core.Threshold.automaticTopHat(self.houghMap)
    identMap = ebsd.core.Identification.identify(peaksMap)
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

    xS, yS = rmlimage.core.Analysis.getCentroid(identMap)
    for i in range(len(xS)):
      x = int(round(xS[i])); y = int(round(yS[i]))
      r = self.houghMap.getR(x, y)
      theta = self.houghMap.getTheta(x, y)

      centroids.append((r,theta))
      centroidsXY.append((x,y))

    #Get area of peaks
    areas = rmlimage.core.Analysis.getArea(identMap)

    #Store information in self._peaks
    self._peaks = {}
    for objectId in range(0,identMap.getObjectCount()):
      averageIntensity = math.Stats.average(intensities[objectId])
      stdDevIntensity = math.Stats.standardDeviation(intensities[objectId])
      centroid = centroids[objectId]
      centroidXY = centroidsXY[objectId]
      area = areas[objectId]

      peak = {'intensity': {'average': averageIntensity, 'standard deviation': stdDevIntensity}
              , 'centroid': centroid
              , 'centroidXY': centroidXY
              , 'area': area}
      self._peaks[objectId] = peak

  def _findPeaks_butterfly(self):
    houghMap = self.duplicate()

    #Crop white edges on top and bottom
    topY = houghMap.getY(self.patternMap.getMaskMap().getRadius())
    bottomY = houghMap.getY(-self.patternMap.getMaskMap().getRadius())

    houghMap.setROI(0, topY, houghMap.width-1, bottomY)
    houghMap_crop = rmlimage.core.Edit.crop(houghMap)
    houghMap.resetROI()

    #Apply median filter
    rmlimage.core.MathMorph.median(houghMap_crop, 3)

    houghMap_crop.setFile('hough1.bmp')
    IO.save(houghMap_crop)

#    MathMorph.closing(houghMap_crop, 1)

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

    kk = rmlimage.core.Kernel(k, 1)

    destMap = rmlimage.core.ByteMap(houghMap_crop.width, houghMap_crop.height)
    ebsd.core.Convolution.convolve(houghMap_crop, kk, destMap)

    destMap.setFile('hough1_b.bmp')
    IO.save(destMap)

#    Convolution.convolve(houghMap_crop, kk)
#
#    houghMap_crop.setFile('hough1_b.bmp')
#    IO.save(houghMap_crop)

    #Thresholding
#    peaksMap = Threshold.automaticTopHat(houghMap_crop)
#
#    #Clean peaks (small peaks)
#
#
#    identMap = Analysis.identify(peaksMap)
#    print identMap.getObjectCount()
#
#    peaksMap.setFile('peaks_b.bmp')
#    IO.save(peaksMap)

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

if __name__ == '__main__':
  import EBSDTools.indexation.masks as masks
  import EBSDTools.indexation.pattern as pattern

  maskMap = masks.MaskDisc(width=168, height=128, centroid=(84,64), radius=59)
  P = pattern.PatternMap(filepath='testData/pattern1.bmp', maskMap=maskMap)
  H = HoughMap(P)

  H.setFile('houghtt1.bmp')
  IO.save(H)
  H.findPeaks(method=FINDPEAKS_BUTTERFLY)
