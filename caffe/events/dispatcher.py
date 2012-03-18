'''
Created on Mar 13, 2012

@author: david
'''

class Dispatcher(object):
    """
    An object that can dispatch events to a privately managed group of subscribers.
    """


    __eventsMap = None


    def set_map(self, emap):
        """
        Sets the map of the subscribed objects
        @type emap: dict
        @param emap: the map of the subscribed objects
        """
        self.__eventsMap = emap


    def get_map(self):
        """
        @return: the map of the subscribed objects
        """
        return self.__eventsMap


    def subscribe(self, subscribed, handler):
        """
        @type subscribed: object
        @param subscribed: an object subscribed to the dispatcher
        @type handler: function
        @param handler: the method called when the event, in which the subscribed object is interested, is triggered
        Subscribes the given handler to an event. Handlers are called in the order they are subscribed.
        """
        if self.__eventsMap is None:
            self.set_map({})
        lst = self.__eventsMap.get(subscribed, None)
        if lst is None:
            lst = [handler]
        else:
            lst.append(handler)
        self.__eventsMap[subscribed] = lst
        
        
    def dispatch(self, event):
        """
        Dispatches the given event to the subscribed handlers for the event's type
        @type event: Event
        @param event: the event dispatched
        """
        if self.__eventsMap is not None:
            lst = self.__eventsMap.get(event.getSubject(), None)
            if lst is None:
                raise ValueError("WARNING. Unknown event: %s.\n" % event.getSubject())
            for l in lst:
                l(event)