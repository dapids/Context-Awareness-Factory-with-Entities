'''
Created on Mar 13, 2012

@author: david
'''

class Event(object):
    """
    An event is a container for attributes.  The source of an event
    creates this object, or a subclass, gives it any kind of data that
    the events handlers need to handle the event, and then calls
    notify(event).

    The target of an event registers a function to handle the event it
    is interested with subscribe().  When a sources calls
    notify(event), each subscriber to that even will be called in no
    particular order.
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
    