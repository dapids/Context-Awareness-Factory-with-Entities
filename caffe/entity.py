'''
Created on Feb 23, 2012

@author: david
'''

from .metaEntity import MetaEntity
from .graphManager import GraphManager
from .tools.exceptions import SemanticException
from .tools.multipleProperty import MultipleProperty as MP

class Entity(object):
    '''
    classdocs
    '''
    
    __metaclass__ = MetaEntity
    __name = None


    def __call__(self, name):
        self.__name = name


    def __setattr__(self, name, value):
        finalValue = value
        if name.isupper():
            try:
                if isinstance(self, self._MetaEntity__propertiesDict[name][0]):
                    if isinstance(value, self._MetaEntity__propertiesDict[name][1]):
                        if self._MetaEntity__propertiesDict[name][3] == 1:
                            try:
                                GraphManager.removeIndProperty(name, self.__name, self.__getattribute__(name), self._MetaEntity__propertiesDict[name][2])
                            except AttributeError:
                                pass
                            else:
                                try:
                                    val = self.__getattribute__(name).getName()
                                except AttributeError:
                                    val = self.__getattribute__(name)
                                finally:
                                    print "Deleting individual property: '%s' -> %s -> '%s'\n" % (self.__name, name, val)
                        else:
                            try:
                                finalValue = self.__getattribute__(name)
                                finalValue.setItem(name, self, value, self._MetaEntity__propertiesDict[name][2])
                            except AttributeError:
                                finalValue = MP()
                                finalValue.setItem(name, self, value, self._MetaEntity__propertiesDict[name][2])
                    else:
                        raise SemanticException("The property '%s' expects a value of type '%s'. The value given is of type '%s'." %
                                            (name, self._MetaEntity__propertiesDict[name][1].__name__, type(value).__name__))
                else:
                    raise SemanticException("The property '%s' has been not defined for the class '%s'." %
                                            (name, self.__class__.__name__))
                
            except TypeError:
                print "Operation not allowed. You are trying to define an individual property before specifying the respective class property.\n"
            except KeyError:
                print "Warning. The property '%s' has not been defined yet.\n" % name
            except SemanticException as e:
                print e
            else:
                GraphManager.mapIndProperty(name, self.__name, value, self._MetaEntity__propertiesDict[name][2])
                try:
                    propValue = value.getName()
                except AttributeError:
                    propValue = value
                finally:
                    print "Mapping individual property: '%s' -> %s -> '%s'\n" % (self.__name, name, propValue)
        object.__setattr__(self, name, finalValue)
        
        
    def __delattr__(self, name):
        if name.isupper():
            if isinstance(self.__getattribute__(name), MP):
                for rng in self.__getattribute__(name).keys():
                    GraphManager.removeIndProperty(name, self.__name, rng, self._MetaEntity__propertiesDict[name][2])
                    print "Deleting individual property: '%s' -> %s -> '%s'\n" % (self.__name, name, rng)
            else:
                GraphManager.removeIndProperty(name, self.__name, self.__getattribute__(name), self._MetaEntity__propertiesDict[name][2])
                try:
                    value = self.__getattribute__(name).getName()
                except AttributeError:
                    value = self.__getattribute__(name)
                finally:
                    print "Deleting individual property: '%s' -> %s -> '%s'\n" % (self.__name, name, value)
        object.__delattr__(self, name)
            
        
    def getName(self):
        return self.__name