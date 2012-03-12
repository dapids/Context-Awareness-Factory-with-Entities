'''
Created on Mar 2, 2012

@author: david
'''

from rdflib import Namespace
from .graphManager import GraphManager

class GlobalContext(object):
    '''
    classdocs
    '''
    
    
    __globalNS = None
    __globalGraph = None


    def __init__(self, gns):
        self.__globalGraph = GraphManager.createGlobalGraph(gns)
        self.__globalNS = Namespace(gns)
        
    
    def getInfo(self):
        return (self.__globalGraph, self.__globalNS)
    
    
    def __str__(self):
        return "Graph: %s\nGlobal namespace: %s" % (self.__globalGraph, self.__globalNS)