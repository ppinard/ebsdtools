import EBSDTools.mathTools.vectors as vectors
from EBSDTools.mathTools.mathExtras import zeroPrecision
import EBSDTools.mathTools.quaternions as quaternions
import EBSDTools.mathTools.eulers as eulers
from math import pi, sqrt
import visual

def kikuchiLineToNormal(m, k, patternCenter, detectorDistance, color=None):
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
  
#  print x2-x1
#  visual.arrow(frame=f, pos=(0,detectorDistance*10,0), axis=((x2-x1)*10).normalize().toTuple(), color=color)
  n = vectors.cross(x2, x1).normalize()
  return n

def calculateOrientation(n1, n2, hkl1, hkl2):
  eP1 = n1 / n1.norm()
  eP2 = vectors.cross(n1, n2)
  eP2 /= eP2.norm()
  eP3 = vectors.cross(eP1, eP2).normalize()
  
#  print eP1, eP2, eP3
  
  mP = [[eP1[0], eP2[0], eP3[0]],
       [eP1[1], eP2[1], eP3[1]],
       [eP1[2], eP2[2], eP3[2]]]
  
  qP = quaternions.matrixtoQuaternion(mP)
#  qP = quaternions.matrixtoQuaternion([eP1.toList(), eP2.toList(), eP3.toList()])
  
  eC1 = hkl1 / hkl1.norm()
  eC2 = vectors.cross(hkl1, hkl2)
  eC2 /= eC2.norm()
  eC3 = vectors.cross(eC1, eC2).normalize()
  
  mC = [[eC1[0], eC2[0], eC3[0]],
       [eC1[1], eC2[1], eC3[1]],
       [eC1[2], eC2[2], eC3[2]]]
  
  qC = quaternions.matrixtoQuaternion(mC)
#  qC = quaternions.matrixtoQuaternion([eC1.toList(), eC2.toList(), eC3.toList()])
  
#    qS = quaternions.axisAngleToQuaternion(-70/180.0*pi, (1,0,0))
  
#  print mP
#  print mC
  
  g = qP * qC.conjugate()
  
#  print g.toMatrix()
  
#  g = g.conjugate()
  
  return g.normalize()


def setZpositive(n):
  if n[2] < 0:
    return -n
  else:
    return n

def setZnegative(n):
  if n[2] > 0:
    return -n
  else:
    return n

def main():
  patternCenter = (0,0)
#  line1 = (-0.78020600871, -0.139892297446) # (1,1,-1)
#  line2 = (1.6731571851, 0.643352076153) # (1,1,1)
  
  detectorDistance = 0.3
  
  visual.display(title='Graph of position', width=400, height=400)
#  visual.sphere(pos=(0,0,0), radius=0.05, color=visual.color.white)
#  visual.box(pos=(0,detectorDistance*10,0), length=10, height=0.1, width=10, color=visual.color.cyan)
#  visual.arrow(pos=(0,0,0), axis=(5,0,0), shaftwidth=0.01, color=visual.color.red)
#  visual.arrow(pos=(0,0,0), axis=(0,5,0), shaftwidth=0.01, color=visual.color.green)
#  visual.arrow(pos=(0,0,0), axis=(0,0,5), shaftwidth=0.01, color=visual.color.blue)
  
  lines = []
  
  #27deg
  line1 = (-0.324919696233, -0.223048820676); hkl1 = vectors.vector(1,1,1) # (111)
  line2 = (3.07768353718, -0.686473683381); hkl2 = vectors.vector(1,-1,-1) # (1-1-1)
  
  #27deg no detectorPosition
  line1 = (-0.437016024449, -0.403499107178); hkl1 = vectors.vector(1,1,1) # (111)
  line2 = (1.34499702393, -0.131104807335); hkl2 = vectors.vector(1,-1,-1) # (1-1-1)
  
#  #78deg no detectorPosition
#  line1 = (0.770235909916, -0.355817787465); hkl1 = vectors.vector(1,1,1) # (111)
#  line2 = (1.18605929155, 0.231070772975); hkl2 = vectors.vector(1,-1,-1) # (1-1-1)
#  
  #41deg no detectorPosition
  line1 = (-0.0986505512323, -0.4232305827645); hkl1 = vectors.vector(1,1,1) # (111)
  line2 = (1.41076860921, -0.0295951653697); hkl2 = vectors.vector(1,-1,-1) # (1-1-1)
  lines.append([line1,line2])
