#!/usr/bin/env jython
""" """

# Script information for the file.
__author__ = "Philippe Pinard (philippe.pinard@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2009 Philippe Pinard"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = ""
__svnDate__ = ""
__svnId__ = ""

# Standard library modules.
import sys

# Third party modules.

# Local modules.

# Globals and constants variables.

# Interfaces.
import rmlimage.module.ebsd.python.interfaces

class HelloWorld(rmlimage.module.ebsd.python.interfaces.HelloWorld):
  def __init__(self):
    pass

  def return_helloworld(self):
    return "Hello World!"

  def return_sys_path(self):
    return sys.path

if __name__ == '__main__':
  helloworld = HelloWorld()
  print helloworld.return_helloworld()
  print helloworld.return_sys_path()
