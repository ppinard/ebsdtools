

from math import pi, tan, sin, cos
import EBSDTools.crystallography.reciprocal as reciprocal
from EBSDTools.mathTools.mathExtras import zeroPrecision
import EBSDTools.indexation.houghPeaks as houghPeaks
import EBSDTools.mathTools.vectors as vectors
import EBSDTools.mathTools.triplets as triplets

#Optional
import RandomUtilities.sort.sortDict as sortDict
import os

#Abbreviations
# PB: Pattern bands

numberOfReflectors = 32

def getLUT(L):
  reflectors = L.getReflectors()
  reflectorsList = reflectors.getReflectorsList()[:numberOfReflectors]
  
  LUT = []
  
  for i in range(len(reflectorsList)):
    for j in range(len(reflectorsList)):
      angle = reciprocal.interplanarAngle(reflectorsList[i], reflectorsList[j], L)
      family1 = reflectors.getReflectorFamily(reflectorsList[i])
      family2 = reflectors.getReflectorFamily(reflectorsList[j])
      
      if angle > zeroPrecision and angle <= (pi/2.0 + zeroPrecision):
        inLUT = False
        for item in LUT:
          if (item['reflector1']['family'] == family1 and item['reflector2']['family'] == family2 and abs(item['angle'] - angle) < zeroPrecision) or \
              (item['reflector1']['family'] == family2 and item['reflector2']['family'] == family1 and abs(item['angle'] - angle) < zeroPrecision): 
              inLUT = True
              break
        
        if not inLUT:
          LUT.append({'angle': angle, 'reflector1': {'family': family1, 'indices': reflectorsList[i]}, 'reflector2': {'family': family2, 'indices': reflectorsList[j]}})
  
  return LUT

def printLUT(lut):
  
  lut = sortDict.sortListByKey(lut, 'angle')
  
  for item in lut:
    print '%4.2f,%i,%i,%2i%2i%2i,%2i%2i%2i' % (item['angle'], item['reflector1']['family'], item['reflector2']['family'], item['reflector1']['indices'][0], item['reflector1']['indices'][1], item['reflector1']['indices'][2], item['reflector2']['indices'][0], item['reflector2']['indices'][1], item['reflector2']['indices'][2])
    

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

def getPBnormals(filename, patternCenter, detectorDistance, patternSize):
  peaks = houghPeaks.rmlImage(filename).getPeaksList()[:10]
  
  normals = []
  for peak in peaks:
    m, k = houghPeaks.houghPeakToKikuchiLine(rho = peak['rho']
                                             , theta = peak['theta']
                                             , patternSize = patternSize)
    
    n = kikuchiLineToNormal(m, k, patternCenter, detectorDistance).positive()
    
    normals.append(n)
  
  return normals

def getPBangles(tripletNormals):
  theta0 = vectors.angle(tripletNormals[0], tripletNormals[1])
  sign0 = 1
  if theta0 > pi/2.0:
    theta0 = pi - theta0
    tripletNormals[1] = -tripletNormals[1]
  
  theta1 = vectors.angle(tripletNormals[1], tripletNormals[2])
  sign1 = 1
  if theta1 > pi/2.0:
    theta1 = pi - theta1
    sign1 = -1
  
  theta2 = vectors.angle(tripletNormals[2], tripletNormals[0])
  sign2 = 1
  if theta2 > pi/2.0:
    theta2 = pi - theta2
    sign2 = -1
  
  band3P = vectors.dot(vectors.cross(tripletNormals[0], tripletNormals[2]), tripletNormals[1])
  
  
  return [{'angle': theta0, 'sign': sign0}, {'angle': theta1, 'sign': sign1}, {'angle': theta2, 'sign': sign2}], band3P

def findBand(thetas, band3P, lut, L):
  total = 0
  answers = []
  
  planes = {}
  planes.setdefault(0, [])
  planes.setdefault(1, [])
  planes.setdefault(2, [])
  
  for j, item in enumerate(lut):
    for i, theta in enumerate(thetas):
      diff = abs(item['angle'] - theta['angle'])
      
      if diff  < 1.0/180.0*pi:
        planes[i].append(item)
  
  for planes0 in planes[0]:
    for planes1 in planes[1]:
      for planes2 in planes[2]:
        
#        print planes0
        
        b0, b1, b2 = checkBandConsistency(planes0, planes1, planes2)
        
        if b0 != False:
#          print b0, b1, b2
          if planes0['reflector1']['family'] == b0['family']:
            kplanes0 = 'reflector1'
          else:
            kplanes0 = 'reflector2'
          if planes1['reflector1']['family'] == b1['family']:
            kplanes1 = 'reflector1'
          else:
            kplanes1 = 'reflector2'
          if planes2['reflector1']['family'] == b2['family']:
            kplanes2 = 'reflector1'
          else:
            kplanes2 = 'reflector2'
          
          count, bands = getExactHKL(kplanes0, kplanes1, kplanes2, planes0, planes1, planes2, thetas, band3P, L)
          total += count
          if count > 0:
            answers.append(bands)
  
  return total, answers

