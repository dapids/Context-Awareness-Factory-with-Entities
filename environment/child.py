'''
Created on Feb 24, 2012

@author: david
'''

from cafe.entity import Entity
from .person import Person

class Child(Person, Entity):
    '''
    classdocs
    '''
    
    def __init__(self):
        pass