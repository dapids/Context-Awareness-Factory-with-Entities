'''
Created on Feb 24, 2012

@author: david
'''

from .student import Student
from caffe.entity import Entity

class Asd(object, Entity): pass

class MasterS(Entity, Student, Asd):
    '''
    classdocs
    '''
        
    def __init__(self):
        pass
