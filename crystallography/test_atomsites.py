#!/usr/bin/env python
"""
================================================================================
:mod:`test_atomsites` -- Unit tests for the module :mod:`atomsites.`
================================================================================

.. module:: test_atomsites
   :synopsis: Unit tests for the module :mod:`atomsites.`
.. moduleauthor:: Philippe Pinard <philippe.pinard@mail.mcgill.ca>

.. inheritance-diagram:: test_atomsites

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
import ebsdtools.crystallography.atomsites as atomsites
import ebsdtools.crystallography.atomsite as atomsite

# Globals and constants variables.

class TestAtomSites(unittest.TestCase):

  def setUp(self):
    unittest.TestCase.setUp(self)

    self.atoms = atomsites.AtomSites()

    self.atom1 = atomsite.AtomSite(13, 0, 0, 0)
    self.atom2 = atomsite.AtomSite(13, 0, 0.5, 0.5)
    self.atom3 = atomsite.AtomSite(13, 0.5, 0, 0.5)
    self.atom4 = atomsite.AtomSite(13, 0, 0.5, 0.5)

  def tearDown(self):
    unittest.TestCase.tearDown(self)

  def testSkeleton(self):
    #self.fail("Test if the TestCase is working.")
    self.assert_(True)

  def test__setitem__(self):
    self.atoms.append(self.atom1)

    func = lambda index, atom: self.atoms.__setitem__(index, atom)
    self.assertRaises(atomsites.AtomSitePositionError
                      , func
                      , 0, self.atom1)

  def testappend(self):
    self.atoms.append(self.atom1)
    self.assertEqual(len(self.atoms), 1)

    func = lambda atom: self.atoms.append(atom)
    self.assertRaises(atomsites.AtomSitePositionError
                      , func
                      , self.atom1)

  def testextend(self):
    self.atoms.extend([self.atom1, self.atom2])
    self.assertEqual(len(self.atoms), 2)

    func = lambda atom: self.atoms.extend(atom)
    self.assertRaises(atomsites.AtomSitePositionError
                      , func
                      , self.atom2)

  def testinsert(self):
    self.atoms.extend([self.atom1, self.atom2])

    self.atoms.insert(1, self.atom3)
    self.assertEqual(len(self.atoms), 3)

    func = lambda index, atom: self.atoms.insert(index, atom)
    self.assertRaises(atomsites.AtomSitePositionError
                      , func
                      , 1, self.atom2)

if __name__ == '__main__': #pragma: no cover
  logging.getLogger().setLevel(logging.DEBUG)
  unittest.main()
