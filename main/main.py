
'''
Created on Jan 30, 2012

@author: david
'''

from caffe.contextSpace import ContextSpace
from environment.student import Student
from environment.person import Person
from environment.masterS import MasterS, Asd

if __name__ == '__main__':

    cs = ContextSpace("http://caffe.ns/home#")
    
    david = cs.createEntity(MasterS, "David")
    andrea = cs.createEntity(Student, "Andrea")
    asd = cs.createEntity(Asd, "asd")
    
    kitchen = cs.setLocalContext("kitchen")
    kitchen.defineProperties(("knows", 0))
    
    info = cs.setLocalContext("info")
    info.defineProperties(("name", 1), ("age", 1))
    
    Person.KNOWS = Person
    Person.NAME = str
    Person.AGE = int
                
    david.KNOWS = andrea
    david.KNOWS = david
    david.NAME = "David Sorrentino"
    david.AGE = 27
    david.AGE = 28
                                                                         
    print ("--------------------------------------------------------\n")
    print cs.serializeContext()

    for index, entry in enumerate(cs.getGlobalContext()[0].contexts()):
        print index, entry