'''
Created on Jan 17, 2012

@author: david
'''

from cafe.contextSpace import ContextSpace
from cafe.tools.utils import Utils

from environment.person import Person
from environment.room import Room
from environment.thing import Thing
from environment.adult import Adult
from environment.child import Child
from environment.elderly import Elderly
from environment.kitchenware import Kitchenware
from environment.appliance import Appliance
from environment.genericObject import GenericObject
from environment.object import Object

if __name__ == '__main__':

    # create the context space
    cs = ContextSpace("http://cafe.ns/home#")
    
    # create the individuals
    rose = cs.createEntity(Adult, "rose")
    marco = cs.createEntity(Adult, "marco")
    andrea = cs.createEntity(Adult, "andrea")
    kitchen = cs.createEntity(Room, "kitchen")
    livingRoom = cs.createEntity(Room, "livingRoom")
    bathroom = cs.createEntity(Room, "bathroom")
    bowl = cs.createEntity(Kitchenware, "bowl")
    spoon = cs.createEntity(Kitchenware, "spoon")
    bottle = cs.createEntity(Kitchenware, "bottle")
    broom = cs.createEntity(GenericObject, "broom")
    television = cs.createEntity(Appliance, "television")
    toaster = cs.createEntity(Appliance, "toaster")
    dishwasher = cs.createEntity(Appliance, "dishwasher")
    
    # create a local context and define the properties belonging to it
    locations = cs.setLocalContext("locations")
    locations.defineProperties(("isLocated", 1))
    
    # create a local context and define the properties belonging to it
    info = cs.setLocalContext("info")
    info.defineProperties(("name", 1), ("age", 1), ("description", 1), ("genre", 1), ("posture", 1),
                          ("celsiusTemp", 1), ("bloodPressure", 1), ("status", 1), ("roomTemperature", 1))
    
    # create a local context and define the properties belonging to it
    actions = cs.setLocalContext("actions")
    actions.defineProperties(("holds", 0), ("uses", 0), ("talksTo", 0, "s"))
    
    # define the domain and the range of the properties
    Thing.ISLOCATED = Room
    Thing.ID = int
    Thing.NAME = str    
    
    Person.AGE = int
    Person.GENRE = str
    Person.POSTURE = str
    Person.CELSIUSTEMP = float
    Person.BLOODTEMP = str
    Person.USES = Appliance
    Person.HOLDS = Kitchenware
    Person.TALKSTO = Person
    
    Object.DESCRIPTION = str
    
    Room.ROOMTEMPERATURE = float
    
    Appliance.STATUS = str

##===============================================================================
## 
##===============================================================================

    # populate the semantic network with some data
    rose.NAME = "Rose_Brown"
    rose.AGE = 27
    rose.ISLOCATED = livingRoom
    
    marco.NAME = "Marco_Sorrentino"
    marco.AGE = 26
#    marco.ISLOCATED = livingRoom
    
    andrea.NAME = "Andrea_Monacchi"
    
    rose.TALKSTO = marco
    rose.HOLDS = spoon
    rose.HOLDS = bowl
    rose.USES = television
    television.ISLOCATED = livingRoom
    andrea.TALKSTO = marco
    
    spoon.ISLOCATED = kitchen
    
    broom.ISLOCATED = bathroom
    
    kitchen.NAME = "Kitchen"
    livingRoom.NAME = "Living Room"
    bathroom.NAME = "Bathroom"
    
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

    #cs.saveContext("/home/david/myContext")
    #print Utils.loadContext("/home/david/myContext")

    #serialize the graph as owl/rdf/xml and upload it on a FTP
    cs.writeOntology(cs.serializeContext(), True)