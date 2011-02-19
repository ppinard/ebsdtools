#!/usr/bin/env python
"""
================================================================================
:mod:`cprGUI` -- GUI to edit CPR files
================================================================================

.. module:: cprGUI
   :synopsis: GUI to edit CPR files

.. inheritance-diagram:: ebsdtools.hkl.flamenco.cprGUI

"""

# Script information for the file.
__author__ = "Philippe Pinard (philippe.pinard@gmail.com)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2008-2009 Philippe Pinard"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = ""
__svnDate__ = ""
__svnId__ = ""

# Standard library modules.
import sys
import platform
import os.path
import Tkinter
import tkFileDialog
import tkMessageBox
import ConfigParser

# Third party modules.

# Local modules.
import tkintertools.Pmw.Pmw as Pmw

from guitools.py2exe import get_main_dir, main_is_frozen

import ebsdtools.hkl.flamenco.cprFile as cprFile

def validator(section, option):
    """
    Create the validator dictionary based on the default parameters of the cprFile module
    """
    parameter = cprFile.cpr.defaultParameters[section][option.lower()]

    validationDict = {}

    #Type
    if parameter[0] == 'float':
        validator = 'real'
    elif parameter[0] == 'integer':
        validator = 'integer'
    elif parameter[0] == 'bool':
        validator = 'alphabetic'
    elif parameter[0] == 'string':
        return {}
    else:
        return {}

    validationDict.setdefault('validator', validator)

    #Min
    if parameter[2] != None:
        min = parameter[2]
        validationDict.setdefault('min', min)
        validationDict.setdefault('minstrict', False)

    #Max
    if parameter[3] != None:
        max = parameter[3]
        validationDict.setdefault('max', max)
        validationDict.setdefault('maxstrict', False)

    return validationDict

def validatorBalloon(validationDict):
    """
    Create a string explaining the validator
    """
    str = ''

    for key in validationDict.keys():
        if key == 'min' or key == 'max' or key == 'validator':
            str += '%s: %s, ' % (key, validationDict[key])

    return str[:-2]

def readConfiguration(configfilepath='cprGUI.ini'):
    """
    Read configuration file and return a dictionary with the inputs
    """
    if os.path.exists(configfilepath):
        parser = ConfigParser.SafeConfigParser()
        file = open(configfilepath, 'r')
        parser.readfp(file)
        file.close()

        config = {}

        if parser.has_section("InitialDir"):
            if parser.has_option("InitialDir", "LoadDirectory"):
                config.setdefault("LoadDirectory", parser.get("InitialDir", "LoadDirectory"))

        if parser.has_section("InitialDir"):
            if parser.has_option("InitialDir", "SaveDirectory"):
                config.setdefault("SaveDirectory", parser.get("InitialDir", "SaveDirectory"))

        if parser.has_section("Tabs"):
            if parser.has_option("Tabs", "Visible"):
                config.setdefault("Tabs", parser.get("Tabs", "Visible").split())

        return config
    else:
        tkMessageBox.showwarning(title='File not found'
                                , message='Could not found ' + str(configfilepath) + ' in the root directory. The default values will be used')
        return {}

