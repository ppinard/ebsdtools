

from math import pi, tan, sin, cos, sqrt
import EBSDTools.crystallography.reciprocal as reciprocal
from EBSDTools.mathTools.mathExtras import zeroPrecision, _acos
import EBSDTools.indexation.houghPeaks as houghPeaks
import EBSDTools.mathTools.vectors as vectors
import EBSDTools.mathTools.quaternions as quaternions
import EBSDTools.mathTools.triplets as triplets
import EBSDTools.crystallography.symmetry as symmetry
import EBSDTools.mathTools.eulers as eulers

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
          LUT.append({'angle': angle, 'reflector1': {'family': family1, 'indices': vectors.vector(reflectorsList[i])}, 'reflector2': {'family': family2, 'indices': vectors.vector(reflectorsList[j])}})
  
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
  peaks = houghPeaks.rmlImage(filename).getPeaksList()[:6]
  
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
  
  band3P = vectors.tripleProduct(tripletNormals[0], tripletNormals[1], tripletNormals[2])
#  print band3P, abs(band3P) > zeroPrecision
  
  return [{'angle': theta0, 'sign': sign0}, {'angle': theta1, 'sign': sign1}, {'angle': theta2, 'sign': sign2}], band3P

def findBand(thetas, band3P, lut, L):
  totalSolutions = []
  
  planes = {}
  planes.setdefault(0, [])
  planes.setdefault(1, [])
  planes.setdefault(2, [])
  
  for j, item in enumerate(lut):
    for i, theta in enumerate(thetas):
      diff = abs(item['angle'] - theta['angle'])
      
      if diff  < 1/180.0*pi:
        planes[i].append(item)
#        print item['angle']*180/pi
  
#  for theta in planes:
#    print theta
#    for item in planes[theta]:
#      print '%4.2f,%i,%i,%2i%2i%2i,%2i%2i%2i' % (item['angle'], item['reflector1']['family'], item['reflector2']['family'], item['reflector1']['indices'][0], item['reflector1']['indices'][1], item['reflector1']['indices'][2], item['reflector2']['indices'][0], item['reflector2']['indices'][1], item['reflector2']['indices'][2])
#  
  for planes0 in planes[0]:
    for planes1 in planes[1]:
      for planes2 in planes[2]:
        
#        print planes0
        
        b0, b1, b2 = checkBandConsistency(planes0, planes1, planes2)
        
        if b0 != False:
#          print '%s %s %4.2f %4.2f || %s %s %4.2f' % (planes0['reflector1']['indices'], planes0['reflector2']['indices'], planes0['angle']*180/pi, vectors.angle(planes0['reflector1']['indices'], planes0['reflector2']['indices'])*180/pi, b0['indices'], b1['indices'], vectors.angle(b0['indices'], b1['indices'])*180/pi)
#          print '%s %s %4.2f %4.2f || %s %s %4.2f' % (planes1['reflector1']['indices'], planes1['reflector2']['indices'], planes1['angle']*180/pi, vectors.angle(planes1['reflector1']['indices'], planes1['reflector2']['indices'])*180/pi, b1['indices'], b2['indices'], vectors.angle(b1['indices'], b2['indices'])*180/pi)
#          print '%s %s %4.2f %4.2f || %s %s %4.2f' % (planes2['reflector1']['indices'], planes2['reflector2']['indices'], planes2['angle']*180/pi, vectors.angle(planes2['reflector1']['indices'], planes2['reflector2']['indices'])*180/pi, b2['indices'], b0['indices'], vectors.angle(b2['indices'], b0['indices'])*180/pi)

#          print b0['indices'] == b1['indices'] or b1['indices'] == b2['indices'] or b2['indices'] == b0['indices']
#          print planes0, planes1, planes2
#          print '='*20
#          answers.append([b0, b1, b2])
          
