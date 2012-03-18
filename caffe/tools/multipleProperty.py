'''
Created on Mar 9, 2012

@author: david
'''

from ..graphManager import GraphManager

class MultipleProperty(dict):
    '''
    An override of the class dict, used to manage deletions of attributes containing lists of values.
    '''
    
    
    __domain = None
    __cntx = None
    __name = None
    
    
    def setItem(self, name, domain, rng, cntx):
        '''
        Sets new items in the dict.
        @type name: str
        @param name: the name of the property
        @type domain: object
        @param domain: the domain of the property
        @type rng: object / int / float / bool / str
        @param rng: the range of the property
        @type cntx: tuple
        @param cntx: the local context in which the property is
        '''
        self.__domain = domain.getId()
        self.__cntx = cntx
        self.__name = name
        return dict.__setitem__(self, rng, None)
        
    
    def __delitem__(self, value):
        """
        Overrides the method to delete an item from the dict. Every time an item is deleted,
        it updated the semantic network.
        @type value: object / int / float / bool / str
        @param value: the object to delete
        """
        result = None
        try:
            try:
                valueName = value.getId()
            except AttributeError:
                valueName = value
            result = dict.__delitem__(self, value)
        except KeyError:
            raise KeyError
        else:
            GraphManager.removeIndProperty(self.__name, self.__domain, value, self.__cntx)
            print "Deleting individual property: '%s' -> %s -> '%s'\n" % (self.__domain, self.__name, valueName)
        return result