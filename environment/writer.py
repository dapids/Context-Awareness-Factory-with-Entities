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
    
    
    def writeOntology(self):
        '''
        Writes the ontology on a local file
        '''
        self.__writeHeader()
        self.__writeEnd()
        
        
    def __writeHeader(self):
        '''
        Defines the header of the ontology (taking it from the file "ontologies/header")
        '''
        header = open(self.__ontology["localpath"] + os.sep + "header").read()
        ontName = self.__ontology["filename"].split(".")[0]
        self.__ontFile.write(header % (self.__ontology["path"], self.__ontology["path"],
                                       ontName, self.__ontology["path"], ontName))

    
    def __writeEnd(self):
        '''
        Defines the end of the ontology
        '''
        self.__ontFile.write("</rdf:RDF>")
        self.__ontFile.close()
      
      
    def uploadOntology(self):
        '''
        Upload an ontology on an FTP domain
        '''
        session = FTP("ftp.ilbello.com", "dapids", "raq1rYtYt")
        session.cwd("ontologies" + os.sep + "2012" + os.sep + "thesis_project" + os.sep + "assisted_living")
        self.__ontFile = open(self.__ontology["localpath"] + os.sep + self.__ontology["filename"], 'rb')
        session.storbinary("STOR context.rdf", self.__ontFile)
        session.quit()
        self.__ontFile.close()
        