#          print planes0['angle'], vectors.angle(b0['indices'], b1['indices'])
#          print planes1['angle'], vectors.angle(b1['indices'], b2['indices'])
#          print planes2['angle'], vectors.angle(b2['indices'], b0['indices'])
          
          
#          print triplets
#          print vectors.tripleProduct(b0['indices'], b1['indices'], b2['indices'])
          
          triplets = {'A': b0, 'B': b1, 'C': b2, 'AB': planes0['angle'], 'BC': planes1['angle'], 'CA': planes2['angle']}
          
          
          solutions = getExactHKL2(triplets, thetas, band3P, L)
#          print len(solutions), b0['indices'],b1['indices'], b2['indices']
          
          totalSolutions += solutions
          
  return totalSolutions

def getExactHKL2(triplets, thetas, band3P, L):
  exhkl = []
  np = 0
  
  dp1 = cos(triplets['AB'])*thetas[0]['sign']
  dp2 = cos(triplets['BC'])*thetas[1]['sign']
  dp3 = cos(triplets['CA'])*thetas[2]['sign']
  
  famA = triplets['A']['family']
  famB = triplets['B']['family']
  famC = triplets['C']['family']
  
  nPermsA = len(L.getReflectors().getReflectorsListByFamily(famA))
  nPermsB = len(L.getReflectors().getReflectorsListByFamily(famB))
  nPermsC = len(L.getReflectors().getReflectorsListByFamily(famC))
  
#  print famA, nPermsA
#  print famB, nPermsB
#  print famC, nPermsC
#  
  reflectorsFamA = L.getReflectors().getReflectorsListByFamily(famA)
  reflectorsFamB = L.getReflectors().getReflectorsListByFamily(famB)
  reflectorsFamC = L.getReflectors().getReflectorsListByFamily(famC)
  
  for iA in range(2*nPermsA):
    if iA < nPermsA:
      A = reflectorsFamA[iA]
    else:
      A = -reflectorsFamA[iA-nPermsA]
    
    for iC in range(2*nPermsC):
      if iC < nPermsC:
        C = reflectorsFamC[iC]
      else:
        C = -reflectorsFamC[iC-nPermsC]
      
      AdC = vectors.directionCosine(A, C)
      dAC = abs(AdC - dp3)
      if dAC > zeroPrecision: continue
      
#      print _acos(AdC)*180/pi, _acos(dp2)*180/pi, A, C
      
      for iB in range(2*nPermsB):
        if iB < nPermsB:
          B = reflectorsFamB[iB]
        else:
          B = -reflectorsFamB[iB-nPermsB]
        
        AdB = vectors.directionCosine(A, B)
        dAB = abs(AdB - dp1)
        if dAB > zeroPrecision: continue
        
#        print _acos(AdB)*180/pi, _acos(dp1)*180/pi, A, B
        
        BdC = vectors.directionCosine(B, C)
        dBC = abs(BdC - dp2)
        if dBC > zeroPrecision: continue
        
#        print _acos(BdC)*180/pi, _acos(dp2)*180/pi, B, C
        
#        print A, B, C
        
        triP = vectors.tripleProduct(A, B, C)
        
        if triP*band3P > 0.0:
#          np += 1
          
          
          
#          print '%s %s %4.2f || %s %s %4.2f' % (triplets['A']['indices'], triplets['B']['indices'], triplets['AB']*180/pi, A, B, vectors.angle(A, B)*180/pi)
          
#        
          exhkl.append({'A': A, 'B': B, 'C': C})
          
          if triP > -zeroPrecision and triP < zeroPrecision:
            exhkl.append({'A': -A, 'B': -B, 'C': C})
            exhkl.append({'A': A, 'B': -B, 'C': C})
  
  return exhkl

def checkBandConsistency(planes0, planes1, planes2):
  for i in ['reflector1', 'reflector2']:
    for j in ['reflector1', 'reflector2']:
      for k in ['reflector1', 'reflector2']:
        i_ = _otherReflector(i)
        j_ = _otherReflector(j)
        k_ = _otherReflector(k)
        
        if planes0[i_]['family'] == planes1[j]['family'] and planes1[j_]['family'] == planes2[k]['family'] and planes2[k_]['family'] == planes0[i]['family']:
