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

import EBSDTools.indexation.peaks as peaks

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

  def findPeaks(self, method=FINDPEAKS_TOP_HAT, **args):
    """
    Find the peaks in the Hough transform with the classic Top Hat thresholding
    """

    if method == FINDPEAKS_TOP_HAT:
      self._findPeaks_top_hat(**args)
    elif method == FINDPEAKS_BUTTERFLY:
      self._findPeaks_butterfly(**args)

  def _findPeaks_top_hat(self, **args):
    #Get peaks from Hough
    peaksMap = ebsd.core.Threshold.automaticTopHat(self.houghMap)
    identMap = rmlimage.core.Identification.identify(peaksMap)
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

  def _findPeaks_butterfly(self, **args):
    houghMap = self.duplicate()

    #Crop white edges on top and bottom using the mask radius if available
    if self.patternMap.getMaskMap() != None:
      radius = self.patternMap.getMaskMap().getRadius()
      houghMap_crop = ebsd.core.Edit.crop(houghMap, radius)
#      for i in range(0, 15):
#        try:
#          radius = self.patternMap.getMaskMap().getRadius() - i
#
#          houghMap_crop = ebsd.core.Edit.crop(houghMap, radius)
#          print 'S', i, radius, houghMap_crop.getRMin(), houghMap_crop.getRMax()
#        except:
#          print 'F', i, radius, houghMap.getRMin(), houghMap.getRMax()
    else:
      houghMap_crop = houghMaphoughMap_crop.getRMax()

    self._houghMap_crop = houghMap_crop

    #Apply median filter
    rmlimage.core.MathMorph.median(houghMap_crop, 3)

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

    ebsd.core.Convolution.convolve(houghMap_crop, kk)

    self._houghMap_convol = houghMap_crop

    #Increase contrast
    invertedHoughMap = houghMap_crop.duplicate()
    rmlimage.core.MapMath.not(invertedHoughMap)

    invertedHoughMap.setFile('invert.bmp')
    IO.save(invertedHoughMap)

    dividedMap = rmlimage.core.ByteMap(houghMap_crop.width, houghMap_crop.height)
    rmlimage.core.MapMath.division(houghMap_crop, invertedHoughMap, 128.0, 0.0, dividedMap)
    dividedMap.setFile('divided.bmp')
    IO.save(dividedMap)

    peaksMap = ebsd.core.Threshold.automaticTopHat(houghMap_crop)



    identMap = rmlimage.core.Identification.identify(peaksMap)

    identMap.setFile('ident2.bmp')
    IO.save(identMap)

    self._peaks = peaks.Peaks(identMap, houghMap_crop)

  def getPeaks(self):
    """
    Return a list of peaks

    :rtype: :keyword:`list`
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

#  H.setFile('houghtt1.bmp')
#  IO.save(H)
  H.findPeaks(method=FINDPEAKS_BUTTERFLY)
  peaks = H.getPeaks()
#  print peaks



#  for numberPeak in range(3, 5):
#    overlayMap = peaks.overlay(P.getOriginalPattern(), numberPeak, (255,0,0))
#
#    overlayMap.setFile('overlay%i.bmp' % numberPeak)
#    IO.save(overlayMap)

#

