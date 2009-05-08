#!/usr/bin/env jython
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
from math import sqrt
import java.io

# Third party modules.
import rmlimage.io.IO as IO
import rmlimage.complex

# Local modules.
import EBSDTools.indexation.pattern as pattern

patt1 = pattern.PatternMap(filepath='../indexation/testData/pattern1.bmp')
patt1Crop = rmlimage.complex.Edit.cropToNearestPowerOfTwo(patt1, rmlimage.complex.Edit.Position.CENTER)
complexMap = rmlimage.complex.Conversion.toComplexMap(patt1Crop) #Convert to complex map
rmlimage.complex.Edit.flip(complexMap) #Flip map

byteMap = rmlimage.complex.Conversion.toByteMap(complexMap)
byteMap.setFile('before.bmp')
IO.save(byteMap)

rmlimage.complex.FFT().forward(complexMap)
rmlimage.complex.Edit.flip(complexMap) #Flip map

print complexMap.size, complexMap.height

sum1 = 0
sum2 = 0
sum3 = 0
for j in range(complexMap.height):
  for i in range(complexMap.width):
    index = i + j*complexMap.width
    
    u = i - complexMap.width/2
    v = j - complexMap.height/2
    
    F = complex(complexMap.rPixArray[index], complexMap.iPixArray[index])
    S = sqrt((F*F.conjugate()).real)
    
    sum1 += S * (u**2 + v**2)
    sum2 += S
    sum3 += (u**2 + v**2)

I = sum1 / sum2
Imax = sum3

Q = 1 - I/Imax

print sum1, sum2, Imax, I, Q

byteMap = rmlimage.complex.Conversion.toByteMap(complexMap)
byteMap.setFile('after.bmp')
IO.save(byteMap)

