#!/usr/bin/env python
"""
================================================================================
:mod:`mapObject` -- Helper for the CTF GUI
================================================================================

.. module:: mapObject
   :synopsis: Helper for the CTF GUI

.. inheritance-diagram:: ebsdtools.hkl.tango.mapObject

"""

# Script information for the file.
__author__ = "Philippe T. Pinard"
__email__ = "philippe.pinard@gmail.com"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2010 Philippe T. Pinard"
__license__ = "GPL v3"

# Standard library modules.
import Tkinter


# Third party modules.
from PIL import Image, ImageTk

# Local modules.
import ebsdtools.hkl.tango.colors as colors

# Globals and constants variables.

class mapTypes:
    def __init__(self, ctf, colorListPath=None):
        """
        Class where the different type of maps are calculated.
        The functions return a RGB array to be filled in an Image object
        
        :arg ctf: a ctf class containing the data
        :type ctf: :class:`ctf <HKLChannel5Tools.Tango.ctfFile.ctf>`
        
        :arg colorListPath: path for the color list csv file
        :type colorListPath: str
        """
        self.ctf = ctf
        self.colorListPath = colorListPath

    def _normalize(self, array, normalizer=255):
        """
        Normalize the value in an array to fit between 0 and the *normalized*
        
        :arg array: array to be normalized
        :type array: list
        
        :arg normalize: maximum value of the normalize array (``default=255``)
        :type normalize: int
        """
        maxValue = float(max(array))

        newArray = []
        for value in array:
            try:
                newValue = int(float(value) / maxValue * normalizer)
            except:
                newValue = 0

            newArray.append(newValue)

        return newArray

    def allEuler(self):
        """
        Return an RGB tuple where R corresponds to *euler1*, B to *euler2* and G to *euler3*.
        
        :rtype: tuple
        """
        r = self._normalize(self.ctf.getPixelArray(key='euler1', noneValue=0))
        g = self._normalize(self.ctf.getPixelArray(key='euler2', noneValue=0))
        b = self._normalize(self.ctf.getPixelArray(key='euler3', noneValue=0))

        return (r, g, b)

    def bandContrast(self):
        """
        Return a grayscale band contrast map
        
        :rtype" tuple
        """
        bc = self._normalize(self.ctf.getPixelArray(key='bc', noneValue=0))

        return (bc, bc, bc)

    def phase(self):
        """
        Return a phase map where every phase has a diffirent color
        
        :rtype: tuple
        """
        phaseColors = [(0, 0, 0)]
        colorList = colors.colorsList(self.colorListPath)
        for iPhase in range(len(self.ctf.getPhasesList())):
            phaseColors.append(colorList.getColorRGB(iPhase))

        data = self.ctf.getPixelArray(key='phase', noneValue=0)
        r = []; g = []; b = []

        for item in data:
            r.append(phaseColors[item][0])
            g.append(phaseColors[item][1])
            b.append(phaseColors[item][2])

        return (r, g, b)