class App(Tkinter.Toplevel):
    def __init__(self, master, masterCprFile, loadDir, saveDir):
        self.cpr = cprFile.cpr(filepath=masterCprFile)
        self.masterCprFile = masterCprFile

        self.app = self

        self.widgets = {}
        self.root = master

        self.filepath = Tkinter.StringVar()
        self.currentLoadDirectory = loadDir
        self.currentSaveDirectory = saveDir

        btnLoad = Tkinter.Button(master, text="Load", command=self.load)
        btnLoad.grid(row=0, column=0, sticky=Tkinter.EW)

        btnSave = Tkinter.Button(master, text="Save", command=self.save)
        btnSave.grid(row=0, column=1, sticky=Tkinter.EW)

        btnSaveAs = Tkinter.Button(master, text="Save As", command=self.saveAs)
        btnSaveAs.grid(row=0, column=2, sticky=Tkinter.EW)

        btnDisplay = Tkinter.Button(master, text="Clear", command=self.clearAllValues)
        btnDisplay.grid(row=0, column=3, sticky=Tkinter.EW)

        btnExit = Tkinter.Button(master, text="Exit", command=self.exit)
        btnExit.grid(row=0, column=4, sticky=Tkinter.EW)

        lblFilename = Tkinter.Label(master, textvariable=self.filepath)
        lblFilename.grid(row=1, column=0, columnspan=5, sticky=Tkinter.NS)

        self.notebook = Pmw.NoteBook(master, lowercommand=lambda event, func=self.updateChangeTab: func(event))
        self.notebook.grid(row=2, column=0, columnspan=5, sticky=Tkinter.NS)

    def addTab(self, title):
        """
        Add a tab to the notebook
        """
        tab = self.notebook.add(title)
        self.notebook.update()
        return tab

    def updateNotebook(self):
        """
        Update the notebook dimensions after all the widgets are created
        """
        self.notebook.setnaturalsize()

    def updateWidgets(self, widgets):
        """
        Add a serie of widgets to the global dictionary self.widgets
        """
        self.widgets.update(widgets)

    def updateChangeTab(self, event=None):
        """
        Action called when the user changes tab
        """
        self.saveAllValues()

    def saveValue(self, event=None, widgetName=None, widget=None):
        """
        Save the value of a widget when it is focused out
        """
        if event:
            self.app.cpr.setParameter(widget['section'], widget['option'].lower(), widget['object'].getvalue())

        self.updateAllValues()

    def saveAllValues(self):
        """
        Save the value of all the widgets
        """
        for widget in self.widgets:
            if 'section' in self.widgets[widget].keys():
                self.app.cpr.setParameter(self.widgets[widget]['section']
                                  , self.widgets[widget]['option'].lower()
                                  , self.widgets[widget]['object'].getvalue())

        self.updateAllValues()

    def clearAllValues(self):
        """
        Clear all the values by loading the default cprmaster.cpr
        """
        if os.path.exists(self.masterCprFile):
            self.filepath.set('')
            self.cpr = cprFile.cpr(self.masterCprFile)
            self.updateAllValues()
        else:
            tkMessageBox.showwarning(title='File not found'
                                   , message='Could not found cprmaster.cpr in the root directory. The values cannot be cleared.')

    def updateAllValues(self):
        """
        Update the values of the different widgets
        Specific actions for certain widgets since they are linked together
        """
        for widget in self.widgets:
            if 'section' in self.widgets[widget].keys():
                value = self.app.cpr.getParameter(self.widgets[widget]['section'], self.widgets[widget]['option'])

                if value != None:
                    if widget[:2] == 'ef':
                        self.widgets[widget]['object'].setentry(value)
                    elif widget[:2] == 'cb' and value != '':
                        self.widgets[widget]['object'].setvalue(value)

                #To update the balloon text
                if 'balloon' in self.widgets[widget].keys():
                    self.widgets[widget]['object'].configure(validate=validator(self.widgets[widget]['section'], self.widgets[widget]['option']))
                    self.widgets[widget]['balloon'].bind(self.widgets[widget]['object'], validatorBalloon(validator(self.widgets[widget]['section'], self.widgets[widget]['option'])))
            else:
                if widget[:2] == 'cv':
                    width = self.app.cpr.defaultParameters['AOI3DHough']['left'][3]
                    height = self.app.cpr.defaultParameters['AOI3DHough']['top'][3]

                    try:
                        left = float(self.app.cpr.getParameter('AOI3DHough', 'Left')) / width * 200 + 3
                    except:
                        left = 0
                    try:
                        top = float(self.app.cpr.getParameter('AOI3DHough', 'Top')) / height * 152 + 3
                    except:
                        top = 0
                    try:
                        right = float(self.app.cpr.getParameter('AOI3DHough', 'Right')) / width * 200 + 3
                    except:
                        right = 0
                    try:
                        bottom = float(self.app.cpr.getParameter('AOI3DHough', 'Bottom')) / height * 152 + 3
                    except:
                        bottom = 0

                    self.widgets[widget]['object'].coords(self.widgets['ciRed']['object'], left, top, right, bottom)

                    x0 = self.app.cpr.getParameter('AOI2DHough', 'X0')
                    y0 = self.app.cpr.getParameter('AOI2DHough', 'Y0')
                    r = self.app.cpr.getParameter('AOI2DHough', 'R')

                    try:
                        left = float(x0 - r) / width * 200 + 3
                    except:
                        left = 0
                    try:
                        top = float(y0 - r) / height * 152 + 3
                    except:
                        top = 0
                    try:
                        right = float(x0 + r) / width * 200 + 3
                    except:
                        right = 0
                    try:
                        bottom = float(y0 + r) / height * 152 + 3
                    except:
                        bottom = 0

                    self.widgets[widget]['object'].coords(self.widgets['ciGreen']['object'], left, top, right, bottom)


    def bindAll(self):
        """
        Bind the widgets with there respective action
        """
        objects = []
        for widget in self.widgetsOrder:
            if widget[:2] == 'ef' or widget[:2] == 'cb':
                self.widgets[widget]['object'].pack(fill=Tkinter.X, expand=1, padx=10, pady=5)

                self.widgets[widget]['object'].bind('<FocusOut>', lambda event, func=self.saveValue
                                                                          , widgetName=widget
                                                                          , widget=self.widgets[widget]:
                                                                           func(event, widgetName, widget))

                objects.append(self.widgets[widget]['object'])
            elif widget[:2] == 'cv':
                self.widgets[widget]['object'].pack(padx=10, pady=5)

        Pmw.alignlabels(objects)

    def load(self, file=None):
        """
        Load a cpr file
        """
        if file == None:
            file = tkFileDialog.askopenfile(parent=self.root, initialdir=self.currentLoadDirectory, mode='r', filetypes=[('Configuration Project File', '*.cpr')], title='Choose a file')
            if file != None:
                file = file.name

        if file != None:
            self.filepath.set(os.path.split(file)[1])
            self.currentLoadDirectory = os.path.split(file)[0]
            self.cpr = cprFile.cpr(file)
            self.updateAllValues()

    def saveAs(self):
        """
        Save as a cpr file
        """
        self.saveAllValues()

        file = tkFileDialog.asksaveasfilename(parent=self.root, initialdir=self.currentSaveDirectory, filetypes=[('Configuration Project File', '*.cpr')] , title="Save the project as...")

        if file != '':
            if file[-4:] != '.cpr':
                file = file + '.cpr'

            self.currentSaveDirectory = os.path.split(file)[0]
            self.cpr.write(filepath=file)

            self.filepath.set(os.path.split(file)[1])

    def save(self):
        """
        Save a cpr file
        """
        self.saveAllValues()
        self.cpr.write()

    def display(self):
        """
        Print the information for the cpr dictionary
        """
        print self.cpr.getCprDict()

    def exit(self):
        """
          Exit the application
        """
        self.root.destroy()

