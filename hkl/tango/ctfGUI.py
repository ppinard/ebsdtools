#!/usr/bin/env python
"""
================================================================================
:mod:`ctfGUI` -- Viewer of CTF file
================================================================================

.. module:: ctfGUI
   :synopsis: Viewer of CTF file

.. inheritance-diagram:: ebsdtools.hkl.tango.ctfGUI

"""

# Script information for the file.
__author__ = "Philippe T. Pinard"
__email__ = "philippe.pinard@gmail.com"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2010 Philippe T. Pinard"
__license__ = "GPL v3"

# Standard library modules.
import os
import sys
import Tkinter
import tkFileDialog
import tkMessageBox
import ConfigParser
import platform

# Third party modules.
from PIL import Image, ImageTk

# Local modules.
import tkintertools.Pmw.Pmw as Pmw

from guitools.py2exe import get_main_dir, main_is_frozen

import ebsdtools.hkl.tango.ctfFile as ctfFile
import ebsdtools.hkl.tango.mapObject as mapObject

def readConfiguration(configfilepath='ctfGUI.ini'):
    """
    Read configuration file and return a dictionary with the inputs
    
    The configuration file contains the initial directory to load and save files
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

        return config
    else:
        tkMessageBox.showwarning(title='File not found',
                                 message='Could not found ' + str(configfilepath) + ' in the root directory. The default values will be used')

class App:
    def __init__(self, master, windowSize, loadDir, saveDir, colorListPath):
        """
        GUI application to visualize ctf file
        
        :arg master: root of the application
        :type master: :class:`Tkinter.Tk` or :class:`Tkinter.TopLevel`
        
        :arg windowSize: initial window size for the map (width, height)
        :type windowSize: tuple
        
        :arg loadDir: initial directory to load ctf file
        :type loadDir: str
        
        :arg saveDir: initial directory to save patterns
        :type saveDir: str
        
        :arg colorListPath: path for the color list csv file
        :type colorListPath: str
        """
        self.root = master
        self.windowSize = windowSize
        self.pattSize = (336, 256) #equivalent 8x8 binning

        #The map type corresponds to what information is displayed from the EBSD map
        self.mapType = None
        self.mapTypeValue = Tkinter.StringVar()

        self.zoomValue = Tkinter.StringVar()

        #Track which pixel is selected
        self.pixelSelected = Tkinter.StringVar()
        self.pixelSelectedText = Tkinter.StringVar()
        self.pixelSelectedInfoText = Tkinter.StringVar()

        self.filepath = Tkinter.StringVar()
        self.currentLoadDirectory = loadDir
        self.currentSaveDirectory = saveDir

        self.colorListPath = colorListPath

        self.ctf = None

        frmButtons = Tkinter.Frame(master)
        frmButtons.pack(side='top', fill='x', expand='no', anchor='n')

        btnLoad = Tkinter.Button(frmButtons, text="Load", command=self.load)
        btnLoad.pack(side='left', expand='yes', fill='x')

        btnSave = Tkinter.Button(frmButtons, text="Save Pattern", command=self.savePatt)
        btnSave.pack(side='left', expand='yes', fill='x')

        btnExit = Tkinter.Button(frmButtons, text="Exit", command=self.exit)
        btnExit.pack(side='left', expand='yes', fill='x')

        frmOptions = Tkinter.Frame(master)
        frmOptions.pack(side='top', fill='x', expand='no', anchor='n')

        lblFilename = Tkinter.Label(frmOptions, textvariable=self.filepath)
        lblFilename.pack(side='top', fill='x', expand='yes', anchor='w')

        frmPatternRoot = Tkinter.Frame(frmOptions)
        frmPatternRoot.pack(side='top', fill='x', expand='yes', anchor='w')

        lblPatternRoot = Tkinter.Label(frmPatternRoot
                                      , text='Images Directory'
                                      , justify='left')
        lblPatternRoot.pack(side='left', anchor='nw', expand='no')

        self.varPatternRoot = Tkinter.StringVar()

        txtPatternRoot = Tkinter.Entry(frmPatternRoot
                                           , textvariable=self.varPatternRoot
                                           , width=80)
        txtPatternRoot.pack(side='left', anchor='nw', fill='x', expand='yes')

        #    btnPatternRootChange = Tkinter.Button(frmPatternRoot
        #                                              , text='Change...'
        #                                              , command=lambda func=self.btnPatternRootChange_Command: func())
        #    btnPatternRootChange.pack(side='left', anchor='nw', fill='x', expand='no')

        frmSelection = Tkinter.Frame(master)
        frmSelection.pack(side='top', fill='x', expand='no', anchor='n')

        comboType = Pmw.OptionMenu(frmSelection
                               , labelpos=Tkinter.W
                               , label_text='Map Type:'
                               , menubutton_textvariable=self.mapTypeValue
                               , items=('All Euler', 'Band Contrast', 'Phase')
                               , initialitem='All Euler')
        comboType.pack(side='left', fill='x', expand='yes', anchor='w')

        comboType = Pmw.OptionMenu(frmSelection
                               , labelpos=Tkinter.W
                               , label_text='Zoom:'
                               , menubutton_textvariable=self.zoomValue
                               , items=('1X', '2X', '5X', '10X', '20X', '50X')
                               , initialitem='1X')
        comboType.pack(side='left', fill='x', expand='yes', anchor='w')

        frmInfos = Tkinter.Frame(master)
        frmInfos.pack(side='top', fill='x', expand='no', anchor='n')

        lblSelectedPixel = Tkinter.Label(frmInfos, textvariable=self.pixelSelectedText)
        lblSelectedPixel.pack(side='top', fill='x', expand='yes', anchor='n')

        lblSelectedPixelInfo = Tkinter.Label(frmInfos, textvariable=self.pixelSelectedInfoText)
        lblSelectedPixelInfo.pack(side='top', fill='x', expand='yes', anchor='n')

        self.map = mapObject.map(master, windowSize)
        self.pixelSelected = self.map.outputSelection
        self.pixelSelected.trace('w', self.updateSelection)
        self.map.pack(side='top', fill='both', expand='yes', anchor='nw')

        self.pattImage = Image.new('RGB', self.pattSize)
        pattFrame = Tkinter.Frame(master, bg='black')
        self.pattObject = ImageTk.PhotoImage(self.pattImage)
        lblPatt = Tkinter.Label(pattFrame, image=self.pattObject, bd=1, fg='white')
        lblPatt.pack(side='left', anchor='nw')
        pattFrame.pack(side='top', fill='x', expand='no', anchor='nw')

        #Track changes
        self.mapTypeValue.trace('w', self.updateMap)
        self.zoomValue.trace('w', self.updateMap)

    def load(self, file=None):
        """
        Load a ctf file
        
        If a *file* is given, the file is automatically loaded.
        Otherwise, a file dialog is displayed.
        
        :arg file: file path of a ctf file
        :type file: str
        """
        if file == None:
            file = tkFileDialog.askopenfile(parent=self.root, initialdir=self.currentLoadDirectory, mode='r', filetypes=[('Channel Text File', '*.ctf')], title='Choose a file')
            if file != None:
                file = file.name

        if file != None:
            self.filepath.set(os.path.split(file)[1])
            self.currentLoadDirectory = os.path.split(file)[0]
            self.ctf = ctfFile.ctf(file)
            self.varPatternRoot.set(self.ctf.getProjectImagesFolderPath())

            self.pattImage = Image.new('RGB', self.pattSize)
            self.pattObject.paste(self.pattImage)

            self.mapType = mapObject.mapTypes(self.ctf, self.colorListPath)
            self.updateMap()

    def savePatt(self):
        """
        Save the selected pattern.
        A directory dialog is displayed to select where to save the pattern.
        """
        dir = tkFileDialog.askdirectory(parent=self.root, initialdir=self.currentSaveDirectory, title='Please select a directory')

        if dir != '':
            self.currentSaveDirectory = dir
            out = self.pattImage.resize(self.pattSize)

            out.save(os.path.join(dir, self.pattTextInfo + '.jpg'))

    def exit(self):
        """
        Exit the application
        """
        self.root.destroy()

    def btnPatternRootChange_Command(self):
        """
        Change the directory where the pattern images are located.
        The default value comes from the ctf file.
        """
        dir = tkFileDialog.askdirectory(parent=self.root, initialdir=self.varPatternRoot.get(), title='Please select a directory')

        if dir != '':
            self.varPatternRoot.set(dir)

    def updateMap(self, *k):
        """
        Update the map when the type or the zoom is changed
        """
        if self.mapType != None:
            if self.mapTypeValue.get() == 'All Euler':
                rgb = self.mapType.allEuler()
            elif self.mapTypeValue.get() == 'Band Contrast':
                rgb = self.mapType.bandContrast()
            elif self.mapTypeValue.get() == 'Phase':
                rgb = self.mapType.phase()

            self.map.drawMap(rgb, (self.ctf.getWidth(), self.ctf.getHeight()))

        zoomStr = self.zoomValue.get()
        if len(zoomStr) > 0:
            zoom = float(zoomStr[:-1])
            self.map.updateImage(scaleFactor=int(zoom))

    def updateSelection(self, *k):
        """
        Update the information from the selected pixel every time a new pixel is selected.
        """
        if self.ctf != None:
            posX, posY = self.pixelSelected.get()
            self.updatePatt(posX, posY)
            imageNumber = self.ctf.getPixelIndexLabel(coord=(posX, posY))

            pixelSelectedText = '(%i, %i) # %s' % (posX, posY, imageNumber)
            self.pixelSelectedText.set(pixelSelectedText)

            pixelInfo = self.ctf.getPixelResults_coordinate((posX, posY))

            if pixelInfo['phase'] != 0:
                phase = self.ctf.getPhaseName(pixelInfo['phase'])
            else:
                phase = 'N/A'
                error = pixelInfo['error']

            if phase != 'N/A':
                pixelSelectedInfoText = 'Phase=%s, MAD=%.4f, BC=%i, BS=%i' % (phase, pixelInfo['mad'], pixelInfo['bc'], pixelInfo['bs'])
            else:
                pixelSelectedInfoText = 'Error=%s, MAD=%.4f, BC=%i, BS=%i' % (error, pixelInfo['mad'], pixelInfo['bc'], pixelInfo['bs'])

            self.pixelSelectedInfoText.set(pixelSelectedInfoText)

            if phase == 'N/A': phase = 'None'
            projectName = self.ctf.getProjectName()
            self.pattTextInfo = '%s%s_%s' % (projectName, imageNumber, str(phase))

    def updatePatt(self, posX, posY):
        """
        Update the pattern displayed based on the pixel selected.
        """
        imageFolder = os.path.split(self.varPatternRoot.get())[-1]
        imageFile = '%s%s.jpg' % (imageFolder.replace('Images', ''), self.ctf.getPixelIndexLabel(coord=(posX, posY)))
        imagePath = os.path.join(self.varPatternRoot.get(), imageFile)

        if os.path.exists(imagePath):
            newPattImage = Image.open(imagePath)
            newPattImage = newPattImage.resize(self.pattSize)

            self.pattObject.paste(newPattImage)
            self.pattImage = newPattImage

if __name__ == '__main__':
    basepath = get_main_dir()

    if main_is_frozen():
        frozenpath = os.path.join(basepath, 'ebsdtools', 'hkl', 'tango')
    else:
        frozenpath = basepath

    ini_path = os.path.join(frozenpath, 'ctfGUI.ini')
    ico_path = os.path.join(frozenpath, 'ctf.ico')
    colors_path = os.path.join(frozenpath, 'colors.csv')

    config = readConfiguration(configfilepath=ini_path)

    root = Tkinter.Tk()
    root.title('pyTango')
    root.resizable(0, 0)
    if platform.system() == 'Windows':
        root.iconbitmap(ico_path)

    Pmw.initialise()

    windowSize = (50, 50)
    application = App(master=root
                        , windowSize=windowSize
                        , loadDir=config.get('LoadDirectory', basepath)
                        , saveDir=config.get('SaveDirectory', basepath)
                        , colorListPath=colors_path)

    if len(sys.argv) > 1:
        application.load(file=sys.argv[1])

    root.mainloop()
