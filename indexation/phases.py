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
    
    self.latticesAngles ={}
    for latticeId in Ls:
      self._calculateLatticeAngles(latticeId, Ls[latticeId])
    
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
        
        angle = _acos(vectors.dot(n1, n2) / (n1.norm() * n2.norm()))
        
        angles.append(angle)
  
    self.patternAngles = angles
    print angles
  
  def _calculateLatticeAngles(self, latticeId, L):
    angles = {}
    
    reflectors = L.getReflectors().getReflectorsList()
    for i, reflector1 in enumerate(reflectors):
      for j, reflector2 in enumerate(reflectors):
        if j >= i:
          continue
        
        angle = reciprocal.interplanarAngle(reflector1, reflector2, L)
        key = '%s-%s' % (reflector1, reflector2)
        
        angles.setdefault(key, angle)
    
    self.latticesAngles[latticeId] = angles
    print angles
  
  def _compareAngles(self):
    bandsTriplets = triplets.findTriplets(len(peaks))
    
    for latticeId in self.latticesAngles:
      for bandTriplets in bandsTriplets:
        m1 = self.findLatticeMatch(latticeId, self.patternAngles[bandTriplets[0]])
        m2 = self.findLatticeMatch(latticeId, self.patternAngles[bandTriplets[1]])
        m3 = self.findLatticeMatch(latticeId, self.patternAngles[bandTriplets[2]])
        
        print m1, m2, m3
  
  def findLatticeMatch(self, latticeId, angle):
    for planes in self.latticesAngles[latticeId]:
      if abs(self.latticesAngles[latticeId][planes] - angle) < self.angularPrecision:
        return (True, planes)
    
    return False,


if __name__ == '__main__':
  from EBSDTools.indexation.houghPeaks import rmlImage
  import EBSDTools.crystallography.lattice as lattice
  
  patternSize = (335,255)
  patternCenter = (0.0, 0.0)
  detectorDistance = 0.3
  
  #Pattern reconstruction
  peaks = rmlImage('I:/Philippe Pinard/workspace/EBSDTools/patternSimulations/rotation/m_000.csv').getPeaksList()
  image = reconstructedPattern(peaks, patternSize)
  folder = 'I:/Philippe Pinard/workspace/EBSDTools/indexation/test'
  image.save(os.path.join(folder, 'test.jpg'))
  
  atoms = {(0,0,0): 14,
           (0.5,0.5,0): 14,
           (0.5,0,0.5): 14,
           (0,0.5,0.5): 14}
#  atoms = {(0,0,0): 14,
#           (0.5,0.5,0.5): 14}
  L = lattice.Lattice(a=5.43, b=5.43, c=5.43, alpha=pi/2, beta=pi/2, gamma=pi/2, atoms=atoms, reflectorsMaxIndice=2)
  
  phases = Phases(Ls = {'fcc': L}
                  , peaks = peaks
                  , patternCenter = patternCenter
                  , detectorDistance = detectorDistance
                  , patternSize = patternSize)
  
  