class map(Tkinter.Frame):
    def __init__(self, master, size, viewSelection=True):
        """
        :class:`Tkinter.Frame` containing an image representing an EBSD map
        
        ..note:: The position of the selected pixel can be found in the class variable ``outputSelection``
        
        :arg master: root of the application
        :type master: :class:`Tkinter.Tk` or :class:`Tkinter.TopLevel` or :class:`Tkinter.Frame`
        
        :arg size: initial size of the map (width, height)
        :type size: tuple
        
        :arg viewSelection: color the pixel selected (``default=True``)
        :type viewSelection: bool
        """
        self.imageSize = size
        self.scaleFactor = 1
        self.canvasSize = (self.imageSize[0] * self.scaleFactor, self.imageSize[1] * self.scaleFactor)
        self.root = master
        self.viewSelectionCursor = viewSelection
        self.outputSelection = Tkinter.Variable()
        self.ctf = None

        #selX and selY are the position selected on teh canvas
        self.selX = 0
        self.selY = 0
        self.pixSelX = 0
        self.pixSelY = 0

        self.outputSelection.set((self.selX, self.selY))

        Tkinter.Frame.__init__(self, master=master, bg='black')

        self.imageMap = Image.new('RGB', self.canvasSize)
        self.objectMap = ImageTk.PhotoImage(self.imageMap)
        self.lblMap = Tkinter.Label(self, image=self.objectMap, bd=1, fg='white')
        self.lblMap.pack(side='left', expand='no', anchor='nw')

        self.updateSelection()
        self.bindAll()

    def bindAll(self):
        """
        Bind the click and arrows actions to their respective action
        """
        self.lblMap.bind('<ButtonRelease-1>', self.click)
        self.root.bind('<Down>', self.keyDown)
        self.root.bind('<Up>', self.keyUp)
        self.root.bind('<Left>', self.keyLeft)
        self.root.bind('<Right>', self.keyRight)

    def drawMap(self, rgb, size):
        """
        Draw a map based on the rgb tuple given to form a new image
        
        :arg rgb: rgb = ([r], [g], [b])
        :type rgb: type
        
        :arg size: size of the image (width, height)
        :type size: tuple
        """
        self.imageSize = size

        # Assert the rgb data is conformed
        assert len(rgb[0]) == len(rgb[1])
        assert len(rgb[1]) == len(rgb[2])

        # Build pixel array
        data = []
        for i in range(len(rgb[0])):
            item = (rgb[0][i], rgb[1][i], rgb[2][i])
            data.append(item)

        # Create new map
        newMap = Image.new('RGB', self.imageSize)
        newMap.putdata(data)

        self.updateImage(newMap)

    def updateImage(self, newImage=None, scaleFactor=None):
        """
        Update the map (image) display
        
        if *newImage* is given, a new image is displayed
        if *scaleFactor* is given, the size of the *newImage* or the scale of the current image is change accordingly
        
        The *scaleFactor* is an integer value that has to be greater than 1.
        
        :arg newImage: new image to display
        :type newImage: :class:`PIL.Image`
        
        :arg scaleFactor: scaling factor of the image
        :type scaleFactor: int
        """

        if scaleFactor != None: self.scaleFactor = scaleFactor
        if newImage != None: self.imageMap = newImage
        assert round(self.scaleFactor) - self.scaleFactor == 0.0

        # Resize to canvas size
        self.canvasSize = (self.imageSize[0] * self.scaleFactor, self.imageSize[1] * self.scaleFactor)
        self.imageMap = self.imageMap.resize(self.canvasSize)

        self.lblMap.pack_forget()
        self.objectMap = ImageTk.PhotoImage(self.imageMap)
        self.lblMap = Tkinter.Label(self, image=self.objectMap, bd=1, fg='white')
        self.lblMap.pack(side='left', expand='no', anchor='nw')

        self.bindAll()

    def updateSelection(self):
        """
        Update the pixel selected and update the image if *viewSelection* is *True*.
        """
        self.outputSelection.set((self.pixSelX, self.pixSelY))

        if self.viewSelectionCursor:
            newImage = self.imageMap.copy()
            pixels = newImage.load()

            cornerLeft = self.pixSelX * self.scaleFactor
            cornerTop = self.pixSelY * self.scaleFactor
            cornerRight = (cornerLeft) + self.scaleFactor
            cornerBottom = (cornerTop) + self.scaleFactor

            originalColor = pixels[cornerLeft, cornerTop]
            newColor = (255 - originalColor[0], 255 - originalColor[1], 255 - originalColor[2])

            for i in range(cornerLeft, cornerRight):
                for j in range(cornerTop, cornerBottom):
                    try:
                        pixels[i, j] = newColor
                    except:
                        pass

            self.objectMap.paste(newImage)

    def click(self, event):
        """
        Action when the button 1 of the mouse is pressed
        """
        # update of selection position
        newPixSelX = int(event.x / float(self.scaleFactor))
        newPixSelY = int(event.y / float(self.scaleFactor))

        canvasLimitX = self.canvasSize[0] / self.scaleFactor - 1
        imageLimitX = self.imageSize[0] - 1
        canvasLimitY = self.canvasSize[1] / self.scaleFactor - 1
        imageLimitY = self.imageSize[1] - 1

        lowerBoundaryX = min([canvasLimitX, imageLimitX])
        lowerBoundaryY = min([canvasLimitY, imageLimitY])

        if newPixSelX <= lowerBoundaryX and newPixSelY <= lowerBoundaryY:
            self.pixSelX = newPixSelX
            self.pixSelY = newPixSelY
            self.updateSelection()
        elif newPixSelX <= lowerBoundaryX and not newPixSelY <= lowerBoundaryY:
            self.pixSelX = newPixSelX
            self.pixSelY = newPixSelY
            self.updateSelection()
        elif not newPixSelX <= lowerBoundaryX and newPixSelY <= lowerBoundaryY:
            self.pixSelX = newPixSelX
            self.pixSelY = newPixSelY
            self.updateSelection()

    def keyUp(self, event):
        """
        Action when the up arrow is pressed
        """
        # update of selection position
        newPixSelY = self.pixSelY - 1

        if newPixSelY >= 0:
            self.pixSelY = newPixSelY
            self.updateSelection()

    def keyDown(self, event):
        """
        Action when the down arrow is pressed
        """
        # update of selection position
        newPixSelY = self.pixSelY + 1

        canvasLimit = self.canvasSize[1] / self.scaleFactor - 1
        imageLimit = self.imageSize[1] - 1

        lowerBoundaryY = min([canvasLimit, imageLimit])

        if newPixSelY <= (lowerBoundaryY):
            self.pixSelY = newPixSelY
            self.updateSelection()

    def keyLeft(self, event):
        """
        Action when the left arrow is pressed
        """
        # update of selection position
        newPixSelX = self.pixSelX - 1

        if newPixSelX >= 0:
            self.pixSelX = newPixSelX
            self.updateSelection()

    def keyRight(self, event):
        """
        Action when the right arrow is pressed
        """
        # update of selection position
        newPixSelX = self.pixSelX + 1

        canvasLimit = self.canvasSize[0] / self.scaleFactor - 1
        imageLimit = self.imageSize[0] - 1

        lowerBoundaryX = min([canvasLimit, imageLimit])

        if newPixSelX <= (lowerBoundaryX):
            self.pixSelX = newPixSelX
            self.updateSelection()

class App:
    def __init__(self, master, ctf):
        mapFrame = map(root, (50, 50))
        mapFrame.pack(fill='both', expand='yes')

        lblInfo = Tkinter.Label(master, textvariable=mapFrame.outputSelection)
        lblInfo.pack()

        t = mapTypes(ctf)
        mapFrame.drawMap(t.phase(), (ctf.getWidth(), ctf.getHeight()))
    #    self.f.drawMap(t.allEuler(), (self.ctf.getWidth(), self.ctf.getHeight()))
    #    self.f.drawMap(t.bandContrast(), (self.ctf.getWidth(), self.ctf.getHeight()))

    def action(self, *event):
        print 'action'

if __name__ == '__main__':
    import ebsdtools.hkl.tango.ctfFile as ctfFile

    root = Tkinter.Tk()
    ctf = ctfFile.ctf('testdata/test_ctfFile.ctf')

    app = App(root, ctf)

    root.mainloop()


