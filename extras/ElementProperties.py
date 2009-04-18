#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2007 Hendrix Demers"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = "$Revision: 1186 $"
__svnDate__ = "$Date: 2009-01-24 17:14:04 -0500 (Sat, 24 Jan 2009) $"
__svnId__ = "$Id: ElementProperties.py 1186 2009-01-24 22:14:04Z hdemers $"

# Standard library modules.
import math

# Third party modules.

# Local modules.

# Globals and constants variables.
g_AvogadroNumber_atom_mol = 6.02205E23

g_elementSymbol = [
    "H"  , "He" , "Li" , "Be" , "B"  , "C"  , "N"  , "O"
  , "F"  , "Ne" , "Na" , "Mg" , "Al" , "Si" , "P"  , "S"
  , "Cl" , "Ar" , "K"  , "Ca" , "Sc" , "Ti" , "V"  , "Cr"
  , "Mn" , "Fe" , "Co" , "Ni" , "Cu" , "Zn" , "Ga" , "Ge"
  , "As" , "Se" , "Br" , "Kr" , "Rb" , "Sr" , "Y"  , "Zr"
  , "Nb" , "Mo" , "Tc" , "Ru" , "Rh" , "Pd" , "Ag" , "Cd"
  , "In" , "Sn" , "Sb" , "Te" , "I"  , "Xe" , "Cs" , "Ba"
  , "La" , "Ce" , "Pr" , "Nd" , "Pm" , "Sm" , "Eu" , "Gd"
  , "Tb" , "Dy" , "Ho" , "Er" , "Tm" , "Yb" , "Lu" , "Hf"
  , "Ta" , "W"  , "Re" , "Os" , "Ir" , "Pt" , "Au" , "Hg"
  , "Tl" , "Pb" , "Bi" , "Po" , "At" , "Rn" , "Fr" , "Ra"
  , "Ac" , "Th" , "Pa" , "U"  , "Np" , "Pu" , "Am" , "Cm"
  , "Bk" , "Cf" , "Es" , "Fm" , "Md" , "No" , "Lr" , "Unq"
  , "Unp" , "Unh"]

g_elementName = [
    "Hydrogen"
  , "Helium"
  , "Lithium"
  , "Beryllium"
  , "Boron"
  , "Carbon"
  , "Nitrogen"
  , "Oxygen"
  , "Fluorine"
  , "Neon"
  , "Sodium"
  , "Magnesium"
  , "Aluminium"
  , "Silicon"
  , "Phosphorus"
  , "Sulfur"
  , "Chlorine"
  , "Argon"
  , "Potassium"
  , "Calcium"
  , "Scandium"
  , "Titanium"
  ,  "Vanadium"
  , "Chromium"
  , "Manganese"
  , "Iron"
  , "Cobalt"
  , "Nickel"
  , "Copper"
  , "Zinc"
  , "Gallium"
  , "Germanium"
  , "Arsenic"
  , "Selenium"
  , "Bromine"
  , "Krypton"
  , "Rubidium"
  , "Strontium"
  , "Yttrium"
  , "Zirconium"
  , "Niobium"
  , "Molybdenum"
  , "Technetium"
  , "Ruthenium"
  , "Rhodium"
  , "Palladium"
  , "Silver"
  , "Cadmium"
  , "Indium"
  , "Tin"
  , "Antimony"
  , "Tellurium"
  , "Iodine"
  , "Xenon"
  , "Cesium"
  , "Barium"
  , "Lanthanum"
  , "Cerium"
  , "Praseodymium"
  , "Neodymium"
  , "Promethium"
  , "Samarium"
  , "Europium"
  , "Gadolinium"
  , "Terbium"
  , "Dysprosium"
  , "Holmium"
  , "Erbium"
  , "Thulium"
  , "Ytterbium"
  ,  "Lutetium"
  , "Hafnium"
  , "Tantalum"
  , "Tungsten"
  , "Rhenium"
  , "Osmium"
  , "Iridium"
  , "Platinum"
  , "Gold"
  , "Mercury"
  , "Thallium"
  , "Lead"
  , "Bismuth"
  , "Polonium"
  , "Astatine"
  , "Radon"
  , "Francium"
  , "Radium"
  , "Actinium"
  , "Thorium"
  , "Protactinium"
  , "Uranium"
  , "Neptunium"
  , "Plutonium"
  , "Americium"
  , "Curium"
  , "Berkelium"
  , "Californium"
  , "Einsteinium"
  , "Fermium"
  , "Mendelevium"
  , "Nobelium"
  , "Lawrencium"
  , "Unnilquadium"
  , "Unnilpentium"
  , "Unnilhexium"]

