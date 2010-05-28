#!/usr/bin/env jython
""" """

# Script information for the file.
__author__ = "Philippe Pinard (philippe.pinard@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2008-2009 Philippe Pinard"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = ""
__svnDate__ = ""
__svnId__ = ""

# Standard library modules.
import os
from math import pi, cos, atan, sqrt, tan, sin, log

# Third party modules.

# Local modules.
import ebsdtools.crystallography.plane as plane
import ebsdtools.crystallography.reflectors as reflectors
import ebsdtools.crystallography.calculations as calculations

import mathtools.rotation.quaternions as quaternions
import mathtools.algebra.vectors as vectors
from mathtools.rotation.trigo import acos

import RandomUtilities.DrawingTools.colors as colors

import ebsdtools.patternSimulations.linedrawing as linedrawing


"""
Band Color Intensity Function

:arg normalizedIntensity: normalized intensity between 0.0 and 1.0
:type normalizedIntensity: float

:arg intensityMin: minimum intensity
:type intensityMin: int

:arg intensityMax: maximum intensity
:type intensityMax: int

:return: a value between 0.0 and 1.0
:rtype: int
"""
def bandColorIntensityLog(args):
  normalizedIntensity = args['normalizedIntensity']
  intensityMax = args['intensityMax'] / 255.0
  intensityMin = args['intensityMin'] / 255.0

  return log(normalizedIntensity + 1) * ((intensityMax - intensityMin) / log(2)) + intensityMin

def bandColorIntensityLog10(args):
  normalizedIntensity = args['normalizedIntensity']
  intensityMax = args['intensityMax'] / 255.0
  intensityMin = args['intensityMin'] / 255.0

  return log10(normalizedIntensity + 1) * ((intensityMax - intensityMin) / log10(2)) + intensityMin

def bandColorIntensity(args):
  normalizedIntensity = args['normalizedIntensity']
  intensityMax = args['intensityMax'] / 255.0
  intensityMin = args['intensityMin'] / 255.0

  return normalizedIntensity * ((intensityMax - intensityMin)) + intensityMin

"""
Band Gaussian Distribution Functions

:arg thickness: thickness of the band
:type thickness: int

:arg normalizedIntensity: normalized intensity between 0.0 and 1.0
:type normalizedIntensity: float

:return: the standard deviation and minimum color of the Gaussian distribution
:rtype: tuple
"""
def bandGaussian(args):
  thickness = args['thickness']

  return thickness / 10.0, 0








class PatternBandCenter(Pattern):
  pass

class PatternBandFull(Pattern):
  pass


