'''
Created on Feb 12, 2012

@author: david
'''

from sets import Set
from Queue import Queue
import socket, fcntl, struct
from threading import Thread
from .graphManager import GraphManager
from .localContext import LocalContext
from .tools.exceptions import SemanticException
from .globalContext import GlobalContext
from .tools.utils import Utils
from .events.dispatcher import Dispatcher
from .events.eventGenerator import EventGenerator
from .querySystem.queryServer import QueryServer, QSHandler
from .querySystem.retriever import Retriever

class ContextSpace(object):
    '''
    classdocs
    '''
    
    
    __globalContext = None
    __localContexts = dict()
    __registeredClasses = Set()
    __registeredIndividuals = dict()
    __propertiesDict = dict()
    __dispatcher = None
    __dataQueue = None
    __queryServerAddress = None
    __performQuery = None
        
        
    def __init__(self, gns):
        """
        Creates a global context, a dispatcher, a task-queue to manage the data from sensors, and an event generator.
        @type gns: str
        @param gns: the namespace of the global context
        """
        self.__globalContext = GlobalContext(gns)
        self.__dispatcher = Dispatcher()
        self.__dataQueue = Queue()
        EventGenerator(self.__dispatcher, self.__dataQueue, 1, self.__registeredIndividuals)
        self.__performQuery = Retriever(self.getGlobalContext()).performQuery
        print("Creating new context-space: %s\n%s" % (gns[gns.rfind("/")+1:gns.find("#")].upper(), self.__globalContext))
    
    
    def getGlobalContext(self):
        """
        @return: a tuple containing info about the global context related to the context space
        """
        return self.__globalContext.getInfo()
    
    
    def getCSAddress(self):
        return self.__address
    
    
    def setLocalContext(self, name):
        """
        Creates a new local context.
        @type name: str
        @param name: the local context to create
        @return: a local context
        """
        lc = LocalContext(name, self.__globalContext.getInfo(), self.__propertiesDict)
        self.__localContexts[name] = lc
        return lc
    
    
    def createEntity(self, cl, identifier):
        """
        @type cl: type
        @param cl: class which the entity to create belongs to
        @type identifier: str
        @param identifier: identifier of the entity to create
        @return: object representing the entity created
        """
        if cl not in self.__registeredClasses:
            try:
                if Utils.isSubOfEntity(cl):
                    self.__registeredClasses.update(GraphManager.mapClass(cl, self.__globalContext.getInfo(), self.__propertiesDict, self.__registeredClasses))
                else:
                    raise SemanticException("The class '%s' does not inherit the class 'Entity'." % cl.__name__)
            except SemanticException as e:
                print e
        if identifier not in self.__registeredIndividuals.keys():
            GraphManager.mapIndividual(identifier, cl.__name__, self.__globalContext)
            print "Mapping individual: '%s' (%s)\n" % (identifier, cl.__name__)
            ind = cl()
            ind(identifier, self.__dispatcher, self.__performQuery)
            self.__registeredIndividuals[identifier] = ind
        else:
            print "It is not possible to create the entity '%s'. An entity called in the same way already exists.\n" % identifier
            ind = None
        return ind
    
    
    def serializeContext(self, formatType="pretty-xml"):
        """
        Serialises the global context in one of the available formats.
        @type formatType: str
        @param formatType: the serialisation format
        @return: a serialisation of the global context
        """
        return self.__globalContext.getInfo()[0].serialize(format = formatType)
    
    
    def printContextsList(self):
        """
        Prints out the list of the local contexts belonging to a context space.
        """
        print "Contexts list:"
        for index, entry in enumerate(self.getGlobalContext()[0].contexts()):
            print "%s: %s" % (index, entry)
        print("")
    
    
    def __launchQueryServer(self):
        address = None
        sck = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        interfaces = "eth0", "wlan0"
        for iface in interfaces:
            try:
                address = socket.inet_ntoa(fcntl.ioctl(sck.fileno(),0x8915,struct.pack('256s', iface[:15]))[20:24]), 7777
            except IOError:
                pass
            else:
                break
        qs = QueryServer(address, QSHandler, self.__performQuery)
        qsThread = Thread(target=qs.serve_forever)
        qsThread.daemon = True
        qsThread.start()
        return address, qs
    
    
    def launchServers(self):
        qs = self.__launchQueryServer()
        self.__queryServerAddress = qs[0]
        print("Query server available @ %s, %s\n" % self.__queryServerAddress)
        raw_input("Press a key to shutdown the servers.\n\n")
        qs[1].shutdown()
        print("Servers are down. Quit.")
    
    
    def pushData(self, data):
        """
        Adds to the task-queue a new data taken from the sensors.
        @type data: str
        @param data: data from sensors
        """
        self.__dataQueue.put(data)