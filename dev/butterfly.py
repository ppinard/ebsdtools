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
from math import log

# Third party modules.
#import numpy.fft
#import PIL

# Local modules.

def houghMap():
  import EBSDTools.indexation.hough as hough
  import rmlimage.io.IO as IO
  
  mask = hough.createMaskDisc(width=168, height=128, centroid=(84,64), radius=59)
  
  H = hough.Hough('c:/documents/workspace/EBSDTools/indexation/testData/pattern1.bmp')
  H.calculateHough(angleIncrement=0.5, maskMap=mask)
  
  H._houghMap.setFile('c:/documents/workspace/EBSDTools/dev/hough1.bmp')
  IO.save(H._houghMap)
  

def butterfly():
  import numpy
  from PIL import Image
  
  mhough = numpy.asarray(Image.open('c:/documents/workspace/EBSDTools/dev/Lena256x256.bmp'))
#  mhough = numpy.fft.fftshift(mhough)
  
  mkernel = numpy.asarray(Image.open('c:/documents/workspace/EBSDTools/dev/5x5.bmp'))
#  mkernel = numpy.fft.fftshift(mkernel)
  
  fftHough = numpy.fft.fft2(mhough)
  fftKernel = numpy.fft.fft2(mkernel)
  
  print fftHough.shape, fftKernel.shape
  
  fftConvol = fftHough * fftKernel
  
#  sfftConvol = numpy.fft.ifftshift(fftConvol)
  convol = numpy.fft.ifft2(fftConvol)
  convol = 255 / (1+numpy.max(convol)) * convol
  
  
  sfftHough = numpy.fft.ifftshift(fftHough)
  sfftKernel = numpy.fft.ifftshift(fftKernel)
  
  
  m = numpy.sqrt(convol * numpy.conj(convol))
  m2 = 255 / (log(1+numpy.max(m))) * numpy.log(m+1)
  
  
  
  Image.fromarray(numpy.uint8(convol)).show()

def butterfly2():
  from PIL import Image, ImageFilter
  
  im = Image.open('c:/documents/workspace/EBSDTools/dev/hough1.bmp')
  print im.mode
  f = ImageFilter.Kernel(size=(3,3), kernel=[0,-2,0,1,2,1,0,-2,0])
  im1 = im.filter(f)
  im1.show()
  
  
if __name__ == '__main__':
  butterfly2()