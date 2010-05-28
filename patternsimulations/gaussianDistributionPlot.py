'''
Created on Apr 24, 2009

@author: ppinard
'''
import Chart.chart
from math import exp, pi, sqrt,cos, log10
import EBSDTools.mathTools.errorFunction as errorFunction


arrhenius = lambda p, x: p[0] * exp(float(p[1]/x)) + p[2]

erfP = lambda p, x: p[0] * errorFunction.erf(p[1]*(x-p[2])) + p[3]

def stddev(thickness, normalizedIntensity):
  amplitude = (2*thickness-(thickness/5.0))/2.0
  p = [amplitude, -5, 0.5, amplitude+thickness/5.0]
  x = normalizedIntensity
  return erfP(p, x)

def colormin(intensityBackground, normalizedIntensity, intensityBand, intensityMin):
  intensityBackground = 0.0
  amplitude = (1.0-intensityBackground/2.0)/2.0
  p = [amplitude, -4, 0.6, amplitude+intensityBackground/2.0]
  x = normalizedIntensity
  return erfP(p,x)*intensityBand
  
def bandColorIntensityLog10(**args):
  normalizedIntensity = args['normalizedIntensity']
  intensityMax = args['intensityMax']
  intensityMin = args['intensityMin']
  
  return log10(normalizedIntensity+1)*((intensityMax-intensityMin)/log10(2))+intensityMin


graph = Chart.chart.Figure()

x = []
y = []
thickness = 10
for i in range(0,100):
  normalizedIntensity = i/100.0
  x.append(normalizedIntensity)
  y.append(stddev(thickness, normalizedIntensity))

marker = Chart.chart.createMarker(ms=0)
graph.addSerieScatter(x=x, y=y, paramsMarker=marker)

graph.setAxisLabel('Normalized Intensity', axis_id='ax1')
graph.setAxisLabel(r'$\sigma$', axis_id='ay1')

graph.show()

graph = Chart.chart.Figure()

x = []
y1 = []
y2 = []
y3 = []
p = [1.0, 5, 0.5, 0.0]
intensityBackground = 0.5
intensityMin = intensityBackground
thickness = 10
for i in range(1,100):
  normalizedIntensity = i/100.0
  x.append(normalizedIntensity)
  intensityBand = bandColorIntensityLog10(intensityMin=intensityMin
                                          , intensityMax=1.0
                                          , normalizedIntensity=normalizedIntensity)
  y1.append(colormin(intensityBackground, normalizedIntensity, intensityBand, intensityMin))
  y2.append(intensityBand)
  y3.append(intensityBackground)
  

marker = Chart.chart.createMarker(ms=0)
graph.addSerieScatter(x=x, y=y1, label='Minimum', paramsMarker=marker)
graph.addSerieScatter(x=x, y=y2, label='Band', paramsMarker=marker)
graph.addSerieScatter(x=x, y=y3, label='Background', paramsMarker=marker)

graph.setAxisLabel('Normalized Intensity', axis_id='ax1')
graph.setAxisLabel('Intensity (color)', axis_id='ay1')

graph.addLegend()

graph.show()