def drawPattern(reflectors
                , bandcenter=True
                , bandedges=False
                , bandfull=False
                , intensityFunction=bandColorIntensity
                , intensityMin=0
                , intensityMax=255
                , intensityBackground=128
                , gaussianFunction=None
                , patterncenter_x=0.0
                , patternCenterY=0.0
                , detectordistance=0.3
                , energy=20e3
                , numberOfReflectors=32
                , qRotations=quaternions.quaternion(1)
                , patternWidth=2680
                , patternHeight=2040
                , patternCenterVisible=True
                , colormode=drawing.COLORMODE_GRAYSCALE
                , reflectorsInfo=[]):
  """
  Draw a pattern based on the crystallography and detector parameters

  :arg bandcenter: Draw the band center? (``default=True``)
  :type bandcenter: bool

  :arg bandedges: Draw the band edges? (``default=False``)
  :type bandedges: bool

  :arg bandfull: Draw filled bands (full bands)? (``default=False``)
  :type bandfull: bool

  :arg intensityMin: the minimum intensity of the bands (value between 0 and 255)
  :type intensityMin: int

  :arg intensityMax: the maximum intensity of the bands (value between 0 and 255)
  :type intensityMax: int

  :arg intensityBackground: the background intensity (value between 0 and 255)
  :type intensityBackground: int

  :arg intensityFunction: the function to calculate the intensity of the bands from the reflectors' intensity (``default=bandColorIntensity``)
  :type intensityFunction: func

  :arg gaussianFunction: the function to calculate the parameters for the gaussian distribution of the line intensity. If ``None`` the line has no distribution (``default=None``)
  :type gaussianFunction: func

  :arg patternCenterY: Coordinates of the pattern center in the horizontal direction (in fraction of the pattern's width) (``default=0.0``)
  :type patternCenterY: float

  :arg patternCenterY: Coordinates of the pattern center in the vertical direction (in fraction of the pattern's  height) (``default=0.0``)
  :type patternCenterY: float

  .. note:: A pattern center of ``(0.0, 0.0)`` is centered

  :arg detectordistance: distance of the detector (in fraction of the pattern's width) (``default=0.3``)
  :arg detectordistance: float

  :arg energy: accelerating energy (in eV) (``default=20e3``)
  :type energy: float

  :arg numberOfReflectors: number of reflectors drawn in the pattern (``default=32``)
  :type numberOfReflectors: int

  :arg qRotations: quaternion representing the rotation of the pattern (``default=quaternions.quaternion(1)``, i.e. no rotation)
  :type qRotations: :class:`quaternion <EBSDTools.mathTools.quaternions.quaternion>`

  :arg patternSizeWidth: width of the pattern (in pixels) (``default=2680``)
  :type patternSizeWidth: int

  :arg patternSizeHeight: height of the pattern (in pixels) (``default=2040``)
  :type patternSizeHeight: int

  :arg patternCenterVisible: Draw the location of the pattern center? (``default=False``)
  :type patternCenterVisible: bool

  :arg colormode: either drawing.COLORMODE_GRAYSCALE or drawing.COLORMODE_RGB
  :type colormode: str

  :arg reflectorsInfo: list to return the info on the reflectors in the pattern. It should be pointing to an empty list.
  :type reflectorsInfo: list

  :rtype: :class:`ImageLine <RandomUtilities.DrawingTools.drawing.ImageLine>`
  """

  im = drawing.ImageLine(patternWidth, patternHeight, origin=drawing.ORIGIN_CENTER, colormode=colormode)

  #Add an uniform background
  if colormode == drawing.COLORMODE_GRAYSCALE:
    im.drawGrayBrackground(color=intensityBackground)
  elif colormode == drawing.COLORMODE_RGB:
    im.drawGrayBrackground(color=(intensityBackground, intensityBackground, intensityBackground))
    colorsList = colors.colorsList()

  planes = reflectors.getReflectorsList()[:numberOfReflectors]
  planes.reverse()

#  print '-'*40

  for index, plane in enumerate(planes):
    qPlane = quaternions.quaternion(0, plane)
    planeRot = quaternions.rotate(qPlane, qRotations).vector()

    m, k = computePlaneEquationOnCamera(plane=planeRot
                                        , patterncenter_x=patterncenter_x
                                        , patternCenterY=patternCenterY
                                        , detectordistance=detectordistance)

    #Line parallel to the screen
    if m == None and k == None:
      continue

#    print plane, m, k

    if bandedges or bandfull:
      x0 = vectors.vector(0, 0, 0)

      if m == None:
        x1 = vectors.vector(k, detectordistance, 0.0)
        x2 = vectors.vector(k, detectordistance, 0.1)
      elif abs(m) < zeroPrecision:
        x1 = vectors.vector(0.0, detectordistance, k)
        x2 = vectors.vector(0.1, detectordistance, k)
      else:
        x1 = vectors.vector(0.0, detectordistance, k)
        if abs(k) > zeroPrecision:
          x2 = vectors.vector(-k / m, detectordistance, 0.0)
        else: # abs(k) < zeroPrecision:
          x2 = vectors.vector((1 - k) / m, detectordistance, 1.0)

      n = vectors.cross(x2 - x1, x1 - x0)
      s = vectors.vector(n[0], 0, n[2])
      d = n.norm() / (x2 - x1).norm()
      cosalpha = vectors.dot(n, s) / (n.norm()*s.norm())
      alpha = _acos(cosalpha)

      #Diffraction angle
      planeSpacing = reflectors.getReflectorPlaneSpacing(plane)
      wavelength = bragg.electronWavelength(energy)
      theta = bragg.diffractionAngle(planeSpacing, wavelength)

      #Half-width of the band
      w = d * sin(theta) / cos(alpha - theta)
      w2 = d * sin(theta) / cos(alpha + theta)

    #Color according to intensity
    normalizedIntensity = reflectors.getReflectorNormalizedIntensity(plane)
    intensityBand = intensityFunction(locals())
    if colormode == drawing.COLORMODE_RGB:
      baseColor = colorsList.getColorRGB(index)
      color = (int(baseColor[0] * intensityBand), int(baseColor[1] * intensityBand), int(baseColor[2] * intensityBand))
      colorInfo = color
    elif colormode == drawing.COLORMODE_GRAYSCALE:
      color = int(intensityBand * 255)
      colorInfo = (color, color, color)

