'''
Created on Mar 13, 2012

@author: david
'''

from threading import Thread
import re
from .event import AddEvent, DelEvent
from ..tools.exceptions import InputException

class EventGenerator(object):
    '''
    classdocs
    '''

    
    __dispatcher = None
    __dataQueue = None
    __registeredIndividuals = None
    

    def __init__(self, disp, dq, nThreads, ri):
        self.__dispatcher = disp
        self.__dataQueue = dq
        self.__registeredIndividuals = ri
        for i in range(nThreads): #@UnusedVariable
            t = Thread(target=self.__manageEvent)
            t.daemon = True
            t.start()

    
    def __manageEvent(self):
        while True:
            data = self.__dataQueue.get()
            try:
                self.__checkData(data)
            except InputException as e:
                print e
            self.__dataQueue.task_done()
    
    
    def __checkData(self, data):
        if re.match("^\s*(del\s+){0,1}\w+\s+\w+(\s+\w+){0,1};\s*$", data):
            try:
                (n, s, p, o) = data.split(" ") #@UnusedVariable
                self.__genDelEvent(self.__getSPO(s, p, o))
            except ValueError:
                prop = data.split(" ")
                if prop[0] == "del":
                    s, p = prop[1], prop[2]
                    self.__genDelEvent(self.__getSPO(s, p))
                else:
                    s, p, o = prop[0], prop[1], prop[2]
                    self.__genAddEvent(self.__getSPO(s, p, o))
                    
        else:
            raise InputException("Input allowed: '[not] subject predicate object;'")
        
    
    def __getSPO(self, s, p, o=None):
        try:
            s = self.__registeredIndividuals[s]
        except KeyError:
            raise InputException("The individual '%s' has not been defined yet." % s)
        p = p.upper()
        if o is not None:
            o = o[0:o.find(";")]
            try:
                o = self.__registeredIndividuals[o]
            except KeyError:
                try:
                    o = int(o)
                except ValueError:
                    try:
                        o = float(o)
                    except ValueError:
                        if o.lower() == "true":
                            o = True
                        elif o.lower() == "false":
                            o = False
        else:
            p = p[0:p.find(";")]
        return (s, p, o)
        
    
    def __genDelEvent(self, data):
        self.__dispatcher.dispatch(DelEvent(data))
       
        
    def __genAddEvent(self, data):
        self.__dispatcher.dispatch(AddEvent(data))
