'''
Created on Feb 24, 2012

@author: david
'''

from .person import Person
from caffe.entity import Entity

class Owner(Entity, Person):
    '''
    classdocs
    '''
        
    __surname = None    
        
    def __init__(self):
        pass
