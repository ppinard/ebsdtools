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
      b = -detectorDistance*k/h + patternCenter[0]
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
                , qRotations=quaternions.quaternion(1)
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
  
  reflectors = L.getReflectors()
  
  planes = reflectors.getReflectorsList()
  planes.reverse()
  
  for plane in planes:
    qPlane = quaternions.quaternion(0, plane)
    planeRot = quaternions.rotate(qPlane, qRotations).vector()
    
    m, k = computePlaneEquationOnCamera(plane=planeRot
                                        , patternCenter=patternCenter
                                        , detectorDistance=detectorDistance)
    
    if m == None and k == None:
      continue
    
    if bandedges or bandfull:
      #Distance from the sample to the screen at x = 0
      d = vectors.vector(-patternCenter[0], detectorDistance, k-patternCenter[1]).norm()
      
      x0 = vectors.vector(0,0,0)
      
      if m == None or abs(m) < zeroPrecision:
        x1 = vectors.vector(k, detectorDistance, 0.0)
        x2 = vectors.vector(k, detectorDistance, 0.1)
      else:
        x1 = vectors.vector(0.0, detectorDistance, k)
        if abs(k) > zeroPrecision:
          x2 = vectors.vector(-k/m, detectorDistance, 0.0)
        else: # abs(b) < zeroPrecision:
          x2 = vectors.vector((1-k)/m, detectorDistance, 1.0)
      
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
    
#    print plane, 'm', m, 'k', k, 'd', d, 'theta', theta, 'w', w, 'alpha', cosalpha, 'g', grayLevel
    
    if bandcenter:
      im.drawLinearFunction(m=m
                            , k=k
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
                            , k=k+h
                            , grayLevel=grayLevel)
      im.drawLinearFunction(m=m
                            , k=k-h
                            , grayLevel=grayLevel)
    
    if bandfull:
      im.drawLinearFunction(m=m
                            , k=k
                            , width=2*w
                            , grayLevel=grayLevel)
  
  #Mark the pattern center
  if patternCenterVisible:
    im.draw.ellipse((patternSize[0]/2.0-20+patternCenter[0],patternSize[1]/2.0-20+patternCenter[1] \
                     ,patternSize[0]/2.0+20+patternCenter[0],patternSize[1]/2.0+20+patternCenter[1]), fill=255)
  
  return im()

def main():
  import crystallography.lattice as lattice
  import PIL.ImageEnhance
  import mathTools.eulers as eulers
  import os.path

  
#  #FCC
  atoms = {(0,0,0): 14,
           (0.5,0.5,0): 14,
           (0.5,0,0.5): 14,
           (0,0.5,0.5): 14}
#  atoms = {(0,0,0): 14,
#           (0.5,0.5,0.5): 14}
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
  
  q = quaternions.quaternion(0, 1, 0, 0)
#  
#  q1 = quaternions.eulerAnglesToQuaternion(50,34,56)
#  q2 = quaternions.eulerAnglesToQuaternion(60, 80, 152)
#  q3 = quaternions.eulerAnglesToQuaternion(150,0,12)
#  
#  qq1 = quaternions.rotate(q, [q1])
#  qq1q2 = quaternions.rotate(qq1, [q2])
#  qq1q2q3 = quaternions.rotate(qq1q2, [q3])
#  
#  print qq1q2q3
#  
#  print quaternions.rotate(q, [q1,q2,q3])
#  print quaternions.rotate(q, [q3,q2,q1])
  
  qTilt = quaternions.axisAngleToQuaternion(-90/180.0*pi, (0,1,0))
  qDetectorOrientation = quaternions.eulerAnglesToQuaternion(eulers.fromHKLeulers(0.0/180.0*pi, 0.0/180.0*pi, 0.0/180.0*pi)).conjugate()
  
  qDetectorOrientation_ = qTilt * qDetectorOrientation * qTilt.conjugate()
  
  
  for theta in range(0,90, 5):
#    angles = eulers.fromHKLeulers(-pi/2.0, theta/180.0*pi, pi/2.0) #y
    angles = eulers.fromHKLeulers(theta/180.0*pi, 0, 0) #z
#    angles = eulers.fromHKLeulers(0, theta/180.0*pi, 0) #x
    print theta
    
    qSpecimenRotation = quaternions.eulerAnglesToQuaternion(angles)
    
    qRotations = [qSpecimenRotation, qTilt, qDetectorOrientation_]
    
    image = drawPattern(L
                , bandcenter=False
                , bandedges=False
                , bandfull=True
                , intensity=True
                , patternCenter=(0,0)
                , detectorDistance=0.3
                , energy=20e3
                , qRotations=qRotations
                , patternSize=(2680 ,2040)
                , patternCenterVisible=True)
    
    folder = 'c:/documents/workspace/EBSDTools/patternSimulations/rotation'
    imageName = '%s_%3i.jpg' % ('theta2', theta)
    imageName = imageName.replace(' ', '0')
    image.save(os.path.join(folder, imageName))
  

if __name__ == '__main__':
  main()
  