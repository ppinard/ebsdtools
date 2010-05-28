#!/usr/bin/env python
"""
================================================================================
:mod:`rotation` -- Combine rotation of the crystal, specimen, microscope to
                   create a pattern.
================================================================================

.. module:: rotation
   :synopsis: Combine rotation of the crystal, specimen, microscope to
              create a pattern.
.. moduleauthor:: Philippe Pinard <philippe.pinard@mail.mcgill.ca>

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
from math import pi

# Third party modules.

# Local modules.
import mathtools.rotation.quaternions as quaternions

# Globals and constants variables.

def hkl_equivalent_rotation(crystal
                            , tilt=70
                            , specimen=quaternions.Quaternion(1)):
  """
  Return a list of :class:`quaternions.Quaternion` representing the rotation
  of a pattern.
  The overall rotation is equivalent to the rotation defined in HKL Flamenco.

  :arg crystal: rotation of the crystal (reported rotation)
  :type crystal: :class:`quaternions.Quaternion`

  :arg tilt: tilt angle in degrees
  :type tilt: :class:`float`

  :arg specimen: rotation of the specimen (in respect to the microscope)
    This should not take into account the tilt.
  :type specimen: :class:`quaternions.Quaternion`

  :rtype: :class:`list`

  """
  tilt = quaternions.axisangle_to_quaternion(-tilt / 180.0 * pi, (1, 0, 0))
  detector = quaternions.axisangle_to_quaternion(pi / 2.0, (1, 0, 0)) * \
              quaternions.axisangle_to_quaternion(pi, (0, 0, 1))
  detector_withtilt = tilt * quaternions.conjugate(detector) * \
                        quaternions.conjugate(tilt)

  rotations = [specimen, crystal, tilt, detector_withtilt]

  return rotations

def pattern_rotation(crystal
                     , tilt=70
                     , specimen=quaternions.Quaternion(1)):
  """
  Return a list of :class:`quaternions.Quaternion` representing the rotation
  of a pattern.
  It combines the crystal orientation, the specimen rotation and the tilt.

  :arg crystal: rotation of the crystal (reported rotation)
  :type crystal: :class:`quaternions.Quaternion`

  :arg tilt: tilt angle in degrees
  :type tilt: :class:`float`

  :arg specimen: rotation of the specimen (in respect to the microscope)
    This should not take into account the tilt.
  :type specimen: :class:`quaternions.Quaternion`

  :rtype: :class:`list`

  """
  tilt = quaternions.axisangle_to_quaternion(-tilt / 180.0 * pi, (1, 0, 0))
  detector = quaternions.Quaternion(1)

  rotations = [specimen, crystal, tilt, detector]

  return rotations

if __name__ == '__main__': #pragma: no cover
  import DrixUtilities.Runner as Runner
  Runner.Runner().run(runFunction=None)

