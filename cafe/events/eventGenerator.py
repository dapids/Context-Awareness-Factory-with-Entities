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
    Checks input data and generates events related to them.
    '''

    
    __dispatcher = None
    __dataQueue = None
    __registeredIndividuals = None
    

    def __init__(self, disp, dq, nThreads, ri):
        """
        @type disp: Dispatcher
        @param disp: a dispatcher triggering events
        @type dq: Queue
        @param dq: a queue of input data to check
        @type nThreads: int
        @param nThreads: number of threads to check input data and generate events
        """
        self.__dispatcher = disp
        self.__dataQueue = dq
        self.__registeredIndividuals = ri
        for i in range(nThreads): #@UnusedVariable
            t = Thread(target=self.__manageEvent)
            t.daemon = True
            t.start()

    
    def __manageEvent(self):
        """
        Executes the procedure to generate an event related to the input.
        """
        while True:
            data = self.__dataQueue.get()
            try:
                genEvent = self.__checkData(data)
                s, p, o = genEvent[1]
                genEvent[0](self.__getSPO(s, p, o))
            except InputException as e:
                print e
            self.__dataQueue.task_done()
    
    
    def __checkData(self, data):
        """
        Checks the data taken in input and, if they are valid, returns the methods invoke in order to generate the proper events. 
        @type data: str
        @param data: input data from sensors
        @return: a tuple containing the method to call in order to generate the event and its parameters
        """
        result = None, None
        if re.match("^\s*(del\s+){0,1}\w+\s+\w+(\s+\w+){0,1};\s*$", data):
            try:
                (n, s, p, o) = data.split(" ") #@UnusedVariable
                result = self.__genDelEvent, (s, p, o)
#                self.__genDelEvent(self.__getSPO(s, p, o))
            except ValueError:
                prop = data.split(" ")
                if prop[0] == "del":
                    s, p = prop[1], prop[2]
                    result = self.__genDelEvent, (s, p, None)
#                    self.__genDelEvent(self.__getSPO(s, p))
                else:
                    s, p, o = prop[0], prop[1], prop[2]
#                    self.__genAddEvent(self.__getSPO(s, p, o))
                    result = self.__genAddEvent, (s, p, o)
        else:
            raise InputException("Input allowed: '[del] subject predicate object;'")
        return result
    
    
    def __getSPO(self, s, p, o):
        """
        Takes a proposition of elements of type str and returns a proposition of elements of proper types.
        @type s: str
        @param s: the subject of the proposition
        @type p: str 
        @param p: the predicate of the proposition
        @type o: str
        @param o: the object of the proposition
        @return: a tuple containing the proposition, after giving subject, predicate and object the proper types 
        """
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
        """
        Generates a DelEvent.
        @type data: tuple
        @param data: the proposition representing the data to delete
        """
        try:
            self.__dispatcher.dispatch(DelEvent(data))
        except ValueError as e:
            print e
       
        
    def __genAddEvent(self, data):
        """
        Generates an AddEvent.
        @type data: tuple
        @param data: the proposition representing the data to insert
        """
        try:
            self.__dispatcher.dispatch(AddEvent(data))
        except ValueError as e:
            print e
