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
from math import sin, cos, pi, acos, atan2, exp, sqrt

# Third party modules.

# Local modules.
import mathTools.vectors

def _computeStructureFactor(plane, atomPositions):
  
  sum = 0
  
  for atomPosition in atomPositions:
#    print atomPosition, (-1)**(2*mathTools.quaternions._dotproduct(plane, atomPosition))
    sum += (-1)**(2*mathTools.vectors.dotproduct(plane, atomPosition))
  return sum

def _greatestCommonDivisor(a, b):
  """
    Return the greatest common divisor between a and b
    Definition: the largest positive integer that divides both numbers without remainder (wikipedia)
    Source: ?
    
    Inputs:
      a,b: integers
    
    Outputs:
      integer
  """
  
  if a == 0 or b == 0:
    return None
  
  while a % b != 0:
    a, b = round(b), round(a % b)

  return int(b)

def _positiveIndices(plane):
  h = plane[0]
  k = plane[1]
  l = plane[2]
  
  #h always greater than 0
  if h < 0:
    h = -h
    k = -k
    l = -l
  elif h == 0 and k < 0:
    h = 0
    k = -k
    l = -l
  elif h == 0 and k == 0 and l <0:
    h = 0
    k = 0
    l = -l
  
  return (h,k,l)

def _angleBetweenPlanes(n1, n2):
  norm1 = sqrt(n1[0]**2 + n1[1]**2 + n1[2]**2)
  norm2 = sqrt(n2[0]**2 + n2[1]**2 + n2[2]**2)
  dot = mathTools.vectors.dotproduct(n1, n2)
  
  costheta = dot / (norm1 * norm2)
  
  if costheta >= 1.0:
    return 0
  elif costheta <= -1.0:
    return pi
  else:
    return acos(dot / norm1 / norm2)

def _areEquivalent(plane1, plane2):
  angle = _angleBetweenPlanes(plane1, plane2)
  
  if angle < 1e-5 or abs(angle - pi) < 1e-5:
    if abs(plane1[0]) == abs(plane2[0]):
      return True
    else:
      return False
  else:
    return False

def findReflectors(atomPositions, maxIndice=2):
  reflectors = []
  
  for h in range(-maxIndice, maxIndice+1):
    for k in range(-maxIndice, maxIndice+1):
      for l in range(-maxIndice, maxIndice+1):
        plane = _positiveIndices((h,k,l))
        
        if not plane == (0,0,0):
          if _computeStructureFactor(plane, atomPositions) != 0:
            for reflector in reflectors:
              if _areEquivalent(plane, reflector):
                plane = None
                break
                
            if plane != None:
              reflectors.append(plane)
  
  reflectors.sort()
  return reflectors
  
if __name__ == '__main__':
  atomPositions = [(0,0,0), (0,.5,.5), (.5,0,.5), (.5,.5,0)]
  
  print findReflectors(atomPositions, maxIndice=2)
  