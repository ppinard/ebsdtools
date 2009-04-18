#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Philippe Pinard (philippe.pinard@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2008-2009 Philippe Pinard"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = ""
__svnDate__ = ""
__svnId__ = ""

# Standard library modules.
from math import sin, cos, pi
import warnings

# Third party modules.

# Local modules.
from EBSDTools.mathTools.mathExtras import _acos
import EBSDTools.crystallography.reflectors as reflectors
import EBSDTools.crystallography.cif as cif
try:
  import DatabasesTools.ElementProperties as ElementProperties
except:
  import EBSDTools.extras.ElementProperties as ElementProperties

warnings.filterwarnings(action='ignore', category=RuntimeWarning)

def latticeFromCif(cifreader):
  """
  Create a :class:`Lattice <EBSDTools.crystallography.lattice.Lattice>` class from a cif 
  
  :arg cifreader: a cifreader class
  :type cifreader: :class:`cifreader <EBSDTools.crystallography.cif.cifreader>`
  
  :rtype: :class:`Lattice <EBSDTools.crystallography.lattice.Lattice>`
  """
  a = cifreader.getValue(cif.CELL_LENGTH_A)[0]
  b = cifreader.getValue(cif.CELL_LENGTH_B)[0]
  c = cifreader.getValue(cif.CELL_LENGTH_C)[0]
  alpha = cifreader.getValue(cif.CELL_ANGLE_ALPHA)[0] * pi / 180.0
  beta = cifreader.getValue(cif.CELL_ANGLE_BETA)[0] * pi / 180.0
  gamma = cifreader.getValue(cif.CELL_ANGLE_GAMMA)[0] * pi / 180.0
  
  atoms = _applySymmetryToAtomSite(cifreader.getValue(cif.SYMMETRY_EQUIV_POS_AS_XYZ)
                                   , cifreader.getValue(cif.ATOM_SITE_LABEL)
                                   , cifreader.getValue(cif.ATOM_SITE_FRACT_X)
                                   , cifreader.getValue(cif.ATOM_SITE_FRACT_Y)
                                   , cifreader.getValue(cif.ATOM_SITE_FRACT_Z))
  
  return Lattice(a, b, c, alpha, beta, gamma, atoms)

def _applySymmetryToAtomSite(symmetry_equiv_pos_as_xyz
                            , atom_site_labels
                            , atom_site_fract_xs
                            , atom_site_fract_ys
                            , atom_site_fract_zs):
  
  atomSites = {}
  for i, atom_site_label in enumerate(atom_site_labels):
    #Remove digits after the chemical symbol
    if len(atom_site_label) > 1 and atom_site_label[1].isdigit():
      symbol = atom_site_label[0]
    else:
      symbol = atom_site_label[:2]
    
    atomicnumber = ElementProperties.getAtomicNumberBySymbol(symbol)
    
    atomSites.setdefault((atom_site_fract_xs[i][0], atom_site_fract_ys[i][0], atom_site_fract_zs[i][0]), atomicnumber)
  
  for atomSite in atomSites.keys():
    x, y, z = atomSite
    atomicnumber = atomSites[atomSite]
    
    for equivPos in symmetry_equiv_pos_as_xyz:
      equivX, equivY, equivZ = equivPos
      
      #Allow float division
      equivX = equivX.replace('1/', '1.0/').replace('2/', '2.0/').replace('3/', '3.0/').replace('4/', '4.0/').replace('6/', '6.0/')
      equivY = equivY.replace('1/', '1.0/').replace('2/', '2.0/').replace('3/', '3.0/').replace('4/', '4.0/').replace('6/', '6.0/')
      equivZ = equivZ.replace('1/', '1.0/').replace('2/', '2.0/').replace('3/', '3.0/').replace('4/', '4.0/').replace('6/', '6.0/')
      
      #Replace x, y, z by the value
      newX = eval(equivX.replace('x', str(x)).replace('y', str(y)).replace('z', str(z)))
      newY = eval(equivY.replace('x', str(x)).replace('y', str(y)).replace('z', str(z)))
      newZ = eval(equivZ.replace('x', str(x)).replace('y', str(y)).replace('z', str(z)))
      
      if newX < 0: newX += 1
      if newY < 0: newY += 1
      if newZ < 0: newZ += 1
      
      #Add if new position
      if not (newX, newY, newZ) in atomSites.keys():
        atomSites.setdefault((newX, newY, newZ), atomicnumber)
    
  return atomSites

