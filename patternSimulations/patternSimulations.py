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
from math import pi

# Third party modules.

# Local modules.
import mathTools.quaternions as quaternions
import RandomUtilities.DrawingTools.drawing as drawing

def computePlaneEquationOnCamera(hkl
                                 , patternCenter=(0,0)
                                 , detectorDistance=1.0
                                 , tiltAngle=70/180.0*pi
                                 , tiltAxis=(1,0,0)):
  """
    Return the slope and intercept of the projection of a plane (hkl) 
      on a detector located at detectorDistance and patternCenter
    
    Inputs:
      hkl: a tuple of the three components of the diffracted plane
      patternCenter: tuple of the location of the pattern center [default=(0,0)]
      detectorDistance: distance between the sample and the detector window [default=1.0]
      tiltAngle: tilt angle of the specimen [default=1.21173rad (70deg)]
      tiltAxis: tilt axis of the specimen [default=(1,0,0) (x-axis)]
    
    Outputs:
      (m, b): a tuple with the slope m and y-intercept k
  """
  
  #Rotation of the plane by the tilt angle along the tilt axis
  R70 = quaternions.axisAngleToQuaternion(-tiltAngle, tiltAxis)
  hkl = quaternions.quaternion(0, hkl)
  
  hkl70 = R70 * hkl * R70.conjugate()
  
  #Calculation of the slope and intercept
  h70 = hkl70[1]
  k70 = hkl70[2]
  l70 = hkl70[3]
  
  if l70 != 0:
    m = -(h70/l70)
    k = (h70/l70)*patternCenter[0] - detectorDistance*k70/l70 + patternCenter[1]
  else:
    #TODO: verify
    m = None
    k = detectorDistance*k70/h70

  return m, k

def main():
  #FCC
  planes = [(1,-1,-1), (1,1,1), (1,1,-1), (1,-1,1),
            (2,-2,0), (2,0,-2), (0,2,-2), (2,2,0), (0,2,2), (2,0,2),
            (0,0,4), (4,0,0), (0,4,0)]
  
#  planes = [(1,-1,-1), (1,1,1), (1,1,-1), (1,-1,1), (-1,-1,1), (-1,1,-1), (-1,1,1),
#            (2,-2,0), (2,0,-2), (0,2,-2), (2,2,0), (0,2,2), (2,0,2),
#            (0,0,4), (4,0,0), (0,4,0)]
#            (1,1,3), (1,-3,1), (1,-1,-3), (1,1,-3), (1,-1,3), (1,-3,1), (3,-1,1), (3,1,1), (3,-1,-1), (1,3,-1), (1,3,1), (3,1,-1)]
  
  #BCC
#  planes = [(1,-1,0), (1,0,-1), (0,1,-1), (1,1,0), (0,1,1), (1,0,1),
#            (2,0,0), (0,2,0), (0,0,2),
#            (1,-1,2), (1,1,2), (1,-1,-2), (1,1,-2), (1,-2,1), (1,-2,-1), (2,1,1), (1,2,-1), (2,-1,1), (2,-1,-1), (2,1,-1), (1,2,1)]
  
  im = drawing.ImageLine(size=(335,255), origin='center')
  
  for plane in planes:
    m, k = computePlaneEquationOnCamera(hkl=plane
                         , patternCenter=(0,0)
                         , detectorDistance=0.1)
    im.drawLinearFunction(m=m
                          , k=k)
  
  im().show()

if __name__ == '__main__':
  main()
  print 
