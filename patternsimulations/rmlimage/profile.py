#!/usr/bin/env jython
"""
================================================================================
:mod:`module` -- ??
================================================================================

.. currentmodule:: module
.. moduleauthor:: Philippe Pinard <philippe.pinard@mail.mcgill.ca>

.. inheritance-diagram:: module

"""

# Script information for the file.
__author__ = "Philippe Pinard <philippe.pinard@mail.mcgill.ca>"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2009 Philippe Pinard"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = ""
__svnDate__ = ""
__svnId__ = ""

# Standard library modules.
import os.path

# Third party modules.
import rmlimage.module.real.io as io
import rmlimage.module.real.core as real
import rmlimage.io

# Local modules.
import DrixUtilities.Files as Files

import ebsdtools.patternsimulations.rmlimage.pattern as pattern
#import ebsdtools.patternsimulations.pattern as pattern

import ebsdtools.crystallography.reflectors as reflectors
import ebsdtools.crystallography.atomsites as atomsites
import ebsdtools.crystallography.unitcell as unitcell
import ebsdtools.crystallography.scatteringfactors as scatteringfactors

# Globals and constants variables.

def create_pattern():
  # Init pattern
  patt = pattern.PatternFullSolidBand()
#  patt = pattern.Pattern()

  # Reflectors
  cell = unitcell.create_cubic_unitcell(3)
  atoms = atomsites.create_fcc_atomsites(14)

  relativepath = os.path.join('..', '..', 'testdata', 'goodconfiguration.cfg')
  configurationfilepath = Files.getCurrentModulePath(__file__, relativepath)
  scatter = scatteringfactors.XrayScatteringFactors(configurationfilepath)

  refls = reflectors.Reflectors(cell, atoms, scatter)

  # Parameters
  patt.set_reflectors(refls)

  patt.set_numberreflectors(len(refls))
  patt.set_energy(30e3)
  patt.set_detectordistance(0.3)
  patt.set_patterncenter(0, 0)

  # Draw pattern
  image = patt.draw()

  # Save image
  bytemap = real.Contrast.expansion(image)
  bytemap.setFile('/tmp/pattern.bmp')
  rmlimage.io.IO.save(bytemap)

def profiler():
  for i in range(10):
    print i
    create_pattern()

if __name__ == '__main__':
  profiler()
