#!/usr/bin/env jython
"""
Module to be compile using jythonc for RML-Image
"""

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
from math import pi
import java.lang
import rmlshared.io.FileUtil as FileUtil

# Third party modules.

# Local modules.
import EBSDTools.patternSimulations.patternSimulations as patternSimulations
import EBSDTools.crystallography.reflectors as reflectors
import EBSDTools.mathTools.quaternions as quaternions
import EBSDTools.mathTools.eulers as eulers
import EBSDTools.crystallography.lattice as lattice

class jPatternSimulations(java.lang.Object):
  """
  Test Bean Shell Script
  elastic_atomic_scattering_factors_0_2.csv and elastic_atomic_scattering_factors_2_6.csv should be in the class folder of RML-Image
  
  import rmlimage.plugin.ebsd.python.jPatternSimulations;

  jPatternSimulations patt = new jPatternSimulations(335, 255, false, 0.0, 0.0, 0.3, 20000.0, 32, 70.0);
  ByteMap sim = patt.patternFCC(0.0, 0.0, 0.0);
  
  RMLImage.add(sim);
  
  """
  def __init__(self, patternWidth=2680, patternHeight=2040, intensity=False, patternCenterX=0.0, patternCenterY=0.0, detectorDistance=0.3, energy=20e3, numberOfReflectors=32, tilt=70.0):
    "@sig public jPatternSimulations(int patternWidth, int patternHeight, boolean intensity, double patternCenterX, double patternCenterY, double detectorDistance, double energy, int numberOfReflectors, double tilt)"
    """
    :arg patternWidth: width of the pattern (in pixels) (``default=2680``)
    :type patternWidth: int
    
    :arg patternHeight: height of the pattern (in pixels) (``default=2040``)
    :type patternHeight: int
    
    :arg intensity: The color of the bands should reflect the intensity? (``default=False``)
    :arg intensity: bool
    
    :arg patternCenterY: Coordinates of the pattern center in the horizontal direction (in fraction of the pattern's width) (``default=0.0``)
    :type patternCenterY: float
    
    :arg patternCenterY: Coordinates of the pattern center in the vertical direction (in fraction of the pattern's  height) (``default=0.0``)
    :type patternCenterY: float
    
    .. note:: A pattern center of ``(0.0, 0.0)`` is centered
    
    :arg detectorDistance: distance of the detector (in fraction of the pattern's width) (``default=0.3``)
    :arg detectorDistance: float
    
    :arg energy: accelerating energy (in eV) (``default=20e3``)
    :type energy: float
    
    :arg numberOfReflectors: number of reflectors drawn in the pattern (``default=32``)
    :type numberOfReflectors: int
    
    :arg tilt: tilt of the sample (``default=70.0``)
    :type tilt: float
    """
    self.patternWidth = patternWidth
    self.patternHeight = patternHeight
    self.intensity = intensity
    self.patternCenterX = patternCenterX
    self.patternCenterY = patternCenterY
    self.detectorDistance = detectorDistance
    self.energy = energy
    self.numberOfReflectors = numberOfReflectors
    self.tilt = tilt
  
  def patternFCC(self, euler1, euler2, euler3):
    "@sig public rmlimage.kernel.ByteMap patternFCC(double euler1, double euler2, double euler3)"
    """
    :arg euler1: first euler angle in degrees (0 < euler1 < 360)
    :type euler1: float
    
    :arg euler2: second euler angle in degrees (0 < euler2 < 180)
    :type euler2: float
    
    :arg euler3: third euler angle in degrees (0 < euler3 < 360)
    :type euler3: float
    """
    atoms = {(0,0,0): 14,
             (0.5,0.5,0): 14,
             (0.5,0,0.5): 14,
             (0,0.5,0.5): 14}
    
    L = lattice.Lattice(a=5.43
                        , b=5.43
                        , c=5.43
                        , alpha=pi/2
                        , beta=pi/2
                        , gamma=pi/2
                        , atoms=atoms)
    
    ref = reflectors.Reflectors(L
                                , maxIndice=4
                                , filepath_0_2=FileUtil.getFile('rmlimage/plugin/ebsd/python/data/elastic_atomic_scattering_factors_0_2.csv')
                                , filepath_2_6=FileUtil.getFile('rmlimage/plugin/ebsd/python/data/elastic_atomic_scattering_factors_2_6.csv'))
    
    angles = eulers.eulers(euler1/180.0*pi, euler2/180.0*pi, euler3/180.0*pi) 
    qSpecimenRotation = quaternions.quaternion(1,0,0,0)
    qCrystalRotation = quaternions.eulerAnglesToQuaternion(angles)
    qTilt = quaternions.axisAngleToQuaternion(-self.tilt/180.0*pi, (1,0,0))
    qDetectorOrientation = quaternions.axisAngleToQuaternion(90/180.0*pi, (1,0,0)) * quaternions.axisAngleToQuaternion(pi, (0,0,1))
#    qDetectorOrientation = quaternions.quaternion(1,0,0,0)
    qDetectorOrientation_ = qTilt * qDetectorOrientation.conjugate() * qTilt.conjugate()
    
    qRotations = [qSpecimenRotation, qCrystalRotation, qTilt, qDetectorOrientation_]
    
    patt = patternSimulations.drawPattern(reflectors=ref
                                          , bandcenter=False
                                          , bandedges=False
                                          , bandfull=True
                                          , intensity=self.intensity
                                          , patternCenterX=self.patternCenterX
                                          , patternCenterY=self.patternCenterY
                                          , detectorDistance=self.detectorDistance
                                          , energy=self.energy
                                          , numberOfReflectors=self.numberOfReflectors
                                          , qRotations=qRotations
                                          , patternWidth=self.patternWidth
                                          , patternHeight=self.patternHeight
                                          , patternCenterVisible=False
                                          , colormode=patternSimulations.drawing.COLORMODE_GRAYSCALE
                                          )
    return patt
  
if __name__ == '__main__':
  patt = jPatternSimulations(335, 255, False, 0.0, 0.0, 0.3, 20e3, 32, 70.0)
  print patt.patternFCC(0.0, 0.0, 0.0)
  