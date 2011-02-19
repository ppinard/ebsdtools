#!/usr/bin/env python
"""
================================================================================
:mod:`crystalObject` -- Crystal 3D representation using visual library
================================================================================

.. module:: crystalObject
   :synopsis: Crystal 3D representation using visual library

.. inheritance-diagram:: ebsdtools.hkl.tango.crystalObject

"""

# Script information for the file.
__author__ = "Philippe T. Pinard"
__email__ = "philippe.pinard@gmail.com"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2010 Philippe T. Pinard"
__license__ = "GPL v3"

# Standard library modules.
import math

# Third party modules.
import visual

# Local modules.

class crystal:
    def __init__(self):
        self.canvas = visual.display(title='Crystal Viewer'
                                     , width=500
                                     , height=500
                                     , background=(0, 0, 0)
                                     , fov=math.pi / 10
                                     , scale=(0.5, 0.5, 0.5)
                                     , userspin=0
                                     , exit=0)

        self.lastRotation = (0, 0, 0)

    def rotateReset(self, object):
        object.rotate(angle= -self.lastRotation[2] * math.pi / 180
                      , axis=(1, 0, 0)
                      , origin=(0, 0, 0))

        object.rotate(angle= -self.lastRotation[1] * math.pi / 180
                      , axis=(0, 0, 1)
                      , origin=(0, 0, 0))

        object.rotate(angle= -self.lastRotation[0] * math.pi / 180
                      , axis=(1, 0, 0)
                      , origin=(0, 0, 0))

    def rotate(self, object, eulers=(0, 0, 0)):
        self.rotateReset(object)

        object.rotate(angle=eulers[0] * math.pi / 180
                      , axis=(1, 0, 0)
                      , origin=(0, 0, 0))

        object.rotate(angle=eulers[1] * math.pi / 180
                      , axis=(0, 0, 1)
                      , origin=(0, 0, 0))

        object.rotate(angle=eulers[2] * math.pi / 180
                      , axis=(1, 0, 0)
                      , origin=(0, 0, 0))

        self.lastRotation = eulers

    def cubic(self, latticeparameters=(1, 1, 1)):
        cube = visual.frame()

        visual.box(frame=cube
                   , pos=(0, 0, 0)
                   , size=latticeparameters
                   , color=(1, 0.7, 0.2))

        visual.arrow(frame=cube
                     , pos=(latticeparameters[0] / 2, 0, 0)
                     , axis=(1, 0, 0)
                     , shaftwidth=0.1
                     , color=(1, 0, 0))

        visual.arrow(frame=cube
                     , pos=(0, latticeparameters[0] / 2, 0)
                     , axis=(0, 1, 0)
                     , shaftwidth=0.1
                     , color=(0, 1, 0))

        visual.arrow(frame=cube
                     , pos=(0, 0, latticeparameters[0] / 2)
                     , axis=(0, 0, 1)
                     , shaftwidth=0.1
                     , color=(0, 0, 1))

        return cube

    def hexagonal(self, CAratio=1.6):
        hexagonal = visual.frame()

        base1 = visual.box(frame=hexagonal
                           , pos=(0, -CAratio / 2.0, 0)
                           , size=(math.sqrt(3), 0.01, 1)
                           , color=(1, 0.7, 0.2))
        base1 = base1.__copy__()
        base1.rotate(angle=math.pi * 60 / 180, axis=(0, 1, 0), origin=(0, 0, 0))
        base1 = base1.__copy__()
        base1.rotate(angle=math.pi * 60 / 180, axis=(0, 1, 0), origin=(0, 0, 0))

        base2 = visual.box(frame=hexagonal
                           , pos=(0, CAratio / 2.0, 0)
                           , size=(math.sqrt(3), 0.01, 1)
                           , color=(1, 0.7, 0.2))
        base2 = base2.__copy__()
        base2.rotate(angle=math.pi * 60 / 180, axis=(0, 1, 0), origin=(0, 0, 0))
        base2 = base2.__copy__()
        base2.rotate(angle=math.pi * 60 / 180, axis=(0, 1, 0), origin=(0, 0, 0))

        face = visual.box(frame=hexagonal
                          , pos=(math.sqrt(3) / 2.0, 0, 0)
                          , size=(0.01, CAratio, 1)
                          , color=(1, 0.7, 0.2))
        for _i in range(6):
            face = face.__copy__()
            face.rotate(angle=math.pi * 60 / 180, axis=(0, 1, 0), origin=(0, 0, 0))

        visual.arrow(frame=hexagonal
                     , pos=(0, CAratio / 2, 0)
                     , axis=(0, 0.5, 0)
                     , shaftwidth=0.1
                     , color=(1, 0, 0))

        visual.arrow(frame=hexagonal
                     , pos=(CAratio / 2, 0, 0)
                     , axis=(0.5, 0, 0)
                     , shaftwidth=0.1
                     , color=(0, 1, 0))

        return hexagonal

if __name__ == '__main__':
    c = crystal()

    #  cube = c.cubic()
    #  c.rotate(cube, (math.pi/2,math.pi/2,math.pi/2))

    hexagonal = c.hexagonal()
    c.rotate(hexagonal, (math.pi / 2, math.pi / 2, math.pi / 2))
