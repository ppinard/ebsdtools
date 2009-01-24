import warnings
warnings.filterwarnings('ignore') #Ignore warnings for now

from math import pi #import the constant pi
import EBSDTools.crystallography.lattice as lattice #Load the lattice class

#Create an hexagonal lattice
L = lattice.Lattice(a=3.21
                    , b=3.21
                    , c=5.21
                    , alpha=pi/2
                    , beta=pi/2
                    , gamma=120.0/180*pi
                    , atoms={(0,0,0): 14, (1/3.0, 2/3.0, 0.5): 14})

#Return information for the first 20 reflectors
reflectors = L.getReflectors().getReflectorsList()[:20]

print str("Plane").center(11), "|", str("Plane spacing").center(14), "|", "Normalized Intensity"
print '='*51

for reflector in reflectors:
  print '%2i, %2i, %2i  |  %12.10f  |  %12.10f' % (reflector[0]
                                                   , reflector[1]
                                                   , reflector[2]
                                                   , L.getReflectors().getReflectorPlaneSpacing(reflector)
                                                   , L.getReflectors().getReflectorNormalizedIntensity(reflector))
