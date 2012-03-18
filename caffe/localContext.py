'''
Created on Mar 1, 2012

@author: david
'''

import string
from rdflib import Namespace, Graph

class LocalContext(object):
    '''
    Provides a local context. A local context is composed of a global graph and a global namespace.
    '''
    
    
    __globalContext = None
    __name = None
    __localNS = None
    __graph = None
    __propertiesDict = dict()


    def __init__(self, name, globalContext, propertiesDict):
        """
        Creates a graph and a namespace for a local context.
        @type name: str
        @param name: the name of the local context
        @type globalContext: tuple
        @param globalContext: a graph and a namespace representing the global context in which the local context is.
        @type propertiesDict: dict
        @param propertiesDict: contains all the properties related to the local context.        
        """
        self.__name = name
        self.__globalContext = globalContext
        self.__localNS = Namespace(self.__globalContext[1][0:self.__globalContext[1].find("#")] + "/context#")[self.__name]
        self.__graph = Graph(self.__globalContext[0].store, self.__localNS)
        self.__propertiesDict = propertiesDict
        print("Creating new local context: %s\n%s\n" % (name.upper(), self))
        
        
    def defineProperties(self, *properties):
        """
        Saves all the properties in a dictionary.
        @type properties: list
        @param properties: list of properties defined by the user
        """
        for prop in properties:
            characteristics = list()
            try:
                name, card, typology = prop
                if typology == "s":
                    characteristics.append("simmetry")
            except ValueError:
                name, card = prop
                typology = None
            print "Defining class property: %s" % name
            print "Cardinality: %s" % (1 if card == 1 else "*")
            print "Characteristics: %s\n" % characteristics
            self.__propertiesDict[string.upper(name)] = [None, None, self, card, typology]
            
  
    def getInfo(self):
        """
        Gets all the important information related to a local context.
        @return: name, graph, global namespace and local namespace related to a local context
        """
        return (self.__name, self.__graph, self.__globalContext[1], self.__localNS)
    
    
    def __str__(self):
        """
        Overrides the str method with a proper format.
        @return: the string in the new format
        """
        return ("Graph: %s\nGlobal namespace: %s\nLocal Namespace: %s") % (self.__graph, self.__globalContext[1], self.__localNS)