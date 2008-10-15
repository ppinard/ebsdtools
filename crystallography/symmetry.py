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

# Third party modules.

# Local modules.
import EBSDTools.mathTools.quaternions as quaternions

def cubic(plane):
  #Six diads about <100>
#  qSymmetries = []
#  qSymmetries.append(quaternions.quaternion(1,0,0,0))
#  qSymmetries.append(quaternions.quaternion(-1,0,0,0))
#  qSymmetries.append(quaternions.quaternion(0,1,0,0))
#  qSymmetries.append(quaternions.quaternion(0,-1,0,0))
#  qSymmetries.append(quaternions.quaternion(0,0,1,0))
#  qSymmetries.append(quaternions.quaternion(0,0,-1,0))
  pass
  
if __name__ == '__main__':
  planes = [(1, 1, 1), (-1, -1, 1), (-1, 1, -1), (-1, 1, 1), (1, -1, -1), (1, -1, 1), (1, 1, -1)]
  planes = [(1,1,1)]
  
  qs = []
  
  #Three-fold
  qs.append(quaternions.matrixtoQuaternion([[1,0,0], [0,1,0], [0,0,1]]))
  
  qs.append(quaternions.matrixtoQuaternion([[0,0,1], [1,0,0], [0,1,0]]))
  qs.append(quaternions.matrixtoQuaternion([[0,0,-1], [1,0,0], [0,-1,0]]))
  qs.append(quaternions.matrixtoQuaternion([[0,0,-1], [-1,0,0], [0,1,0]]))
  qs.append(quaternions.matrixtoQuaternion([[0,0,1], [-1,0,0], [0,-1,0]]))
#  
  qs.append(quaternions.matrixtoQuaternion([[0,1,0], [0,0,1], [1,0,0]]))
  qs.append(quaternions.matrixtoQuaternion([[0,-1,0], [0,0,1], [-1,0,0]]))
  qs.append(quaternions.matrixtoQuaternion([[0,-1,0], [0,0,-1], [1,0,0]]))
  qs.append(quaternions.matrixtoQuaternion([[0,1,0], [0,0,-1], [-1,0,0]]))
  
  #Two-fold
  qs.append(quaternions.matrixtoQuaternion([[-1,0,0], [0,1,0], [0,0,-1]]))
  qs.append(quaternions.matrixtoQuaternion([[-1,0,0], [0,-1,0], [0,0,1]]))
  qs.append(quaternions.matrixtoQuaternion([[1,0,0], [0,-1,0], [0,0,-1]]))
  
  #Four-fold
  qs.append(quaternions.matrixtoQuaternion([[0,0,-1], [0,-1,0], [-1,0,0]]))
  qs.append(quaternions.matrixtoQuaternion([[0,0,1], [0,-1,0], [1,0,0]]))
  qs.append(quaternions.matrixtoQuaternion([[0,0,1], [0,1,0], [-1,0,0]]))
  qs.append(quaternions.matrixtoQuaternion([[0,0,-1], [0,1,0], [1,0,0]]))
  
  qs.append(quaternions.matrixtoQuaternion([[-1,0,0], [0,0,-1], [0,-1,0]]))
  qs.append(quaternions.matrixtoQuaternion([[1,0,0], [0,0,-1], [0,1,0]]))
  qs.append(quaternions.matrixtoQuaternion([[1,0,0], [0,0,1], [0,-1,0]]))
  qs.append(quaternions.matrixtoQuaternion([[-1,0,0], [0,0,1], [0,1,0]]))
  
  qs.append(quaternions.matrixtoQuaternion([[0,-1,0], [-1,0,0], [0,0,-1]]))
  qs.append(quaternions.matrixtoQuaternion([[0,1,0], [-1,0,0], [0,0,1]]))
  qs.append(quaternions.matrixtoQuaternion([[0,1,0], [1,0,0], [0,0,-1]]))
  qs.append(quaternions.matrixtoQuaternion([[0,-1,0], [1,0,0], [0,0,1]]))
  
  
  for plane in planes:
    vi = quaternions.quaternion(0,plane)
    
    count = []
    for q in qs:
      vf = q * vi * q.conjugate()
      
      newplane = (int(vf[1]), int(vf[2]), int(vf[3]))
      
      print newplane
      
      if newplane in planes:
        if not newplane in count:
          count.append(newplane)
    
#    print plane, count
  

  
  