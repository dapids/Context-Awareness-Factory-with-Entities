
'''
Created on Jan 17, 2012

@author: david
'''

from cafe.contextSpace import ContextSpace
from cafe.tools.writer import Writer

from environment.person import Person
from environment.host import Host
from environment.room import Room
from environment.thing import Thing
from environment.guest import Guest
from environment.passiveObj import PassiveObj
from environment.activeObj import ActiveObj

if __name__ == '__main__':

    # create the context space
    cs = ContextSpace("http://caffe.ns/home#")
    
    # create the individuals
    david = cs.createEntity(Host, "david")
    marco = cs.createEntity(Guest, "marco")
    andrea = cs.createEntity(Guest, "andrea")
    kitchen = cs.createEntity(Room, "kitchen")
    livingRoom = cs.createEntity(Room, "livingRoom")
    bowl = cs.createEntity(PassiveObj, "bowl")
    spoon = cs.createEntity(PassiveObj, "spoon")
    television = cs.createEntity(ActiveObj, "television")
    toaster = cs.createEntity(ActiveObj, "toaster")
    
    # create a local context and define the properties belonging to it
    locations = cs.setLocalContext("locations")
    locations.defineProperties(("isLocated", 1))
    
    # create a local context and define the properties belonging to it
    info = cs.setLocalContext("info")
    info.defineProperties(("name", 1), ("age", 1), ("graduated", 1))
    
    # create a local context and define the properties belonging to it
    actions = cs.setLocalContext("actions")
    actions.defineProperties(("holds", 0), ("uses", 0), ("talksTo", 0, "s"))
    
    # define the domain and the range of the properties
    Person.NAME = str
    Person.AGE = int
    Person.GRADUATED = bool
    Thing.ISLOCATED = Room
    Person.USES = ActiveObj
    Person.HOLDS = PassiveObj
    Person.TALKSTO = Person

##===============================================================================
## 
##===============================================================================

    # populate the semantic network with some data
    david.NAME = "David_Sorrentino"
    david.AGE = 27
    david.ISLOCATED = livingRoom
    
    marco.NAME = "Marco_Sorrentino"
    marco.AGE = 26
    marco.ISLOCATED = livingRoom
    
    andrea.NAME = "Andrea_Monacchi"
    
    bowl.ISLOCATED = livingRoom
    spoon.ISLOCATED = livingRoom
    television.ISLOCATED = livingRoom
    toaster.ISLOCATED = kitchen
    
    david.TALKSTO = marco
    david.HOLDS = spoon
    david.HOLDS = bowl
    david.USES = television
    andrea.TALKSTO = marco
    david.GRADUATED = True
    
##===============================================================================
## 
##===============================================================================

    # update the semantic network
#    del david.TALKSTO[marco]
#    del david.HOLDS
#    del david.USES[television]
#    david.ISLOCATED = kitchen
#    david.USES = toaster

##===============================================================================
## 
##===============================================================================
        
    cs.printContextsList()
    
    cs.launchServers()

    #serialize the graph as owl/rdf/xml and upload it on a FTP
    wr = Writer()
    wr.writeOntology(cs.serializeContext(), True)