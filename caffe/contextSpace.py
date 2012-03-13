'''
Created on Feb 12, 2012

@author: david
'''

from sets import Set
from Queue import Queue
from .graphManager import GraphManager
from .localContext import LocalContext
from .tools.exceptions import SemanticException
from .globalContext import GlobalContext
from .tools.utils import Utils
from .messages.dispatcher import Dispatcher
from .messages.eventGenerator import EventGenerator

class ContextSpace(object):
    '''
    classdocs
    '''
    
    
    __globalContext = None
    __registeredClasses = Set()
    __registeredIndividuals = dict()
    __propertiesDict = dict()
    __dispatcher = None
    __dataQueue = None
        
        
    def __init__(self, gns):
        self.__globalContext = GlobalContext(gns)
        self.__dispatcher = Dispatcher()
        self.__dataQueue = Queue()
        EventGenerator(self.__dispatcher, self.__dataQueue, 1, self.__registeredIndividuals)
        print("Creating new context-space: %s\n%s\n" % (gns[gns.rfind("/")+1:gns.find("#")].upper(), self.__globalContext))
    
    
    def getGlobalContext(self):
        return self.__globalContext.getInfo()
    
    
    def setLocalContext(self, name):
        lc = LocalContext(name, self.__globalContext.getInfo(), self.__propertiesDict)
        return lc
    
    
    def createEntity(self, cl, name):
        if cl not in self.__registeredClasses:
            try:
                if Utils.isSubOfEntity(cl):
                    self.__registeredClasses.update(GraphManager.mapClass(cl, self.__globalContext.getInfo(), self.__propertiesDict, self.__registeredClasses))
                else:
                    raise SemanticException("The class '%s' does not inherit the class 'Entity'." % cl.__name__)
            except SemanticException as e:
                print e
        if name not in self.__registeredIndividuals.keys():
            GraphManager.mapIndividual(name, cl.__name__, self.__globalContext)
            print "Mapping individual: '%s' (%s)\n" % (name, cl.__name__)
            ind = cl()
            ind(name, self.__dispatcher)
            self.__registeredIndividuals[name] = ind
        else:
            print "It is not possible to create the entity '%s'. An entity called in the same way already exists.\n" % name
            ind = None
        return ind
    
    
    def serializeContext(self, formatType="pretty-xml"):
        return self.__globalContext.getInfo()[0].serialize(format = formatType)
    
    
    def pushData(self, data):
        self.__dataQueue.put(data)