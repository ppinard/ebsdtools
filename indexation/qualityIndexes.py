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
import os
import java.io

# Third party modules.
import rmlimage.io.IO as IO
import rmlimage.kernel as kernel
import rmlimage.plugin.ebsd.Analysis as Analysis

# Local modules.

class QualityIndexes(object):
  def __init__(self):
    pass
  
  def calculate(self, *args):
    raise NotImplementedError
  
class average(QualityIndexes):
  def __init__(self):
    QualityIndexes.__init__(self)
  
  def calculate(self, pattern):
    return Analysis.average(pattern)

class standardDeviation(QualityIndexes):
  def __init__(self):
    QualityIndexes.__init__(self)
  
  def calculate(self, pattern):
    return Analysis.standardDeviation(pattern)

class entropy(QualityIndexes):
  def __init__(self):
    QualityIndexes.__init__(self)
  
  def calculate(self, pattern):
    return Analysis.entropy(pattern)

if __name__ == '__main__':
  import pattern
  
  patt1 = pattern.Pattern(filepath='testData/pattern1.bmp')
  
  print average().calculate(patt1)
  print standardDeviation().calculate(patt1)
  print entropy().calculate(patt1)