#    print plane, 'm', m, 'k', k#, 'd', d, 'theta', theta, 'w', w, 'alpha', cosalpha, 'g', grayLevel

    #Translation due to the pattern center
    if m != None:
      k += -m * patterncenter_x + patternCenterY
    else:
      k += patterncenter_x

    if bandcenter:
      im.drawLinearFunction(m=m
                            , k=k
                            , color=color)

    if bandedges:
      #Correction for the slope of the band
      if m != None:
        beta = atan(m)
      else:
        beta = 0.0

      h = w / cos(beta)
      im.drawLinearFunction(m=m
                            , k=k + h
                            , color=color)

      h2 = w2 / cos(beta)
      im.drawLinearFunction(m=m
                            , k=k - h2
                            , color=color)

    if bandfull:
      thickness = int(2 * w * patternWidth) + 1 #The +1 prevents lien with 0 thickness
      if gaussianFunction == None:
        im.drawLinearFunction(m=m
                              , k=k
                              , thickness=thickness
                              , color=color)
      else:
        stddev, colorMin = gaussianFunction(locals())
        im.drawLinearFunctionGaussianDistribution(m=m
                                                  , k=k
                                                  , thickness=thickness
                                                  , colorMax=color
                                                  , colorMin=colorMin
                                                  , stddev=stddev)

    if bandcenter or bandedges or bandfull:
      reflectorsInfo.append({'indices': plane, 'rgb': colorInfo, 'intensity': normalizedIntensity})
  #Mark the pattern center
  if patternCenterVisible:
    if colormode == drawing.COLORMODE_RGB:
      im.drawCrossMarker(positionX=patterncenter_x, positionY=patternCenterY, color=(255, 255, 255))
    elif colormode == drawing.COLORMODE_GRAYSCALE:
      im.drawCrossMarker(positionX=patterncenter_x, positionY=patternCenterY, color=255)

  return im()

def main():
  import EBSDTools.crystallography.lattice as lattice
  import EBSDTools.crystallography.reflectors as reflectors
  import EBSDTools.mathTools.eulers as eulers
  import os.path
  if os.name == 'java':
    import rmlimage.io.IO as IO

#  #FCC
  atoms = {(0, 0, 0): 14,
           (0.5, 0.5, 0): 14,
           (0.5, 0, 0.5): 14,
           (0, 0.5, 0.5): 14}
#  atoms = {(0,0,0): 14,
#           (0.5,0.5,0.5): 14}
  L = lattice.Lattice(a=5.43, b=5.43, c=5.43, alpha=pi / 2, beta=pi / 2, gamma=pi / 2, atoms=atoms)
  R = reflectors.Reflectors(L, maxIndice=4)
#  print len(R.getReflectorsList())

  angles = eulers.eulers(0 / 180.0 * pi, 0, 0) #z

  qSpecimenRotation = quaternions.quaternion(1, 0, 0, 0)
  qCrystalRotation = quaternions.eulerAnglesToQuaternion(angles)
  qTilt = quaternions.axisAngleToQuaternion(-70 / 180.0 * pi, (1, 0, 0))
  qDetectorOrientation = quaternions.axisAngleToQuaternion(90 / 180.0 * pi, (1, 0, 0)) * quaternions.axisAngleToQuaternion(pi, (0, 0, 1))
  qDetectorOrientation = quaternions.quaternion(1, 0, 0, 0)
  qDetectorOrientation_ = qTilt * qDetectorOrientation.conjugate() * qTilt.conjugate()

  qRotations = [qSpecimenRotation, qCrystalRotation, qTilt, qDetectorOrientation_]

  image = drawPattern(R
              , bandcenter=False
              , bandedges=False
              , bandfull=True
              , intensityMin=120
              , intensityMax=255
              , gaussianFunction=None
              , intensityBackground=128
              , patterncenter_x=0.0
              , patternCenterY=0.0
              , detectordistance=0.4
              , energy=15e3
              , numberOfReflectors=100
              , qRotations=qRotations
              , patternWidth=335
              , patternHeight=255
              , patternCenterVisible=False
              , colormode=drawing.COLORMODE_GRAYSCALE)

  if os.name == 'java':
    image.setFile(r'test.bmp')
    IO.save(image)
  else:
    image.show()

if __name__ == '__main__':
  main()
