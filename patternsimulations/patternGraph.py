import Chart
import Chart.graphics
import Chart.scatter2
import numpy
from math import cos, sin, pi

def computeYs(Xs,dd,pc,h,k,l):
  Ys = []
  
  tilt = 70 * pi / 180
  
  h70 = h
  k70 = k*cos(tilt) + l*sin(tilt)
  l70 = -k*sin(tilt) + l*cos(tilt)
  
  if l70 != 0:
    for x in Xs:
      Ys.append(-(h70/l70)*(x-pc[0]) - dd*k70/l70 + pc[1])
  
    return Ys
  else:
    return []

def main():
  scatter = Chart.scatter2.scatter(subplots='1x1'
                                  , axes={1:(1,1)}
                                  )
  
  Xs = numpy.arange(-3,3,0.1)
  
  dd = 1
  pc = (0,0)
  
  m = Chart.graphics.createMarker(ms=0)
  l = Chart.graphics.createLine(color='b')
  
  #FCC
  planes = [(1,-1,-1), (1,1,1), (1,1,-1), (1,-1,1),
            (2,-2,0), (2,0,-2), (0,2,-2), (2,2,0), (0,2,2), (2,0,2),
            (0,0,2), (2,0,0), (0,2,0),
            (1,1,2), (1,-3,1), (1,-1,-3), (1,1,-3), (1,-1,3), (1,-3,1), (3,-1,1), (3,1,1), (3,-1,-1), (1,3,-1), (1,3,1), (3,1,-1)]
  print len(planes)
  #BCC
  planes = [(1,-1,0), (1,0,-1), (0,1,-1), (1,1,0), (0,1,1), (1,0,1),
            (2,0,0), (0,2,0), (0,0,2),
            (1,-1,2), (1,1,2), (1,-1,-2), (1,1,-2), (1,-2,1), (1,-2,-1), (2,1,1), (1,2,-1), (2,-1,1), (2,-1,-1), (2,1,-1), (1,2,1)]
  print len(planes)
  
  for plane in planes:
    Ys = computeYs(Xs, dd, pc, plane[0], plane[1], plane[2])
    if len(Ys) > 0:
      scatter.addSerie(x=Xs, y=Ys, label=str(plane), marker=m, line=l)
  
  scatter.setupTicks(subplot_id=1
                     , axis_id='ax1'
                     , limits=[-3,3])
  scatter.setupTicks(subplot_id=1
                     , axis_id='ay1'
                     , limits=[-3,3])
  
#  scatter.addLegend()
  
  
  scatter.show()


if __name__ == '__main__':
  main()