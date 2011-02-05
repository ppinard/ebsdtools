#!/usr/bin/env python
"""
================================================================================
:mod:`test_symmetry` -- Unit tests for the module :mod:`symmetry`.
================================================================================

.. module:: test_symmetry
   :synopsis: Unit tests for the module :mod:`symmetry`.

"""

# Script information for the file.
__author__ = "Philippe T. Pinard"
__email__ = "philippe.pinard@gmail.com"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2009 Philippe T. Pinard"
__license__ = "GPL v3"

# Standard library modules.
import unittest
import logging

# Third party modules.

# Local modules.
#import ebsdtools.crystallography.symmetry as symmetry
#import mathtools.rotation.quaternions as quaternions

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

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
