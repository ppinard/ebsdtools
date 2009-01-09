from EBSDTools.mathTools.mathExtras import zeroPrecision
import EBSDTools.mathTools.quaternions as quaternions
import EBSDTools.mathTools.eulers as eulers
import EBSDTools.mathTools.matrices as matrices
import EBSDTools.mathTools.vectors as vectors
from math import pi, sqrt
import visual
import time

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
    x2 = vectors.vector(k, detectorDistance, 1.0)
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
#  x1 = x1.positive()
#  x2 = x2.positive()
#  visual.arrow(frame=f, pos=(0,0,0), axis=x1.normalize().toTuple(), color=visual.color.white, shaftwidth=0.01)
#  visual.arrow(frame=f, pos=(0,0,0), axis=x2.normalize().toTuple(), color=visual.color.blue, shaftwidth=0.01)
  n = vectors.cross(x1,x2).normalize()
#  print vectors.cross(x2, x1).normalize(), vectors.cross(x1, x2).normalize()
  return n

def calculateOrientation(n1, n2, hkl1, hkl2):
  eP1 = n1 / n1.norm()
  eP2 = vectors.cross(n1, n2)
  eP2 /= eP2.norm()
  eP3 = vectors.cross(eP1, eP2).normalize()
  
#  print eP1, eP2, eP3
  
  mP = matrices.matrix([[eP1[0], eP2[0], eP3[0]],
                        [eP1[1], eP2[1], eP3[1]],
                        [eP1[2], eP2[2], eP3[2]]])
#  mP = matrices.matrix([eP1.toList(), eP2.toList(), eP3.toList()])
  
  qP = quaternions.matrixtoQuaternion(mP)
#  qP = quaternions.matrixtoQuaternion([eP1.toList(), eP2.toList(), eP3.toList()])
  
  eC1 = hkl1 / hkl1.norm()
  eC2 = vectors.cross(hkl1, hkl2)
  eC2 /= eC2.norm()
  eC3 = vectors.cross(eC1, eC2).normalize()
  
  mC = matrices.matrix([[eC1[0], eC2[0], eC3[0]],
                        [eC1[1], eC2[1], eC3[1]],
                        [eC1[2], eC2[2], eC3[2]]])
#  mC = matrices.matrix([eC1.toList(), eC2.toList(), eC3.toList()])
  
  qC = quaternions.matrixtoQuaternion(mC) 
#  qC = quaternions.matrixtoQuaternion([eC1.toList(), eC2.toList(), eC3.toList()])
  
#    qS = quaternions.axisAngleToQuaternion(-70/180.0*pi, (1,0,0))
  
#  print mP
#  print mC
  
  g = qC.conjugate() * qP
  
#  print g.toMatrix()
  
#  g = g.conjugate()
  
  return g


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
  import EBSDTools.patternSimulations.patternSimulations as patternSimulations
  
  patternCenter = (0,0)
  detectorDistance = 0.3
  
  visual.display(title='Graph of position', width=400, height=400,ambient=0.5)
#  visual.sphere(pos=(0,0,0), radius=0.05, color=visual.color.white)
#  visual.box(pos=(0,detectorDistance*10,0), length=10, height=0.1, width=10, color=visual.color.cyan)
#  visual.arrow(pos=(0,0,0), axis=(5,0,0), shaftwidth=0.01, color=visual.color.red)
#  visual.arrow(pos=(0,0,0), axis=(0,5,0), shaftwidth=0.01, color=visual.color.green)
#  visual.arrow(pos=(0,0,0), axis=(0,0,5), shaftwidth=0.01, color=visual.color.blue)
  
  global f 
  f =visual.frame()
  
  colors = [visual.color.red, visual.color.green, visual.color.blue, visual.color.magenta, visual.color.white, visual.color.orange, visual.color.yellow, visual.color.cyan]
  
  tilt = 0.0
  inputs = []
#  inputs = [{'eulers': [0.0, 0.0, 0.0], 'tilt': tilt},
#              {'eulers': [34.0, 0.0, 0.0], 'tilt': tilt},
#              {'eulers': [98.0, 0.0, 0.0], 'tilt': tilt},
#              {'eulers': [198.0, 0.0, 0.0], 'tilt': tilt},
#              {'eulers': [355.0, 0.0, 0.0], 'tilt': tilt},
##              {'eulers': [0.0, 36.0, 0.0], 'tilt': tilt},
##              {'eulers': [78.0, 36.0, 256.0], 'tilt': tilt},
##              {'eulers': [12.0, 36.0, 25.0], 'tilt': tilt},
##              {'eulers': [346.0, 75.0, 12.0], 'tilt': tilt},
##              {'eulers': [78.0, 78.0, 178.0], 'tilt': tilt},
##              {'eulers': [78.0, 78.0, 156.0], 'tilt': tilt},
##              {'eulers': [78.0, 78.0, 215.0], 'tilt': tilt},
##              {'eulers': [78.0, 78.0, 1.0], 'tilt': tilt}
#            ]
  
  step =15
  for i in range(0,360,step):
    for j in range(0,180,step):
      for k in range(0,360,step):
        inputs.append({'eulers': [i, j, k], 'tilt': tilt})
