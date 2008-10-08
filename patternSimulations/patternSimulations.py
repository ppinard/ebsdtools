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
from math import pi, cos, atan, sqrt

# Third party modules.

# Local modules.
import mathTools.quaternions as quaternions

import crystallography.bragg as bragg
import mathTools.vectors as vectors
import RandomUtilities.DrawingTools.drawing as drawing

def rotatePlane(plane
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
  
  if l != 0:
    m = -(h/l)
    b = (h/l)*patternCenter[0] - detectorDistance*k/l + patternCenter[1]
  else:
    #TODO: verify
    m = None
    b = detectorDistance*k/h

  return m, b

def drawPattern(L
                , bandcenter=False
                , bandedges=True
                , bandfull=True
                , patternCenter=(0.0,0.0)
                , detectorDistance=0.3
                , energy=20e3
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
  
  for plane in L.planes:
    planeRot = rotatePlane(plane)
    
    m, b = computePlaneEquationOnCamera(plane=planeRot
                                        , patternCenter=patternCenter
                                        , detectorDistance=detectorDistance)
    
    if bandedges or bandfull:
      #Distance from the sample to the screen at z = b
      d = vectors.vector(0,detectorDistance,b).norm()
      
      #Diffraction angle
      planeSpacing = L.planes[plane]['plane spacing']
      wavelength = bragg.electronWavelength(energy)
      theta = bragg.diffractionAngle(planeSpacing, wavelength) 
      
      #Width of the band
      w = sqrt(2*d**2*(1-cos(theta)))
      
      #Create the line representing the width of the band
#      if planeRot[2] != 0:
#        alpha = atan(planeRot[0] /planeRot[2])
#        h = w / cos(alpha)
#      else:
#        h = w
      
      h = w
      
  #    print plane, 'd', planeSpacing, 'w', w, 'h', h, 'alpha', alpha
    
    if bandcenter:
      im.drawLinearFunction(m=m
                            , k=b)
    
    if bandedges:
      im.drawLinearFunction(m=m
                            , k=b+h)
      im.drawLinearFunction(m=m
                            , k=b-h)
    
    if bandfull:
      im.drawLinearFunction(m=m
                            , k=b
                            , width=int(2*h*patternSize[1]*1))
  
  return im()

def main():
  import crystallography.lattice as lattice
  
#  #FCC
#  L = lattice.Lattice(a=5.43, b=5.43, c=5.43, alpha=pi/2, beta=pi/2, gamma=pi/2, atomPositions=[(0,0,0), (0,.5,.5), (.5,0,.5), (.5,.5,0)])
  #BCC
  L = lattice.Lattice(a=5.43, b=5.43, c=5.43, alpha=pi/2, beta=pi/2, gamma=pi/2, atomPositions=[(0,0,0), (.5,.5,.5)])
#  #HCP
#  L = lattice.Lattice(a=2, b=2, c=4, alpha=pi/2, beta=pi/2, gamma=120.0/180*pi, atomPositions=[])
  L.calculatePlanes(reflectorsMaxIndice=2)
#  for plane in L.planes:
#    print plane, L.planes[plane]['intensity']
  
  
#  planes = [(1,-1,-1), (1,1,1), (1,1,-1), (1,-1,1),
#            (2,-2,0), (2,0,-2), (0,2,-2), (2,2,0), (0,2,2), (2,0,2),
#            (0,0,4), (4,0,0), (0,4,0)]
#  
##  planes = [(2,0,2),(2,0,-2)]
  
  drawPattern(L
              , bandcenter=False
              , bandedges=False
              , bandfull=True
              , patternCenter=(0,0)
              , detectorDistance=0.3
              , energy=20e3
              , patternSize=(2680,2040)
              , patternCenterVisible=False).show()

if __name__ == '__main__':
  main()
  
