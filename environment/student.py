'''
Created on Feb 24, 2012

@author: david
'''

from caffe.entity import Entity
from .person import Person

class Student(Person, Entity):
    '''
    classdocs
    '''
    
    def __init__(self):
        pass