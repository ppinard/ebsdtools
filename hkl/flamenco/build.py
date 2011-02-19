#!/usr/bin/env python
"""
================================================================================
:mod:`build` -- Distribution builder
================================================================================

.. module:: build
   :synopsis: Distribution builder

"""

# Script information for the file.
__author__ = "Philippe T. Pinard"
__email__ = "philippe.pinard@gmail.com"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2010 Philippe T. Pinard"
__license__ = "GPL v3"

# Standard library modules.
import os

# Third party modules.

# Local modules.
from setuputilities.builder.project import Project
from setuputilities.builder.base import BaseBuild
from setuputilities.builder.setup import SetupBuild
from setuputilities.builder.doc import DocBuild
from setuputilities.builder.test import TestBuild
from setuputilities.builder.cover import CoverageBuild
from setuputilities.builder.py2exe import Py2exeBuild
from setuputilities.builder.nsis import NSISBuild
from setuputilities.util import find_package_path, find_packages

from tkintertools.build import project as tkintertools_project

# Globals and constants variables.

project = Project(find_package_path('ebsdtools.hkl.flamenco'))

# dependencies
project.dependencies.append(tkintertools_project)

# base
project.metadata.name = "pyFlamenco"
project.metadata.author = "Philippe T. Pinard"
project.metadata.author_email = "philippe.pinard@gmail.com"
project.metadata.version = "0.1"
project.metadata.description = "Editor/viewer of the HKL Channel 5 CPR file"
project.metadata.license = "GPL v3"
project.metadata.classifiers = [
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Scientific/Engineering"]
project.metadata.platforms = "OS Independent"

# setup
project.packages = find_packages("ebsdtools.hkl.flamenco",
                                 where=project.dir)
project.package_data = \
    {'ebsdtools.hkl.flamenco': ['cprGUI.ini', 'cpr.ico', 'cprmaster.cpr']}
project.data_files = []

# py2exe
project.windows_scripts = [{"script": os.path.join(project.dir, 'cprGUI.py'),
                            "icon_resources": [(1, os.path.join(project.dir, 'cpr.ico'))]}]
project.console_scripts = []

# nsis
project.nsi_filepath = os.path.join(project.dir, 'build.nsi')

# doc
project.doc_dir = os.path.join(project.dir, 'doc')

class Build(BaseBuild, SetupBuild, DocBuild, TestBuild, CoverageBuild,
            Py2exeBuild, NSISBuild):
    def __init__(self, project):
        BaseBuild.__init__(self, project)
        SetupBuild.__init__(self, project)
        DocBuild.__init__(self, project)
        TestBuild.__init__(self, project)
        CoverageBuild.__init__(self, project)
        Py2exeBuild.__init__(self, project, tkinter=True)
        NSISBuild.__init__(self, project)

if __name__ == '__main__': #pragma: no cover
    build = Build(project)
    build.run()
