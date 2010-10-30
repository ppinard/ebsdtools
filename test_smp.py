"""
================================================================================
:mod:`test_smp` -- Unit tests for the module MODULE.
================================================================================

.. currentmodule:: test_smp
.. moduleauthor:: Philippe Pinard <philippe.pinard@mail.mcgill.ca>

"""

# Script information for the file.
__author__ = "Philippe Pinard (philippe.pinard@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2010 Philippe Pinard"
__license__ = ""

# Standard library modules.
import unittest
import logging

# Third party modules.


# Local modules.
import smp

# Globals and constants variables.

class Test(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.reader = smp.reader(open('test.smp', 'rb'))

    def tearDown(self):
        unittest.TestCase.tearDown(self)

        self.reader.close()

    def testskeleton(self):
        self.assertTrue(True)
        self.assertEqual(256, self.reader.width)
        self.assertEqual(256, self.reader.height)
        self.assertEqual(256 * 256, self.reader.size)
        self.assertEqual(1000, self.reader.start_index)
        self.assertEqual(1003, self.reader.end_index)
        self.assertEqual(4, len(self.reader))

    def testcall(self):
        im = self.reader(1000)
        self.assertEqual('L', im.mode)
        self.assertEqual((256, 256), im.size)

    def testread(self):
        im = self.reader.read(1000)
        self.assertEqual('L', im.mode)
        self.assertEqual((256, 256), im.size)

        self.assertRaises(IndexError, self.reader.read, 999)
        self.assertRaises(IndexError, self.reader.read, 1004)

    def testnext(self):
        for im in self.reader:
            self.assertEqual('L', im.mode)
            self.assertEqual((256, 256), im.size)

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
