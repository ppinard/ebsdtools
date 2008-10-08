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
import mathTools.vectors as vectors
import reciprocal
import lattice

def _computeStructureFactor(plane, atomPositions):
  
  sum = 0
  
  for atomPosition in atomPositions:
    sum += (-1)**(2*vectors.dot(plane, atomPosition))
  return sum

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

def _areEquivalent(plane1, plane2, L):
  angle = reciprocal.interplanarAngle(plane1, plane2, L)
  
  if angle < 1e-5 or abs(angle - pi) < 1e-5:
    if abs(plane1[0]) == abs(plane2[0]):
      return True
    else:
      return False
  else:
    return False

def findReflectors(L, maxIndice=2):
  reflectors = []
  
  for h in range(-maxIndice, maxIndice+1):
    for k in range(-maxIndice, maxIndice+1):
      for l in range(-maxIndice, maxIndice+1):
        plane = _positiveIndices((h,k,l))
        
        if not plane == (0,0,0): #Remove plane (0,0,0)
          if _computeStructureFactor(plane, L.atomPositions) != 0:
            for reflector in reflectors:
              if _areEquivalent(plane, reflector, L):
                plane = None
                break
                
            if plane != None:
              reflectors.append(plane)
  
  reflectors.sort()
  return reflectors
  
if __name__ == '__main__':
  atomPositions = [(0,0,0), (0,.5,.5), (.5,0,.5), (.5,.5,0)]
  
  L = lattice.Lattice(a=2, b=2, c=2, alpha=pi/2, beta=pi/2, gamma=pi/2, atomPositions=atomPositions)
  L.calculatePlaneSpacing(reflectorsMaxIndice=5)
  print len(L.reflectors)
#  print L.planeSpacings
  
  