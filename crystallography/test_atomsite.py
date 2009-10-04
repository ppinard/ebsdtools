#!/usr/bin/env python
"""
================================================================================
:mod:`test_atomsite` -- Unit tests for the module :mod:`atomsite.`
================================================================================

.. module:: test_atomsite
   :synopsis: Unit tests for the module :mod:`atomsite.`
.. moduleauthor:: Philippe Pinard <philippe.pinard@mail.mcgill.ca>

.. inheritance-diagram:: test_atomsite

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
import ebsdtools.crystallography.atomsite as atomsite

# Globals and constants variables.

class TestAtomSite(unittest.TestCase):

  def setUp(self):
    unittest.TestCase.setUp(self)

    self.atom1 = atomsite.AtomSite(13, 0, 0.5, 0.5)
    self.atom2 = atomsite.AtomSite(14, (0.3, 0.2, 0.1))

  def tearDown(self):
    unittest.TestCase.tearDown(self)

  def testSkeleton(self):
    #self.fail("Test if the TestCase is working.")
    self.assert_(True)

  def testconstructor(self):
    self.assertEqual(self.atom1.atomicnumber, 13)
    self.assertEqual(self.atom2.atomicnumber, 14)

    self.assertEqual(self.atom1.position, [0, 0.5, 0.5])
    self.assertEqual(self.atom2.position, [0.3, 0.2, 0.1])

  def test__repr__(self):
    self.assertEqual(str(self.atom1), "Al->[0.0, 0.5, 0.5]")
    self.assertEqual(str(self.atom2), "Si->[0.29999999999999999, 0.20000000000000001, 0.10000000000000001]")

  def test__eq__(self):
    atom = atomsite.AtomSite(13, 0, 0.5, 0.5)
    self.assertTrue(self.atom1 == atom)

  def test__ne__(self):
    self.assertTrue(self.atom1 != self.atom2)

if __name__ == '__main__': #pragma: no cover
  logging.getLogger().setLevel(logging.DEBUG)
  unittest.main()