"""
 * Mass density of element in atomic number order.
 *
 * For elment H to Cm (1--96).
 *
 * In \f$ \gram\per\centi\meter^{3} \f$.
 *
 * From: Tableau periodique des elements, Sargent-Welch scientifique Canada
 * Limitee.
 *
 * @note Element Z = 85 and 87 set to 1 for the calculation.
"""
g_massDensity_g_cm3 = [
  0.0899, 0.1787, 0.5300, 1.8500, 2.3400, 2.6200, 1.2510, 1.4290,
  1.6960, 0.9010, 0.9700, 1.7400, 2.7000, 2.3300, 1.8200, 2.0700,
  3.1700, 1.7840, 0.8600, 1.5500, 3.0000, 4.5000, 5.8000, 7.1900,
  7.4300, 7.8600, 8.9000, 8.9000, 8.9600, 7.1400, 5.9100, 5.3200,
  5.7200, 4.8000, 3.1200, 3.7400, 1.5300, 2.6000, 4.5000, 6.4900,
  8.5500, 10.200, 11.500, 12.200, 12.400, 12.000, 10.500, 8.6500,
  7.3100, 7.3000, 6.6800, 6.2400, 4.9200, 5.8900, 1.8700, 3.5000,
  6.7000, 6.7800, 6.7700, 7.0000, 6.4750, 7.5400, 5.2600, 7.8900,
  8.2700, 8.5400, 8.8000, 9.0500, 9.3300, 6.9800, 9.8400, 13.100,
  16.600, 19.300, 21.000, 22.400, 22.500, 21.400, 19.300, 13.530,
  11.850, 11.400, 9.8000, 9.4000, 1.0000, 9.9100, 1.0000, 5.0000,
  10.070, 11.700, 15.400, 18.900, 20.400, 19.800, 13.600, 13.511
]
"""
 * Atomic weight of element in atomic number order.
 *
 * For element H to Sg (1--106).
 *
 * Unit \f$ \gram\per\mole \f$.
 *
 * From: Tableau periodique des elements, Sargent-Welch scientifique Canada
 * Limitee.
"""
g_atomicMass_g_mol = [
  1.0079000, 4.0026000, 6.9410000, 9.0121800, 10.810000, 12.011000,
  14.006700, 15.999400, 18.998403, 20.179000, 22.989770, 24.305000,
  26.981540, 28.085500, 30.973760, 32.060000, 35.453000, 39.948000,
  39.098300, 40.080000, 44.955900, 47.900000, 50.941500, 51.996000,
  54.938000, 55.847000, 58.933200, 58.700000, 63.546000, 65.380000,
  69.720000, 72.590000, 74.921600, 78.960000, 79.904000, 83.800000,
  85.467800, 87.620000, 88.905600, 91.220000, 92.906400, 95.940000,
  98.000000, 101.07000, 102.90550, 106.40000, 107.86800, 112.41000,
  114.82000, 118.69000, 121.75000, 127.60000, 126.90450, 131.30000,
  132.90540, 137.33000, 138.90550, 140.12000, 140.90770, 144.24000,
  145.00000, 150.40000, 151.96000, 157.25000, 158.92540, 162.50000,
  164.93040, 167.26000, 168.93420, 173.04000, 174.96700, 178.49000,
  180.94790, 183.85000, 186.20700, 190.20000, 192.22000, 195.09000,
  196.96650, 200.59000, 204.37000, 207.20000, 208.98040, 209.00000,
  210.00000, 222.00000, 223.00000, 226.02540, 227.02780, 232.03810,
  231.03590, 238.02900, 237.04820, 244.00000, 243.00000, 247.00000,
  247.00000, 251.00000, 252.00000, 257.00000, 258.00000, 259.00000,
  260.00000, 261.00000, 262.00000, 263.00000
]