class tabMicroscope(App):
    def __init__(self, app, tab):
        self.widgets = {}
        self.widgetsOrder = []
        self.app = app

        widgetsOrder, widgets = self.buildColumn(tab)
        self.widgets.update(widgets)
        self.widgetsOrder += widgetsOrder

        widgetsOrder, widgets = self.buildStage(tab)
        self.widgets.update(widgets)
        self.widgetsOrder += widgetsOrder

        self.bindAll()
        self.updateAllValues()

    def buildColumn(self, tab):
        widgets = {}
        widgetsOrder = []
        group = Pmw.Group(tab, tag_text='Column')
        group.pack(fill=Tkinter.X, padx=2, pady=2)

        widgetName = 'efkV'
        widget = {'section': 'Job', 'option': 'kV'}
        validationDict = validator(widget['section'], widget['option'])
        validationString = validatorBalloon(validationDict)
        efkV = Pmw.EntryField(group.interior()
                              , labelpos=Tkinter.W
                              , label_text='Voltage (kV): '
                              , validate=validationDict)
        widget.update({'object': efkV})
        Pmw.Balloon(tab).bind(widget['object'], validationString)
        widgets.setdefault(widgetName, widget)
        widgetsOrder.append(widgetName)

        widgetName = 'efMag'
        widget = {'section': 'Job', 'option': 'Magnification'}
        validationDict = validator(widget['section'], widget['option'])
        validationString = validatorBalloon(validationDict)
        efMag = Pmw.EntryField(group.interior()
                               , labelpos=Tkinter.W
                               , label_text='Magnification: '
                               , validate=validationDict)
        widget.update({'object': efMag})
        Pmw.Balloon(tab).bind(widget['object'], validationString)
        widgets.setdefault(widgetName, widget)
        widgetsOrder.append(widgetName)

        widgetName = 'efWD'
        widget = {'section': 'Job', 'option': 'WorkingDistance'}
        validationDict = validator(widget['section'], widget['option'])
        validationString = validatorBalloon(validationDict)
        efWD = Pmw.EntryField(group.interior()
                               , labelpos=Tkinter.W
                               , label_text='WD (mm): '
                               , validate=validationDict)
        widget.update({'object': efWD})
        Pmw.Balloon(tab).bind(widget['object'], validationString)
        widgets.setdefault(widgetName, widget)
        widgetsOrder.append(widgetName)

        return widgetsOrder, widgets

    def buildStage(self, tab):
        widgets = {}
        widgetsOrder = []
        group = Pmw.Group(tab, tag_text='Stage')
        group.pack(fill=Tkinter.X, padx=2, pady=2)

        widgetName = 'efX'
        widget = {'section': 'StagePosition', 'option': 'XPos'}
        validationDict = validator(widget['section'], widget['option'])
        validationString = validatorBalloon(validationDict)
        efX = Pmw.EntryField(group.interior()
                              , labelpos=Tkinter.W
                              , label_text='X pos: '
                              , validate=validationDict)
        widget.update({'object': efX})
        Pmw.Balloon(tab).bind(widget['object'], validationString)
        widgets.setdefault(widgetName, widget)
        widgetsOrder.append(widgetName)

        widgetName = 'efY'
        widget = {'section': 'StagePosition', 'option': 'YPos'}
        validationDict = validator(widget['section'], widget['option'])
        validationString = validatorBalloon(validationDict)
        efY = Pmw.EntryField(group.interior()
                              , labelpos=Tkinter.W
                              , label_text='Y pos: '
                              , validate=validationDict)
        widget.update({'object': efY})
        Pmw.Balloon(tab).bind(widget['object'], validationString)
        widgets.setdefault(widgetName, widget)
        widgetsOrder.append(widgetName)

        widgetName = 'efZ'
        widget = {'section': 'StagePosition', 'option': 'ZPos'}
        validationDict = validator(widget['section'], widget['option'])
        validationString = validatorBalloon(validationDict)
        efZ = Pmw.EntryField(group.interior()
                              , labelpos=Tkinter.W
                              , label_text='Z pos: '
                              , validate=validationDict)
        widget.update({'object': efZ})
        Pmw.Balloon(tab).bind(widget['object'], validationString)
        widgets.setdefault(widgetName, widget)
        widgetsOrder.append(widgetName)

        widgetName = 'efR'
        widget = {'section': 'StagePosition', 'option': 'RPos'}
        validationDict = validator(widget['section'], widget['option'])
        validationString = validatorBalloon(validationDict)
        efR = Pmw.EntryField(group.interior()
                              , labelpos=Tkinter.W
                              , label_text='R pos: '
                              , validate=validationDict)
        widget.update({'object': efR})
        Pmw.Balloon(tab).bind(widget['object'], validationString)
        widgets.setdefault(widgetName, widget)
        widgetsOrder.append(widgetName)

        widgetName = 'efT'
        widget = {'section': 'StagePosition', 'option': 'TPos'}
        validationDict = validator(widget['section'], widget['option'])
        validationString = validatorBalloon(validationDict)
        efT = Pmw.EntryField(group.interior()
                              , labelpos=Tkinter.W
                              , label_text='T pos: '
                              , validate=validationDict)
        widget.update({'object': efT})
        Pmw.Balloon(tab).bind(widget['object'], validationString)
        widgets.setdefault(widgetName, widget)
        widgetsOrder.append(widgetName)

        return widgetsOrder, widgets