def getExactHKL(kplanes0, kplanes1, kplanes2, planes0, planes1, planes2, thetas, band3P, L):
  exhkl = {}
  np = 0
  
  dp1 = cos(planes0['angle'])*thetas[0]['sign']
  dp2 = cos(planes1['angle'])*thetas[1]['sign']
  dp3 = cos(planes2['angle'])*thetas[2]['sign']
  
  famA = planes0[kplanes0]['family']
  famB = planes1[kplanes1]['family']
  famC = planes2[kplanes2]['family']
  
  nPermsA = len(L.getReflectors().getReflectorsListByFamily(famA))
  nPermsB = len(L.getReflectors().getReflectorsListByFamily(famB))
  nPermsC = len(L.getReflectors().getReflectorsListByFamily(famC))
  
  for iA in range(2*nPermsA):
    if iA < nPermsA:
      A = L.getReflectors().getReflectorsListByFamily(famA)[iA]
    else:
      A = -L.getReflectors().getReflectorsListByFamily(famA)[iA-nPermsA]
    
    for iC in range(2*nPermsC):
      if iC < nPermsC:
        C = L.getReflectors().getReflectorsListByFamily(famC)[iC]
      else:
        C = -L.getReflectors().getReflectorsListByFamily(famC)[iC-nPermsC]
      
      AdC = vectors.angle(A, C)
      
      dAC = abs(AdC - dp3)
      if dAC > zeroPrecision:
        continue
      
      for iB in range(2*nPermsB):
        if iB < nPermsB:
          B = L.getReflectors().getReflectorsListByFamily(famB)[iB]
        else:
          B = -L.getReflectors().getReflectorsListByFamily(famB)[iB-nPermsB]
        
        AdB = vectors.angle(A, B)
        dAB = abs(AdB - dp1)
        if dAB > zeroPrecision:
          continue
        
        BdC = vectors.angle(B, C)
        dBC = abs(BdC - dp2)
        if dBC > zeroPrecision:
          continue
        
        AxC = vectors.cross(A, C)
        triP = vectors.dot(AxC, B)
        
        if triP*band3P >= 0.0:
          exhkl[np] = {'A': A, 'B': B, 'C': C}
          
          np += 1
          
          if triP > -zeroPrecision and triP < zeroPrecision:
            exhkl[np] = {'A': -A, 'B': -B, 'C': C}
            exhkl[np+1] = {'A': A, 'B': -B, 'C': C}
            np += 2

  return np, exhkl

def checkBandConsistency(planes0, planes1, planes2):
  for i in ['reflector1', 'reflector2']:
    for j in ['reflector1', 'reflector2']:
      for k in ['reflector1', 'reflector2']:
        i_ = _otherReflector(i)
        j_ = _otherReflector(j)
        k_ = _otherReflector(k)
        
        if planes0[i_]['family'] == planes1[j]['family'] and planes1[j_]['family'] == planes2[k]['family'] and planes2[k_]['family'] == planes0[i]['family']:
          return planes0[i], planes1[j], planes2[k]
  
  return False, False, False

def _otherReflector(reflector):
  if reflector == 'reflector1':
    return 'reflector2'
  else:
    return 'reflector1'

def isColinear():
  pass

if __name__ == '__main__':
  
  import EBSDTools.crystallography.lattice as lattice
  
  patternSize = (335,255)
  patternCenter = (0.0, 0.0)
  detectorDistance = 0.3
  
  #Pattern reconstruction
  root = 'i:/Philippe Pinard/'
#  root = 'c:/documents/'
#  folder = 'I:/Philippe Pinard/workspace/EBSDTools/patternSimulations/rotation/m_000.csv'
#  folder = 'c:/documents/workspace/EBSDTools/patternSimulations/test/fcc_pcz__001.bmp' + ".csv"
  filename = os.path.join(root, 'workspace/EBSDTools/indexation/test/fcc_pcz__000.bmp' + ".csv")
#  folder = os.path.join(root, 'workspace/EBSDTools/patternSimulations/rotation/test_2_000' + ".csv")
  
  atomsFCC = {(0,0,0): 26, 
           (0,0.5,0.5): 26,
           (0.5,0,0.5): 26,
           (0.5,0.5,0): 26}
  atomsBCC = {(0,0,0): 26, 
           (0.5,0.5,0.5): 26}
  
  L = lattice.Lattice(a=5.34, b=5.34, c=5.34, alpha=pi/2, beta=pi/2, gamma=pi/2, atoms=atomsBCC, reflectorsMaxIndice=4)
  
  lut = getLUT(L)
#  print len(lut)
#  printLUT(lut)
  
  kikuchiNormals = getPBnormals(filename, patternCenter, detectorDistance, patternSize)
  
  triplets = triplets.findTriplets(len(kikuchiNormals))
  for triplet in triplets:
    tripletNormals = [kikuchiNormals[triplet[0]], kikuchiNormals[triplet[1]], kikuchiNormals[triplet[2]]]
#  print len(tripletNormals)
  
    thetas, band3P = getPBangles(tripletNormals)
    
    total, bands = findBand(thetas, band3P, lut, L)
    if total > 0:
      print total, bands