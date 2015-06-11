#!/usr/bin/env python
"""
================================================================================
:mod:`txtFile` -- Reader of HKL Channel 5 TXT output file
================================================================================

.. module:: txtFile
   :synopsis: Reader of HKL Channel 5 TXT output file

.. inheritance-diagram:: ebsdtools.hkl.tango.txtFile

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

# Globals and constants variables.

class txt:
    def __init__(self, filepath=''):
        """
          Class is used to extract data from a ctf file
        """

        self.filepath = filepath

        #Store the CTF file in self.lines
        self.readerCTF = csv.reader(open(filepath, 'r'))
        self.lines = list(self.readerCTF)

        self.setHeader(self.lines[0])
        #Delete the title line
        del self.lines[0]

        self.setStepSize()
        self.setSize()
        self.setEDXanalyses()

    def setHeader(self, firstline):
        """
        Set the variable self.header to the header content
        """
        self.header = []

        for column in firstline:
            column = column.strip()

            if len(column) > 0:
                self.header.append(column.lower())

    def getHeader(self):
        """
        Return the header content
        
        :return: list of all the column headers
        """
        return self.header

    def setEDXanalyses(self):
        """
         Set the variable self.EDXanalyses to the number of EDX analyses 
         performed (i.e. number of elements and lines)
        """
        count = 0

        for column in self. header:
            if 'edxcount' in column:
                count += 1

        self.EDXanalyses = count

    def getEDXanalyses(self):
        """
        Return the number of EDX analyses performed (i.e. number of elements and lines)
        
        :return: integer of the number of analyses
        """
        return self.EDXanalyses

    def setStepSize(self):
        """
        Set the variable self.stepSize to the step size used for the mapping
        """
        line1 = self._resultsLinetoDict(self.lines[0])
        line2 = self._resultsLinetoDict(self.lines[1])

        self.stepSize = line2['x'] - line1['x']

    def getStepSize(self):
        """
        Return the step size used for the mapping
        
        :return: float of the step size
        """
        return self.stepSize

    def setSize(self):
        """
        Set the variable self.size to the size of the mapping
        """
        lastline = self._resultsLinetoDict(self.lines[-1])

        xSize = lastline['x'] / self.getStepSize() + 1
        ySize = lastline['y'] / self.getStepSize() + 1

        self.size = (int(xSize), int(ySize))

    def getSize(self):
        """
        Return the size of the mapping
        
        :return: tuple of the mapping size
        """
        return self.size

    def getColumnPos(self, columnName):
        """
        Return the position of a given column
          
        :arg columnName: name of the column
          
        :return: integer for the position of the column
        """
        for i, column in enumerate(self.header):
            if columnName == column:
                return i

    def getPixelResults(self, coord=(0, 0)):
        """
        Return a dictionary with the data for a given coordinate
          
        :arg coord: integer tuple (x, y)
            the coordinate starts at (0,0) and max = (xcells-1, ycells-1)

        :return: dictionary with the line info, all the keys are in lowercase
        """
        #    xPos = self.getColumnPos('x')
        #    yPos = self.getColumnPos('y')
        #    stepSize = self.getStepSize()

        linePos = coord[1] * self.getSize()[0] + coord[0]

        try:
            return self._resultsLinetoDict(self.lines[linePos])
        except:
            return {}

        #    for line in self.lines:
        #      x = int(float(line[xPos]) / float(stepSize))
        #      y = int(float(line[yPos]) / float(stepSize))
        #      
        #      if x == int(coord[0]) and y == int(coord[1]):
        #        results = self.resultsLinetoDict(line)
        #        break
        #    
        #    return results

    def _resultsLinetoDict(self, line):
        """
        Build a dictionary from the information of a given line. 
        The value are converted to the right type
          
        :arg line: list of one line from self.lines
          
        :return: All the keys are in lowercase
        """
        errorCodes = self._getErrorCodesDict()

        results = {}

        for i, column in enumerate(self.header):
            if column.lower() == 'phase':
                results.setdefault('phase', int(line[i]))
            elif column.lower() == 'x':
                results.setdefault('x', float(line[i]))
            elif column.lower() == 'y':
                results.setdefault('y', float(line[i]))
            elif column.lower() == 'euler1':
                results.setdefault('euler1', float(line[i]))
            elif column.lower() == 'euler2':
                results.setdefault('euler2', float(line[i]))
            elif column.lower() == 'euler3':
                results.setdefault('euler3', float(line[i]))
            elif column.lower() == 'mad':
                results.setdefault('mad', float(line[i]))
            elif column.lower() == 'bc':
                results.setdefault('bc', int(line[i]))
            elif column.lower() == 'bs':
                results.setdefault('bs', int(line[i]))
            elif column.lower() == 'bands':
                results.setdefault('bands', int(line[i]))
            elif column.lower() == 'error':
                results.setdefault('errorcode', int(line[i]))
                results.setdefault('error', errorCodes[int(line[i])])
            elif column.lower() == 'reliabilityindex':
                results.setdefault('reliabilityindex', float(line[i]))
            elif 'edxcount' in column.lower():
                results.setdefault(column.lower(), float(line[i]))

        return results

    def getPixelArray(self, phaseNo=0, key='euler1'):
        """
        Return a list of values for a given column header.
        If phaseNo is not equal to 0, the phase must match phaseNo
          
        :arg phaseNo: integer identifying a given phase
        :arg key: the column to be return
          
        :return: list of values
        """
        array = []

        for line in self.lines:
            lineDict = self._resultsLinetoDict(line)

            if key == None:
                value = 1
            else:
                value = lineDict[str(key).lower()]

            if phaseNo != 0:
                if lineDict['phase'] != int(phaseNo):
                    array.append(-1)
                else:
                    array.append(value)
            else:
                array.append(value)

        return array

    def _getErrorCodesDict(self):
        """
        Build a dictionary with the significance of the error code
        
        :return: dictionary with the error code and their significance
        """
        errorCodes = {}
        errorCodes.setdefault(0, 'Success')
        errorCodes.setdefault(1, 'Low band contrast')
        errorCodes.setdefault(2, 'Low band slope')
        errorCodes.setdefault(3, 'No solution')
        errorCodes.setdefault(4, 'High MAD')
        errorCodes.setdefault(5, 'Not yet analysed (job cancelled before point!)')
        errorCodes.setdefault(6, 'Unexpected error (excepts etc.)')

        return errorCodes


if __name__ == '__main__': #pragma: no cover
    txt = txt('Project10kv_5IBE_09.txt')
    print txt.getEDXanalyses()
    print txt.getStepSize()
    #  print ctf.errorCodes()

    print txt.getPixelResults((10, 0))
    #  print txt.getPixelArray(6, key='euler1')
