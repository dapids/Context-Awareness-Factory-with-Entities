'''
Created on Feb 24, 2012

@author: david
'''

from .tools.graphManager import GraphManager
from .tools.exceptions import SemanticException

class MetaEntity(type):
    '''
    classdocs
    '''
    
    
    def __new__(cls, name, bases, dct):
        if name != "Entity":
            print "Init'ing class '%s'.\n" % name
            ent = None
            lBases = list()
            for el in bases:
                if el.__name__ == "Entity":
                    ent = el
                elif el.__name__ != "object":
                    lBases.append(el)
            if ent != None:
                lBases.append(ent)
            bases = tuple(lBases)
        return super(MetaEntity, cls).__new__(cls, name, bases, dct)

    
    def __setattr__(self, name, value):
        if name.isupper():
            try:
                if (self.__propertiesDict[name][0] is None) and (self.__propertiesDict[name][1] is None):
                    GraphManager.mapClassProperty(name, self, value, self.__propertiesDict[name][2])
                else:
                    raise SemanticException (("The property '%s' have been already defined as '%s %s %s'." +
                                              "It is not possible to override it.") % (name,
                                                                                       self.__propertiesDict[name][0].__name__,
                                                                                       name, self.__propertiesDict[name][1].__name__))
            except TypeError:
                print "Operation not allowed. You are trying to define an entity property before creating the entity.\n"
            except KeyError:
                print "Warning. The property '%s' has not been defined yet.\n" % name
            except SemanticException as e:
                print e
            else:
                print "Mapping class property: '%s' -> '%s' -> '%s'.\n" % (self.__name__, name, value.__name__)
                self.__propertiesDict[name][0] = self
                self.__propertiesDict[name][1] = value
            name = "__" + name
        type.__setattr__(self, name, value)
        
    
    def getPropsDict(self, pd):    
        self.__propertiesDict = pd
        
        
    def __init__(cls, name, bases, dct):
        cls.__propertiesDict = None
        super(MetaEntity, cls).__init__(name, bases, dct)