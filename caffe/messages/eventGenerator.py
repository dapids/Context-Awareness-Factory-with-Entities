'''
Created on Mar 13, 2012

@author: david
'''

from threading import Thread
from .event import Event

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
            if self.__checkData(data):
                self.__genEvent(data)
            self.__dataQueue.task_done()
    
    
    def __checkData(self, data):
        return True
    
    def __genEvent(self, data):
        (s, p, o) = data.split(" ")
        s = self.__registeredIndividuals[s]
        p = p.upper()
        o = self.__registeredIndividuals[o]
        self.__dispatcher.dispatch(Event((s, p, o)))