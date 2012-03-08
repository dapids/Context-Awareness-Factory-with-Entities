'''
Created on Mar 1, 2012

@author: david
'''

import string
from rdflib import Namespace, Graph

class LocalContext(object):
    '''
    classdocs
    '''
    
    
    __globalContext = None
    __name = None
    __localNS = None
    __graph = None
    __propertiesDict = None


    def __init__(self, name, globalContext, propertiesDict):
        self.__name = name
        self.__globalContext = globalContext
        self.__localNS = Namespace(self.__globalContext[1][0:self.__globalContext[1].find("#")] + "/context#")[self.__name]
        self.__graph = Graph(self.__globalContext[0].store, self.__localNS)
        self.__propertiesDict = propertiesDict
        print("Creating new local context: %s\n%s\n" % (name.upper(), self))
        
        
    def defineProperties(self, *properties):
        for name, card in properties:
            self.__propertiesDict[string.upper(name)] = [None, None, self, card]
            
  
    def getInfo(self):
        return (self.__name, self.__graph, self.__globalContext[1], self.__localNS)
    
    
    def __str__(self):
        return ("Graph: %s\nGlobal namespace: %s\nLocal Namespace: %s") % (self.__graph, self.__globalContext[1], self.__localNS)