#          if planes0[i]['indices'] == planes1[j]['indices']: continue
#          if planes1[j]['indices'] == planes2[k]['indices']: continue
#          if planes2[k]['indices'] == planes0[i]['indices']: continue
          
          return planes0[i], planes1[j], planes2[k]
  
  return False, False, False

def _otherReflector(reflector):
  if reflector == 'reflector1':
    return 'reflector2'
  else:
    return 'reflector1'

def isColinear():
  pass

def calculateOrientation(n1, n2, hkl1, hkl2):
#  try:
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
    
#    qS = quaternions.axisAngleToQuaternion(-70/180.0*pi, (1,0,0))
    
    g = qC.conjugate() * qP #* qS.conjugate()
    
    return g.normalize()
#  except:
#    return False

def calculateOrientation2(norm, normp, bhkl, bhklp):
  
  es = [[0,0,0],[0,0,0],[0,0,0]]
  ec = [[0,0,0],[0,0,0],[0,0,0]]
  g = [[0,0,0],[0,0,0],[0,0,0]]
  
  mag = 2.0 * vectors.dot(norm, normp)
  mag0 = 1.0 / sqrt(2.0 + mag)
  mag1 = 1.0 / sqrt(2.0 - mag)
  for i in range(3):
    es[0][i] = (norm[i]+normp[i]) * mag0
    es[1][i] = (norm[i]-normp[i]) * mag0
  es[2] = vectors.cross(vectors.vector(es[0]), vectors.vector(es[1]))
  
  mag0 = 1.0 /sqrt(vectors.dot(bhkl,bhkl))
  mag1 = 1.0 /sqrt(vectors.dot(bhklp,bhklp))
  
  for i in range(3):
    bhkl[i] *= mag0
    bhklp[i] *= mag1
  
  mag = 2*vectors.dot(bhkl, bhklp)
  mag0 = 1.0 / sqrt(2.0 + mag)
  mag1 = 1.0 / sqrt(2.0 - mag)
  for i in range(3):
    ec[0][i] = (bhkl[i]+bhklp[i])*mag0
    ec[1][i] = (bhkl[i]-bhklp[i])*mag1
  ec[2] = vectors.cross(vectors.vector(ec[0]), vectors.vector(ec[1]))
  
  for i in range(3):
    for j in range(3):
      g[i][j] = ec[0][i]*es[0][j] + ec[1][i]*es[1][j] + ec[2][i]*es[2][j]
  
  return quaternions.matrixtoQuaternion(g)

def uniqueSolution(orientations):
  uniqueOrientations = []
  
  if len(orientations) > 0:
    uniqueOrientations.append(orientations[0])
  
  for i in range(1, len(orientations)):
    for j in range(i):
      tg = False
      tg = compareOrientation(orientations[j], orientations[i])
      if tg: break
    
    if not tg:
      uniqueOrientations.append(orientations[i])
  
  return uniqueOrientations

def compareOrientation(o1, o2):
  symmetries = symmetry.cubicSymmetries()
  
  toltr = 1 + 2*cos(3/180.0*pi)
  dtr = 2*sin(3/180.0*pi)
  
  for qS in symmetries:
    trace = 0.0
    
    matrix = (qS * o1 * o2.conjugate()).toMatrix()
    trace += matrix[0][0] + matrix[1][1] + matrix[2][2]
    
    if trace > toltr:
      return True
    
    if abs(trace-1) > dtr and abs(trace) > dtr and abs(trace+1) > dtr: return False
    
  return False
    
if __name__ == '__main__':
  
  import EBSDTools.crystallography.lattice as lattice
  
  patternSize = (670,510)
  patternCenter = (0.0, 0.0)
  detectorDistance = 0.3
  
  #Pattern reconstruction
#  root = 'i:/Philippe Pinard/'
  root = 'c:/documents/'