class tabDetector(App):
    def __init__(self, app, tab):
        self.widgets = {}
        self.widgetsOrder = []
        self.app = app

        widgetsOrder, widgets = self.buildCamera(tab)
        self.widgets.update(widgets)
        self.widgetsOrder += widgetsOrder

        widgetsOrder, widgets = self.buildBackground(tab)
        self.widgets.update(widgets)
        self.widgetsOrder += widgetsOrder

        self.bindAll()
        self.updateAllValues()

    def buildCamera(self, tab):
        widgets = {}
        widgetsOrder = []
        group = Pmw.Group(tab, tag_text='Camera')
        group.pack(fill=Tkinter.X, padx=2, pady=2)

        widgetName = 'cbBinning'
        widget = {'section': 'FG_DCam parameters', 'option': 'Binning'}
        cbBinning = Pmw.OptionMenu(group.interior()
                              , labelpos=Tkinter.W
                              , label_text='Binning: '
                              , command=lambda event, func=self.saveValue, widgetName=widgetName, widget=widget: func(event, widgetName, widget)
                              , items=("No binning", "2x2 binning", "4x4 binning", "8x8 binning", "8x8 superfast"))
        widget.update({'object': cbBinning})
        widgets.setdefault(widgetName, widget)
        widgetsOrder.append(widgetName)

        widgetName = 'cbGain'
        widget = {'section': 'FG_DCam parameters', 'option': 'Gain'}
        cbGain = Pmw.OptionMenu(group.interior()
                              , labelpos=Tkinter.W
                              , label_text='Binning: '
                              , command=lambda event, func=self.saveValue, widgetName=widgetName, widget=widget: func(event, widgetName, widget)
                              , items=("Low", "High"))
        widget.update({'object': cbGain})
        widgets.setdefault(widgetName, widget)
        widgetsOrder.append(widgetName)

        widgetName = 'efMinTimePerFrame'
        widget = {'section': 'Live EBSP', 'option': 'MinTimePerFrame'}
        validationDict = validator(widget['section'], widget['option'])
        validationString = validatorBalloon(validationDict)
        efMinTimePerFrame = Pmw.EntryField(group.interior()
                              , labelpos=Tkinter.W
                              , label_text='Min Time Per Frame (ms): '
                              , validate=validationDict)
        widget.update({'object': efMinTimePerFrame})
        Pmw.Balloon(tab).bind(widget['object'], validationString)
        widgets.setdefault(widgetName, widget)
        widgetsOrder.append(widgetName)

        widgetName = 'efNoFrames'
        widget = {'section': 'Live EBSP', 'option': 'NoFrames'}
        validationDict = validator(widget['section'], widget['option'])
        validationString = validatorBalloon(validationDict)
        efNoFrames = Pmw.EntryField(group.interior()
                              , labelpos=Tkinter.W
                              , label_text='Average Frames: '
                              , validate=validationDict)
        widget.update({'object': efNoFrames})
        Pmw.Balloon(tab).bind(widget['object'], validationString)
        widgets.setdefault(widgetName, widget)
        widgetsOrder.append(widgetName)

        return widgetsOrder, widgets

    def buildBackground(self, tab):
        widgets = {}
        widgetsOrder = []
        group = Pmw.Group(tab, tag_text='Background')
        group.pack(fill=Tkinter.X, padx=2, pady=2)

        widgetName = 'cbBackgroundMode'
        widget = {'section': 'Live EBSP', 'option': 'BackgroundMode'}
        cbBackgroundMode = Pmw.OptionMenu(group.interior()
                              , labelpos=Tkinter.W
                              , label_text='Backgroung Mode: '
                              , command=lambda event, func=self.saveValue, widgetName=widgetName, widget=widget: func(event, widgetName, widget)
                              , items=("Substract", "Divide"))
        widget.update({'object': cbBackgroundMode})
        widgets.setdefault(widgetName, widget)
        widgetsOrder.append(widgetName)

        widgetName = 'efNoFramesBackGround'
        widget = {'section': 'Live EBSP', 'option': 'NoFramesBackGround'}
        validationDict = validator(widget['section'], widget['option'])
        validationString = validatorBalloon(validationDict)
        efNoFramesBackGround = Pmw.EntryField(group.interior()
                              , labelpos=Tkinter.W
                              , label_text='Background frames: '
                              , validate=validationDict)
        widget.update({'object': efNoFramesBackGround})
        Pmw.Balloon(tab).bind(widget['object'], validationString)
        widgets.setdefault(widgetName, widget)
        widgetsOrder.append(widgetName)

        widgetName = 'cbBackgroundOn'
        widget = {'section': 'Live EBSP', 'option': 'InSoftware'}
        cbBackgroundOn = Pmw.OptionMenu(group.interior()
                              , labelpos=Tkinter.W
                              , label_text='Backgroung On: '
                              , command=lambda event, func=self.saveValue, widgetName=widgetName, widget=widget: func(event, widgetName, widget)
                              , items=("False", "True"))
        widget.update({'object': cbBackgroundOn})
        widgets.setdefault(widgetName, widget)
        widgetsOrder.append(widgetName)

        widgetName = 'cbDynamicBackground'
        widget = {'section': 'Live EBSP', 'option': 'AutoBackgroundOn'}
        cbDynamicBackground = Pmw.OptionMenu(group.interior()
                              , labelpos=Tkinter.W
                              , label_text='Dynamic Background: '
                              , command=lambda event, func=self.saveValue, widgetName=widgetName, widget=widget: func(event, widgetName, widget)
                              , items=("False", "True"))
        widget.update({'object': cbDynamicBackground})
        widgets.setdefault(widgetName, widget)
        widgetsOrder.append(widgetName)

        widgetName = 'cbAutoStretch'
        widget = {'section': 'Live EBSP', 'option': 'AutoStretch'}
        cbAutoStretch = Pmw.OptionMenu(group.interior()
                              , labelpos=Tkinter.W
                              , label_text='AutoStretch: '
                              , command=lambda event, func=self.saveValue, widgetName=widgetName, widget=widget: func(event, widgetName, widget)
                              , items=("False", "True"))
        widget.update({'object': cbAutoStretch})
        widgets.setdefault(widgetName, widget)
        widgetsOrder.append(widgetName)

        return widgetsOrder, widgets

