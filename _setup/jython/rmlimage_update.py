#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Philippe Pinard (philippe.pinard@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2009 Philippe Pinard"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = ""
__svnDate__ = ""
__svnId__ = ""

# Standard library modules.
import os
import glob
import ConfigParser
import shutil

# Third party modules.

# Local modules.
import InternetTools.ftp.ftp as ftp
import RandomUtilities.zipTools.myzip as myzip
import DrixUtilities.Files as Files

class UpdateConfiguration:
  def __init__(self
               , configurationFile
               , location):
    self._readConfiguration(configurationFile, location)
    self.location = location

  def _readConfiguration(self, configurationFile, location):
    config = ConfigParser.SafeConfigParser()
    config.readfp(open(configurationFile, 'r'))

    if config.has_section(location):
      if config.has_option(location, "source"):
        self.source = config.get(location, "source")

      if config.has_option(location, "path_lib"):
        self.path_lib = config.get(location, "path_lib")

      if config.has_option(location, "prefix_lib"):
        self.prefix_lib = config.get(location, "prefix_lib")

      if config.has_option(location, "path_gui"):
        self.path_gui = config.get(location, "path_gui")

      if config.has_option(location, "prefix_gui"):
        self.prefix_gui = config.get(location, "prefix_gui")

      if config.has_option(location, "filetype"):
        self.filetype = config.get(location, "filetype")

      if config.has_option(location, "username"):
        self.username = config.get(location, "username")

      if config.has_option(location, "password"):
        self.password = config.get(location, "password")

      if config.has_option(location, "download_location"):
        self.download_location = config.get(location, "download_location")

def updateJythonLib(location):
  """
  There are two types of location: ftp or local
  They are defined in the configuration file
  """
  configurationFile = Files.getCurrentModulePath(__file__, 'rmlimage_update.cfg')
  config = UpdateConfiguration(configurationFile=configurationFile
                               , location=location)

  if location == 'ftp':
    server = ftp.FTP(host = config.source
                     , username = config.username
                     , password = config.password)

    distros = server.directoryListing('distro/')['files'].keys()
    files = []
    for distro in distros:
      if config.prefix_lib in distro:
        files.append(distro)

    lastVersionFilename = sorted(files)[-1]
    server.download('distro/%s' % lastVersionFilename, config.download_location)
    lastVersion = os.path.join(config.download_location, lastVersionFilename)
  elif location == 'local':
    files = glob.glob(os.path.join(config.source, '%s*.%s' % (config.prefix_lib, config.filetype)))
    lastVersion = sorted(files)[-1]

  #Read zip
  print lastVersion
  zip = myzip.reader(filename=lastVersion, debug=True)

  #Remove and create source folder
  rml_folder = config.path_lib
  if os.path.exists(rml_folder): shutil.rmtree(rml_folder)
  os.mkdir(rml_folder)

  #Extract zip
  zip.extractAll(rml_folder)
  zip.close()

#  #Copy main jar to uniform jar name
  mainjar = glob.glob(os.path.join(rml_folder, 'rml-image_ebsd*.jar'))[0]
  print mainjar
  os.rename(mainjar, os.path.join(rml_folder, 'rml-image_ebsd.jar'))

def updateProgram(location):
  """
  There are two types of location: ftp or local
  They are defined in the configuration file
  """
  configurationFile = Files.getCurrentModulePath(__file__, 'rmlimage_update.cfg')
  config = UpdateConfiguration(configurationFile=configurationFile
                               , location=location)

  if location == 'ftp':
    server = ftp.FTP(host = config.source
                     , username = config.username
                     , password = config.password)

    distros = server.directoryListing('distro/')['files'].keys()
    files = []
    for distro in distros:
      if config.prefix_gui in distro:
        files.append(distro)

    lastVersionFilename = sorted(files)[-1]
    server.download('distro/%s' % lastVersionFilename, config.download_location)
    lastVersion = os.path.join(config.download_location, lastVersionFilename)
  elif location == 'local':
    files = glob.glob(os.path.join(config.source, '%s*.%s' % (config.prefix_gui, config.filetype)))
    lastVersion = sorted(files)[-1]

  #Read zip
  print lastVersion
  zip = myzip.reader(filename=lastVersion, debug=True)

  #Remove and create source folder
  rml_folder = config.path_gui
  if os.path.exists(rml_folder): shutil.rmtree(rml_folder)
  os.mkdir(rml_folder)

  #Extract zip
  zip.extractAll(rml_folder)
  zip.close()

if __name__ == '__main__':
  updateJythonLib('ftp')
  updateProgram('ftp')
