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

# Third party modules.
import rmlimage.module.complex as imag
import rmlimage.module.real as real
import rmlimage

# Local modules.

# Globals and constants variables.

def createRadiusMap(width, height):
  realMap = real.core.RealMap(width, height)

  centerX = width / 2
  centerY = height / 2

  for x in range(width):
    for y in range(height):
      rsquare = (x - centerX)**2 + (y - centerY)**2
      realMap.setPixValue(x, y, rsquare)

  return realMap

def sumMap(realMap):
  average = real.core.Stats.average(realMap.pixArray)
  count = realMap.size

  return count * average

def qualityIndex(patternMap):
  patternCrop = imag.core.Edit.cropToNearestPowerOfTwo(patternMap, imag.core.Edit.Position.CENTER)

#  patternCrop.setFile('crop.bmp')
#  rmlimage.io.IO.save(patternCrop)

  fftMap = imag.core.FFT().forward(patternCrop)
  imag.core.Edit.flip(fftMap)

#  fftMap_byte = imag.core.Conversion.toByteMap(fftMap)
#  fftMap_byte.setFile('fft.bmp')
#  rmlimage.io.IO.save(fftMap_byte)

  normMap = imag.core.Extract.norm(fftMap)

#  normMap.setFile('norm.rmp')
#  real.io.IO.save(normMap)

  radiusMap = createRadiusMap(normMap.width, normMap.height)

  radiusMapSquared = real.core.RealMap(radiusMap.width, radiusMap.height)
  real.core.MapMath.multiplication(radiusMap, radiusMap, radiusMapSquared)

  numeratorMap = real.core.RealMap(normMap.width, normMap.height)
  real.core.MapMath.multiplication(normMap, radiusMapSquared, numeratorMap)

  numerator = sumMap(numeratorMap)
#  print numerator

  denominator = sumMap(normMap)
#  print denominator

  intensity = numerator / denominator
#  print intensity

  intensityMax = sumMap(radiusMapSquared) / (radiusMapSquared.width * radiusMapSquared.height)
#  print intensityMax

  quality = 1.0 - intensity / intensityMax
#  print quality

  return quality

if __name__ == '__main__':
  import EBSDTools.indexation.pattern as pattern

  P = pattern.PatternMap(filepath='testData/pattern1.bmp', maskMap=None)
#  P = pattern.PatternMap(filepath='testData/noise.bmp', maskMap=None)
  print qualityIndex(P)
#  import rmlimage
#
#  realMap = radiusMap(256, 256)
#  byteMap = real.core.Contrast.expansion(realMap)
#
#  realMap.setFile('radiusmap.rmp')
#  real.io.IO.save(realMap)
