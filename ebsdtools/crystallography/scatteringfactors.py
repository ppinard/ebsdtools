#!/usr/bin/env python
"""
================================================================================
:mod:`scatteringfactors` -- Diffraction scattering factors.
================================================================================

.. module:: scatteringfactors
   :synopsis: Diffraction scattering factors.

.. inheritance-diagram:: ebsdtools.crystallography.scatteringfactors

"""

# Script information for the file.
__author__ = "Philippe T. Pinard"
__email__ = "philippe.pinard@gmail.com"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2009 Philippe T. Pinard"
__license__ = "GPL v3"

# Subversion informations for the file.
__svnRevision__ = ""
__svnDate__ = ""
__svnId__ = ""

# Standard library modules.
import os.path
import configparser
import csv
import warnings
from math import pi, exp

# Third party modules.

# Local modules.
import DatabasesTools.ElementProperties as ElementProperties

# Globals and constants variables.

class ScatteringFactors:
    SECTION_NAME = None
    OPTION_FILEPATH_0_2 = None
    OPTION_FILEPATH_2_6 = None

    def __init__(self, configurationfilepath=None):
        """
        Read scattering factors from tables.
        
        Two implementations:
        
          * :class:`ElasticAtomicScatteringFactors`
          * :class:`XrayScatteringFactors`
        
        """
        if configurationfilepath is None:
            relativepath = os.path.join('..', 'ebsdtools.cfg')
            configurationfilepath = \
                os.path.join(os.path.dirname(__file__), relativepath)

        self._readconfiguration(configurationfilepath)

        self._read()

    def _readconfiguration(self, configurationfilepath):
        """
        Read the configuration file for filepaths of the data files.
        
        """
        config = configparser.ConfigParser()

        config.readfp(open(configurationfilepath))

        if config.has_section(self.SECTION_NAME):
            if config.has_option(self.SECTION_NAME, self.OPTION_FILEPATH_0_2):
                self._filepath_0_2 = config.get(self.SECTION_NAME,
                                                self.OPTION_FILEPATH_0_2)

            if config.has_option(self.SECTION_NAME, self.OPTION_FILEPATH_2_6):
                self._filepath_2_6 = config.get(self.SECTION_NAME,
                                                self.OPTION_FILEPATH_2_6)

    def _read(self):
        raise NotImplementedError

