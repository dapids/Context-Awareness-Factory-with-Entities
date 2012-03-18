'''
Created on Feb 23, 2012

@author: david
'''

from .metaEntity import MetaEntity
from .graphManager import GraphManager
from .tools.exceptions import SemanticException
from .tools.multipleProperty import MultipleProperty as MP
from .messages.event import AddEvent, DelEvent

class Entity(object):
    '''
    classdocs
    '''
    
    __metaclass__ = MetaEntity
    __id = None


    def __call__(self, identificator, dispatcher):
        self.__id = identificator
        dispatcher.subscribe(self, self.__handler)
        

    def __handler(self, event):
        if isinstance(event, AddEvent):
            self.__setattr__(event.getPredicate(), event.getObject())
        elif isinstance(event, DelEvent):
            try:
                prop = self.__getattribute__(event.getPredicate())
                if event.getObject() is None:
                    self.__delattr__(event.getPredicate())
                else:
                    del prop[event.getObject()]
            except AttributeError:
                print("Deletion was not possible. The property '%s %s' does not exist.\n" % (event.getSubject().getId(), event.getPredicate()))
            except KeyError:
                print ("Deletion was not possible. The property '%s %s %s' does not exist.\n" % (event.getSubject().getId(), event.getPredicate(), event.getObject()))
            except TypeError:
                if prop == event.getObject():
                    self.__delattr__(event.getPredicate())
                else:
                    print("Deletion was not possible. The property '%s %s %s' does not exist.\n" % (event.getSubject().getId(), event.getPredicate(), event.getObject()))


    def __setattr__(self, name, value):
        finalValue = value
        if name.isupper():
            try:
                if isinstance(self, self._MetaEntity__propertiesDict[name][0]):
                    if isinstance(value, self._MetaEntity__propertiesDict[name][1]):
                        if self._MetaEntity__propertiesDict[name][3] == 1:
                            try:
                                GraphManager.removeIndProperty(name, self.__id, self.__getattribute__(name), self._MetaEntity__propertiesDict[name][2])
                            except AttributeError:
                                pass
                            else:
                                try:
                                    val = self.__getattribute__(name).getId()
                                except AttributeError:
                                    val = self.__getattribute__(name)
                                finally:
                                    print "Deleting individual property: '%s' -> %s -> '%s'\n" % (self.__id, name, val)
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
                GraphManager.mapIndProperty(name, self.__id, value, self._MetaEntity__propertiesDict[name][2],
                                            self._MetaEntity__propertiesDict[name][4])
                try:
                    propValue = value.getId()
                except AttributeError:
                    propValue = value
                finally:
                    print "Mapping individual property: '%s' -> %s -> '%s'\n" % (self.__id, name, propValue)
                    if self._MetaEntity__propertiesDict[name][4] == "s":
                        print "Mapping individual symmetric property: '%s' -> %s -> '%s'\n" % (propValue, name, self.__id)
        object.__setattr__(self, name, finalValue)
        
        
    def __delattr__(self, name):
        if name.isupper():
            if isinstance(self.__getattribute__(name), MP):
                for rng in self.__getattribute__(name).keys():
                    GraphManager.removeIndProperty(name, self.__id, rng, self._MetaEntity__propertiesDict[name][2])
                    try:
                        rng = rng.getId()
                    except AttributeError:
                        pass
                    print "Deleting individual property: '%s' -> %s -> '%s'\n" % (self.__id, name, rng)
                    prop = self.__getattribute__(name)
                    prop.clear()
            else:
                GraphManager.removeIndProperty(name, self.__id, self.__getattribute__(name), self._MetaEntity__propertiesDict[name][2])
                try:
                    value = self.__getattribute__(name).getId()
                except AttributeError:
                    value = self.__getattribute__(name)
                finally:
                    print "Deleting individual property: '%s' -> %s -> '%s'\n" % (self.__id, name, value)
                    object.__setattr__(self, name, None)
        else:
            object.__delattr__(self, name)
            
        
    def getId(self):
        return self.__id