class Lattice:
  def __init__(self, a, b, c, alpha, beta, gamma, atoms=None):
    """
    Initiate the :class:`Lattice`.
    The reciprocal basis and volume are automatically calculated.
    A :class:`Reflectors <EBSDTools.crystallography.reflectors.Reflectors>` is initiated based on the atoms positions
    
    :arg a, b, c: lattice parameter in :math:`\\text{angstroms}`
    :type a, b, c: float
    
    :arg alpha, beta, gamma: lattice angle in :math:`\\text{radians}`
    :type alpha, beta, gamma: float
    
    :arg atoms: atoms positions in fraction of lattice parameters and atomic number of the atom at that position (``default=None``)
    :type atoms: dict
    
    :arg reflectorsMaxIndice: maximum indices for the reflectors calculation (``default=4``)
    :type reflectorsMaxIndice: integer
    
    **Example** ::
      
      atoms = {(0,0,0): 14, (0.5,0.5,0.5): 13} #Si atoms at (0,0,0) and Aluminum atoms at (0.5, 0.5, 0.5)
    """
    
    self.a = float(a)
    self.b = float(b)
    self.c =  float(c)
    self.alpha =  float(alpha)
    self.beta =  float(beta)
    self.gamma =  float(gamma)
    
    self.__calculateReciprocalAngle()
    self.__calculateLatticeVolume()
    self.__calculateReciprocalBasis()
    self.__calculateReciprocalVolume()
    
    self.atoms = atoms
  
  def __calculateReciprocalAngle(self):
    self.alpha_ = _acos((cos(self.beta)*cos(self.gamma) - cos(self.alpha)) / (sin(self.beta)*sin(self.gamma)))
    self.beta_ = _acos((cos(self.alpha)*cos(self.gamma) - cos(self.beta)) / (sin(self.alpha)*sin(self.gamma)))
    self.gamma_ = _acos((cos(self.alpha)*cos(self.beta) - cos(self.gamma)) / (sin(self.alpha)*sin(self.beta)))
  
  def __calculateLatticeVolume(self):
    self.volume = self.a*self.b*self.c*sin(self.alpha_)*sin(self.beta)*sin(self.gamma)
  
  def __calculateReciprocalBasis(self):
    self.a_ = self.b*self.c*sin(self.alpha) / self.volume
    self.b_ = self.a*self.c*sin(self.beta) / self.volume
    self.c_ = self.a*self.b*sin(self.gamma) / self.volume
  
  def __calculateReciprocalVolume(self):
    self.volume_ = 1.0 / self.volume
  
  def __call__(self):
    """
    Return the lattice parameters and angle in real and reciprocal space. 
    The real and reciprocal volume are also returned.
    
    :key a, b, c: lattice parameters in :math:`\\text{angstroms}`
    :key alpha, beta, gamma: lattice angle in :math:`\\text{radians}`
    :key a*, b*, c*: reciprocal lattice parameters in :math:`\\text{angstroms}`
    :key alpha*, beta*, gamma*: reciprocal lattice angle in :math:`\\text{radians}`
    :key V: lattice volume in :math:`\\text{angstroms}^3`
    :key V*: reciprocal lattice volume in :math:`\\text{angstroms}^3`
    
    :rtype: dict
    """
    return {'a': self.a
            , 'b': self.b
            , 'c': self.c
            , 'a*': self.a_
            , 'b*': self.b_
            , 'c*': self.c_
            , 'alpha': self.alpha
            , 'beta': self.beta
            , 'gamma': self.gamma
            , 'alpha*': self.alpha_
            , 'beta*': self.beta_
            , 'gamma*': self.gamma_
            , 'V': self.volume
            , 'V*': self.volume_
            }
  
  def getAtomsPositions(self):
    """
    Return the atom positions as a list (without the atomic numbers)
    
    :rtype: list
    """
    if self.atoms != None:
      return self.atoms.keys()
    else:
      return None

if __name__ == '__main__':
  pass
  