"""
 * Fermi energy of element in atomic number order.
 *
 * For element H to Lr (1--103).
 * From: CASINO source code, DOS version.
 *
 * @todo Add units.
"""
g_FermiEnergy = [
  1.000, 1.000, 4.700, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000,
  1.000, 3.100, 1.000, 1.000, 0.555, 1.000, 1.000, 1.000, 1.000,
  1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000,
  1.000, 7.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000,
  1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000,
  1.000, 5.500, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000,
  1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000,
  1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000,
  1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 5.500, 1.000, 1.000,
  1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000,
  1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 0.000,
  1.000, 1.000, 1.000, 1.000
]

"""
 * Fermi wavelength of element in atomic number order.
 *
 * For element H to Lr (1--103).
 * From: CASINO source code, DOS version.
 *
 * @todo Add units.
"""
g_kFermi = [
  7.00E7, 7.00E7, 1.10E8, 7.00E7, 7.00E7, 7.00E7, 7.00E7, 7.00E7,
  7.00E7, 7.00E7, 9.00E7, 7.00E7, 7.00E7, 4.00E7, 7.00E7, 7.00E7,
  7.00E7, 7.00E7, 7.00E7, 7.00E7, 7.00E7, 7.00E7, 7.00E7, 7.00E7,
  7.00E7, 7.00E7, 7.00E7, 7.00E7, 1.35E8, 7.00E7, 7.00E7, 7.00E7,
  7.00E7, 7.00E7, 7.00E7, 7.00E7, 7.00E7, 7.00E7, 7.00E7, 7.00E7,
  7.00E7, 7.00E7, 7.00E7, 7.00E7, 7.00E7, 7.00E7, 1.19E8, 7.00E7,
  7.00E7, 7.00E7, 7.00E7, 7.00E7, 7.00E7, 7.00E7, 7.00E7, 7.00E7,
  7.00E7, 7.00E7, 7.00E7, 7.00E7, 7.00E7, 7.00E7, 7.00E7, 7.00E7,
  7.00E7, 7.00E7, 7.00E7, 7.00E7, 7.00E7, 7.00E7, 7.00E7, 7.00E7,
  7.00E7, 7.00E7, 7.00E7, 7.00E7, 7.00E7, 7.00E7, 1.19E8, 7.00E7,
  7.00E7, 7.00E7, 7.00E7, 7.00E7, 7.00E7, 7.00E7, 7.00E7, 7.00E7,
  7.00E7, 7.00E7, 7.00E7, 7.00E7, 7.00E7, 7.00E7, 7.00E7, 7.00E7,
  7.00E7, 7.00E7, 0.00E0, 7.00E7, 7.00E7, 7.00E7, 7.00E7
]

"""
 * Plasmon energy of element in atomic number order.
 *
 * For element H to Lr (1--103).
 * From: CASINO source code, DOS version.
 *
 * @todo Add units.
"""
g_plasmonEnergy = [
  15.0, 15.0, 7.10, 18.7, 22.7, 15.0, 15.0, 15.0, 15.0, 15.0, 5.70,
  10.3, 15.0, 16.7, 15.0, 15.0, 15.0, 15.0, 3.70, 8.80, 14.0, 17.9,
  21.8, 24.9, 21.6, 23.0, 20.9, 20.7, 19.3, 17.2, 13.8, 16.2, 15.0,
  15.0, 15.0, 15.0, 3.41, 8.00, 12.5, 15.0, 15.0, 15.0, 15.0, 15.0,
  15.0, 15.0, 15.0, 19.2, 15.0, 13.4, 15.2, 17.0, 11.4, 15.0, 2.90,
  7.20, 15.0, 15.0, 15.0, 15.0, 15.0, 15.0, 15.0, 15.0, 13.3, 15.0,
  15.0, 14.0, 15.0, 15.0, 15.0, 15.0, 15.0, 15.0, 15.0, 15.0, 15.0,
  35.0, 15.0, 15.0, 15.0, 13.0, 14.2, 15.0, 15.0, 15.0, 15.0, 15.0,
  25.0, 15.0, 15.0, 15.0, 15.0, 15.0, 15.0, 15.0, 15.0, 15.0, 15.0,
  15.0, 15.0, 15.0, 15.0
]
def getMassDensity_g_cm3(atomicNumber):
  index = atomicNumber-1
  return g_massDensity_g_cm3[index]