class tabAoi(App):
    def __init__(self, app, tab):
        self.widgets = {}
        self.widgetsOrder = []
        self.app = app

        widgetsOrder, widgets = self.buildRed(tab)
        self.widgets.update(widgets)
        self.widgetsOrder += widgetsOrder

        widgetsOrder, widgets = self.buildGreen(tab)
        self.widgets.update(widgets)
        self.widgetsOrder += widgetsOrder

        widgetsOrder, widgets = self.buildCanvas(tab)
        self.widgets.update(widgets)
        self.widgetsOrder += widgetsOrder

        self.bindAll()
        self.updateAllValues()

    def buildRed(self, tab):
        widgets = {}
        widgetsOrder = []
        group = Pmw.Group(tab, tag_text='Red Square')
        group.pack(fill=Tkinter.X, padx=2, pady=2)

        widgetName = 'efAOILeft'
        widget = {'section': 'AOI3DHough', 'option': 'Left'}
        validationDict = validator(widget['section'], widget['option'])
        validationString = validatorBalloon(validationDict)
        efAOILeft = Pmw.EntryField(group.interior()
                              , labelpos=Tkinter.W
                              , label_text='Left: '
                              , validate=validationDict)
        widget.update({'object': efAOILeft})
        balloonAOILeft = Pmw.Balloon(tab)
        balloonAOILeft.bind(widget['object'], validationString)
        widget.update({'balloon': balloonAOILeft})
        widgets.setdefault(widgetName, widget)
        widgetsOrder.append(widgetName)

        widgetName = 'efAOITop'
        widget = {'section': 'AOI3DHough', 'option': 'Top'}
        validationDict = validator(widget['section'], widget['option'])
        validationString = validatorBalloon(validationDict)
        efAOITop = Pmw.EntryField(group.interior()
                              , labelpos=Tkinter.W
                              , label_text='Top: '
                              , validate=validationDict)
        widget.update({'object': efAOITop})
        balloonAOITop = Pmw.Balloon(tab)
        balloonAOITop.bind(widget['object'], validationString)
        widget.update({'balloon': balloonAOITop})
        widgets.setdefault(widgetName, widget)
        widgetsOrder.append(widgetName)

        widgetName = 'efAOIRight'
        widget = {'section': 'AOI3DHough', 'option': 'Right'}
        validationDict = validator(widget['section'], widget['option'])
        validationString = validatorBalloon(validationDict)
        efAOIRight = Pmw.EntryField(group.interior()
                              , labelpos=Tkinter.W
                              , label_text='Right: '
                              , validate=validationDict)
        widget.update({'object': efAOIRight})
        balloonAOIRight = Pmw.Balloon(tab)
        balloonAOIRight.bind(widget['object'], validationString)
        widget.update({'balloon': balloonAOIRight})
        widgets.setdefault(widgetName, widget)
        widgetsOrder.append(widgetName)

        widgetName = 'efAOIBottom'
        widget = {'section': 'AOI3DHough', 'option': 'Bottom'}
        validationDict = validator(widget['section'], widget['option'])
        validationString = validatorBalloon(validationDict)
        efAOIBottom = Pmw.EntryField(group.interior()
                              , labelpos=Tkinter.W
                              , label_text='Bottom: '
                              , validate=validationDict)
        widget.update({'object': efAOIBottom})
        balloonAOIBottom = Pmw.Balloon(tab)
        balloonAOIBottom.bind(widget['object'], validationString)
        widget.update({'balloon': balloonAOIBottom})
        widgets.setdefault(widgetName, widget)
        widgetsOrder.append(widgetName)

        return widgetsOrder, widgets

    def buildGreen(self, tab):
        widgets = {}
        widgetsOrder = []
        group = Pmw.Group(tab, tag_text='Green circle')
        group.pack(fill=Tkinter.X, padx=2, pady=2)

        widgetName = 'efAOIX0'
        widget = {'section': 'AOI2DHough', 'option': 'X0'}
        validationDict = validator(widget['section'], widget['option'])
        validationString = validatorBalloon(validationDict)
        efAOIX0 = Pmw.EntryField(group.interior()
                              , labelpos=Tkinter.W
                              , label_text='X: '
                              , validate=validationDict)
        widget.update({'object': efAOIX0})
        Pmw.Balloon(tab).bind(widget['object'], validationString)
        widgets.setdefault(widgetName, widget)
        widgetsOrder.append(widgetName)

        widgetName = 'efAOIY0'
        widget = {'section': 'AOI2DHough', 'option': 'Y0'}
        validationDict = validator(widget['section'], widget['option'])
        validationString = validatorBalloon(validationDict)
        efAOIY0 = Pmw.EntryField(group.interior()
                              , labelpos=Tkinter.W
                              , label_text='Y: '
                              , validate=validationDict)
        widget.update({'object': efAOIY0})
        Pmw.Balloon(tab).bind(widget['object'], validationString)
        widgets.setdefault(widgetName, widget)
        widgetsOrder.append(widgetName)

        widgetName = 'efAOIR'
        widget = {'section': 'AOI2DHough', 'option': 'R'}
        validationDict = validator(widget['section'], widget['option'])
        validationString = validatorBalloon(validationDict)
        efAOIR = Pmw.EntryField(group.interior()
                              , labelpos=Tkinter.W
                              , label_text='Radius: '
                              , validate=validationDict)
        widget.update({'object': efAOIR})
        balloonAOIR = Pmw.Balloon(tab)
        balloonAOIR.bind(widget['object'], validationString)
        widget.update({'balloon': balloonAOIR})
        widgets.setdefault(widgetName, widget)
        widgetsOrder.append(widgetName)

        return widgetsOrder, widgets

    def buildCanvas(self, tab):
        widgets = {}
        widgetsOrder = []

        widgetName = 'cvAOI'
        cvAOI = Tkinter.Canvas(tab
                              , width=203
                              , height=155
                              , background='#000000')
        widget = {'object': cvAOI}
        widgets.setdefault(widgetName, widget)
        widgetsOrder.append(widgetName)

        widgetName = 'ciRed'
        ciRed = cvAOI.create_rectangle(3, 3, 203, 155
                                      , width=3
                                      , outline='#FF0000')
        widget = {'object': ciRed}
        widgets.setdefault(widgetName, widget)
        widgetsOrder.append(widgetName)

        widgetName = 'ciGreen'
        ciGreen = cvAOI.create_oval(3, 3, 100, 100
                                      , width=3
                                      , outline='#00FF00')
        widget = {'object': ciGreen}
        widgets.setdefault(widgetName, widget)
        widgetsOrder.append(widgetName)

        return widgetsOrder, widgets

