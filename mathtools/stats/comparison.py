#!/usr/bin/env python
"""
================================================================================
:mod:`comparison` -- Statistical comparison test between samples
================================================================================

.. module:: comparison
   :synopsis: Statistical comparison test between samples

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
import scipy.stats.distributions as distributions
warnings.filterwarnings("ignore", category=DeprecationWarning, module="scipy")

# Local modules.

# Globals and constants variables.

def _significance(alpha, p):
    """
    Test of significance: "If a test of significance gives a p-value lower than 
    the alpha-level, the null hypothesis is rejected." (Wikipedia).
    
    :arg alpha: significance level
    :arg p: p-value
    
    :return: ``true`` if the null hypothesis is rejected 
    """
    return alpha > p

def ztest_onesample(sample, value, variance, alternative="!=", ci=0.95):
    """
    z-test for the comparison of a sample's mean to a specified value.
    Population's mean and variance must be known.
    
    :math:`H_0: \\mu = \\mu_0`
    
    :arg sample: an array
    :arg value: expected value for the mean
    :arg variance: population's variance
    :arg alternative: comparison sign (either !=, < or >) [default: !=]
    :arg ci: confidence interval [default: 0.95]
    
    :return: rejected, z-value, p-value, (lower, upper) values of confidence interval 
      rejected indicates if the hypothesis (H0) is rejected
    """
    assert alternative in ["!=", ">", "<"]

    alpha = 1.0 - ci
    smean = np.mean(sample)

    num = smean - value
    det = np.sqrt(variance / len(sample))
    z0 = num / det

    if alternative == "!=":
        p = 2 * (1 - distributions.norm.cdf(abs(z0)))
        beta = -distributions.norm.ppf(alpha / 2.0) * det
        lower = smean - beta
        upper = smean + beta
    elif alternative == "<":
        p = distributions.norm.cdf(z0)
        beta = -distributions.norm.ppf(alpha) * det
        lower = smean + beta
        upper = float('inf')
    elif alternative == ">":
        p = 1 - distributions.norm.cdf(z0)
        beta = -distributions.norm.ppf(alpha) * det
        lower = -float('inf')
        upper = smean - beta

    return _significance(alpha, p), z0, p, (lower, upper)

#def ztest_twosamples(sample1, sample2, variance1, variance2,
#                     alternative="!=", ci=0.95):
#    """
#    z-test for the comparison of two samples' mean where the variances of both 
#    populations are known.
#    
#    :math:`H_0: \\mu = \\mu_0`
#    
#    :arg sample1: array of sample #1
#    :arg sample2: array of sample #2
#    :arg variance1: variance of population #1
#    :arg variance2: variance of population #2
#    :arg alternative: comparison sign (either !=, < or >) [default: !=]
#    :arg ci: confidence interval [default: 0.95]
#    
#    :return: rejected, z-value, p-value, (lower, upper) values of confidence interval
#      rejected indicates if the hypothesis (H0) is rejected
#    """
#    assert alternative in ["!=", ">", "<"]
#
#    alpha = 1.0 - ci
#    y1m = np.mean(sample1)
#    y2m = np.mean(sample2)
#    n1 = len(sample1)
#    n2 = len(sample2)
#
#    num = y1m - y2m
#    det = np.sqrt(variance1 / n1 + variance2 / n2)
#    z0 = num / det
#
#    if alternative == "!=":
#        p = 2 * (1.0 - distributions.norm.cdf(np.abs(z0)))
#        beta = -distributions.norm.ppf(alpha / 2.0) * det
#        lower = num - beta
#        upper = num + beta
#    elif alternative == "<":
#        p = distributions.norm.cdf(z0)
#        beta = -distributions.norm.ppf(alpha) * det
#        lower = smean + beta
#        upper = float('inf')
#    elif alternative == ">":
#        p = 1.0 - distributions.norm.cdf(z0)
#        beta = -distributions.norm.ppf(alpha) * det
#        lower = -float('inf')
#        upper = smean - beta
#
#    return _significance(alpha, p), z0, p, (lower, upper)

def ttest_onesample(sample, value, alternative="!=", ci=0.95):
    """
    t-test for the comparison of a sample's mean to a specified value.
    The population's variance is unknown.
    The sample must be normally distributed.
    
    :math:`H_0: \\mu = \\mu_0`
    
    :arg sample: an array
    :arg value: expected value for the mean
    :arg alternative: comparison sign (either !=, < or >) [default: !=]
    :arg ci: confidence interval [default: 0.95]
    
    :return: rejected, t-value, p-value, (lower, upper) values of confidence interval
      rejected indicates if the hypothesis (H0) is rejected
    """
    assert alternative in ["!=", ">", "<"]

    alpha = 1.0 - ci
    smean = np.mean(sample)

    num = smean - value
    det = np.sqrt(np.var(sample, ddof=1) / len(sample))
    t0 = num / det
    df = len(sample) - 1

    if alternative == "!=":
        p = 2 * distributions.t.sf(np.abs(t0), df)
        beta = -distributions.t.ppf(alpha / 2.0, df) * det
        lower = smean - beta
        upper = smean + beta
    elif alternative == "<":
        p = distributions.t.cdf(t0, df)
        beta = -distributions.t.ppf(alpha, df) * det
        lower = smean + beta
        upper = float('inf')
    elif alternative == ">":
        p = 1.0 - distributions.t.cdf(t0, df)
        beta = -distributions.t.ppf(alpha, df) * det
        lower = float('-inf')
        upper = smean - beta

    return _significance(alpha, p), t0, p, (lower, upper)

