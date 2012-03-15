'''
Created on Mar 13, 2012

@author: david
'''

class AddEvent(object):
    """
    
    """


    __subject = None
    __predicate = None
    __object = None
    

    def __init__(self, (subj, pred, obj)):
        self.__subject, self.__predicate, self.__object = (subj, pred, obj)
    
    
    def getSubject(self):
        return self.__subject
    
    
    def getPredicate(self):
        return self.__predicate
        
    
    def getObject(self):
        return self.__object
    
    
    def __repr__(self):
        return '<Event: %s %s %s>' % (self.__subject, self.__predicate, self.__object)
    
    
class DelEvent(object):
    """
    
    """


    __subject = None
    __predicate = None
    __object = None
    

    def __init__(self, (subj, pred, obj)):
        self.__subject, self.__predicate, self.__object = (subj, pred, obj)
    
    
    def getSubject(self):
        return self.__subject
    
    
    def getPredicate(self):
        return self.__predicate
        
    
    def getObject(self):
        return self.__object
    
    
    def __repr__(self):
        return '<Event: %s %s %s>' % (self.__subject, self.__predicate, self.__object)
    