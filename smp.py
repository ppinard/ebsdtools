#!/usr/bin/env python
"""
================================================================================
:mod:`smp` -- Reader of stream maps file format (SMP)
================================================================================

.. module:: smp
   :synopsis: Reader of stream maps file format (SMP)
.. moduleauthor:: Philippe Pinard <philippe.pinard@mail.mcgill.ca>

.. inheritance-diagram:: ebsdtools.smp

Reads a series of maps saved in the "proprietary" SMP format. 
All the maps will have the same type and the same dimensions.

The file format is pretty straightforward. 
The first three bytes are 83, 77 and 80 which translate to SMP. 
The next byte is the version label. 
The next byte is the number of characters of the full class name of the
maps in the file. 
The next bytes represent the full class name of the maps held in the file. 
The rest of the file consists of a series of numbers saved in Java binary format. 
The first two numbers are the width and the height of the maps in integer format. 
Then comes the index of the first map (useful for split SMP files) in integer format. 
The rest of the file is filled with the values of the maps sequentially. 

"""

# Script information for the file.
__author__ = "Philippe Pinard (philippe.pinard@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2010 Philippe Pinard"
__license__ = ""

# Standard library modules.
import logging
import struct

# Third party modules.
import Image

# Local modules.

# Globals and constants variables.
from os import SEEK_END

class Reader:
    def __init__(self, f):
        """
        Reads a SMP file.
        
        :arg f: file-object
        """
        self._f = f

        # Validate header
        header = f.read(3)
        if header != 'SMP':
            raise IOError, "The file is not a stream map"

        # Read version
        version = int(f.read(1))
        logging.debug("Version: %i" % version)

        # Read the map type
        maptype_length = struct.unpack('b', f.read(1))[0]
        self._maptype = f.read(maptype_length)
        logging.debug("Map type: %s" % self._maptype)

        # For now
        if not self._maptype.endswith('ByteMap'):
            raise IOError, "Invalid map type (%s). Only ByteMap is supported." % \
                    self._maptype

        # Read the dimensions of the Maps
        self._width = struct.unpack('>i', f.read(4))[0]
        self._height = struct.unpack('>i', f.read(4))[0]
        self._size = self.width * self.height
        logging.debug("Maps' width: %i" % self.width)
        logging.debug("Maps' height: %i" % self.height)
        logging.debug("Maps' size: %i" % self.size)

        # If it is an SMP2, read the index of the first Map in the file
        if version == 1:
            self._start_index = 0
            #= "SMP#" + classNameLength + className + width + height
            self._header_length = 4 + 1 + maptype_length + 4 + 4
        elif version == 2:
            self._start_index = struct.unpack('>i', f.read(4))[0]
            # "SMP#" + classNameLength + className + width + height + startIndex
            self._header_length = 4 + 1 + maptype_length + 4 + 4 + 4
        else:
            raise IOError, "Invalid SMP version (%i)" % version

        logging.debug("Start index: %s" % self.start_index)

        # Number of maps
        f.seek(0, SEEK_END)
        file_length = f.tell()
        self._maps_count = int((file_length - self._header_length) / self.size)
        assert (file_length - self._header_length) % self.size == 0, \
            "Too many bytes (%i)" % (file_length - self._header_length) % self.size
        logging.debug("Maps count: %i" % len(self))

        # Iterator
        self._current_index = self._start_index - 1

    def __iter__(self):
        return self

    def __len__(self):
        """
        Number of maps.
        """
        return self._maps_count

    def __call__(self, index):
        return self.read(index)

    @property
    def width(self):
        """
        Width of the maps.
        """
        return self._width

    @property
    def height(self):
        """
        Height of the maps.
        """
        return self._height

    @property
    def size(self):
        """
        Size of the maps (width times height).
        """
        return self._size

    @property
    def start_index(self):
        """
        Index of the first map.
        """
        return self._start_index

    @property
    def end_index(self):
        """
        Index of the last map.
        """
        return self.start_index + len(self) - 1

    def close(self):
        """
        Closes the reader.
        """
        self._f.close()

    def read(self, index):
        """
        Reads the map at the specified *index* and returns a PIL Image.
        
        :arg index: index of the map
        
        :return: a PIL image
        """
        if index < self.start_index or index > self.end_index:
            raise IndexError, "Index (%i) must between %i and %i." % \
                    (index, self.start_index, self.end_index)

        self._f.seek((index - self.start_index) * self.size + self._header_length)

        if self._maptype == 'rmlimage.core.ByteMap':
            mode = "L"

        size = (self.width, self.height)
        data = self._f.read(self.size)
        return Image.frombuffer(mode, size, data, "raw", mode, 0, 1)

    def next(self):
        if self._current_index >= self.end_index:
            raise StopIteration
        self._current_index += 1
        return self.read(self._current_index)


reader = Reader

def export_to_hkl(reader, project_name, outputdir):
    """
    Exports all the images in a SMP to single files in a folder to be used by
    HKL Channel 5.
    
    :arg reader: smp reader
    :arg project_name: name of the project
    :arg outputdir: output directory
    """
    import os

    outputdir = os.path.join(outputdir, project_name + "Images")
    if not os.path.exists(outputdir):
        os.makedirs(outputdir)

    width = len(str(len(reader)))
    for index, im in enumerate(reader):
        index += reader.start_index
        filename = project_name + str(index).zfill(width)

        im.save(os.path.join(outputdir, filename + ".jpg"))

        if index % 1000 == 0:
            progress = float(index) / len(reader) * 100.0
            print "Progress: %4.2f" % progress

