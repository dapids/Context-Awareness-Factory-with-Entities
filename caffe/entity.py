'''
Created on Feb 23, 2012

@author: david
'''

from .metaEntity import MetaEntity
from .tools.graphManager import GraphManager
from .tools.exceptions import SemanticException

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
                                finalValue = self.__getattribute__(name)
                                finalValue.append(value.getName())
                            except AttributeError:
                                finalValue = [value.getName()]
                        GraphManager.mapIndProperty(name, self, value, self._MetaEntity__propertiesDict[name][2])
                    else:
                        raise SemanticException("The property '%s' expects a value of type '%s'. The value given is of type '%s'." %
                                            (name, self._MetaEntity__propertiesDict[name][1].__name__, type(value).__name__))
                else:
                    raise SemanticException("The property '%s' has been not defined for the class '%s'." %
                                            (name, self.__class__.__name__))
            except TypeError:
                print "Operation not allowed. You are trying to define an individual property before specifying the respective class property.\n"
            except KeyError:
                pass
            except SemanticException as e:
                print e
            else:
                try:
                    propValue = value.getName()
                except AttributeError:
                    propValue = value
                finally:
                    print "Mapping individual property: '%s' -> '%s' -> '%s'.\n" % (self.__name, name, propValue)
        object.__setattr__(self, name, finalValue)
        
    def __delattr__(self, name):
        GraphManager.removeIndProperty(name, self.__name, self.__getattribute__(name), self._MetaEntity__propertiesDict[name][2])
        try:
            value = self.__getattribute__(name).getName()
        except AttributeError:
            value = self.__getattribute__(name)
        print "Deleting individual property: '%s' -> '%s' -> '%s'.\n" % (self.__name, name, value)
        object.__setattr__(self, name, None)
        
        
    def getName(self):
        return self.__name