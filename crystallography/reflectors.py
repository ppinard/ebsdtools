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
from math import sin, cos, pi, acos, atan2, exp, sqrt
import csv
import os.path

# Third party modules.

# Local modules.
import EBSDTools
import mathTools.vectors as vectors
import reciprocal
import lattice
import bragg
import RandomUtilities.sort.sortDict as sortDict

class scatteringFactors:
  def __init__(self
               , filepath_0_2='data/elastic_atomic_scattering_factors_0_2.csv'
               , filepath_2_6='data/elastic_atomic_scattering_factors_2_6.csv'):
    
    basedir = EBSDTools.__path__
    
    reader = csv.reader(open(os.path.join(basedir,filepath_0_2), 'r'))
    rows = list(reader)
    self.__read_0_2(rows[1:])
    
    reader = csv.reader(open(os.path.join(basedir,filepath_2_6), 'r'))
    rows = list(reader)
    self.__read_2_6(rows[1:])
    
  def __read_0_2(self, rows):
    self.parameters_0_2 = {}
    
    for row in rows:
      Z = int(row[0])
      self.parameters_0_2.setdefault(Z, {})
      self.parameters_0_2[Z]['a1'] = float(row[1])
      self.parameters_0_2[Z]['a2'] = float(row[2])
      self.parameters_0_2[Z]['a3'] = float(row[3])
      self.parameters_0_2[Z]['a4'] = float(row[4])
      self.parameters_0_2[Z]['a5'] = float(row[5])
      self.parameters_0_2[Z]['b1'] = float(row[6])
      self.parameters_0_2[Z]['b2'] = float(row[7])
      self.parameters_0_2[Z]['b3'] = float(row[8])
      self.parameters_0_2[Z]['b4'] = float(row[9])
      self.parameters_0_2[Z]['b5'] = float(row[10])
  
  def __read_2_6(self, rows):
    self.parameters_2_6 = {}
    
    for row in rows:
      Z = int(row[0])
      self.parameters_2_6.setdefault(Z, {})
      self.parameters_2_6[Z]['a1'] = float(row[1])
      self.parameters_2_6[Z]['a2'] = float(row[2])
      self.parameters_2_6[Z]['a3'] = float(row[3])
      self.parameters_2_6[Z]['a4'] = float(row[4])
      self.parameters_2_6[Z]['a5'] = float(row[5])
      self.parameters_2_6[Z]['b1'] = float(row[6])
      self.parameters_2_6[Z]['b2'] = float(row[7])
      self.parameters_2_6[Z]['b3'] = float(row[8])
      self.parameters_2_6[Z]['b4'] = float(row[9])
      self.parameters_2_6[Z]['b5'] = float(row[10])
  
  def getScatteringFactor(self, Z, s):
    """
      Return the scattering factor for atomic number Z and s
      s is defined as $\frac{4\pi\sin\theta}{\lambda}$
      
      The values are limited for $0 < s < 2 \AA$
      
      References:
        Prince2004
      
      Inputs:
        Z: atomic number (integer)
        s: norm of the scattering vector in $\AA$ (float)
      
      Outputs:
        a float of the scattering factor
    """
    
    if s >= 0 and s < 2:
      a = [self.parameters_0_2[Z]['a1'], self.parameters_0_2[Z]['a2'], self.parameters_0_2[Z]['a3'], self.parameters_0_2[Z]['a4'], self.parameters_0_2[Z]['a5']]
      b = [self.parameters_0_2[Z]['b1'], self.parameters_0_2[Z]['b2'], self.parameters_0_2[Z]['b3'], self.parameters_0_2[Z]['b4'], self.parameters_0_2[Z]['b5']]
#    elif s >= 2 and s < 6:
    elif s >= 2:
      a = [self.parameters_2_6[Z]['a1'], self.parameters_2_6[Z]['a2'], self.parameters_2_6[Z]['a3'], self.parameters_2_6[Z]['a4'], self.parameters_2_6[Z]['a5']]
      b = [self.parameters_2_6[Z]['b1'], self.parameters_2_6[Z]['b2'], self.parameters_2_6[Z]['b3'], self.parameters_2_6[Z]['b4'], self.parameters_2_6[Z]['b5']]
#    else:
#      a = [0,0,0,0,0]
#      b = [0,0,0,0,0]
      
    f = 0.0
    
    for i in range(5):
      f += a[i]*exp(-b[i]*s**2)
    
    return f

