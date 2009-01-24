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
from math import pi

# Third party modules.

# Local modules.
from EBSDTools.mathTools.mathExtras import zeroPrecision

def degEulersToRadEulers(*data):
  """
  Return a eulers from a set of 3 euler angles (in degrees)
    
  **Parameters:**
    * ``len(data) == 0``: zero eulers (0,0,0)
    * ``len(data) == 1``: List of 3 angles (theta1, theta2, theta3)
    * ``len(data) == 3``: 3 angles theta1, theta2, theta3 
  
  :rtype: :class:`eulers <EBSDTools.mathTools.eulers.eulers>`
  """
  
  if len(data) == 0:
    theta1 = 0
    theta2 = 0
    theta3 = 0
  elif len(data) == 1:
    theta1 = data[0][0]
    theta2 = data[0][1]
    theta3 = data[0][2]
  elif len(data) == 3:
    theta1 = data[0]
    theta2 = data[1]
    theta3 = data[2]
  
  return eulers(radEulers(theta1, theta2, theta3))

class eulers:
  def __init__(self, *data):
    """
    Define a set of 3 euler angles (in radians) as defined by the Bunge convention
      
    **Parameters:**
      * ``len(data) == 0``: zero eulers (0,0,0)
      * ``len(data) == 1``: List of 3 angles (theta1, theta2, theta3)
      * ``len(data) == 3``: 3 angles theta1, theta2, theta3 
    """
    
    if len(data) == 0:
      self._theta1 = 0.0
      self._theta2 = 0.0
      self._theta3 = 0.0
    elif len(data) == 1:
      self._theta1 = float(data[0][0])
      self._theta2 = float(data[0][1])
      self._theta3 = float(data[0][2])
    elif len(data) == 3:
      self._theta1 = float(data[0])
      self._theta2 = float(data[1])
      self._theta3 = float(data[2])
  
  def __getitem__(self, key):
    """
    Return the value of the euler angles in radians as they are called
      
    :arg name: Either theta1, theta2, theta3 or phi1, phi, phi2 or alpha, beta, gamma
    :type name: string
      
    :rtype: float
    
    **Examples:** ::
      
      e = eulers(0.5, 1, 0.2)
      print eulers['theta1'] #Return 0.5
      print eulers['beta'] #Return 1.0
      print eulers['phi2'] #Return 0.2
    """
    
    if isinstance(key, str):
      if key[-3:].lower() == 'deg':
        key = key[:-3]
        if key == 'theta1' or key == 'phi1' or key == 'alpha':
          return self._theta1 / pi * 180.0
        elif key == 'theta2' or key == 'phi' or key == 'beta':
          return self._theta2 / pi * 180.0
        elif key == 'theta3' or key == 'phi2' or key == 'gamma':
          return self._theta3 / pi * 180.0
      elif key[-3:].lower() == 'rad':
        key = key[:-3]
        if key == 'theta1' or key == 'phi1' or key == 'alpha':
          return self._theta1
        elif key == 'theta2' or key == 'phi' or key == 'beta':
          return self._theta2
        elif key == 'theta3' or key == 'phi2' or key == 'gamma':
          return self._theta3
      else:
        if key == 'theta1' or key == 'phi1' or key == 'alpha':
          return self._theta1
        elif key == 'theta2' or key == 'phi' or key == 'beta':
          return self._theta2
        elif key == 'theta3' or key == 'phi2' or key == 'gamma':
          return self._theta3
    elif isinstance(key, int):
      if key == 1:
        return self._theta1
      elif key == 2:
        return self._theta2
      elif key == 3:
        return self._theta3
        
    
  
  def __setitem__(self, key, value):
    """
    Modify an euler angle
      
    :arg name: Either theta1, theta2, theta3 or phi1, phi, phi2 or alpha, beta, gamma
    :type name: string
    
    :arg value: angle in radians
    :type value: float
    
    **Example:** ::
      
      e = eulers(0.5, 1, 0.2)
      e['theta2'] = 2.1
      e == eulers(0.5, 2.1, 0.2) #Equivalent
    """
    
    if isinstance(key, str):
      if key == 'theta1' or key == 'phi1' or key == 'alpha':
        self._theta1 = value
      elif key == 'theta2' or key == 'phi' or key == 'beta':
        self._theta2 = value
      elif key == 'theta3' or key == 'phi2' or key == 'gamma':
        self._theta3 = value
    elif isinstance(key, int):
      if key == 1:
        self._theta1 = value
      elif key == 2:
        self._theta2 = value
      elif key == 3:
        self._theta3 = value
  
  def __str__(self):
    """
    Return a string representing the euler angles
    
    :rtype: string
    """
    
    return "(%f, %f, %f)" % (self._theta1, self._theta2, self._theta3)
  
  def toDeg(self):
    """
    Return a tuple of the eulers in degrees
    
    :rtype: tuple
    """
    
    return degEulers(self._theta1, self._theta2, self._theta3)
  
  def toRad(self):
    """
    Return a tuple of the eulers in radians
    
    :rtype: tuple
    """
    
    return (self._theta1, self._theta2, self._theta3)
  
  def positive(self):
    """
    Convert eulers from 
      * :math:`-pi < \\text{theta0} < pi`
      * :math:`0 < \\text{theta1} < pi`
      * :math:`-pi < \\text{theta2} < pi`
    to
      * :math:`0 < \\text{theta0} < 2pi`
      * :math:`0 < \\text{theta1} < pi`
      * :math:`0 < \\text{theta2} < 2pi`
      
    :rtype: :class:`eulers <EBSDTools.mathTools.eulers.eulers>`
    """
    
    theta1 = self._theta1; theta2 = self._theta2; theta3 = self._theta3
    
    while theta1 < 0:
      theta1 += 2*pi
    while theta3 < 0:
      theta3 += 2*pi
    
    return eulers(theta1, theta2, theta3)
  
  def negative(self):
    """
    Convert eulers from 
      * :math:`0 < \\text{theta0} < 2pi`
      * :math:`0 < \\text{theta1} < pi`
      * :math:`0 < \\text{theta2} < 2pi`
    to
      * :math:`-pi < \\text{theta0} < pi`
      * :math:`0 < \\text{theta1} < pi`
      * :math:`-pi < \\text{theta2} < pi`
        
    :rtype: :class:`eulers <EBSDTools.mathTools.eulers.eulers>`
    """
    
    theta1 = self._theta1; theta2 = self._theta2; theta3 = self._theta3
    
    while theta1 > pi:
      theta1 -= 2*pi
    while theta3 > pi:
      theta3 -= 2*pi
    
    return eulers(theta1, theta2, theta3)

