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
from math import pi, tan, sin
import os

# Third party modules.

# Local modules.
import RandomUtilities.DrawingTools.drawing as drawing
from EBSDTools.mathTools.mathExtras import zeroPrecision, _acos
import EBSDTools.indexation.houghPeaks as houghPeaks
import EBSDTools.mathTools.vectors as vectors
import EBSDTools.crystallography.reciprocal as reciprocal
import EBSDTools.mathTools.triplets as triplets

def kikuchiLineToNormal(m, k, patternCenter, detectorDistance):
  #Shift line to a pattern centre at (0,0)
  if m != None:
      k -= -m*patternCenter[0] + patternCenter[1]
  else:
    k -= patternCenter[0]
  
  #Build two vectors (x2-x1 and x1-x0) to calculate the normal
  x0 = vectors.vector(0,0,0)
  
  if m == None:
    x1 = vectors.vector(k, detectorDistance, 0.0)
    x2 = vectors.vector(k, detectorDistance, 0.1)
  elif abs(m) < zeroPrecision:
    x1 = vectors.vector(0.0, detectorDistance, k)
    x2 = vectors.vector(0.1, detectorDistance, k)
  else:
    x1 = vectors.vector(0.0, detectorDistance, k)
    if abs(k) > zeroPrecision:
      x2 = vectors.vector(-k/m, detectorDistance, 0.0)
    else: # abs(k) < zeroPrecision:
      x2 = vectors.vector((1-k)/m, detectorDistance, 1.0)
  
  n = vectors.cross(x2-x1, x1-x0)
  
  return n

def reconstructedPattern(peaks, patternSize):
  """
    Return an image of the reconstructed pattern from the hough peaks
  """
  
  im = drawing.ImageLine(patternSize, origin='center')
  
  for peak in peaks:
    m, k = houghPeaks.houghPeakToKikuchiLine(peak['rho'], peak['theta'], patternSize)
    
    im.drawLinearFunction(m=m
                            , k=k)
  
  return im()

def positiveIndices(plane):
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
    
    return vectors.vector(h,k,l)

class Phases:
  def __init__(self
               , Ls
               , peaks
               , patternCenter
               , detectorDistance
               , patternSize
               , angularPrecision=0.5/180.0*pi):
    
    self.angularPrecision = angularPrecision
    
    self._calculatePatternAngles(peaks, patternCenter, detectorDistance, patternSize)
    
    self.latticesTriplets ={}
    for latticeId in Ls:
      self._calculateLatticeTriplets(latticeId, Ls[latticeId])
    
    self._compareAngles()
  
  def _calculatePatternAngles(self, peaks, patternCenter, detectorDistance, patternSize):
    
    #Find the normal of each Kikuchi line
    normals = []
    for peak in peaks:
      m, k = houghPeaks.houghPeakToKikuchiLine(rho = peak['rho']
                                               , theta = peak['theta']
                                               , patternSize = patternSize)
      
      n = kikuchiLineToNormal(m, k, patternCenter, detectorDistance)
      
      normals.append(n)
    
    #Find the angles between each normal
    angles = []
    for i, n1 in enumerate(normals):
      for j, n2 in enumerate(normals):
        if j >= i:
          continue
        
        n1 = n1.positive()
        n2 = n2.positive()
        angle = _acos(vectors.dot(n1, n2) / (n1.norm() * n2.norm()))
        
        angles.append(angle)
  
    self.patternAngles = angles
    print angles
  
  def _calculateLatticeTriplets(self, latticeId, L):
    latticeTriplets = []
    reflectors = L.getReflectors().getReflectorsList()
    basisTriplets = triplets.findTriplets(len(reflectors))
    
    for basisTriplet in basisTriplets:
      A = reflectors[basisTriplet[0]]
      B = reflectors[basisTriplet[1]]
      C = reflectors[basisTriplet[2]]
      
      AB = reciprocal.interplanarAngle(A, B, L)
      BC = reciprocal.interplanarAngle(B, C, L)
      AC = reciprocal.interplanarAngle(A, C, L)
      
      latticeTriplets.append({'A': A, 'B': B, 'C': C, 'AB': AB, 'BC': BC, 'AC': AC})
