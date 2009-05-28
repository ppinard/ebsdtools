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
      
      if config.has_option(location, "jython_lib"):
        self.jython_lib = config.get(location, "jython_lib")
      
      if config.has_option(location, "prefix"):
        self.prefix = config.get(location, "prefix")
        
      if config.has_option(location, "filetype"):
        self.filetype = config.get(location, "filetype")
      
      if config.has_option(location, "username"):
        self.username = config.get(location, "username")
      
      if config.has_option(location, "password"):
        self.password = config.get(location, "password")
      
      if config.has_option(location, "download_location"):
        self.download_location = config.get(location, "download_location")

def update(location):
  """
  There are two types of location: ftp or local
  They are defined in the configuration file
  """
  configurationFile = os.path.join(os.path.dirname(__file__), 'rmlimage_update.cfg')
  config = UpdateConfiguration(configurationFile=configurationFile
                               , location=location)
  
  if location == 'ftp':
    server = ftp.FTP(host = config.source
                     , username = config.username
                     , password = config.password)
    
    distros = server.directoryListing('distro/')['files'].keys()
    files = []
    for distro in distros:
      if config.prefix in distro:
        files.append(distro)
    
    lastVersionFilename = sorted(files)[-1]
    server.download('distro/%s' % lastVersionFilename, config.download_location)
    lastVersion = os.path.join(config.download_location, lastVersionFilename)
  elif location == 'local':
    files = glob.glob(os.path.join(config.source, '%s*.%s' % (config.prefix, config.filetype)))
    lastVersion = sorted(files)[-1]
  
  #Read zip
  print lastVersion
  zip = myzip.reader(filename=lastVersion, debug=True)
  
  #Remove and create source folder
  rml_folder = os.path.join(config.jython_lib, 'rml/')
  if os.path.exists(rml_folder): shutil.rmtree(rml_folder)
  os.mkdir(rml_folder)
  
  #Extract zip
  zip.extractAll(rml_folder)
  zip.close()
  
  #Extract jar
  jarFiles = glob.glob(os.path.join(rml_folder, '*.jar'))
  for jarFile in jarFiles:
    zip = myzip.reader(filename=jarFile, debug=True)
    zip.extractAll(rml_folder)
    zip.close()
  
  #Copy main jar to uniform jar name
  mainjar = glob.glob(os.path.join(rml_folder, 'rml-image_ebsd*.jar'))[0]
  print mainjar
  shutil.copy(mainjar, os.path.join(rml_folder, 'rml-image_ebsd.jar'))
  
  #Remove folders in library path
  rmlimage_folder = os.path.join(config.jython_lib, 'rmlimage/')
  if os.path.exists(rmlimage_folder): shutil.rmtree(rmlimage_folder)
  
  rmlshared_folder = os.path.join(config.jython_lib, 'rmlshared/')
  if os.path.exists(rmlshared_folder): shutil.rmtree(rmlshared_folder)
  
  microscope_folder = os.path.join(config.jython_lib, 'microscope/')
  if os.path.exists(microscope_folder): shutil.rmtree(microscope_folder)
  
  shutil.move(os.path.join(rml_folder, 'rmlimage/'), rmlimage_folder)
  shutil.move(os.path.join(rml_folder, 'rmlshared/'), rmlshared_folder)
  shutil.move(os.path.join(rml_folder, 'microscope/'), microscope_folder)

if __name__ == '__main__':
  print __file__
  update('ftp')
