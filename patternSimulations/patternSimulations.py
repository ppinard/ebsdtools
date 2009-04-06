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
from math import pi, cos, atan, sqrt, tan,sin

# Third party modules.

# Local modules.
import EBSDTools.mathTools.quaternions as quaternions
import EBSDTools.mathTools.vectors as vectors
import EBSDTools.crystallography.bragg as bragg
import RandomUtilities.DrawingTools.colors as colors
from EBSDTools.mathTools.mathExtras import zeroPrecision, _acos
import RandomUtilities.DrawingTools.drawing as drawing

if os.name == 'java':
  import rmlimage.kernel as kernel
  
def computePlaneEquationOnCamera(plane
                                 , patternCenterX=0.0
                                 , patternCenterY=0.0
                                 , detectorDistance=1.0
                                 ):
  """
  Return the slope and intercept of the projection of a plane (hkl) on a detector located at *detectorDistance* and *patternCenter*
    
  :arg plane: diffracted plane
  :type plane: :class:`vector <EBSDTools.mathTools.vectors.vector>`
  
  :arg patternCenterX: location of the pattern center in the horizontal direction (``default=0.0``)
  :type patternCenterX: float
  
  :arg patternCenterY: location of the pattern center in the vertical direction (``default=0.0``)
  :type patternCenterY: float
  
  .. note:: A pattern center of ``(0.0, 0.0)`` is centered
  
  :arg detectorDistance: distance between the sample and the detector window [default=1.0]
  :type detectorDistance: float
    
  :return: :math:`(m, k)` the slope m and y-intercept k
  :rtype: tuple
  """
  
  nx = plane[0]
  ny = plane[1]
  nz = plane[2]
  
  if abs(nz) > zeroPrecision:
    m = -(nx/nz)
#    b = (h/l)*patternCenter[0] - detectorDistance*k/l + patternCenter[1]
    k = - detectorDistance*ny/nz
  else:
    if abs(nx) > zeroPrecision:
      m = None
#      b = -detectorDistance*k/h + patternCenter[0]
      k = -detectorDistance*ny/nx
    else: #Plane parallel to the screen
      m = None
      k = None

  return m, k

def drawPattern(L
                , bandcenter=True
                , bandedges=False
                , bandfull=False
                , intensity=False
                , patternCenterX=0.0
                , patternCenterY=0.0
                , detectorDistance=0.3
                , energy=20e3
                , numberOfReflectors=32
                , qRotations=quaternions.quaternion(1)
                , patternWidth=2680
                , patternHeight=2040
                , patternCenterVisible=True
                , colormode='grayscale'
                , reflectorsInfo=[]):
  """
  Draw a pattern based on the crystallography and detector parameters
    
  :arg bandcenter: Draw the band center? (``default=True``)
  :type bandcenter: bool
  
  :arg bandedges: Draw the band edges? (``default=False``)
  :arg bandedges: bool
  
  :arg bandfull: Draw filled bands (full bands)? (``default=False``)
  :arg bandfull: bool
  
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
  
  :arg qRotations: quaternion representing the rotation of the pattern (``default=quaternions.quaternion(1)``, i.e. no rotation)
  :type qRotations: :class:`quaternion <EBSDTools.mathTools.quaternions.quaternion>`  
  
  :arg patternSizeWidth: width of the pattern (in pixels) (``default=2680``)
  :type patternSizeWidth: int
  
  :arg patternSizeHeight: height of the pattern (in pixels) (``default=2040``)
  :type patternSizeHeight: int
  
  :arg patternCenterVisible: Draw the location of the pattern center? (``default=False``)
  :type patternCenterVisible: bool
  
  :arg colormode: either `'grayscale'` or `'RGB'`
  :type colormode: str
  
  :arg reflectorsInfo: list to return the info on the reflectors in the pattern. It should be pointing to an empty list.
  :type reflectorsInfo: list
    
  :rtype: :class:`ImageLine <RandomUtilities.DrawingTools.drawing.ImageLine>`
  """
  
  im = drawing.ImageLine(patternWidth, patternHeight, origin='center', colormode=colormode)
  
  #Add an uniform background
  if colormode == 'grayscale':
    im.drawGrayBrackground(color=1)
  elif colormode == 'RGB':
    im.drawGrayBrackground(color=(1,1,1))
    colorsList = colors.colorsList()
  
  reflectors = L.getReflectors()
  
  planes = reflectors.getReflectorsList()[:numberOfReflectors]
  planes.reverse()
  
#  print '-'*40
  
  for index, plane in enumerate(planes):
    qPlane = quaternions.quaternion(0, plane)
    planeRot = quaternions.rotate(qPlane, qRotations).vector()
    
    m, k = computePlaneEquationOnCamera(plane=planeRot
                                        , patternCenterX=patternCenterX
                                        , patternCenterY=patternCenterY
                                        , detectorDistance=detectorDistance)
    
    #Line parallel to the screen 
    if m == None and k == None:
      continue
    
