'''
Created on Feb 9, 2012

@author: david
'''

import os
import ConfigParser
from ftplib import FTP

class Writer(object):
    '''
    Allows to write an ontology both in local and in remote (FTP).
    Edit config.ini to change the settings about paths and filenames.
    '''
    __ontology = None
    __ontFile = None

    def __init__(self):
        config = ConfigParser.ConfigParser()
        config.readfp(open(os.getcwd() + os.sep + "config" + os.sep + "config.ini"))
        self.__ontology = dict(config.items("ontology"))
        self.__ontFile = open(self.__ontology["localpath"] + os.sep + self.__ontology["filename"], 'w')
    
    
    def writeOntology(self, ont, upload=False):
        '''
        Writes the ontology in a local/remote file.
        @type ont: str
        @param ont: the ontology to write in a local/remote file
        @type upload: boolean
        @param upload: if True it uploads the ontology on a FTP
        '''
        self.__ontFile.write(ont)
        if upload:
            self.__ontFile = open(self.__ontology["localpath"] + os.sep + self.__ontology["filename"], 'rb')
            self.uploadOntology()
        self.__ontFile.close()
      
      
    def uploadOntology(self):
        '''
        Uploads an ontology on a FTP.
        '''
        session = FTP(self.__ontology["ftpaddr"], self.__ontology["ftpuser"], self.__ontology["ftppass"])
        session.cwd(self.__ontology["ftpdir"])
        session.storbinary("STOR context.rdf", self.__ontFile)
        session.quit()
        self.__ontFile.close()
        print "Network uploaded on '%s'!" % (self.__ontology["ftpaddr"])