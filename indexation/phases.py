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
#import RandomUtilities.DrawingTools.drawing as drawing
import RandomUtilities.sort.sortDict as sortDict
from EBSDTools.mathTools.mathExtras import zeroPrecision, _acos, smallAngle
import EBSDTools.indexation.houghPeaks as houghPeaks
import EBSDTools.mathTools.vectors as vectors
import EBSDTools.mathTools.quaternions as quaternions
import EBSDTools.crystallography.reciprocal as reciprocal
import EBSDTools.mathTools.triplets as triplets
import EBSDTools.mathTools.eulers as eulers

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
      
      n = kikuchiLineToNormal(m, k, patternCenter, detectorDistance).positive()
      
      normals.append(n)
    
    #Build the triplets
    self.peakTripletsAngles = []
    peaksTriplets = triplets.findTriplets(len(peaks))
    
    for peakTriplet in peaksTriplets:
      peakAngles = []
      AB0 = smallAngle(vectors.angle(normals[peakTriplet[0]], normals[peakTriplet[1]]))
      AB1 = smallAngle(vectors.angle(normals[peakTriplet[1]], normals[peakTriplet[2]]))
      AB2 = smallAngle(vectors.angle(normals[peakTriplet[2]], normals[peakTriplet[0]]))
      
      peakAngles.append({'A': normals[peakTriplet[0]], 'B': normals[peakTriplet[1]], 'AB': AB0})
      peakAngles.append({'A': normals[peakTriplet[1]], 'B': normals[peakTriplet[2]], 'AB': AB1})
      peakAngles.append({'A': normals[peakTriplet[2]], 'B': normals[peakTriplet[0]], 'AB': AB2})
      peakAngles = sortDict.sortListByKey(peakAngles, 'AB')
      
      self.peakTripletsAngles.append(peakAngles)
    
#    print len(self.peakTripletsAngles)
    
  def _calculateLatticeTripletsAngles(self, latticeId, L):
    latticeTripletsAngles = []
    reflectors = L.getReflectors().getReflectorsList()[:self.numberOfReflectors]
    latticeTriplets = triplets.findTriplets(len(reflectors))
    
    for latticeTriplet in latticeTriplets:
      latticeAngles = []
      AB0 = smallAngle(reciprocal.interplanarAngle(reflectors[latticeTriplet[0]], reflectors[latticeTriplet[1]], L))
      AB1 = smallAngle(reciprocal.interplanarAngle(reflectors[latticeTriplet[1]], reflectors[latticeTriplet[2]], L))
      AB2 = smallAngle(reciprocal.interplanarAngle(reflectors[latticeTriplet[2]], reflectors[latticeTriplet[0]], L))
      
      latticeAngles.append({'A': vectors.vector(reflectors[latticeTriplet[0]]), 'B': vectors.vector(reflectors[latticeTriplet[1]]), 'AB': AB0})
      latticeAngles.append({'A': vectors.vector(reflectors[latticeTriplet[1]]), 'B': vectors.vector(reflectors[latticeTriplet[2]]), 'AB': AB1})
      latticeAngles.append({'A': vectors.vector(reflectors[latticeTriplet[2]]), 'B': vectors.vector(reflectors[latticeTriplet[0]]), 'AB': AB2})
      latticeAngles = sortDict.sortListByKey(latticeAngles, 'AB')
      
      latticeTripletsAngles.append(latticeAngles)
    
    self.latticesTripletsAngles[latticeId] = latticeTripletsAngles
#    print len(latticeTripletsAngles)
#    print latticesAngle
  
  def _compareAngles(self, peaks):
    
    for latticeId in self.latticesTripletsAngles:
      total = 0
      results = {}
      for latticeTripletsAngles in self.latticesTripletsAngles[latticeId]:
        hits = 0
        
        for peakTripletsAngles in self.peakTripletsAngles:
          match = self.match(peakTripletsAngles, latticeTripletsAngles)
          
          if match:
            hits += 1
            
            for i in range(2):
              orientation = self.calculateOrientation(n1=peakTripletsAngles[i]['A']
                                      , n2=peakTripletsAngles[i]['B']
                                      , hkl1=latticeTripletsAngles[i]['A']
                                      , hkl2=latticeTripletsAngles[i]['B'])
              
              var = 0
              for result in results.keys():
                if quaternions.similar(orientation, result, self.angularPrecision):
                  results[result] += 1
                  var = 1
                  break
              
              if var == 0:
                results[orientation] = 1
            
          
