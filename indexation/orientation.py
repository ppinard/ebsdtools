#!/usr/bin/env jython
""" """

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
from math import atan2, acos, sqrt

# Third party modules.

# Local modules.
import EBSDTools.mathTools.quaternions as quaternions
import EBSDTools.mathTools.matrices as matrices
import EBSDTools.mathTools.vectors as vectors
import EBSDTools.mathTools.eulers as eulers

def calculateOrientation(n1, n2, hkl1, hkl2):
  eP1 = n1 / n1.norm()
  eP2 = vectors.cross(n1, n2)
  eP2 /= eP2.norm()
  eP3 = vectors.cross(eP1, eP2).normalize()
  
  mP = matrices.matrix([[eP1[0], eP2[0], eP3[0]],
                        [eP1[1], eP2[1], eP3[1]],
                        [eP1[2], eP2[2], eP3[2]]])
  
  qP = quaternions.matrixtoQuaternion(mP)
  
  eC1 = hkl1 / hkl1.norm()
  eC2 = vectors.cross(hkl1, hkl2)
  eC2 /= eC2.norm()
  eC3 = vectors.cross(eC1, eC2).normalize()
  
  mC = matrices.matrix([[eC1[0], eC2[0], eC3[0]],
                        [eC1[1], eC2[1], eC3[1]],
                        [eC1[2], eC2[2], eC3[2]]])
  
  qC = quaternions.matrixtoQuaternion(mC) 
  
  q = qC.conjugate() * qP
  
  return q.conjugate()

def calculateOrientationWright(n1, n2, hkl1, hkl2):
  mag = 2*vectors.dot(n1,n2)
  mag0 = 1.0/sqrt(2.0+mag)
  mag1 = 1.0/sqrt(2.0-mag)
  
  es0 = (n1+n2)*mag0
  es1 = (n1-n2)*mag1
  es2 = vectors.cross(es0, es1)
  
  mag0 = 1.0/sqrt(vectors.dot(hkl1, hkl1))
  mag1 = 1.0/sqrt(vectors.dot(hkl2, hkl2))
  hkl1 *= mag0
  hkl2 *= mag1
  
  mag = 2.0*vectors.dot(hkl1, hkl2)
  mag0 = 1.0/sqrt(2.0+mag)
  mag1 = 1.0/sqrt(2.0-mag)
  
  ec0 = (hkl1+hkl2)*mag0
  ec1 = (hkl1-hkl2)*mag1
  ec2 = vectors.cross(ec0, ec1)
  
  m = matrices.matrix()
  for i in range(3):
    for j in range(3):
      m[j][i] = ec0[i]*es0[j] + ec1[i]*es1[j] + ec2[i]*es2[j]
  
  m = matrices.transpose(m)
  q = quaternions.matrixtoQuaternion(m)
  
  return q 
  