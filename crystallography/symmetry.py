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

# Third party modules.

# Local modules.
import EBSDTools.mathTools.quaternions as quaternions
from math import sqrt

def cubicSymmetries():
  sr2 = sqrt(2) / 2.0
  qSymmetries = []
  
  qSymmetries.append(quaternions.quaternion(1,0,0,0))
  
  #Three-fold
  qSymmetries.append(quaternions.quaternion( 0.5, 0.5, 0.5, 0.5))
  qSymmetries.append(quaternions.quaternion( 0.5,-0.5,-0.5, 0.5))
  qSymmetries.append(quaternions.quaternion( 0.5, 0.5,-0.5,-0.5))
  qSymmetries.append(quaternions.quaternion( 0.5,-0.5, 0.5,-0.5))
  
  qSymmetries.append(quaternions.quaternion( 0.5,-0.5,-0.5,-0.5))
  qSymmetries.append(quaternions.quaternion( 0.5,-0.5, 0.5, 0.5))
  qSymmetries.append(quaternions.quaternion( 0.5, 0.5,-0.5, 0.5))
  qSymmetries.append(quaternions.quaternion( 0.5, 0.5, 0.5,-0.5))
  
  #Two-fold
  qSymmetries.append(quaternions.quaternion( 0.0, 0.0, 1.0, 0.0))
  qSymmetries.append(quaternions.quaternion( 0.0, 0.0, 0.0, 1.0))
  qSymmetries.append(quaternions.quaternion( 0.0, 1.0, 0.0, 0.0))
  
  #Four-fold
  qSymmetries.append(quaternions.quaternion( 0.0,-sr2, 0.0, sr2))
  qSymmetries.append(quaternions.quaternion( 0.0, sr2, 0.0, sr2))
  qSymmetries.append(quaternions.quaternion( sr2, 0.0, sr2, 0.0))
  qSymmetries.append(quaternions.quaternion( sr2, 0.0,-sr2, 0.0))
  
  qSymmetries.append(quaternions.quaternion( 0.0, 0.0,-sr2, sr2))
  qSymmetries.append(quaternions.quaternion( sr2, sr2, 0.0, 0.0))
  qSymmetries.append(quaternions.quaternion( sr2,-sr2, 0.0, 0.0))
  qSymmetries.append(quaternions.quaternion( 0.0, 0.0, sr2, sr2))
  
  qSymmetries.append(quaternions.quaternion( 0.0,-sr2, sr2, 0.0))
  qSymmetries.append(quaternions.quaternion( sr2, 0.0, 0.0,-sr2))
  qSymmetries.append(quaternions.quaternion( 0.0, sr2, sr2, 0.0))
  qSymmetries.append(quaternions.quaternion( sr2, 0.0, 0.0, sr2))

  return qSymmetries
  
if __name__ == '__main__':
  pass
  