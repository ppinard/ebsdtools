#!/usr/bin/env python
"""
================================================================================
:mod:`colors` -- List of colours
================================================================================

.. module:: colors
   :synopsis: List of colours

.. inheritance-diagram:: ebsdtools.hkl.tango.colors

"""

# Script information for the file.
__author__ = "Philippe T. Pinard"
__email__ = "philippe.pinard@gmail.com"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2010 Philippe T. Pinard"
__license__ = "GPL v3"

# Standard library modules.
import os.path
import csv

# Third party modules.

# Local modules.

def RGB255toRGB1(r, g, b):
    """
      Convert rgb in 255 range to a rgb tuple in 1.0 range
      e.g. (255, 255, 0) -> (1.0, 1.0, 0.0)
    """
    return (r / 255.0, g / 255.0, b / 255.0)

class colorsList:
    def __init__(self, filepath=None):
        if filepath == None:
            basedir = os.path.dirname(__file__)
            filepath = os.path.join(basedir, 'colors.csv')

        rows = csv.reader(open(filepath, 'r'), dialect=csv.excel)
        self.__buildColorList(rows)
        self.maxIndex = len(self.colorList) - 1

    def __buildColorList(self, rows):
        self.colorList = []

        for row in rows:
            r = int(row[0])
            g = int(row[1])
            b = int(row[2])
            name = row[3]

            self.colorList.append({'name': name, 'rgb': (r, g, b)})

    def getColorRGB(self, index):
        return self.colorList[index % self.maxIndex]['rgb']

    def getColorName(self, index):
        return self.colorList[index]['name']

def formatFortran():
    """
      Used to format a file from Penelope Color code
    """
    file = open(r'C:\Documents and Settings\ppinard\Desktop\color', 'r')
    file2 = csv.writer(open(r'C:\Documents and Settings\ppinard\Desktop\colors.csv', 'w'), lineterminator='\n')

    for line in file.readlines():
        b = line[15:18]
        g = line[29:32]
        r = line[43:46]
        name = line[50:-2]

        file2.writerow([r, g, b, name])

if __name__ == '__main__':
    colors = colorsList()
    for i in range(10):
        print colors.getColorRGB(i), colors.getColorName(i)
