#!/usr/bin/env jython
""" """

# Script information for the file.
__author__ = "Philippe Pinard (philippe.pinard@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2009"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = ""
__svnDate__ = ""
__svnId__ = ""

# Standard library modules.
import os
import sys

# Third party modules.
import rmlimage.core.MathMorph as MathMorph
import rmlimage.io.IO as IO

# Local modules.
import RandomUtilities.csvTools.mycsv as mycsv

import EBSDTools.indexation.pattern as pattern
import EBSDTools.indexation.masks as masks
import EBSDTools.indexation.hough as hough
import EBSDTools.indexation.qualityIndexes as qualityIndexes

import HKLChannel5Tools.Tango.ctfFile as ctfFile

from DeformationSamplePrep.qualityIndexes.constants import *

# Globals and constants variables.

print sys.argv

job_id = sys.argv[1]

log_file_dir = sys.argv[2]
patterns_location = sys.argv[3]
project_ctf = sys.argv[4]
results_folder = sys.argv[5]
index = int(sys.argv[6])

print patterns_location
print project_ctf
print results_folder

ctf = ctfFile.ctf(project_ctf)

imageLabel = ctf.getPixelImageLabel(index=index)
imagePath = os.path.join(patterns_location, '%s.jpg' % imageLabel)
patt = pattern.PatternMap(filepath=imagePath)

#Save original pattern
patt.setFile(os.path.join(results_folder, 'pattern_%i.bmp' % index))
IO.save(patt)

maskMap = masks.MaskDisc(patt.width, patt.height, (patt.width/2, patt.height/2), patt.height/2-10)
maskMap.setFile(os.path.join(results_folder, 'mask_%i.bmp' % index))
IO.save(maskMap)

MathMorph.median(patt, 2)

patt.applyMask(maskMap)

#Save original pattern
patt.setFile(os.path.join(results_folder, 'patternmask_%i.bmp' % index))
IO.save(patt)

houghMap = hough.HoughMap(patt)

houghMap.findPeaks(hough.FINDPEAKS_BUTTERFLY)
peaks = houghMap.getPeaks()

#Hough map cropped
houghMap_crop = houghMap._houghMap_crop.duplicate()
houghMap_crop.setFile(os.path.join(results_folder, 'houghmapcrop_%i.bmp' % (index)))
IO.save(houghMap_crop)

#Hough map convoluted
houghMap_convol = houghMap._houghMap_crop.duplicate()
houghMap_convol.setFile(os.path.join(results_folder, 'houghmapconvol_%i.bmp' % (index)))
IO.save(houghMap_convol)

#BinMap
identMap = peaks._identMap.duplicate()
identMap.setFile(os.path.join(results_folder, 'identMap_%i.bmp' % (index)))
IO.save(identMap)

for numberPeak in range(3, 15):
  overlayMap = peaks.overlay(patt.getOriginalPattern(), numberPeak, (255,0,0))

  overlayMap.setFile(os.path.join(results_folder, 'overlay_%i_%i.bmp' % (index, numberPeak)))
  IO.save(overlayMap)

