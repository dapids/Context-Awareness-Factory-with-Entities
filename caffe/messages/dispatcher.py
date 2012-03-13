'''
Created on Mar 13, 2012

@author: david
'''

class Dispatcher(object):
    """
    An object that can dispatch events to a privately managed group of
    subscribers.
    """


    __eventsMap = None


    def set_map(self, amap):
        self.__eventsMap = amap


    def get_map(self):
        return self.__eventsMap


    def subscribe(self, event, handler):
        """ Subscribe the given handler to an event. Handlers are called in the order they are subscribed. """
        if self.__eventsMap is None:
            self.set_map({})
        lst = self.__eventsMap.get(event, None)
        if lst is None:
            lst = [handler]
        else:
            lst.append(handler)
        self.__eventsMap[event] = lst
        
        
    def dispatch(self, event):
        """ Dispatch the given event to the subscribed handlers for the event's type"""
        if self.__eventsMap is not None:
            lst = self.__eventsMap.get(event.getSubject(), None)
            if lst is None:
                raise ValueError("Unknown event: %s" % event.getSubject())
            for l in lst:
                l(event)