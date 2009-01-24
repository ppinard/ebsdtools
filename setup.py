#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Philippe Pinard (philippe.pinard@gmail.com)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2009 Philippe Pinard"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = ""
__svnDate__ = ""
__svnId__ = ""

# Standard library modules.
from distutils.core import setup
import sys
import os

# Third party modules.

# Local modules.
import EBSDTools
import RandomUtilities

if sys.argv[1] == 'sdist':
  package_dir = {'EBSDTools': ''}
  packages = ['EBSDTools', 'EBSDTools.crystallography', 'EBSDTools.mathTools']
  package_data = {'EBSDTools': [r'data\*.csv',]}
elif sys.argv[1] == 'bdist_wininst':
  package_dir = {'EBSDTools': EBSDTools.__path__[0]
                 , 'RandomUtilities': RandomUtilities.__path__[0]}
  packages = ['EBSDTools', 'EBSDTools.crystallography', 'EBSDTools.mathTools'
              , 'RandomUtilities', 'RandomUtilities.sort']
  package_data = {'EBSDTools': [r'data\*.csv',]}
  
setup(name='EBSDTools'
      , version=EBSDTools.__version__
      , description='Tools for EBSD characterization'
      , author=EBSDTools.__author__
      , author_email=EBSDTools.__author_info__['Philippe Pinard']["email"]
      , url='http://philippepinard.web.aplus.net/EBSDTools/'
      
      , package_dir = package_dir 
      , packages = packages
      , package_data = package_data
      )
