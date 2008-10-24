#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Philippe Pinard (philippe.pinard@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2008 Philippe Pinard"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = ""
__svnDate__ = ""
__svnId__ = ""

# Standard library modules.
import cProfile
import pstats
import hotshot, hotshot.stats

# Third party modules.

# Local modules.
import EBSDTools.indexation.phases


#cProfile.run('EBSDTools.indexation.phases.run()', 'results')
#
#p = pstats.Stats('results')
#p.sort_stats('time')
#p.print_stats(['findLatticeMatch', '_calculatePatternAngles', '_compareAngles'])


prof = hotshot.Profile("phases.prof")
prof.run('EBSDTools.indexation.phases.run()')
prof.close()
stats = hotshot.stats.load("phases.prof")
stats.strip_dirs()
stats.sort_stats('time', 'calls')
stats.print_stats()