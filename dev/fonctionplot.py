'''
Created on Apr 24, 2009

@author: ppinard
'''
import Chart.chart
from math import exp, pi, sqrt,cos
import Chart.fit


arrhenius = lambda p, x: p[0] * exp(float(p[1]/x)) + p[2]
def erf(p, x):
  z = p[1]*(x - p[2])
  
  answer = 2.0/sqrt(pi)*p[0]*(z - z**3/3.0 + z**5/10.0 - z**7/42.0 + z**9/216.0) + p[3]
  
  return answer

scos = lambda p, x: p[0] * cos(2*pi*p[1]*(x-p[2])) + p[3]


graph = Chart.chart.Figure()

x = []
y = []
thickness = 10
amplitude = (2*thickness-(thickness/5.0))/2.0
p = [-amplitude, 0.5, 0.0, amplitude+thickness/5.0]
print p
#p = [-0.5,0.5,0.0, 0.5]
for i in range(0,100):
  x.append(i/100.0)
  y.append(scos(p,i/100.0))

graph.addSerieScatter(x=x, y=y)

graph.show()
