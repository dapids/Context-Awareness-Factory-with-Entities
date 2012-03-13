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
        
        '''
        self.__domain = domain.getId()
        self.__cntx = cntx
        self.__name = name
        return dict.__setitem__(self, rng, None)
        
    
    def __delitem__(self, value):
        GraphManager.removeIndProperty(self.__name, self.__domain, value, self.__cntx)
        try:
            valueName = value.getId()
        except:
            pass
        print "Deleting individual property: '%s' -> %s -> '%s'\n" % (self.__domain, self.__name, valueName)
        return dict.__delitem__(self, value)