#  
#  #41deg no detectorPosition
#  line1 = (-0.0986505512323, -0.4232305827645); hkl1 = vectors.vector(1,1,1) # (111)
#  line2 = (0.0986505512323, 0.423230582764); hkl2 = vectors.vector(1,1,-1) # (1-1-1)
#  lines.append([line1,line2])
  
  #43deg no detectorPosition
  line1 = (-0.0493553415567, -0.424005618505); hkl1 = vectors.vector(1,1,1) # (111)
  line2 = (1.41335206168, -0.014806602467); hkl2 = vectors.vector(1,-1,-1) # (1-1-1)
  lines.append([line1,line2])
  
  
  #45deg no detectorPosition
  line1 = (1.11022302463e-016, -0.424264068712); hkl1 = vectors.vector(1,1,1) # (111)
  line2 = (1.41421356237, 3.33066907388e-017); hkl2 = vectors.vector(1,1,-1) # (1-1-1)
  lines.append([line1,line2])
  
  #50deg no detectorPosition
  line1 = (0.123256833432, -0.422649615842); hkl1 = vectors.vector(1,1,1) # (111)
  line2 = (1.40883205281, 0.0369770500297); hkl2 = vectors.vector(1,-1,-1) # (1-1-1)
  lines.append([line1,line2])
  
  #55deg no detectorPosition
  line1 = (0.245575607938, -0.417818544192); hkl1 = vectors.vector(1,1,1) # (111)
  line2 = (1.39272848064, 0.0736726823814); hkl2 = vectors.vector(1,-1,-1) # (1-1-1)
  lines.append([line1,line2])
  
#  #25deg euler2 no detectorPosition
#  line1 = (-0.752487319306, -0.10919107028); hkl1 = vectors.vector(1,1,1) # (111)
#  line2 = (0.752487319306, -0.10919107028); hkl2 = vectors.vector(1,-1,-1) # (1-1-1)
#  
#  #36deg euler2 no detectorPosition
#  line1 = (-0.71592095616, -0.0475153320974); hkl1 = vectors.vector(1,1,1) # (111)
#  line2 = (0.71592095616, -0.0475153320974); hkl2 = vectors.vector(1,-1,-1) # (1-1-1)
#  
#  #70deg euler2 no detectorPosition
#  line1 = (-0.78020600871, 0.139892297446); hkl1 = vectors.vector(1,1,1) # (111)
#  line2 = (0.78020600871, 0.139892297446); hkl2 = vectors.vector(1,-1,-1) # (1-1-1)
#  
#  95deg euler2 no detectorPosition
#  line1 = (-1.10006286763, 0.357526077778); hkl1 = vectors.vector(1,1,1) # (111)
#  line2 = (1.10006286763, 0.357526077778); hkl2 = vectors.vector(1,-1,-1) # (1-1-1)
#  
#  #15-15-15 no detectorPosition
#  line1 = (-0.345942194925, -0.251548262237); hkl1 = vectors.vector(1,1,1) # (111)
#  line2 = (1.12521433251, -0.0242186091053); hkl2 = vectors.vector(1,-1,-1) # (1-1-1)
  
  #98deg euler1 no detectorPosition
  line1 = ( 1.1294411697, -0.255328490334); hkl1 = vectors.vector(1,1,1) # (111)
  line2 = (0.851094967782, 0.33883235091); hkl2 = vectors.vector(1,-1,-1) # (1-1-1)
  lines.append([line1,line2])
  
  #194DEG euler1 no detectorPosition
  line1 = ( 0.728373830676, 0.363665286563); hkl1 = vectors.vector(1,1,1) # (111)
  line2 = (-1.21221762188, 0.218512149203); hkl2 = vectors.vector(1,-1,-1) # (1-1-1)
  lines.append([line1,line2])
  
  #286deg euler1 no detectorPosition
  line1 = (-1.23689905176, 0.205687302036); hkl1 = vectors.vector(1,1,1) # (111)
  line2 = (-0.685624340121, -0.371069715527); hkl2 = vectors.vector(1,-1,-1) # (1-1-1)
  lines.append([line1,line2])
  
  #355deg euler1 no detectorPosition
  line1 = (-1.08335044084, -0.272711686603); hkl1 = vectors.vector(1,1,1) # (111)
  line2 = (0.909038955344, -0.325005132252); hkl2 = vectors.vector(1,-1,-1) # (1-1-1)
  lines.append([line1,line2])
  
  global f 
  f =visual.frame()
  
  colors = [visual.color.red, visual.color.green, visual.color.blue, visual.color.magenta, visual.color.white, visual.color.orange, visual.color.yellow, visual.color.cyan, visual.color.magenta]
  
  for i, line in enumerate(lines):
    print '=' * 35
    n1 = setZpositive(kikuchiLineToNormal(line[0][0], line[0][1], patternCenter, detectorDistance, colors[i]).positive())
    n2 = setZnegative(kikuchiLineToNormal(line[1][0], line[1][1], patternCenter, detectorDistance, colors[i]).positive())
    print n1, n2
    visual.arrow(frame=f, pos=(0,0,0), axis=n1.toTuple(), color=colors[i])
    visual.arrow(frame=f, pos=(0,0,0), axis=n2.toTuple(), color=colors[i])
  
  
    q = calculateOrientation(n1, n2, hkl1, hkl2)
  #  q = calculateOrientation2(n1.positive(), n2.positive(), hkl1, hkl2)
    print q
  #  q = calculateOrientation(n1, n2, hkl1, hkl2)
    print eulers.degEulers(eulers.positiveEulers(q.toEulerAngles()))
  
  

if __name__ == '__main__':
  main()