#  folder = 'I:/Philippe Pinard/workspace/EBSDTools/patternSimulations/rotation/m_000.csv'
#  folder = 'c:/documents/workspace/EBSDTools/patternSimulations/test/fcc_pcz__001.bmp' + ".csv"
#  filename = os.path.join(root, 'workspace/EBSDTools/indexation/test/fcc_1_pcz__000.bmp' + ".csv")
  filename = os.path.join(root, 'workspace/EBSDTools/indexation/test/test_wright1.bmp' + ".csv")
#  folder = os.path.join(root, 'workspace/EBSDTools/patternSimulations/rotation/test_2_000' + ".csv")
  
  atomsFCC = {(0,0,0): 26, 
           (0,0.5,0.5): 26,
           (0.5,0,0.5): 26,
           (0.5,0.5,0): 26}
  atomsBCC = {(0,0,0): 26, 
           (0.5,0.5,0.5): 26}
  
  L = lattice.Lattice(a=5.34, b=5.34, c=5.34, alpha=pi/2, beta=pi/2, gamma=pi/2, atoms=atomsFCC, reflectorsMaxIndice=3)
  
  lut = getLUT(L)
#  print len(lut)
#  printLUT(lut)
  
  totalThetas = []
  totalSolutions = []
  
  kikuchiNormals = getPBnormals(filename, patternCenter, detectorDistance, patternSize)
  
  triplets = triplets.findTriplets(len(kikuchiNormals))
  for triplet in triplets:
    print '='*25
    tripletNormals = [kikuchiNormals[triplet[0]], kikuchiNormals[triplet[1]], kikuchiNormals[triplet[2]]]
#  print len(tripletNormals)
#  
    thetas, band3P = getPBangles(tripletNormals)
#    print thetas
#    totalThetas.append(thetas[0]['angle'])
#    totalThetas.append(thetas[1]['angle'])
#    totalThetas.append(thetas[2]['angle'])
    solutions = findBand(thetas, band3P, lut, L)
    
    
    orientations = []
    if len(solutions) > 0:
#      print tripletNormals, thetas, total
#      print total , bands
#      print total
      for solution in solutions:
        orientations.append(calculateOrientation(tripletNormals[0], tripletNormals[1], solution['A'], solution['B']))
    
    
      uniqueSolutions = uniqueSolution(orientations)
      
      for newSolution in uniqueSolutions:
        tg = False
        for oldSolution in totalSolutions:
          tg = compareOrientation(oldSolution['q'], newSolution)
          if tg:
            oldSolution['vote'] += 1
            break
        
        if not tg:
          totalSolutions.append({'q': newSolution, 'vote': 1})
          
#      for solution in uniqueSolutions:
#        print eulers.degEulers(eulers.positiveEulers(solution.toEulerAngles()))
      
      
  print totalSolutions
  
  max = 0
  
  for solution in totalSolutions:
    print eulers.degEulers(eulers.positiveEulers(solution['q'].toEulerAngles())), solution['vote']
    
    if solution['vote'] > max:
      max = solution['vote']
      topSolution = solution
  
  print topSolution
  print eulers.degEulers(eulers.positiveEulers(topSolution['q'].toEulerAngles()))
  
  qDetectorOrientation = quaternions.axisAngleToQuaternion(pi, (0,0,1)) * quaternions.axisAngleToQuaternion(-90/180.0*pi, (1,0,0))
  
  ad = topSolution['q'] * qDetectorOrientation.conjugate()
  print eulers.degEulers(eulers.positiveEulers(ad.toEulerAngles()))
  
  ad = topSolution['q'] * qDetectorOrientation
  print eulers.degEulers(eulers.positiveEulers(ad.toEulerAngles()))
  
  
  
  
#  qDetectorOrientation_ = qTilt * qDetectorOrientation.conjugate() * qTilt.conjugate()
  
#  smallTotalThetas = []
#  for theta in totalThetas:
#    inSmall = False
#    for smallTheta in smallTotalThetas:
#      if abs(theta - smallTheta) < zeroPrecision:
#        inSmall = True
#      
#    if not inSmall:
#      smallTotalThetas.append(theta)
#  
#  smallTotalThetas.sort()
#  print smallTotalThetas
#  print totalCounts>>>>>>> MERGE-SOURCE
