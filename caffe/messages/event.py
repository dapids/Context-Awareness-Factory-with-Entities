'''
Created on Mar 13, 2012

@author: david
'''

class AddEvent(object):
    """
    Triggers the insert of new data into the semantic network.
    """


    __subject = None
    __predicate = None
    __object = None
    

    def __init__(self, (subj, pred, obj)):
        """
        @type (subj, pred, obj): tuple
        @param (subj, pred, obj): the proposition representing the data to insert
        """
        self.__subject, self.__predicate, self.__object = (subj, pred, obj)
    
    
    def getSubject(self):
        """
        @return: the subject of the proposition
        """
        return self.__subject
    
    
    def getPredicate(self):
        """
        @return: the predicate of the proposition
        """
        return self.__predicate
        
    
    def getObject(self):
        """
        @return: the object of the proposition
        """
        return self.__object
    
    
    def __repr__(self):
        """
        @return: the new format of the event
        """
        return '<Event: %s %s %s>' % (self.__subject, self.__predicate, self.__object)
    
    
class DelEvent(object):
    """
    Triggers the deletion of data from the semantic network.
    """


    __subject = None
    __predicate = None
    __object = None
    

    def __init__(self, (subj, pred, obj)):
        """
        @type (subj, pred, obj): tuple
        @param (subj, pred, obj): the proposition representing the data to delete
        """
        self.__subject, self.__predicate, self.__object = (subj, pred, obj)
    
    
    def getSubject(self):
        """
        @return: the subject of the proposition
        """
        return self.__subject
    
    
    def getPredicate(self):
        """
        @return: the predicate of the proposition
        """
        return self.__predicate
        
    
    def getObject(self):
        """
        @return: the object of the proposition
        """
        return self.__object
    
    
    def __repr__(self):
        """
        @return: the new format of the event
        """
        return '<Event: %s %s %s>' % (self.__subject, self.__predicate, self.__object)
    