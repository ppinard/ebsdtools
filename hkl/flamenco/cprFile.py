#!/usr/bin/env python
"""
================================================================================
:mod:`cprFile` -- Reader and writer of CPR file
================================================================================

.. module:: cprFile
   :synopsis: Reader and writer of CPR file

.. inheritance-diagram:: ebsdtools.hkl.flamenco.cprFile

"""

# Script information for the file.
__author__ = "Philippe T. Pinard"
__email__ = "philippe.pinard@gmail.com"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2010 Philippe T. Pinard"
__license__ = "GPL v3"

# Standard library modules.
import ConfigParser

# Third party modules.

# Local modules.

class cpr:
    defaultParameters = {'ProjectionParameters': {
                      'vhratio': ["float", None, 0, None],
                      'pcx': ["float", None, 0, None],
                      'pcy': ["float", None, -1, None],
                      'dd': ["float", None, 0.1, None]},
                    'SEMFields': {
                      'doeuler1': ["float", 357.95000, 0, 360],
                      'doeuler2': ["float", 89.94500, 0, 180],
                      'doeuler3': ["float", 0.39900, 0, 360]},
                    'AOI2DHough': {
                      'x0': ["integer", None, 0, None],
                      'y0': ["integer", None, 0, None],
                      'r': ["integer", None, 30, None]},
                    'AOI3DHough': {
                      'left': ["integer", 0, 0, 1340],
                      'top': ["integer", 0, 0, 1023],
                      'right': ["integer", 1340, 0, 1340],
                      'bottom': ["integer", 1023, 0, 1023]},
                    'Band Detection': {
                      'detect': ["integer", 1, 0, 3],
                      'divergence': ["integer", 1, 0, 2],
                      'min': ["integer", None, 3, None],
                      'max': ["integer", None, 3, None],
                      'houghres': ["integer", None, 15, 125],
                      'olocklevel': ["integer", None, 1, 4],
                      'usebandwidth': ["bool", 'False', None, None],
                      'olock': ["bool", None, None, None]},
                    'Discriminators': {
                      'bc': ["integer", None, 0, 255],
                      'bs': ["integer", None, 0, 255],
                      'mad': ["float", None, 0, 5]},
                    'Live EBSP': {
                      'delay': ["integer", 0, None, None],
                      'mintimeperframe': ["integer", None, 0, 1000],
                      'backgroundmode': ["integer", None, 0, 1],
                      'autobackgroundlevel': ["float", None, None, None],
                      'noframesbackground': ["integer", None, 1, None],
                      'noframes': ["integer", None, 1, 256],
                      'lowerlimit': ["float", None, None, None],
                      'upperlimit': ["float", None, None, None],
                      'insoftware': ["bool", None, None, None],
                      'backgroundcorron': ["bool", None, None, None],
                      'autobackgroundon': ["bool", None, None, None],
                      'autostretch': ["bool", None, None, None]},
                    'FG_DCam parameters': {
                      'binning': ["string", "4x4 binning", None, None],
                      'gain': ["string", "High", None, None]},
                    'Image Compression': {
                      'method': ["integer", 0, 0, 0],
                      'quality': ["float", 100.0, 0.0, 100.0],
                      'smoothing': ["integer", 0, 0, 5],
                      'nonvisibleblack': ["integer", 1, 0, 1],
                      'savewhen': ["integer", 2, 0, 3],
                      'percentage': ["float", 100.0, 0.0, 100.0]},
                    'Phases': {
                      'noreflectors': ["integer", 37, 0, 30000],
                      'count': ["integer", None, 0, None]},
                    'StagePosition': {
                      'xpos': ["float", None, None, None],
                      'ypos': ["float", None, None, None],
                      'zpos': ["float", None, None, None],
                      'rpos': ["float", None, 0, 360],
                      'tpos': ["float", None, None, None],
                      'zvalid': ["bool", False, None, None]},
                    'EDX Control': {
                      'mappingenabled': ["bool", 'False', None, None],
                      'mincycletime': ["integer", 200, 0, None],
                      'windowcount': ["integer", 0, 0, None]},
                    'Job': {
                      'top': ["float", None, None, None],
                      'left': ["float", None, None, None],
                      'coverage': ["integer", 100, None, None],
                      'magnification': ["integer", None, 25, 500000],
                      'kv': ["float", None, 0.1, 40],
                      'workingdistance': ["float", 20.0, 5.0, 30.0],
                      'tiltangle': ["float", 70, 0, 90],
                      'tiltaxis': ["float", 0, None, None],
                      'device': ["string", "None", None, None],
                      'griddistx': ["float", None, None, None],
                      'griddisty': ["float", None, None, None],
                      'xcells': ["integer", None, None, None],
                      'ycells': ["integer", None, None, None],
                      'automatic': ["bool", 'True', None, None],
                      'noofpoints': ["integer", None, None, None]},
                    'EDX Windows': {
                      'count': ["integer", None, 0, None]},
                    'General': {
                      'version': ["float", 5.0, None, None],
                      'date': ["string", None, None, None],
                      'time': ["string", None, None, None],
                      'duration': ["string", None, None, None],
                      'percycle': ["string", None, None, None],
                      'description': ["string", None, None, None],
                      'author': ["string", None, None, None],
                      'notes': ["string", None, None, None],
                      'jobmode': ["string", "RegularGrid", None, None],
                      'samplesymmetry': ["integer", 2, None, None]},
                    'Acquisition Surface': {
                      'euler1': ["float", 0, 0, 360],
                      'euler2': ["float", 0, 0, 180],
                      'euler3': ["float", 0, 0, 360]},
                    'Fields': {
                      'count': ["integer", 9, None, None],
                      'field1': ["integer", 3, None, None],
                      'field2': ["integer", 4, None, None],
                      'field3': ["integer", 5, None, None],
                      'field4': ["integer", 6, None, None],
                      'field5': ["integer", 7, None, None],
                      'field6': ["integer", 8, None, None],
                      'field7': ["integer", 10, None, None],
                      'field8': ["integer", 11, None, None],
                      'field9': ["integer", 12, None, None]},
                    'References': {
                      'originalprojectname': ["string", None, None, None],
                      'imagestoragefolder': ["string", None, None, None]}
                  }

    def __init__(self, filepath):
        self.filepath = filepath

        self.parser = ConfigParser.RawConfigParser()
        fileCPR = open(filepath, 'r')
        self.parser.readfp(fileCPR)
        fileCPR.close()

        self.crossRef('FG_DCam parameters', 'binning', self.getParameter('FG_DCam parameters', 'binning'))
        self.crossRef('Job', 'griddistx', self.getParameter('Job', 'griddistx'))
        self.crossRef('Job', 'griddisty', self.getParameter('Job', 'griddisty'))
        self.crossRef('Job', 'xcells', self.getParameter('Job', 'xcells'))
        self.crossRef('Job', 'ycells', self.getParameter('Job', 'ycells'))

    def write(self, filepath=None):
        if filepath == None:
            filepath = self.filepath

        newCprFile = open(filepath, 'w')
        self.parser.write(newCprFile)

    def validateMinMax(self, section, option, value):
        parameter = self.defaultParameters[section][option.lower()]

        if value != None and value != '' :
            if parameter[0] == 'float':
                if parameter[2] != None and parameter[3] != None:
                    if float(value) >= parameter[2] and float(value) <= parameter[3]:
                        return True,
                    else:
                        return False, 'Not in the value range (' + str(parameter[1]) + ', ' + str(parameter[3]) + ')'
                elif parameter[2] == None and parameter[3] != None:
                    if float(value) <= parameter[3]:
                        return True,
                    else:
                        return False, 'Above the maximum value  (' + str(parameter[3]) + ')'
                elif parameter[2] != None and parameter[3] == None:
                    if float(value) >= parameter[2]:
                        return True,
                    else:
                        return False, 'Below the minimum value  (' + str(parameter[2]) + ')'
            elif parameter[0] == 'integer':
                if parameter[2] != None and parameter[3] != None:
                    if int(value) >= parameter[2] and int(value) <= parameter[3]:
                        return True,
                    else:
                        return False, 'Not in the value range (' + str(parameter[1]) + ', ' + str(parameter[3]) + ')'
                elif parameter[2] == None and parameter[3] != None:
                    if int(value) <= parameter[3]:
                        return True,
                    else:
                        return False, 'Above the maximum value  (' + str(parameter[3]) + ')'
                elif parameter[2] != None and parameter[3] == None:
                    if int(value) >= parameter[2]:
                        return True,
                    else:
                        return False, 'Below the minimum value  (' + str(parameter[2]) + ')'
            elif parameter[0] == 'bool':
                if str(value).lower() == 'true' or str(value).lower() == 'false':
                    return True,
                else:
                    return False, "Value not boolean"

        return True, "Not validable"


    def validateSpecial(self, section, option, value):
        if value != None and value != '' :
            if section == "FG_DCam parameters":
                if option.lower() == "binning":
                    if value == "No binning" or value == "2x2 binning" or value == "4x4 binning" or value == "8x8 binning" or value == "8x8 superfast":
                        return True,
                    else:
                        return False, "Invalid Binning"
                if option.lower() == "gain":
                    if value == "Low" or value == "High":
                        return True,
                    else:
                        return False, "Invalid Gain"

        return True, "Not validable"

    def crossRef(self, section, option, value):
        """
        Modify the options that are linked together
        The section, option, value in the parameters are those that provokes the modification to other options
        """
        if section == "FG_DCam parameters":
            if option.lower() == "binning":
                if value == "No binning":
                    right = 1340
                    bottom = 1023
                    radius = 750
                elif value == "2x2 binning":
                    right = 670
                    bottom = 510
                    radius = 375
                elif value == "4x4 binning":
                    right = 335
                    bottom = 255
                    radius = 187
                elif value == "8x8 binning" or value == "8x8 superfast":
                    right = 167
                    bottom = 128
                    radius = 94
                else:
                    right = 0
                    bottom = 0
                    radius = 30

                self.defaultParameters["AOI3DHough"]["right"][1] = right
                self.defaultParameters["AOI3DHough"]["bottom"][1] = bottom
                self.defaultParameters["AOI3DHough"]["right"][3] = right
                self.defaultParameters["AOI3DHough"]["bottom"][3] = bottom
                self.defaultParameters["AOI3DHough"]["left"][3] = right
                self.defaultParameters["AOI3DHough"]["top"][3] = bottom
                self.defaultParameters["AOI2DHough"]["r"][3] = radius

                if not self.validateMinMax("AOI3DHough", "right", self.getParameter("AOI3DHough", "right"))[0] == True:
                    self.setParameter("AOI3DHough", "right", self.defaultParameters["AOI3DHough"]["right"][3])
                if not self.validateMinMax("AOI3DHough", "bottom", self.getParameter("AOI3DHough", "bottom"))[0] == True:
                    self.setParameter("AOI3DHough", "bottom", self.defaultParameters["AOI3DHough"]["bottom"][3])
                if not self.validateMinMax("AOI3DHough", "left", self.getParameter("AOI3DHough", "left"))[0] == True:
                    self.setParameter("AOI3DHough", "left", self.defaultParameters["AOI3DHough"]["left"][3])
                if not self.validateMinMax("AOI3DHough", "top", self.getParameter("AOI3DHough", "top"))[0] == True:
                    self.setParameter("AOI3DHough", "top", self.defaultParameters["AOI3DHough"]["top"][3])
                if not self.validateMinMax("AOI2DHough", "r", self.getParameter("AOI2DHough", "r"))[0] == True:
                    self.setParameter("AOI2DHough", "r", self.defaultParameters["AOI2DHough"]["r"][3])

        elif section == "Job":
            if option.lower() == "griddistx":
                try:
                    newValue = self.getParameter("Job", "griddistx")
                except:
                    newValue = ''

                self.setParameter("Job", "griddisty", newValue)
            elif option.lower() == "xcells":
                try:
                    newValue = self.getParameter("Job", "xcells") * self.getParameter("Job", "ycells")
                except:
                    newValue = ''
                self.setParameter("Job", "noofpoints", newValue)
            elif option.lower() == "ycells":
                try:
                    newValue = self.getParameter("Job", "xcells") * self.getParameter("Job", "ycells")
                except:
                    newValue = ''
                self.setParameter("Job", "noofpoints", newValue)

        return True,

    def valueToParameter(self, section, option, value):
        values = []

        if section == "Band Detection":
            if option.lower() == 'detect':
                values = ['Band Centers', 'Band Edges', 'Adaptive', 'Enhanced Adaptive']
            elif option.lower() == 'divergence':
                values = ['Low', 'Standard', 'High']
        elif section == "Live EBSP":
            if option.lower() == 'backgroundmode':
                values = ['Substract', 'Divide']
        elif section == "Image Compression":
            if option.lower() == 'savewhen':
                values = ['Do not save', "Save if can't index", 'Save %', "Save all and don't index"]

        if value in values:
            return values.index(value)
        else:
            return value

    def parameterToValue(self, section, option, value):
        values = []

        if section == "Band Detection":
            if option.lower() == 'detect':
                values = ['Band Centers', 'Band Edges', 'Adaptive', 'Enhanced Adaptive']
            elif option.lower() == 'divergence':
                values = ['Low', 'Standard', 'High']
        elif section == "Live EBSP":
            if option.lower() == 'backgroundmode':
                values = ['Substract', 'Divide']
        elif section == "Image Compression":
            if option.lower() == 'savewhen':
                values = ['Do not save', "Save if can't index", 'Save %', "Save all and don't index"]

        if len(values) > 0 and value < len(values) and value >= 0:
            return values[int(value)]
        else:
            return value

    def getParameter(self, section, option):
        try:
            value = self.parser.get(section, option.lower())
        except:
            value = None

        return self.parameterToValue(section, option.lower(), self.formatValue(section, option.lower(), value))


    def setParameter(self, section, option, value):
        value = self.valueToParameter(section, option.lower(), value)

        validateSpecial = self.validateSpecial(section, option, value)
        validateMinMax = self.validateMinMax(section, option, value)

        if validateSpecial[0]:
            if validateMinMax[0]:
                try:
                    self.parser.set(section, option.lower(), self.formatValue(section, option.lower(), value))
                except ConfigParser.NoSectionError:
                    return False,
                else:
                    self.crossRef(section, option, value)
                    return True,
            else:
                return False, "validateMinMax: " + str(validateMinMax[1])
        else:
            return False, "validateSpecial: " + str(validateSpecial[1])

    def formatValue(self, section, option, value):
        type = self.defaultParameters[section][option.lower()][0]

        if value != '' and value != None:
            if type == "float":
                return float(value)
            elif type == "integer":
                return int(value)
            elif type == "bool":
                return str(value)
            elif type == "string":
                return str(value)
            else:
                return value
        else:
            return ''

    def getCprDict(self):
        cprDict = {}

        for section in self.parser.sections():
            cprDict.setdefault(section, {})

            options = self.parser.items(section)

            for option, value in options:
                cprDict[section].setdefault(option.lower(), value)

        return cprDict

if __name__ == '__main__': #pragma: no cover
    cpr = cpr()

    #  print cpr.getCprDict()

    print cpr.valueToParameter("Band Detection", "Detect", "Adaptive")
    print cpr.parameterToValue("Band Detection", "Detect", 3)
    #  
    #  print cpr.getCprDict()

    cpr.write("TextXray_2.cpr")

