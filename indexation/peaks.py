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
  def __init__(self
               , centroidRho
               , centroidTheta
               , maximumIntensity):
    """

    """
    self[CENTROID_RHO] = centroidRho
    self[CENTROID_THETA] = centroidTheta
    self[MAXIMUM_INTENSITY] = maximumIntensity

  def getMaximumIntensity(self):
    return self.get(MAXIMUM_INTENSITY)

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

  def __deepcopy__(self, memo=None):
    return Peaks(self._identMap, self._houghMap)

  def _findPeaks(self):
    peaks = []

    #Remove peaks touching the edges
    rmlimage.core.Identification.removeObjectsTouchingEdges(self._identMap)

    #Maximum
    maximums = ebsd.core.Analysis.getMaximum(self._identMap, self._houghMap).val

    #Centroid
    binMap = rmlimage.core.Conversion.toBinMap(self._identMap)
    centroids = ebsd.core.Analysis.getCentroid(binMap)
    centroidsRho = centroids.r
    centroidsTheta = centroids.theta

    #Create Peak object
    for i in range(self._identMap.getObjectCount()):
      maximumIntensity = maximums[i]
      centroidRho = centroidsRho[i]
      centroidTheta = centroidsTheta[i]

      peak = Peak(centroidRho, centroidTheta, maximumIntensity)

      peaks.append(peak)

    return peaks

  def sort(self, key, reverse=False):
    self = sortDict.sortListByKey(self, key, reverse)

#  def overlay(self, originalPatternMap, numberPeaks, color):
#    peaks = self.__deepcopy__()
#    overlayMap = originalPatternMap.duplicate()
#
#    peaks.sort(MAXIMUM_INTENSITY, reverse=True)
#    peaks = peaks[:numberPeaks]
#
#    peaksBinMap = peaks[0]._peakBinMap
#    for peak in peaks[1:]:
#      rmlimage.core.MapMath.orOp(peaksBinMap, peak._peakBinMap, peaksBinMap)
#
#    rgb = rmlimage.core.RGB(*color)
#    ebsd.core.QC().overlay(overlayMap, peaksBinMap, rgb)
#
#    peaksBinMap.setFile('bin%i.bmp' % numberPeaks)
#    rmlimage.io.IO.save(peaksBinMap)
#
#    return overlayMap

if __name__ == '__main__':
  pass