class tabBands(App):
    def __init__(self, app, tab):
        self.widgets = {}
        self.widgetsOrder = []
        self.app = app

        widgetsOrder, widgets = self.buildBand(tab)
        self.widgets.update(widgets)
        self.widgetsOrder += widgetsOrder

        widgetsOrder, widgets = self.buildProjection(tab)
        self.widgets.update(widgets)
        self.widgetsOrder += widgetsOrder

        self.bindAll()
        self.updateAllValues()

    def buildBand(self, tab):
        widgets = {}
        widgetsOrder = []
        group = Pmw.Group(tab, tag_text='Band Detection')
        group.pack(fill=Tkinter.X, padx=2, pady=2)

        widgetName = 'cbDetect'
        widget = {'section': 'Band Detection', 'option': 'Detect'}
        cbDetect = Pmw.OptionMenu(group.interior()
                              , labelpos=Tkinter.W
                              , label_text='Bands: '
                              , command=lambda event, func=self.saveValue, widgetName=widgetName, widget=widget: func(event, widgetName, widget)
                              , items=('Band Centers', 'Band Edges', 'Adaptive', 'Enhanced Adaptive'))
        widget.update({'object': cbDetect})
        widgets.setdefault(widgetName, widget)
        widgetsOrder.append(widgetName)

        widgetName = 'cbDivergence'
        widget = {'section': 'Band Detection', 'option': 'Divergence'}
        cbDivergence = Pmw.OptionMenu(group.interior()
                              , labelpos=Tkinter.W
                              , label_text='Divergence: '
                              , command=lambda event, func=self.saveValue, widgetName=widgetName, widget=widget: func(event, widgetName, widget)
                              , items=('Low', 'Standard', 'High'))
        widget.update({'object': cbDivergence})
        widgets.setdefault(widgetName, widget)
        widgetsOrder.append(widgetName)

        widgetName = 'efBandsMin'
        widget = {'section': 'Band Detection', 'option': 'Min'}
        validationDict = validator(widget['section'], widget['option'])
        validationString = validatorBalloon(validationDict)
        efBandsMin = Pmw.EntryField(group.interior()
                              , labelpos=Tkinter.W
                              , label_text='Min: '
                              , validate=validationDict)
        widget.update({'object': efBandsMin})
        Pmw.Balloon(tab).bind(widget['object'], validationString)
        widgets.setdefault(widgetName, widget)
        widgetsOrder.append(widgetName)

        widgetName = 'efBandsMax'
        widget = {'section': 'Band Detection', 'option': 'Max'}
        validationDict = validator(widget['section'], widget['option'])
        validationString = validatorBalloon(validationDict)
        efBandsMax = Pmw.EntryField(group.interior()
                              , labelpos=Tkinter.W
                              , label_text='Max: '
                              , validate=validationDict)
        widget.update({'object': efBandsMax})
        Pmw.Balloon(tab).bind(widget['object'], validationString)
        widgets.setdefault(widgetName, widget)
        widgetsOrder.append(widgetName)

        widgetName = 'cbAdvancedFit'
        widget = {'section': 'Band Detection', 'option': 'OLock'}
        cbAdvancedFit = Pmw.OptionMenu(group.interior()
                              , labelpos=Tkinter.W
                              , label_text='Advanced Fit: '
                              , command=lambda event, func=self.saveValue, widgetName=widgetName, widget=widget: func(event, widgetName, widget)
                              , items=('False', 'True'))
        widget.update({'object': cbAdvancedFit})
        widgets.setdefault(widgetName, widget)
        widgetsOrder.append(widgetName)

        widgetName = 'cbAdvancedFitLevel'
        widget = {'section': 'Band Detection', 'option': 'OLockLevel'}
        cbAdvancedFitLevel = Pmw.OptionMenu(group.interior()
                              , labelpos=Tkinter.W
                              , label_text='Advanced Fit Level: '
                              , command=lambda event, func=self.saveValue, widgetName=widgetName, widget=widget: func(event, widgetName, widget)
                              , items=(1, 2, 3, 4))
        widget.update({'object': cbAdvancedFitLevel})
        widgets.setdefault(widgetName, widget)
        widgetsOrder.append(widgetName)

        widgetName = 'efHoughRes'
        widget = {'section': 'Band Detection', 'option': 'HoughRes'}
        validationDict = validator(widget['section'], widget['option'])
        validationString = validatorBalloon(validationDict)
        efHoughRes = Pmw.EntryField(group.interior()
                              , labelpos=Tkinter.W
                              , label_text='Hough Resolution: '
                              , validate=validationDict)
        widget.update({'object': efHoughRes})
        Pmw.Balloon(tab).bind(widget['object'], validationString)
        widgets.setdefault(widgetName, widget)
        widgetsOrder.append(widgetName)

        widgetName = 'efReflectors'
        widget = {'section': 'Phases', 'option': 'NoReflectors'}
        validationDict = validator(widget['section'], widget['option'])
        validationString = validatorBalloon(validationDict)
        efReflectors = Pmw.EntryField(group.interior()
                              , labelpos=Tkinter.W
                              , label_text='No of Reflectors: '
                              , validate=validationDict)
        widget.update({'object': efReflectors})
        Pmw.Balloon(tab).bind(widget['object'], validationString)
        widgets.setdefault(widgetName, widget)
        widgetsOrder.append(widgetName)

        return widgetsOrder, widgets

    def buildProjection(self, tab):
        widgets = {}
        widgetsOrder = []
        group = Pmw.Group(tab, tag_text='Projection Parameters')
        group.pack(fill=Tkinter.X, padx=2, pady=2)

        widgetName = 'efVHRatio'
        widget = {'section': 'ProjectionParameters', 'option': 'VHRatio'}
        validationDict = validator(widget['section'], widget['option'])
        validationString = validatorBalloon(validationDict)
        efVHRatio = Pmw.EntryField(group.interior()
                              , labelpos=Tkinter.W
                              , label_text='VHRatio: '
                              , validate=validationDict)
        widget.update({'object': efVHRatio})
        Pmw.Balloon(tab).bind(widget['object'], validationString)
        widgets.setdefault(widgetName, widget)
        widgetsOrder.append(widgetName)

        widgetName = 'efPCX'
        widget = {'section': 'ProjectionParameters', 'option': 'PCX'}
        validationDict = validator(widget['section'], widget['option'])
        validationString = validatorBalloon(validationDict)
        efPCX = Pmw.EntryField(group.interior()
                              , labelpos=Tkinter.W
                              , label_text='PC X: '
                              , validate=validationDict)
        widget.update({'object': efPCX})
        Pmw.Balloon(tab).bind(widget['object'], validationString)
        widgets.setdefault(widgetName, widget)
        widgetsOrder.append(widgetName)

        widgetName = 'efPCY'
        widget = {'section': 'ProjectionParameters', 'option': 'PCY'}
        validationDict = validator(widget['section'], widget['option'])
        validationString = validatorBalloon(validationDict)
        efPCY = Pmw.EntryField(group.interior()
                              , labelpos=Tkinter.W
                              , label_text='PC Y: '
                              , validate=validationDict)
        widget.update({'object': efPCY})
        Pmw.Balloon(tab).bind(widget['object'], validationString)
        widgets.setdefault(widgetName, widget)
        widgetsOrder.append(widgetName)

        widgetName = 'efDD'
        widget = {'section': 'ProjectionParameters', 'option': 'DD'}
        validationDict = validator(widget['section'], widget['option'])
        validationString = validatorBalloon(validationDict)
        efDD = Pmw.EntryField(group.interior()
                              , labelpos=Tkinter.W
                              , label_text='DD: '
                              , validate=validationDict)
        widget.update({'object': efDD})
        Pmw.Balloon(tab).bind(widget['object'], validationString)
        widgets.setdefault(widgetName, widget)
        widgetsOrder.append(widgetName)

        return widgetsOrder, widgets