#    print plane, m, k
    
    if bandedges or bandfull:
      x0 = vectors.vector(0,0,0)
      
      if m == None:
        x1 = vectors.vector(k, detectorDistance, 0.0)
        x2 = vectors.vector(k, detectorDistance, 0.1)
      elif abs(m) < zeroPrecision:
        x1 = vectors.vector(0.0, detectorDistance, k)
        x2 = vectors.vector(0.1, detectorDistance, k)
      else:
        x1 = vectors.vector(0.0, detectorDistance, k)
        if abs(k) > zeroPrecision:
          x2 = vectors.vector(-k/m, detectorDistance, 0.0)
        else: # abs(k) < zeroPrecision:
          x2 = vectors.vector((1-k)/m, detectorDistance, 1.0)
      
      n = vectors.cross(x2-x1, x1-x0)
      s = vectors.vector(n[0], 0, n[2])
      d = n.norm() / (x2-x1).norm()
      cosalpha = vectors.dot(n,s) / (n.norm()*s.norm())
      alpha = _acos(cosalpha)
      
      #Diffraction angle
      planeSpacing = reflectors.getReflectorPlaneSpacing(plane)
      wavelength = bragg.electronWavelength(energy)
      theta = bragg.diffractionAngle(planeSpacing, wavelength) 
      
      #Half-width of the band
      w = d * sin(theta) / cos(alpha-theta)
      w2 = d * sin(theta) / cos(alpha+theta)
    
    if colormode == 'RGB':
      baseColor = colorsList.getColorRGB(index)
    elif colormode == 'grayscale':
      baseColor = 255
    
    normalizedIntensity = reflectors.getReflectorNormalizedIntensity(plane)
    if intensity:
      if colormode == 'RGB':
        color = (int(baseColor[0]*normalizedIntensity), int(baseColor[1]*normalizedIntensity), int(baseColor[2]*normalizedIntensity))
      elif colormode == 'grayscale':
        color = int(baseColor*normalizedIntensity)
    else:
      color = baseColor
    
#    print plane, 'm', m, 'k', k#, 'd', d, 'theta', theta, 'w', w, 'alpha', cosalpha, 'g', grayLevel
    
    #Translation due to the pattern center
    if m != None:
      k += -m*patternCenterX + patternCenterY
    else:
      k += patternCenterX
    
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
      
      h = w/cos(beta)
      im.drawLinearFunction(m=m
                            , k=k+h
                            , color=color)
      
      h2 = w2/cos(beta)
      im.drawLinearFunction(m=m
                            , k=k-h2
                            , color=color)
    
    if bandfull:
      im.drawLinearFunction(m=m
                            , k=k
                            , thickness=int(2*w*patternWidth)
                            , color=color)
    
    if bandcenter or bandedges or bandfull:
      reflectorsInfo.append({'indices': plane, 'rgb': color, 'intensity': normalizedIntensity})
  #Mark the pattern center
  if patternCenterVisible:
    if colormode == 'RGB':
      im.drawCrossMarker(positionX=patternCenterX, positionY=patternCenterY, color=(255,255,255))
    elif colormode == 'grayscale':
      im.drawCrossMarker(positionX=patternCenterX, positionY=patternCenterY, color=255)
  
  return im()

def main():
  import EBSDTools.crystallography.lattice as lattice
  import EBSDTools.mathTools.eulers as eulers
  import os.path
  import rmlimage.io.IO as IO
  
#  #FCC
  atoms = {(0,0,0): 14,
           (0.5,0.5,0): 14,
           (0.5,0,0.5): 14,
           (0,0.5,0.5): 14}
#  atoms = {(0,0,0): 14,
#           (0.5,0.5,0.5): 14}
  L = lattice.Lattice(a=5.43, b=5.43, c=5.43, alpha=pi/2, beta=pi/2, gamma=pi/2, atoms=atoms, reflectorsMaxIndice=4)

  angles = eulers.eulers(0/180.0*pi, 0, 0) #z
  
  qSpecimenRotation = quaternions.quaternion(1,0,0,0)
  qCrystalRotation = quaternions.eulerAnglesToQuaternion(angles)
  qTilt = quaternions.axisAngleToQuaternion(-70/180.0*pi, (1,0,0))
  qDetectorOrientation = quaternions.axisAngleToQuaternion(90/180.0*pi, (1,0,0)) * quaternions.axisAngleToQuaternion(pi, (0,0,1))
  qDetectorOrientation = quaternions.quaternion(1,0,0,0)
  qDetectorOrientation_ = qTilt * qDetectorOrientation.conjugate() * qTilt.conjugate()
  
  qRotations = [qSpecimenRotation, qCrystalRotation, qTilt, qDetectorOrientation_]

  image = drawPattern(L
              , bandcenter=False
              , bandedges=False
              , bandfull=True
              , intensity=True
              , patternCenterX=0.0
              , patternCenterY=0.0
              , detectorDistance=0.4
              , energy=15e3
              , numberOfReflectors=32
              , qRotations=qRotations
              , patternWidth=335 
              , patternHeight=255
              , patternCenterVisible=True
              , colormode='grayscale')
    
#  image.show()
  image.setFile(r'test.bmp')
  
  IO.save(image)
  
if __name__ == '__main__':
  main()
  