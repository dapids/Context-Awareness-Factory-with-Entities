'''
Created on Feb 24, 2012

@author: david
'''

from .person import Person
from cafe.entity import Entity

class Adult(Entity, Person):
    '''
    classdocs
    '''
        
    __surname = None    
        
    def __init__(self):
        pass
