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
from math import pi, tan, sin
import os

# Third party modules.

# Local modules.
import RandomUtilities.DrawingTools.drawing as drawing
import RandomUtilities.sort.sortDict as sortDict
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
               , numberOfReflectors=32
               , angularPrecision=1.0/180.0*pi):
    
    self.angularPrecision = angularPrecision
    self.numberOfReflectors = numberOfReflectors
    
    self.latticesTripletsAngles ={}
    for latticeId in Ls:
      self._calculateLatticeTripletsAngles(latticeId, Ls[latticeId])
    
    self._calculatePatternAngles(peaks, patternCenter, detectorDistance, patternSize)
    
    self._compareAngles(peaks)
  
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
        
        angles.append({'A': n1, 'B': n2, 'AB': angle})
  
    self.patternAngles = angles
#    print angles
#    print len(angles)
  
  def _calculateLatticeTripletsAngles(self, latticeId, L):
    latticeTripletsAngles = []
    reflectors = L.getReflectors().getReflectorsList()[:32]
    basisTriplets = triplets.findTriplets(len(reflectors))
    
    for basisTriplet in basisTriplets:
      latticeAngles = []
      latticeAngles.append({'A': reflectors[basisTriplet[0]], 'B': reflectors[basisTriplet[1]], 'AB': reciprocal.interplanarAngle(reflectors[basisTriplet[0]], reflectors[basisTriplet[1]], L)})
      latticeAngles.append({'A': reflectors[basisTriplet[1]], 'B': reflectors[basisTriplet[2]], 'AB': reciprocal.interplanarAngle(reflectors[basisTriplet[1]], reflectors[basisTriplet[2]], L)})
      latticeAngles.append({'A': reflectors[basisTriplet[2]], 'B': reflectors[basisTriplet[0]], 'AB': reciprocal.interplanarAngle(reflectors[basisTriplet[2]], reflectors[basisTriplet[0]], L)})
      latticeAngles = sortDict.sortListByKey(latticeAngles, 'AB')
      
      latticeTripletsAngles.append(latticeAngles)
    
    self.latticesTripletsAngles[latticeId] = latticeTripletsAngles
#    print latticesAngle
  
  def _compareAngles(self, peaks):
    peaksTriplets = triplets.findTriplets(len(peaks))
    
    results = {}
    
    for latticeId in self.latticesTripletsAngles:
      hits = 0
      for peakTriplets in peaksTriplets:
        patternTripletsAngles = []
        patternTripletsAngles.append(self.patternAngles[peakTriplets[0]])
        patternTripletsAngles.append(self.patternAngles[peakTriplets[1]])
        patternTripletsAngles.append(self.patternAngles[peakTriplets[2]])
        patternTripletsAngles = sortDict.sortListByKey(patternTripletsAngles, 'AB')
        
        match = self.findLatticeMatch(latticeId, patternTripletsAngles)
        print match
#        if match[0] == True:
##          print patternTripletsAngles
#          print match
#          
#          
#          hits += 1
      
      results[latticeId] = hits
    
    print results

  
  def findLatticeMatch(self, latticeId, patternTripletsAngles):
    hits = 0
    for latticeTripletsAngles in self.latticesTripletsAngles[latticeId]:
#      print ab, bc, ac, latticeTriplets['AB'], latticeTriplets['BC'], latticeTriplets['AC']
      if abs(patternTripletsAngles[0]['AB'] - latticeTripletsAngles[0]['AB']) < self.angularPrecision:
        if abs(patternTripletsAngles[1]['AB'] - latticeTripletsAngles[1]['AB']) < self.angularPrecision:
          if abs(patternTripletsAngles[2]['AB'] - latticeTripletsAngles[2]['AB']) < self.angularPrecision:
