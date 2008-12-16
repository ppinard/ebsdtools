#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Philippe Pinard (philippe.pinard@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2008 Philippe Pinard"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = ""
__svnDate__ = ""
__svnId__ = ""

# Standard library modules.
from math import pi, cos, atan, sqrt, tan,sin

# Third party modules.

# Local modules.
import EBSDTools.mathTools.quaternions as quaternions
import EBSDTools.mathTools.vectors as vectors
from EBSDTools.mathTools.mathExtras import zeroPrecision, _acos
import EBSDTools.crystallography.bragg as bragg
import RandomUtilities.DrawingTools.drawing as drawing
import RandomUtilities.DrawingTools.colors as colors
import EBSDTools.dev.orientation as orientation


def computePlaneEquationOnCamera(plane
                                 , patternCenter=(0,0)
                                 , detectorDistance=1.0
                                 ):
  """
    Return the slope and intercept of the projection of a plane (hkl) 
      on a detector located at detectorDistance and patternCenter
    
    Inputs:
      plane: a vector class of the diffracted plane
      patternCenter: tuple of the location of the pattern center [default=(0,0)]
      detectorDistance: distance between the sample and the detector window [default=1.0]
    
    Outputs:
      (m, b): a tuple with the slope m and y-intercept k
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
                , bandcenter=False
                , bandedges=True
                , bandfull=True
                , intensity=False
                , patternCenter=(0.0,0.0)
                , detectorDistance=0.3
                , energy=20e3
                , numberOfReflectors=32
                , qRotations=quaternions.quaternion(1)
                , patternSize=(2680,2040)
                , patternCenterVisible=True
                , colorMode=False
                , reflectorsInfo=[]):
  """
    Draw a pattern based on the crystallography and detector parameters
    
    Inputs:
      bandcenter: Draw the band center? (True or False)
      bandedges: Draw the band edges? (True or False)
      patternCenter: Coordonnates of the pattern center
      detectorDistance: distance of the detector
      energy: accelerating enerny (in eV)
      patternSize: tuple of the dimensions of the pattern (in pixels)
      patternCenterVisible: Draw the location of the pattern center? (True or False)
    
    Output:
      a ImageLine class (related to PIL.Image)
  """
  
  im = drawing.ImageLine(patternSize, origin='center')
  im.drawGrayBrackground(color=(1,1,1))
  colorsList = colors.colorsList()
  
  reflectors = L.getReflectors()
  
  planes = reflectors.getReflectorsList()[:numberOfReflectors]
  planes.reverse()
  
#  planes = [(1,-1,-1), 
#            (1,1,-1), 
#            (1,1,1), 
#            (1,-1,1), 
#            (2,-2,0), 
#            (2,0,-2), 
#            (0,2,-2), 
#            (2,2,0), 
#            (0,2,2), 
#            (2,0,2)]
  
  print '-'*40
  
  for index, plane in enumerate(planes):
#    print plane, reflectors.getReflectorNormalizedIntensity(plane)
    qPlane = quaternions.quaternion(0, plane)
    planeRot = quaternions.rotate(qPlane, qRotations).vector()
    
    m, k = computePlaneEquationOnCamera(plane=planeRot
                                        , patternCenter=patternCenter
                                        , detectorDistance=detectorDistance)
    
    if m == None and k == None:
      continue
    
    try:
      normal = orientation.kikuchiLineToNormal(m,k, patternCenter, detectorDistance)
    except:
      normal = []
    
    print plane, m, k, normal.positive()
    
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
    
    if colorMode:
      baseColor = colorsList.getColorRGB(index)
    else:
      baseColor = (255,255,255)
    
    normalizedIntensity = reflectors.getReflectorNormalizedIntensity(plane)
    if intensity:
      color = (baseColor[0]*normalizedIntensity, baseColor[1]*normalizedIntensity, baseColor[2]*normalizedIntensity)
    else:
      color = baseColor
    
#    print plane, 'm', m, 'k', k#, 'd', d, 'theta', theta, 'w', w, 'alpha', cosalpha, 'g', grayLevel
    
    #Translation due to the pattern center
    if m != None:
      k += -m*patternCenter[0] + patternCenter[1]
    else:
      k += patternCenter[0]
    
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
                            , width=2*w
                            , color=color)
    
    if bandcenter or bandedges or bandfull:
      reflectorsInfo.append({'indices': plane, 'rgb': color, 'intensity': normalizedIntensity})
  #Mark the pattern center
  if patternCenterVisible:
    im.drawCrossMarker(position=patternCenter, color=(255,255,255))
  
  return im()

def main():
  import EBSDTools.crystallography.lattice as lattice
  import EBSDTools.mathTools.eulers as eulers
  import os.path
  
#  #FCC
  atoms = {(0,0,0): 14,
           (0.5,0.5,0): 14,
           (0.5,0,0.5): 14,
           (0,0.5,0.5): 14}
#  atoms = {(0,0,0): 14,
#           (0.5,0.5,0.5): 14}
  L = lattice.Lattice(a=5.43, b=5.43, c=5.43, alpha=pi/2, beta=pi/2, gamma=pi/2, atoms=atoms, reflectorsMaxIndice=4)
  #BCC
#  atoms = {(0,0,0): 14,
#           (0.5,0.5,0.5): 14}
#  L = lattice.Lattice(a=5.43, b=5.43, c=5.43, alpha=pi/2, beta=pi/2, gamma=pi/2, atoms=atoms, reflectorsMaxIndice=2)
#  #HCP
#  L = lattice.Lattice(a=2, b=2, c=4, alpha=pi/2, beta=pi/2, gamma=120.0/180*pi, atomPositions=[])

#  for n in range(0,95, 5):
  for n in [0]:
#    angles = eulers.fromHKLeulers(-pi/2.0, theta/180.0*pi, pi/2.0) #y
    angles = eulers.negativeEulers(n/180.0*pi, 0, 0) #z
#    angles = eulers.negativeEulers(0, 0.0*n/180.0*pi, 0) #x
    angles = eulers.negativeEulers(261.155/180.0*pi, 4.593/180.0*pi, 0.222/180.0*pi) 
    print n
    
    qSpecimenRotation = quaternions.quaternion(1,0,0,0)
    qCrystalRotation = quaternions.eulerAnglesToQuaternion(angles)
    qTilt = quaternions.axisAngleToQuaternion(-70/180.0*pi, (1,0,0))
    qDetectorOrientation = quaternions.axisAngleToQuaternion(90/180.0*pi, (1,0,0)) * quaternions.axisAngleToQuaternion(pi, (0,0,1))
#    qDetectorOrientation = quaternions.quaternion(1,0,0,0)
    qDetectorOrientation_ = qTilt * qDetectorOrientation.conjugate() * qTilt.conjugate()
    
    qRotations = [qSpecimenRotation, qCrystalRotation, qTilt, qDetectorOrientation_]
#    print qRotations
    
    image = drawPattern(L
                , bandcenter=False
                , bandedges=False
                , bandfull=True
                , intensity=False
                , patternCenter=(0.4,0.4)
                , detectorDistance=0.4
                , energy=15e3
                , numberOfReflectors=25
                , qRotations=qRotations
                , patternSize=(335 ,255)
                , patternCenterVisible=True
                , colorMode=False)
    
    folder = 'c:/documents/workspace/EBSDTools/patternSimulations/rotation'
#    folder = 'I:/Philippe Pinard/workspace/EBSDTools/patternSimulations/comparison'
    imageName = '%s_%3i.bmp' % ('test_2', n)
    imageName = imageName.replace(' ', '0')
    image.save(os.path.join(folder, imageName))
  

if __name__ == '__main__':
  main()
  