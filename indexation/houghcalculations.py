#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Philippe Pinard (philippe.pinard@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2009 Philippe Pinard"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = ""
__svnDate__ = ""
__svnId__ = ""

# Standard library modules.
from math import pi, cos, sin, sqrt

# Third party modules.
import numpy
import scitools.multipleloop as multipleloop

# Local modules.
import Chart.chart

# Globals and constants variables.
THETA0 = 'theta0'
RHO0 = 'rho0'
RADIUS = 'radius'
WIDTH = 'width'

def boundaries():
  theta = numpy.arange(0, pi, 0.1)

  functions = []

  rho1 = (rho0 + w/2.0) * numpy.cos(theta - theta0) + \
         numpy.sqrt(R**2 - rho0**2)*numpy.sin(theta - theta0)
  functions.append(rho1)

  rho2 = (rho0 - w/2.0) * numpy.cos(theta - theta0) + \
         numpy.sqrt(R**2 - rho0**2)*numpy.sin(theta - theta0)
  functions.append(rho2)

  rho3 = (rho0 + w/2.0) * numpy.cos(theta - theta0) - \
         numpy.sqrt(R**2 - rho0**2)*numpy.sin(theta - theta0)
  functions.append(rho3)

  rho4 = (rho0 - w/2.0) * numpy.cos(theta - theta0) - \
         numpy.sqrt(R**2 - rho0**2)*numpy.sin(theta - theta0)
  functions.append(rho4)

  #Display
  fig = Chart.chart.Figure()

  paramsMarker = Chart.chart.createMarker(ms=0)
  for iFunction, function in enumerate(functions):
    fig.addSerieScatter(label='%i' % iFunction
                        , x=theta*180.0/pi
                        , y=function
                        , paramsMarker=paramsMarker)

  fig.setAxisLabel(r'$\theta$', axis_id='ax1')
  fig.setAxisLabel(r'$\rho$', axis_id='ay1')
  fig.addFigureLegend()

  fig.show()

def calculateRadon(theta0, rho0, width, radius):
  thetas = numpy.arange(theta0-5.0/180*pi, theta0+5.0/180*pi, 0.1/180*pi)
  rhos = numpy.arange(rho0-1, rho0+1, 0.01)

  #Radon counter
  print len(thetas), len(rhos)
  radon = numpy.zeros((len(rhos), len(thetas)))

  #Boundary limits
  fRho1 = lambda theta: (rho0 + width/2.0) * cos(theta - theta0) + \
                        sqrt(radius**2 - rho0**2)*sin(theta - theta0)
  fRho2 = lambda theta: (rho0 - width/2.0) * cos(theta - theta0) + \
                        sqrt(radius**2 - rho0**2)*sin(theta - theta0)
  fRho3 = lambda theta: (rho0 + width/2.0) * cos(theta - theta0) - \
                        sqrt(radius**2 - rho0**2)*sin(theta - theta0)
  fRho4 = lambda theta: (rho0 - width/2.0) * cos(theta - theta0) - \
                        sqrt(radius**2 - rho0**2)*sin(theta - theta0)

  #Radon solution
  fRegionA = lambda rho, theta: 2*sqrt(radius**2 - rho0**2) / abs(cos(theta - theta0))
  fRegionB = lambda rho, theta: width / abs(sin(theta - theta0))
  fRegionC_1 = lambda rho, theta: abs(rho + sqrt(radius**2 - rho0**2)*sin(theta - theta0) - \
                                      (rho0 + width/2.0)*cos(theta - theta0)) / \
                                      abs(sin(theta - theta0)*cos(theta - theta0))
  fRegionC_2 = lambda rho, theta: abs(rho - sqrt(radius**2 - rho0**2)*sin(theta - theta0) - \
                                      (rho0 + width/2.0)*cos(theta - theta0)) / \
                                      abs(sin(theta - theta0)*cos(theta - theta0))
  fRegionC_3 = lambda rho, theta: abs(rho + sqrt(radius**2 - rho0**2)*sin(theta - theta0) - \
                                      (rho0 - width/2.0)*cos(theta - theta0)) / \
                                      abs(sin(theta - theta0)*cos(theta - theta0))
  fRegionC_4 = lambda rho, theta: abs(rho - sqrt(radius**2 - rho0**2)*sin(theta - theta0) - \
                                      (rho0 - width/2.0)*cos(theta - theta0)) / \
                                      abs(sin(theta - theta0)*cos(theta - theta0))

  positions1Rhos = []
  positions1Thetas = []
  positions2Rhos = []
  positions2Thetas = []
  positions3Rhos = []
  positions3Thetas = []

  for i, theta in enumerate(thetas):
    rho1 = fRho1(theta)
    rho2 = fRho2(theta)
    rho3 = fRho3(theta)
    rho4 = fRho4(theta)
#    print rho1, rho2, rho3, rho4

    for j, rho in enumerate(rhos):
      #Region A
      if rho <= rho1 and \
         rho >= rho2 and \
         rho <= rho3 and \
         rho >= rho4:
        positions1Rhos.append(rho)
        positions1Thetas.append(theta)
        radon[j][i] = fRegionA(rho, theta)

      #Region B
      if (rho > rho1 and rho < rho4) or \
         (rho > rho3 and rho < rho2):
        positions2Rhos.append(rho)
        positions2Thetas.append(theta)
        radon[j][i] = fRegionB(rho, theta)

      #Region C
      if (rho > rho1 and rho < rho3 and rho > rho4):
        radon[j][i] = fRegionC_1(rho, theta)
      if (rho > rho3 and rho < rho1 and rho > rho2):
        radon[j][i] = fRegionC_2(rho, theta)
      if (rho < rho2 and rho > rho4 and rho < rho3):
        radon[j][i] = fRegionC_3(rho, theta)
      if (rho < rho4 and rho > rho2 and rho < rho1):
        radon[j][i] = fRegionC_4(rho, theta)

  return thetas, rhos, radon

def plotRadon(theta0,rho0, width, radius):
  fig = Chart.chart.Figure()

  thetas, rhos, radon = calculateRadon(theta0, rho0, width, radius,)
  fig.addSerieContour(x=thetas, y=rhos, z=radon, subplot_id=1)
  fig.setAxisLimits(limits=(rhos[0], rhos[-1]), axis_id='ay1', subplot_id=1)
  fig.setAxisLimits(limits=(thetas[0], thetas[-1]), axis_id='ax1', subplot_id=1)

  fig.show()
  return

def regions():
  parameters = {}

  parameters[THETA0] = [0, pi/4, pi/6]
  parameters[RHO0] = [0.5]
  parameters[RADIUS] = [1]
  parameters[WIDTH] = [0.5]

  (allCases, names, varied) = multipleloop.combine(parameters)

  for case in allCases:
    case = dict(zip([THETA0, RHO0, RADIUS, WIDTH], case))
    print case
    theta0 = case[THETA0]
    rho0 = case[RHO0]
    width = case[RADIUS]
    radius = case[WIDTH]

    plotRadon(theta0, rho0, width, radius)

if __name__ == '__main__':
  regions()
