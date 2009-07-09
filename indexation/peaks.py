#!/usr/bin/env python
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
import rmlimage.core
import rmlimage.io
import rmlimage.module.ebsd as ebsd

# Local modules.
import RandomUtilities.sort.sortDict as sortDict

# Globals and constants variables.
AVERAGE_INTENSITY = 'average intensity'
STDDEV_INTENSITY = 'stddev intensity'
MAXIMUM_INTENSITY = 'maximum intensity'
MINIMUM_INTENSITY = 'minimum intensity'
AREA = 'area'
CENTROID_RHO = 'centroid rho'
CENTROID_THETA = 'centroid theta'
RHO_MAX = 'rho max'
RHO_MIN = 'rho min'
THETA_MAX = 'theta max'
THETA_MIN = 'theta min'

class Peak(dict):
  def __init__(self, peakBinMap, houghMap):
    """

    """
    self._peakBinMap = peakBinMap
    self._houghMap = houghMap

    self._peakHoughMap = rmlimage.core.ByteMap(houghMap.width, houghMap.height)
    rmlimage.core.MapMath.andOp(houghMap, peakBinMap, self._peakHoughMap)

    self._peakIdentMap = rmlimage.core.Identification.identify(peakBinMap)
    assert self._peakIdentMap.getObjectCount() == 1

    dict.__init__(self)

    self._calculateIntensityStats()
    self._calculateArea()
#    self._calculateCentroid()

  def _calculateIntensityStats(self):
    average = ebsd.core.Analysis.average(self._peakHoughMap)
    self[AVERAGE_INTENSITY] = average

    stddev = ebsd.core.Analysis.standardDeviation(self._peakHoughMap)
    self[STDDEV_INTENSITY] = stddev

    maximum = max(self._peakHoughMap.pixArray)
    self[MAXIMUM_INTENSITY] = maximum

    minimum = max(self._peakHoughMap.pixArray)
    self[MINIMUM_INTENSITY] = minimum

  def _calculateArea(self):
    area = rmlimage.core.Analysis.getArea(self._peakIdentMap).val[0]
    self[AREA] = area

  def _calculateCentroid(self):
    centroid = rmlimage.core.Analysis.getCentroid(self._peakIdentMap)
    centroidX = centroid.x[0]
    centroidY = centroid.y[0]
    centroidRho = self._houghMap.getR(centroidX, centroidY)
    centroidTheta = self._houghMap.getTheta(centroidX, centroidY)

    self[CENTROID_RHO] = centroidRho
    self[CENTROID_THETA] = centroidTheta

  def getIntensityAverage(self):
    return self.get(AVERAGE_INTENSITY)

  def getIntensityStandardDeviation(self):
    return self.get(STDDEV_INTENSITY)

  def getArea(self):
    return self.get(AREA)

  def getCentroid(self):
    return self.get(CENTROID_RHO), self.get(CENTROID_THETA)


class Peaks(list):
  def __init__(self, identMap, houghMap):
    """

    """
    self._identMap = identMap
    self._houghMap = houghMap

    peaks = self._findPeaks()
    list.__init__(self, peaks)

  def __deepcopy__(self, memo):
    return Peaks(self._identMap, self._houghMap)

  def _findPeaks(self):
    peaks = []

    #Remove peaks touching the edges
    rmlimage.core.Identification.removeObjectsTouchingEdges(self._identMap)

    #Peaks count
    numberPeaks = self._identMap.getObjectCount()

    for iPeak in range(1, numberPeaks+1):
      #Create a binMap with only one peak
      identMap = self._identMap.duplicate()
      rmlimage.core.Identification.keepObjects(identMap, [iPeak])
      peakBinMap = rmlimage.core.Conversion.toBinMap(identMap)

      #Dilation of the peak
      rmlimage.core.MathMorph.dilation(peakBinMap, 2, 8, 3)

      #Create a Peak class
      peak = Peak(peakBinMap, self._houghMap)
      peaks.append(peak)

#      peak._peakHoughMap.setFile('peak%i.bmp' % iPeak)
#      rmlimage.io.IO.save(peak._peakHoughMap)
    return peaks

  def sort(self, key, reverse=False):
    self = sortDict.sortListByKey(self, key, reverse)

if __name__ == '__main__':
  pass
