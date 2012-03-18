'''
Created on Mar 2, 2012

@author: david
'''

from rdflib import Namespace
from .graphManager import GraphManager

class GlobalContext(object):
    '''
    Provides a global context. A global context is composed of a global graph and a global namespace.
    '''
    
    
    __globalNS = None
    __globalGraph = None


    def __init__(self, gns):
        '''
        Creates a graph and a namespace for a global context.
        @type gns: str 
        @param gns: the string representing the namespace related to the context
        '''
        self.__globalGraph = GraphManager.createGlobalGraph(gns)
        self.__globalNS = Namespace(gns)
        
    
    def getInfo(self):
        '''
        @return: a tuple containing a global graph and a namespace
        '''
        return (self.__globalGraph, self.__globalNS)
    
    
    def __str__(self):
        '''
        @return: a string containing a global graph instance and a namespace
        '''
        return "Graph: %s\nGlobal namespace: %s" % (self.__globalGraph, self.__globalNS)