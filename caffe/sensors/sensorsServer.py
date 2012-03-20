'''
Created on Mar 19, 2012

@author: david
'''

import SocketServer
from ..tools.exceptions import InputException

class SensorsServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    '''
    classdocs
    '''
    
    dataQueue = None

    def __init__(self, addr, handler, dq):
        SocketServer.TCPServer.__init__(self, addr, handler)
        self.dataQueue = dq
        

class SSHandler(SocketServer.BaseRequestHandler):
    '''
    classdocs
    '''    

    def handle(self):
        '''
        Handler
        '''
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print ("SENSORS_SERVER: got data from the client @ %s" % (self.client_address[0]))
        try:
            self.server.dataQueue.put(self.data)
        except InputException as e:
            print e
        self.request.sendall("")