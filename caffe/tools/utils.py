'''
Created on Mar 1, 2012

@author: david
'''
import caffe
from .exceptions import SemanticException

class Utils(object):
    '''
    Contains a series of classmethods useful to other classes.
    '''


    @classmethod
    def isSubOfEntity(cls, cl):
        '''
        Checks whether a class is subclass of Entity.
        @type cl: type
        @param cl: the class to check
        @return: True or False, depending on whether or not the class checked is subclass of Entity, respectively
        '''
        result = False
        if cl is not caffe.entity.Entity and issubclass(cl, caffe.entity.Entity):
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