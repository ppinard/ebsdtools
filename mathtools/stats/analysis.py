#!/usr/bin/env python
"""
================================================================================
:mod:`analysis` -- Design of experiment analysis
================================================================================

.. module:: analysis
   :synopsis: Design of experiment analysis

"""

# Script information for the file.
__author__ = "Philippe T. Pinard"
__email__ = "philippe.pinard@gmail.com"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2010 Philippe T. Pinard"
__license__ = "GPL v3"

# Standard library modules.
import warnings

# Third party modules.
import numpy as np
from scipy.stats import probplot
warnings.filterwarnings("ignore", category=DeprecationWarning, module="scipy")

from matplotlib.figure import Figure

# Local modules.

# Globals and constants variables.


def probplot_frequency(*args):
    """
    Draws a probability plot to verify if samples are normally distributed using
    the observed comulative frequency.
    Wrapper over :func:`scipy.stats.probplot`.
    
    :arg args: samples
    :type args: tuple with (name, data)
    
    :return: :class:`matplotlib.figure.Figure`
    """
    fig = Figure()
    ax = fig.add_subplot("111")

    for i, arg in enumerate(args):
        if isinstance(arg, tuple):
            assert len(arg) == 2
            name = arg[0]
            data = arg[1]
        else:
            name = "Sample %i" % i
            data = arg

        (xs, ys), (slope, intercept, r) = probplot(data)

        ax.plot(xs, ys, 'o-', label=name)

        fit_ys = [slope * x + intercept for x in xs]

        ax.plot(xs, fit_ys, '-', label=r'r=%f' % r)

    ax.set_xlabel(r"Order statistic medians")
    ax.set_ylabel(r"Ordered response data")

    ax.legend(loc='best')

    return fig

def probplot_residuals(*args):
    """
    Draws a probability plot to verify if samples are normally distributed using
    the residuals (for ANOVA analysis).
    Wrapper over :func:`scipy.stats.probplot`.
    
    :arg args: samples
    
    :return: :class:`matplotlibtools.figure.Figure`
    """
    # Calculate sample means
    means = np.zeros(len(args))
    for i, sample in enumerate(args):
        means[i] = np.mean(sample)

    # Calculate residuals
    residuals = []
    for i, sample in enumerate(args):
        for datum in sample:
            residual = datum - means[i]
            residuals.append(residual)

    # Create figure
    fig = Figure()
    ax = fig.add_subplot("111")

    (xs, ys), (slope, intercept, r) = probplot(residuals)

    ax.plot(xs, ys, 'o', label="__nolabel__")

    fit_ys = [slope * x + intercept for x in xs]

    ax.plot(xs, fit_ys, '-', label=r'r=%f' % r)

    ax.set_xlabel(r"Ordered statistic medians")
    ax.set_ylabel(r"Ordered residuals")

    ax.legend(loc='best')

    return fig

def anova_table():
    pass

if __name__ == '__main__': #pragma: no cover
    import DrixUtilities.Runner as Runner
    Runner.Runner().run(runFunction=None)