#            print '.'*80
#            
#            print patternTripletsAngles[0]['AB'], patternTripletsAngles[0]['AB']
#            print patternTripletsAngles[0]['A'], patternTripletsAngles[0]['B']
#            print latticeTripletsAngles[0]['A'], latticeTripletsAngles[0]['B']
#            
#            print patternTripletsAngles[1]['AB'], patternTripletsAngles[1]['AB']
#            print patternTripletsAngles[1]['A'], patternTripletsAngles[1]['B']
#            print latticeTripletsAngles[1]['A'], latticeTripletsAngles[1]['B']
#            
#            print patternTripletsAngles[2]['AB'], patternTripletsAngles[2]['AB']
#            print patternTripletsAngles[2]['A'], patternTripletsAngles[2]['B']
#            print latticeTripletsAngles[2]['A'], latticeTripletsAngles[2]['B']
#            
#            common = self.commonReflector(patternTripletsAngles[0], patternTripletsAngles[1])
#            if common != None:
#              match.append((self.commonReflector(latticeTripletsAngles[0], latticeTripletsAngles[1]),common))
#            
#            common = self.commonReflector(patternTripletsAngles[1], patternTripletsAngles[2])
#            if common != None:
#              match.append((self.commonReflector(latticeTripletsAngles[1], latticeTripletsAngles[2]),common))
#            
#            common = self.commonReflector(patternTripletsAngles[2], patternTripletsAngles[0])
#            if common != None:
#              match.append((self.commonReflector(latticeTripletsAngles[2], latticeTripletsAngles[0]),common))
#            
#            print match
            hits += 1
    return hits
    
  def commonReflector(self, triplet1, triplet2):
    if triplet1['A'] == triplet2['A'] or triplet1['A'] == triplet2['B']:
      return triplet1['A']
    elif triplet1['B'] == triplet2['A'] or triplet1['B'] == triplet2['B']:
      return triplet1['B']
    else:
      return None
  
  def commonAngle(self, pattern, lattice):
    for i in range(len(pattern)):
      for j in range(len(lattice)):
        if abs(pattern[i]['AB'] - lattice[j]['AB']) < self.angularPrecision:
          print lattice[j]['AB']
          print pattern[i]['A'], pattern[i]['B']
          print lattice[j]['A'], lattice[j]['B']

def run():
  from EBSDTools.indexation.houghPeaks import rmlImage
  import EBSDTools.crystallography.lattice as lattice
  
  patternSize = (335,255)
  patternCenter = (0.0, 0.0)
  detectorDistance = 0.3
  
  #Pattern reconstruction
#  folder = 'I:/Philippe Pinard/workspace/EBSDTools/patternSimulations/rotation/m_000.csv'
#  folder = 'c:/documents/workspace/EBSDTools/patternSimulations/test/fcc_pcz__001.bmp' + ".csv"
  folder = 'i:/Philippe Pinard/workspace/EBSDTools/indexation/test/fcc_pcz__000.bmp' + ".csv"
  folder = 'i:/Philippe Pinard/workspace/EBSDTools/patternSimulations/rotation/test_2_000' + ".csv"
  peaks = rmlImage(folder).getPeaksList()[:8]
  
  image = reconstructedPattern(peaks, patternSize)
#  folder = 'c:/documents/workspace/EBSDTools/indexation/test'
  folder = 'i:/Philippe Pinard/workspace/EBSDTools/indexation/test'
  image.save(os.path.join(folder, 'test.jpg'))
  
  atoms = {(0,0,0): 14,
           (0.5,0.5,0): 14,
           (0.5,0,0.5): 14,
           (0,0.5,0.5): 14}
  Lfcc = lattice.Lattice(a=5.43, b=5.43, c=5.43, alpha=pi/2, beta=pi/2, gamma=pi/2, atoms=atoms, reflectorsMaxIndice=4)
#  print len(Lfcc.getReflectors().getReflectorsList()), Lfcc.getReflectors().getReflectorsList()[:32]
  atoms = {(0,0,0): 14,
           (0.5,0.5,0.5): 14}
  Lbcc = lattice.Lattice(a=5.43, b=5.43, c=5.43, alpha=pi/2, beta=pi/2, gamma=pi/2, atoms=atoms, reflectorsMaxIndice=4)
#  print len(Lbcc.getReflectors().getReflectorsList()), Lbcc.getReflectors().getReflectorsList()[:32]
#  atoms = {}
#  self.Lhexagonal = lattice.Lattice(a=2, b=2, c=3, alpha=pi/2, beta=pi/2, gamma=120.0/180*pi, atoms=atoms, reflectorsMaxIndice=1)
  
  phases = Phases(Ls = {'fcc': Lfcc}#, 'bcc': Lbcc}
                  , peaks = peaks
                  , patternCenter = patternCenter
                  , detectorDistance = detectorDistance
                  , patternSize = patternSize)
  
if __name__ == '__main__':
  run()