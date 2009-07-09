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
import copy

# Third party modules.
import rmlimage.module.ebsd as ebsd
import rmlshared.math.Stats
import EBSDTools.indexation.hough as hough
import EBSDTools.indexation.peaks as peaks

# Local modules.

class QualityIndexes(object):
  def getValue(self, *args):
    raise NotImplementedError

class PatternQualityIndexes(QualityIndexes):
  def __init__(self, patternMap):
    self._patternMap = patternMap

class HoughQualityIndexes(QualityIndexes):
  def __init__(self, houghMap):
    self._houghMap = houghMap
    houghMap.findPeaks(hough.FINDPEAKS_BUTTERFLY)
    self._peaksList = houghMap.getPeaks()
    self._peaksList.sort(peaks.AVERAGE_INTENSITY, reverse=True)

  def getValue(self, numberPeaks):
    return self._calculate(self._peaksList[:numberPeaks])

  def _calculate(self, peaksList):
    raise NotImplementedError

class average(PatternQualityIndexes):
  def getValue(self):
    return ebsd.core.Analysis.average(self._patternMap)

class standardDeviation(PatternQualityIndexes):
  def getValue(self):
    return ebsd.core.Analysis.standardDeviation(self._patternMap)

class entropy(PatternQualityIndexes):
  def getValue(self):
    return ebsd.core.Analysis.entropy(self._patternMap)

class imageQuality(HoughQualityIndexes):
  def _calculate(self, peaksList):
    numberPeaks = len(peaksList)

    value = 0.0
    for peak in peaksList:
      value += peak.getIntensityAverage()

    value /= numberPeaks

    return value

class numberPeaks(HoughQualityIndexes):
  def getValue(self):
    return len(self._peaksList)

class averageIntensity(HoughQualityIndexes):
  def _calculate(self, peaksList):
    intensities = []
    for peak in peaksList:
      intensities.append(peak.getIntensityAverage())

    return rmlshared.math.Stats.average(intensities)

class standardDeviationIntensity(HoughQualityIndexes):
  def _calculate(self, peaksList):
    intensities = []
    for peak in peaksList:
      intensities.append(peak.getIntensityStandardDeviation())

    return rmlshared.math.Stats.average(intensities)



if __name__ == '__main__':
  import pattern

  patt1 = pattern.PatternMap(filepath='testData/pattern1.bmp')

  print average(patt1).getValue()
  print standardDeviation(patt1).getValue()
  print entropy(patt1).getValue()
  iq = imageQuality(patt1)
  print iq.getValue(5)
  print iq.getValue(6)
  print iq.getValue(3)
  print iq.getValue(100)
