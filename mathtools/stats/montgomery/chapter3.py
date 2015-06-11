#!/usr/bin/env python
"""
================================================================================
:mod:`chapter3` -- Example from Montgomery's Design of experiment book
================================================================================

.. module:: chapter3
   :synopsis: Example from Montgomery's Design of experiment book

"""

# Script information for the file.
__author__ = "Philippe T. Pinard"
__email__ = "philippe.pinard@gmail.com"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2010 Philippe T. Pinard"
__license__ = "GPL v3"

# Standard library modules.

# Third party modules.
import numpy as np
from scipy.stats import f_oneway

# Local modules.
from mathtools.stats.analysis import probplot_residuals
from matplotlibtools.figurewx import show

# Globals and constants variables.
s1 = np.array([575, 542, 530, 539, 570])
s2 = np.array([565, 593, 590, 579, 610])
s3 = np.array([600, 651, 610, 637, 629])
s4 = np.array([725, 700, 715, 685, 710])

def example3_1():
    f, p = f_oneway(s1, s2, s3, s4)
    print "F = %e, p-value = %e" % (f, p)

def figure3_4():
    fig = probplot_residuals(s1, s2, s3, s4)
    show(fig)

if __name__ == '__main__': #pragma: no cover
    import DrixUtilities.Runner as Runner
    Runner.Runner().run(runFunction=figure3_4)

