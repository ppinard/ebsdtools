#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Philippe Pinard (philippe.pinard@gmail.com)"
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
import optparse
import random

# Third party modules.

# Local modules.
import CasirTools
import CasirTools.database as database
import CasirTools.launcher as launcher

import DrixUtilities.Files as Files

import HKLChannel5Tools.Tango.ctfFile as ctfFile

import DeformationSamplePrep.qualityIndexes.configuration as configuration

# Globals and constants variables.
AUTHOR_FIRSTNAME = 'Philippe'
AUTHOR_LASTNAME = 'Pinard'
AUTHOR_EMAIL = 'philippe.pinard@gmail.com'

PROJECT_NAME = 'EBSD indexing'
PROJECT_DESCRIPTION = 'Evaluate the indexing routine'

APPLICATION_NAME = 'index.py'
APPLICATION_DESCRIPTION = 'Index diffraction patterns'
APPLICATION_VERSION = '0.1'
APPLICATION_PLATFORM = launcher.PLATFORM_JYTHON
APPLICATION_PATH = Files.getCurrentModulePath(__file__, 'index.py')
APPLICATION_BZR_REV = launcher.getBzrRev(APPLICATION_PATH)

def launch(mapping, numberPatterns, seed):
  random.seed(seed)

  #Define author
  author_id = database.AuthorsDB(database.DATABASE_FILE).addAuthorUnique(firstname=AUTHOR_FIRSTNAME
                                                                , lastname=AUTHOR_LASTNAME
                                                                , email=AUTHOR_EMAIL)

  #Define project
  project_id = database.ProjectsDB(database.DATABASE_FILE).addProjectUnique(name=PROJECT_NAME
                                                                   , description=PROJECT_DESCRIPTION
                                                                   , author_id=author_id)

  ctf = ctfFile.ctf(mapping.getCtfFilePath())
  maxPattern = ctf.getSize()

  patterns = []
  for i in range(len(numberPatterns)):
    patterns.append(random.randrange(0, maxPattern+1))

  #Create results folder
  if not os.path.exists(mapping.getResultsFolderPath()):
    os.makedirs(mapping.getResultsFolderPath())

  #List all the jobs in a text file to allow the assembly of these files after
  currentJobs_filepath = os.path.join(mapping.getResultsFolderPath(), '%s_jobs.txt' % mapping.getTitle())
  currentJobs_file = open(currentJobs_filepath, 'w')

  print patterns

  for pattern in patterns:
    index = pattern

    print 'Index %i' % (index)

    arguments = [mapping.getPatternsFolderPath(), mapping.getCtfFilePath(), mapping.getResultsFolderPath(), str(index)]
    argumentsStr = ' '.join(arguments)

    #Define application
    application_id = database.ApplicationsDB(database.DATABASE_FILE).addApplicationUnique(name=APPLICATION_NAME
                                                       , author_id=author_id
                                                       , description=APPLICATION_DESCRIPTION
                                                       , version=APPLICATION_VERSION
                                                       , platform=APPLICATION_PLATFORM
                                                       , path=APPLICATION_PATH
                                                       , bzr_rev=APPLICATION_BZR_REV)

    #Define job
    jobs = database.JobsDB(database.DATABASE_FILE)
    job_id = jobs.addJob(name=mapping.getName()
                         , description=mapping.getDescription()
                         , author_id=author_id
                         , project_id=project_id
                         , application_id=application_id
                         , casir_id=0
                         , arguments=argumentsStr)

    job_id_text = jobs.getJob(job_id)['id_text']
    log_file = '%s.log' % job_id_text

    del jobs

    runner = launcher.Launcher(job_id=job_id
                               , job_id_text=job_id_text
                               , log_file=log_file)

    currentJobs_file.write('%s\n' % runner.getLogFileDir())

    runner.launch()

  currentJobs_file.close()

if __name__ == '__main__':
  usage = "Usage: %prog [options]\n Launch the indexing routine on Casir."
  parser = optparse.OptionParser()
  parser.add_option("-c"
                    , "--configuration"
                    , action="store"
                    , type="string"
                    , dest="configurationFile"
                    , help="configuration file containing the projects to run")
  parser.add_option("--all"
                    , action="store_true"
                    , dest="all"
                    , default=None
                    , help="run all projects in the configuration file")
  parser.add_option("-p"
                    , "--project"
                    , action="store"
                    , dest="project"
                    , default=None
                    , help="run this specific project from the configuration file")
  parser.add_option("-n"
                    , "--number"
                    , action="store"
                    , dest="numberPatterns"
                    , default=50
                    , type="int"
                    , help="number of patterns to study")
  parser.add_option("-s"
                    , "--seed"
                    , action="store"
                    , dest="seed"
                    , default=None
                    , type="int"
                    , help="seed for the random number generator")

  (options, args) = parser.parse_args()

  config = configuration.Configuration(options.configurationFile)

  if options.all == None and options.project != None:
    mapping = config.getMapping(options.project)
    launch(mapping, options.jobs, options.numberPatterns, options.seed)
  elif options.all == True:
    mappings = config.getMappings()
    for mapping in mappings.values():
      launch(mapping, options.jobs, options.numberPatterns, options.seed)
  else:
    print 'Give proper arguments'
