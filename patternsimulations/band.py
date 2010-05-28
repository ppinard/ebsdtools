#!/usr/bin/env python
"""
================================================================================
:mod:`band` -- Store information of a Kikuchi band.
================================================================================

.. module:: band
   :synopsis: Store information of a Kikuchi band.
.. moduleauthor:: Philippe Pinard <philippe.pinard@mail.mcgill.ca>

.. inheritance-diagram:: band

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

# Third party modules.

# Local modules.
import ebsdtools.crystallography.reflectors as reflectors

# Globals and constants variables.

class Band(reflectors.Reflector):
  SLOPE = 'm'
  INTERCEPT = 'k'
  THICKNESS = 'thickness'
  HALFWIDTHS = 'halfwidths'
  EDGEINTERCEPTS = 'edgeintercepts'

  def __init__(self, reflector):
    """
    Store information of a Kikuchi band.

    :arg reflector: reflector of the band
    :type reflector: :class:`reflectors.Reflector`

    **Attributes**

      * plane (indices): :attr:`plane`
      * plane spacing: :attr:`planespacing`
      * intensity: :attr:`intensity`
      * normalized intensity: :attr:`normalizedintensity`
      * slope: :attr:`m`
      * intercept: :attr:`k`
      * thickness: :attr:`thickness`
      * half widths: :attr:`halfwidths` (:class:`tuple`)
      * intercept of the band edges: :attr:`edgeintercepts` (:class:`tuple`)

    """
    dict.__init__(self, reflector)

if __name__ == '__main__': #pragma: no cover
  import DrixUtilities.Runner as Runner
  Runner.Runner().run(runFunction=None)