#  
#  for j in range(0,180,step):
#    inputs.append({'eulers': [0, j, 0], 'tilt': tilt})
  
#  for k in range(0,360,step):
#    inputs.append({'eulers': [k, 0,0], 'tilt': tilt})
  
  ms = []
  ks = []
  
  for i, input in enumerate(inputs):
    
    eulerAngles = input['eulers']
    tilt = input['tilt']
    planes = {'111': {'vector': (1,1,1)}, '1-1-1': {'vector': (1,-1,-1)}}
    
    angles = eulers.degEulersToRadEulers(eulerAngles[0], eulerAngles[1], eulerAngles[2]) 
    
    qCrystalRotation = quaternions.eulerAnglesToQuaternion(angles)
    
    qTilt = quaternions.axisAngleToQuaternion(-tilt/180.0*pi, (1,0,0))
    qDetectorOrientation = quaternions.axisAngleToQuaternion(pi, (0,0,1)) * quaternions.axisAngleToQuaternion(-90/180.0*pi, (1,0,0))
    qDetectorOrientation_ = qTilt * qDetectorOrientation.conjugate() * qTilt.conjugate()
  
#      qRotations = [qDetectorOrientation_ * qTilt * qCrystalRotation * qSpecimenRotation]
    qRotations = [qDetectorOrientation_ * qTilt * qCrystalRotation]
    qRotations = [qTilt * qCrystalRotation]
    
    for plane in planes:
      qPlane = quaternions.quaternion(0, planes[plane]['vector'])
      planeRot = quaternions.rotate(qPlane, qRotations).vector()
    
      m, k = patternSimulations.computePlaneEquationOnCamera(plane=planeRot
                                        , patternCenter=patternCenter
                                        , detectorDistance=detectorDistance)
      
      planes[plane]['m'] = m
      planes[plane]['k'] = k
      
    
#      n1 = orientation.setZpositive(orientation.kikuchiLineToNormal(planes['111']['m'], planes['111']['k'], patternCenter, detectorDistance).positive())
#      n2 = orientation.setZnegative(orientation.kikuchiLineToNormal(planes['1-1-1']['m'], planes['1-1-1']['k'], patternCenter, detectorDistance).positive())
    
    n1 = kikuchiLineToNormal(planes['111']['m'], planes['111']['k'], patternCenter, detectorDistance)
    n2 = kikuchiLineToNormal(planes['1-1-1']['m'], planes['1-1-1']['k'], patternCenter, detectorDistance)
    
    
    qRotations_ = [(qDetectorOrientation_ * qTilt).conjugate()]
    qRotations_ = [qTilt.conjugate()]
#    n1_ = quaternions.rotate(quaternions.quaternion(0, n1), qRotations_).vector().positive()
#    n2_ = quaternions.rotate(quaternions.quaternion(0, n2), qRotations_).vector().positive()
    n1_ = setZpositive(quaternions.rotate(quaternions.quaternion(0, n1), qRotations_).vector())
    n2_ = setZnegative(quaternions.rotate(quaternions.quaternion(0, n2), qRotations_).vector())
    
    
    visual.arrow(frame=f, pos=(0,0,0), axis=n1_.toTuple(), color=colors[0], shaftwidth=0.01)
    visual.arrow(frame=f, pos=(0,0,0), axis=n2_.toTuple(), color=colors[0], shaftwidth=0.01)
#    visual.arrow(frame=f, pos=(0,0,0), axis=n1.toTuple(), color=colors[1], shaftwidth=0.01)
#    visual.arrow(frame=f, pos=(0,0,0), axis=n2.toTuple(), color=colors[1], shaftwidth=0.01)
    
    q = calculateOrientation(n1_, n2_, vectors.vector(planes['111']['vector']), vectors.vector(planes['1-1-1']['vector']))
    qf = q.conjugate()
    qAngles = qf.toEulerAngles().toDeg()
    
    
#    print '-'*35
#    print qCrystalRotation.normalize(), qCrystalRotation.toEulerAngles().toDeg()
#    print (planes['111']['m'], planes['111']['k']), (planes['1-1-1']['m'], planes['1-1-1']['k'])
#    print n1_, n2_
#    print qf, qAngles
    
    if planes['111']['m'] != None:
      ms.append(planes['111']['m'])
    else:
      ms.append(0)
    if planes['111']['k'] != None:
      ks.append(planes['111']['k'])
    else:
      ks.append(0)
    
#    time.sleep(0.5)
  
  
#  import Chart.chart
#  scatter = Chart.chart.Figure(subplots='1x1', axes={1:(1,2)})
#  scatter.addSerieScatter(axis_id='ax1', x=range(0,180,5), y=ms)
#  scatter.addSerieScatter(axis_id='ay2', x=range(0,180,5), y=ks)
#  scatter.show()

if __name__ == '__main__':
  main()