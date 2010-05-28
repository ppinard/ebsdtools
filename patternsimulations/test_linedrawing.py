#!/usr/bin/env python
"""
================================================================================
:mod:`test_linedrawing` -- Unit tests for the module :mod:`linedrawing`.
================================================================================

.. module:: test_linedrawing
   :synopsis: Unit tests for the module :mod:`linedrawing`.
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
import unittest
import logging

# Third party modules.

# Local modules.
import ebsdtools.patternsimulations.linedrawing as linedrawing

# Globals and constants variables.

class TestLinedrawing(unittest.TestCase):

  def setUp(self):
    unittest.TestCase.setUp(self)

  def tearDown(self):
    unittest.TestCase.tearDown(self)

  def testSkeleton(self):
    #self.fail("Test if the TestCase is working.")
    self.assert_(True)

  def testslopeintercept_to_points(self):
    p0, p1 = linedrawing.slopeintercept_to_points(m= -1.0, k=0
                                                  , width=5, height=5
                                                  , origin_x=0.5, origin_y=0.5)
    print p0, p1
#    self.assertEqual(p0, (-1, 6))
#    self.assertEqual(p1, (6, -1))

    p0, p1 = linedrawing.slopeintercept_to_points(m= -1.0, k=1
                                                  , width=5, height=5
                                                  , origin_x=0.5, origin_y=0.5)
    print p0, p1
#    self.assertEqual(p0, (-1, 1))
#    self.assertEqual(p1, (6, -6))


if __name__ == '__main__': #pragma: no cover
  logging.getLogger().setLevel(logging.DEBUG)
  unittest.main()
