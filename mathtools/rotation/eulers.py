#!/usr/bin/env python
"""
================================================================================
:mod:`eulers` -- Euler angles.
================================================================================

.. module:: eulers
   :synopsis: Euler angles.

.. inheritance-diagram:: mathtools.rotation.eulers

"""

# Script information for the file.
__author__ = "Philippe T. Pinard"
__email__ = "philippe.pinard@gmail.com"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2010 Philippe T. Pinard"
__license__ = "GPL v3"

# Standard library modules.
from math import pi

# Third party modules.

# Local modules.

# Globals and constants variables.

def eulers_deg_to_eulers_rad(*data):
    """
    Return a :class:`Eulers <mathtools.rotation.eulers.Eulers>`
    from a set of 3 Euler angles (in degrees)
    
    **Parameters:**
        =============   =========================================
        ``len(data)``   Description
        =============   =========================================
        0               Zero eulers (0,0,0)
        1               List of 3 angles (theta1, theta2, theta3)
        3               3 angles theta1, theta2, theta3
        =============   =========================================
    
    :rtype: :class:`eulers.Eulers`
    
    """
    if len(data) == 0:
        theta1 = 0
        theta2 = 0
        theta3 = 0
    elif len(data) == 1:
        theta1 = data[0][0]
        theta2 = data[0][1]
        theta3 = data[0][2]
    elif len(data) == 3:
        theta1 = data[0]
        theta2 = data[1]
        theta3 = data[2]

    theta1 = theta1 / 180.0 * pi
    theta2 = theta2 / 180.0 * pi
    theta3 = theta3 / 180.0 * pi

    return Eulers(theta1, theta2, theta3)

class Eulers(object):
    def __init__(self, *data):
        """
        Define a set of 3 Euler angles (in radians)
        as defined by the Bunge convention.
        
        **Parameters**
          =============   =========================================
          ``len(data)``   Description
          =============   =========================================
          0               Zero eulers (0,0,0)
          1               List of 3 angles (theta1, theta2, theta3)
          3               3 angles theta1, theta2, theta3
          =============   =========================================
        
        """
        if len(data) == 0:
            self._theta1 = 0.0
            self._theta2 = 0.0
            self._theta3 = 0.0
        elif len(data) == 1:
            self._theta1 = float(data[0][0])
            self._theta2 = float(data[0][1])
            self._theta3 = float(data[0][2])
        elif len(data) == 3:
            self._theta1 = float(data[0])
            self._theta2 = float(data[1])
            self._theta3 = float(data[2])

    def __getitem__(self, key):
        """
        Return the value of the Euler angles in radians as they are called.
        
        :arg name: Either theta1, theta2, theta3 or phi1, phi, phi2 or
                    alpha, beta, gamma
        :type name: :class:`str`
        
        :rtype: :class:`float`
        
        **Examples** ::
        
          e = eulers(0.5, 1, 0.2)
          print eulers['theta1'] #Return 0.5
          print eulers['beta'] #Return 1.0
          print eulers['phi2'] #Return 0.2
        
        """
        if isinstance(key, str):
            key = key.lower()
            if key == 'theta1' or key == 'phi1' or key == 'alpha':
                return self._theta1
            elif key == 'theta2' or key == 'phi' or key == 'beta':
                return self._theta2
            elif key == 'theta3' or key == 'phi2' or key == 'gamma':
                return self._theta3
        elif isinstance(key, int):
            if key == 1:
                return self._theta1
            elif key == 2:
                return self._theta2
            elif key == 3:
                return self._theta3

    def __setitem__(self, key, value):
        """
        Modify an Euler angle.
        
        :arg name: Either theta1, theta2, theta3 or phi1, phi, phi2 or
                    alpha, beta, gamma
        :type name: :class:`str`
        
        :arg value: angle in radians
        :type value: :class:`float`
        
        **Examples** ::
        
          e = eulers(0.5, 1, 0.2)
          e['theta2'] = 2.1
          e == eulers(0.5, 2.1, 0.2) #Equivalent
        
        """
        if isinstance(key, str):
            key = key.lower()
            if key == 'theta1' or key == 'phi1' or key == 'alpha':
                self._theta1 = float(value)
            elif key == 'theta2' or key == 'phi' or key == 'beta':
                self._theta2 = float(value)
            elif key == 'theta3' or key == 'phi2' or key == 'gamma':
                self._theta3 = float(value)
        elif isinstance(key, int):
            if key == 1:
                self._theta1 = float(value)
            elif key == 2:
                self._theta2 = float(value)
            elif key == 3:
                self._theta3 = float(value)

    def __str__(self):
        """
        Return a string representing the Euler angles.
        
        :rtype: :class:`str`
        """
        return "(%f, %f, %f)" % (self._theta1, self._theta2, self._theta3)

    def __eq__(self, other):
        equality = True

        equality = equality and self._theta1 == other._theta1
        equality = equality and self._theta2 == other._theta2
        equality = equality and self._theta3 == other._theta3

        return equality

    def __ne__(self, other):
        return not self == other

    def to_deg(self):
        """
        Return a tuple of the Euler angles in degrees.
        
        :rtype: :class:`tuple`
        """
        theta0 = self._theta1 * 180.0 / pi
        theta1 = self._theta2 * 180.0 / pi
        theta2 = self._theta3 * 180.0 / pi

        return (theta0, theta1, theta2)

    def to_rad(self):
        """
        Return a tuple of the Euler angles in radians.
        
        :rtype: :class:`tuple`
        """
        return (self._theta1, self._theta2, self._theta3)

    def positive(self):
        """
        .. seealso:: :func:`eulers.positive`
        """
        eulers = positive(self)
        Eulers.__init__(self, eulers._theta1, eulers._theta2, eulers._theta3)

    def negative(self):
        """
        .. seealso:: :func:`eulers.negative`
        """
        eulers = negative(self)
        Eulers.__init__(self, eulers._theta1, eulers._theta2, eulers._theta3)

