#!/usr/bin/env jython
"""
Module to be compile using jythonc for RML-Image
"""

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
import java.lang

# Third party modules.

# Local modules.
import EBSDTools.indexation.masks as masks

class jMasks(java.lang.Object):
  def discMask(self, width, height, centroidX, centroidY, radius):
    "@sig public rmlimage.kernel.BinMap discMask(int width, int height, int centroidX, int centroidY, int radius)"
    """
    Create a binMap where a white disc is drawn according to the parameter
    """
    return masks.createMaskDisc(width=width
                                , height=height
                                , centroid=(centroidX, centroidY)
                                , radius=radius)
    