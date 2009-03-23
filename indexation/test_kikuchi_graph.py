#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Philippe Pinard (philippe.pinard@gmail.com)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2009 Philippe Pinard"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = ""
__svnDate__ = ""
__svnId__ = ""

# Standard library modules.
import os
import csv

# Third party modules.

# Local modules.
import Chart.chart

# Globals and constants variables.

def plotKikuchiLineToNormalResults():
  graph = Chart.chart.Figure(subplots='2x2'
                             , figsize=(8,8)
                             , axes={1:(1,1),2:(1,1),3:(1,1),4:(1,1)})
  
  results = list(csv.reader(open('test_kikuchi.csv' ,'r')))
  
  rhos = [-49] + range(-40,50,10) + [49]
  
  for rho in range(len(results[0])/3):
    xS = []
    yS = []
    
    #x-z
    for angle in range(len(results)):
      xS.append(results[angle][rho*3])
      yS.append(results[angle][rho*3+2])
      
    graph.addSerieScatter(subplot_id=1, x=xS, y=yS, label='%i' % rhos[rho])
    
    xS = []
    yS = []
    
    #x-y
    for angle in range(len(results)):
      xS.append(results[angle][rho*3])
      yS.append(results[angle][rho*3+1])
      
    graph.addSerieScatter(subplot_id=3, x=xS, y=yS, label='__nolegend__')
    
    xS = []
    yS = []
    
    #y-z
    for angle in range(len(results)):
      xS.append(results[angle][rho*3+1])
      yS.append(results[angle][rho*3+2])
      
    graph.addSerieScatter(subplot_id=2, x=xS, y=yS, label='__nolegend__')
  
  graph.setAxisLabel('$x$', axis_id='ax1', subplot_id=1)
  graph.setAxisLabel('$z$', axis_id='ay1', subplot_id=1)
  graph.setAxisLabel('$y$', axis_id='ax1', subplot_id=2)
  graph.setAxisLabel('$z$', axis_id='ay1', subplot_id=2)
  graph.setAxisLabel('$x$', axis_id='ax1', subplot_id=3)
  graph.setAxisLabel('$y$', axis_id='ay1', subplot_id=3)
  
  for subplot_id in range(4):
    graph.setAxisLimits(limits=[-1,1], axis_id='ax1', subplot_id=subplot_id+1)
    graph.setAxisLimits(limits=[-1,1], axis_id='ay1', subplot_id=subplot_id+1)
  
  graph.addFigureLegend(location='lower right')
  graph.show()

if __name__ == '__main__':
  plotKikuchiLineToNormalResults()
