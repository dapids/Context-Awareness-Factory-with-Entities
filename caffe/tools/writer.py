'''
Created on Feb 9, 2012

@author: david
'''

import os
import ConfigParser
from ftplib import FTP

class Writer(object):
    '''
    Allows to write an ontology in local or in remote (FTP)
    Edit config.ini to change the settings
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
        Writes the ontology on a local file
        '''
        self.__ontFile.write(ont)
        self.__ontFile.close()
        if upload:
            self.__ontFile = open(self.__ontology["localpath"] + os.sep + self.__ontology["filename"], 'rb')
            self.uploadOntology()
            self.__ontFile.close()
      
      
    def uploadOntology(self):
        '''
        Upload an ontology on an FTP domain
        '''
        session = FTP(self.__ontology["ftpaddr"], self.__ontology["ftpuser"], self.__ontology["ftppass"])
        session.cwd(self.__ontology["ftpdir"])
        session.storbinary("STOR context.rdf", self.__ontFile)
        session.quit()
        self.__ontFile.close()