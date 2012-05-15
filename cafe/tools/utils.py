'''
Created on Mar 1, 2012

@author: david
'''
import rdflib
import os, datetime
import shelve
import cafe
from .contextHistory import ContextHistory
from .exceptions import SemanticException

class Utils(object):
    '''
    Contains a series of classmethods useful to other classes.
    '''
    
    @classmethod
    def mergeContextSpaces(cls, csList):
        gcs = rdflib.Graph()
        for el in csList:
            gcs += el
        print "Resultant graph:\n\t%s" % gcs
        return gcs
    
    @classmethod
    def parseOntology(cls, filepath):
        g = rdflib.Graph()
        g.parse(filepath)
        print "Ontology '%s' parsed into the graph:\n\t'%s'" % (filepath, g)
        return g
    
    @classmethod
    def loadContext(cls, filename):
        storedContext = shelve.open(filename)
        result = ContextHistory()
        for key, value in storedContext.iteritems():
            result[key] = value
        storedContext.close()
        return result

    @classmethod
    def isSubOfEntity(cls, cl):
        '''
        Checks whether a class is subclass of Entity.
        @type cl: type
        @param cl: the class to check
        @return: True or False, depending on whether or not the class checked is subclass of Entity, respectively
        '''
        result = False
        if cl is not cafe.entity.Entity and issubclass(cl, cafe.entity.Entity):
            result = True
        return result
    
    @classmethod
    def checkClassRange(cls, name, domain, rng):
        '''
        Checks whether the value assigned to a property is correct and discovers the type of the property.
        @type name: str
        @param name: the name of the property to check
        @type domain: str
        @param domain: the name of the domain class
        @type rng: type / [int, str, bool, float]
        @param rng: the range class to check
        @return: the typology of property. None if the value assigned to the property is not valid
        '''
        result = None
        if isinstance(rng, type(type)) and cls.isSubOfEntity(rng):
            result = "objectProperty"
        elif rng in [int, bool, float, str]:
            result = "dataProperty"
        else:
            raise SemanticException(("The value assigned to '%s.%s' should be either a subclass of 'Entity' " +
                                    "or one of the following ones [int, bool, float, string].") % (domain, name))
        return result
    
    
    @classmethod
    def triplesToDot(cls, triples, filename, cntxName):
        out=file("%s.dot" % filename, 'w')
        out.write('graph "%s" {\n' % cntxName)
        out.write('overlap = "scale";\n')
        for t in triples:
            out.write('"%s" -- "%s" [label="%s"]\n' % (cls.__redefineNodeName(t[0]),
                                                       cls.__redefineNodeName(t[2]),
                                                       cls.__redefineNodeName(t[1])))
        out.write('}')
        out.close()
        os.system("neato -Teps -O%s %s.dot" % (filename, filename))
        print("Context printed at time %s." % datetime.datetime.now())
        
    
    @classmethod
    def __redefineNodeName(cls, node):
        newName = node[node.find("#")+1:]
        if newName == "subClassOf" or newName == "type":
            newName = "is a"
        return newName