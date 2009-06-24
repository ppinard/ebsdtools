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
import optparse

# Third party modules.

# Local modules.
import InternetTools.ftp.ftp as ftp
import RandomUtilities.zipTools.myzip as myzip
import DrixUtilities.Files as Files

# Globals and constants variables.
SOURCE_LOCAL = 'local'
SOURCE_REMOTE = 'remote'

class UpdateConfiguration:
  def __init__(self
               , configurationFile
               , source):
    self._readConfiguration(configurationFile, source)
    self.source = source

  def _readConfiguration(self, configurationFile, source):
    config = ConfigParser.SafeConfigParser()
    config.readfp(open(configurationFile, 'r'))

    if config.has_section(source):
      if config.has_option(source, "location"):
        self.location = config.get(source, "location")

      if config.has_option(source, "path_lib"):
        self.path_lib = config.get(source, "path_lib")

      if config.has_option(source, "prefix_lib"):
        self.prefix_lib = config.get(source, "prefix_lib")

      if config.has_option(source, "path_gui"):
        self.path_gui = config.get(source, "path_gui")

      if config.has_option(source, "prefix_gui"):
        self.prefix_gui = config.get(source, "prefix_gui")

      if config.has_option(source, "filetype"):
        self.filetype = config.get(source, "filetype")

      if config.has_option(source, "username"):
        self.username = config.get(source, "username")

      if config.has_option(source, "password"):
        self.password = config.get(source, "password")

      if config.has_option(source, "download_location"):
        self.download_location = config.get(source, "download_location")

def updateJythonLib(source):
  """
  There are two types of source: remote or local
  They are defined in the configuration file
  """
  configurationFile = Files.getCurrentModulePath(__file__, 'rmlimage_update.cfg')
  config = UpdateConfiguration(configurationFile=configurationFile
                               , source=source)

  if source == SOURCE_REMOTE:
    server = ftp.FTP(host = config.location
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
  elif source == SOURCE_LOCAL:
    files = glob.glob(os.path.join(config.location, '%s*.%s' % (config.prefix_lib, config.filetype)))
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

def updateProgram(source):
  """
  There are two types of source: remote or local
  They are defined in the configuration file
  """
  configurationFile = Files.getCurrentModulePath(__file__, 'rmlimage_update.cfg')
  config = UpdateConfiguration(configurationFile=configurationFile
                               , source=source)

  if source == SOURCE_REMOTE:
    server = ftp.FTP(host = config.location
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
  elif source == SOURCE_LOCAL:
    files = glob.glob(os.path.join(config.location, '%s*.%s' % (config.prefix_gui, config.filetype)))
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

def main():
  usage = "Usage: %prog [options]\n Update the local folder with newer version of RML-Image."
  parser = optparse.OptionParser(usage=usage)
  parser.add_option("-l"
                    , "--local"
                    , action="store_true"
                    , dest="local"
                    , help="Update from the local source")
  parser.add_option("-r"
                    , "--remote"
                    , action="store_true"
                    , dest="remote"
                    , help="Update from the remote source (ftp) (default)")

  (options, args) = parser.parse_args()

  if options.remote:
    source = SOURCE_REMOTE
  elif options.local:
    source = SOURCE_LOCAL
  else:
    source = SOURCE_REMOTE

  print source
  updateJythonLib(source)
  updateProgram(source)

if __name__ == '__main__':
  main()
