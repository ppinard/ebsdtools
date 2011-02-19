#!/usr/bin/env python
"""
================================================================================
:mod:`grainDetectionFile` -- Reader of HKL grain detection results
================================================================================

.. module:: grainDetectionFile
   :synopsis: Reader of HKL grain detection results

.. inheritance-diagram:: ebsdtools.hkl.tango.grainDetectionFile

"""

# Script information for the file.
__author__ = "Philippe T. Pinard"
__email__ = "philippe.pinard@gmail.com"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2010 Philippe T. Pinard"
__license__ = "GPL v3"

# Standard library modules.
import csv

# Third party modules.

# Local modules.

class grainDetectionResults:
    def __init__(self, filepath):
        """
        Reads a csv output of the grain detection results from HKL Tango.
        
        :arg filepath: location of the csv file
        :type filepath: string
        """
        reader = csv.reader(open(filepath, 'r'))

        self._results = []
        self._phases = []

        for i, line in enumerate(reader):
            if i == 0: continue

            id = int(line[0])
            phase = str(line[1])
            if not phase in self._phases:
                self._phases.append(phase)

            area = float(line[2])
            diameter = float(line[3])
            centroid = (float(line[5]), float(line[6]))
            aspectRatio = float(line[7])
            if len(line[8].strip()) > 0:
                slope = float(line[8])
            else:
                slope = None
            meanMisorientationAngle = float(line[9])
            meanMisorientationEuler1 = float(line[10])
            meanMisorientationEuler2 = float(line[11])
            meanMisorientationEuler3 = float(line[12])

            lineDict = {'id': id,
                        'phase': phase,
                        'area': area,
                        'diameter': diameter,
                        'centroid': centroid,
                        'aspect ratio': aspectRatio,
                        'slope': slope,
                        'mean misorientation angle': meanMisorientationAngle,
                        'mean misorientation euler1': meanMisorientationEuler1,
                        'mean misorientation euler2': meanMisorientationEuler2,
                        'mean misorientation euler3': meanMisorientationEuler3}

            self._results.append(lineDict)

    def eliminateNegativeSlopeGrains(self):
        """
        Eliminate all the results with negative slope.
        They correspond to small errorness grains. 
        """
        newResults = []

        for result in self._results:
            if result['slope'] != None:
                newResults.append(result)

        self._results = newResults

    def getPhasesList(self):
        """
        Return a list of the phases present in the results
        
        :rtype: list
        """
        return self._phases

    def getResults(self, **conditions):
        """
        Return the filtered results (subset) for a set of conditions.
        The results are a list of dictionary containing the following keys:
        
        ===========================    ========================================
        Key                            Description
        ===========================    ========================================
        id                             id of each grain
        phase                          phase id
        area                           area in :math:`\\mu m^2`
        diameter                       diameter in :math:`\\mu m`
        centroid                       (x, y) position of the grain centroid
        aspect ratio                   aspect ratio
        slope                          slope
        mean misorientation angle      average misorientation within the grain
        mean misorientation euler1     orientation of the grain (euler1)
        mean misorientation euler2     orientation of the grain (euler2)
        mean misorientation euler3     orientation of the grain (euler3)
        ===========================    ========================================
        
        **Parameters:**
          The conditions are given as a *tuple* where 
            * the first element is the operator (``'=', '>', '>=', '<', '<=', '!='``)
            * the second element is the value 
        
        .. note:: The greater than and less than only works with float and decimal.
        
        **Examples:**::
          
          # Return all the Al grains with an area greater than 0.5 um^2
          results = grainDetectionResults.getResults(phase=('=', 'Al'), area=('>', 0.5))
        
        :rtype: list
        """
        subsetResults = []

        for result in self._results:
            valid = True

            for condition in conditions:
                value = conditions[condition][1]
                operator = conditions[condition][0]

                if operator == '=':
                    statement = result[condition] == value
                elif operator == '>':
                    statement = result[condition] > value
                elif operator == '>=':
                    statement = result[condition] >= value
                elif operator == '<':
                    statement = result[condition] < value
                elif operator == '<=':
                    statement = result[condition] <= value
                elif operator == '!=':
                    statement = result[condition] != value

                if statement:
                    valid = True
                else:
                    valid = False
                    break

            if valid:
                subsetResults.append(result)

        return subsetResults

if __name__ == '__main__': #pragma: no cover
    grains = grainDetectionResults(r'F:\Zr\results\zr18-3\zr18-3_grains_2deg_10.csv')
    grains.eliminateNegativeSlopeGrains()

    print grains.getPhasesList()
    subset = grains.getResults(phase=('=', 'Zr Alpha'), diameter=('>', 0.1311))
    print len(subset)