class Reflectors:
  def __init__(self, L, maxIndice=2):
    self.L = L
    
    self.scatteringFactors = scatteringFactors()
    
    self._calculateReflectors(maxIndice)
    
  def _calculateReflectors(self, maxIndice):
    self.reflectors = {}
    intensities = []
    
    planes = self.__findReflectors(maxIndice)
    
    for plane in planes:
      self.reflectors.setdefault(plane, {})
      self.reflectors[plane]['reflector'] = plane
      
      planeSpacing = self.__calculatePlaneSpacing(plane)
      self.reflectors[plane]['plane spacing'] = planeSpacing
      
      intensity = self.__calculateIntensity(plane, planeSpacing)
      intensities.append(intensity)
      self.reflectors[plane]['intensity'] = intensity
    
    intensityMax = max(intensities)
    if intensityMax > 0.0:
      for plane in planes:
        self.reflectors[plane]['normalized intensity'] = self.reflectors[plane]['intensity'] / intensityMax
    
  def __positiveIndices(self, plane):
    h = plane[0]
    k = plane[1]
    l = plane[2]
    
    #h always greater than 0
    if h < 0:
      h = -h
      k = -k
      l = -l
    elif h == 0 and k < 0:
      h = 0
      k = -k
      l = -l
    elif h == 0 and k == 0 and l <0:
      h = 0
      k = 0
      l = -l
    
    return (h,k,l)
  
  def __areEquivalent(self, plane1, plane2):
    angle = reciprocal.interplanarAngle(plane1, plane2, self.L)
    
    if angle < 1e-5 or abs(angle - pi) < 1e-5:
      if abs(plane1[0]) == abs(plane2[0]):
        return True
      else:
        return False
    else:
      return False

  def __isDiffracting(self, plane):
    sum = 0
    
    atomPositions = self.L.getAtomsPositions()
    
    for atomPosition in atomPositions:
      sum += (-1)**(2*vectors.dot(plane, atomPosition))
    
    if sum > 0:
      return True
    else:
      return False

  def __findReflectors(self, maxIndice):
    reflectors = []
    
    for h in range(-maxIndice, maxIndice+1):
      for k in range(-maxIndice, maxIndice+1):
        for l in range(-maxIndice, maxIndice+1):
          plane = self.__positiveIndices((h,k,l))
          
          if not plane == (0,0,0): #Remove plane (0,0,0)
            if self.__isDiffracting(plane):
              for reflector in reflectors:
                if self.__areEquivalent(plane, reflector):
                  plane = None
                  break
                  
              if plane != None:
                reflectors.append(plane)
    
    reflectors.sort()
    return reflectors
  
  def __calculatePlaneSpacing(self, plane):
    return reciprocal.planeSpacing(plane, self.L)
  
  def __calculateIntensity(self, plane, planeSpacing):
    sum = 0.0
    
    for atom in self.L.atoms:
      s = 2*pi/planeSpacing
      
      sum += (-1)**(2*vectors.dot(plane, atom)) * self.scatteringFactors.getScatteringFactor(self.L.atoms[atom], s)
    
    return sum**2
  
  def getReflectorsDict(self):
    return self.reflectors
  
  def getReflectorsList(self):
    """
      Return a list of reflectors sorted in decreasing order of intensity
      
      Inputs:
        None
      
      Outputs:
        a list
    """
    intensityDict = {}
    for reflector in self.reflectors.keys():
      intensityDict.setdefault(reflector, self.reflectors[reflector]['normalized intensity'])
    
    sortedIntensityDict = sortDict.sortDictByValue(intensityDict, reverse=True)
    
    keys = []
    for item in sortedIntensityDict:
      keys.append(item[0])
    
    return keys
  
  def getReflectorInfo(self, plane):
    if plane in self.reflectors.keys():
      return self.reflectors[plane]
  
  def getReflectorPlaneSpacing(self, plane):
    if plane in self.reflectors.keys():
      return self.reflectors[plane]['plane spacing']
  
  def getReflectorIntensity(self, plane):
    if plane in self.reflectors.keys():
      return self.reflectors[plane]['intensity']
  
  def getReflectorNormalizedIntensity(self, plane):
    if plane in self.reflectors.keys():
      return self.reflectors[plane]['normalized intensity']

if __name__ == '__main__':
  
  atoms = {(0,0,0): 26, 
           (0,0.5,0.5): 26,
           (0.5,0,0.5): 26,
           (0.5,0.5,0): 26}
  
  L = lattice.Lattice(a=3.59, b=3.59, c=3.59, alpha=pi/2, beta=pi/2, gamma=pi/2, atoms=atoms, reflectorsMaxIndice=2)
  
  reflectors = L.getReflectors().getReflectorsList()
  print reflectors
  
#  for plane in reflectors.getReflectorsList():
#    print '%2i%2i%2i %6.4f %e %4.2f' % (plane[0],plane[1],plane[2], reflectors.getReflectorPlaneSpacing(plane), reflectors.getReflectorIntensity(plane), reflectors.getReflectorNormalizedIntensity(plane)*100.0)
#  
  