#TODO: Eliminate useless functions
def positiveEulers(*thetas):
  """
    Convert eulers from 
      -pi < theta0 < pi
      0 < theta1 < pi
      -pi < theta2 < pi
    to
      0 < theta0 < 2pi
      0 < theta1 < pi
      0 < theta2 < 2pi
  """
  if len(thetas) == 1:
    theta0 = thetas[0][0]
    theta1 = thetas[0][1]
    theta2 = thetas[0][2]
  elif len(thetas) == 3:
    theta0 = thetas[0]
    theta1 = thetas[1]
    theta2 = thetas[2]
  
  if theta0 < 0:
    theta0 += 2*pi
  if theta2 < 0:
    theta2 += 2*pi
  
  return theta0, theta1, theta2

def negativeEulers(theta0, theta1, theta2):
  """
    Convert eulers from
      0 < theta0 < 2pi
      0 < theta1 < pi
      0 < theta2 < 2pi
    to
      -pi < theta0 < pi
      0 < theta1 < pi
      -pi < theta2 < pi
  """
  if theta0 > pi:
    theta0 -= 2*pi
  if theta2 > pi:
    theta2 -= 2*pi
  
  return theta0, theta1, theta2

def degEulers(*thetas):
  """
    Convert from rad to deg
  """
  if len(thetas) == 1:
    theta0 = thetas[0][0]
    theta1 = thetas[0][1]
    theta2 = thetas[0][2]
  elif len(thetas) == 3:
    theta0 = thetas[0]
    theta1 = thetas[1]
    theta2 = thetas[2]
    
  theta0 *= 180.0 / pi
  theta1 *= 180.0 / pi
  theta2 *= 180.0 / pi
  
  return theta0, theta1, theta2

def radEulers(*thetas):
  """
    Convert from deg to rad
  """
  if len(thetas) == 1:
    theta0 = thetas[0][0]
    theta1 = thetas[0][1]
    theta2 = thetas[0][2]
  elif len(thetas) == 3:
    theta0 = thetas[0]
    theta1 = thetas[1]
    theta2 = thetas[2]
    
  theta0 *= pi / 180.0
  theta1 *= pi / 180.0
  theta2 *= pi / 180.0
  
  return theta0, theta1, theta2