class tabJob(App):
    def __init__(self, app, tab):
        self.widgets = {}
        self.widgetsOrder = []
        self.app = app

        widgetsOrder, widgets = self.buildMapping(tab)
        self.widgets.update(widgets)
        self.widgetsOrder += widgetsOrder

        widgetsOrder, widgets = self.buildStorage(tab)
        self.widgets.update(widgets)
        self.widgetsOrder += widgetsOrder

        widgetsOrder, widgets = self.buildDisciminators(tab)
        self.widgets.update(widgets)
        self.widgetsOrder += widgetsOrder

        self.bindAll()
        self.updateAllValues()

    def buildMapping(self, tab):
        widgets = {}
        widgetsOrder = []
        group = Pmw.Group(tab, tag_text='Mapping')
        group.pack(fill=Tkinter.X, padx=2, pady=2)

        widgetName = 'efStep'
        widget = {'section': 'Job', 'option': 'GridDistX'}
        validationDict = validator(widget['section'], widget['option'])
        validationString = validatorBalloon(validationDict)
        efStep = Pmw.EntryField(group.interior()
                              , labelpos=Tkinter.W
                              , label_text='Step (um): '
                              , validate=validationDict)
        widget.update({'object': efStep})
        Pmw.Balloon(tab).bind(widget['object'], validationString)
        widgets.setdefault(widgetName, widget)
        widgetsOrder.append(widgetName)

        widgetName = 'efxCells'
        widget = {'section': 'Job', 'option': 'xCells'}
        validationDict = validator(widget['section'], widget['option'])
        validationString = validatorBalloon(validationDict)
        efxCells = Pmw.EntryField(group.interior()
                              , labelpos=Tkinter.W
                              , label_text='# of points in X: '
                              , validate=validationDict)
        widget.update({'object': efxCells})
        Pmw.Balloon(tab).bind(widget['object'], validationString)
        widgets.setdefault(widgetName, widget)
        widgetsOrder.append(widgetName)

        widgetName = 'efyCells'
        widget = {'section': 'Job', 'option': 'yCells'}
        validationDict = validator(widget['section'], widget['option'])
        validationString = validatorBalloon(validationDict)
        efyCells = Pmw.EntryField(group.interior()
                              , labelpos=Tkinter.W
                              , label_text='# of points in Y: '
                              , validate=validationDict)
        widget.update({'object': efyCells})
        Pmw.Balloon(tab).bind(widget['object'], validationString)
        widgets.setdefault(widgetName, widget)
        widgetsOrder.append(widgetName)

        widgetName = 'efJobLeft'
        widget = {'section': 'Job', 'option': 'Left'}
        validationDict = validator(widget['section'], widget['option'])
        validationString = validatorBalloon(validationDict)
        efJobLeft = Pmw.EntryField(group.interior()
                              , labelpos=Tkinter.W
                              , label_text='Upper-left corner Left: '
                              , validate=validationDict)
        widget.update({'object': efJobLeft})
        Pmw.Balloon(tab).bind(widget['object'], validationString)
        widgets.setdefault(widgetName, widget)
        widgetsOrder.append(widgetName)

        widgetName = 'efJobTop'
        widget = {'section': 'Job', 'option': 'Top'}
        validationDict = validator(widget['section'], widget['option'])
        validationString = validatorBalloon(validationDict)
        efJobTop = Pmw.EntryField(group.interior()
                              , labelpos=Tkinter.W
                              , label_text='Upper-left corner Top: '
                              , validate=validationDict)
        widget.update({'object': efJobTop})
        Pmw.Balloon(tab).bind(widget['object'], validationString)
        widgets.setdefault(widgetName, widget)
        widgetsOrder.append(widgetName)

        return widgetsOrder, widgets

    def buildStorage(self, tab):
        widgets = {}
        widgetsOrder = []
        group = Pmw.Group(tab, tag_text='Image Storage')
        group.pack(fill=Tkinter.X, padx=2, pady=2)

        widgetName = 'cbSaveWhen'
        widget = {'section': 'Image Compression', 'option': 'SaveWhen'}
        cbSaveWhen = Pmw.OptionMenu(group.interior()
                              , labelpos=Tkinter.W
                              , label_text='Save When: '
                              , command=lambda event, func=self.saveValue, widgetName=widgetName, widget=widget: func(event, widgetName, widget)
                              , items=('Do not save', "Save if can't index", 'Save %', "Save all and don't index"))
        widget.update({'object': cbSaveWhen})
        widgets.setdefault(widgetName, widget)
        widgetsOrder.append(widgetName)

        widgetName = 'efSavePercentage'
        widget = {'section': 'Image Compression', 'option': 'Percentage'}
        validationDict = validator(widget['section'], widget['option'])
        validationString = validatorBalloon(validationDict)
        efSavePercentage = Pmw.EntryField(group.interior()
                              , labelpos=Tkinter.W
                              , label_text='Percentage: '
                              , validate=validationDict)
        widget.update({'object': efSavePercentage})
        Pmw.Balloon(tab).bind(widget['object'], validationString)
        widgets.setdefault(widgetName, widget)
        widgetsOrder.append(widgetName)

        return widgetsOrder, widgets

    def buildDisciminators(self, tab):
        widgets = {}
        widgetsOrder = []
        group = Pmw.Group(tab, tag_text='Disciminators')
        group.pack(fill=Tkinter.X, padx=2, pady=2)

        widgetName = 'efBC'
        widget = {'section': 'Discriminators', 'option': 'BC'}
        validationDict = validator(widget['section'], widget['option'])
        validationString = validatorBalloon(validationDict)
        efBC = Pmw.EntryField(group.interior()
                              , labelpos=Tkinter.W
                              , label_text='Band Contrast: '
                              , validate=validationDict)
        widget.update({'object': efBC})
        Pmw.Balloon(tab).bind(widget['object'], validationString)
        widgets.setdefault(widgetName, widget)
        widgetsOrder.append(widgetName)

        widgetName = 'efBS'
        widget = {'section': 'Discriminators', 'option': 'BS'}
        validationDict = validator(widget['section'], widget['option'])
        validationString = validatorBalloon(validationDict)
        efBS = Pmw.EntryField(group.interior()
                              , labelpos=Tkinter.W
                              , label_text='Band Slope: '
                              , validate=validationDict)
        widget.update({'object': efBS})
        Pmw.Balloon(tab).bind(widget['object'], validationString)
        widgets.setdefault(widgetName, widget)
        widgetsOrder.append(widgetName)

        widgetName = 'efMAD'
        widget = {'section': 'Discriminators', 'option': 'MAD'}
        validationDict = validator(widget['section'], widget['option'])
        validationString = validatorBalloon(validationDict)
        efMAD = Pmw.EntryField(group.interior()
                              , labelpos=Tkinter.W
                              , label_text='MAD: '
                              , validate=validationDict)
        widget.update({'object': efMAD})
        Pmw.Balloon(tab).bind(widget['object'], validationString)
        widgets.setdefault(widgetName, widget)
        widgetsOrder.append(widgetName)

        return widgetsOrder, widgets

