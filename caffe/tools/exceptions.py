'''
Created on Feb 28, 2012

@author: david
'''

class SemanticException(Exception):
    '''
    classdocs
    '''
    def __init__(self, text):
        self.text = "Warning: semantic exception. %s" % text
    
    def __str__(self):
        return self.text+"\n"