def getAtomicMass_g_mol(atomicNumber):
  index = atomicNumber-1
  return g_atomicMass_g_mol[index]

def getFermiEnergy_eV(atomicNumber):
  index = atomicNumber-1
  return g_FermiEnergy[index]

def getKFermi_eV(atomicNumber):
  index = atomicNumber-1
  return g_kFermi[index]

def getPlasmonEnergy_eV(atomicNumber):
  index = atomicNumber-1
  return g_plasmonEnergy[index]

def getMeanIonizationEnergy_eV(atomicNumber):
  """
   * Get the mean ionization potential from the atomic number.
   *
   * In \f$ \electronvolt \f$.
   *
   * @param[in] atomicNumber Atomic number.
  """

  if atomicNumber <= 13.0:
    Value = 11.5*atomicNumber
  else:
    if math.pow(atomicNumber, 0.19) > 0.0:
      Value = 9.76*atomicNumber + 58.8/math.pow(atomicNumber, 0.19)
    else:
      Value = 0.0

  return Value

def getKRatioCorrection(atomicNumber):
  """
   * Get the constant k ratio correction needed by the mean ionization potential
   * from the atomic number.
   *
   * @param[in] atomicNumber Atomic number.
  """
  Value = 0.734*math.pow(atomicNumber, 0.037);

  return Value

def computeAtomicDensity_atom_cm3(massDensity_g_cm3, atomicMass_g_mol):
  """
   * Compute the atomic density.
   *
   * \f[
   *   n_{i} = \frac{N_{A} \rho_{i}}{A_{i}}
   * \f]
   * where
   * - \f$ n_{i} \f$ is the atomic density in \f$ \mathrm{atoms}\per\centi\meter^{3} \f$
   * - \f$ N_{A} \f$ is the Avogadro number in \f$ \mathrm{atoms}\per\mole \f$
   * - \f$ \rho_{i} \f$ is the mass density in \f$ \gram\per\centi\meter^{3} \f$
   * - \f$ A_{i} \f$ is the atomic mass in \f$ \gram\per\mole \f$
   *
   * \param[in] massDensity_g_cm3
   * \param[in] atomicMass_g_mol
  """

  return g_AvogadroNumber_atom_mol*massDensity_g_cm3/atomicMass_g_mol

def getSymbol(atomicNumber):
  index = atomicNumber-1
  return g_elementSymbol[index]

def getName(atomicNumber):
  index = atomicNumber-1
  return g_elementName[index]

def getAtomicNumber(symbol=None):
  if symbol:
    try:
      return g_elementSymbol.index(symbol.capitalize())+1
    except ValueError:
      print symbol

def getAtomicNumberBySymbol(symbol):
    try:
      return g_elementSymbol.index(symbol.capitalize())+1
    except ValueError:
      print symbol

def getAtomicNumberByName(name):
    try:
      return g_elementName.index(name.capitalize())+1
    except ValueError:
      print symbol

def getAtomicNumber(atomicNumber=None, name=None, symbol=None):
  if atomicNumber != None:
    return int(atomicNumber)
  elif name != None:
    return getAtomicNumberByName(name)
  elif symbol != None:
    return getAtomicNumberBySymbol(symbol)

def run():
  print getMassDensity_g_cm3(24)
  print 7.19*0.054

if __name__ == '__main__': #pragma: no cover
  import DrixUtilities.Runner as Runner
  Runner.Runner().run(runFunction=run)
