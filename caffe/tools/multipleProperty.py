'''
Created on Mar 9, 2012

@author: david
'''

from ..graphManager import GraphManager

class MultipleProperty(dict):
    
    __domain = None
    __cntx = None
    __name = None
    
    
    def setItem(self, name, domain, rng, cntx):
        self.__domain = domain.getName()
        self.__cntx = cntx
        self.__name = name
        return dict.__setitem__(self, rng, None)
        
    
    def __delitem__(self, value):
        GraphManager.removeIndProperty(self.__name, self.__domain, value, self.__cntx)
        try:
            valueName = value.getName()
        except:
            pass
        print "Deleting individual property: '%s' -> %s -> '%s'\n" % (self.__domain, self.__name, valueName)
        return dict.__delitem__(self, value)