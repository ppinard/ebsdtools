#!/usr/bin/env python
"""
================================================================================
:mod:`peak` -- Hough peak
================================================================================

.. module:: peak
   :synopsis: Hough peak
.. moduleauthor:: Philippe Pinard <philippe.pinard@mail.mcgill.ca>

.. inheritance-diagram:: peak

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

# Globals and constants variables.
RHO = 'rho'
THETA = 'theta'
OBJECT_ID = 'objectid'
MAXIMUM_INTENSITY = 'maximum_intensity'

class Peak(dict):
  def __init__(self
               , rho
               , theta):
    """
    Store information about a Hough peak.

    :arg rho: rho value in Hough space.
    :type rho: :class:`float`

    :arg theta: theta value in Hough space (in radians).
    :type theta: :class:`float`

    """
    dict.__init__(self)

    self.setdefault(RHO, rho)
    self.setdefault(THETA, theta)

  def __getattr__(self, attr):
    """
    Possible attributes:

      * rho: :attr:`rho`
      * theta: :attr:`theta`
      * object id: :attr:`objectid`
      * maximum intensity: :attr:`maximum_intensity`

    """
    return self.get(attr)

  def __repr__(self):
    return '(%f, %f)' % (self.rho, self.theta)

  def __hash__(self):
    """
    Hash only with the rho and theta value since they are unique for any given
    peaks.

    """
    return hash((self.rho, self.theta))

  def __eq__(self, other):
    """
    Two peaks are equal if they have the same rho and theta.

    """
    equality = True

    equality = equality and hash(self) == hash(other)

    return equality

  def __ne__(self, other):
    return not self == other


if __name__ == '__main__': #pragma: no cover
  import DrixUtilities.Runner as Runner
  Runner.Runner().run(runFunction=None)

