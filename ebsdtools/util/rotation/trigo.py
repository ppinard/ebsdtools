#!/usr/bin/env python
"""
================================================================================
:mod:`trigo` -- Trigonometry functions.
================================================================================

.. module:: trigo
   :synopsis: Trigonometry functions

"""

# Script information for the file.
__author__ = "Philippe T. Pinard"
__email__ = "philippe.pinard@gmail.com"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2010 Philippe T. Pinard"
__license__ = "GPL v3"

# Standard library modules.
from math import pi as pi
from math import acos as acos_org

# Third party modules.

# Local modules.

def acos(angle):
    """
    Prevent rounding error when using ``acos(angle)``.
    
      * If *angle* is greater or equal to 1.0, ``acos(angle)=0``
      * If *angle* is less or equal to 1.0, ``acos(angle)=pi``
    
    :rtype: :class:`float`
    """
    if angle >= 1.0:
        return 0.0
    elif angle <= -1.0:
        return pi
    else:
        return acos_org(angle)

def smallangle(angle):
    """
    Return an angle between 0 and :math:`\\frac{\\pi}{2}`
    
    :rtype: :class:`float`
    
    """
    if angle >= 0 and angle <= pi:
        if angle > pi / 2.0:
            angle = pi - angle

    return angle

if __name__ == '__main__': #pragma: no cover
    import DrixUtilities.Runner as Runner
    Runner.Runner().run(runFunction=None)