#          if hits >= 10:
#            print results
#            return
        
        total += hits
#        if hits > 0:
#          print hits, latticeTripletsAngles
      
      print latticeId, total, float(total) / len(self.peakTripletsAngles)**2
    
      maxVote = ('q',0)
      for result in results:
#        if results[result] > 30:
#          print result, results[result]
        if results[result] > maxVote[1]:
          maxVote = (result, results[result])
      
      print maxVote
      print eulers.degEulers(eulers.positiveEulers(maxVote[0].toEulerAngles()))
      print maxVote[0].toEulerAngles()
  
  def match(self, peakTripletsAngles, latticeTripletsAngles):
    if abs(peakTripletsAngles[0]['AB'] - latticeTripletsAngles[0]['AB']) < self.angularPrecision:
      if abs(peakTripletsAngles[1]['AB'] - latticeTripletsAngles[1]['AB']) < self.angularPrecision:
        if abs(peakTripletsAngles[2]['AB'] - latticeTripletsAngles[2]['AB']) < self.angularPrecision:
          return True
    
    return False
    
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

  def calculateOrientation(self, n1, n2, hkl1, hkl2):
    eP1 = n1 / n1.norm()
    eP2 = vectors.cross(n1, n2)
    eP2 /= eP2.norm()
    eP3 = vectors.cross(eP1, eP2)
    
    qP = quaternions.matrixtoQuaternion([eP1.toList(), eP2.toList(), eP3.toList()])
    
    eC1 = hkl1 / hkl1.norm()
    eC2 = vectors.cross(hkl1, hkl2)
    eC2 /= eC2.norm()
    eC3 = vectors.cross(eC1, eC2)
    
    qC = quaternions.matrixtoQuaternion([eC1.toList(), eC2.toList(), eC3.toList()])
    
    qS = quaternions.axisAngleToQuaternion(-70/180.0*pi, (1,0,0))
    
    g = qC.conjugate() * qP * qS.conjugate()
    
    return g.normalize()

def run():
  from EBSDTools.indexation.houghPeaks import rmlImage
  import EBSDTools.crystallography.lattice as lattice
  
  patternSize = (335,255)
  patternCenter = (0.0, 0.0)
  detectorDistance = 0.3
  
  #Pattern reconstruction
  root = 'i:/Philippe Pinard/'
#  root = 'c:/documents/'
#  folder = 'I:/Philippe Pinard/workspace/EBSDTools/patternSimulations/rotation/m_000.csv'
#  folder = 'c:/documents/workspace/EBSDTools/patternSimulations/test/fcc_pcz__001.bmp' + ".csv"
  folder = os.path.join(root, 'workspace/EBSDTools/indexation/test/fcc_pcz__000.bmp' + ".csv")
#  folder = os.path.join(root, 'workspace/EBSDTools/patternSimulations/rotation/test_2_000' + ".csv")
  peaks = rmlImage(folder).getPeaksList()[:8]
  
#  image = reconstructedPattern(peaks, patternSize)
#  folder = 'c:/documents/workspace/EBSDTools/indexation/test'
##  folder = 'i:/Philippe Pinard/workspace/EBSDTools/indexation/test'
#  image.save(os.path.join(folder, 'test.jpg'))
  
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
  
  phases = Phases(Ls = {'fcc': Lfcc, 'bcc': Lbcc}
                  , peaks = peaks
                  , patternCenter = patternCenter
                  , detectorDistance = detectorDistance
                  , patternSize = patternSize)
  
if __name__ == '__main__':
  run()