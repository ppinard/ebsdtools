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
      
      Inputs:
        len(data) == 0: Zero matrix
        len(data) == 1: List of lists [[a,b,c], [d,e,f], [g,h,i]]
        len(data) == 3: Lists [a,b,c], [d,e,f], [g,h,i]
        len(data) == 9: a,b,c,d,e,f,g,h,i
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
      Return the coefficient or row of the matrix
      
      Inputs:
        index: integer between 0 and 2
      
      Outputs:
        int/float or list
    """
    
    if index >= 0 and index <= 2:
      return self._m[index]
  
  def __repr__(self):
    """
      Return a string of the matrix
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
      Comparison of matrices
      Check if two matrices are equal, i.e. if all their elements are equal
      
      Outputs:
        True: equal
        False: not equal
    """
    
    for i in range(3):
      for j in range(3):
        if abs(self._m[i][j] - other._m[i][j]) > zeroPrecision:
          return False
    
    return True
  
  def isSU3(self):
    """
      Return is the matrix is a special orthogonal (SU3)
         det(matrix) = +1)
         
      Outputs:
        True if the matrix is a SU3
    """
    
    if abs(det(self._m) - 1.0) < zeroPrecision: # and trace(self._m) > zeroPrecision:
      return True
    else:
      return False

def det(m):
  a = m[0][0]*m[1][1]*m[2][2] + m[0][1]*m[1][2]*m[2][0] + m[0][2]*m[2][1]*m[1][0]
  b = m[0][0]*m[1][2]*m[2][1] + m[0][1]*m[2][2]*m[1][0] + m[0][2]*m[2][0]*m[1][1]
  
  return a - b

def trace(m):
  return m[0][0] + m[1][1] + m[2][2]