#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Philippe Pinard (philippe.pinard@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2008 Philippe Pinard"
__license__ = ""
__reference__ = "Altmann (1986) Rotation, Quaternions and Double Groups"

# Subversion informations for the file.
__svnRevision__ = ""
__svnDate__ = ""
__svnId__ = ""

# Standard library modules.
from math import pi, cos, atan, sqrt, tan

# Third party modules.

# Local modules.
import mathTools.quaternions as quaternions
import mathTools.vectors as vectors
from mathTools.mathExtras import zeroPrecision
import crystallography.bragg as bragg
import RandomUtilities.DrawingTools.drawing as drawing

def tiltSpecimen(plane
                , tiltAngle=70/180.0*pi
                , tiltAxis=(1,0,0)):
  """
    Return a rotated plane by the tiltAngle along the tiltAxis
    
    Inputs:
      plane : a vector class of the diffracted plane
      tiltAngle: tilt angle of the specimen [default=1.21173rad (70deg)]
      tiltAxis: tilt axis of the specimen [default=(1,0,0) (x-axis)]
    
    Outputs:
      vector
  """
  
  R70 = quaternions.axisAngleToQuaternion(-tiltAngle, tiltAxis)
  hkl = quaternions.quaternion(0, plane)
  
  hkl70 = R70 * hkl * R70.conjugate()
  
  return hkl70.vector()

def rotateSpecimen(plane
                   , rotationQuaternion):
  hkl = quaternions.quaternion(0, plane)
  
  hklRot = rotationQuaternion * hkl * rotationQuaternion.conjugate()
  
  return hklRot.vector()

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
  
  h = plane[0]
  k = plane[1]
  l = plane[2]
  
  if abs(l) > zeroPrecision:
    m = -(h/l)
    b = (h/l)*patternCenter[0] - detectorDistance*k/l + patternCenter[1]
  else:
    if abs(h) > zeroPrecision:
      m = None
      b = detectorDistance*k/h
    else: #Plane parallel to the screen
      m = None
      b = None

  return m, b

def drawPattern(L
                , bandcenter=False
                , bandedges=True
                , bandfull=True
                , intensity=False
                , patternCenter=(0.0,0.0)
                , detectorDistance=0.3
                , energy=20e3
                , specimenRotation=quaternions.quaternion(1)
                , patternSize=(2680,2040)
                , patternCenterVisible=True):
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
  
  #Mark the pattern center
  if patternCenterVisible:
    im.draw.ellipse((patternSize[0]/2.0-20+patternCenter[0],patternSize[1]/2.0-20+patternCenter[1] \
                     ,patternSize[0]/2.0+20+patternCenter[0],patternSize[1]/2.0+20+patternCenter[1]), fill=255)
  
  reflectors = L.getReflectors()
  
  planes = reflectors.getReflectorsList()
  planes.reverse()
  
  for plane in planes:
    planeRot = rotateSpecimen(plane, specimenRotation)
    planeTilt = tiltSpecimen(planeRot, tiltAngle=70*pi/180, tiltAxis=(1,0,0))
    
    m, b = computePlaneEquationOnCamera(plane=planeTilt
                                        , patternCenter=patternCenter
                                        , detectorDistance=detectorDistance)
    
    if m == None and b == None:
      continue
    
    if bandedges or bandfull:
      #Distance from the sample to the screen at x = 0
      d = vectors.vector(-patternCenter[0], detectorDistance, b-patternCenter[1]).norm()
      
      x0 = vectors.vector(0,0,0)
      x1 = vectors.vector(0.0, detectorDistance, b)
      if m == None or abs(m) < zeroPrecision:
        x2 = vectors.vector(0.0, detectorDistance, b+0.1)
      else:
        if abs(b) > zeroPrecision:
          x2 = vectors.vector(-b/m, detectorDistance, 0.0)
        else: # abs(b) < zeroPrecision:
          x2 = vectors.vector((1-b)/m, detectorDistance, 1.0)
      
      n = vectors.cross(x2-x1, x1-x0)
      s = vectors.vector(n[0], 0, n[2])
      d = n.norm() / (x2-x1).norm()
      cosalpha = vectors.dot(n,s) / (n.norm()*s.norm())
      
      #Diffraction angle
      planeSpacing = reflectors.getReflectorPlaneSpacing(plane)
      wavelength = bragg.electronWavelength(energy)
      theta = bragg.diffractionAngle(planeSpacing, wavelength) 
      
      #Half-width of the band
#      w = sqrt(2*d**2*(1-cos(theta)))
      w = d*tan(theta) / cosalpha
      
    if intensity:
      grayLevel = reflectors.getReflectorNormalizedIntensity(plane) * 255
    else:
      grayLevel = 255
    
#    print plane, 'm', m, 'b', b, 'd', d, 'theta', theta, 'w', w, 'g', grayLevel
    
    if bandcenter:
      im.drawLinearFunction(m=m
                            , k=b
                            , grayLevel=grayLevel)
    
    if bandedges:
      #Correction for the slope of the band
      v = x2-x1
      if abs(v[0]) > zeroPrecision:
        alpha = atan(v[2]/v[0])
      else:
        alpha = 0.0
      
      h = w*cos(alpha)
      
      im.drawLinearFunction(m=m
                            , k=b+h
                            , grayLevel=grayLevel)
      im.drawLinearFunction(m=m
                            , k=b-h
                            , grayLevel=grayLevel)
    
    if bandfull:
      im.drawLinearFunction(m=m
                            , k=b
                            , width=int(2*w*patternSize[1]*1)
                            , grayLevel=grayLevel)
    
  return im()

def main():
  import crystallography.lattice as lattice
  import PIL.ImageEnhance



  
#  #FCC
  atoms = {(0,0,0): 14,
           (0.5,0.5,0): 14,
           (0.5,0,0.5): 14,
           (0,0.5,0.5): 14}
  atoms = {(0,0,0): 14,
           (0.5,0.5,0.5): 14}
  L = lattice.Lattice(a=5.43, b=5.43, c=5.43, alpha=pi/2, beta=pi/2, gamma=pi/2, atoms=atoms, reflectorsMaxIndice=2)
  #BCC
#  atoms = {(0,0,0): 14,
#           (0.5,0.5,0.5): 14}
#  L = lattice.Lattice(a=5.43, b=5.43, c=5.43, alpha=pi/2, beta=pi/2, gamma=pi/2, atoms=atoms, reflectorsMaxIndice=2)
#  #HCP
#  L = lattice.Lattice(a=2, b=2, c=4, alpha=pi/2, beta=pi/2, gamma=120.0/180*pi, atomPositions=[])


#  for plane in L.planes:
#    print plane, L.planes[plane]['intensity']
  
  
#  planes = [(1,-1,-1), (1,1,1), (1,1,-1), (1,-1,1),
#            (2,-2,0), (2,0,-2), (0,2,-2), (2,2,0), (0,2,2), (2,0,2),
#            (0,0,4), (4,0,0), (0,4,0)]
#  
##  planes = [(2,0,2),(2,0,-2)]
  
  rotation = quaternions.eulerAnglesToQuaternion(0,0,0)
  
  image = drawPattern(L
              , bandcenter=False
              , bandedges=False
              , bandfull=True
              , intensity=True
              , patternCenter=(0,0)
              , detectorDistance=0.3
              , energy=20e3
              , specimenRotation=rotation
              , patternSize=(2680,2040)
              , patternCenterVisible=True)
  
  image.show()

if __name__ == '__main__':
  main()
  