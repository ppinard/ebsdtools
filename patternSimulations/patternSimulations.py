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
from math import pi, cos, atan, sqrt, tan,sin

# Third party modules.

# Local modules.
import EBSDTools.mathTools.quaternions as quaternions
import EBSDTools.mathTools.vectors as vectors
from EBSDTools.mathTools.mathExtras import zeroPrecision, _acos
import EBSDTools.crystallography.bragg as bragg
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
  im.drawGrayBrackground(grayLevel=1)
  
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
      
    if intensity:
      grayLevel = reflectors.getReflectorNormalizedIntensity(plane) * 255
    else:
      grayLevel = 255
    
#    print plane, 'm', m, 'k', k#, 'd', d, 'theta', theta, 'w', w, 'alpha', cosalpha, 'g', grayLevel
    
    #Translation due to the pattern center
    if m != None:
      k += -m*patternCenter[0] + patternCenter[1]
    else:
      k += patternCenter[0]
    
    if bandcenter:
      im.drawLinearFunction(m=m
                            , k=k
                            , grayLevel=grayLevel)
    
    if bandedges:
      #Correction for the slope of the band
      if m != None:
        alpha = atan(m)
      else:
        alpha = 0.0
      
      h = w*cos(alpha)
      im.drawLinearFunction(m=m
                            , k=k+h
                            , grayLevel=grayLevel)
      
      h2 = w2*cos(alpha)
      im.drawLinearFunction(m=m
                            , k=k-h2
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
  import EBSDTools.crystallography.lattice as lattice
  import PIL.ImageEnhance
  import EBSDTools.mathTools.eulers as eulers
  import os.path
  
#  #FCC
  atoms = {(0,0,0): 14,
           (0.5,0.5,0): 14,
           (0.5,0,0.5): 14,
           (0,0.5,0.5): 14}
#  atoms = {(0,0,0): 14,
#           (0.5,0.5,0.5): 14}
  L = lattice.Lattice(a=5.43, b=5.43, c=5.43, alpha=pi/2, beta=pi/2, gamma=pi/2, atoms=atoms, reflectorsMaxIndice=1)
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
#  q1 = quaternions.axisAngleToQuaternion(pi/2.0, (0,0,1))
#  q2 = quaternions.axisAngleToQuaternion(pi/2.0, (1,0,0))
#  
#  qOut1 = quaternions.rotate(q, [q1])
#  print quaternions.rotate(qOut1, [q2])
#  print quaternions.rotate(q, [q1,q2])
#  print quaternions.rotate(q, [q2,q1])
  
  
  
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
  
  
#  print q1 * q1.conjugate(), q1.conjugate() * q1
  
#  for n in range(0,95, 5):
  for n in range(0, 1, 1):
#    angles = eulers.fromHKLeulers(-pi/2.0, theta/180.0*pi, pi/2.0) #y
#    angles = eulers.negativeEulers(theta/180.0*pi, 0, 0) #z
    angles = eulers.negativeEulers(0, 0.0*n/180.0*pi, 0) #x
    print n
    
    qSpecimenRotation = quaternions.quaternion(1,0,0,0)
    qCrystalRotation = quaternions.eulerAnglesToQuaternion(angles)
    qTilt = quaternions.axisAngleToQuaternion(-0/180.0*pi, (1,0,0))
    qDetectorOrientation = quaternions.axisAngleToQuaternion(90/180.0*pi, (1,0,0)) * quaternions.axisAngleToQuaternion(pi, (0,0,1))
    qDetectorOrientation = quaternions.quaternion(1,0,0,0)
    qDetectorOrientation_ = qTilt * qDetectorOrientation.conjugate() * qTilt.conjugate()
    
    qRotations = [qSpecimenRotation, qCrystalRotation, qTilt, qDetectorOrientation_]
#    print qRotations
    
    image = drawPattern(L
                , bandcenter=False
                , bandedges=False
                , bandfull=True
                , intensity=False
                , patternCenter=(0.0,n/10.0)
                , detectorDistance=0.3
                , energy=20e3
                , qRotations=qRotations
                , patternSize=(335 ,255)
                , patternCenterVisible=False)
    
    folder = 'c:/documents/workspace/EBSDTools/patternSimulations/rotation'
#    folder = 'I:/Philippe Pinard/workspace/EBSDTools/patternSimulations/rotation'
    imageName = '%s_%3i.bmp' % ('m', n)
    imageName = imageName.replace(' ', '0')
    image.save(os.path.join(folder, imageName))
  

if __name__ == '__main__':
  main()
  