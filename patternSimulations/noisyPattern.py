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
import random
from math import pi
import java.io

# Third party modules.
import rmlimage.core
import rmlimage.io.IO as IO
import rmlimage.module.ebsd as ebsd
import rmlimage.utility

# Local modules.
import EBSDTools.crystallography.lattice as lattice
import EBSDTools.crystallography.reflectors as reflectors
import EBSDTools.mathTools.eulers as eulers
import EBSDTools.mathTools.quaternions as quaternions
import EBSDTools.patternSimulations.patternSimulations as patternSimulations
import EBSDTools.mathTools.errorFunction as errorFunction
import RandomUtilities.DrawingTools.drawing as drawing

erfP = lambda p, x: p[0] * errorFunction.erf(p[1]*(x-p[2])) + p[3]

def gaussianDistribution(args):
  thickness = args['thickness']
  normalizedIntensity = args['normalizedIntensity']
  intensityBackground = args['intensityBackground']/255.0
  intensityBand = args['intensityBand']

  x = normalizedIntensity

  amplitude = (2*thickness-(thickness/5.0))/2.0
  p = [amplitude, -5, 0.5, amplitude+thickness/5.0]
  stddev = erfP(p, x)

  amplitude = (1.0-intensityBackground/2.0)/2.0
  p = [amplitude, -4, 0.6, amplitude+intensityBackground/2.0]
  colorMin = erfP(p,x)*intensityBand

  return stddev, int(colorMin*255)

def noisy1():
#  #FCC
  atoms = {(0,0,0): 14,
           (0.5,0.5,0): 14,
           (0.5,0,0.5): 14,
           (0,0.5,0.5): 14}
  L = lattice.Lattice(a=5.43, b=5.43, c=5.43, alpha=pi/2, beta=pi/2, gamma=pi/2, atoms=atoms)
  R = reflectors.Reflectors(L, maxIndice=5)
  print len(R.getReflectorsList())

  angles = eulers.eulers(random.randint(0,360)/180.0*pi, random.randint(0,360)/180.0*pi, random.randint(0,360)/180.0*pi) #z

  qSpecimenRotation = quaternions.quaternion(1,0,0,0)
  qCrystalRotation = quaternions.eulerAnglesToQuaternion(angles)
  qTilt = quaternions.axisAngleToQuaternion(-70/180.0*pi, (1,0,0))
  qDetectorOrientation = quaternions.axisAngleToQuaternion(90/180.0*pi, (1,0,0)) * quaternions.axisAngleToQuaternion(pi, (0,0,1))
#  qDetectorOrientation = quaternions.quaternion(1,0,0,0)
  qDetectorOrientation_ = qTilt * qDetectorOrientation.conjugate() * qTilt.conjugate()

  qRotations = [qSpecimenRotation, qCrystalRotation, qTilt, qDetectorOrientation_]

  image = patternSimulations.drawPattern(R
                      , bandcenter=False
                      , bandedges=False
                      , bandfull=True
                      , intensityMin=128
                      , intensityMax=255
                      , intensityFunction=patternSimulations.bandColorIntensity
                      , gaussianFunction=None
                      , intensityBackground=128
                      , patternCenterX=0.0
                      , patternCenterY=0.0
                      , detectorDistance=0.4
                      , energy=20e3
                      , numberOfReflectors=50
                      , qRotations=qRotations
                      , patternWidth=1344
                      , patternHeight=1024
                      , patternCenterVisible=False
                      , colormode=drawing.COLORMODE_GRAYSCALE)

  image.setFile('original.bmp')
  IO.save(image)


  image = patternSimulations.drawPattern(R
                      , bandcenter=False
                      , bandedges=False
                      , bandfull=True
                      , intensityMin=128
                      , intensityMax=255
                      , intensityFunction=patternSimulations.bandColorIntensityLog
                      , gaussianFunction=gaussianDistribution
                      , intensityBackground=128
                      , patternCenterX=0.0
                      , patternCenterY=0.0
                      , detectorDistance=0.4
                      , energy=20e3
                      , numberOfReflectors=50
                      , qRotations=qRotations
                      , patternWidth=1344
                      , patternHeight=1024
                      , patternCenterVisible=False
                      , colormode=drawing.COLORMODE_GRAYSCALE)

  image.setFile('noisy1before.bmp')
  IO.save(image)

  #Apply smooth filter
  kernelsize = 11
  kk = [[1,1,1,1,1,1,1,1,1,1,1]]*11
  kernel = rmlimage.core.Kernel(kk, kernelsize**2)
  rmlimage.core.Convolution.convolve(image, kernel)

  #Binning
  image = rmlimage.core.Transform.binning(image, 8, 8)

  image.setFile('binned.bmp')
  IO.save(image)

  #Noise
  for i in range(4):
    rmlimage.utility.Noise.gaussian(image, 25.0)

    image.setFile('noisy1_gn%i.bmp' % (i+1))
    IO.save(image)

if __name__ == '__main__':
  noisy1()
