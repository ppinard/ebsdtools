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


class Peaks(list):
  def __init__(self, identMap, houghMap):
    """

    """
    self._houghMap = houghMap

    peaks = self._findPeaks(identMap)
    list.__init__(self, peaks)

  def __deepcopy__(self, memo=None):
    return Peaks(self._identMap, self._houghMap)

  def _findPeaks(self, identMap):
    peaks = []

    #Dilation of peaks to increase their area
    binMap = rmlimage.core.Conversion.toBinMap(identMap)
    rmlimage.core.MathMorph.dilation(binMap, 2, 8, 3)
    self._identMap = rmlimage.core.Identification.identify(binMap)

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
      id = i + 1 #the background is id=0
      maximumIntensity = maximums[i]
      centroidRho = centroidsRho[i]
      centroidTheta = centroidsTheta[i]

      peak = Peak(id, centroidRho, centroidTheta, maximumIntensity)

      peaks.append(peak)

    return peaks

  def sort(self, key, reverse=False):
    self = sortDict.sortListByKey(self, key, reverse)

  def overlay(self, originalPatternMap, numberPeaks, color):
    peaks = self.__deepcopy__()
    overlayMap = originalPatternMap.duplicate()

    peaks.sort(MAXIMUM_INTENSITY, reverse=True)
    peaks = peaks[:numberPeaks]

    ids = []
    for i in range(min(numberPeaks, len(peaks))):
      ids.append(peaks[i].getObjectId())
    print ids

    identMap = self._identMap.duplicate()
    peaksBinMap = rmlimage.core.Identification.extractObjects(identMap, ids)
    peaksBinMap.setProperties(identMap)

    rgb = rmlimage.core.RGB(*color)
    ebsd.core.QC().overlay(overlayMap, peaksBinMap, rgb)

    peaksBinMap.setFile('bin%i.bmp' % numberPeaks)
    rmlimage.io.IO.save(peaksBinMap)

    return overlayMap

if __name__ == '__main__':
  pass
