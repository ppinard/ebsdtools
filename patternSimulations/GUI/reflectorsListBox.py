#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = 'Philippe Pinard (philippe.pinard@gmail.com)'
__version__ = ""
__date__ = "2008-07-13"
__copyright__ = "Copyright (c) 2008"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = ""
__svnDate__ = ""
__svnId__ = ""

# Standard library modules.
import Tkinter

# Third party modules.

# Local modules.

class reflectorsListBox(Tkinter.Frame):
  def __init__(self, master, reflectorsInfo, **args):
    
    Tkinter.Frame.__init__(self, master, **args)
    
    #Setup of scrollbar and canvas
    vscrollbar = Tkinter.Scrollbar(self)
    vscrollbar.grid(row=1, column=1, sticky='ns')
    
    self.canvas = Tkinter.Canvas(self
                                 , width=15
                                 , yscrollcommand=vscrollbar.set)
    
    self.canvas.grid(row=1, column=0, sticky='nsew')
    vscrollbar.config(command=self.canvas.yview)
    
    self.grid_rowconfigure(1, weight=1)
    self.grid_columnconfigure(0, weight=1)
    
    self.frame = Tkinter.Frame(self.canvas, relief='flat', bd=0)
    
    #Setup of variables
    self.entries = {}
    self.reflectorsInfo = reflectorsInfo
    
    #Setup of header
    headerFrame = Tkinter.Frame(self)
    headerFrame.grid(row=0, column=0, columnspan=2, sticky='nsew')
    
    headerColor = Tkinter.Label(headerFrame
                                  , text = ' '
                                  , relief = 'raised'
                                  , width=5)
    headerColor.pack(side='left', anchor='w', fill='x', expand='no')
    
    headerIndices = Tkinter.Label(headerFrame
                             , text = 'Indices'
                             , relief = 'raised'
                             , width=10)
    headerIndices.pack(side='left', anchor='w', fill='x', expand='no')
    
    headerIntensity = Tkinter.Label(headerFrame
                             , text = 'Intensity (%)'
                             , relief = 'raised'
                             , width=10)
    headerIntensity.pack(side='left', anchor='w', fill='x', expand='no')
    
    headerScrollbar = Tkinter.Label(headerFrame
                                 , text = '   '
                                 , relief = 'raised'
                                 , width=2)
    headerScrollbar.pack(side='left', anchor='w', fill='x', expand='no')
    
    self.canvas.create_window(0, 0, anchor='nw', window=self.frame)
    self._updateScrolling()
    
    self.update()
  
  def _updateScrolling(self):
    self.frame.update_idletasks()
    self.canvas.config(scrollregion=self.canvas.bbox("all"))

  def addEntry(self, reflectorInfo):
    idEntry = len(self.entries)
    self.entries.setdefault(idEntry, {})
    
    self.entries[idEntry]['frame'] = Tkinter.Frame(self.frame, bg='white')
    self.entries[idEntry]['frame'].pack(side='top', anchor='nw', fill='both', expand='yes')
    
    rgb = reflectorInfo['rgb']
    color = "#%02x%02x%02x" % (rgb[0], rgb[1], rgb[2])
    
    self.entries[idEntry]['canvasColor'] = Tkinter.Label(self.entries[idEntry]['frame']
                                                   , width=4
                                                   , bg=color
                                                   , bd=4
                                                   , relief='flat'
                                                   , highlightthickness=0)
    self.entries[idEntry]['canvasColor'].pack(side='left', anchor='w', fill='x', expand='yes')
    
    self.entries[idEntry]['lblIndices'] = Tkinter.Label(self.entries[idEntry]['frame']
                                                   , text=reflectorInfo['indices']
                                                   , relief='flat'
                                                   , bg='white'
                                                   , width=9
                                                   , bd=4)
    self.entries[idEntry]['lblIndices'].pack(side='left', anchor='w', fill='x', expand='yes')
    
    intensity_text = '%4.2f' % (reflectorInfo['intensity']*100)
    
    self.entries[idEntry]['lblIntensity'] = Tkinter.Label(self.entries[idEntry]['frame']
                                                   , text=intensity_text
                                                   , relief='flat'
                                                   , bg='white'
                                                   , width=9
                                                   , bd=4)
    self.entries[idEntry]['lblIntensity'].pack(side='left', anchor='w', fill='x', expand='yes')

  def update(self):
    self.clear()
    
    for reflectorInfo in self.reflectorsInfo:
      self.addEntry(reflectorInfo)
    
    self._updateScrolling()
    
  def clear(self):
    for idEntry in self.entries.keys():
      self.entries[idEntry]['frame'].destroy()
      del self.entries[idEntry]

class App:
  def __init__(self, root):
    
    reflectors = [{'indices': (1,1,0), 'intensity': 1, 'rgb':(255,0,0)},
                  {'indices': (1,0,0), 'intensity': 1, 'rgb':(0,255,0)},
                  {'indices': (1,0,1), 'intensity': 1, 'rgb':(0,0,255)}]
    
    lstReflectors = reflectorsListBox(root, reflectors)
    lstReflectors.pack(fill='both', expand='yes')


if __name__ == '__main__':
  root = Tkinter.Tk()
  
  App(root)
  
  root.mainloop()