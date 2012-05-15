'''
Created on Gen 17, 2012

@author: david
'''

import datetime
import shelve
from sets import Set
from Queue import Queue
import socket, fcntl, struct
from threading import Thread
from rdflib.term import URIRef
from .graphManager import GraphManager
from .localContext import LocalContext
from .tools.exceptions import SemanticException
from .globalContext import GlobalContext
from .tools.utils import Utils
from .events.dispatcher import Dispatcher
from .events.eventGenerator import EventGenerator
from .querySystem.queryServer import QueryServer, QSHandler
from .querySystem.retriever import Retriever
from .sensors.sensorsServer import SensorsServer, SSHandler
from .tools.writer import Writer

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
    __queryServerAddress = [None, 7777]
    __sensorsServerAddress = [None, 9999]
    __performQuery = None
        
        
    def __init__(self, gns):
        """
        Creates a global context, a dispatcher, a task-queue to manage the data from sensors, and an event generator.
        @type gns: str
        @param gns: the namespace of the global context
        """
        self.__globalContext = GlobalContext(gns)
        gnsName = self.__globalContext.getInfo()[2]
        self.__dispatcher = Dispatcher()
        self.__dataQueue = Queue()
        EventGenerator(self.__dispatcher, self.__dataQueue, 2, self.__registeredIndividuals)
        self.__performQuery = Retriever(self.getGlobalContext()).performQuery
        print("\nCreating new context-space: %s\n%s" % (gnsName.upper(), self.__globalContext))
    
    
    def getGlobalContext(self):
        """
        @return: a tuple containing info about the global context related to the context space
        """
        return self.__globalContext.getInfo()
    
    
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
            print "Mapping individual: '%s' (%s)" % (identifier, cl.__name__)
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
        print "Context serialized in OWL."
        return self.__globalContext.getInfo()[0].serialize(format = formatType)
    
    
    def printContextsList(self):
        """
        Prints out the list of the local contexts belonging to a context space.
        """
        print "Contexts list:"
        for index, entry in enumerate(self.getGlobalContext()[0].contexts()):
            print "%s: %s" % (index, entry)
        print("")
    
    
    def __getAddress(self):
        address = "127.0.0.1"
        sck = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        interfaces = "eth0", "wlan0"
        for iface in interfaces:
            try:
                address = socket.inet_ntoa(fcntl.ioctl(sck.fileno(),0x8915,struct.pack('256s', iface[:15]))[20:24])
            except IOError:
                pass
            else:
                break
        return address
    
    
    def launchServers(self):
        address = self.__getAddress()
        
        self.__queryServerAddress[0] = address
        qs = QueryServer(tuple(self.__queryServerAddress), QSHandler, self.__performQuery)
        qsThread = Thread(target=qs.serve_forever)
        qsThread.daemon = True
        qsThread.start()
        print("Query server available @ %s\n" % self.__queryServerAddress)
        
        self.__sensorsServerAddress[0] = address
        ss = SensorsServer(tuple(self.__sensorsServerAddress), SSHandler, self.__dataQueue)
        ssThread = Thread(target=ss.serve_forever)
        ssThread.daemon = True
        ssThread.start()
        print("Sensors server available @ %s\n" % self.__sensorsServerAddress)
        
        try:
            key = raw_input("Type 's' to shutdown the servers or press any other key to visualise the context.\n\n")
        except KeyboardInterrupt:
            print ""
        except EOFError:
            print ""
        flag = True
        while flag:
            if key == "s":
                print "Shutting down servers..."
                qs.shutdown()
                ss.shutdown()
                print("Servers are down. Quitting...")
                flag = False
            else:
                self.visualizeContext()
                key = raw_input()
            
    
    def saveContext(self, filename):
        storedContext = shelve.open(filename)
        timestamp = str(datetime.datetime.now())
        storedContext[timestamp] = str(self.__globalContext.getInfo()[1]), self.__globalContext.getInfo()[0]
        storedContext.close()
        print "Context snapshot taken at the time '%s'." % timestamp
            
            
    def visualizeContext(self):
        contextGraph = self.getGlobalContext()
        semNet = list()
        triples = list(contextGraph[0].triples((None, None, None)))
        for el in triples:
            if el[1] == URIRef("http://www.w3.org/2000/01/rdf-schema#subClassOf"):
                semNet.append(el)
            elif el[1] == URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"):
                if not str(el[2]).startswith("http://www.w3.org"):
                    semNet.append(el)
            elif not str(el[1]).startswith("http://www.w3.org") and not str(el[1]).endswith("ID"):
                semNet.append(el)
        Utils.triplesToDot(semNet, "Semantic_Network", contextGraph[1])
#        triples = contextGraph[0].triples((None, None, None))
#        for t in triples:
#            print t

    def writeContext(self, ontology, upload=False):
        wr = Writer()
        wr.writeOntology(ontology, upload)