class ElasticAtomicScatteringFactors(ScatteringFactors):
    SECTION_NAME = 'ElasticAtomicScatteringFactors'
    OPTION_FILEPATH_0_2 = 'filepath_0_2'
    OPTION_FILEPATH_2_6 = 'filepath_2_6'

    ATOMICNUMBER = 'Z'

    def __init__(self, configurationfilepath=None):
        """
        Return the elastic atomic scattering factors as given by the
        Crystallography Tables.
        The data is a exponential fit of the scattering factors.
        
        It is calculated from :math:`s = \\frac{4\\pi\\sin\\theta}{\\lambda}`.
        It is separated into two files: from 0 to 2 A^{-1} and 2 to 6 A^{-1}.
        
        :arg configurationfilepath: file path of the configuration file for the
            module. If ``None``, the default configuration file is loaded.
        :type configurationfilepath: :class:`str`
        
        **References**
          International Tables For Crystallography, Volume C, p. 262 and 282-285
        
        """
        if configurationfilepath is None:
            relativepath = os.path.join('..', 'ebsdtools.cfg')
            configurationfilepath = \
                os.path.join(os.path.dirname(__file__), relativepath)

        self._readconfiguration(configurationfilepath)

        self._read()

    def _read(self):
        """
        Read the data in the data files and store them in
        
          * :attr:`coefficients_0_2`
          * :attr:`coefficients_2_6`
        
        """
        # Data from 0 to 2 A^{-1}.
        self.coefficients_0_2 = {}
        rows = csv.DictReader(open(self._filepath_0_2, 'r'))

        for row in rows:
            atomicnumber = int(row[self.ATOMICNUMBER])
            row.pop(self.ATOMICNUMBER) # Remove item

            self.coefficients_0_2.setdefault(atomicnumber, self._formatrow(row))

        # Data from 2 to 6 A^{-1}.
        self.coefficients_2_6 = {}
        rows = csv.DictReader(open(self._filepath_2_6, 'r'))

        for row in rows:
            atomicnumber = int(row[self.ATOMICNUMBER])
            row.pop(self.ATOMICNUMBER)

            self.coefficients_2_6.setdefault(atomicnumber, self._formatrow(row))

    def _formatrow(self, row):
        """
        Format the values in the row to be :class:`float`.
        
        """
        for key, value in row.iteritems():
            row[key] = float(value)

        return row

    def get(self, atomicnumber, planespacing):
        """
        Return the scattering factor for *atomicnumber* and a *plane*.
        
        :arg atomicnumber: atomic number of the atom
        :type atomicnumber: :class:`int`
        
        :arg planespacing: spacing of a given plane in angstroms
        :type planespacing: :class:`float`
        
        **Calculations**
        
          The variable *s* used in the calculations is defined as
          :math:`s = \\frac{4\\pi\\sin\\theta}{\\lambda}`.
        
          The values are limited for 0 < s < 6 A^{-1}.
          A warning is returned is *s* exceeds these limits.
        
          More easily it can be calculated from the plane spacing (*d*):
          :math:`s = \\frac{2\\pi}{d}`.
        
          For the plane spacing the values are limited for d > 1.047 angstroms.
        
        :rtype: :class:`float`
        
        """
        s = 2 * pi / planespacing
        return self._get(atomicnumber, s)

    def _get(self, atomicnumber, s):
        """
        Return scattering factor.
        
        """
        # For s between 0 and 2.
        if s >= 0 and s < 2:
            return self._calculate_scatteringfactor_0_2(s, atomicnumber)

        # For s between 2 and 6.
        elif s >= 2 and s < 6:
            return self._calculate_scatteringfactor_2_6(s, atomicnumber)

        # For s greater than 6.
        else:
            warnings.warn("Outside table range of s (%e) < 6\AA" % s,
                          ScatteringFactorWarning)
            return self._calculate_scatteringfactor_2_6(s, atomicnumber)

    def _calculate_scatteringfactor_0_2(self, s, atomicnumber):
        """
        Calculate the scattering factor between 0 and 2.
        
        """
        coeffs = self.coefficients_0_2.get(atomicnumber)
        if coeffs is None:
            raise KeyError("Atomic number not in table")

        a = [coeffs['a1'], coeffs['a2'], coeffs['a3'], coeffs['a4'], coeffs['a5']]
        b = [coeffs['b1'], coeffs['b2'], coeffs['b3'], coeffs['b4'], coeffs['b5']]

        return self._calculate_scatteringfactor(s, a, b)

    def _calculate_scatteringfactor_2_6(self, s, atomicnumber):
        """
        Calculate the scattering factor between 2 and 6.
        
        """
        coeffs = self.coefficients_2_6.get(atomicnumber)
        if coeffs is None:
            raise KeyError("Atomic number not in table")

        a = [coeffs['a1'], coeffs['a2'], coeffs['a3'], coeffs['a4'], coeffs['a5']]
        b = [coeffs['b1'], coeffs['b2'], coeffs['b3'], coeffs['b4'], coeffs['b5']]

        return self._calculate_scatteringfactor(s, a, b)

    def _calculate_scatteringfactor(self, s, a, b):
        """
        Calculate factor.
        
        """
        f = 0.0

        for i in range(5):
            f += a[i] * exp(-b[i] * s ** 2)

        return f

