'''
Created on Feb 28, 2012

@author: david
'''

class SemanticException(Exception):
    '''
    Custom exception.
    '''
    def __init__(self, text):
        '''
        @type text: str
        @param text: the description of the error
        '''
        self.text = "WARNING: semantic exception. %s" % text
    
    def __str__(self):
        '''
        Override of the __str__ method.
        @return: a custom string format
        '''
        return self.text+"\n"


class InputException(Exception):
    '''
    Custom exception.
    '''
    def __init__(self, text):
        '''
        @type text: str
        @param text: the description of the error
        '''
        self.text = "ERROR: wrong input. %s" % text
    
    def __str__(self):
        '''
        Override of the __str__ method.
        @return: a custom string format
        '''
        return self.text+"\n"