def ttest_twosamples(sample1, sample2, alternative="!=", ci=0.95, equal_var=False):
    """
    t-test for the comparison of two samples' mean where the variances of both 
    populations are unknown.
    
    :math:`H_0: \\mu = \\mu_0`
    
    :arg sample1: array of sample #1
    :arg sample2: array of sample #2
    :arg alternative: comparison sign (either !=, < or >) [default: !=]
    :arg ci: confidence interval [default: 0.95]
    :arg equal_var: if it can be reasonably assume that the populations' 
      variances are equal [default: ``False``]
    :type equal_var: :class:`bool`
    
    :return: rejected, t-value, p-value, (lower, upper) values of confidence interval
      rejected indicates if the hypothesis (H0) is rejected
    """
    assert alternative in ["!=", ">", "<"]

    alpha = 1.0 - ci
    n1 = len(sample1)
    n2 = len(sample2)
    v1 = np.var(sample1, ddof=1)
    v2 = np.var(sample2, ddof=1)

    num = np.mean(sample1) - np.mean(sample2)
    if equal_var:
        df = n1 + n2 - 2
        sp = ((n1 - 1) * v1 + (n2 - 1) * v2) / float(df)

        det = np.sqrt(sp * (1.0 / n1 + 1.0 / n2))
    else:
        num2 = (v1 / n1 + v2 / n2) ** 2
        det2 = ((v1 / n1) ** 2) / (n1 - 1) + ((v2 / n2) ** 2) / (n2 - 1)
        df = num2 / det2

        det = np.sqrt(v1 / n1 + v2 / n2)

    t0 = num / det

    if alternative == "!=":
        p = 2 * distributions.t.sf(np.abs(t0), df)
        beta = -distributions.t.ppf(alpha / 2.0, df) * det
        lower = num - beta
        upper = num + beta
    elif alternative == "<":
        p = distributions.t.cdf(t0, df)
        beta = -distributions.t.ppf(alpha, df) * det
        lower = num + beta
        upper = float('inf')
    elif alternative == ">":
        p = 1.0 - distributions.t.cdf(t0, df)
        beta = -distributions.t.ppf(alpha, df) * det
        lower = float('-inf')
        upper = num - beta

    return _significance(alpha, p), t0, p, (lower, upper)

def chisquare_onesample(sample, value, alternative="!=", ci=0.95):
    """
    chisquare-test for the comparison of a sample's variance to a specified value.
    The sample must be normally distributed.
    
    :math:`H_0: \\mu = \\mu_0`
    
    :arg sample: an array
    :arg value: expected value for the variance
    :arg alternative: comparison sign (either !=, < or >) [default: !=]
    :arg ci: confidence interval [default: 0.95]
    
    :return: rejected, chisquare-value, (lower, upper) values of confidence interval
      rejected indicates if the hypothesis (H0) is rejected
    """
    assert alternative in ["!=", ">", "<"]

    alpha = 1.0 - ci
    n = len(sample)
    df = n - 1
    v = np.var(sample, ddof=1)

    num = df * v
    det = value
    x0 = num / det

    if alternative == "!=":
        p = 2 * distributions.chi2.cdf(np.abs(x0), df)
        lower = num / distributions.chi2.ppf(1.0 - alpha / 2.0, df)
        upper = num / distributions.chi2.ppf(alpha / 2.0, df)
    elif alternative == "<":
        p = distributions.chi2.cdf(x0, df)
        lower = num / distributions.chi2.ppf(alpha, df)
        upper = float("inf")
    elif alternative == ">":
        p = 1.0 - distributions.chi2.cdf(x0, df)
        lower = float("-inf")
        upper = num / distributions.chi2.ppf(1.0 - alpha, df)

    return _significance(alpha, p), x0, p, (lower, upper)

def ftest_twosamples(sample1, sample2, alternative="!=", ci=0.95):
    """
    F-test for the comparison of two samples' variances where the variances of 
    both populations are unknown.
    
    :math:`H_0: \\mu = \\mu_0`
    
    :arg sample1: array of sample #1
    :arg sample2: array of sample #2
    :arg alternative: comparison sign (either !=, < or >) [default: !=]
    :arg ci: confidence interval [default: 0.95]
    
    :return: rejected, F-value, p-value, (lower, upper) values of confidence interval
      rejected indicates if the hypothesis (H0) is rejected
    """

    assert alternative in ["!=", ">", "<"]

    alpha = 1.0 - ci
    v1 = np.var(sample1, ddof=1)
    v2 = np.var(sample2, ddof=1)
    df1 = len(sample1) - 1
    df2 = len(sample2) - 1

    f0 = v1 / v2

    if alternative == "!=":
        p = 2 * (1.0 - distributions.f.cdf(np.abs(f0), df1, df2))
    elif alternative == "<":
        p = distributions.f.cdf(f0, df1, df2)
    elif alternative == ">":
        p = 1.0 - distributions.f.cdf(f0, df1, df2)

    return _significance(alpha, p), f0, p

if __name__ == '__main__': #pragma: no cover
    import DrixUtilities.Runner as Runner
    Runner.Runner().run(runFunction=None)

