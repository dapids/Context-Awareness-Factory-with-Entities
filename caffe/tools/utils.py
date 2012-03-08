'''
Created on Mar 1, 2012

@author: david
'''
import caffe
from .exceptions import SemanticException

class Utils(object):
    '''
    classdocs
    '''


    @classmethod
    def isSubOfEntity(cls, cl):
        result = False
        if cl is not caffe.entity.Entity and issubclass(cl, caffe.entity.Entity):
            result = True
        return result
    
    @classmethod
    def checkClassRange(cls, name, domain, rng):
        result = None
        if isinstance(rng, type(type)) and cls.isSubOfEntity(rng):
            result = "objectProperty"
        elif rng in [int, long, float, str]:
            result = "dataProperty"
        else:
            raise SemanticException(("The value assigned to '%s.%s' should be either a subclass of 'Entity' " +
                                    "or one of the following ones [int, long, float, string].") % (domain.__name__, name))
        return result