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
from math import sqrt

# Third party modules.

# Local modules.
import EBSDTools.mathTools.vectors as vectors
from EBSDTools.mathTools.mathExtras import zeroPrecision

class matrix:
  def __init__(self, *data):
    """
    Define a 3x3 matrix
    
    **Parameters:**
      =============   =========================================
      ``len(data)``   Description
      =============   =========================================
      0               Zero matrix
      1               List of lists [[a,b,c], [d,e,f], [g,h,i]]
      3               Lists [a,b,c], [d,e,f], [g,h,i]
      9               a,b,c,d,e,f,g,h,i
      =============   =========================================
    """
    
    if len(data) == 0:
      self._m = [[0.0,0.0,0.0], [0.0,0.0,0.0], [0.0,0.0,0.0]]
    elif len(data) == 1:
      self._m = data[0]
    elif len(data) == 3:
      self._m = [data[0],data[1], data[2]]
    elif len(data) == 9:
      self._m = [[data[0], data[1], data[2]],
                 [data[3], data[4], data[5]],
                 [data[6], data[7], data[8]]]
  
  def __getitem__(self, index):
    """
    Return the coefficient or row of the matrix.
      
    :arg index: integer between 0 and 2
    :type index: int
      
    :rtype: float or list
    
    **Examples:** ::
      
      >>> m = matrix([[1,2,3], [4,5,6], [7,8,9]])
      >>> print m[1][2]
      >>> 5
    """
    
    if index >= 0 and index <= 2:
      return self._m[index]
  
  def __repr__(self):
    """
    Return a string of the matrix.
    
    :rtype: str
    """
    
    return "%f, %f, %f\n%f, %f, %f\n%f, %f, %f" % (self._m[0][0], self._m[0][1], self._m[0][2], self._m[1][0], self._m[1][1], self._m[1][2], self._m[2][0], self._m[2][1], self._m[2][2])
  
  def __mul__(self, other):
    """
      Multiply two matrices or one matrix and a scalar
      Multiplication of matrices is not commutative (AB \neq BA)
      
      Outputs:
        a matrix
    """
    
    pass
  
  def __eq__(self, other):
    """
    .. note:: When ``m1 == m2`` is called.
    
    Comparison of matrices.
    Check if two matrices are equal, i.e. if all their elements are equal
      
    :rtype: bool
    """
    
    for i in range(3):
      for j in range(3):
        if abs(self._m[i][j] - other._m[i][j]) > zeroPrecision:
          return False
    
    return True
  
  def isSU3(self):
    """
    Return is the matrix is a special orthogonal (SU3)
    
    **Equations:**
      :math:`\\deter{\\matrixL{M}} = +1`
         
    :rtype: bool
    """
    
    if abs(det(self._m) - 1.0) < zeroPrecision: # and trace(self._m) > zeroPrecision:
      return True
    else:
      return False

def det(m):
  """
  Return the determinant of a 3x3 matrix: :math:`\\deter{\\matrixL{M}}`.
  
  :arg m: a matrix
  :type m: :class:`matrix <EBSDTools.mathTools.matrices.matrix>`
  
  rtype: float
  """
  
  a = m[0][0]*m[1][1]*m[2][2] + m[0][1]*m[1][2]*m[2][0] + m[0][2]*m[2][1]*m[1][0]
  b = m[0][0]*m[1][2]*m[2][1] + m[0][1]*m[2][2]*m[1][0] + m[0][2]*m[2][0]*m[1][1]
  
  return a - b

def trace(m):
  """
  Return the trace of a 3x3 matrix: :math:`\\trace{\\matrixL{M}}`.
  
  :arg m: a matrix
  :type m: :class:`matrix <EBSDTools.mathTools.matrices.matrix>`
  
  rtype: float
  """
  
  return m[0][0] + m[1][1] + m[2][2]