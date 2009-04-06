#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Philippe Pinard (philippe.pinard@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2008-2009 Philippe Pinard"
__license__ = ""

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
    Multiply two matrices or one matrix and a scalar.
    Multiplication of matrices is not commutative (:math:`\\matrixL{A}\\matrixL{B} \neq \\matrixL{B}\\matrixL{A}`)
      
    :rtype: :class:`matrix <EBSDTools.mathTools.matrices.matrix>`
    """
    
    m = matrix()
    
    if isinstance(self, matrix) and isinstance(other, matrix):
      for i in range(3):
        for j in range(3):
          for k in range(3):
            m[i][j] += self._m[i][k] * other._m[k][j]
    elif isinstance(other, int) or isinstance(other, float):
      for i in range(3):
        for j in range(3):
          m[i][j] = other*self._m[i][j]
    
    return m

  
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
  
  def isSO3(self):
    """
    Return is the matrix is a special orthogonal (SO3)
    
    **Equations:**
      :math:`\\deter{\\matrixL{M}} = +1`
         
    :rtype: bool
    """
    
    if abs(self.det() - 1.0) < zeroPrecision: # and trace(self._m) > zeroPrecision:
      return True
    else:
      return False
  
  def toList(self):
    """
    Return the matrix in a list form
    
    :rtype:list
    """
    return self._m

  def det(self):
    """
    Return the determinant of the matrix: :math:`\\deter{\\matrixL{M}}`.
    
    rtype: float
    """
    
    a = self._m[0][0]*self._m[1][1]*self._m[2][2] + self._m[0][1]*self._m[1][2]*self._m[2][0] + self._m[0][2]*self._m[2][1]*self._m[1][0]
    b = self._m[0][0]*self._m[1][2]*self._m[2][1] + self._m[0][1]*self._m[2][2]*self._m[1][0] + self._m[0][2]*self._m[2][0]*self._m[1][1]
    
    return a - b

  def transpose(self):
    """
    Return the transpose of the matrix: :math:`\\matrixL{M}^T`.
    
    rtype: :class:`matrix <EBSDTools.mathTools.matrices.matrix>`
    """
    m_ = matrix()
    for i in range(3):
      for j in range(3):
        m_[i][j] = self._m[j][i]
    
    return m_

  def trace(self):
    """
    Return the trace of the matrix: :math:`\\trace{\\matrixL{M}}`.
    
    rtype: float
    """
    
    return self._m[0][0] + self._m[1][1] + self._m[2][2]