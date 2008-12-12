#!/usr/bin/env python
"""
A list based vector class that supports elementwise mathematical operations

In this version, the vector call inherits from list; this 
requires Python 2.2 or later.
"""

# Script information for the file.
__author__ = "Philippe Pinard (philippe.pinard@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2008 Philippe Pinard"
__license__ = ""
__reference__ = "A. Pletzer (http://code.activestate.com/recipes/52272/)"

# Subversion informations for the file.
__svnRevision__ = ""
__svnDate__ = ""
__svnId__ = ""

# Standard library modules.
import math

# Third party modules.

# Local modules.
from mathExtras import _acos

class vector:
  def __init__(self, *data):
    """
      A vector of n elements 
      
      Inputs:
        
    """
    if len(data) == 0:
      self.vector = []
    elif len(data) == 1:
      if isinstance(data[0], list):
        self.vector = data[0]
      elif isinstance(data[0], tuple):
        self.vector = list(data[0])
      else:
        self.vector = [data[0]]
    elif len(data) > 1:
      self.vector = []
      for datum in data:
        self.vector.append(datum)

  def __repr__(self):
    """
      Return a string representation of the vector
    """
    return str(self.vector)

  def __getslice__(self, low, high):
    """
      Return a slide of the vector depending on the low and high values
    """
    return vector(self.vector[low:high])
  
  def __getitem__(self, key):
    """
      Return the value of a component 
    """
    return self.vector[key]
  
  def __setitem__(self, key, value):
    """
      Set value to the vector key
    """
    if key >= 0 and key < len(self.vector):
      self.vector[key] = value
  
  def __delitem__(self, key):
    """
      Delete a component
    """
    if key >= 0 and key < len(self.vector):
      del self.vector[key]
  
  def __lt__(self, other):
    """
      Comparison of two vectors: Less than
    """
    if len(self.vector) == len(other.vector):
      if sum(self.vector) < sum(other.vector):
        return True
      else:
        return False
    else:
      if len(self.vector) < len(other.vector):
        return True
      else:
        return False
  
  def __le__(self, other):
    """
      Comparison of two vectors: Less or equal than
    """
    if len(self.vector) == len(other.vector):
      if sum(self.vector) <= sum(other.vector):
        return True
      else:
        return False
    else:
      if len(self.vector) <= len(other.vector):
        return True
      else:
        return False
  
  def __gt__(self, other):
    """
      Comparison of two vectors: Greater than
    """
    if len(self.vector) == len(other.vector):
      if sum(self.vector) > sum(other.vector):
        return True
      else:
        return False
    else:
      if len(self.vector) > len(other.vector):
        return True
      else:
        return False
  
  def __ge__(self, other):
    """
      Comparison of two vectors: Greater or equal than
    """
    if len(self.vector) == len(other.vector):
      if sum(self.vector) >= sum(other.vector):
        return True
      else:
        return False
    else:
      if len(self.vector) >= len(other.vector):
        return True
      else:
        return False

  def __eq__(self, other):
    """
      Comparison of two vectors: Equal
    """
    if isinstance(self, vector) and isinstance(other, vector):
      if len(self.vector) == len(other.vector):
        for i in range(len(self.vector)):
          if self.vector[i] != other.vector[i]:
            return False
        
        return True
    
    return False
  
  def __ne__(self, other):
    """
      Comparison of two vectors: Not equal
    """
    return not self == other

  def __add__(self, other):
    """
      Addition of two vectors
    """
    output = []
    if len(self.vector) == len(other.vector):
      for i in range(len(self.vector)):
        output.append(self.vector[i] + other.vector[i])
    
    return vector(output)

  def __neg__(self):
    """
      Negation of a vector
    """
    output = []
    for i in range(len(self.vector)):
      output.append(-self.vector[i])
    
    return vector(output)
  
  def __sub__(self, other):
    """
      Addition of two vectors
    """
    output = []
    if len(self.vector) == len(other.vector):
      for i in range(len(self.vector)):
        output.append(self.vector[i] - other.vector[i])
    
    return vector(output)
  
  def __mul__(self, other):
    """
      Multiplication by a scalar
    """
    if isinstance(other, float) or isinstance(other, int):
      output = []
      for i in range(len(self.vector)):
        output.append(self.vector[i] * other)
    
    return vector(output)

  def __rmul__(self, other):
    return self*other

  def __div__(self, other):
    """
      Division by a scalar
    """
    return self * (1/float(other))

  def __len__(self):
    return len(self.vector)
  
  def toList(self):
    return self.vector
  
  def toTuple(self):
    return tuple(self.vector)
  
  def norm(self):
    """
      Return the norm of the vector
    """
    return math.sqrt(dot(self, self))

  def normalize(self):
    """
      Return a normalized vector
    """
    norm = self.norm()
    
    output = []
    for i in range(len(self.vector)):
      output.append(self.vector[i] / norm)
    
    return vector(output)
  
  def positive(self):
    output = []
    
    for i in range(len(self.vector)):
      if self.vector[i] == 0:
        output.append(self.vector[i])
        continue
      elif self.vector[i] < 0:
        for j in range(i, len(self.vector)):
          output.append(-self.vector[j])
        break
      else:
        for j in range(i, len(self.vector)):
          output.append(self.vector[j])
        break
    
    return vector(output)

def dot(v1, v2):
  """
    Return the dot product between v1 and v2 
  """
  product = 0.0
  
  if len(v1) == len(v2):
    for i in range(len(v1)):
      product += v1[i]*v2[i]
  
  return product

def cross(v1, v2):
  """
    Return the cross product of v1 and v2
  """
  if len(v1) == len(v2) and len(v1) == 3:
    return vector(v1[1]*v2[2] - v1[2]*v2[1]
                  , v1[2]*v2[0] - v1[0]*v2[2]
                  , v1[0]*v2[1] - v1[1]*v2[0])
  
def angle(v1, v2):
  costheta = dot(v1, v2) / (v1.norm() * v2.norm())
  
  return _acos(costheta)

def directionCosine(v1, v2):
  costheta = dot(v1, v2) / (v1.norm() * v2.norm())
  
  return costheta

def tripleProduct(v1, v2, v3):
  return dot(cross(v1,v2), v3)

if __name__ == "__main__":
  a = vector([0,0,1])
  b = vector(-1,0,1)
  e = vector(1.0,0,0)
  c = vector(1)
  
  print b.positive()