def positive(eulers):
    """
    Convert any :class:`eulers.Eulers` to a :class:`eulers.Eulers`
    with positive Euler angles.
    
    :arg eulers: a set of Euler angles
    :type eulers: :class:`eulers.Eulers`
    
    Convert eulers from
      * :math:`-pi < \\text{theta0} < pi`
      * :math:`0 < \\text{theta1} < pi`
      * :math:`-pi < \\text{theta2} < pi`
    to
      * :math:`0 < \\text{theta0} < 2pi`
      * :math:`0 < \\text{theta1} < pi`
      * :math:`0 < \\text{theta2} < 2pi`
    
    :rtype: :class:`eulers.Eulers`
    
    """
    theta1 = eulers._theta1; theta2 = eulers._theta2; theta3 = eulers._theta3

    while theta1 < 0:
        theta1 += 2 * pi
    while theta3 < 0:
        theta3 += 2 * pi

    return Eulers(theta1, theta2, theta3)

def negative(eulers):
    """
    Convert any :class:`eulers.Eulers` to a :class:`eulers.Eulers`
    with negative Euler angles.
    
    :arg eulers: a set of Euler angles
    :type eulers: :class:`eulers.Eulers`
    
    Convert eulers from
      * :math:`0 < \\text{theta0} < 2pi`
      * :math:`0 < \\text{theta1} < pi`
      * :math:`0 < \\text{theta2} < 2pi`
    to
      * :math:`-pi < \\text{theta0} < pi`
      * :math:`0 < \\text{theta1} < pi`
      * :math:`-pi < \\text{theta2} < pi`
    
    :rtype: :class:`eulers.Eulers`
    
    """
    theta1 = eulers._theta1; theta2 = eulers._theta2; theta3 = eulers._theta3

    while theta1 > pi:
        theta1 -= 2 * pi
    while theta3 > pi:
        theta3 -= 2 * pi

    return Eulers(theta1, theta2, theta3)

if __name__ == '__main__': #pragma: no cover
    import DrixUtilities.Runner as Runner
    Runner.Runner().run(runFunction=None)
