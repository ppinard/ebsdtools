#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Philippe Pinard (philippe.pinard@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2008 Philippe Pinard"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = "$Revision$"
__svnDate__ = "$Date$"
__svnId__ = "$Id$"

# Standard library modules.
import unittest
import logging

# Third party modules.

# Local modules.
import orientation
import EBSDTools.mathTools.quaternions as quaternions
import EBSDTools.mathTools.vectors as vectors
import EBSDTools.mathTools.eulers as eulers
from math import pi
from EBSDTools.mathTools.mathExtras import zeroPrecision

# Globals and constants variables.

class TestOrientation(unittest.TestCase):

  def setUp(self):
    unittest.TestCase.setUp(self)

  def tearDown(self):
    unittest.TestCase.tearDown(self)

  def testSkeleton(self):
#    self.fail("Test if the testcase is working.")
    self.assert_(True)
  
  def testKikuchiLineToNormal(self):
    #Test that the normal are the same at different detector distance
    patternCenter = (0.0, 0.0)
    
    detectorDistance = 0.3
    lines = []
    lines.append((1.22460635382e-016, 0.3)) # (0, 2, -2)
    lines.append((None, 0.3)) #(2, 0, -2)
    lines.append((1.0, -4.99600361081e-017)) #(2, -2, 0)
    lines.append((None, -0.3)) #(2, 0, 2)
    lines.append((-1.0, -8.32667268469e-017)) #(2, 2, 0)
    lines.append((1.22460635382e-016, -0.3)) #(0, 2, 2)
    lines.append((None, -7.39557098645e-033)) #(2, 0, 0)
    lines.append((1.22460635382e-016, -6.66133814775e-017)) #(0, 2, 0)
    lines.append((1.0, -0.3)) #(1, -1, -1)
    lines.append((1.0, 0.3)) #(1, -1, 1) 
    lines.append((-1.0, 0.3)) #(1, 1, -1)
    lines.append((-1.0, -0.3)) #(1, 1, 1)
    
    ns1 = []
    for line in lines:
      ns1.append(orientation.kikuchiLineToNormal(line[0], line[1], patternCenter, detectorDistance))
    
    detectorDistance = 0.5
    lines = []
    lines.append((1.22460635382e-016, 0.5)) #(0, 2, -2)
    lines.append((None, 0.5)) #(2, 0, -2)
    lines.append((1.0, -8.32667268469e-017)) #(2, -2, 0)
    lines.append((None, -0.5)) #(2, 0, 2)
    lines.append((-1.0, -1.38777878078e-016)) #(2, 2, 0)
    lines.append((1.22460635382e-016, -0.5)) #(0, 2, 2)
    lines.append((None, -1.23259516441e-032)) #(2, 0, 0)
    lines.append((1.22460635382e-016, -1.11022302463e-016)) #(0, 2, 0)
    lines.append((1.0, -0.5)) #(1, -1, -1)
    lines.append((1.0, 0.5)) #(1, -1, 1)
    lines.append((-1.0, 0.5)) #(1, 1, -1)
    lines.append((-1.0, -0.5)) #(1, 1, 1)
    
    ns2 = []
    for line in lines:
      ns2.append(orientation.kikuchiLineToNormal(line[0], line[1], patternCenter, detectorDistance))
    
    for i in range(len(ns1)):
      for j in range(3):
        self.assertAlmostEqual(ns1[i][j], ns2[i][j], 3)
  
  def testCalculateOrientation(self):
    import EBSDTools.patternSimulations.patternSimulations as patternSimulations
    
    patternCenter = (0.0, 0.0)
    detectorDistance = 0.3
    
    planes = {'111': {'vector': (1,1,1)}, '1-1-1': {'vector': (1,-1,-1)}}
    
    tilt = 0.0
    inputs = [{'eulers': [0.0, 0.0, 0.0], 'tilt': tilt},
              {'eulers': [34.0, 0.0, 0.0], 'tilt': tilt},
              {'eulers': [98.0, 0.0, 0.0], 'tilt': tilt},
              {'eulers': [198.0, 0.0, 0.0], 'tilt': tilt},
              {'eulers': [305.0, 0.0, 0.0], 'tilt': tilt},
              {'eulers': [0.0, 36.0, 0.0], 'tilt': tilt},
              {'eulers': [78.0, 36.0, 256.0], 'tilt': tilt},
              {'eulers': [12.0, 36.0, 25.0], 'tilt': tilt},
              {'eulers': [346.0, 75.0, 12.0], 'tilt': tilt},
              {'eulers': [78.0, 78.0, 178.0], 'tilt': tilt},
              {'eulers': [78.0, 78.0, 156.0], 'tilt': tilt},
              {'eulers': [78.0, 78.0, 215.0], 'tilt': tilt},
              {'eulers': [78.0, 78.0, 1.0], 'tilt': tilt}]
    
    for input in inputs:
      print '-'*35
      eulerAngles = input['eulers']
      tilt = input['tilt']
      
      angles = eulers.degEulersToRadEulers(eulerAngles[0], eulerAngles[1], eulerAngles[2]) 
      
#      qSpecimenRotation = quaternions.quaternion(1,0,0,0)
      qCrystalRotation = quaternions.eulerAnglesToQuaternion(angles)
      print qCrystalRotation.normalize(), qCrystalRotation.toEulerAngles().toDeg()
      
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
      
      n1 = orientation.kikuchiLineToNormal(planes['111']['m'], planes['111']['k'], patternCenter, detectorDistance)
      n2 = orientation.kikuchiLineToNormal(planes['1-1-1']['m'], planes['1-1-1']['k'], patternCenter, detectorDistance)
      
      qRotations_ = [(qDetectorOrientation_ * qTilt).conjugate()]
      qRotations_ = [qTilt.conjugate()]
      n1_ = orientation.setZpositive(quaternions.rotate(quaternions.quaternion(0, n1), qRotations_).vector().positive())
      n2_ = orientation.setZnegative(quaternions.rotate(quaternions.quaternion(0, n2), qRotations_).vector().positive())
#      n1_ = orientation.setZpositive(n1.positive())
#      n2_ = orientation.setZnegative(n2.positive())
      
#      print n1_, n2_
      
#      print n1, n2
#      n1_ = n1.positive()
#      n2_ = n2.positive()
#      print n1_, n2_
      
      q = orientation.calculateOrientation(n1, n2, vectors.vector(planes['111']['vector']), vectors.vector(planes['1-1-1']['vector']))
#      q = orientation.calculateOrientation(n1_, n2_, vectors.vector(planes['111']['vector']), vectors.vector(planes['1-1-1']['vector']))
      
      qf = -q
      qAngles = qf.toEulerAngles().toDeg()
      
#      print abs(qAngles[0] - angles.toDeg()[0])
#      if abs(qAngles[0] - angles.toDeg()[0]) > zeroPrecision:
      print q
      print qf.normalize(), qAngles
      

if __name__ == '__main__':
  logging.getLogger().setLevel(logging.DEBUG)
  unittest.main()