class XrayScatteringFactors(ScatteringFactors):
    SECTION_NAME = 'XrayScatteringFactors'
    OPTION_FILEPATH_0_2 = 'filepath_0_2'
    OPTION_FILEPATH_2_6 = 'filepath_2_6'

    SYMBOL = 'symbol'
    CHARGE = 'charge'
    MODEL = 'model'

    MODEL_HF = 'HF' # ?
    MODEL_RHF = 'RHF' # Relativistic wavefunctions by Doyle & Turner 1968
    MODEL_RHF_ = '*RHF' # Relativistic wavefunctions by Croner & Waber 1968 using
                        # wavefunctions of Mann 1968
    MODEL_DS_ = '*DS' # Relativistic Dirac-Slater wavefunctions
    MODEL_FOT = 'FOT' # Fox, O'Keefe & Tabbernor 1989

    MODELS = [MODEL_HF, MODEL_DS_, MODEL_RHF, MODEL_RHF_, MODEL_FOT]

    def __init__(self, configurationfilepath=None):
        """
        Return the x-ray scattering factors as given by the
        Crystallography Tables.
        The data is a exponential fit of the scattering factors.
        
        It is calculated from :math:`s = \\frac{\\sin\\theta}{\\lambda}`.
        It is separated into two files: from 0 to 2 A^{-1} and 2 to 6 A^{-1}.
        
        :arg configurationfilepath: file path of the configuration file for the
            module. If ``None``, the default configuration file is loaded.
        :type configurationfilepath: :class:`str`
        
        **References**
          International Tables For Crystallography, Volume C, p. 565 and 578-581
        
        """
        if configurationfilepath is None:
            relativepath = os.path.join('..', 'ebsdtools.cfg')
            configurationfilepath = \
                os.path.join(os.path.dirname(__file__), relativepath)

        self._readconfiguration(configurationfilepath)

        self._read()

    def _read(self):
        """
        Read the data in the data files and store them in
        
          * :attr:`coefficients_0_2`
          * :attr:`coefficients_2_6`
        
        """
        # Data from 0 to 2 A^{-1}.
        self.coefficients_0_2 = {}
        rows = csv.DictReader(open(self._filepath_0_2, 'r'))

        for row in rows:
            atomicnumber = self._readatomicnumber(row)
            charge = self._readcharge(row)
            key = (atomicnumber, charge)

            row.pop(self.SYMBOL) # Remove item
            row.pop(self.CHARGE) # Remove item

            self.coefficients_0_2.setdefault(key, self._formatrow(row))

        # Data from 2 to 6 A^{-1}.
        self.coefficients_2_6 = {}
        rows = csv.DictReader(open(self._filepath_2_6, 'r'))

        for row in rows:
            atomicnumber = self._readatomicnumber(row)
            charge = self._readcharge(row)
            key = (atomicnumber, charge)

            row.pop(self.SYMBOL) # Remove item
            row.pop(self.CHARGE) # Remove item

            self.coefficients_2_6.setdefault(key, self._formatrow(row))

    def _readatomicnumber(self, row):
        symbol = row[self.SYMBOL].strip()
        atomicnumber = ElementProperties.getAtomicNumberBySymbol(symbol)
        return atomicnumber

    def _readcharge(self, row):
        charge = row[self.CHARGE].strip()
        if charge != 'val':
            return int(float(charge))
        else:
            return charge

    def _formatrow(self, row):
        """
        Format the values in the row to be :class:`float`.
        
        """
        for key, value in row.iteritems():
            if key == self.MODEL:
                row[key] = str(value).strip()
            else:
                row[key] = float(value)

        return row

    def get(self, atomicnumber, planespacing, charge=0):
        """
        
        
        :arg atomicnumber: atomic number of the atom
        :type atomicnumber: :class:`int`
        
        :arg planespacing: spacing of a given plane in angstorms
        :type planespacing: :class:`float`
        
        :arg charge: charge of the atom for ionized element
        :type charge: :class:`int`
        
        **Calculations**
        
          The variable *s* used in the calculations is defined as
          :math:`s = \\frac{\\sin\\theta}{\\lambda}`.
        
          The values are limited for 0 < s < 6 A^{-1}.
          A warning is returned is *s* exceeds these limits.
        
          More easily it can be calculated from the plane spacing (*d*):
          :math:`s = \\frac{1}{2d}`.
        
          For the plane spacing the values are limited for d > 1.047 angstroms.
        
        :rtype: :class:`float`
        
        """
        s = 1 / (2.0 * planespacing)
        return self._get(atomicnumber, s, charge)

    def _get(self, atomicnumber, s, charge=0):
        """
        Return scattering factor.
        
        """
        # For s between 0 and 2.
        if s >= 0 and s < 2:
            return self._calculate_scatteringfactor_0_2(s, atomicnumber, charge)

        # For s between 2 and 6.
        elif s >= 2 and s < 6:
            return self._calculate_scatteringfactor_2_6(s, atomicnumber, charge)

        # For s greater than 6.
        else:
            warnings.warn("Outside table range of s (%e) < 6\AA" % s,
                          ScatteringFactorWarning)
            return self._calculate_scatteringfactor_2_6(s, atomicnumber, charge)

    def _calculate_scatteringfactor_0_2(self, s, atomicnumber, charge):
        """
        Calculate the scattering factor between 0 and 2.
        
        """
        # Coefficients
        coeffs = self.coefficients_0_2.get((atomicnumber, charge))
        if coeffs is None:
            raise KeyError("Atomic number with specified charge not in table")

        a = [coeffs['a1'], coeffs['a2'], coeffs['a3'], coeffs['a4']]
        b = [coeffs['b1'], coeffs['b2'], coeffs['b3'], coeffs['b4']]
        c = coeffs['c']

        # Calculate factor
        f = 0.0

        for i in range(4):
            f += a[i] * exp(-b[i] * s ** 2)

        f += c

        return f

    def _calculate_scatteringfactor_2_6(self, s, atomicnumber, charge):
        """
        Calculate the scattering factor between 2 and 6.
        
        """
        # Coefficients
        coeffs = self.coefficients_2_6.get((atomicnumber, charge))
        if coeffs is None:
            raise KeyError("Atomic number with specified charge not in table")

        a = [coeffs['a0'], coeffs['a1'], coeffs['a2'] / 10.0, coeffs['a3'] / 100.0]

        # Calculate factor
        f = 0.0

        for i in range(4):
            f += a[i] * s ** i

        f = exp(f)

        return f

class ScatteringFactorWarning(Warning):
    """
    Warning when the requested scattering factor is outside
    the range of the data.
    """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