#      print {'A': A, 'B': B, 'C': C, 'AB': AB, 'BC': BC, 'AC': AC}
    
    self.latticesTriplets[latticeId] = latticeTriplets
  
  def _compareAngles(self):
    peaksTriplets = triplets.findTriplets(len(peaks))
    
#    self.patternAngles = [1.910,1.2309,1.2309,1.2309,1.2309,1.910]
    
    results = {}
    
    for latticeId in self.latticesTriplets:
      hits = 0
      for peakTriplets in peaksTriplets:
        ab = self.patternAngles[peakTriplets[0]]
        bc = self.patternAngles[peakTriplets[1]]
        ac = self.patternAngles[peakTriplets[2]]
        
        match = self.findLatticeMatch(latticeId, ab, bc, ac)
        if match[0] == True:
          print match[1]
          hits += 1
      
      results[latticeId] = hits
    
    print results

  
  def findLatticeMatch(self, latticeId, ab, bc, ac):
    for latticeTriplets in self.latticesTriplets[latticeId]:
#      print ab, bc, ac, latticeTriplets['AB'], latticeTriplets['BC'], latticeTriplets['AC']
      
      if abs(ab - latticeTriplets['AB']) < self.angularPrecision:
        if abs(bc - latticeTriplets['BC']) < self.angularPrecision:
          if abs(ac - latticeTriplets['AC']) < self.angularPrecision:
            return True, latticeTriplets
        elif abs(bc - latticeTriplets['AC']) < self.angularPrecision:
          if abs(ac - latticeTriplets['BC']) < self.angularPrecision:
            return True, latticeTriplets
      elif abs(ab - latticeTriplets['BC']) < self.angularPrecision:
        if abs(bc - latticeTriplets['AB']) < self.angularPrecision:
          if abs(ac - latticeTriplets['AC']) < self.angularPrecision:
            return True, latticeTriplets
        elif abs(bc - latticeTriplets['AC']) < self.angularPrecision:
          if abs(ac - latticeTriplets['AB']) < self.angularPrecision:
            return True, latticeTriplets
      elif abs(ab - latticeTriplets['AC']) < self.angularPrecision:
        if abs(bc - latticeTriplets['BC']) < self.angularPrecision:
          if abs(ac - latticeTriplets['AB']) < self.angularPrecision:
            return True, latticeTriplets
        elif abs(bc - latticeTriplets['AB']) < self.angularPrecision:
          if abs(ac - latticeTriplets['BC']) < self.angularPrecision:
            return True, latticeTriplets
    
    return False,


if __name__ == '__main__':
  from EBSDTools.indexation.houghPeaks import rmlImage
  import EBSDTools.crystallography.lattice as lattice
  
  patternSize = (335,255)
  patternCenter = (0.0, 0.0)
  detectorDistance = 0.3
  
  #Pattern reconstruction
#  folder = 'I:/Philippe Pinard/workspace/EBSDTools/patternSimulations/rotation/m_000.csv'
  folder = 'c:/documents/workspace/EBSDTools/patternSimulations/rotation/theta_000.csv'
  peaks = rmlImage(folder).getPeaksList()
  
#  image = reconstructedPattern(peaks, patternSize)
#  folder = 'I:/Philippe Pinard/workspace/EBSDTools/indexation/test'
#  image.save(os.path.join(folder, 'test.jpg'))
  
  atoms = {(0,0,0): 14,
           (0.5,0.5,0): 14,
           (0.5,0,0.5): 14,
           (0,0.5,0.5): 14}
  Lfcc = lattice.Lattice(a=5.43, b=5.43, c=5.43, alpha=pi/2, beta=pi/2, gamma=pi/2, atoms=atoms, reflectorsMaxIndice=1)
  atoms = {(0,0,0): 14,
           (0.5,0.5,0.5): 14}
  Lbcc = lattice.Lattice(a=5.43, b=5.43, c=5.43, alpha=pi/2, beta=pi/2, gamma=pi/2, atoms=atoms, reflectorsMaxIndice=1)
  
  phases = Phases(Ls = {'fcc': Lfcc, 'bcc': Lbcc}
                  , peaks = peaks
                  , patternCenter = patternCenter
                  , detectorDistance = detectorDistance
                  , patternSize = patternSize)
  
  