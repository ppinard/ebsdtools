#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Philippe Pinard (philippe.pinard@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2008-2009 Philippe Pinard"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = "$Revision$"
__svnDate__ = "$Date$"
__svnId__ = "$Id$"

# Standard library modules.
import unittest

# Third party modules.

# Local modules.
import EBSDTools.crystallography.symmetry as symmetry
import EBSDTools.mathTools.quaternions as quaternions

# Globals and constants variables.

class TestSymmetry(unittest.TestCase):
    
    def setUp(self):
        unittest.TestCase.setUp(self)
    
    def tearDown(self):
        unittest.TestCase.tearDown(self)
        
#    def testCubicSymmetries(self):
#      m = []
#      
#      m.append([[1,0,0], [0,1,0], [0,0,1]])
#      
#      m.append([[0,0,1], [1,0,0], [0,1,0]])
#      m.append([[0,0,-1], [1,0,0], [0,-1,0]])
#      m.append([[0,0,-1], [-1,0,0], [0,1,0]])
#      m.append([[0,0,1], [-1,0,0], [0,-1,0]])
#      
#      m.append([[0,1,0], [0,0,1], [1,0,0]])
#      m.append([[0,-1,0], [0,0,1], [-1,0,0]])
#      m.append([[0,-1,0], [0,0,-1], [1,0,0]])
#      m.append([[0,1,0], [0,0,-1], [-1,0,0]])
#      
#      #Two-fold
#      m.append([[-1,0,0], [0,1,0], [0,0,-1]])
#      m.append([[-1,0,0], [0,-1,0], [0,0,1]])
#      m.append([[1,0,0], [0,-1,0], [0,0,-1]])
#      
#      #Four-fold
#      m.append([[0,0,-1], [0,-1,0], [-1,0,0]])
#      m.append([[0,0,1], [0,-1,0], [1,0,0]])
#      m.append([[0,0,1], [0,1,0], [-1,0,0]])
#      m.append([[0,0,-1], [0,1,0], [1,0,0]])
#      
#      m.append([[-1,0,0], [0,0,-1], [0,-1,0]])
#      m.append([[1,0,0], [0,0,-1], [0,1,0]])
#      m.append([[1,0,0], [0,0,1], [0,-1,0]])
#      m.append([[-1,0,0], [0,0,1], [0,1,0]])
#      
#      m.append([[0,-1,0], [-1,0,0], [0,0,-1]])
#      m.append([[0,1,0], [-1,0,0], [0,0,1]])
#      m.append([[0,1,0], [1,0,0], [0,0,-1]])
#      m.append([[0,-1,0], [1,0,0], [0,0,1]])
#      
#      qm = []
#      for matrix in m:
#        qm.append(quaternions.matrixtoQuaternion(matrix))
#      
#      qq = symmetry.cubicSymmetries()
#      
#      self.assertEqual(qm, qq)
      
if __name__ == '__main__':
    unittest.main()