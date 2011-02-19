#!/usr/bin/env python
"""
================================================================================
:mod:`ctfFile` -- Reader of CTF file
================================================================================

.. module:: ctfFile
   :synopsis: Reader of CTF file

.. inheritance-diagram:: ebsdtools.hkl.tango.ctfFile

"""

# Script information for the file.
__author__ = "Philippe T. Pinard"
__email__ = "philippe.pinard@gmail.com"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2010 Philippe T. Pinard"
__license__ = "GPL v3"

# Standard library modules.
import os
import csv

# Third party modules.

# Local modules.

class ctf:
    def __init__(self, filepath):
        """
        Class is used to extract data from a HKL Channel 5 ctf file
        
        :arg filepath: location of the ctf file
        :type filepath: str
        """

        self.filepath = filepath

        #Store the CTF file in self.lines
        readerCTF = csv.reader(open(filepath, 'r'), dialect='excel-tab')
        lines = list(readerCTF)

        self._parseHeader(lines)
        self._data = lines[self._firstDataLine:]
        del lines

    def _parseHeader(self, lines):
        """
        Read the header lines to get information about the acquisition and the phases
        """

        #Parse variables
        for i, line in enumerate(lines):
            if line[0] == 'Prj':
                self._projectPath = line[1]
            if line[0] == 'Author':
                self._author = line[1]
            elif line[0] == 'JobMode':
                self._jobMode = line[1]
            elif line[0] == 'XCells':
                self._xcells = int(line[1])
            elif line[0] == 'YCells':
                self._ycells = int(line[1])
            elif line[0] == 'XStep':
                self._xstep = float(line[1])
            elif line[0] == 'YStep':
                self._ystep = float(line[1])
            elif line[0] == 'AcqE1':
                self._acquisitionEuler1 = int(line[1])
            elif line[0] == 'AcqE2':
                self._acquisitionEuler2 = int(line[1])
            elif line[0] == 'AcqE3':
                self._acquisitionEuler3 = int(line[1])
            elif line[0] == 'Euler angles refer to Sample Coordinate system (CS0)!':
                for j, item in enumerate(line[1:]):
                    if item == 'Mag':
                        self._magnification = int(line[j + 2])
                    elif item == 'Coverage':
                        self._coverage = int(line[j + 2])
                    elif item == 'Device':
                        self._device = int(line[j + 2])
                    elif item == 'KV':
                        self._acceleratingVoltage = float(line[j + 2])
                    elif item == 'TiltAngle':
                        self._tiltAngle = float(line[j + 2])
                    elif item == 'TiltAxis':
                        self._tiltAxis = int(line[j + 2])
            elif line[0] == 'Phases':
                self._numberPhases = int(line[1])
                self._firstPhaseLine = i + 1
            elif line[0] == 'Phase':
                self._firstDataLine = i + 1
                break

        #Parse phases
        self._phases = {}
        for id, line in enumerate(lines[self._firstPhaseLine : self._firstPhaseLine + self._numberPhases]):
            id += 1 #The first phase is 1
            self._phases.setdefault(id, {})
            self._phases[id]['id'] = id

            latticeParameters = line[0].split(';')
            self._phases[id]['cell_length_a'] = float(latticeParameters[0])
            self._phases[id]['cell_length_b'] = float(latticeParameters[1])
            self._phases[id]['cell_length_c'] = float(latticeParameters[2])

            latticeAngles = line[1].split(';')
            self._phases[id]['cell_angle_alpha'] = float(latticeAngles[0])
            self._phases[id]['cell_angle_beta'] = float(latticeAngles[1])
            self._phases[id]['cell_angle_gamma'] = float(latticeAngles[2])

            self._phases[id]['chemical_name_mineral'] = line[2]

            self._phases[id]['symmetry_Int_Tables_number'] = int(line[4])

            self._phases[id]['publ_author_name'] = line[7]

    def getProjectName(self):
        """
        Return the name of the project (No .cpr or .ctf) from the information stored in the ctf.
        
        :rtype: str
        """
        return self._projectPath.split('\\')[-1].split('.')[0]

    def getProjectFolderName(self):
        """
        Return the immediate folder where the project is located from the information stored in the ctf.
        
        :rtype: str
        """
        return self._projectPath.split('\\')[-2]

    def getProjectFolderPath(self):
        """
        Return the full path of the folder where the project is located from the information stored in the ctf.
        
        :rtype: str
        """
        return os.path.normpath('/'.join(self._projectPath.split('\\')[:-1]))

    def getProjectImagesFolderName(self):
        """
        Return the folder name where the project images are located from the information stored in the ctf.
        
        :rtype: str
        """
        return '%sImages' % self.getProjectFolderName()

    def getProjectImagesFolderPath(self):
        """
        Return the full path of the folder where the project images are located from the information stored in the ctf.
        
        :rtype: str
        """
        return os.path.normpath(os.path.join(self.getProjectFolderPath(), '%sImages' % self.getProjectName()))

    def getAuthor(self):
        """
        Return the author
        
        :rtype: str
        """
        return self._author

    def getJobMode(self):
        """
        Return the job mode
        
        :rtype: str
        """
        return self._jobMode

    def getXCells(self):
        """
        Return the number of points in the X direction [units=px]
        
        :rtype: int
        """
        return self._xcells

    def getYCells(self):
        """
        Return the number of points in the Y direction [units=px]
        
        :rtype: int
        """
        return self._ycells

    def getSize(self):
        """
        Return the number of points in the mapping [units=px]
        
        :rtype: int
        """
        return self._xcells * self._ycells

    def getWidth(self):
        """
        Return the width of mapping (points in ) [units=px]
        
        :rtype: int
        """
        return self._xcells

    def getHeight(self):
        """
        Return the height of mapping (points in Y) [units=px]
        
        :rtype: int
        """
        return self._ycells

    def getXStep(self):
        """
        Return the size of the step in the X direction [units= :math:`\\mu m`]
        
        :rtype: float
        """
        return self._xstep

    def getYStep(self):
        """
        Return the size of the step in the Y direction [units= :math:`\\mu m`]
        
        :rtype: float
        """
        return self._ystep

    def getAcquisitionEuler1(self):
        """
        Return the acquisition euler angle (:math:`\\theta_1`) [units=deg]
        
        :rtype: float
        """
        return self._acquisitionEuler1

    def getAcquisitionEuler2(self):
        """
        Return the acquisition euler angle (:math:`\\theta_2`) [units=deg]
        
        :rtype: float
        """
        return self._acquisitionEuler2

    def getAcquisitionEuler3(self):
        """
        Return the acquisition euler angle (:math:`\\theta_3`) [units=deg]
        
        :rtype: float
        """
        return self._acquisitionEuler3

    def getAcquisitionEulers(self):
        """
        Return the acquisition euler angles :math:`(\\theta_1, \\theta_2, \\theta_3)` [units=deg]
        
        :rtype: float
        """
        return (self._acquisitionEuler1, self._acquisitionEuler2, self._acquisitionEuler3)

    def getMagnification(self):
        """
        Return the magnification [units=X]
        
        :rtype: float
        """
        return self._magnification

    def getCoverage(self):
        return self._coverage

    def getDevice(self):
        return self._device

    def getAcceleratingVoltage(self):
        """
        Return the accelerating voltage [units=kV]
        
        :rtype: float
        """
        return self._acceleratingVoltage

    def getTiltAngle(self):
        """
        Return the tilt angle [units=deg]
        
        :rtype: float
        """
        return self._tiltAngle

    def getTiltAxis(self):
        """
        Return the tilt axis
        
        :rtype: int
        """
        return self._tiltAxis

    def getNumberPhases(self):
        """
        Return the number of phases
        
        :rtype: int
        """
        assert self._numberPhases == len(self._phases)
        return self._numberPhases

    def getPhases(self, id=None):
        """
        Return the dictionary of a given phase *id* or the whole phase dictionary if ``id == None``
        
        :arg id: id of the phase (the first phase has ``id == 1``)
        :type id: int
        
        :rtype: dict
        """
        if id == None:
            return self._phases
        else:
            return self._phases[id]

    def getPhasesList(self):
        """
        Return a list with all the phases name.
        
        :rtype: list
        """
        phasesList = []

        for phaseId in self._phases:
            phasesList.append(self.getPhaseName(phaseId))

        return phasesList

    def getPhaseName(self, id):
        """
        Return the phase of a given phase *id*
        
        :arg id: id of the phase (the first phase has ``id == 1``)
        :type id: int
        
        :rtype: str
        """
        return self._phases[id]['chemical_name_mineral']

    def getPhaseLatticeParameterA(self, id):
        """
        Return the lattice parameter a of a given phase *id* [units=:math:`\\text{angstroms}`]
        
        :arg id: id of the phase (the first phase has ``id == 1``)
        :type id: int
        
        :rtype: float
        """
        return self._phases[id]['cell_length_a']

    def getPhaseLatticeParameterB(self, id):
        """
          Return the lattice parameter b of a given phase *id* [units=:math:`\\text{angstroms}`]
        
        :arg id: id of the phase (the first phase has ``id == 1``)
        :type id: int
        
        :rtype: float
        """
        return self._phases[id]['cell_length_b']

    def getPhaseLatticeParameterC(self, id):
        """
          Return the lattice parameter c of a given phase *id* [units=:math:`\\text{angstroms}`]
        
        :arg id: id of the phase (the first phase has ``id == 1``)
        :type id: int
        
        :rtype: float
        """
        return self._phases[id]['cell_length_c']

    def getPhaseLatticeParameters(self, id):
        """
        Return the lattice parameters of a given phase *id* [units=:math:`\\text{angstroms}`]
        
        :arg id: id of the phase (the first phase has ``id == 1``)
        :type id: int
        
        :rtype: (float(a), float(b), float(c))
        """
        return (self._phases[id]['cell_length_a'], self._phases[id]['cell_length_b'], self._phases[id]['cell_length_c'])

    def getPhaseLatticeAngleAlpha(self, id):
        """
        Return the lattice angle :math:`\\alpha` of a given phase *id* [units=deg]
        
        :arg id: id of the phase (the first phase has ``id == 1``)
        :type id: int
        
        :rtype: float
        """
        return self._phases[id]['cell_angle_alpha']

    def getPhaseLatticeAngleBeta(self, id):
        """
        Return the lattice angle :math:`\\beta` of a given phase *id* [units=deg]
        
        :arg id: id of the phase (the first phase has ``id == 1``)
        :type id: int
        
        :rtype: float
        """
        return self._phases[id]['cell_angle_beta']

    def getPhaseLatticeAngleGamma(self, id):
        """
        Return the lattice angle :math:`\\gamma` of a given phase *id* [units=deg]
        
        :arg id: id of the phase (the first phase has ``id == 1``)
        :type id: int
        
        :rtype: float
        """
        return self._phases[id]['cell_angle_gamma']

    def getPhaseLatticeAngles(self, id):
        """
        Return the lattice angles of a given phase *id* [units=deg]
        
        :arg id: id of the phase (the first phase has ``id == 1``)
        :type id: int
        
        :rtype: (float(:math:`\\alpha`), float(:math:`\\beta`), float(:math:`\\gamma`))
        """
        return (self._phases[id]['cell_angle_alpha'], self._phases[id]['cell_angle_beta'], self._phases[id]['cell_angle_gamma'])

    def getPhaseSpaceGroupNo(self, id):
        """
        Return the space group no. of a given phase
        
        :arg id: id of the phase (the first phase has ``id == 1``)
        :type id: int
        
        :rtype: int between [1, 230]
        """
        return self._phases[id]['symmetry_Int_Tables_number']

    def getNumberPixels(self):
        """
        Return the number of pixels in the map
        
        :rtype: int
        """
        return len(self._data)

    def getPixelIndex(self, coord):
        """
        Return the index of the pixel which also represents the image number of that pixel.
        The pixel (0,0) has an index of 1.
        
        :arg coord: a integer tuple (x, y) between
        
          * :math:`0 < x <= (\\text{XCells} - 1)`
          * :math:`0 < y <= (\\text{YCells} - 1)`
        
        :type coord: tuple
        
        :rtype: int
        """
        return coord[0] + coord[1] * self.getXCells() + 1

    def getPixelCoordinate(self, index):
        """
        Return the coordinate of the pixel from its index.
        The pixel (0,0) has an index of 1.
        
        :arg index: the index of the pixel
        :type index: int
        
        :rtype: a integer tuple (x, y)
        """
        index -= 1
        y = index / self.getWidth()
        x = index - (y * self.getWidth())

        assert 0 <= y < self.getHeight()
        assert 0 <= x < self.getWidth()

        return x, y

    def getPixelIndexLabel(self, **data):
        """
        Return the label of the index of the pixel which also represents the image number of that pixel.
        The pixel (0,0) has an index of 1.
        The number of zero before the index is asjusted accordingly to the maximum index.
        
        :arg coord: a integer tuple (x, y) between
        
          * :math:`0 < x <= (\\text{XCells} - 1)`
          * :math:`0 < y <= (\\text{YCells} - 1)`
        
        :type coord: tuple
        
        :rtype: str
        """
        if 'coord' in data.keys():
            index = self.getPixelIndex(data['coord'])
        elif 'index' in data.keys():
            index = data['index']

        width = len(str(self.getNumberPixels()))
        imageNumber = str(index).zfill(width)

        return imageNumber

    def getPixelImageLabel(self, **data):
        """
        Return the filename of the pixel image (diffraction pattern).
        
        :arg coord: a integer tuple (x, y) between
        
          * :math:`0 < x <= (\\text{XCells} - 1)`
          * :math:`0 < y <= (\\text{YCells} - 1)`
        
        :type coord: tuple
        
        :arg index: index of the pixel
        :type index: int
        
        :rtype: string
        """
        projectName = self.getProjectName()
        imageNumber = self.getPixelIndexLabel(**data)

        return '%s%s' % (projectName, imageNumber)

    def getPixelResults_coordinate(self, coord):
        """
        Return a dictionary with the data for a given coordinate.
        
        ==========   =================================================
        key          Description
        ==========   =================================================
        phase        id of the phase (the first phase has ``id == 1``)
        x            x position of the pixel
        y            y position of the pixel
        bands        number of bands used in the indexation
        errorcode    see below
        error        explanation of the *errorcode*
        euler1       first euler angle (Bunge convention)
        euler2       second euler angle (Bunge convention)
        euler3       third euler angle (Bunge convention)
        mad          mean angular deviation
        bc           band contrast
        bs           band slope
        ==========   =================================================
        
        ==========   =================================================
        errorcode    Description
        ==========   =================================================
        0            Success
        1            Low band contrast
        2            Low band slope
        3            No solution
        4            High MAD
        5            Not yet analysed (job cancelled before point!)
        6            Unexpected error (excepts etc.)
        ==========   =================================================
        
        :arg coord: a integer tuple (x, y) between
        
          * :math:`0 < x <= (\\text{XCells} - 1)`
          * :math:`0 < y <= (\\text{YCells} - 1)`
        
        :type coord: tuple
        
        :rtype: dict
        """
        lineNo = coord[0] + coord[1] * self.getXCells()
        if lineNo < len(self._data):
            return self._resultsLinetoDict(self._data[lineNo])
        else:
            return {}

    def getPixelResults_index(self, index):
        """
        Return a dictionary with the data for a given index.
        
        .. seealso: :func:`getPixelResults_coordinate <ctf.getPixelResults_coordinate>`
        
        :arg index: the index of the pixel
        :type index: int
        
        :rtype: dict
        """
        if index - 1 < len(self._data):
            return self._resultsLinetoDict(self._data[index - 1])
        else:
            return {}

    def _resultsLinetoDict(self, line):
        """
        Build a dictionary from the information of a given line.
        All the keys are in lowercase.
        The value are converted to the right type.
        
        :arg line: list of values
        
        :rtype: dict
        """

        errorCodes = self._getErrorCodesDict()

        results = {}

        results.setdefault('phase', int(line[0]))
        results.setdefault('x', float(line[1]))
        results.setdefault('y', float(line[2]))
        results.setdefault('bands', int(line[3]))
        results.setdefault('errorcode', int(line[4]))
        results.setdefault('error', errorCodes[int(line[4])])
        results.setdefault('euler1', float(line[5]))
        results.setdefault('euler2', float(line[6]))
        results.setdefault('euler3', float(line[7]))
        results.setdefault('mad', float(line[8]))
        results.setdefault('bc', int(line[9]))
        results.setdefault('bs', int(line[10]))

        return results

    def getPixelArray(self, key='euler1', noneValue=None, **conditions):
        """
        Return the filtered list for a given column header *key* and a set of conditions.
        The pixels that don't respect the condition(s) have a value of *noneValue*.
        
        **Parameters:**
          *key*: name of the columns. Refer to :func:`getPixelResults() <HKLChannel5Tools.Tango.ctfFile.ctf.getPixelResults>` for list of keys.
        
          The conditions are given as a *tuple* where
            * the first element is the operator (``'=', '>', '>=', '<', '<=', '!='``)
            * the second element is the value
        
        .. note:: The greater than and less than only works with float and decimal.
        
        **Examples:**::
        
          # Return a array of band contrast for pixels of only the second phase
          # and that have a band contrast higher than 50
          pixArray = ctf.getPixelArray(key='bc', phase=('=', 2), bc=('>', 50)))
        
        :rtype: list
        """
        pixArray = []

        for line in self._data:
            lineDict = self._resultsLinetoDict(line)
            valid = True

            for condition in conditions:
                value = conditions[condition][1]
                operator = conditions[condition][0]

                if operator == '=':
                    statement = lineDict[condition] == value
                elif operator == '>':
                    statement = lineDict[condition] > value
                elif operator == '>=':
                    statement = lineDict[condition] >= value
                elif operator == '<':
                    statement = lineDict[condition] < value
                elif operator == '<=':
                    statement = lineDict[condition] <= value
                elif operator == '!=':
                    statement = lineDict[condition] != value

                if statement:
                    valid = True
                else:
                    valid = False
                    break

            if valid:
                pixArray.append(lineDict[key])
            else:
                pixArray.append(noneValue)

        return pixArray

    getPixArray = getPixelArray

    def _getErrorCodesDict(self):
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
    ctf = ctf('test_ctfFile.ctf')
    print len(ctf.getPixelArray(key='bc', phase=('=', 2), bc=('>', 50)))