class tabGeneral(App):
    def __init__(self, app, tab):
        self.widgets = {}
        self.widgetsOrder = []
        self.app = app

        widgetsOrder, widgets = self.buildDesc(tab)
        self.widgets.update(widgets)
        self.widgetsOrder += widgetsOrder

        self.bindAll()
        self.updateAllValues()

    def buildDesc(self, tab):
        widgets = {}
        widgetsOrder = []
        group = Pmw.Group(tab, tag_text='Description')
        group.pack(fill=Tkinter.X, padx=2, pady=2)

        widgetName = 'efDescription'
        widget = {'section': 'General', 'option': 'Description'}
        validationDict = validator(widget['section'], widget['option'])
        validationString = validatorBalloon(validationDict)
        efDescription = Pmw.EntryField(group.interior()
                              , labelpos=Tkinter.W
                              , label_text='Description: '
                              , validate=validationDict)
        widget.update({'object': efDescription})
        Pmw.Balloon(tab).bind(widget['object'], validationString)
        widgets.setdefault(widgetName, widget)
        widgetsOrder.append(widgetName)

        widgetName = 'efNotes'
        widget = {'section': 'General', 'option': 'Notes'}
        validationDict = validator(widget['section'], widget['option'])
        validationString = validatorBalloon(validationDict)
        efNotes = Pmw.EntryField(group.interior()
                              , labelpos=Tkinter.W
                              , label_text='Notes: '
                              , validate=validationDict)
        widget.update({'object': efNotes})
        Pmw.Balloon(tab).bind(widget['object'], validationString)
        widgets.setdefault(widgetName, widget)
        widgetsOrder.append(widgetName)

        return widgetsOrder, widgets

class tabEds(App):
    def __init__(self, app, tab):
        self.widgets = {}
        self.widgetsOrder = []
        self.app = app

        widgetsOrder, widgets = self.buildMapping(tab)
        self.widgets.update(widgets)
        self.widgetsOrder += widgetsOrder

        self.bindAll()
        self.updateAllValues()

    def buildMapping(self, tab):
        widgets = {}
        widgetsOrder = []
        group = Pmw.Group(tab, tag_text='Mapping')
        group.pack(fill=Tkinter.X, padx=2, pady=2)

        widgetName = 'cbEDSMapping'
        widget = {'section': 'EDX Control', 'option': 'MappingEnabled'}
        cbEDSMapping = Pmw.OptionMenu(group.interior()
                              , labelpos=Tkinter.W
                              , label_text='Enabled: '
                              , command=lambda event, func=self.saveValue, widgetName=widgetName, widget=widget: func(event, widgetName, widget)
                              , items=("False", "True"))
        widget.update({'object': cbEDSMapping})
        widgets.setdefault(widgetName, widget)
        widgetsOrder.append(widgetName)

        widgetName = 'efCycle'
        widget = {'section': 'EDX Control', 'option': 'MinCycleTime'}
        validationDict = validator(widget['section'], widget['option'])
        validationString = validatorBalloon(validationDict)
        efCycle = Pmw.EntryField(group.interior()
                              , labelpos=Tkinter.W
                              , label_text='Acquisition Time (ms): '
                              , validate=validationDict)
        widget.update({'object': efCycle})
        Pmw.Balloon(tab).bind(widget['object'], validationString)
        widgets.setdefault(widgetName, widget)
        widgetsOrder.append(widgetName)

        return widgetsOrder, widgets

    def buildElements(self, tab):
        widgets = {}
        widgetsOrder = []
        group = Pmw.Group(tab, tag_text='Elements')
        group.pack(fill=Tkinter.X, padx=2, pady=2)

        return widgetsOrder, widgets

if __name__ == '__main__':
    basepath = get_main_dir()

    if main_is_frozen():
        frozenpath = os.path.join(basepath, 'ebsdtools', 'hkl', 'flamenco')
    else:
        frozenpath = basepath

    cpr_path = os.path.join(frozenpath, 'cprmaster.cpr')
    ini_path = os.path.join(frozenpath, 'cprGUI.ini')
    ico_path = os.path.join(frozenpath, 'cpr.ico')

    if os.path.exists(cpr_path):
        config = readConfiguration(configfilepath=ini_path)

        root = Tkinter.Tk()
        root.title('Flamenco Wizard')
        root.resizable(0, 0)
        if platform.system() == 'Windows':
            root.iconbitmap(ico_path)

        Pmw.initialise()

        application = App(master=root
                          , masterCprFile=cpr_path
                          , loadDir=config.get('LoadDirectory', basepath)
                          , saveDir=config.get('SaveDirectory', basepath))

        for tab in config.get('Tabs', []):
            try:
                exec('tab=tab' + str(tab).capitalize() + '(application, application.addTab("' + str(tab) + '"))')
                application.updateWidgets(tab.widgets)
            except:
                tkMessageBox.showwarning(title='Invalid tab'
                                     , message='Tab ' + str(tab) + ' is invalid. Check the spelling of the tabs. The tabs should be separated with only one space.')

        if len(sys.argv) > 1:
            application.load(file=sys.argv[1])

        application.updateNotebook()
        root.update()
        root.mainloop()
    else:
        tkMessageBox.showwarning(title='File not found'
                                 , message='Could not found cprmaster.cpr in the root directory. ')
